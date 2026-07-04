import json

def get_sector_data(sector):

    with open(
        "industry_benchmark.json",
        "r",
        encoding="utf-8"
    ) as f:

        benchmark = json.load(f)

    sector_mapping = {

        "Technology":
            "Information Technology",

        "Healthcare":
            "Health Care",

        "Financial Services":
            "Financials",

        "Consumer Defensive":
            "Consumer Staples",

        "Consumer Cyclical":
            "Consumer Discretionary"
    }

    sector = sector_mapping.get(
        sector,
        sector
    )

    if sector in benchmark:

        return benchmark[sector]

    return None