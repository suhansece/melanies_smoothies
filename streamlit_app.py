# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothies! :cup_with_straw:")
st.write(
"Choose your fruits you want in custom smoothies"
)


cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)
name_on_order = st.text_input('Name On Smoothie!')
ingrediencts_list =st.multiselect(
    'Choose up to 5 ingrediencts',
    my_dataframe,
    max_selections=5
)

if ingrediencts_list:
    ingredients_string = ''
    for fruits_choose in ingrediencts_list:
        ingredients_string+=fruits_choose +' '
        st.subheader(fruits_choose + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ fruits_choose)
        st_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order +"""')"""
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your smoothi is ordered")


