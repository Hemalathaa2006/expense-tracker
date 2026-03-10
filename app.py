import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Expense Tracker", layout="centered")

st.title("💰 Personal Expense Tracker & Analyzer")

try:
    data = pd.read_csv("expenses.csv")
except:
    data = pd.DataFrame(columns=["Date","Category","Amount","Description"])

st.header("Add New Expense")

date = st.date_input("Date")
category = st.selectbox("Category",["Food","Transport","Shopping","Bills","Other"])
amount = st.number_input("Amount", min_value=0)
description = st.text_input("Description")

if st.button("Add Expense"):
    new_row = pd.DataFrame([[date,category,amount,description]],
                           columns=data.columns)
    
    data = pd.concat([data,new_row],ignore_index=True)
    data.to_csv("expenses.csv",index=False)
    
    st.success("Expense Added Successfully!")

st.header("Expense History")

st.dataframe(data)

if not data.empty:

    total = data["Amount"].sum()
    st.subheader(f"Total Expense: ₹ {total}")

    category_sum = data.groupby("Category")["Amount"].sum()

    st.subheader("Expense Distribution")

    fig1, ax1 = plt.subplots()

    ax1.pie(
        category_sum,
        labels=category_sum.index,
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.8
    )

    ax1.axis("equal")

    st.pyplot(fig1)

    st.subheader("Category Comparison")

    fig2, ax2 = plt.subplots()

    category_sum.plot(kind="bar", ax=ax2)

    ax2.set_xlabel("Category")
    ax2.set_ylabel("Amount")

    st.pyplot(fig2)

else:
    st.info("No expenses added yet.")