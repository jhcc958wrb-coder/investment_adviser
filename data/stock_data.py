import yfinance as yf

def get_stock_info(symbol):

    ticker = yf.Ticker(symbol)

    info = ticker.info

    price = info.get("currentPrice")
    eps = info.get("trailingEps")
    book_value = info.get("bookValue")

    per = info.get("trailingPE")
    pbr = info.get("priceToBook")

    if per is None and eps not in [None, 0]:
        per = price / eps
    
    if pbr is None and book_value not in [None, 0]:
        pbr = price / book_value

    return {
        "company": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "price": info.get("currentPrice"),
        "market_cap": info.get("marketCap"),
        "per": per,
        "pbr": pbr,
        "per": info.get("trailingPE"),
        "pbr": info.get("priceToBook"),
        "roe": info.get("returnOnEquity"),
        "eps": info.get("trailingEps"),
        "dividend_yield": info.get("dividendYield"),
        "debt_ratio": info.get("debtToEquity"),
        "revenue_growth": info.get("revenueGrowth"),
        "earnings_growth": info.get("earningsGrowth"),
        "currency": info.get("currency"),
        "beta": info.get("beta"),
        "target_price": info.get("targetMeanPrice")
    }
    
def get_news(symbol):

    ticker = yf.Ticker(symbol)

    news = ticker.news

    return news[:3]
