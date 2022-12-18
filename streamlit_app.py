import streamlit as st
import pandas as pd
import requests

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
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json())

# take the json version of the response and normalize it
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
st.dataframe(fruityvice_normalized)
