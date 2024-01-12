import requests

def get_conversion_rate(from_currency, to_currency, api_key):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"


    headers = {
        'X-CMC_PRO_API_KEY': api_key,
        'Accepts': 'application/json'
    }
    parameters = {
        'symbol': ','.join([from_currency, to_currency])
    }
    
    
    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()

    from_price = data['data'][from_currency]['quote']['USD']['price']
    to_price = data['data'][to_currency]['quote']['USD']['price']

    rate = from_price / to_price
    return rate

def convert_crypto(amount, from_currency, to_currency, api_key):
    rate = get_conversion_rate(from_currency, to_currency, api_key)
    converted_amount = amount * rate
    return converted_amount


api_key = "39a10038-46ef-40df-840f-87a402232775" #API 
amount = 2 
from_currency = "BTC" 
to_currency = "USDT" 

converted_amount = convert_crypto(amount, from_currency, to_currency, api_key)
print(f"{amount} {from_currency} is equal to {converted_amount:.4f} {to_currency}")
