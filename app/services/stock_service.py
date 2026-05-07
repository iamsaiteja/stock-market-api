import yfinance as yf
import pandas as pd
from datetime import datetime
from app.schemas.stock import StockPrice, HistoricalData


def format_nse_symbol(symbol: str) -> str:
    """
    NSE/BSE symbol format చేయడం.
    Example: RELIANCE → RELIANCE.NS
             RELIANCE.BSE → RELIANCE.BO
    """
    symbol = symbol.upper().strip()
    if symbol.endswith(".NS") or symbol.endswith(".BO"):
        return symbol
    if symbol.endswith(".BSE"):
        return symbol.replace(".BSE", ".BO")
    # Default గా NSE
    return f"{symbol}.NS"


def get_live_price(symbol: str) -> StockPrice:
    """Yahoo Finance నుండి live stock price తీసుకోవడం"""
    fmt_symbol = format_nse_symbol(symbol)
    ticker = yf.Ticker(fmt_symbol)
    info = ticker.info

    if not info or info.get("regularMarketPrice") is None:
        # Fast_info try చేయడం
        fast = ticker.fast_info
        current = fast.get("lastPrice") or fast.get("last_price")
        if not current:
            raise ValueError(f"'{symbol}' కోసం data దొరకలేదు. Symbol సరిగ్గా ఉందో చూడండి.")
    else:
        current = info.get("regularMarketPrice") or info.get("currentPrice", 0)

    previous_close = info.get("regularMarketPreviousClose") or info.get("previousClose", 0)
    change = round(current - previous_close, 2)
    change_pct = round((change / previous_close * 100), 2) if previous_close else 0.0

    return StockPrice(
        symbol=fmt_symbol,
        company_name=info.get("longName") or info.get("shortName") or symbol,
        current_price=round(current, 2),
        previous_close=round(previous_close, 2),
        change=change,
        change_percent=change_pct,
        day_high=round(info.get("dayHigh") or info.get("regularMarketDayHigh") or current, 2),
        day_low=round(info.get("dayLow") or info.get("regularMarketDayLow") or current, 2),
        volume=info.get("volume") or info.get("regularMarketVolume") or 0,
        market_cap=info.get("marketCap"),
        pe_ratio=info.get("trailingPE"),
        timestamp=datetime.now(),
    )


def get_historical_data(symbol: str, period: str = "3mo") -> HistoricalData:
    """
    Historical data తీసుకోవడం.
    Period options: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y
    """
    valid_periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y"]
    if period not in valid_periods:
        period = "3mo"

    fmt_symbol = format_nse_symbol(symbol)
    ticker = yf.Ticker(fmt_symbol)
    hist = ticker.history(period=period)

    if hist.empty:
        raise ValueError(f"'{symbol}' కోసం historical data దొరకలేదు.")

    records = []
    for date, row in hist.iterrows():
        records.append({
            "date": date.strftime("%Y-%m-%d"),
            "open": round(row["Open"], 2),
            "high": round(row["High"], 2),
            "low": round(row["Low"], 2),
            "close": round(row["Close"], 2),
            "volume": int(row["Volume"]),
        })

    return HistoricalData(symbol=fmt_symbol, period=period, data=records)


def get_multiple_prices(symbols: list[str]) -> list[dict]:
    """Multiple stocks ఒకేసారి fetch చేయడం"""
    results = []
    for sym in symbols:
        try:
            price = get_live_price(sym)
            results.append({"success": True, "data": price.model_dump()})
        except Exception as e:
            results.append({"success": False, "symbol": sym, "error": str(e)})
    return results