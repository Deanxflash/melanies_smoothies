import streamlit as st
from snowflake.snowpark.functions import col

# Streamlit UI
st.title(" 🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruit you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Multiselect input for ingredients
ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe , max_selections=5)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list).strip()  # Join selected fruits into a string

    # Fixing the SQL query based on the number of columns
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # st.write(my_insert_stmt)  # Debugging output

    # Button to submit order
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f' Your Smoothie is ordered, {name_on_order}!', icon="✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())
st.df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
