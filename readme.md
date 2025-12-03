# 🚀 MAHIR Advanced Quotex Signal Generator

**Professional Trading Signal System with Real-Time Analysis & Historical Data**

[![Status](https://img.shields.io/badge/Status-Production%20Ready-success)](https://github.com)
[![Version](https://img.shields.io/badge/Version-2.0-blue)](https://github.com)
[![License](https://img.shields.io/badge/License-MIT-green)](https://github.com)

---

## 🌟 **Features**

### ✅ **Core Functionality**
- 🎯 **Single Signal Generation** - Generate precise signals for individual assets
- 🚀 **Batch Signal Generation** - Generate 10 signals at once
- ⏱️ **Live Mode** - Auto-generate signals every 30 seconds
- 📊 **Historical Data Viewer** - View 30 candles of price history for any asset
- 📋 **Signal Export** - Copy formatted signals to clipboard
- 🌍 **Timezone Support** - Customizable UTC offset (-12 to +14)
- 🎲 **Martingale Options** - 1, 2, or 3 step configurations

### 🔬 **Advanced Technical Analysis**
- **RSI (Relative Strength Index)** - Momentum indicator
- **MACD (Moving Average Convergence Divergence)** - Trend following
- **EMA (Exponential Moving Average)** - 5 & 20 period
- **Bollinger Bands** - Volatility analysis
- **Multi-Indicator Scoring** - Weighted confidence system

### 💎 **Premium UI/UX**
- 🎨 **Dark Theme** with glassmorphism effects
- ✨ **Smooth Animations** - Slide-in, pulse, hover effects
- 📱 **Fully Responsive** - Works on desktop, tablet, mobile
- 🎭 **Modal Popups** - Beautiful history data display
- 🌈 **Color-Coded Signals** - Green (CALL) / Red (PUT)

### 🌐 **80+ Trading Assets**
- **Major Forex Pairs** - EURUSD, GBPUSD, USDJPY, etc.
- **OTC Forex** - 24/7 trading pairs
- **Exotic Pairs** - USDCOP, USDBRL, USDTRY, etc.
- **Commodities** - GOLD, SILVER, OIL, COPPER
- **Cryptocurrencies** - BTC, ETH, SHIBA, DOGE, PEPE, etc.
- **Stocks** - AAPL, MSFT, FB, BOEING, etc.

---

## 🚀 **Quick Start**

### **Option 1: Local Development**

1. **Clone/Download** the project
2. **Install dependencies:**
   ```bash
   pip install Flask quotexpy requests
   ```
3. **Run the server:**
   ```bash
   python api/index.py
   ```
4. **Open browser:**
   ```
   http://127.0.0.1:5000
   ```

### **Option 2: Deploy to Vercel (Recommended)**

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   vercel --prod
   ```

4. **Add Environment Variables** (in Vercel Dashboard):
   - `QUOTEX_EMAIL` = your Quotex email
   - `QUOTEX_PASSWORD` = your Quotex password

5. **Done!** Your app is live at `https://your-app.vercel.app`

---

## 📂 **Project Structure**

```
📁 Project Root
├── 📁 api/
│   └── index.py              # Flask backend API
├── 📁 public/
│   ├── index.html            # Main HTML page
│   ├── script.js             # Frontend JavaScript
│   └── styles.css            # Premium CSS styling
├── .env                      # Environment variables (local)
├── vercel.json               # Vercel deployment config
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── HISTORY_API_UPDATE.md     # History feature docs
```

---

## 🎮 **How to Use**

### **1. Generate Signals**

#### **Single Signal:**
- Click **"🎯 Single Signal (1 Only)"**
- Generates 1 random signal instantly

#### **Batch Signals (10):**
- Click **"🚀 GENERATE 10 SIGNALS"** (green button)
- Generates 10 signals from different assets

#### **Live Mode:**
- Click **"▶️ Start Live Mode (30s)"**
- Auto-generates signals every 30 seconds
- Click **"⏸️ Stop Live"** to stop

### **2. View Historical Data**

- Click **"📊 History"** on any signal card
- Modal opens showing 30 candles of price data
- Color-coded: 🟢 Green (up) / 🔴 Red (down)
- Close by clicking X or outside modal

### **3. Export Signals**

- Click **"📋 Copy All Signals"**
- Formatted text copied to clipboard
- Paste in Telegram, WhatsApp, etc.

### **4. Customize Settings**

- **Timezone:** Set your UTC offset (-12 to +14)
- **Timeframe:** 1 MINUTE (fixed for accuracy)
- **Martingale:** Choose 1, 2, or 3 step MTG

---

## 🔌 **API Endpoints**

### **1. Generate Signal**
```http
GET /api/signal?pair=EURUSD&timeframe=1&tz=6
```
**Response:**
```json
{
  "status": "success",
  "pair": "EURUSD",
  "dir": "CALL",
  "time": "13:05",
  "indicators": {
    "rsi": 45.23,
    "macd": 0.0012,
    "ema5": 1.1050
  }
}
```

### **2. Batch Signals**
```http
GET /api/signal?pair=ALL&timeframe=1&tz=6
```
**Response:**
```json
{
  "status": "success",
  "signals": [
    {"pair": "EURUSD", "dir": "CALL", "time": "13:05"},
    {"pair": "BTCUSD-OTC", "dir": "PUT", "time": "13:05"}
  ]
}
```

### **3. Historical Data** 🆕
```http
GET /api/history?pair=EURUSD&count=30&period=60
```
**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "time": 1733212800,
      "open": 1.1050,
      "close": 1.1052,
      "high": 1.1053,
      "low": 1.1049
    }
  ],
  "source": "quotex_unofficial_api"
}
```

### **4. Available Assets**
```http
GET /api/assets
```

### **5. System Status**
```http
GET /api/status
```

---

## 🔐 **Environment Variables**

Create a `.env` file in the root directory:

```env
QUOTEX_EMAIL=your-email@example.com
QUOTEX_PASSWORD=your-password
```

**For Vercel:**
- Add these as **Environment Variables** in your Vercel dashboard
- Settings → Environment Variables → Add

---

## 🎨 **Customization**

### **Change Colors:**
Edit `public/styles.css`:
```css
:root {
    --accent-gold: #fbbf24;      /* Primary color */
    --accent-emerald: #10b981;   /* CALL signals */
    --accent-rose: #f43f5e;      /* PUT signals */
}
```

### **Change Branding:**
Edit `public/index.html` and `public/script.js`:
- Replace "MAHIR" with your brand name
- Update footer with your info

### **Adjust Daily Limits:**
Edit `api/index.py`:
```python
daily_limit = 9999  # Change to your preferred limit
```

---

## 📊 **Technical Analysis Details**

### **Signal Scoring System:**
- **RSI (30% weight)** - Oversold/Overbought detection
- **EMA Crossover (25% weight)** - Trend direction
- **MACD (25% weight)** - Momentum confirmation
- **Bollinger Bands (20% weight)** - Volatility analysis

### **Confidence Calculation:**
```
Confidence = (Bullish Score / Total Score) × 100
Maximum: 95% (capped for realism)
```

---

## 🛠️ **Troubleshooting**

### **"quotexpy not found" Warning:**
- **Solution:** Install quotexpy: `pip install quotexpy`
- **Impact:** System runs in simulation mode (still functional)

### **Daily Limit Reached:**
- **Solution:** Wait until tomorrow or modify `daily_limit` in code
- **Testing:** Set `daily_limit = 9999` for unlimited signals

### **History Modal Not Opening:**
- **Solution:** Check browser console for errors
- **Fix:** Clear cache and refresh page

### **Signals Not Generating:**
- **Solution:** Check if server is running
- **Fix:** Restart server: `python api/index.py`

---

## 🚀 **Deployment Checklist**

- [x] ✅ Install dependencies (`pip install -r requirements.txt`)
- [x] ✅ Configure `.env` file with credentials
- [x] ✅ Test locally (`http://127.0.0.1:5000`)
- [x] ✅ Update `vercel.json` with environment variables
- [x] ✅ Deploy to Vercel (`vercel --prod`)
- [x] ✅ Add environment variables in Vercel dashboard
- [x] ✅ Test production URL
- [x] ✅ Share with users!

---

## 📱 **Browser Compatibility**

✅ **Fully Tested:**
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

---

## 🔄 **Updates & Changelog**

### **Version 2.0** (Latest)
- ✅ Added Historical Data API (`/api/history`)
- ✅ Modal popup for price history
- ✅ Color-coded candle display
- ✅ Improved asset list (80+ pairs)
- ✅ Enhanced UI/UX with animations
- ✅ Optimized Vercel deployment

### **Version 1.0**
- Initial release
- Signal generation
- Technical analysis
- Export functionality

---

## 📞 **Support & Contact**

- **Owner:** @LUX_DOT 💸
- **System:** X MAHIR SYSTEM
- **Platform:** Quotex Trading Signals

---

## ⚠️ **Disclaimer**

**Trading involves risk. Signals are for educational purposes only.**

- Not financial advice
- Past performance ≠ future results
- Trade responsibly with risk management
- Use safety margin and stop-loss
- Never invest more than you can afford to lose

---

## 📜 **License**

MIT License - Free to use and modify

---

## 🎯 **Key Benefits**

✅ **100% Free & Open Source**
✅ **No API Limits** (in simulation mode)
✅ **Real-time Analysis** (with quotexpy)
✅ **Professional Design**
✅ **Easy Deployment** (Vercel ready)
✅ **Mobile Friendly**
✅ **Fully Customizable**

---

## 🏆 **Best Practices**

1. **Use Safety Margin** - Always trade with buffer
2. **Follow MTG Rules** - Martingale recommended
3. **Skip After 2 Losses** - Avoid consecutive losses
4. **Check History** - View price trends before trading
5. **Set Daily Limits** - Don't overtrade
6. **Test First** - Use demo account initially

---

## 🚀 **Ready to Deploy?**

```bash
# Quick Deploy to Vercel
vercel --prod

# Or run locally
python api/index.py
```

**Your professional signal generator is ready! 🎉**

---

**Made with ❤️ by MAHIR Team | Powered by Advanced Technical Analysis**