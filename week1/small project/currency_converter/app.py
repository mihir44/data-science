import streamlit as st
from PIL import Image
import pandas as pd
import requests
import json

st.title("Currency Converter App")
st.markdown('''
    This app converts the value of foregin currency
''')

st.sidebar.header("Inputs")

currency_list = ['AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'GBP', 'HKD', 'HRK', 'HUF', 
'IDR', 'ILS', 'INR', 'ISK', 'JPY', 'KRW', 'MXN', 'MYR', 'NOK', 'NZD', 'PHP', 'PLN', 'RON', 'RUB', 'SEK', 'SGD', 'THB', 'TRY', 'USD', 'ZAR']

base_price_unit = st.sidebar.selectbox("Select base currency for conversion",currency_list)
symbols_price_unit = st.sidebar.selectbox("Select target currency to convert to",currency_list)

@st.cache
def load_data():
    url = ''.join(['https://api.fastforex.io/fetch-one?from=', base_price_unit, '&to=', symbols_price_unit,'&api_key=afc1c474aa-20db327ca8-r21bes'])
    response = requests.get(url)
    data = response.json()
    base_currency = pd.Series( data['base'], name='base_currency')
    rates_df = pd.DataFrame.from_dict( data['result'].items() )
    rates_df.columns = ['converted_currency', 'price']
    conversion_date = pd.Series( data['updated'].split(" ")[0], name='date' )
    df = pd.concat( [base_currency, rates_df, conversion_date], axis=1 )
    return df

df = load_data()

st.header("Currency conversion")
st.write(df)