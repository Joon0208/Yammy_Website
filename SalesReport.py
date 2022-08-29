import pandas as pd
import plotly.express as px
from bokeh.models.widgets import Div
import streamlit as st

EXAMPLE_NO = 1

st.set_page_config(page_title=" Yammy Sales Dashboard", page_icon=":bar_chart:", layout="wide")



if st.button('Go back Home'):
    js = "window.open('http://127.0.0.1:5000/')"  # New tab or window
    js = "window.location.href = 'http://127.0.0.1:5000/'"  # Current tab
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)

@st.cache
def get_data_from_excel():
    df = pd.read_csv("https://raw.githubusercontent.com/prrriyaaa/excel-2/main/Yammy_sales_dataset.csv"
    )
    # Add 'hour' column to dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M").dt.hour
    return df

df = get_data_from_excel()


st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the Region:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

df_selection = df.query(
    "City == @city & Customer_type ==@customer_type & Gender == @gender"
)


st.title(":bar_chart: Yammy Sales Dashboard")
st.markdown("##")


total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating =  int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")


sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)




qty_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Quantity"]].sort_values(by="Quantity")
)
fig_product_qty = px.bar(
    qty_by_product_line,
    x="Quantity",
    y=qty_by_product_line.index,
    orientation="h",
    title="<b>Order Quantity by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(qty_by_product_line),
    template="plotly_white",
)
fig_product_qty.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

right_column, bottom_column= st.columns(2)
right_column.plotly_chart(fig_product_sales, use_container_width=True)
bottom_column.plotly_chart(fig_product_qty, use_container_width=True)


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)