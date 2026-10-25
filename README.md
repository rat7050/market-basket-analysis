# 🛒 Market Basket Analysis

### Discover what customers buy together—and turn patterns into smarter cross-selling ideas.

<p align="center">
  <a href="https://market-basket-analysis-aboauko8fcxerqebbpwfxl.streamlit.app/">
    <img src="https://img.shields.io/badge/🚀%20Live%20Demo-Open%20Dashboard-ff4b4b?style=for-the-badge&logo=streamlit" alt="Open live dashboard">
  </a>
  <a href="https://github.com/rat7050/market-basket-analysis">
    <img src="https://img.shields.io/badge/GitHub-Source%20Code-181717?style=for-the-badge&logo=github" alt="GitHub repository">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-ff4b4b?style=flat-square&logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/Algorithm-Apriori-orange?style=flat-square" alt="Apriori">
  <img src="https://img.shields.io/badge/Analytics-Association%20Rules-purple?style=flat-square" alt="Association rules">
</p>

Market Basket Analysis is a data analytics project that explores product combinations within retail transactions. It uses the **Apriori algorithm** and **association rule mining** to find frequently purchased items, evaluate product relationships, and generate practical cross-selling ideas.

The project includes an interactive Streamlit dashboard, a Jupyter Notebook for exploration, and downloadable CSV results.

---

## 🌐 Live Demo

**[Launch the Market Basket Analysis Dashboard](https://market-basket-analysis-aboauko8fcxerqebbpwfxl.streamlit.app/)**

Explore the dashboard, adjust analysis thresholds, inspect frequent itemsets and association rules, and download results for further review.

---

## 📸 Dashboard Screenshots

> **Add a screenshot of the live app:** capture the dashboard in your browser, then upload it to the repository at `assets/dashboard-overview.png`. The image below will appear once that file exists.

<p align="center">
  <img src="assets/dashboard-overview.png" alt="Market Basket Analysis Streamlit dashboard overview" width="95%">
</p>

<p align="center"><i>Dashboard overview — replace this placeholder with a screenshot of the running app.</i></p>

### More visual examples

After uploading screenshots using the filenames below, these previews will render in GitHub:

<table>
  <tr>
    <td align="center" width="50%">
      <img src="assets/top-products.png" alt="Top products chart" width="100%">
      <br><b>Top Products</b>
    </td>
    <td align="center" width="50%">
      <img src="assets/association-rules.png" alt="Association rules table and chart" width="100%">
      <br><b>Association Rules</b>
    </td>
  </tr>
  <tr>
    <td align="center" width="50%">
      <img src="assets/frequent-itemsets.png" alt="Frequent itemsets table" width="100%">
      <br><b>Frequent Itemsets</b>
    </td>
    <td align="center" width="50%">
      <img src="assets/cross-selling.png" alt="Cross-selling recommendations" width="100%">
      <br><b>Cross-Selling Ideas</b>
    </td>
  </tr>
</table>

*The repository contains analysis outputs and a precomputed cross-selling CSV; the screenshot files above are placeholders for UI captures, not existing images.*

---

## 🎯 Business Problem

Retailers often want to understand which products tend to appear in the same order. These patterns can help teams explore product bundling, related-product recommendations, promotions, and store layout ideas.

This project uses historical transaction data to answer questions such as:

- Which products or combinations frequently appear in the same basket?
- When a basket contains one item, which other items are associated with it?
- How strong are the discovered relationships?
- Which product relationships may be worth testing as cross-selling opportunities?

Association rules describe relationships in the observed data. They do **not** prove that one product purchase causes another.

## ✨ Key Features

- **Retail data cleaning** — removes cancelled invoices, missing values, invalid purchase lines, and duplicate rows.
- **Interactive dashboard** — explore the analysis through Streamlit tabs.
- **Country filtering** — focus analysis on one country or all available countries.
- **Adjustable thresholds** — configure minimum support, confidence, and lift.
- **Frequent itemsets** — find combinations that appear together across transactions.
- **Association rules** — review antecedents, consequents, support, confidence, and lift.
- **Visual analytics** — inspect top products, country-level transactions, itemsets, and rule relationships.
- **Cross-selling recommendations** — explore related-product ideas ranked by association strength.
- **CSV downloads** — export frequent itemsets, association rules, and cross-selling suggestions.
- **Jupyter Notebook** — follow the workflow and understand the analysis step by step.

## 🧭 How It Works

```text
Online Retail Transactions
           │
           ▼
   Data Cleaning & Filtering
           │
           ▼
   Group Products by Invoice
           │
           ▼
     Basket / Item Matrix
           │
           ▼
    Apriori Frequent Itemsets
           │
           ▼
      Association Rules
           │
           ▼
 Support • Confidence • Lift
           │
           ▼
 Streamlit Dashboard & CSV Exports
           │
           ▼
 Cross-Selling Ideas to Test
```

## 📊 Dataset

This project uses the **Online Retail** dataset from the UCI Machine Learning Repository.

- **Dataset page:** [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)
- **Local file expected:** `data/Online Retail.xlsx`
- **Time period:** December 2010 to December 2011
- **Domain:** Online retail transactions

The data includes fields such as invoice number, product description, quantity, unit price, and country. The dashboard uses positive purchase quantities and prices for this basket analysis.

**Dataset attribution:** Chen, D. (2012). *Online Retail* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33

## 📐 Understanding the Metrics

| Metric | What it tells you | How to interpret it |
|---|---|---|
| **Support** | How often an itemset appears across all baskets | Higher support means the combination occurs more frequently |
| **Confidence** | How often the consequent appears when the antecedent appears | Higher confidence means the rule is more reliable within the observed data |
| **Lift** | How much more often the items occur together than expected from the consequent's baseline frequency | Lift > 1 indicates a positive association; around 1 suggests little association; below 1 suggests a negative association |

For example, a rule `A → B` asks how often product B appears in baskets that contain product A. It does not mean buying A causes a customer to buy B.

## 🧰 Tech Stack

| Tool | Purpose |
|---|---|
| Python | Project implementation |
| Pandas | Data cleaning, transformation, and tabular analysis |
| NumPy | Numerical operations |
| MLxtend | Apriori algorithm and association rule mining |
| Streamlit | Interactive application |
| Matplotlib & Seaborn | Charts and visual analytics |
| Jupyter Notebook | Exploratory analysis and documentation |
| OpenPyXL | Reading the Excel dataset |

## 📁 Project Structure

```text
market-basket-analysis/
├── app.py
├── market_basket_analysis.ipynb
├── cross_selling_recommendations.csv
├── requirements.txt
├── data/
│   └── Online Retail.xlsx
└── README.md
```

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/rat7050/market-basket-analysis.git
cd market-basket-analysis
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Check the dataset

Confirm that the Excel dataset is available at:

```text
data/Online Retail.xlsx
```

If needed, download it from the [official UCI dataset page](https://archive.ics.uci.edu/dataset/352/online+retail) and place it in the `data` folder.

### 5. Launch the dashboard

```bash
streamlit run app.py
```

Open the local URL printed in the terminal, usually `http://localhost:8501`.

### 6. Run the notebook

```bash
jupyter notebook
```

Open `market_basket_analysis.ipynb` and run its cells from top to bottom.

## 🔎 How to Use the Dashboard

1. Open the [live dashboard](https://market-basket-analysis-aboauko8fcxerqebbpwfxl.streamlit.app/) or run the app locally.
2. Choose a country, or leave the selection on all countries.
3. Adjust minimum support, confidence, and lift in the sidebar.
4. Review the **Overview** tab for top products and transaction patterns.
5. Explore **Frequent Itemsets** to find common product combinations.
6. Inspect **Association Rules** to compare confidence and lift.
7. Use **Cross-Selling** for potential recommendations.
8. Download the resulting CSV files for further analysis.

Lower support thresholds may reveal more combinations but can increase computation time and produce less common patterns. Increase thresholds to focus on more frequent associations.

## 💼 Potential Business Applications

- **Product recommendations:** suggest related items on product pages.
- **Bundle experiments:** test offers for products that often appear together.
- **Merchandising:** explore whether associated items should be displayed nearby.
- **Promotion planning:** develop hypotheses for targeted campaigns.
- **Inventory coordination:** check availability before promoting related items.

These are ideas to validate through business experiments. Association metrics alone do not guarantee increased revenue or profit.

## ⚠️ Data & Methodology Notes

- Invoice numbers beginning with `C` are treated as cancellations and excluded.
- Rows with missing invoice numbers, descriptions, quantities, or unit prices are removed.
- Non-positive quantities and unit prices are excluded.
- Duplicate rows are removed.
- Each product is counted once per invoice for basket presence; quantity does not multiply product presence.
- Apriori may become slow with low support thresholds or many distinct products. Start with a sensible threshold, such as 0.02, and adjust carefully.
- Recorded sales value is not the same as profit.
- Association does not prove causation.

## 🚀 Future Improvements

- Add product-level filters and date-range analysis.
- Compare product associations across customer segments and time periods.
- Evaluate recommendations using an A/B test or other business validation.
- Add a product search field for finding rules related to a selected item.
- Improve performance for larger transaction datasets.
- Add repeatable automated tests and continuous integration.
- Include actual dashboard screenshots in the repository.

## 👨‍💻 Author

**Ratnesh Kumar**

- **GitHub:** [@rat7050](https://github.com/rat7050)
- **Project repository:** [Market Basket Analysis](https://github.com/rat7050/market-basket-analysis)
- **Live application:** [Open Streamlit Dashboard](https://market-basket-analysis-aboauko8fcxerqebbpwfxl.streamlit.app/)

---

<p align="center">
  <b>Built with Python, Pandas, MLxtend, and Streamlit.</b>
</p>
