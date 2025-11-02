# AllYouNeedIsWheel

mphinance edits/additions 11/1/2025: swapped out Interactive Brokers for Snaptrade. Work in process

AllYouNeedIsWheel is a financial options trading assistant specifically designed for the "Wheel Strategy" that connects to Snaptrade. It helps traders analyze, visualize, and execute the wheel strategy effectively by retrieving portfolio data, analyzing options chains for cash-secured puts and covered calls, and presenting recommendations through a user-friendly web interface.
<img width="1680" alt="Screen Shot 2025-04-26 at 00 32 08" src="https://github.com/user-attachments/assets/d27d525e-1fb4-4494-b5be-eba17e774322" />
<img width="1321" alt="Screen Shot 2025-04-26 at 00 33 00" src="https://github.com/user-attachments/assets/24634bbf-3110-46fa-85c4-b05301e11a88" />
<img width="1311" alt="Screen Shot 2025-04-26 at 00 33 21" src="https://github.com/user-attachments/assets/0688ca0a-7fca-41fc-83b4-91881a2e9848" />
<img width="1309" alt="Screen Shot 2025-04-26 at 00 33 41" src="https://github.com/user-attachments/assets/3e029e78-406c-44d4-b557-39b55c691f8a" />
<img width="1500" alt="Screen Shot 2025-04-26 at 00 34 06" src="https://github.com/user-attachments/assets/12a6539c-f74a-4d18-b868-ac7bef766dc8" />
<img width="1357" alt="Screen Shot 2025-04-26 at 00 34 38" src="https://github.com/user-attachments/assets/d9b2f57f-606d-4f4f-9d83-08b933ba71da" />

## Features


- **Portfolio Dashboard**: View your current portfolio positions, value, and performance metrics
- **Wheel Strategy Focus**: Specialized tools for implementing the wheel strategy (selling cash-secured puts and covered calls)
- **Options Analysis**: Analyze option chains to find the best cash-secured puts and covered calls for any stock ticker
- **Trading Recommendations**: Get wheel strategy trade recommendations with projected premium income
- **Option Rollover Management**: Tool for rolling option positions approaching strike price to later expirations
- **Interactive Web Interface**: Modern, responsive web application with data visualizations
- **API Integration**: Backend API to interact with Interactive Brokers
- **Order Management**: Create, cancel, and execute wheel strategy option orders through the dashboard

## Prerequisites

- Python 3.10+
- Interactive Brokers TWS (Trader Workstation) or IB Gateway
- IB account with market data subscriptions for options

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/AllYouNeedIsWheel.git
   cd AllYouNeedIsWheel
   ```

2. Set up a virtual environment and install required dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
   *Note: The `run_api.py` script will automatically check and install all required dependencies from requirements.txt when run, including platform-specific dependencies like waitress (Windows) or gunicorn (Unix/Linux/Mac).*

3. Create your connection configuration file:
   ```bash
   cp connection.json.example connection.json
   ```

4. Edit `connection.json` with your Interactive Brokers connection details:
   ```json
   {
       "host": "127.0.0.1",
       "port": 7497,
       "client_id": 1,
       "readonly": true,
       "account_id": "YOUR_ACCOUNT_ID",
       "db_path": "options_dev.db",
       "comment": "Port 7496 for TWS, 7497 for IB Gateway. Set readonly to true for safety during testing."
   }
   ```

## Configuration

Two connection files can be maintained:
- `connection.json` - For paper trading (default)
- `connection_real.json` - For real-money trading

The key configuration parameters are:
- `host`: Usually "127.0.0.1" for local TWS/IB Gateway
- `port`: 7497 for IB Gateway paper trading, 7496 for TWS live trading
- `client_id`: Unique client ID (important if you have multiple connections)
- `readonly`: Set to `true` to prevent actual order execution (safer for testing)
- `db_path`: Path to the SQLite database file

## Interactive Brokers TWS/Gateway Configuration

Configure TWS/Gateway for API connections with these essential settings:

1. **Enable API**: 
   - TWS: File → Global Configuration → API → Settings
   - Gateway: Configure → Settings → API → Settings
   - Check "Enable ActiveX and Socket Clients"
   - Uncheck "Read-Only API" if you want to execute trades (required for orders)

2. **Socket Port**: 
   - Set to match your config file (7496 for TWS, 7497 for Gateway)

3. **Trusted IPs**:
   - Add "127.0.0.1" to trusted IPs if running locally

4. **Data Subscriptions**:
   - Ensure you have market data subscriptions for options

Note: TWS/Gateway must be running and logged in for the API to function.

## Usage

### Starting the Development Server

```bash
# For paper trading (default)
python3 run_api.py
```
### Starting the Production API Server

```bash
# For real money trading
python3 run_api.py --realmoney
```

This will start the application on http://localhost:8000


By default, the server will run on port 8000 with 4 workers. You can change these settings with environment variables:

```bash
# Change port and worker count
PORT=8080 WORKERS=2 python3 run_api.py
```

### API Endpoints

- **Portfolio**: 
  - GET `/api/portfolio/` - Get current portfolio positions and account data

- **Options**:
  - GET `/api/options/<ticker>` - Get option chain for ticker
  - GET `/api/options/<ticker>/<expiration>` - Get option chain for specific expiration date

- **Orders**:
  - GET `/api/options/orders` - Get orders with optional filters
  - POST `/api/options/order` - Create a new order
  - DELETE `/api/options/order/<order_id>` - Cancel an order
  - PUT `/api/options/order/<order_id>` - Update an order status
  - POST `/api/options/execute/<order_id>` - Execute an order through TWS
  - POST `/api/options/rollover` - Create rollover orders (close current position and open new one)

- **Stock Data**:
  - GET `/api/stock/<ticker>` - Get stock price and basic data

### Web Interface

The web interface consists of five main pages:

1. **Dashboard** (http://localhost:8000/): Overview of your portfolio and key metrics
2. **Portfolio** (http://localhost:8000/portfolio): Detailed view of all positions
3. **Rollover** (http://localhost:8000/rollover): Interface for managing option positions approaching strike price

### Frozen Data

The application automatically uses frozen data from Interactive Brokers in the following scenarios:
- When the market is closed (outside of 9:30 AM - 4:00 PM ET, Monday-Friday)
- On weekends and market holidays

Frozen data is actual historical data provided by Interactive Brokers rather than generated mock data. This ensures that all data provided by the application represents real market conditions even when markets are closed.

When no connection to Interactive Brokers TWS/IB Gateway is available or when API requests fail for any reason, the application will return appropriate error messages rather than falling back to mock data.

The application clearly indicates when it's using frozen data in the UI to avoid confusion with real-time market data.

## Project Structure

```
AllYouNeedIsWheel/
├── api/                      # Flask API backend
│   ├── __init__.py           # API initialization and factory function
│   ├── routes/               # API route modules
│   ├── services/             # Business logic for API
│   └── models/               # Data models
├── core/                     # Core trading functionality
│   ├── __init__.py
│   ├── connection.py         # Interactive Brokers connection handling
│   ├── logging_config.py     # Logging configuration
│   └── utils.py              # Utility functions
├── db/                       # Database operations
│   ├── __init__.py
│   └── database.py           # SQLite database wrapper
├── frontend/                 # Frontend web application
│   ├── static/               # Static assets (CSS, JS)
│   └── templates/            # Jinja2 HTML templates
├── logs/                     # Log files directory
├── app.py                    # Main Flask application entry point
├── run_api.py                # Production API server runner (cross-platform)
├── config.py                 # Configuration handling
├── connection.json           # IB connection configuration (paper trading)
├── connection_real.json      # IB connection configuration (real money)
├── connection.json.example   # Example configuration template
├── options_dev.db            # Development database (SQLite)
├── requirements.txt          # Python dependencies
└── .gitignore                # Git ignore rules
```

## Development

### Adding New Features

1. For backend changes, add routes in `api/routes/` and implement business logic in `api/services/`
2. For frontend changes, modify the templates in `frontend/templates/` and static assets in `frontend/static/`
3. For database changes, update the schema and queries in `db/database.py`

### Database

The application uses SQLite for storage. Two database files are maintained:
- `options_dev.db` - For development/testing
- `options_prod.db` - For production use

## Troubleshooting

### Connection Issues

- Ensure TWS or IB Gateway is running and API connections are enabled
- Verify the correct port (7496 for TWS, 7497 for IB Gateway)
- Check that the client ID is not already in use
- Confirm you have the right market data subscriptions for options

### Common Errors

- "Socket Connection Broken": TWS/IB Gateway is not running
- "Client ID already in use": Another application is using the same client ID
- "No market data permissions": You need to subscribe to market data for the securities you're requesting
- "ModuleNotFoundError: No module named 'fcntl'": This is a Windows-specific issue. The script will automatically install waitress as an alternative to gunicorn when run on Windows, or you can install it manually with `pip install waitress`

## Security Notes

- Never commit `connection_real.json` to version control (it's in `.gitignore`)
- Always use `readonly: true` during development to prevent accidental order execution
- Use caution when running with the `--realmoney` flag as real trades can be executed

## License

[Apache License 2.0](LICENSE)

## Acknowledgments

- [IB Async](https://github.com/ib-api-reloaded/ib_async) for Interactive Brokers API integration
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Gunicorn](https://gunicorn.org/) for WSGI HTTP server
- [Waitress](https://docs.pylonsproject.org/projects/waitress/) for Windows-compatible WSGI HTTP server
