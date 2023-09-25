import streamlit as st
import mysql.connector
import pandas as pd
db=mysql.connector.connect(host="localhost",user="root",password="ujjwal",database="stock")
c=db.cursor()
def homepage():
    st.title("Welcome to Stock Management Pro")
    st.write("Our Stock Management Pro is your ultimate solution for efficient stock management. Whether you're running a small business or a large enterprise, our platform is designed to streamline your inventory control.")
    st.write("With Stock Management Pro, you can:"
             "- Easily track and manage your entire inventory."
             "Experience the power of efficient stock management. Join us today!")
    st.write("Sign up or log in to Stock Management Pro now!")
    if st.button("Login Now!",type="primary"):
        st.session_state.page = "login"
def aboutpage():
    st.title("Our Stock Management System")
    st.write("where we take stock management to a whole new level, we believe in simplifying the complex, and that's exactly what we do with your inventory.")
def helppage():
    st.title("Contact Support")
    st.write("our dedicated support is here to assist you. Contact us through one of the following methods:")
    st.write("Email: support@stockmanagementpro.com")
    st.write("user guide will be upload soon...")
def creditpage():
    st.title("Credits")
    st.title("Development Team")
    st.write("Ujjwal ")
    st.write("Pushkar")
    st.write("Prathmesh")
def show_data(i=0,n=0):
    l=True
    if n!=0:
             c.execute(f"select * from stock where (name={n} or id={i})")
             d=c.fetchall()
    elif i!=0:
            p="select * from stock where id = %s"
            c.execute(p,(i,))
            d=c.fetchall()         
    else:
        c.execute("select * from stock")
        d=c.fetchall()

    return d
def show_by_date(d='0'):
    c.execute(f"select * from stock where date=%s",(d,))
    d=c.fetchall()
    return d
t=False
def login():
    st.title("Login")
    i_=st.text_input("Enter Username")
    p=st.text_input("Enter Password", type="password")
    if st.button("Login",type="primary"):
        if i_ and p:
            c.execute("SELECT id, password FROM user WHERE id = %s AND password = %s",(i_,p))
            result = c.fetchall()
            if result:
                st.write('s')
                st.session_state.page = "op"
                    
                    
def op():
    u = st.selectbox("STOCK",("select","add stock", "show stock","remove stock"))
    if u=="add stock":
        st.session_state.page = "add stock"
    elif u=="show stock":
        st.session_state.page = "show stock"
    elif u=="remove stock":
        st.session_state.page = "remove stock"
    u = st.selectbox("ISSUE",("select","issue stock","add department", "show issue"))
    if u=="issue stock":
        st.session_state.page = "issue stock"
    elif u=="add department":
        st.session_state.page = "add department"
    elif u=="show issue":
        st.session_state.page = "show issued stock"
def addstock():
    st.title("add stock")
    n = st.text_input("name")
    i = st.text_input("id no.")
    q = st.text_input("qty")
    d = st.date_input("date")
    w = st.text_input("warranty period(in months)")
    cc = st.text_input("ok or not ok")
    s = st.text_input("specifications")
    l=st.button("insert")
    if l:
        if n and i and q:              
                c.execute('insert into stock values (%s,%s,%s,%s,%s,%s,%s)',(n,i,q,d,w,cc,s))
                db.commit()
                st.write('success')
                st.success('done')
                if st.button("back"):
                   st.session_state.page = "op"
    elif st.button("back"):
        st.session_state.page = "op"
def showstock():
    st.title("show stock")
    s=st.selectbox("Select Action", ("show by id","show by date","show all"))
    if s=="show by id":
        r=st.text_input("enter id no.")
        if r:
            d=show_data(r)
            f=pd.DataFrame(d,columns=("name","id","qty","date","warranty","c","specs"))
            st.table(f)
            st.title("more info")
            c.execute(f"select * from stock where id=%s",(r,))
            d=c.fetchall()
            c.execute(f"select month(curdate())")
            dt=c.fetchall()
            c.execute(f"select year(curdate())")
            dt2=c.fetchall()
            w=int(d[0][4])
            m1=int(d[0][3].split("-")[1])
            y1=int(d[0][3].split("-")[0])
            m2=dt[0][0]
            y2=dt2[0][0]
            i=y2-y1,m2-m1
            b=w-(i[0]*12+i[1])
            S=d[0][6]
            C=d[0][5]
            st.write(f"warranty period:{w} months({b} months remaining)")
            st.write(f"specification:{S}")
            st.write(f"condition:{C}")
            G=st.radio("s",("issue it",))
            if G=="issue it":
                c.execute("select * from issue")
                D1=c.fetchall()
                n=(D1[-1][0])+1
                st.write(f"ISSUE ID:{n}")
                c.execute("select * from department")
                D=c.fetchall()
                C=[]
                for j in range (len(D)):
                    C.append(f"{D[j][0]}-{D[j][1]}")
                D=C
                q=st.selectbox("dept no",D)
                Q=q.split("-")
                q=int(Q[0])
                qty=st.number_input("qty to issue",1)
                d = st.date_input("date of issue")
                l=st.button("ISSUE")
                if l:
                    if n and r and q:

                            c.execute('insert into issue values (%s,%s,%s,%s,%s)',(n,r,q,qty,d))
                            db.commit()
                            st.write('Success')
                            st.success('Done')
                            if st.button("back"):
                                 st.session_state.page = "op"
                elif st.button("back"):
                    st.session_state.page = "op"
            elif st.button("back"):
                st.session_state.page = "op"
        elif st.button("back"):
                st.session_state.page = "op"
    elif s=="show by date":
        d=st.date_input("enter date")
        if d:
            d=show_by_date(d)
            f=pd.DataFrame(d,columns=("name","id","qty","date","warranty","c","specs"))
            st.table(f)
            st.title("more info")
            i=st.text_input("id")
            c.execute(f"select * from stock where id=%s",(i,))
            d=c.fetchall()
            c.execute(f"select month(curdate())")
            dt=c.fetchall()
            c.execute(f"select year(curdate())")
            dt2=c.fetchall()
            w=int(d[0][4])
            m1=int(d[0][3].split("-")[1])
            y1=int(d[0][3].split("-")[0])
            m2=dt[0][0]
            y2=dt2[0][0]
            r=y2-y1,m2-m1
            b=w-(r[0]*12+r[1])
            S=d[0][6]
            C=d[0][5]
            st.write(f"warranty period:{w} months({b} months remaining)")
            st.write(f"specification:{S}")
            st.write(f"condition:{C}")
            G=st.radio("s",("issue it",))
            if G=="issue it":
                c.execute("select * from issue")
                D1=c.fetchall()
                n=(D1[-1][0])+1
                st.write(f"ISSUE ID:{n}")
                qty=st.number_input("qty to issue",1)
                c.execute("select * from department")
                D=c.fetchall()
                C=[]
                for j in range (len(D)):
                    C.append(f"{D[j][0]}-{D[j][1]}")
                D=C
                q=st.selectbox("dept no",D)
                Q=q.split("-")
                q=int(Q[0])
                d = st.date_input("date of issue")
                l=st.button("ISSUE")
                if l:
                    if n and i and q:              
                            c.execute('insert into issue values (%s,%s,%s,%s,%s)',(n,i,q,qty,d))
                            db.commit()
                            st.write('Success')
                            st.success('Done')
                            if st.button("back"):
                                 st.session_state.page = "op"
                elif st.button("back"):
                    st.session_state.page = "op"
            elif st.button("back"):
                st.session_state.page = "op"
        elif st.button("back"):
                st.session_state.page = "op"

    elif s=="show all":
        d=show_data()
        f=pd.DataFrame(d,columns=("name","id","qty","date","warranty","c","specs"))
        st.table(f)
        st.title("more info")
        i=st.text_input("id")
        c.execute(f"select * from stock where id=%s",(i,))
        d=c.fetchall()
        c.execute(f"select month(curdate())")
        dt=c.fetchall()
        c.execute(f"select year(curdate())")
        dt2=c.fetchall()
        w=int(d[0][4])
        m1=int(d[0][3].split("-")[1])
        y1=int(d[0][3].split("-")[0])
        m2=dt[0][0]
        y2=dt2[0][0]
        r=y2-y1,m2-m1
        b=w-(r[0]*12+r[1])
        S=d[0][6]
        C=d[0][5]
        st.write(f"warranty period:{w} months({b} months remaining)")
        st.write(f"specification:{S}")
        st.write(f"condition:{C}")
        G=st.radio("s",("issue it",))
        if G=="issue it":
                c.execute("select * from issue")
                D1=c.fetchall()
                n=(D1[-1][0])+1
                st.write(f"ISSUE ID:{n}")
                qty=st.number_input("qty to issue",1)
                c.execute("select * from department")
                D=c.fetchall()
                C=[]
                for j in range (len(D)):
                    C.append(f"{D[j][0]}-{D[j][1]}")
                D=C
                q=st.selectbox("dept no",D)
                Q=q.split("-")
                q=int(Q[0])
                d = st.date_input("date of issue")
                l=st.button("ISSUE")
                if l:
                    if n and i and q:              
                            c.execute('insert into issue values (%s,%s,%s,%s,%s)',(n,i,q,qty,d))
                            db.commit()
                            st.write('Success')
                            st.success('Done')
                            if st.button("back"):
                                 st.session_state.page = "op"
                elif st.button("back"):
                    st.session_state.page = "op"
    elif st.button("back"):
        st.session_state.page = "op"
def removestock():
    st.title("remove stock")
    i=st.text_input("enter id.")
    c.execute(f"select * from stock where id=%s",(i,))
    d=c.fetchall()
    st.table(d)
    if st.button("confirm"):
        c.execute(f"delete from stock where id=%s",(i,))
        db.commit()
        st.success("deleted")
        if st.button("back"):
            st.session_state.page = "op"
    elif st.button("back"):
            st.session_state.page = "op"
def issuestock():
    st.title("Issue stock")
    c.execute("select * from department")
    D1=c.fetchall()
    n=(D1[-1][0])+1
    st.write(f"ISSUE ID:{n}")
    i = st.text_input("stock id")
    qty=st.number_input("qty to issue",1)
    c.execute("select * from department")
    D=c.fetchall()
    C=[]
    for j in range (len(D)):
        C.append(f"{D[j][0]}-{D[j][1]}")
    D=C
    q=st.selectbox("dept no",D)
    Q=q.split("-")
    q=int(Q[0])
    d = st.date_input("date of issue")
    l=st.button("Insert")
    if l:
        if n and i and q:              
                c.execute('insert into issue values (%s,%s,%s,%s,%s)',(n,i,q,qty,d))
                db.commit()
                st.write('Success')
                st.success('Done')
                if st.button("Back"):
                   st.session_state.page = "op"
    elif st.button("back"):
        st.session_state.page = "op"

def show_issuedstock():
    st.title("show issued stock")
    s=st.selectbox("Select Action", ("show by issue id","show by issue date","show by dept","show all"))
    if s=="show by issue id":
        r=st.text_input("enter id no.")
        if r:
            p="select * from issue where issue_no = %s"
            c.execute(p,(r,))
            d=c.fetchall()
            f=pd.DataFrame(d,columns=("issue id","stock id","dept no","qty issued","issued date"))
            st.table(f)
    elif s=="show by issue date":
        r=st.text_input("enter department no.")
        d=st.date_input("enter date")
        if r or d:
            c.execute(f"select * from issue where idate=%s",(d,))
            d=c.fetchall()
            f=pd.DataFrame(d,columns=("issue id","stock id","dept no","qty issued","issued date"))
            st.table(f)
            if st.button("back"):
                st.session_state.page = "op"
    elif s=="show by dept":
        r=st.text_input("enter department no.")
        c.execute("select * from department")
        D=c.fetchall()
        C=[]
        for j in range (len(D)):
            C.append(f"{D[j][0]}-{D[j][1]}")
        D=C
        q=st.selectbox("dept no",D)
        Q=q.split("-")
        q=int(Q[0])
                
        
    elif s=="show all":
        p="select * from issue"
        c.execute(p)
        d=c.fetchall()
        f=pd.DataFrame(d,columns=("issue id","stock id","dept no","qty issued","issued date"))
        st.table(f)
        st.title("more info")
        i=st.text_input("issueid")
        if st.button("back"):
                st.session_state.page = "op"
    elif st.button("back"):
        st.session_state.page = "op"
def add_dept():
    d=st.text_input("enter department no.")
    n=st.text_input("dept name")
    i=st.text_input("incharge name")
    l=st.button("insert")
    if l:
        if d and i :              
                c.execute('insert into department values (%s,%s,%s)',(d,n,i))
                db.commit()
                st.write('success')
                st.success('done')
                if st.button("back"):
                   st.session_state.page = "op"
    elif st.button("back"):
                   st.session_state.page = "op"
    
    
    

