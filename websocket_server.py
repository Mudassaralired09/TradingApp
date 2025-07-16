import asyncio
import websockets
import json
import requests
import time
from datetime import datetime
import threading

class CryptoWebSocketServer:
    def __init__(self):
        self.clients = set()
        self.running = False
        self.data_cache = {}
        
    async def register(self, websocket):
        """Register a new client"""
        self.clients.add(websocket)
        print(f"Client connected. Total clients: {len(self.clients)}")
        
    async def unregister(self, websocket):
        """Unregister a client"""
        self.clients.discard(websocket)
        print(f"Client disconnected. Total clients: {len(self.clients)}")
        
    async def send_to_all(self, message):
        """Send message to all connected clients"""
        if self.clients:
            await asyncio.gather(
                *[client.send(message) for client in self.clients],
                return_exceptions=True
            )
    
    def fetch_price_data(self, symbol):
        """Fetch current price data from Binance"""
        try:
            url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol.upper()}USDT"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'symbol': symbol.upper(),
                    'price': float(data['lastPrice']),
                    'change': float(data['priceChange']),
                    'changePercent': float(data['priceChangePercent']),
                    'volume': float(data['volume']),
                    'high': float(data['highPrice']),
                    'low': float(data['lowPrice']),
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            print(f"Error fetching price data for {symbol}: {e}")
        return None
    
    def fetch_fear_greed_index(self):
        """Fetch Fear & Greed Index"""
        try:
            response = requests.get("https://api.alternative.me/fng/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data and 'data' in data and len(data['data']) > 0:
                    return {
                        'value': int(data['data'][0]['value']),
                        'classification': data['data'][0]['value_classification'],
                        'timestamp': datetime.now().isoformat()
                    }
        except Exception as e:
            print(f"Error fetching Fear & Greed Index: {e}")
        return None
    
    async def price_updater(self):
        """Background task to update prices"""
        symbols = ['BTC', 'ETH', 'BNB', 'SOL', 'ADA', 'DOGE', 'DOT', 'LINK', 'LTC', 'UNI']
        
        while self.running:
            try:
                # Update prices for all symbols
                price_updates = {}
                for symbol in symbols:
                    price_data = self.fetch_price_data(symbol)
                    if price_data:
                        price_updates[symbol] = price_data
                        self.data_cache[f"price_{symbol}"] = price_data
                
                if price_updates:
                    message = json.dumps({
                        'type': 'price_update',
                        'data': price_updates
                    })
                    await self.send_to_all(message)
                
                # Update Fear & Greed Index every 5 minutes
                if int(time.time()) % 300 == 0:  # Every 5 minutes
                    fg_data = self.fetch_fear_greed_index()
                    if fg_data:
                        self.data_cache['fear_greed'] = fg_data
                        message = json.dumps({
                            'type': 'fear_greed_update',
                            'data': fg_data
                        })
                        await self.send_to_all(message)
                
                await asyncio.sleep(10)  # Update every 10 seconds
                
            except Exception as e:
                print(f"Error in price updater: {e}")
                await asyncio.sleep(5)
    
    async def handle_client(self, websocket, path):
        """Handle individual client connections"""
        await self.register(websocket)
        
        # Send cached data to new client
        if self.data_cache:
            welcome_message = json.dumps({
                'type': 'welcome',
                'data': self.data_cache
            })
            await websocket.send(welcome_message)
        
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    
                    if data.get('type') == 'subscribe':
                        # Handle subscription requests
                        symbol = data.get('symbol', '').upper()
                        if symbol:
                            price_data = self.fetch_price_data(symbol)
                            if price_data:
                                response = json.dumps({
                                    'type': 'subscription_data',
                                    'symbol': symbol,
                                    'data': price_data
                                })
                                await websocket.send(response)
                    
                    elif data.get('type') == 'ping':
                        # Handle ping requests
                        pong_message = json.dumps({
                            'type': 'pong',
                            'timestamp': datetime.now().isoformat()
                        })
                        await websocket.send(pong_message)
                        
                except json.JSONDecodeError:
                    error_message = json.dumps({
                        'type': 'error',
                        'message': 'Invalid JSON format'
                    })
                    await websocket.send(error_message)
                    
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            await self.unregister(websocket)
    
    async def start_server(self, host='0.0.0.0', port=8765):
        """Start the WebSocket server"""
        self.running = True
        
        # Start background price updater
        asyncio.create_task(self.price_updater())
        
        print(f"Starting WebSocket server on {host}:{port}")
        
        async with websockets.serve(self.handle_client, host, port):
            await asyncio.Future()  # Run forever

def run_websocket_server():
    """Run the WebSocket server"""
    server = CryptoWebSocketServer()
    asyncio.run(server.start_server())

if __name__ == "__main__":
    run_websocket_server()

