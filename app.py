from flask import Flask, request, render_template
import requests

app = Flask(__name__)
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjViYWVkZmMwLTRkNWEtNDhmMi1iNDY5LTY2NTAyNTQ3YzIwOCIsIm9yZ0lkIjoiNDAyMTkxIiwidXNlcklkIjoiNDEzMjgzIiwidHlwZUlkIjoiMzM2ZWJhMzctYzE2OS00YjMyLTllMzQtNWNiNWI5ODMxYWE2IiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3MjI0NzA2MDAsImV4cCI6NDg3ODIzMDYwMH0.vtkYPbUU4kkBQr0ily2NLEsFw4PzcflTRwKn1Rn7IP4"

# Helper function to call Moralis API
def call_moralis_api(endpoint, params=None):
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    url = f'https://deep-index.moralis.io/api/v2/{endpoint}'
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError as e:
            return {"error": "Failed to parse JSON response", "details": str(e)}
    else:
        return {"error": f"API request failed with status code {response.status_code}", "details": response.text}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_balances', methods=['POST'])
def get_balances():
    address = request.form['address']
    try:
        # Define API endpoints
        endpoints = {
            'wallet_balances': f'address/{address}/balance',
            'wallet_history': f'address/{address}/transactions',
            'wallet_net_worth': f'address/{address}/net_worth',
            'nfts': f'address/{address}/nfts',
            'erc20_balances': f'address/{address}/erc20',
            'erc20_balances_with_prices': f'address/{address}/erc20/prices',
            'erc20_allowance': f'address/{address}/erc20/allowance'
        }

        # Get data from APIs
        wallet_balances = call_moralis_api(endpoints['wallet_balances'])
        wallet_history = call_moralis_api(endpoints['wallet_history'])
        wallet_net_worth = call_moralis_api(endpoints['wallet_net_worth'])
        nfts = call_moralis_api(endpoints['nfts'])
        erc20_balances = call_moralis_api(endpoints['erc20_balances'])
        erc20_balances_with_prices = call_moralis_api(endpoints['erc20_balances_with_prices'])
        erc20_allowance = call_moralis_api(endpoints['erc20_allowance'])

        return render_template('index.html', 
                               balances=wallet_balances, 
                               history=wallet_history,
                               net_worth=wallet_net_worth,
                               nfts=nfts,
                               tokens=erc20_balances,
                               token_prices=erc20_balances_with_prices,
                               allowance=erc20_allowance)
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
