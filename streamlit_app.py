# Import python packages
import streamlit as st
import requests  
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(f"Customize Your Smoothie! :cup_with_straw:")
st.write(  """Choose the fruits you want in your custom Smoothie!.""")

name_on_order = st.text_input(label = "Name on Smoothie:", value="", max_chars=None)
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    label = 'Choose up to 5 ingredients:',
    options = my_dataframe,
    max_selections = 5
)

if ingredients_list:
    ingredients_string = ''

    for fruit in ingredients_list:
        ingredients_string += fruit + ' '
        url = "https://my.smoothiefroot.com/api/fruit/" + fruit
        smoothiefroot_response = requests.get(url) 
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into SMOOTHIES.public.orders(ingredients, name_on_order) 
                      values('""" + ingredients_string + """',""" + chr(39) + name_on_order + chr(39) + ")"

    st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered! Thanks ' + name_on_order, icon="✅")


