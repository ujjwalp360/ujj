import streamlit as st
import mysql.connector

# Create a connection to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ujjwal",
    database="stock"  
)
c = db.cursor()
def add_room(r,n):
    c.execute("create table %s(name varchar(),id varchar(),qty_added int,add_date timestamp()",(r))
    c.commit()
def add_stock(r,n,i,q):
    l=True
    if l:
        c.execute('insert into {r} values (%s,%s,%s)'),(n,i,int(q))
        c.commit()
    else:
        l=False
    return l
def add_stockid(r,n,i):
    l=add_stock(r,n,i,1)
    return l
def show_data(r=0,i=0,n=0):
    l=True
    if r!=0:
        if i!=0:
            if n!=0:
                c.execute("select * from {r} where (name={n} or id={i})")
                d=c.fetchall()
            else:
                c.execute("select * from {r} where (id={i})")
                d=c.fetchall()         
        else:
            c.execute("select * from {r}")
            d=c.fetchall()
    else:
        d=[]
        c.execute("show tables")
        f = c.fetchall()
        for i in range(0,len(f)):
            c.execute("select * from {d[i][0]}")
            g=c.fetchall()
            l.append(g)
    return d
t=True
if t:
    st.title("login")
    i_=st.text_input("Enter Username")
    p=st.text_input("Enter Password", type="password")
    if st.button("Login as Editor"):
        c.execute("SELECT id, password FROM user WHERE id = %s AND password = %s",(i_,p))
        result = c.fetchall()
        if result:
             t=False
menu = st.sidebar.selectbox("Menu", ["add room", "add stock with id","add stock without id","show data","find data"])
if menu == "add room" and t==False:
    st.header("add room")
    r = st.number_input("enter room no.")
    n = st.text_input("enter room name.")
    if st.button("Insert"):
        add_room(r,n)
        st.success('added')
    else:
        st.error('nn')
elif menu=="add stock with id":
    st.header("add stock with id")
    r = st.number_input("enter room no.")
