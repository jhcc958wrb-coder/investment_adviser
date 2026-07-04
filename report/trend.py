import yfinance as yf
import matplotlib.pyplot as plt

def print_trend(symbol):

    ticker = yf.Ticker(symbol)

    hist = ticker.history(period="6mo")

    hist["MA20"] = hist["Close"].rolling(20).mean()

    hist["MA60"] = hist["Close"].rolling(60).mean()

    current = hist["Close"].iloc[-1]

    ma20 = hist["MA20"].iloc[-1]

    ma60 = hist["MA60"].iloc[-1]

    print("\n===== 주가 추세 =====")

    print(f"현재주가 : ${current:.2f}")
    print(f"20일 이동평균 : ${ma20:.2f}")
    print(f"60일 이동평균 : ${ma60:.2f}")

    if current > ma20 and current > ma60:

        print("현재 주가는 단기·중기 이동평균선을 모두 상회하고 있습니다.")
        trend = "Strong Uptrend"

    elif current > ma20:

        print("단기 상승 추세를 유지하고 있습니다.")
        trend = "Uptrend"

    elif current < ma20 and current < ma60:

        print("현재 주가는 이동평균선 아래에 위치해 약세 추세입니다.")
        trend = "Downtrend"

    else:

        print("뚜렷한 방향성이 없는 횡보 구간입니다.")
        trend = "Sideways"

    plt.figure(figsize=(10,5))

    plt.plot(
        hist.index,
        hist["Close"],
        label="Close Price",
        linewidth=2
    )

    plt.plot(
        hist.index,
        hist["MA20"],
        label="MA20",
        linewidth=1.5
    )

    plt.plot(
        hist.index,
        hist["MA60"],
        label="MA60",
        linewidth=1.5
    )

    plt.title(f"{symbol.upper()} Price Trend")

    plt.xlabel("Date")

    plt.ylabel("Price")

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    plt.savefig("trend.png", dpi=300)

    plt.close()

    return {

        "trend": trend,

        "ma20": ma20,

        "ma60": ma60

    }