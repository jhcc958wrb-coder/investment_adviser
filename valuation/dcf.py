import yfinance as yf

def calculate_discount_rate(beta):

    if beta is None:
        beta = 1.0

    risk_free_rate = 0.04
    market_risk_premium = 0.05

    cost_of_equity = (
        risk_free_rate
        + beta * market_risk_premium
    )

    return cost_of_equity

def calculate_growth_rate(
    revenue_growth,
    earnings_growth
):

    if (
        revenue_growth is None
        or earnings_growth is None
    ):
        return 0.05

    growth = (
        revenue_growth
        + earnings_growth
    ) / 2
    growth *= 0.5

    return growth / 100
  
def calculate_discount_rate(beta):

    if beta is None:
        beta = 1.0

    risk_free_rate = 0.045
    market_risk_premium = 0.055

    return (
        risk_free_rate
        + beta * market_risk_premium
    )

def dcf_scenario(
    symbol,
    growth_rate,
    discount_rate,
    terminal_growth=0.03
    
):

    ticker = yf.Ticker(symbol)

    cashflow = ticker.cashflow

    info = ticker.info

    try:

        operating_cf = cashflow.loc[
            "Operating Cash Flow"
        ].iloc[0]

        capex = abs(
            cashflow.loc[
                "Capital Expenditure"
            ].iloc[0]
        )

        fcf = operating_cf - capex

        shares = info.get(
            "sharesOutstanding"
        )

        pv = 0

        current_fcf = fcf

        growth_schedule = [

            growth_rate,

            growth_rate * 0.9,

            growth_rate * 0.8,

            growth_rate * 0.7,

            growth_rate * 0.6
        ]

        for year, g in enumerate(
            growth_schedule,
            start=1
        ):

            current_fcf *= (
                1 + g
            )

            pv += (
                current_fcf
                / (
                    (1 + discount_rate)
                    ** year
                )
            )

        terminal_fcf = (
            current_fcf
            * (1 + terminal_growth)
        )

        terminal_value = (
            terminal_fcf
            / (
                discount_rate
                - terminal_growth
            )
        )

        terminal_pv = (
            terminal_value
            / ((1 + discount_rate) ** 5)
        )

        enterprise_value = (
            pv + terminal_pv
        )

        intrinsic_value = (
            enterprise_value
            / shares
        )

        return round(
            intrinsic_value,
            2
        )

    except Exception as e:

        print("DCF 오류:", e)

        return None
    

def calculate_dcf_range(
    symbol,
    base_growth,
    beta
):
    base_discount_rate = (
    calculate_discount_rate(beta)
    )
    bear_discount = (
    base_discount_rate + 0.02
    )

    bull_discount = max(
        base_discount_rate - 0.02,
        0.05
    )

    bear_growth = max(
        base_growth - 0.02,
        0.01
    )

    bull_growth = (
        base_growth + 0.02
    )

    return {

        "bear": dcf_scenario(
            symbol,
            growth_rate=bear_growth,
            discount_rate=bear_discount
        ),

        "base": dcf_scenario(
            symbol,
            growth_rate=base_growth,
            discount_rate=base_discount_rate
        ),

        "bull": dcf_scenario(
            symbol,
            growth_rate=bull_growth,
            discount_rate=bull_discount
        )
    }
