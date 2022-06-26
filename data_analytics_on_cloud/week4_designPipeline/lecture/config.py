import requests

# Database Variables
database_ip = "34.96.166.20" # change this to your public ip
database_username = "root"
database_password = "root"
default_email = 'glsandbox98@gmail.com'

# Function to send slack message
slack_webhook = "https://hooks.slack.com/services/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" # change this to your url
def send_msg(text_string):
    requests.post(slack_webhook, json={'text': text_string})