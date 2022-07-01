from bs4 import BeautifulSoup
import requests
import json
import lxml
import smtplib
from email.message import EmailMessage

########## USER INPUT ##########
URL = 'https://www.amazon.com/iRobot-Roomba-7550-Wi-Fi-Connecte/dp/B07GNPDMRP/ref=as_li_ss_tl?ie=UTF8&linkCode=sl1&tag=moderncastle-20&linkId=448949f5d49ce223c0c4480c758a67fb&language=en_US'
#URL = 'https://www.amazon.com/dp/B0835G4HP3/ref=sspa_dk_detail_2?psc=1&pd_rd_i=B0835G4HP3&pd_rd_w=UsqIZ&content-id=amzn1.sym.d533dd31-f352-432f-87d0-ace6fec162b4&pf_rd_p=d533dd31-f352-432f-87d0-ace6fec162b4&pf_rd_r=VPKE8YX38TKN6784APMP&pd_rd_wg=16XeH&pd_rd_r=3ffd3f06-f895-4942-90be-e6b1e5e0e050&s=home-garden&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExUFNVRENBRU41R1U2JmVuY3J5cHRlZElkPUEwMDY0Nzc2MzU5WjRQMEc5UVZPNyZlbmNyeXB0ZWRBZElkPUEwMzEwNDcwMkJTRlM1OUowSEM1SiZ3aWRnZXROYW1lPXNwX2RldGFpbF90aGVtYXRpYyZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU='

MY_EMAIL = 'flightsnotifier@gmail.com'
APP_PASSWORD = 'drleamqeglmnssrx'

DESIRED_PRICE = 800

HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44',
    'Accept-Language': 'en-US,en;q=0.9'
}

########### CHECK PRICE ##############
response = requests.get(URL, headers=HEADERS)
result = response.text
soup = BeautifulSoup(result, 'lxml')
price_w_currency = soup.find(name='span', class_='a-offscreen').get_text()
price = float(price_w_currency.split('$')[1])

product = soup.find(name='span', class_='a-size-large product-title-word-break').get_text().strip()

#print(price)
#print(product)

############# EMAIL USER #########
smtp_address_book = {"yahoo.com":"smtp.mail.yahoo.com", "gmail.com":"smtp.gmail.com", "hotmail.com":"smtp.live.com", "outlook.com":"smtp-mail.outlook.com"}

try:
    smtp_address = smtp_address_book[MY_EMAIL.split('@')[-1].lower()]
except KeyError as message:
    smtp_address = print(f"{message} is not a compatible server. Please input your server smtp: \n")
    if smtp_address == '':
        quit()

def send_emails(message, link, greeting, end, subject, signature):
    with open('users.json') as file:
        users = json.load(file)

    with smtplib.SMTP(smtp_address, port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=APP_PASSWORD)

        for user in users['users']:
            email = EmailMessage()
            email['Subject'] = subject
            email['From'] = MY_EMAIL
            email.set_content(f'<p>{greeting} {user["First Name"]}!<br> <p> {message} <a href="{link}">{end}</a> <br> <p> {signature}', subtype='html')

            email['To'] = user["Email"]
            connection.send_message(email)

if price < DESIRED_PRICE:
    send_emails(f'{product} is now ${price}', link = URL, greeting='Hello', end='Check it out here.', subject='Amazon Price Alert!', signature='Your Favorite Bot' )