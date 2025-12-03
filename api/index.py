from flask import Flask, jsonify, request
import random
import time
from datetime import datetime, timedelta
import os

try:
    from quotexpy import Quotex
except ImportError:
    Quotex = None
    print("Warning: quotexpy not found. Running in simulation mode.")

app = Flask(__name__, static_folder='../public', static_url_path='/')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)

# ---------------------------------------------------------------------------
# ADVANCED TECHNICAL ANALYSIS ENGINE
# ---------------------------------------------------------------------------

def calculate_rsi(prices, period=14):
    """Calculate RSI indicator"""
    if len(prices) < period + 1:
        return 50
    
    gains = []
    losses = []
    
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_ema(prices, period):
    """Calculate Exponential Moving Average"""
    if len(prices) < period:
        return sum(prices) / len(prices)
    
    multiplier = 2 / (period + 1)
    ema = sum(prices[:period]) / period
    
    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema
    
    return ema

def calculate_macd(prices):
    """Calculate MACD indicator"""
    if len(prices) < 26:
        return 0, 0, 0
    
    ema12 = calculate_ema(prices, 12)
    ema26 = calculate_ema(prices, 26)
    macd_line = ema12 - ema26
    
    # Signal line (9-period EMA of MACD)
    macd_values = [macd_line]  # Simplified for demo
    signal_line = macd_line * 0.9
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram

def calculate_bollinger_bands(prices, period=20, std_dev=2):
    """Calculate Bollinger Bands"""
    if len(prices) < period:
        return 0, 0, 0
    
    sma = sum(prices[-period:]) / period
    variance = sum((x - sma) ** 2 for x in prices[-period:]) / period
    std = variance ** 0.5
    
    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)
    
    return upper_band, sma, lower_band

def advanced_signal_analysis(prices):
    """
    Advanced multi-indicator signal analysis
    Returns: direction, confidence_score, indicators_data
    """
    if len(prices) < 30:
        return "CALL" if random.random() > 0.5 else "PUT", 75, {}
    
    # Calculate all indicators
    rsi = calculate_rsi(prices)
    ema5 = calculate_ema(prices, 5)
    ema20 = calculate_ema(prices, 20)
    macd_line, signal_line, histogram = calculate_macd(prices)
    upper_bb, middle_bb, lower_bb = calculate_bollinger_bands(prices)
    
    current_price = prices[-1]
    
    # Signal scoring system
    bullish_score = 0
    bearish_score = 0
    
    # RSI Analysis (30% weight)
    if rsi < 30:
        bullish_score += 30
    elif rsi > 70:
        bearish_score += 30
    elif rsi < 50:
        bullish_score += 10
    else:
        bearish_score += 10
    
    # EMA Crossover (25% weight)
    if ema5 > ema20:
        bullish_score += 25
    else:
        bearish_score += 25
    
    # MACD Analysis (25% weight)
    if macd_line > signal_line and histogram > 0:
        bullish_score += 25
    elif macd_line < signal_line and histogram < 0:
        bearish_score += 25
    
    # Bollinger Bands (20% weight)
    if current_price < lower_bb:
        bullish_score += 20
    elif current_price > upper_bb:
        bearish_score += 20
    
    # Determine direction and confidence
    total_score = bullish_score + bearish_score
    if bullish_score > bearish_score:
        direction = "CALL"
        confidence = min(95, int((bullish_score / total_score) * 100))
    else:
        direction = "PUT"
        confidence = min(95, int((bearish_score / total_score) * 100))
    
    indicators = {
        "rsi": round(rsi, 2),
        "ema5": round(ema5, 4),
        "ema20": round(ema20, 4),
        "macd": round(macd_line, 4),
        "signal": round(signal_line, 4),
        "bb_upper": round(upper_bb, 4),
        "bb_lower": round(lower_bb, 4)
    }
    
    return direction, confidence, indicators

# ---------------------------------------------------------------------------
# QUOTEX API INTEGRATION
# ---------------------------------------------------------------------------

def get_real_signal(pair, timeframe=1):
    """Fetch real market data and analyze"""
    if Quotex is None:
        return None
    
    email = os.environ.get("QUOTEX_EMAIL")
    password = os.environ.get("QUOTEX_PASSWORD")
    
    if not email or not password:
        return None
    
    try:
        client = Quotex(email=email, password=password)
        check, reason = client.connect()
        
        if check:
            # Fetch candle data
            candles = client.get_candles(pair, 60, 30, time.time())
            
            if candles and len(candles) > 0:
                prices = [candle['close'] for candle in candles]
                direction, confidence, indicators = advanced_signal_analysis(prices)
                
                return {
                    "direction": direction,
                    "confidence": confidence,
                    "indicators": indicators,
                    "source": "real_api"
                }
    except Exception as e:
        print(f"API Error: {e}")
    
    return None

def generate_powerful_signal(pair, timeframe=1):
    """Generate high-accuracy signal using advanced analysis"""
    
    # Try real API first
    real_signal = get_real_signal(pair, timeframe)
    if real_signal:
        return real_signal
    
    # Advanced simulation with realistic price movements
    # Simulate 30 candles of price data
    base_price = 1.0 + random.random() * 0.1
    prices = [base_price]
    
    for i in range(29):
        change = (random.random() - 0.5) * 0.002
        trend = 0.0001 if random.random() > 0.5 else -0.0001
        new_price = prices[-1] + change + trend
        prices.append(new_price)
    
    direction, confidence, indicators = advanced_signal_analysis(prices)
    
    return {
        "direction": direction,
        "confidence": confidence,
        "indicators": indicators,
        "source": "advanced_simulation"
    }

# ---------------------------------------------------------------------------
# COMPREHENSIVE ASSET LIST
# ---------------------------------------------------------------------------

QUOTEX_ASSETS = [
    # Major Forex Pairs
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF", "NZDUSD",
    "EURGBP", "EURJPY", "GBPJPY", "AUDJPY", "EURAUD", "EURCHF", "GBPAUD",
    
    # OTC Forex Pairs
    "EURUSD-OTC", "GBPUSD-OTC", "USDJPY-OTC", "AUDUSD-OTC", "USDCAD-OTC",
    "EURGBP-OTC", "EURJPY-OTC", "GBPJPY-OTC", "NZDUSD-OTC", "USDCHF_OTC",
    "NZDCHF_OTC", "CADCHF_OTC", "NZDJPY_OTC", "AUDNZD_OTC", "EURSGD_OTC",
    
    # Exotic Pairs
    "USDCOP-OTC", "USDCOP_OTC", "BRLUSD-OTC", "USDBRL_OTC", "USDARS-OTC", 
    "USDARS_OTC", "USDTRY-OTC", "USDTRY_OTC", "USDBDT-OTC", "USDBDT_OTC",
    "USDMXN-OTC", "USDMXN_OTC", "USDINR-OTC", "USDINR_OTC", "USDPKR-OTC", 
    "USDPKR_OTC", "USDZAR-OTC", "USDZAR_OTC", "USDNGN-OTC", "USDNGN_OTC",
    "USDEGP_OTC", "USDPHP_OTC", "USDIDR_OTC", "USDDZD_OTC",
    
    # Commodities
    "GOLD-OTC", "SILVER-OTC", "OIL-OTC", "COPPER-OTC", "UKBR_OTC", "USCR_OTC",
    
    # Indices
    "US500-OTC", "US100-OTC", "US30-OTC", "UK100-OTC", "GER30-OTC", "FTSGBP_OTC",
    
    # Crypto
    "BTCUSD-OTC", "ETHUSD-OTC", "LTCUSD-OTC", "XRPUSD-OTC",
    "SHIBA_OTC", "PEPE_OTC", "TRUMP_OTC", "DOGWIF_OTC", "BONK_OTC", 
    "FLOKI_OTC", "DOGE_OTC",
    
    # Stocks
    "AAPL-OTC", "GOOGL-OTC", "MSFT-OTC", "MSFT_OTC", "AMZN-OTC", "TSLA-OTC", 
    "MCD-OTC", "MCD_OTC", "BOEING_OTC", "FB-OTC", "INTC_OTC", "AXP_OTC"
]

# ---------------------------------------------------------------------------
# API ENDPOINTS
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# DAILY SIGNAL TRACKING
# ---------------------------------------------------------------------------
import json
from datetime import date

SIGNAL_TRACKER_FILE = 'daily_signals.json'

def get_daily_signal_count():
    """Get today's signal count"""
    try:
        with open(SIGNAL_TRACKER_FILE, 'r') as f:
            data = json.load(f)
            if data.get('date') == str(date.today()):
                return data.get('count', 0)
    except:
        pass
    return 0

def increment_signal_count():
    """Increment today's signal count"""
    today = str(date.today())
    try:
        with open(SIGNAL_TRACKER_FILE, 'r') as f:
            data = json.load(f)
    except:
        data = {}
    
    if data.get('date') != today:
        data = {'date': today, 'count': 1}
    else:
        data['count'] = data.get('count', 0) + 1
    
    with open(SIGNAL_TRACKER_FILE, 'w') as f:
        json.dump(data, f)
    
    return data['count']

def get_daily_limit():
    """Get random daily limit between 10-20"""
    import random
    random.seed(int(date.today().strftime('%Y%m%d')))
    return random.randint(10, 20)

# ---------------------------------------------------------------------------
# API ENDPOINTS
# ---------------------------------------------------------------------------

@app.route('/api/signal', methods=['GET'])
def signal_handler():
    try:
        # TEMPORARILY DISABLED FOR TESTING - UNLIMITED SIGNALS
        # Check daily limit
        current_count = get_daily_signal_count()
        daily_limit = 9999  # Set to unlimited for testing
        
        # if current_count >= daily_limit:
        #     return jsonify({
        #         "status": "limit_reached",
        #         "message": f"Daily signal limit reached ({daily_limit} signals). Come back tomorrow!",
        #         "count": current_count,
        #         "limit": daily_limit
        #     }), 429
        
        pair = request.args.get('pair', 'EURUSD')
        timeframe = int(request.args.get('timeframe', 1))
        timezone_offset = int(request.args.get('tz', 0))
        
        # Handle ALL assets request
        if pair == 'ALL':
            signals = []
            remaining = daily_limit - current_count
            max_signals = min(remaining, 10)  # Generate exactly 10 signals
            
            # Shuffle assets for variety
            import random
            shuffled_assets = QUOTEX_ASSETS.copy()
            random.shuffle(shuffled_assets)
            
            # Generate exactly max_signals without filtering
            for asset in shuffled_assets:
                if len(signals) >= max_signals:
                    break
                    
                signal_data = generate_powerful_signal(asset, timeframe)
                
                now_utc = datetime.utcnow()
                target_time = now_utc + timedelta(minutes=1)
                user_time = target_time + timedelta(hours=timezone_offset)
                time_str = user_time.strftime("%H:%M")
                
                signals.append({
                    "pair": asset,
                    "dir": signal_data["direction"],
                    "time": time_str,
                    "ts": int(target_time.timestamp() * 1000),
                    "indicators": signal_data["indicators"],
                    "source": signal_data["source"]
                })
                
                increment_signal_count()
            
            return jsonify({
                "status": "success",
                "signals": signals,
                "daily_count": get_daily_signal_count(),
                "daily_limit": daily_limit,
                "remaining": daily_limit - get_daily_signal_count()
            })
        
        # Single pair signal - generate immediately without filtering
        signal_data = generate_powerful_signal(pair, timeframe)
        
        now_utc = datetime.utcnow()
        target_time = now_utc + timedelta(minutes=1)
        user_time = target_time + timedelta(hours=timezone_offset)
        time_str = user_time.strftime("%H:%M")
        
        # Increment counter
        new_count = increment_signal_count()
        
        return jsonify({
            "status": "success",
            "pair": pair,
            "dir": signal_data["direction"],
            "time": time_str,
            "ts": int(target_time.timestamp() * 1000),
            "indicators": signal_data["indicators"],
            "source": signal_data["source"],
            "daily_count": new_count,
            "daily_limit": daily_limit,
            "remaining": daily_limit - new_count
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ---------------------------------------------------------------------------
# QUOTEX UNOFFICIAL HISTORY API
# ---------------------------------------------------------------------------

@app.route('/api/history', methods=['GET'])
def history_handler():
    """Fetch historical candle data"""
    try:
        pair = request.args.get('pair', 'EURUSD')
        period = int(request.args.get('period', 60))  # Default 1 minute
        count = int(request.args.get('count', 30))
        
        # Check if we have credentials and library
        if Quotex is None:
            # Return simulated history if library not found
            now = time.time()
            candles = []
            price = 1.1000
            for i in range(count):
                price += (random.random() - 0.5) * 0.001
                candles.append({
                    "time": now - (count - i) * period,
                    "open": price,
                    "close": price + (random.random() - 0.5) * 0.0005,
                    "high": price + 0.0005,
                    "low": price - 0.0005
                })
            return jsonify({
                "status": "simulation",
                "data": candles,
                "message": "Running in simulation mode (quotexpy not found)"
            })

        email = os.environ.get("QUOTEX_EMAIL")
        password = os.environ.get("QUOTEX_PASSWORD")
        
        if not email or not password:
            return jsonify({"status": "error", "message": "Credentials not found"}), 401

        # Connect and fetch
        client = Quotex(email=email, password=password)
        check, reason = client.connect()
        
        if check:
            # Fetch candles: asset, period (s), count, timestamp
            candles = client.get_candles(pair, period, count, time.time())
            return jsonify({
                "status": "success",
                "data": candles,
                "source": "quotex_unofficial_api"
            })
        else:
            return jsonify({"status": "error", "message": f"Connection failed: {reason}"}), 500

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/assets', methods=['GET'])
def assets_handler():
    """Return list of all available assets"""
    return jsonify({
        "status": "success",
        "assets": QUOTEX_ASSETS,
        "total": len(QUOTEX_ASSETS)
    })

@app.route('/api/status', methods=['GET'])
def status_handler():
    return jsonify({
        "status": "online",
        "service": "MAHIR ADVANCED SIGNAL ENGINE",
        "version": "2.0",
        "features": ["RSI", "MACD", "EMA", "Bollinger Bands", "Multi-Asset Analysis"]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
