from dataclasses import dataclass
import pandas as pd
import numpy as np

@dataclass
class DirectionResult:
    direction: str
    score: int
    confidence: int
    reasons: list[str]

def ema(s, n):
    return s.ewm(span=n, adjust=False).mean()

def rsi(s, n=14):
    d=s.diff()
    gain=d.clip(lower=0).ewm(alpha=1/n, adjust=False).mean()
    loss=(-d.clip(upper=0)).ewm(alpha=1/n, adjust=False).mean()
    rs=gain/loss.replace(0,np.nan)
    return 100-(100/(1+rs))

def macd(s):
    m=ema(s,12)-ema(s,26)
    sig=ema(m,9)
    return m, sig, m-sig

def bollinger(s,n=20,k=2):
    mid=s.rolling(n).mean()
    sd=s.rolling(n).std()
    return mid, mid+k*sd, mid-k*sd

def atr(df,n=14):
    prev=df.close.shift(1)
    tr=pd.concat([(df.high-df.low),(df.high-prev).abs(),(df.low-prev).abs()],axis=1).max(axis=1)
    return tr.ewm(alpha=1/n,adjust=False).mean()

def vwap(df):
    typical=(df.high+df.low+df.close)/3
    return (typical*df.volume).cumsum()/df.volume.cumsum()

def analyze(df):
    df=df.copy()
    e9,e21=ema(df.close,9),ema(df.close,21)
    r=rsi(df.close).iloc[-1]
    m,s,h=macd(df.close)
    mid,up,lo=bollinger(df.close)
    vw=vwap(df).iloc[-1]

    score=50
    reasons=[]
    if e9.iloc[-1] > e21.iloc[-1]:
        score += 15; reasons.append("EMA9 > EMA21")
    else:
        score -= 15; reasons.append("EMA9 < EMA21")
    if m.iloc[-1] > s.iloc[-1]:
        score += 10; reasons.append("MACD bullish")
    else:
        score -= 10; reasons.append("MACD bearish")
    if df.close.iloc[-1] > vw:
        score += 8; reasons.append("Price above VWAP")
    else:
        score -= 8; reasons.append("Price below VWAP")
    if 50 <= r <= 70:
        score += 7; reasons.append("RSI supports momentum")
    elif r < 40:
        score -= 7; reasons.append("Weak RSI")
    elif r > 75:
        score -= 5; reasons.append("Overbought risk")

    score=int(max(0,min(100,score)))
    if score >= 70:
        direction="CALL"
        confidence=score
    elif score <= 30:
        direction="PUT"
        confidence=100-score
    else:
        direction="BEKLE"
        confidence=50-abs(score-50)

    return DirectionResult(direction,score,int(confidence),reasons)

def load_warrants(path="data/warrants.csv"):
    return pd.read_csv(path)

def select_warrants(warrants, direction, underlying):
    w=warrants[(warrants.underlying==underlying)&(warrants.direction==direction)].copy()
    if w.empty: return w
    w["spread_pct"]=(w.ask-w.bid)/((w.ask+w.bid)/2)*100
    # Practical ranking: liquidity + usable delta + leverage, penalize wide spread.
    w["score"]=(w.delta.abs()*35 + np.minimum(w.leverage,15)/15*30
                + np.minimum(np.log1p(w.volume),12)/12*20
                + np.maximum(0,10-w.spread_pct)*1.5).round(2)
    return w.sort_values("score",ascending=False)
