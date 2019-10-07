from flask import Flask, render_template, request, make_response, redirect, url_for
import sys
import json
import requests



app = Flask(__name__)

@app.route("/")
def home():
    #definitions
    base = "base"
    to = "to"
    amount = "amount"
    convert = "convert"
    response = make_response(render_template("index.html",
                                             base=base,
                                             to=to,
                                             amount=amount,
                                             convert=convert))
    return response


#having trouble getting inputs processed with GET/POST method, new to flask so have to look up documentation at every step. Any insight here?
@app.route("/convert", methods=['POST'])
def convert(amount, base, to):
    url = f'https://api.ratesapi.io/api/latest?base={base}&symbols={to}'
    response = requests.get(url).json()
    amount = request.form['amount']
    base = request.form['base']
    to = request.form['to']
    result = request.form['result']
    return redirect(url_for('index', float(response[base][to])*float(amount)))

#can remove debug if you want -- but obv we need it
if __name__ == "__main__":
    app.run(debug=True)



#to test individual python code for logic uncomment the below and comment out all code above until app = Flask etc
# Then just run like normal python convertapp.py

#def convert(amount, base, to):
    #url = f'https://api.ratesapi.io/api/latest?base={base}&symbols={to}'
    #response = requests.get(url).json()
    #return float(response['rates'][to])*float(amount)


#if __name__ == "__main__":
    #if len(sys.argv) == 4:
        #amount = sys.argv[1]
        #base = sys.argv[2].upper()
        #to_currency = sys.argv[3].upper()

    #else:
        #amount = int(input("[*]Enter amount > "))
        #base = input("[*]Enter Base Currency > ").upper()
        #to_currency = input(
            #"[*]Enter the currency you need to convert in > ").upper()

    #result = convert(amount, base, to_currency)
    #print(result)

