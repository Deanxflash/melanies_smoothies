import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd

# Streamlit UI
st.title(" 🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruit you want in your custom Smoothie!")

# Input field for the customer's name
name_on_order = st.text_input("Name on Smoothie:")
st.write('The name on your Smoothie will be:', name_on_order)

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch available fruits from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()  # Convert to Pandas DataFrame

# Multi-select input for fruit ingredients
ingredients_list = st.multiselect('Choose up to 5 ingredients:', pd_df['FRUIT_NAME'], max_selections=5)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list).strip()  # ✅ Fix: No duplication

    if st.button("Place Order"):
        try:
            # Insert order into Snowflake
            session.sql(f"""
                INSERT INTO smoothies.public.orders (NAME_ON_ORDER, INGREDIENTS, ORDER_FILLED, ORDER_TS)
                VALUES ('{name_on_order}', '{ingredients_string}', FALSE, CURRENT_TIMESTAMP())
            """).collect()
            st.success("✅ Order placed successfully!", icon="🎉")
        except Exception as e:
            st.error(f"❌ Error placing order: {e}")
