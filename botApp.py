from werkzeug.serving import run_simple
from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
import requests
import json
import ssl
import os

bot_details = dict()
with open('./bot.json', 'r') as f:
  bot_details = json.load(f)
  print(json.dumps(bot_details, indent=2))

API_URL = f'{bot_details["url"]}{bot_details["token"]}'
print(API_URL)
print(f'{bot_details["url"]}')
print(f'{bot_details["token"]}')
r = False

# with open('./node-v10.5.0/mycert.pem', 'rb') as f:
#     ca_certitificate = {'certificate': f}
#     r = requests.post(f'{API_URL}/setWebhook?url={bot_details["domain"]}', files={'certificate': f})
r = requests.post(f'{API_URL}/setWebhook?url={bot_details["domain"]}', files={'certificate': open('./node-v10.5.0/vallotta-party-bot.com.crt', 'rb')})

print(json.dumps(dict(r.headers), indent=2))
print(r)
print(r.text)

app = Flask(__name__)

@app.route('/bot', methods=['POST', 'GET'])
def test():
    if request.method == 'POST':
        print('POST')
    else:
        return Response('--- GET request ----', status=200)

@app.route('/', methods=['POST', 'GET']) 
def bot():
#   print(request.form)
    if request.method == 'POST':
        msg = request.get_json()
        # with open('./POST_telegram_request.json', 'w') as f:
        #     f.write(msg)
        print(msg)
        return Response('Ok', status=200)
    else:
        # msg = request.get_json(force=True)
        # print(msg)
        print(request.args.to_dict())
        # with open('./GET_telegram_request.json', 'w') as f:
        #     f.write(dict(msg))
        return Response('--- GET request ----', status=200)
        # return f'--- GET request ----'

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('./node-v10.5.0/vallotta-party-bot.com.crt', './node-v10.5.0/private.key')
run_simple('0.0.0.0', 443, app, ssl_context=context)

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port='443', debug=True, ssl_context=('./node-v10.5.0/vallotta-party-bot.com.crt', './node-v10.5.0/private.key'))
    # app.run(host='127.0.0.1', port='8443', debug=True, ssl_context=('./node-v10.5.0/vallotta-party-bot.com.crt', './node-v10.5.0/private.key'))
    # app.run(host='0.0.0.0', port=88, debug=True)



# from moviesandseries import MoviesAndSeries
# import re


# mes = MoviesAndSeries()
# runBot(mes)

# openssl req -newkey rsa:2048 -sha256 -nodes -keyout ./new-private.key -x509 -days 365 -out ./vallotta-party-bot.com.crt -subj "/C=US/ST=New York/L=Brooklyn/O=Example Brooklyn Company/CN=https://www.vallotta-party-bot.com"

# openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout publickey.pem -out cert.pem

# openssl rsa -in private.key -out nopassword.key