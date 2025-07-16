#!/usr/bin/env python3
import requests
import json
import time

def test_api_endpoint(url, description):
    print(f"\n=== Testing {description} ===")
    print(f"URL: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)[:500]}...")
        else:
            print(f"Error Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    base_url = "http://localhost:5000/api"
    
    # Test endpoints
    test_api_endpoint(f"{base_url}/coins/list", "Coins List")
    test_api_endpoint(f"{base_url}/fear-greed-index", "Fear & Greed Index")
    test_api_endpoint(f"{base_url}/technical-analysis/BTCUSDT", "Technical Analysis for BTC")
    
    # Test trading calculator
    print(f"\n=== Testing Trading Calculator ===")
    try:
        calc_data = {
            "entry_price": 50000,
            "leverage": 10,
            "position_type": "long",
            "position_size": 1000
        }
        response = requests.post(f"{base_url}/trading-calculator", json=calc_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Error Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

