# Varant Direction AI

GitHub-ready MVP scaffold for a short-term CALL/PUT direction engine and warrant selector.

## Current MVP
- Provider abstraction for Yahoo Finance and Finnhub
- Technical indicators: EMA, RSI, MACD, Bollinger Bands, ATR, VWAP
- 0-100 direction score
- CALL / PUT / BEKLE decision
- Warrant CSV import structure
- Warrant scoring based on delta, leverage, spread and days to expiry
- Manual-data fallback
- No API keys embedded in the app

## Next
1. Add backend secrets through GitHub Actions / deployment environment.
2. Connect live provider endpoints.
3. Import the user's warrant CSV.
4. Add Flutter Android UI.
5. Add automated APK build.
