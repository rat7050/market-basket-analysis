# Market Basket Analysis

Discover which products customers frequently buy together using the UCI Online Retail dataset, the Apriori algorithm, and association rules.

## Features
- Cleans retail invoice lines and excludes cancelled invoices
- Finds frequent product itemsets with Apriori
- Calculates support, confidence, and lift
- Interactive Streamlit dashboard with filters
- Exports association rules and cross-selling suggestions to CSV
- Jupyter Notebook for learning and explaining the workflow

## Dataset
Download **Online Retail.xlsx** from the [official UCI dataset page](https://archive.ics.uci.edu/dataset/352/online+retail) and put it in the `data/` folder.

The dataset contains UK online retailer transactions from December 2010 to December 2011. Please credit the UCI Machine Learning Repository when sharing this project.

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run the notebook
```powershell
jupyter notebook
```
Open `market_basket_analysis.ipynb` and run cells from top to bottom.

## Run the dashboard
```powershell
streamlit run app.py
```

## Metrics
- **Support**: fraction of baskets containing the itemset.
- **Confidence**: fraction of baskets with the antecedent that also contain the consequent.
- **Lift**: confidence divided by the consequent's overall support. Lift > 1 indicates a positive association.

## Important notes
- Invoice numbers beginning with `C` indicate cancellations and are excluded.
- Returns/negative quantities and non-positive prices are excluded from this basket analysis.
- Each product is counted once per invoice; quantity is not used to multiply product presence.
- Apriori can be slow when support is very low or many unique products are included. Start with minimum support around 0.02, then reduce carefully.
- Association does not prove causation.

## Citation
Chen, D. (2012). *Online Retail* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33
