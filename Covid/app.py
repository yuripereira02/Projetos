import streamlit as st

st.set_page_config(page_title='COVID-19', layout='wide')

st.navigation(pages=[
    st.Page(page='context.py', title='Sobre o COVID-19'),
    st.Page(page='analise.py', title='Análises')
]).run()

