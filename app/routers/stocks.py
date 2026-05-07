from fastapi import APIRouter, HTTPException, Query
from app.services.stock_service import get_live_price, get_historical_data, get_multiple_prices
from app.schemas.stock import StockPrice, HistoricalData, ErrorResponse

router = APIRouter(prefix="/stocks", tags=["📈 Stock Prices"])

# Popular Indian stocks shortcut
POPULAR_STOCKS = [
    "RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK",
    "SBIN", "WIPRO", "ADANIENT", "BAJFINANCE", "TATAMOTORS"
]


@router.get(
    "/{symbol}/price",
    response_model=StockPrice,
    summary="Live Stock Price",
    description="NSE/BSE stock యొక్క live price తీసుకోవడం. Example: RELIANCE, TCS, INFY",
)
def live_price(symbol: str):
    try:
        return get_live_price(symbol)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data fetch చేయడంలో error: {str(e)}")


@router.get(
    "/{symbol}/history",
    response_model=HistoricalData,
    summary="Historical Price Data",
    description="Stock యొక్క historical OHLCV data తీసుకోవడం.",
)
def historical_data(
    symbol: str,
    period: str = Query(
        default="3mo",
        description="Period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y",
        pattern="^(1d|5d|1mo|3mo|6mo|1y|2y|5y)$",
    ),
):
    try:
        return get_historical_data(symbol, period)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/bulk",
    summary="Multiple Stocks Price",
    description="Multiple stocks ఒకేసారి fetch చేయడం. Max 10 symbols.",
)
def bulk_prices(symbols: list[str]):
    if len(symbols) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 symbols మాత్రమే allowed.")
    return get_multiple_prices(symbols)


@router.get(
    "/popular/nse",
    summary="Popular NSE Stocks",
    description="Top 10 popular NSE stocks యొక్క live prices.",
)
def popular_stocks():
    return get_multiple_prices(POPULAR_STOCKS)