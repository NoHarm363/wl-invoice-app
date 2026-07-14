import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
import datetime

# ---------------------------------------------------------
# 1. REPORTLAB PDF GENERATION FUNCTION
# ---------------------------------------------------------
def create_invoice_from_image(jpg_template_path, output_pdf_path, invoice_data):
    # STEP 1: Create the Canvas
    c = canvas.Canvas(output_pdf_path, pagesize=A4)
    width, height = A4 
    
    # STEP 2: Draw the JPG Background
    c.drawImage(jpg_template_path, 0, 0, width=width, height=height)
    
    # STEP 3: Draw the Text Over the Image
    c.setFont("Helvetica", 12)
    
    # --- TOP RIGHT: Invoice Header Details ---
    c.drawString(457, 684, invoice_data['Invoice_No']) 
    c.drawString(459, 636, str(invoice_data['Invoice_Date'])) # Ensure string format
    
    # --- TOP LEFT: Customer Details ---
    cust_name = invoice_data['Customer_Name']
    if len(cust_name) > 34:
        c.setFont("Helvetica", 10) # Smaller font for long text
    else:
        c.setFont("Helvetica", 12) # Normal font
    c.drawString(65, 588, invoice_data['Customer_Name'])
    c.setFont("Helvetica", 12)

    # Check Address Line 1 length and adjust font
    addr_1 = invoice_data['Customer_Address_1st_Line']
    if len(addr_1) > 44:
        c.setFont("Helvetica", 10) # Smaller font for long text
    else:
        c.setFont("Helvetica", 12) # Normal font
    c.drawString(30, 553, addr_1)
    c.setFont("Helvetica", 12)
    
    # Check Address Line 2 length and adjust font
    addr_2 = invoice_data['Customer_Address_2nd_Line']
    if len(addr_2) > 44:
        c.setFont("Helvetica", 10)
    else:
        c.setFont("Helvetica", 12)
    c.drawString(30, 518, addr_2)
    c.setFont("Helvetica", 12)


    loaded_from = invoice_data['Loaded_From']
    if len(loaded_from) > 26:
        c.setFont("Helvetica", 10)
    else:
        c.setFont("Helvetica", 12)
    c.drawString(383, 598, loaded_from)
    c.setFont("Helvetica", 12)


    unloaded_to = invoice_data['Unloaded_To']
    if len(unloaded_to) > 26:
        c.setFont("Helvetica", 10)
    else:
        c.setFont("Helvetica", 12)
    c.drawString(383, 560, unloaded_to)
    c.setFont("Helvetica", 12)

    
    # --- MIDDLE LEFT: Job Details ---
    first_from = invoice_data['1st_From']
    if len(first_from) > 21:
        c.setFont("Helvetica", 10)
    else:
        c.setFont("Helvetica", 12)
    c.drawString(88, 435, first_from)
    c.setFont("Helvetica", 12)

    first_to = invoice_data['1st_To']
    if len(first_to) > 21:
        c.setFont("Helvetica", 10)
    else:
        c.setFont("Helvetica", 12)
    c.drawString(247, 435, first_to)
    c.setFont("Helvetica", 12)


    second_from = invoice_data['2nd_From']
    if len(second_from) > 21:
        c.setFont("Helvetica", 10)
    else:
        c.setFont("Helvetica", 12)
    c.drawString(88, 397, second_from)
    c.setFont("Helvetica", 12)


    second_to = invoice_data['2nd_To']
    if len(second_to) > 21:
        c.setFont("Helvetica", 10)
    else:
        c.setFont("Helvetica", 12)
    c.drawString(247, 397, second_to)
    c.setFont("Helvetica", 12)
    
    # --- MIDDLE RIGHT: Pricing Columns ---
    c.drawString(450, 397, invoice_data['Amount'])
    c.drawString(530, 397, invoice_data['CTS'])
    c.drawString(77, 297, invoice_data['Remark_1'])  # Limit remark to 65 characters
    c.drawString(77, 259, invoice_data['Remark_2'])  # Limit remark to 65 characters
    c.drawString(77, 221, invoice_data['Remark_3'])  # Limit remark to 65 characters

    # --- FOOTER: Driver Info ---
    c.drawString(88, 109, invoice_data['Driver_No'])
    driver_name = invoice_data['Driver_Name']
    if len(driver_name) > 15:
        c.setFont("Helvetica", 9) # Smaller font for long text
    else:
        c.setFont("Helvetica", 12) # Normal font
    c.drawString(68, 69, driver_name)
    c.setFont("Helvetica", 12)

    # --- BOTTOM RIGHT: Grand Total ---
    c.setFont("Helvetica-Bold", 14)
    c.drawString(450, 190, invoice_data['Grand_Total'])

    # STEP 4: Save the Final PDF
    c.save()

# ---------------------------------------------------------
# 2. STREAMLIT WEB APP INTERFACE
# ---------------------------------------------------------
st.set_page_config(page_title="Invoice Generator", layout="centered")
st.title("WL LorryCrane Cash Invoice Generator")
st.write("Fill in the details below to generate a new PDF invoice.")

current_date = datetime.datetime.now()
yy_mm = current_date.strftime("%y%m")
default_invoice_no = f"WL INV {yy_mm} 0001"

# Using st.form ensures the app doesn't refresh on every single keystroke
with st.form("invoice_form"):
    
    # Section 1: Header
    st.subheader("Invoice Info")
    col1, col2 = st.columns(2)
    with col1:
        inv_no = st.text_input("Invoice No", value=default_invoice_no)
    with col2:
        inv_date = st.date_input("Invoice Date") 

    # Section 2: Customer Data
    st.subheader("Customer Details")
    cust_name = st.text_input("Customer Name", value="")

    # Add max_chars=44 to these two lines
    addr_1 = st.text_input("Address 1st Line (Max 44 chars)", value="", max_chars=44)
    addr_2 = st.text_input("Address 2nd Line (Max 44 chars)", value="", max_chars=44)
    
    col_load1, col_load2 = st.columns(2)
    with col_load1:
        loaded_from = st.text_input("Loaded From", value="")
    with col_load2:
        unloaded_to = st.text_input("Unloaded To", value="")

    # Section 3: Job Details
    st.subheader("Time & Job Details")
    col3, col4 = st.columns(2)
    with col3:
        first_from = st.text_input("1st Time From", value="")
        second_from = st.text_input("2nd Time From", value="")
    with col4:
        first_to = st.text_input("1st Time To", value="")
        second_to = st.text_input("2nd Time To", value="")

    # Section 4: Pricing & Remarks
    st.subheader("Pricing & Remarks")
    col5, col6 = st.columns([2, 1]) 
    with col5:
        amount = st.text_input("Amount (RM). Example: 1000.00", value="")
    with col6:
        cts = st.text_input("CTS", value="1")
        
    remark_1 = st.text_input("Remark 1", value="", max_chars=73)
    remark_2 = st.text_input("Remark 2", value="", max_chars=73)
    remark_3 = st.text_input("Remark 3", value="", max_chars=73)

    # Section 5: Driver Info
    st.subheader("Driver Info")
    col8, col9 = st.columns(2)
    with col8:
        driver_no = st.text_input("Vehicle/Driver No", value="", max_chars=10)
    with col9:
        driver_name = st.text_input("Driver Name", value="")

    # Form Submit Button
    submitted = st.form_submit_button("Generate PDF Invoice", type="primary")

# ---------------------------------------------------------
# 3. HANDLING THE FORM SUBMISSION
# ---------------------------------------------------------
grand_total = (float(amount) * float(cts)) if amount and cts else 0.0
if submitted:
    # Package inputs into the dictionary required by the function
    my_data = {
        'Invoice_No': inv_no,
        'Invoice_Date': str(inv_date), # Convert date object to string
        'Customer_Name': cust_name,
        'Customer_Address_1st_Line': addr_1,
        'Customer_Address_2nd_Line': addr_2,
        'Loaded_From': loaded_from,
        'Unloaded_To': unloaded_to,
        '1st_From': first_from,
        '1st_To': first_to,
        '2nd_From': second_from,
        '2nd_To': second_to,
        'Amount': str(amount),
        'CTS': str(cts),
        'Remark_1': remark_1,
        'Remark_2': remark_2,
        'Remark_3': remark_3,
        'Grand_Total': str(f"{grand_total:.2f}"),
        'Driver_No': driver_no,
        'Driver_Name': driver_name
    }
    
    output_filename = f"{inv_no}.pdf"
    
    try:
        # Generate the PDF
        create_invoice_from_image("ckh.jpg", output_filename, my_data)
        st.success("Invoice generated successfully!")
        
        # Provide the download button
        with open(output_filename, "rb") as pdf_file:
            st.download_button(
                label="⬇️ Download Invoice",
                data=pdf_file,
                file_name=f"{inv_no.replace(' ', '_')}_invoice.pdf",
                mime="application/pdf"
            )
    except Exception as e:
        st.error(f"An error occurred: {e}. Please ensure 'ckh.jpg' is in the same folder as this script.")
