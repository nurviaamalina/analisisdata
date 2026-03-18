import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Olist Dashboard", layout="wide")

# -------------------------
# Load Dataset
# -------------------------
@st.cache_data
def load_data():
    # Load Orders dengan parse tanggal
    orders_df = pd.read_csv("data/olist_orders_dataset.csv", 
                            parse_dates=['order_purchase_timestamp', 
                                         'order_approved_at', 
                                         'order_delivered_carrier_date', 
                                         'order_delivered_customer_date', 
                                         'order_estimated_delivery_date'])
    
    # Load Order Items
    order_items_df = pd.read_csv("data/olist_order_items_dataset.csv")
    
    # Load Products
    products_df = pd.read_csv("data/olist_products_dataset.csv")
    
    # Merge order_items dengan products untuk kategori
    merged_df = pd.merge(order_items_df, 
                         products_df[['product_id','product_category_name']],
                         on='product_id', how='left')
    
    return orders_df, order_items_df, products_df, merged_df

# Load data
orders_df, order_items_df, products_df, merged_df = load_data()

# -------------------------
# Dashboard
# -------------------------
st.title("📊 Olist E-commerce Dashboard")

# -------------------------
# Tabel Data Mentah
# -------------------------
st.header("Preview Data")
st.subheader("Orders")
st.dataframe(orders_df.head(10))

st.subheader("Order Items")
st.dataframe(order_items_df.head(10))

st.subheader("Products")
st.dataframe(products_df.head(10))

# -------------------------
# 1. Kategori Produk Terlaris
# -------------------------
st.header("Top 10 Kategori Produk Terlaris")
kategori_count = merged_df['product_category_name'].value_counts().head(10)

fig, ax = plt.subplots(figsize=(7,4))
sns.barplot(x=kategori_count.values, y=kategori_count.index, palette='viridis', ax=ax)
ax.set_xlabel("Jumlah Penjualan")
ax.set_ylabel("Kategori Produk")
st.pyplot(fig)

# -------------------------
# 2. Distribusi Jumlah Produk per Pesanan
# -------------------------
st.header("Distribusi Jumlah Produk per Pesanan")
produk_per_order = merged_df.groupby('order_id')['product_id'].count()

fig, ax = plt.subplots(figsize=(7,4))
sns.histplot(produk_per_order, bins=20, kde=False, color='skyblue', ax=ax)
ax.set_xlim(0, 10)
ax.set_xlabel("Jumlah Produk per Pesanan")
ax.set_ylabel("Jumlah Pesanan")
st.pyplot(fig)

st.write(f"Rata-rata jumlah produk per pesanan: **{produk_per_order.mean():.2f}**")

# -------------------------
# 3. Trend Penjualan Bulanan
# -------------------------
st.header("Trend Jumlah Pesanan per Bulan")
orders_df['month'] = orders_df['order_purchase_timestamp'].dt.to_period('M')
trend_bulanan = orders_df.groupby('month').size()

fig, ax = plt.subplots(figsize=(8,3))
trend_bulanan.plot(marker='o', ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Pesanan")
plt.xticks(rotation=45)
st.pyplot(fig)