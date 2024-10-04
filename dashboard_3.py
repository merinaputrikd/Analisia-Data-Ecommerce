import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set page configuration as the first Streamlit command
st.set_page_config(layout="wide", page_title="E-commerce Data Analysis Dashboard")

# Load Data
@st.cache_data
def load_data():
    all_df = pd.read_csv("all_data_fix.csv")
    return all_df

all_df = load_data()

# Title of the Dashboard
def main():
    st.title("E-commerce Data Analysis Dashboard")

    # Sidebar for Navigation
    st.sidebar.title("Navigation")
    options = st.sidebar.radio("Select an option:", 
                                ["Overview", 
                                 "Best Selling Products", 
                                 "Customer Demographics", 
                                 "Buyer Satisfaction", 
                                 "Payment Installments", 
                                 "Payment Types"])

    # Overview Section
    if options == "Overview":
        st.subheader("Data Overview")
        st.write(all_df.head())
        st.write("Total Records: ", len(all_df))

    # Best Selling Products Section
    if options == "Best Selling Products":
        st.subheader("Best Selling Products by Customer State")

        # Filter product category
        product_category = st.selectbox("Select Product Category", all_df['product_category_name'].unique())
        
        filtered_df = all_df[all_df['product_category_name'] == product_category]
        top_selling_per_state_sorted = filtered_df.groupby(['customer_state', 'product_id']).size().reset_index(name='order_count')
        top_selling_per_state = top_selling_per_state_sorted.loc[top_selling_per_state_sorted.groupby('customer_state')['order_count'].idxmax()]

        plt.figure(figsize=(10, 6))
        sns.barplot(data=top_selling_per_state, x='order_count', y='customer_state', hue='product_id', palette="Set2")
        plt.title(f"Best Selling Products in {product_category}", fontsize=16)
        plt.xlabel("Order Count", fontsize=14)
        plt.ylabel("Customer State", fontsize=14)
        st.pyplot(plt)

    # Customer Demographics Section
    if options == "Customer Demographics":
        st.subheader("Customer Demographics by City")

        # Filter based on state and select top-N cities
        customer_state = st.selectbox("Select Customer State", all_df['customer_state'].unique())
        filtered_state_df = all_df[all_df['customer_state'] == customer_state]

        top_n = st.slider("Select Top N Cities", min_value=5, max_value=20, value=10)
        
        city_count = filtered_state_df['customer_city'].value_counts().head(top_n)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x=city_count.index, y=city_count.values, palette="coolwarm")
        plt.title(f"Top {top_n} Customer Cities in {customer_state}", fontsize=16)
        plt.xlabel("City", fontsize=14)
        plt.ylabel("Number of Customers", fontsize=14)
        plt.xticks(rotation=45, fontsize=12)
        st.pyplot(plt)

    # Buyer Satisfaction Section
    if options == "Buyer Satisfaction":
        st.subheader("Average Review Scores by Product Category")

        # Filter product categories by review score
        min_review_score = st.slider("Select Minimum Average Review Score", min_value=1.0, max_value=5.0, value=3.0, step=0.1)
        
        avg_review_score = all_df.groupby('product_category_name')['review_score'].mean().reset_index()
        filtered_review_score = avg_review_score[avg_review_score['review_score'] >= min_review_score]

        top_n_categories = st.slider("Select Top N Categories", min_value=5, max_value=20, value=10)
        top_10_categories = filtered_review_score.sort_values(by='review_score', ascending=False).head(top_n_categories)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x='review_score', y='product_category_name', data=top_10_categories, palette='Blues_r')
        plt.title(f"Top {top_n_categories} Product Categories by Review Score (Min Score: {min_review_score})", fontsize=16)
        plt.xlabel("Average Review Score", fontsize=14)
        plt.ylabel("Product Category", fontsize=14)
        st.pyplot(plt)

    # Payment Installments Section
    if options == "Payment Installments":
        st.subheader("Average Payment Installments by Product Category")

        # Filter by payment installments
        min_installments = st.slider("Select Minimum Average Installments", min_value=1, max_value=12, value=3, step=1)

        avg_installments_by_category = all_df.groupby('product_category_name')['payment_installments'].mean().reset_index()
        filtered_installments = avg_installments_by_category[avg_installments_by_category['payment_installments'] >= min_installments]

        top_n_installments = st.slider("Select Top N Categories for Installments", min_value=5, max_value=20, value=10)
        top_installments = filtered_installments.sort_values(by='payment_installments', ascending=False).head(top_n_installments)

        plt.figure(figsize=(10, 6))
        sns.barplot(x='payment_installments', y='product_category_name', data=top_installments, palette='coolwarm')
        plt.title(f"Top {top_n_installments} Product Categories by Payment Installments (Min Installments: {min_installments})", fontsize=16)
        plt.xlabel("Average Payment Installments", fontsize=14)
        plt.ylabel("Product Category", fontsize=14)
        st.pyplot(plt)

    # Payment Types Section
    if options == "Payment Types":
        st.subheader("Credit Card Payments by Product Category")

        # Filter by payment type
        payment_type = st.selectbox("Select Payment Type", all_df['payment_type'].unique())
        
        payment_data = all_df[all_df['payment_type'] == payment_type]
        payment_counts_by_category = payment_data.groupby('product_category_name')['payment_type'].count().reset_index()
        top_n_payments = st.slider("Select Top N Categories for Payments", min_value=5, max_value=20, value=10)
        
        top_10_payment_categories = payment_counts_by_category.sort_values(by='payment_type', ascending=False).head(top_n_payments)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x='payment_type', y='product_category_name', data=top_10_payment_categories, palette='Set2')
        plt.title(f"Top {top_n_payments} Product Categories by {payment_type.capitalize()} Payments", fontsize=16)
        plt.xlabel(f"{payment_type.capitalize()} Payment Count", fontsize=14)
        plt.ylabel("Product Category", fontsize=14)
        st.pyplot(plt)

# Running Streamlit
if __name__ == "__main__":
    main()

