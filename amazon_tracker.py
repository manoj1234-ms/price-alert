import streamlit as st
from bs4 import BeautifulSoup
import json
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ===== Streamlit UI =====
st.title("🛒 Amazon Price Alert")

# User inputs
threshold_price = st.number_input("Enter price threshold (₹)", min_value=0.0, value=2000.0)
uploaded_file = st.file_uploader("Upload Amazon HTML file", type="html")
sender_email = st.text_input("Your Gmail address")
sender_password = st.text_input("Your App Password", type="password")
receiver_email = st.text_input("Recipient Email")
send_email = st.checkbox("Send email alert if products found")

# ===== Logic starts after file is uploaded =====
if uploaded_file:
    soup = BeautifulSoup(uploaded_file, "html.parser")
    product_divs = soup.find_all("div", class_="a-section a-spacing-small puis-padding-left-micro puis-padding-right-micro")

    products = []
    alert_products = []

    for div in product_divs:
        try:
            product_name = div.find("span", class_="a-size-base-plus a-color-base").get_text(strip=True)
        except:
            product_name = " "

        try:
            price_text = div.find("span", class_="a-price-whole").get_text(strip=True)
            product_price = float(price_text.replace(",", ""))
        except:
            product_price = 0.0

        try:
            link_tag = div.find("a", class_="a-link-normal s-line-clamp-2 s-link-style a-text-normal", href=True)
            product_url = "https://www.amazon.in" + link_tag["href"] if link_tag else " "
        except:
            product_url = " "

        try:
            rating_tag = div.find("span", class_="a-size-small a-color-base", attrs={"aria-hidden": "true"})
            rating = rating_tag.get_text(strip=True) if rating_tag else "No rating"
        except:
            rating = "No rating"

        product = {
            "Product Name": product_name,
            "Price (₹)": product_price,
            "URL": product_url,
            "Rating": rating
        }

        products.append(product)
        if 0 < product_price < threshold_price:
            alert_products.append(product)

    # ===== Display Results =====
    st.subheader("📋 All Products Found")
    st.json(products)

    if alert_products:
        st.subheader(f"🔔 Products Below ₹{threshold_price}")
        for p in alert_products:
            st.markdown(f"**{p['Product Name']}** - ₹{p['Price (₹)']}  \n"
                        f"[Link]({p['URL']})  \n"
                        f"Rating: {p['Rating']}")
    else:
        st.success("✅ No products found below threshold.")

    # ===== Email Alert =====
    if send_email and sender_email and sender_password and receiver_email and alert_products:
        try:
            html_content = f"<h2>🛒 Amazon Products Below ₹{threshold_price}</h2><ul>"
            for p in alert_products:
                html_content += f"<li><b>{p['Product Name']}</b> - ₹{p['Price (₹)']}<br><a href='{p['URL']}'>{p['URL']}</a><br>Rating: {p['Rating']}</li><br>"
            html_content += "</ul>"

            message = MIMEMultipart("alternative")
            message["Subject"] = "🔔 Amazon Price Alert"
            message["From"] = sender_email
            message["To"] = receiver_email
            message.attach(MIMEText(html_content, "html"))

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, message.as_string())

            st.success("📧 Email sent successfully!")

        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")
