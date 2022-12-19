import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt", index_col="Fruit")

st.title('🥞🥓 My sisters new healthy Diner! 🍳☕')
st.header('Breakfast Favorites')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🍓 Build Your own Fruit Smoothie 🥝🍍')

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = st.multiselect(label="Pick some fruits:", options=list(my_fruit_list.index), default=['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table on the page
st.dataframe(fruits_to_show)

# New Section to display fruityvice api resonse
st.header('Fruityvice Fruit Advice!')
fruit_choice = st.text_input('What fruit would you like information about?', "kiwi")
st.write('The user entered', fruit_choice)
fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")
# st.text(fruityvice_response.json())

# take the json version of the response and normalize it
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
st.dataframe(fruityvice_normalized)

st.stop()

conn = snowflake.connector.connect(**st.secrets["snowflake"])
cursor = conn.cursor()

# cursor.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
cursor.execute("select * from fruit_load_list")
# my_data_row = cursor.fetchone()
my_data_row = cursor.fetchall()

st.header("The fruit load list contains:")
st.dataframe(my_data_row)

# allow the end user to add a fruit to the list
add_my_fruit = st.text_input('What fruit would you like to add?')
st.write('Thanks for adding', add_my_fruit)

cursor.execute("insert into fruit_load_list values ('from streamlit')")
