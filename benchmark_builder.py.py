import pandas as pd
import yfinance as yf
import statistics
import json
from tqdm import tqdm

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

sp500 = pd.read_html(
    url,
    storage_options={
        "User-Agent": "Mozilla/5.0"
    }
)[0]

benchmarks = {}

sectors = sp500["GICS Sector"].unique()

for sector in sectors:

    print(f"\n===== {sector} =====")

    sector_companies = sp500[
        sp500["GICS Sector"] == sector
    ]

    symbols = sector_companies["Symbol"].tolist()

    per_list = []
    pbr_list = []
    roe_list = []
    debt_list = []
    revenue_growth_list = []
    earnings_growth_list = []

    # 우선 테스트용으로 업종당 10개만
    for symbol in tqdm(symbols):
        try:
            symbol = symbol.replace(".", "-")
            info = yf.Ticker(symbol).info

            per = info.get("trailingPE")
            pbr = info.get("priceToBook")
            roe = info.get("returnOnEquity")
            debt_ratio = info.get("debtToEquity")
            revenue_growth = info.get("revenueGrowth")
            earnings_growth = info.get("earningsGrowth")

            if per is not None and per > 0:
                per_list.append(per)

            if pbr is not None and pbr > 0:
                pbr_list.append(pbr)

            if roe is not None:
                roe_list.append(roe * 100)
                
            if debt_ratio is not None and debt_ratio > 0:
                debt_list.append(debt_ratio)

            if revenue_growth is not None:
                revenue_growth_list.append(
                    revenue_growth * 100
                )

            if earnings_growth is not None:
                earnings_growth_list.append(
                    earnings_growth * 100
                )
        except:
            pass

    print(f"\n{sector}")

    print(f"PER 데이터 수 : {len(per_list)}")
    print(f"PBR 데이터 수 : {len(pbr_list)}")
    print(f"ROE 데이터 수 : {len(roe_list)}")
    print(f"Debt 데이터 수 : {len(debt_list)}")
    print(f"Revenue Growth 데이터 수 : {len(revenue_growth_list)}")
    print(f"Earnings Growth 데이터 수 : {len(earnings_growth_list)}")

    if (
    len(per_list) > 0
    and len(pbr_list) > 0
    and len(roe_list) > 0
    and len(debt_list) > 0
    and len(revenue_growth_list) > 0
    and len(earnings_growth_list) > 0
    ):

        benchmarks[sector] = {

            "PER": round(
                statistics.median(per_list),
                2
            ),

            "PBR": round(
                statistics.median(pbr_list),
                2
            ),

            "ROE": round(
                statistics.median(roe_list),
                2
            ),

            "Debt": round(
                statistics.median(debt_list),
                2
            ),
            "RevenueGrowth": round(
                statistics.median(
                    revenue_growth_list
            ),
            2
            ),
            "EarningsGrowth": round(
                statistics.median(
                    earnings_growth_list
            ),
            2
            )
        }

with open(
    "industry_benchmark.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        benchmarks,
        f,
        indent=4,
        ensure_ascii=False
    )

print("\n완료!")
print(benchmarks)