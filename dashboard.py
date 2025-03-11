import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title='E-Commerce Dashboard',
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Load dataset
merged_df = pd.read_csv('E_Commerce_Dataset/merged_df.csv')

# Title
st.title('E-Commerce Dashboard')

# Subheader: Overview Section
st.markdown("""
    Dashboard ini memberikan berbagai informasi penting mengenai penjualan, jenis pembayaran, performa pengiriman, serta analisis terkait proses bisnis E-Commerce.
    visualisasi akan memberikan gambaran mengenai performa e-commerce berdasarkan data yang tersedia.
""")

# First Graph: Top Product Sales, Second Graph: Most Used Payment Types, Third Graph: Delivery Performance vs Review Score
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader('Top Product Sales')
    top_product = merged_df.groupby('product_category_name', as_index=False).agg({
        'order_id': 'nunique',
        'price': 'sum',
    }).sort_values(by=['order_id'], ascending=False).head().reset_index(drop=True)

    product_fig = px.bar(top_product, x='product_category_name', y='order_id')
    product_fig.update_xaxes(title_text='')  # Remove x-axis title
    st.plotly_chart(product_fig, use_container_width=True)

with col2:
    st.subheader('Most Used Payment Types')
    most_used_payment = merged_df.groupby('payment_type', as_index=False).agg({
        'order_id': 'nunique',
        'payment_value': 'sum',
        'payment_installments': 'mean'
    }).sort_values(by='order_id', ascending=False).reset_index(drop=True)

    payment_fig = px.bar(most_used_payment , x='payment_type', y='payment_value')
    payment_fig.update_xaxes(title_text='')  # Remove x-axis title
    st.plotly_chart(payment_fig, use_container_width=True)

with col3:
    st.subheader('Delivery Performance vs Review Score')
    ma = pd.crosstab(merged_df['delivery_performance'], merged_df['review_score']).reset_index()
    ma_melted = pd.melt(ma, id_vars='delivery_performance', var_name='score', value_name='count')

    fig = px.bar(ma_melted, x='delivery_performance', y='count', color='score')
    fig.update_xaxes(title_text='')  # Remove x-axis title
    st.plotly_chart(fig, use_container_width=True)

# Fourth Graph: Freight Analysis (Weight vs Freight & Volume vs Freight)
st.subheader('Freight Analysis: Weight vs Freight and Volume vs Freight')
fig = make_subplots(rows=1, cols=2)

fig.add_trace(
    go.Scatter(x=merged_df['freight_value'], y=merged_df['product_weight'], mode='markers', name='Weight vs Freight'),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(x=merged_df['freight_value'], y=merged_df['volume_product'], mode='markers', name='Volume vs Freight'),
    row=1, col=2
)

fig.update_layout(height=600, width=1000)
st.plotly_chart(fig, use_container_width=True)

# Fifth Graph: Seller vs Consumer
st.subheader('Top 10 Seller States and Consumer Data')
seller_consumer = merged_df.groupby('seller_state', as_index=False).agg({
    'seller_id': 'nunique',
    'customer_unique_id': 'nunique'
}).sort_values(by='customer_unique_id', ascending=False).head(10).reset_index(drop=True)

fig_1 = go.Figure(data=[go.Table(
    header=dict(values=list(seller_consumer.columns),
                fill_color='paleturquoise',
                align='center'),
    cells=dict(values=[seller_consumer.seller_state, seller_consumer.seller_id, seller_consumer.customer_unique_id],
               fill_color='lavender',
               align='center'))])

fig_1.update_layout(width=800)
st.plotly_chart(fig_1, use_container_width=True)
