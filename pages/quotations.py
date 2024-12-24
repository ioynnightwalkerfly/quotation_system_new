import streamlit as st
from database.db import add_quotation, add_quotation_detail, get_customers, get_products, get_quotations
from datetime import date

# ตัวแปรเก็บรายการสินค้าในใบเสนอราคา
if "quotation_items" not in st.session_state:
    st.session_state["quotation_items"] = []

def quotations_page():
    st.title("สร้างใบเสนอราคา")

    # ส่วนเลือกลูกค้า
    st.subheader("เลือกลูกค้า")
    customers = get_customers()
    customer_options = {c[0]: c[1] for c in customers}
    customer_id = st.selectbox("เลือกลูกค้า", options=customer_options.keys(), format_func=lambda x: customer_options[x])

    # ส่วนเลือกสินค้า
    st.subheader("เลือกสินค้า")
    products = get_products()
    product_options = {p[0]: f"{p[1]} - {p[2]} บาท" for p in products}

    col1, col2 = st.columns([3, 1])
    with col1:
        product_id = st.selectbox("เลือกสินค้า", options=product_options.keys(), format_func=lambda x: product_options[x])
    with col2:
        quantity = st.number_input("จำนวน", min_value=1, value=1)

    # ปุ่มเพิ่มสินค้าในใบเสนอราคา
    if st.button("เพิ่มสินค้า"):
        product = next((p for p in products if p[0] == product_id), None)
        if product:
            st.session_state["quotation_items"].append({
                "product_id": product[0],
                "name": product[1],
                "price": product[2],
                "quantity": quantity,
                "total": product[2] * quantity
            })
            st.success(f"เพิ่ม {product[1]} จำนวน {quantity} หน่วยในใบเสนอราคาเรียบร้อย!")

    # แสดงตารางรายการสินค้าในใบเสนอราคา
    st.subheader("รายการสินค้าในใบเสนอราคา")
    if len(st.session_state["quotation_items"]) > 0:
        total_price = 0
        for i, item in enumerate(st.session_state["quotation_items"]):
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            with col1:
                st.write(item["name"])
            with col2:
                st.write(f"{item['quantity']} หน่วย")
            with col3:
                st.write(f"{item['price']} บาท")
            with col4:
                st.write(f"{item['total']} บาท")
            with col5:
                if st.button("ลบ", key=f"delete_{i}"):
                    st.session_state["quotation_items"].pop(i)
                    st.success("ลบรายการสำเร็จ!")
                    break

            total_price += item["total"]

        # แสดงยอดรวม
        st.write("**ยอดรวมทั้งหมด**: {:.2f} บาท".format(total_price))
    else:
        st.info("ยังไม่มีรายการสินค้าในใบเสนอราคา")

    # ปุ่มบันทึกใบเสนอราคา
    if st.button("สร้างใบเสนอราคา"):
        if customer_id and len(st.session_state["quotation_items"]) > 0:
            quotation_id = add_quotation(customer_id, date.today().isoformat())
            for item in st.session_state["quotation_items"]:
                add_quotation_detail(quotation_id, item["product_id"], item["quantity"])
            st.session_state["quotation_items"] = []  # ล้างรายการสินค้า
            st.success(f"สร้างใบเสนอราคา ID {quotation_id} สำเร็จ!")
        else:
            st.error("กรุณาเลือกลูกค้าและเพิ่มสินค้าในใบเสนอราคาก่อน!")
