import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Streamlit UI
st.title(" 🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruit you want in your custom Smoothie!")

# Input for name on order
name_on_order = st.text_input("Name on Smoothie:")
st.write('The name on your Smoothie will be:', name_on_order)

# Snowflake Connection
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch Data from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# Convert Snowflake DataFrame to Pandas DataFrame
pd_df = my_dataframe.to_pandas()

# Display DataFrame (Uncomment for debugging)
# st.dataframe(pd_df)

# Multiselect input for ingredients (now using Pandas DataFrame list)
ingredients_list = st.multiselect('Choose up to 5 ingredients:', pd_df['FRUIT_NAME'].tolist(), max_selections=5)

# Processing selected ingredients
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list).strip()  # Join selected fruits into a string
    st.write("Selected Ingredients:", ingredients_string)

    for fruit_chosen in ingredients_list:
        # Ensure that fruit_chosen exists in DataFrame to prevent IndexError
        matching_rows = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON']
        
        if not matching_rows.empty:
            search_on = matching_rows.iloc[0]  # Get the first matching value
            st.write(f'The search value for {fruit_chosen} is: {search_on}')
        else:
            st.write(f'No search value found for {fruit_chosen}')
