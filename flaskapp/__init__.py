#! /usr/bin/env python
# -*- coding: utf-8 -*-
from indices_module import ndvi
from logic_module import coord2pixel
from flask import Flask
from flask import render_template, request, redirect
import requests
import json
from datetime import datetime
import jinja2


app = Flask(__name__)

@app.route("/")
def main():
    app_url = "https://magicink.bitrix24.ru/oauth/authorize/?response_type=code&client_id=b1e825a33cb7f7e4ce9ed894bf02b2ba&redirect_uri=http%3A%2F%2F93.170.100.46%3A8181"
    code = request.args.get("code")
    if code is None:
        return redirect(app_url)
    else:
        result = requests.get('https://magicink.bitrix24.ru/oauth/token/?grant_type=authorization_code&client_id=b1e825a33cb7f7e4ce9ed894bf02b2ba&client_secret=1603abfef4d8b0a95f3ce61d88b48780&code={0}&scope=user,crm&redirect_uri=http%3A%2F%2F93.170.100.46%3A8181'.format(code)).content
        result = json.loads(result)
        try:
            access_token = result['access_token']
            deals = requests.get('https://magicink.bitrix24.ru/rest/crm.deal.list.json?auth='+access_token).content
            deals = json.loads(deals)

            invoices = requests.get('https://magicink.bitrix24.ru/rest/crm.invoice.list.json?auth='+access_token).content
            invoices = json.loads(invoices)
            # ID to companies
            # for i in enumerate(invoices):
            #     i[1]['UF_COMPANY_ID'] = unicode("test")
            return render_template('template.html', deals=deals['result'], invoices=invoices['result'])
        except KeyError:
            return redirect(app_url)

def format_datetime(value):
    dt = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S+04:00').strftime('%d.%m.%Y')
    return dt
    
def company(value):
    company = requests.get('https://magicink.bitrix24.ru/rest/crm.company.get.json?id='+value+'&auth='+access_token).content
    company = json.loads(company)
    return company['result']['TITLE']

jinja2.filters.FILTERS['format_datetime'] = format_datetime
jinja2.filters.FILTERS['company'] = company

if __name__ == "__main__":
    app.debug = True
    app.run(host= '0.0.0.0', port=8181)
    # app.run(host= '0.0.0.0')