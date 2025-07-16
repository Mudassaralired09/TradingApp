from flask import Blueprint, jsonify, request
import requests
import json
from datetime import datetime

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
        # Return a simple hardcoded list for testing
        sample_coins = [
            {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"},
            {"id": "ethereum", "symbol": "eth", "name": "Ethereum"},
            {"id": "binancecoin", "symbol": "bnb", "name": "BNB"},
            {"id": "solana", "symbol": "sol", "name": "Solana"},
            {"id": "cardano", "symbol": "ada", "name": "Cardano"},
            {"id": "dogecoin", "symbol": "doge", "name": "Dogecoin"},
            {"id": "polkadot", "symbol": "dot", "name": "Polkadot"},
            {"id": "chainlink", "symbol": "link", "name": "Chainlink"},
            {"id": "litecoin", "symbol": "ltc", "name": "Litecoin"},
            {"id": "uniswap", "symbol": "uni", "name": "Uniswap"}
        ]
        return jsonify({"success": True, "data": sample_coins})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@crypto_bp.route('/fear-greed-index', methods=['GET'])
def get_fear_greed_index():
    """Get Fear & Greed Index from Alternative.me"""
    try:
        # Return sample data for testing
        sample_data = {
            "name": "Fear and Greed Index",
            "data": [
                {
                    "value": "73",
                    "value_classification": "Greed",
                    "timestamp": "1642204800",
                    "time_until_update": "86400"
                }
            ]
        }
        return jsonify({"success": True, "data": sample_data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@crypto_bp.route('/technical-analysis/<symbol>', methods=['GET'])
def get_technical_analysis(symbol):
    """Get technical analysis indicators"""
    try:
        # Return sample technical data for testing
        sample_indicators = {
            'rsi': 65.5,
            'macd': 0.0012,
            'macd_signal': 0.0008,
            'bb_upper': 52000.0,
            'bb_middle': 50000.0,
            'bb_lower': 48000.0,
            'ema_12': 50500.0,
            'ema_26': 49800.0,
            'sma_20': 50200.0,
            'sma_50': 49500.0,
            'volume_sma': 1500000.0,
            'stoch_k': 70.2,
            'stoch_d': 68.5,
            'current_price': 50000.0
        }
        
        return jsonify({"success": True, "data": sample_indicators})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@crypto_bp.route('/trading-calculator', methods=['POST'])
def trading_calculator():
    """Calculate trading levels (liquidation, stop loss, take profit)"""
    try:
        data = request.get_json()
        
        entry_price = float(data.get('entry_price', 0))
        leverage = float(data.get('leverage', 1))
        position_type = data.get('position_type', 'long').lower()  # 'long' or 'short'
        position_size = float(data.get('position_size', 0))
        
        if entry_price <= 0 or leverage <= 0:
            return jsonify({"success": False, "error": "Invalid entry price or leverage"}), 400
        
        # Calculate liquidation price
        if position_type == 'long':
            liquidation_price = entry_price * (1 - (1 / leverage))
            stop_loss = entry_price * 0.97  # 3% below entry
            take_profit = entry_price * 1.05  # 5% above entry
        else:  # short
            liquidation_price = entry_price * (1 + (1 / leverage))
            stop_loss = entry_price * 1.03  # 3% above entry
            take_profit = entry_price * 0.95  # 5% below entry
        
        # Calculate PnL at different levels
        if position_size > 0:
            if position_type == 'long':
                sl_pnl = (stop_loss - entry_price) * position_size * leverage
                tp_pnl = (take_profit - entry_price) * position_size * leverage
            else:
                sl_pnl = (entry_price - stop_loss) * position_size * leverage
                tp_pnl = (entry_price - take_profit) * position_size * leverage
        else:
            sl_pnl = 0
            tp_pnl = 0
        
        result = {
            'entry_price': entry_price,
            'leverage': leverage,
            'position_type': position_type,
            'liquidation_price': round(liquidation_price, 6),
            'stop_loss': round(stop_loss, 6),
            'take_profit': round(take_profit, 6),
            'sl_pnl': round(sl_pnl, 2),
            'tp_pnl': round(tp_pnl, 2),
            'risk_reward_ratio': round(abs(tp_pnl / sl_pnl) if sl_pnl != 0 else 0, 2)
        }
        
        return jsonify({"success": True, "data": result})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@crypto_bp.route('/ai-prediction/<symbol>', methods=['GET'])
def get_ai_prediction(symbol):
    """Generate AI-based trend prediction"""
    try:
        # Simple rule-based prediction for testing
        result = {
            'symbol': symbol.upper(),
            'prediction': 'LONG',
            'confidence': 75.5,
            'explanation': 'RSI indicates oversold conditions. MACD is above signal line (bullish). Fear & Greed Index shows moderate greed.',
            'technical_data': {
                'rsi': 65.5,
                'macd': 0.0012,
                'current_price': 50000.0
            },
            'fear_greed_index': 73,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({"success": True, "data": result})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

