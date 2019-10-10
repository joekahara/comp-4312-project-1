from flask import Flask, render_template, request, redirect
import requests


app = Flask(__name__)

@app.route("/", methods = ["GET","POST"])
def home():
    if request.method == "POST":
        url = "https://api.exchangeratesapi.io/latest?base=ILS"
        base = request.form.get("base")
        to = request.form.get("to")
        amount = request.form.get("amount")

        response = requests.get(url).json()
    
        baseRate = response["rates"][base]
        toRate = response["rates"][to]
        result = (toRate / baseRate) * float(amount)

        currencyInfo = dict()
        currencyInfo["base"] = base
        currencyInfo["to"] = to
        currencyInfo["amount"] = amount
        currencyInfo["result"] = round(result, 2)

        return render_template("index.html", info = currencyInfo)

    else:
        return render_template("index.html")

@app.route("/clear")
def reset():
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
