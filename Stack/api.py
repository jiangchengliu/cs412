import requests
from .models import * 
from django.core.management.base import BaseCommand
import time

"""
use alpha vantage to retrieve stock data
"""

API_KEY = "08ab9bf22fmshf6a900ca9c8a6cfp134057jsn9f48f0c06ebf"  # Replace with your actual API key

def get_stock_data():
    # Predefined mapping of tickers to company names
    tickers_to_names = {
        "AAPL": "Apple Inc.",
        "MSFT": "Microsoft Corporation",
        "GOOGL": "Alphabet Inc.",
        "AMZN": "Amazon.com Inc.",
        "META": "Meta Platforms Inc.",
        "TSLA": "Tesla Inc.",
        "NVDA": "NVIDIA Corporation",
        "PYPL": "PayPal Holdings Inc.",
        "INTC": "Intel Corporation",
        "CSCO": "Cisco Systems Inc.",
        "AMD": "Advanced Micro Devices Inc.",
        "NFLX": "Netflix Inc.",
        "QCOM": "Qualcomm Inc.",
        "AVGO": "Broadcom Inc.",
        "CHTR": "Charter Communications Inc.",
        "TXN": "Texas Instruments Inc.",
        "MS": "Morgan Stanley",
        "INTU": "Intuit Inc.",
        "PEP": "PepsiCo Inc.",
        "ASML": "ASML Holding",
        "LULU": "Lululemon Athletica",
        "AMGN": "Amgen Inc.",
        "COST": "Costco Wholesale Corporation",
        "MRNA": "Moderna Inc.",
        "SBUX": "Starbucks Corporation",
        "WBA": "Walgreens Boots Alliance Inc.",
        "GILD": "Gilead Sciences Inc.",
        "REGN": "Regeneron Pharmaceuticals",
        "ISRG": "Intuitive Surgical Inc.",
        "BMRN": "BioMarin Pharmaceutical",
        "KLAC": "KLA Corporation",
        "ADI": "Analog Devices Inc.",
        "WDC": "Western Digital Corporation",
        "MU": "Micron Technology Inc.",
        "BIIB": "Biogen Inc.",
        "VRTX": "Vertex Pharmaceuticals",
        "EXC": "Exelon Corporation",
        "LRCX": "Lam Research Corporation",
        "MRVL": "Marvell Technology Inc.",
        "ATVI": "Activision Blizzard Inc.",
        "CSX": "CSX Corporation",
        "TTWO": "Take-Two Interactive",
        "FISV": "Fiserv Inc.",
        "ADBE": "Adobe Inc.",
        "MDLZ": "Mondelez International Inc.",
        "BIDU": "Baidu Inc.",
        "SNPS": "Synopsys Inc.",
        "FLEX": "Flex Ltd.",
        "ORLY": "O'Reilly Automotive Inc.",
        "CERN": "Cerner Corporation",
        "ZBRA": "Zebra Technologies Corporation",
        "ILMN": "Illumina Inc.",
        "SPLK": "Splunk Inc.",
        "NLOK": "NortonLifeLock Inc.",
        "TTD": "The Trade Desk Inc.",
        "SWKS": "Skyworks Solutions Inc.",
        "TRIP": "TripAdvisor Inc.",
        "AMAT": "Applied Materials Inc.",
        "BABA": "Alibaba Group",
        "CHKP": "Check Point Software Technologies",
        "RMD": "ResMed Inc.",
        "VRSK": "Verisk Analytics Inc.",
        "CTSH": "Cognizant Technology Solutions",
        "VZ": "Verizon Communications",
        "SIRI": "SiriusXM Holdings Inc.",
        "STX": "Seagate Technology Holdings",
        "IDXX": "IDEXX Laboratories Inc.",
        "TCOM": "Trip.com Group",
        "MXIM": "Maxim Integrated Products",
        "VOD": "Vodafone Group",
        "SYMC": "Symantec Corporation",
        "ORCL": "Oracle Corporation",
        "ALGN": "Align Technology Inc.",
        "NTRA": "Natera Inc.",
        "DOCU": "DocuSign Inc.",
        "PAYX": "Paychex Inc.",
        "TROW": "T. Rowe Price Group",
        "KHC": "Kraft Heinz Company",
        "NXPI": "NXP Semiconductors",
        "TMO": "Thermo Fisher Scientific Inc.",
        "UNH": "UnitedHealth Group",
        "SYF": "Synchrony Financial"
    }

    url = "https://alpha-vantage.p.rapidapi.com/query"
    
    for idx, ticker in enumerate(tickers_to_names):
        # Limit the number of requests to 5 per minute
        
        querystring = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "datatype": "json"
        }

        headers = {
            "x-rapidapi-key": API_KEY,
            "x-rapidapi-host": "alpha-vantage.p.rapidapi.com"
        }

        # Send the API request
        response = requests.get(url, headers=headers, params=querystring)

        # Print the JSON response with both stock data and company name
        if response.status_code == 200:
            stock_data = response.json()
            company_name = tickers_to_names[ticker]
            print(f"Stock data for {company_name} ({ticker}):")
            Stock.objects.delete
            Stock.objects.create(ticker=ticker, name = tickers_to_names[ticker], price=stock_data["Global Quote"]["05. price"])
            print("stock created")
        else:
            print(f"Failed to retrieve data for {ticker}. Status code: {response.status_code}")
        
        time.sleep(12)






    
    
    