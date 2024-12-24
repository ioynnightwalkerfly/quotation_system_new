import streamlit as st
from pages.customers import customer_page
from pages.products import products_page
from pages.quotations import quotations_page
from pages.quotation_list import quotation_list_page

st.sidebar.title("เมนู")
menu = st.sidebar.radio("เลือกหน้า", ["ลูกค้า", "สินค้า", "ใบเสนอราคา", "รายการใบเสนอราคา"])

# แสดงหน้าที่เลือก
if menu == "ลูกค้า":
    customer_page()
elif menu == "สินค้า":
    products_page()
elif menu == "ใบเสนอราคา":
    quotations_page()
elif menu == "รายการใบเสนอราคา":
    quotation_list_page()