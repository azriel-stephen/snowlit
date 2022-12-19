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

# function for getting fruityvice api response
def get_fruityvice_data(choice):
  fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{choice}")
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

# New Section to display fruityvice api resonse
st.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
    st.error("Please select a fruit to get information.")
  else:
    st.dataframe(get_fruityvice_data(fruit_choice))
    
except URLError as e:
  streamlit.error()
  
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
