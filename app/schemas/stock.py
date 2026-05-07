from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class StockPrice(BaseModel):
    symbol: str
    company_name: str
    current_price: float
    previous_close: float
    change: float
    change_percent: float
    day_high: float
    day_low: float
    volume: int
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    timestamp: datetime


class HistoricalData(BaseModel):
    symbol: str
    period: str
    data: list[dict]


class TechnicalIndicators(BaseModel):
    symbol: str
    rsi: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    ema_20: Optional[float] = None
    bollinger_upper: Optional[float] = None
    bollinger_lower: Optional[float] = None


class PredictionResult(BaseModel):
    symbol: str
    company_name: str
    current_price: float
    signal: str
    confidence: float
    reasons: list[str]
    risk_level: str
    target_price: Optional[float] = None
    stop_loss: Optional[float] = None
    indicators: TechnicalIndicators
    timestamp: datetime


class ErrorResponse(BaseModel):
    error: str
    detail: str