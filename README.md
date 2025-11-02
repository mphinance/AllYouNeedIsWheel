# AllYouNeedIsWheel

mphinance edits/additions 11/1/2025: swapped out Interactive Brokers for Snaptrade. Work in process

Credit to https://github.com/xiao81 for original

AllYouNeedIsWheel is a financial options trading assistant specifically designed for the "Wheel Strategy" that connects to Snaptrade. It helps traders analyze, visualize, and execute the wheel strategy effectively by retrieving portfolio data, analyzing options chains for cash-secured puts and covered calls, and presenting recommendations through a user-friendly web interface.
<img width="1680" alt="Screen Shot 2025-04-26 at 00 32 08" src="https://github.com/user-attachments/assets/d27d525e-1fb4-4494-b5be-eba17e774322" />
<img width="1321" alt="Screen Shot 2025-04-26 at 00 33 00" src="https://github.com/user-attachments/assets/24634bbf-3110-46fa-85c4-b05301e11a88" />
<img width="1311" alt="Screen Shot 2025-04-26 at 00 33 21" src="https://github.com/user-attachments/assets/0688ca0a-7fca-41fc-83b4-91881a2e9848" />
<img width="1309" alt="Screen Shot 2025-04-26 at 00 33 41" src="https://github.com/user-attachments/assets/3e029e78-406c-44d4-b557-39b55c691f8a" />
<img width="1500" alt="Screen Shot 2025-04-26 at 00 34 06" src="https://github.com/user-attachments/assets/12a6539c-f74a-4d18-b868-ac7bef766dc8" />
<img width="1357" alt="Screen Shot 2025-04-26 at 00 34 38" src="https://github.com/user-attachments/assets/d9b2f57f-606d-4f4f-9d83-08b933ba71da" />
# **All You Need Is Wheel**

A financial options trading assistant for the "Wheel Strategy", powered by a Flask backend and a modern JavaScript frontend. This version uses the [SnapTrade API](https://snaptrade.com/) to connect with multiple brokerage accounts (like Webull, Robinhood, Alpaca, and more) to pull in portfolio data.

This project was adapted from an Interactive Brokers-specific tool and refactored to be broker-agnostic.

## **Features**

* **Portfolio Dashboard**: View your current portfolio value, cash balance, and margin metrics.  
* **Multi-Broker Support**: Securely connect to and pull data from multiple brokerages using the SnapTrade API.  
* **Live Position Tracking**: The dashboard populates with your live stock and option positions.  
* **Broker Connection Management**: A simple UI to "Connect Broker" (which initiates the SnapTrade login flow) and "Disconnect Broker" (which revokes access).  
* **Rollover Page**: A dedicated page for viewing option positions and (in the future) managing rollovers.  
* **Local Order Management**: A database and UI to queue up potential trades (Note: trade execution via SnapTrade is not yet implemented).

## **Prerequisites**

* Python 3.10+  
* A [SnapTrade Partner Account](https://docs.snaptrade.com/demo/getting-started) to get your API keys.  
* A brokerage account supported by SnapTrade (e.g., Webull, Alpaca, etc.).

## **Installation**

1. Clone this repository:  
   git clone \[https://github.com/mphinance/AllYouNeedIsWheel.git\](https://github.com/mphinance/AllYouNeedIsWheel.git)  
   cd AllYouNeedIsWheel

2. Set up a virtual environment and activate it:  
   python3 \-m venv venv  
   source venv/bin/activate  \# On Windows: venv\\Scripts\\activate

3. Install all required dependencies:  
   pip install \-r requirements.txt

## **Configuration (Important\!)**

This project uses a connection.json file for all API keys and user credentials.

1. Create this file in the root directory:  
   cp connection.json.example connection.json

2. Edit connection.json with your credentials:  
   {  
     "comment": "SnapTrade API Credentials",  
     "snaptrade\_client\_id": "YOUR\_CLIENT\_ID\_FROM\_SNAPTRADE\_PORTAL",  
     "snaptrade\_consumer\_key": "YOUR\_CONSUMER\_KEY\_FROM\_SNAPTRADE\_PORTAL",

     "comment\_user": "These are credentials YOU create for your user",  
     "snaptrade\_user\_id": "a-unique-id-for-you",  
     "app\_base\_url": "\[http://127.0.0.1:6001\](http://127.0.0.1:6001)",

     "comment\_secret": "This key will be auto-generated and saved here",  
     "snaptrade\_user\_secret": null,

     "db\_path": "options.db"  
   }

   * snaptrade\_client\_id: Get this from your SnapTrade Partner Portal.  
   * snaptrade\_consumer\_key: Get this from your SnapTrade Partner Portal.  
   * snaptrade\_user\_id: This is a **unique ID you create** for yourself (e.g., "my-wheel-app" or "mphinance-user").  
   * app\_base\_url: The URL where you are running the app. This is crucial for the redirect after you log in.  
   * snaptrade\_user\_secret: **Leave this as null**. The application will automatically generate this secret on your first login and save it to this file.

## **How to Run**

1. Start the Flask server:  
   python3 run\_api.py

   The server will start on port 6001 (or as specified in run\_api.py).  
2. Open the application in your browser at the app\_base\_url you set (e.g., http://127.0.0.1:6001).  
3. Click the **"Connect Broker"** button in the navigation bar.  
4. You will be redirected to the SnapTrade Connect modal. Select your broker (e.g., Webull) and log in securely.  
5. After a successful login, SnapTrade will redirect you back to your app\_base\_url.  
6. Your portfolio dashboard will now load your account summary and positions.  
   (Note: The very first sync with SnapTrade can sometimes take a few minutes. If your portfolio is empty, wait 5 minutes and hard-refresh the page.)

### **Disconnecting a Broker**

To log out or switch brokers, click the **"Disconnect Broker"** button. This will call the SnapTrade API to remove all brokerage connections associated with your user\_id. You can then click "Connect Broker" again to link a new account.

## **Future Enhancements (Disabled Features)**

This project was originally built for Interactive Brokers, which provided both portfolio data and market data. SnapTrade only provides portfolio data.

The **"Option Opportunities"** section of the dashboard is currently disabled. The backend code (api/services/options\_service.py) is stubbed out. To re-enable this feature, you would need to integrate a third-party market data provider (like Polygon.io, Alpaca, or IEX Cloud) to fetch live option chain data.

## **Project Structure**

AllYouNeedIsWheel/  
├── api/                      \# Flask API backend  
│   ├── \_\_init\_\_.py  
│   ├── routes/               \# API route modules (portfolio.py, snaptrade.py, etc.)  
│   └── services/             \# Business logic (portfolio\_service.py, etc.)  
├── core/                     \# Core backend functionality  
│   ├── \_\_init\_\_.py  
│   ├── connection.py         \# SnapTrade connection client  
│   ├── logging\_config.py     \# Logging configuration  
│   └── utils.py              \# Utility functions  
├── db/                       \# Database operations  
│   └── database.py           \# SQLite database wrapper  
├── frontend/                 \# Frontend web application  
│   ├── static/               \# Static assets (CSS, JS)  
│   └── templates/            \# Jinja2 HTML templates  
├── logs/                     \# Log files directory  
├── app.py                    \# Main Flask application entry point  
├── run\_api.py                \# Production API server runner (cross-platform)  
├── config.py                 \# Configuration handling  
├── connection.json           \# Your private credentials (DO NOT COMMIT)  
├── connection.json.example   \# Template for connection.json  
├── requirements.txt          \# Python dependencies  
└── .gitignore

## **Acknowledgments**

* [SnapTrade](https://snaptrade.com/) for the brokerage aggregation API.  
* [Flask](https://flask.palletsprojects.com/) for the web framework.  
* [Gunicorn](https://gunicorn.org/) & [Waitress](https://docs.pylonsproject.org/projects/waitress/) for the WSGI server.
