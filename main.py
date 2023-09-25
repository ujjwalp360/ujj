import streamlit as st
import mysql.connector
import pandas as pd

from page import *
db=mysql.connector.connect(host="localhost",user="root",password="ujjwal",database="stock")
c=db.cursor()
H=st.sidebar.radio(" ",("home","about","help","credits"))
if H=="home":
    page=st.session_state.get("page","home")
    if page == "home":
            homepage()
    elif page == "login":
            login()
    elif page == "op":
        op()
    elif page == "add stock":
        addstock()
    elif page == "show stock":
        showstock()
    elif page == "remove stock":
        removestock()
    elif page=='issue stock':
       issuestock()
    elif page=="show issued stock":
       show_issuedstock()
    elif page=="add department":
        add_dept()

elif H=="about":
    aboutpage()
elif H=="help":
    helppage()
elif H=="credits":
    creditpage()
