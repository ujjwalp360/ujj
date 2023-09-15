import streamlit as st
import mysql.connector
db = st.experimental_connection('mysql', type='sql')
c=db.cursor()
def add_room(r):
    c = db.cursor()
    cd=f"create table {r} (name varchar(20),id varchar(20),qty_added int(3))"
    c.execute(cd)
    c.commit()
def add_stock(r,n,i,q):
        c=db.cursor()      
        db.commit()
def add_stockid(r,n,i):
    l=add_stock(r,n,i,1)
    return l
def show_data(r=0,i=0,n=0):
    l=True
    if r!=0:
        if i!=0 or n!=0:
             c.execute(f"select * from stock where room no={r} and (name={n} or id={i})")
             d=c.fetchall()
        else:
            p="select * from stock where room no = %s"
            c.execute(p,(r,))
            d=c.fetchall()         
    else:
        c.execute("select * from stock")
        d=c.fetchall()

    return d
def show_by_date(r='0',d='0'):
    c.execute(f"select * from stock where room no =%s or date=%s",(r,d))
    d=c.fetchall()
    return d
t=False
def login():
    st.title("Login")
    i_=st.text_input("Enter Username")
    p=st.text_input("Enter Password", type="password")
    if st.button("Login"):
        if i_ and p:
            c.execute("SELECT id, password FROM user WHERE id = %s AND password = %s",(i_,p))
            result = c.fetchall()
            if result:
                st.write('s')
                return 's'

def addstock():
    st.title("add stock")
    r = st.text_input("enter room no.")
    n = st.text_input("enter name")
    i = st.text_input("enter id no.")
    q = st.text_input("enter qty")
    d = st.date_input("enter date")
    s=st.button("insert")
    if s:
        if r and i and q:              
                c.execute('insert into stock values (%s,%s,%s,%s,%s)',(r,i,n,q,d))
                db.commit()
                st.write('y')
                st.title('home')
def showstock():
    st.title("show stock")
    s=st.selectbox("Select Action", ("show by room","show by date","show all"))
    if s=="show by room":
        r=st.text_input("enter room no.")
        if r:
            d=show_data(r)
            st.table(d)
    elif s=="show by date":
        r=st.text_input("enter room no.")
        d=st.date_input("enter date")
        if r or d:
            d=show_by_date(r,d)
            st.table(d)
    elif s=="show all":
        d=show_data()
        st.table(d)
u = st.sidebar.radio("Select",('login',"add stock", "show stock"))
if u=='login':
    t=login()
elif u=='add stock':
        addstock()
elif u=='show stock':
    showstock()
