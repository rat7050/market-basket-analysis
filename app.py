
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Market Basket Analysis",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Market Basket Analysis")
st.markdown(
    """
    Discover which products customers frequently purchase together
    using the **Apriori algorithm** and association rule mining.
    """
)

# =========================================================
# 2. LOAD DATASET
# =========================================================

DATA_PATH = Path("data/Online Retail.xlsx")


@st.cache_data(show_spinner="Loading retail dataset...")
def load_data(file_path):
    return pd.read_excel(file_path)


if not DATA_PATH.exists():
    st.error(
        "Dataset not found. Place Online Retail.xlsx inside the data folder."
    )
    st.code(
        "market-basket-analysis/\n"
        "├── app.py\n"
        "└── data/\n"
        "    └── Online Retail.xlsx"
    )
    st.markdown(
        "[Download the official UCI dataset]"
        "(https://archive.ics.uci.edu/dataset/352/online+retail)"
    )
    st.stop()

try:
    df_raw = load_data(str(DATA_PATH))
except Exception as error:
    st.error(f"Could not load the Excel dataset: {error}")
    st.stop()

required_columns = {
    "InvoiceNo", "Description", "Quantity", "UnitPrice"
}

missing_columns = required_columns - set(df_raw.columns)

if missing_columns:
    st.error(f"Missing columns: {', '.join(sorted(missing_columns))}")
    st.stop()

# =========================================================
# 3. DATA CLEANING
# =========================================================

df = df_raw.copy()

df["InvoiceNo"] = df["InvoiceNo"].astype("string").str.strip()
df["Description"] = df["Description"].astype("string").str.strip()
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

# Remove cancelled invoices
df = df[
    ~df["InvoiceNo"].str.upper().str.startswith("C", na=False)
].copy()

# Remove missing values and invalid purchase lines
df = df.dropna(
    subset=["InvoiceNo", "Description", "Quantity", "UnitPrice"]
)

df = df[
    (df["Description"] != "")
    & (df["Quantity"] > 0)
    & (df["UnitPrice"] > 0)
]

df = df.drop_duplicates()

# =========================================================
# 4. SIDEBAR FILTERS
# =========================================================

st.sidebar.header("⚙️ Analysis Settings")

if "Country" in df.columns:
    countries = sorted(df["Country"].dropna().unique().tolist())

    selected_country = st.sidebar.selectbox(
        "Select Country",
        ["All countries"] + countries
    )
else:
    selected_country = "All countries"

min_support = st.sidebar.slider(
    "Minimum Support",
    min_value=0.005,
    max_value=0.10,
    value=0.02,
    step=0.005,
    format="%.3f"
)

min_confidence = st.sidebar.slider(
    "Minimum Confidence",
    min_value=0.10,
    max_value=1.00,
    value=0.30,
    step=0.05,
    format="%.2f"
)

min_lift = st.sidebar.slider(
    "Minimum Lift",
    min_value=0.50,
    max_value=5.00,
    value=1.00,
    step=0.25,
    format="%.2f"
)

max_items = st.sidebar.selectbox(
    "Maximum products per itemset",
    [2, 3],
    index=0
)

# Apply country filter
if selected_country != "All countries" and "Country" in df.columns:
    df = df[df["Country"] == selected_country].copy()

if df.empty:
    st.warning("No records available for the selected country.")
    st.stop()

# =========================================================
# 5. DASHBOARD METRICS
# =========================================================

total_records = len(df)
total_transactions = df["InvoiceNo"].nunique()
total_products = df["Description"].nunique()

total_sales = (df["Quantity"] * df["UnitPrice"]).sum()

st.subheader("📊 Business Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Cleaned Records", f"{total_records:,}")
col2.metric("Transactions", f"{total_transactions:,}")
col3.metric("Unique Products", f"{total_products:,}")
col4.metric("Recorded Sales Value", f"£{total_sales:,.2f}")

st.caption(
    "Recorded sales value is calculated from positive quantities and prices "
    "in the cleaned data; it is not a profit calculation."
)

st.divider()

# =========================================================
# 6. TABS
# =========================================================

overview_tab, itemsets_tab, rules_tab, business_tab = st.tabs(
    [
        "📈 Overview",
        "🧺 Frequent Itemsets",
        "🔗 Association Rules",
        "💡 Cross-Selling"
    ]
)

# =========================================================
# 7. OVERVIEW TAB
# =========================================================

with overview_tab:
    st.subheader("Top 15 Products")

    top_products = df["Description"].value_counts().head(15)

    fig, ax = plt.subplots(figsize=(10, 6))

    top_products.sort_values().plot(
        kind="barh",
        ax=ax
    )

    ax.set_xlabel("Invoice lines")
    ax.set_ylabel("Product")
    ax.set_title("Most Frequently Appearing Products")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        "This chart measures invoice-line frequency, not total units sold."
    )

    if "Country" in df.columns and selected_country == "All countries":
        st.subheader("Transactions by Country")

        country_counts = (
            df.groupby("Country")["InvoiceNo"]
            .nunique()
            .sort_values(ascending=False)
            .head(10)
        )

        fig, ax = plt.subplots(figsize=(10, 5))
        country_counts.sort_values().plot(kind="barh", ax=ax)
        ax.set_xlabel("Unique invoices")
        ax.set_ylabel("Country")
        ax.set_title("Top 10 Countries by Transaction Count")

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

# =========================================================
# 8. CREATE TRANSACTIONS
# =========================================================

@st.cache_data(show_spinner=False)
def create_transactions(data):
    grouped = (
        data.groupby("InvoiceNo")["Description"]
        .apply(lambda products: sorted(set(products)))
    )

    return [
        basket for basket in grouped.tolist()
        if len(basket) >= 2
    ]


# =========================================================
# 9. APRIORI ANALYSIS
# =========================================================

@st.cache_data(show_spinner="Running Apriori. This may take a while...")
def run_analysis(
    transactions,
    support,
    confidence,
    lift_threshold,
    max_length
):
    if not transactions:
        return pd.DataFrame(), pd.DataFrame()

    encoder = TransactionEncoder()
    encoded_array = encoder.fit(transactions).transform(transactions)

    basket_matrix = pd.DataFrame(
        encoded_array,
        columns=encoder.columns_
    )

    frequent_itemsets = apriori(
        basket_matrix,
        min_support=support,
        use_colnames=True,
        max_len=max_length,
        low_memory=True
    )

    if frequent_itemsets.empty:
        return frequent_itemsets, pd.DataFrame()

    # Association rules require at least one frequent itemset of size 2.
    if not frequent_itemsets["itemsets"].map(len).ge(2).any():
        return frequent_itemsets, pd.DataFrame()

    rules = association_rules(
        frequent_itemsets,
        metric="confidence",
        min_threshold=confidence
    )

    if not rules.empty:
        rules = rules[rules["lift"] >= lift_threshold].copy()

        rules["antecedents_text"] = rules["antecedents"].apply(
            lambda items: ", ".join(sorted(items))
        )

        rules["consequents_text"] = rules["consequents"].apply(
            lambda items: ", ".join(sorted(items))
        )

        rules = rules.sort_values(
            ["lift", "confidence", "support"],
            ascending=False
        )

    return frequent_itemsets, rules


with st.spinner("Preparing baskets..."):
    transactions = create_transactions(df)

st.info(f"Transactions with at least two products: {len(transactions):,}")

with st.spinner("Analysing product associations..."):
    frequent_itemsets, rules = run_analysis(
        tuple(tuple(basket) for basket in transactions),
        min_support,
        min_confidence,
        min_lift,
        max_items
    )

# =========================================================
# 10. FREQUENT ITEMSETS TAB
# =========================================================

with itemsets_tab:
    st.subheader("Frequently Purchased Product Combinations")

    if frequent_itemsets.empty:
        st.warning(
            "No frequent itemsets found. Try lowering minimum support."
        )
    else:
        display_itemsets = frequent_itemsets.copy()

        display_itemsets["Products"] = display_itemsets["itemsets"].apply(
            lambda items: ", ".join(sorted(items))
        )

        display_itemsets = display_itemsets.rename(
            columns={"support": "Support"}
        )

        display_itemsets = display_itemsets.sort_values(
            "Support",
            ascending=False
        )

        st.dataframe(
            display_itemsets[["Products", "Support"]],
            use_container_width=True,
            hide_index=True
        )

        top_itemsets = display_itemsets.head(15).sort_values("Support")

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.barh(
            top_itemsets["Products"],
            top_itemsets["Support"]
        )

        ax.set_xlabel("Support")
        ax.set_ylabel("Product Combination")
        ax.set_title("Top Frequent Itemsets")

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        itemsets_csv = display_itemsets[
            ["Products", "Support"]
        ].to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Frequent Itemsets CSV",
            data=itemsets_csv,
            file_name="frequent_itemsets.csv",
            mime="text/csv"
        )

# =========================================================
# 11. ASSOCIATION RULES TAB
# =========================================================

with rules_tab:
    st.subheader("Product Association Rules")

    if rules.empty:
        st.warning(
            "No rules match these settings. Lower support, confidence, "
            "or lift, or select a different country."
        )
    else:
        rules_display = rules[
            [
                "antecedents_text",
                "consequents_text",
                "support",
                "confidence",
                "lift"
            ]
        ].copy()

        rules_display = rules_display.rename(
            columns={
                "antecedents_text": "If Customer Buys",
                "consequents_text": "Recommend",
                "support": "Support",
                "confidence": "Confidence",
                "lift": "Lift"
            }
        )

        st.dataframe(
            rules_display,
            use_container_width=True,
            hide_index=True
        )

        fig, ax = plt.subplots(figsize=(9, 5))

        sns.scatterplot(
            data=rules,
            x="support",
            y="confidence",
            hue="lift",
            size="lift",
            sizes=(40, 250),
            palette="viridis",
            ax=ax
        )

        ax.set_title("Support vs Confidence")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        rules_csv = rules_display.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Association Rules CSV",
            data=rules_csv,
            file_name="association_rules.csv",
            mime="text/csv"
        )

# =========================================================
# 12. CROSS-SELLING TAB
# =========================================================

with business_tab:
    st.subheader("Cross-Selling Recommendations")

    if rules.empty:
        st.info(
            "No recommendations available. Adjust the sidebar thresholds."
        )
    else:
        recommendations = rules[
            [
                "antecedents_text",
                "consequents_text",
                "support",
                "confidence",
                "lift"
            ]
        ].copy()

        recommendations = recommendations.rename(
            columns={
                "antecedents_text": "When Customer Buys",
                "consequents_text": "Recommend Product",
                "support": "Support",
                "confidence": "Confidence",
                "lift": "Lift"
            }
        )

        recommendations = recommendations.sort_values(
            ["Lift", "Confidence", "Support"],
            ascending=False
        )

        st.dataframe(
            recommendations.head(30),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### Business Strategies")

        st.markdown(
            """
            - **Product bundling:** test bundles for products often purchased together.
            - **Cross-selling:** recommend related products on product pages.
            - **Store layout:** consider placing associated products strategically.
            - **Targeted promotions:** test offers for promising product combinations.
            - **Inventory planning:** check stock availability before promoting items.
            """
        )

        st.caption(
            "Association does not prove causation. Test recommendations against "
            "actual sales and profit results before making business decisions."
        )

        rec_csv = recommendations.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Cross-Selling Recommendations",
            data=rec_csv,
            file_name="cross_selling_recommendations.csv",
            mime="text/csv"
        )

# =========================================================
# 13. DATA CLEANING DETAILS
# =========================================================

with st.expander("View Data Cleaning Details"):
    st.write("Original rows:", f"{len(df_raw):,}")
    st.write("Rows after cleaning and filters:", f"{len(df):,}")
    st.write("Rows excluded:", f"{len(df_raw) - len(df):,}")

    st.markdown(
        """
        Cleaning rules:
        - Removed cancelled invoices whose invoice numbers begin with C.
        - Removed missing invoice numbers, descriptions, quantities, and prices.
        - Removed non-positive quantities and unit prices.
        - Removed duplicate rows.
        - Counted each product once per invoice for association analysis.
        """
    )

st.divider()
st.caption(
    "Market Basket Analysis | Python • Pandas • MLxtend • Streamlit"
)
