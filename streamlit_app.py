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
  st.error()

# Snowflake-related functions
st.header("The fruit load list contains:")
def get_fruit_load_list():
    with conn.cursor() as cur:
        cur.execute("select * from fruit_load_list")
        return cur.fetchall()

# Add a button to load the fruit
if st.button('Get Fruit Load List'):
    conn = snowflake.connector.connect(**st.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    st.dataframe(my_data_rows)

# st.stop()

# st.write('Thanks for adding', add_my_fruit)

def insert_row_snowflake(fruit):
  with conn.cursor() as cur:
#     cur.execute("insert into fruit_load_list values ('"+ fruit +"')")
    cur.execute(f"insert into fruit_load_list values ('{fruit}')")
    return "Thanks for adding "+ fruit
  
# allow the end user to add a fruit to the list
add_my_fruit = st.text_input('What fruit would you like to add?')
if st.button("Add a Fruit to the list"):
  conn = snowflake.connector.connect(**st.secrets["snowflake"])
  st.text(insert_row_snowflake(add_my_fruit))
