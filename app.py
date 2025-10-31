import streamlit as st

st.set_page_config(
  page_title = "Crimes Against Women in India", layout="wide"
)

visualise1 = st.Page('page1.py', title='Objective 1')

visualise2 = st.Page('page2.py', title='Objective 2')

visualise3 = st.Page('page3.py', title='Objective 3')

pg=st.navigation(
  {
    "Menu":[visualise1, visualise2, visualise3]
  }
)

pg.run()
