import streamlit as st

st.set_page_config(
  page_title = "Crimes Against Women in India"
)

visualise = st.Page('page1.py', title='Objective 1')

pg=st.navigation(
  {
    "Menu":[visualise]
  }
)

pg.run()
