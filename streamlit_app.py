import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Streamlit UI
st.title(" 🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruit you want in your custom Smoothie!")

# Input for name on order
st.subheader("Enter Your Name")
name_on_order = st.text_input("Name on Smoothie:")
st.write('The name on your Smoothie will be:', name_on_order)

# Connect to Snowflake
st.subheader("Fetching Available Ingredients")
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch Data from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# Convert Snowflake DataFrame to Pandas DataFrame
pd_df = my_dataframe.to_pandas()

# Multiselect input for ingredients
st.subheader("Select Your Ingredients")
ingredients_list = st.multiselect('Choose up to 5 ingredients:', pd_df['FRUIT_NAME'].tolist(), max_selections=5)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list).strip()  # Join selected fruits into a string

    for fruit_chosen in ingredients_list:
        st.subheader(f"{fruit_chosen} Nutrition Information")

        # API Request for fruit details
        api_url = f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen}"
        smoothiefroot_response = requests.get(api_url)

        if smoothiefroot_response.status_code == 200:
            fruit_data = smoothiefroot_response.json()
            
            # Convert JSON response to DataFrame if needed
            if isinstance(fruit_data, list):  # If the API returns a list of dicts
                fruit_df = pd.DataFrame(fruit_data)
            elif isinstance(fruit_data, dict):  # If API returns a single dict, wrap it in a DataFrame
                fruit_df = pd.DataFrame([fruit_data])
            else:
                fruit_df = pd.DataFrame()  # Fallback in case of unexpected response

            st.dataframe(fruit_df, use_container_width=True)
        else:
            st.error(f"Failed to fetch nutrition info for {fruit_chosen}. Please try again.")

    # SQL Insert Query - Using Parameterized Query
    try:
        session.sql(
            "INSERT INTO smoothies.public.orders (ingredients, name_on_order) VALUES (?, ?)",
            (ingredients_string, name_on_order)
        ).collect()

        # Button to submit order
        if st.button("Submit Order"):
            st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")

    except Exception as e:
        st.error(f"Error placing order: {str(e)}")
