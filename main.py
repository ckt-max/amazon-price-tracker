import requests
from bs4 import BeautifulSoup as bs
import smtplib
import ssl #for security

#email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print('Fetching product price')
amazon_url = 'https://www.amazon.in/LG-4K-UHD-Monitor-Display-Freesync/dp/B07PGL2WVS/ref=sr_1_2?crid=M78NCKAWA50S&keywords=4k%2Bmonitor&qid=1707634550&sprefix=4k%2B%2Caps%2C238&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1'
# headers for the request
headers = {
    'sec-ch-ua':'"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile':'?0',
    'sec-ch-ua-platform':"Windows",
    'upgrade-insecure-requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
}

r = requests.get(amazon_url, headers=headers)

soup = bs(r.text,'html.parser' )

# getting name of the product
product_name = soup.select_one('h1 #productTitle').get_text().strip()
print(product_name)

# getting price of the product
txt = soup.select_one('.a-price-whole').get_text().replace(',','')
price = int(txt[:txt.find('.')]) # converting txt to int
print(price)
print('Product price fetched successfully')

# ------------------SENDING EMAIL ALERT IF PRICE IS LOWER---------------------
target_price = 25000

print('Composing Email....')
content = ''

email_sender = ''
email_password = ''
email_receiver = ''

content = f"This is now the right time to fulfill your desire. Hurry up and get {product_name} at just ₹ {price}"

#Email details
msg = MIMEMultipart() #function to create email
msg['Subject'] = f'Price dropped for {product_name}'
msg['From'] = email_sender
msg['to'] = email_receiver
msg.attach(MIMEText(content, 'html') )#to attach email body in html format

context = ssl.create_default_context()

#sending Email
with smtplib.SMTP_SSL('smtp.gmail.com',465, context = context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, msg.as_string())
    print("Mail sent......")
