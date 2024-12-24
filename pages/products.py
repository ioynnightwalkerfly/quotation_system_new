import streamlit as st
from database.db import add_product, get_products, update_product, delete_product


def products_page():
    st.title("จัดการข้อมูลสินค้า")

    # ส่วนเพิ่มสินค้าใหม่
    st.subheader("เพิ่มสินค้าใหม่")
    with st.form("add_product_form", clear_on_submit=True):
        name = st.text_input("ชื่อสินค้า")
        price = st.number_input("ราคา", min_value=0.0, format="%.2f")
        unit = st.text_input("หน่วยนับ")
        submitted = st.form_submit_button("บันทึก")

        if submitted:
            if name and price and unit:
                add_product(name, price, unit)
                st.success(f"เพิ่มสินค้า {name} สำเร็จ!")
            else:
                st.error("กรุณากรอกข้อมูลให้ครบถ้วน")

    # ตารางแสดงข้อมูลสินค้า
    st.subheader("รายการสินค้า")
    products = get_products()

    if len(products) == 0:
        st.info("ยังไม่มีข้อมูลสินค้า")
    else:
        for product in products:
            with st.expander(f"{product[1]}"):
                col1, col2 = st.columns(2)

                with col1:
                    new_name = st.text_input("ชื่อสินค้า", value=product[1], key=f"name_{product[0]}")
                    new_price = st.number_input("ราคา", value=product[2], key=f"price_{product[0]}", format="%.2f")
                    new_unit = st.text_input("หน่วยนับ", value=product[3], key=f"unit_{product[0]}")

                with col2:
                    if st.button("แก้ไข", key=f"update_{product[0]}"):
                        update_product(product[0], new_name, new_price, new_unit)
                        st.success(f"แก้ไขข้อมูลสินค้า {new_name} สำเร็จ!")

                    if st.button("ลบ", key=f"delete_{product[0]}"):
                        delete_product(product[0])
                        st.success(f"ลบสินค้า {product[1]} สำเร็จ!")
