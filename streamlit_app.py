import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, due on Oct 6th.")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('ME')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='ME')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
st.write("## Your additions")

# --------------------------------------------------
# (1) CATEGORY DROPDOWN
# --------------------------------------------------

st.write("### (1) Select a Category")

categories = sorted(df["Category"].unique())

category = st.selectbox(
    "Select a Category",
    categories
)


# --------------------------------------------------
# (2) SUB-CATEGORY MULTI-SELECT
# --------------------------------------------------

st.write("### (2) Select Sub-Categories")

category_data = df[df["Category"] == category]

subcategories = sorted(
    category_data["Sub_Category"].unique()
)

selected_subcategories = st.multiselect(
    "Select Sub-Categories",
    subcategories,
    default=subcategories
)


# --------------------------------------------------
# FILTER THE DATA
# --------------------------------------------------

filtered_data = df[
    (df["Category"] == category) &
    (df["Sub_Category"].isin(selected_subcategories))
]


# --------------------------------------------------
# (3) LINE CHART OF SALES
# --------------------------------------------------

st.write("### (3) Sales for Selected Sub-Categories")

if len(selected_subcategories) > 0:

    sales_by_month_subcategory = (
        filtered_data
        .groupby([
            pd.Grouper(freq="ME"),
            "Sub_Category"
        ])["Sales"]
        .sum()
        .reset_index()
    )

    sales_chart = sales_by_month_subcategory.pivot(
        index="Order_Date",
        columns="Sub_Category",
        values="Sales"
    )

    st.line_chart(sales_chart)

else:

    st.write("Please select at least one Sub-Category.")


# --------------------------------------------------
# (4) CALCULATE THE THREE METRICS
# --------------------------------------------------

st.write("### (4) Selected Product Metrics")

# Calculate total sales
total_sales = filtered_data["Sales"].sum()

# Calculate total profit
total_profit = filtered_data["Profit"].sum()

# Calculate profit margin
if total_sales != 0:
    profit_margin = (total_profit / total_sales) * 100
else:
    profit_margin = 0


# --------------------------------------------------
# (5) CALCULATE OVERALL PROFIT MARGIN
# --------------------------------------------------

# Calculate total sales for the entire dataset
overall_sales = df["Sales"].sum()

# Calculate total profit for the entire dataset
overall_profit = df["Profit"].sum()

# Calculate overall profit margin
if overall_sales != 0:
    overall_profit_margin = (
        overall_profit / overall_sales
    ) * 100
else:
    overall_profit_margin = 0


# Calculate the difference between the selected
# profit margin and the overall profit margin
margin_difference = (
    profit_margin - overall_profit_margin
)


# --------------------------------------------------
# DISPLAY THE THREE METRICS
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Sales",
    f"${total_sales:,.2f}"
)

col2.metric(
    "Total Profit",
    f"${total_profit:,.2f}"
)

col3.metric(
    "Profit Margin",
    f"{profit_margin:.2f}%",
    f"{margin_difference:+.2f}%"
)