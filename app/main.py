from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers import stocks, prediction

app = FastAPI(
    title="📈 Stock Market Analysis API",
    description="""
## NSE/BSE Stock Analysis API — Built with FastAPI + yfinance

### Features:
- 📈 **Live Stock Prices** — NSE & BSE stocks real-time data
- 🤖 **AI Buy/Sell Predictions** — Technical analysis based signals
- 📊 **Historical Data** — OHLCV data with custom periods
- 🔢 **Bulk Operations** — Multiple stocks ఒకేసారి

### Popular NSE Symbols:
`RELIANCE`, `TCS`, `INFY`, `HDFCBANK`, `ICICIBANK`, `SBIN`, `WIPRO`

### BSE Symbols:
Symbol తర్వాత `.BO` add చేయండి: `RELIANCE.BO`

---
⚠️ **Disclaimer:** Educational purposes only. Not financial advice.
    """,
    version="1.0.0",
    contact={"name": "Stock API", "email": "dev@example.com"},
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(stocks.router,     prefix="/api/v1")
app.include_router(prediction.router, prefix="/api/v1")


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "📈 Stock Market Analysis API కి స్వాగతం!",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "live_price":    "/api/v1/stocks/{symbol}/price",
            "history":       "/api/v1/stocks/{symbol}/history?period=3mo",
            "popular":       "/api/v1/stocks/popular/nse",
            "bulk_prices":   "POST /api/v1/stocks/bulk",
            "ai_prediction": "/api/v1/predict/{symbol}",
            "bulk_predict":  "POST /api/v1/predict/bulk",
        },
        "example_symbols": ["RELIANCE", "TCS", "INFY", "HDFCBANK", "SBIN"],
    }


@app.get("/health", tags=["Root"])
def health():
    return {"status": "✅ API is running"}