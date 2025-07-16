from flask import Blueprint, jsonify, request
import requests
import pandas as pd
import numpy as np
from ta import add_all_ta_features
from ta.utils import dropna
import json
from datetime import datetime, timedelta

crypto_bp = Blueprint('crypto', __name__)

# CoinGecko API base URL
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

# Binance API base URL
BINANCE_BASE_URL = "https://api.binance.com/api/v3"

# Alternative.me Fear & Greed Index API
FEAR_GREED_URL = "https://api.alternative.me/fng/"

@crypto_bp.route('/coins/list', methods=['GET'])
def get_coins_list():
    """Get list of all coins from CoinGecko"""
    try:
        response = requests.get(f"{COINGECKO_BASE_URL}/coins/list")
        if response.status_code == 200:
            coins = response.json()
            # Filter to get only top coins or Binance-listed coins for better performance
            return jsonify({"success": True, "data": coins[:500]})  # Limit to first 500
        else:
            return jsonify({"success": False, "error": "Failed to fetch coins list"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@crypto_bp.route('/coin/<coin_id>', methods=['GET'])
def get_coin_data(coin_id):
    """Get detailed coin data from CoinGecko"""
    try:
        response = requests.get(f"{COINGECKO_BASE_URL}/coins/{coin_id}")
        if response.status_code == 200:
            coin_data = response.json()
            return jsonify({"success": True, "data": coin_data})
        else:
            return jsonify({"success": False, "error": "Coin not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@crypto_bp.route('/coin/contract/<contract_address>', methods=['GET'])
def get_coin_by_contract(contract_address):
    """Get coin data by contract address"""