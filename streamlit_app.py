import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd
import mmh3  # ✅ MurmurHash3 (matches Snowflake better)

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
    ingredients_string = ' '.join(ingredients_list).strip()  # Ensure consistent formatting

    # ✅ Use MurmurHash3 (matches Snowflake's `HASH()`)
    hashed_ingredients = mmh3.hash64(ingredients_string)[0]  # 64-bit integer

    if st.button("Place Order"):
        try:
            session.sql(f"""
                INSERT INTO smoothies.public.orders (NAME_ON_ORDER, INGREDIENTS, ORDER_FILLED, ORDER_TS, HASH_ING)
                VALUES ('{name_on_order}', '{ingredients_string}', FALSE, CURRENT_TIMESTAMP(), {hashed_ingredients})
            """).collect()
            st.success(f"✅ Order placed successfully! \n\n Hashed Value: {hashed_ingredients}", icon="🎉")
        except Exception as e:
            st.error(f"❌ Error placing order: {e}")
