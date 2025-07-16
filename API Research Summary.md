# API Research Summary

## CoinGecko API
- **Purpose:** Fetching coin metadata (name, logo, market cap, volume, current price), Binance-listed coins, and contract address-based token recognition.
- **Endpoint for Coin List (ID Map):** `https://api.coingecko.com/api/v3/coins/list`
- **Authentication:** Free and open, no authentication key needed for public API.
- **Cache/Update Frequency (Public API):** Every 30 minutes.

## Binance API
- **Purpose:** Real-time candle and price data.
- **Endpoints:**
    - `https://api.binance.com/api/v3/klines` for Kline/candlestick data.
    - WebSocket streams are available for real-time updates (e.g., Kline/Candlestick Streams).
- **Authentication:** Public endpoints do not require authentication.

## Alternative.me Fear & Greed Index API
- **Purpose:** Fetching Fear & Greed Index data.
- **Endpoint:** `https://api.alternative.me/fng/`
- **Authentication:** Free and open, no authentication key needed.

## Next Steps:
- Research open-source TA libraries (TA-Lib, Tulip Indicators, Lightweight Charts).
- Research OCR and AI pattern detection libraries (Tesseract.js, EasyOCR, YOLOv5, Detectron2, OpenCV).
- Research NLP sentiment analysis libraries (TextBlob, HuggingFace Transformers).
- Research news APIs (CryptoPanic, NewsAPI, open RSS feeds).




## Technical Analysis Libraries
- **TA-Lib:** A C++ library with Python wrappers, widely used for technical analysis with over 150 indicators. Installation might require specific steps (e.g., using Anaconda).
- **`ta` (Technical Analysis Library in Python):** A Python library built on Pandas and Numpy for feature engineering from financial time series datasets. Easier to install than TA-Lib.
- **Lightweight Charts:** A free, open-source JavaScript library for creating interactive financial charts. Ideal for frontend visualization.

## OCR and AI Pattern Detection
- **Tesseract.js:** Pure Javascript OCR engine, suitable for browser-based OCR. Supports over 100 languages.
- **EasyOCR:** Ready-to-use OCR with 80+ supported languages, implemented in Python. Good for backend processing.
- **YOLOv5 (Ultralytics YOLOv5):** A popular object detection model, good for AI pattern detection. Requires Python and PyTorch.
- **Detectron2:** Facebook AI Research's platform for object detection, segmentation, and other visual recognition tasks. Also Python-based.
- **OpenCV:** A comprehensive open-source computer vision library, useful for various image processing tasks including pattern detection.

## Sentiment Analysis and News APIs
- **TextBlob:** A Python library for processing textual data, providing a simple API for NLP tasks like sentiment analysis.
- **HuggingFace Transformers:** A powerful library for state-of-the-art NLP models, including sentiment analysis. Offers pre-trained models.
- **CryptoPanic API:** Provides cryptocurrency news. Free tier available, requires API key for integration.
- **NewsAPI:** A simple HTTP REST API for searching and retrieving live articles from various news sources. Requires API key.
- **Open RSS Feeds:** Various cryptocurrency news websites offer RSS feeds (e.g., Cointelegraph, CCN.com). Can be used to aggregate news without specific API keys.

