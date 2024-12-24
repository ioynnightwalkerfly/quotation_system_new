import streamlit as st
from database.db import get_quotations, get_quotation_details, delete_quotation

def quotation_list_page():
    st.title("รายการใบเสนอราคา")

    # แสดงรายการใบเสนอราคาทั้งหมด
    quotations = get_quotations()

    if len(quotations) == 0:
        st.info("ยังไม่มีใบเสนอราคาในระบบ")
    else:
        for quotation in quotations:
            with st.expander(f"ใบเสนอราคา ID: {quotation[0]}"):
                st.write(f"ลูกค้า: {quotation[1]}")
                st.write(f"วันที่: {quotation[2]}")

                # แสดงรายละเอียดสินค้าในใบเสนอราคา
                st.subheader("รายละเอียดสินค้า")
                details = get_quotation_details(quotation[0])
                for detail in details:
                    st.write(f"- {detail[0]}: {detail[1]} หน่วย @ {detail[2]} บาท")

                # สร้าง HTML สำหรับพิมพ์
                html_content = f"""
                <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                        }}
                        .quotation {{
                            border: 1px solid #000;
                            padding: 10px;
                            margin: 10px;
                        }}
                        .header {{
                            text-align: center;
                            font-weight: bold;
                            margin-bottom: 20px;
                        }}
                        table {{
                            width: 100%;
                            border-collapse: collapse;
                        }}
                        table, th, td {{
                            border: 1px solid black;
                        }}
                        th, td {{
                            padding: 8px;
                            text-align: left;
                        }}
                        .total {{
                            text-align: right;
                            font-weight: bold;
                            margin-top: 10px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="quotation">
                        <div class="header">ใบเสนอราคา</div>
                        <p><b>ลูกค้า:</b> {quotation[1]}</p>
                        <p><b>วันที่:</b> {quotation[2]}</p>
                        <table>
                            <tr>
                                <th>ชื่อสินค้า</th>
                                <th>ราคาต่อชิ้น</th>
                                <th>หน่วยนับ</th>
                                <th>ราคารวม</th>
                            </tr>
                """
                total_price = 0
                for detail in details:
                    subtotal = detail[1] * detail[2]
                    html_content += f"""
                            <tr>
                                <td>{detail[0]}</td>
                                <td>{detail[2]:.2f} บาท</td>
                                <td>{detail[1]}</td>
                                <td>{subtotal:.2f} บาท</td>
                            </tr>
                    """
                    total_price += subtotal

                html_content += f"""
                        </table>
                        <div class="total">ยอดรวมทั้งหมด: {total_price:.2f} บาท</div>
                    </div>
                </body>
                </html>
                """

                # ปุ่มแสดง PDF
                st.download_button(
                    label="ดาวน์โหลด PDF",
                    data=html_content,
                    file_name=f"quotation_{quotation[0]}.html",
                    mime="text/html"
                )

                # ปุ่มพิมพ์
                st.markdown(f"""
                <button onclick="window.open('data:text/html;charset=utf-8,{html_content}', '_blank').print()">พิมพ์ใบเสนอราคา</button>
                """, unsafe_allow_html=True)

                # ปุ่มลบใบเสนอราคา
                if st.button(f"ลบใบเสนอราคา ID {quotation[0]}", key=f"delete_{quotation[0]}"):
                    delete_quotation(quotation[0])
                    st.success(f"ลบใบเสนอราคา ID {quotation[0]} สำเร็จ!")
                    st.experimental_set_query_params(refresh="true")