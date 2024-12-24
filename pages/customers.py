import streamlit as st
from database.db import add_customer, get_customers, update_customer, delete_customer

def customer_page():
    st.title("จัดการข้อมูลลูกค้า")

    # ส่วนเพิ่มลูกค้าใหม่
    st.subheader("เพิ่มลูกค้าใหม่")
    with st.form("add_customer_form", clear_on_submit=True):
        name = st.text_input("ชื่อ")
        email = st.text_input("อีเมล")
        address = st.text_area("ที่อยู่")
        submitted = st.form_submit_button("บันทึก")

        if submitted:
            if name and email:
                add_customer(name, email, address)
                st.success(f"เพิ่มลูกค้า {name} สำเร็จ!")
            else:
                st.error("กรุณากรอกข้อมูลให้ครบถ้วน")

    # ตารางแสดงข้อมูลลูกค้า
    st.subheader("รายการลูกค้า")
    customers = get_customers()

    if len(customers) == 0:
        st.info("ยังไม่มีข้อมูลลูกค้า")
    else:
        for customer in customers:
            with st.expander(f"{customer[1]}"):
                col1, col2 = st.columns(2)

                with col1:
                    new_name = st.text_input("ชื่อ", value=customer[1], key=f"name_{customer[0]}")
                    new_email = st.text_input("อีเมล", value=customer[2], key=f"email_{customer[0]}")
                    new_address = st.text_area("ที่อยู่", value=customer[3], key=f"address_{customer[0]}")

                with col2:
                    if st.button("แก้ไข", key=f"update_{customer[0]}"):
                        update_customer(customer[0], new_name, new_email, new_address)
                        st.success(f"แก้ไขข้อมูลลูกค้า {new_name} สำเร็จ!")

                    if st.button("ลบ", key=f"delete_{customer[0]}"):
                        delete_customer(customer[0])
                        st.success(f"ลบลูกค้า {customer[1]} สำเร็จ!")
