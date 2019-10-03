from flask import Flask, render_template, request, make_response
import feedparser
import json
import urllib
import urllib2
import datetime


app = Flask(__name__)

DEFAULTS = {'currency_from': 'CAD',
            'currency_to': 'USD'}

currency_url = "https://openexchangerates.org//api/latest.json?app_id=21046e5c3fa74c8a8847e0dd6c29934b"


@app.route("/")
def home():
   # get customized currency based on user input or default
    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rate(currency_from, currency_to)
    # save cookies and return template
    response = make_response(render_template("index.html",
                                             currency_from=currency_from,
                                             currency_to=currency_to,
                                             rate=rate,
                                             currencies=sorted(currencies)))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response


def get_rate(frm, to):
    all_currency = urllib2.urlopen(currency_url).read()
    parsed = json.loads(all_currency).get("rates")
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate / frm_rate, parsed.keys())


def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]


if __name__ == "__main__":
    app.run(debug=True)
