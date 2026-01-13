import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------
# Page config
# ------------------------
st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

st.markdown("""
    <style>
    .block-container {padding-top: 1rem;}
    </style>
""", unsafe_allow_html=True)

# ------------------------
# Load dataset
# ------------------------
df = pd.read_csv("data/ecommerce_sales.csv")
df['order_date'] = pd.to_datetime(df['order_date'])
all_categories = df['product_category'].unique().tolist()

# ------------------------
# Sidebar filter (compact)
# ------------------------
st.sidebar.markdown("### 🛍️  Product Category")
selected_category = st.sidebar.radio("", ["All"] + all_categories)

filtered_df = df.copy()
if selected_category != "All":
    filtered_df = df[df['product_category'] == selected_category]

# ------------------------
# Proper full title (fixed)
# ------------------------
st.markdown(
    """
    <div style="background:linear-gradient(90deg,#4B0082,#6A5ACD);
                padding:16px;border-radius:14px;margin-bottom:12px">
        <h2 style="color:white;text-align:center;margin:0;">
        🛒 E-commerce Sales Dashboard
        </h2>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------
# Prepare data
# ------------------------
filtered_df['month'] = filtered_df['order_date'].dt.to_period('M').astype(str)

monthly_sales = filtered_df.groupby('month')['sales'].sum().reset_index()

sales_by_cat = df.groupby('product_category')['sales'].sum().reindex(all_categories, fill_value=0).reset_index()

profit_by_cat = df.groupby('product_category')['profit'].sum().reindex(all_categories, fill_value=0).reset_index()

top_products = filtered_df.groupby('product_id')['sales'].sum().sort_values(ascending=False).head(10).reset_index()

config_no_bar = {'displayModeBar': False}

# ------------------------
# Layout → 4 charts side by side
# ------------------------
c1, c2, c3, c4 = st.columns(4, gap="small")

# ------------------------
# 1. Monthly Sales
# ------------------------
fig1 = px.line(monthly_sales, x="month", y="sales", markers=True,
               title="📈 Monthly Sales")
fig1.update_layout(height=340, margin=dict(l=5,r=5,t=40,b=5),
                   plot_bgcolor="white", paper_bgcolor="white",
                   showlegend=False)
c1.plotly_chart(fig1, use_container_width=True, config=config_no_bar)

# ------------------------
# 2. Sales by Category (GREEN highlight)
# ------------------------

base_color = "#4e79a7"   # default blue
highlight_color = "#FFA500"  # orange

bar_colors = []
for cat in sales_by_cat["product_category"]:
    if selected_category != "All" and cat == selected_category:
        bar_colors.append(highlight_color)
    else:
        bar_colors.append(base_color)

fig2 = px.bar(
    sales_by_cat,
    x="product_category",
    y="sales",
    title="📊 Sales by Category"
)

fig2.update_traces(marker_color=bar_colors)

fig2.update_layout(
    height=340,
    margin=dict(l=5, r=5, t=40, b=5),
    plot_bgcolor="white",
    paper_bgcolor="white",
    showlegend=False
)

c2.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

# ------------------------
# 3. Profit Contribution Pie
# ------------------------
fig3 = px.pie(
    profit_by_cat, names="product_category", values="profit",
    title="💹 Profit Contribution",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig3.update_traces(textinfo="percent")
fig3.update_layout(height=340, margin=dict(l=5,r=5,t=40,b=5),
                   showlegend=False)
c3.plotly_chart(fig3, use_container_width=True, config=config_no_bar)

# ------------------------
# 4. Top 10 Products
# ------------------------
fig4 = px.bar(
    top_products, x="product_id", y="sales",
    title="🏆 Top 10 Products",
    color_discrete_sequence=["#32CD32"]
)
fig4.update_layout(height=340, margin=dict(l=5,r=5,t=40,b=5),
                   plot_bgcolor="white", paper_bgcolor="white",
                   showlegend=False)
c4.plotly_chart(fig4, use_container_width=True, config=config_no_bar)











  
















































