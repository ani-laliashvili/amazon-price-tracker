# spotify-playlist-maker

This script uses Beautiful Soup to notify user if the price of a product on Amazon drops below desired price via email.

## User inputs
- URL: URL of a product on Amazon.com
- MY_EMAIL: user's email set up for this application
- APP_PASSWORD: password for a successful connection with user's email
- HEADERS: header values returned from http://myhttpheader.com/
- DESIRED_PRICE: price under which user gets notified. You can use https://camelcamelcamel.com/ to choose a good price for your product. 

## Requirements
- bs4
- requests
- json
- lxml
- smtplib
- email.message
