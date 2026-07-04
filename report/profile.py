def calculate_profile(
    data,
    sector_data
):
    sector_per = sector_data["PER"]

    sector_pbr = sector_data["PBR"]

    sector_roe = sector_data["ROE"]

    sector_debt = sector_data["Debt"]

    sector_revenue_growth = (
        sector_data["RevenueGrowth"]
    )

    sector_earnings_growth = (
        sector_data["EarningsGrowth"]
    )
# -------------------------

# Value

# -------------------------
    if (
        data["per"] is None
        or data["pbr"] is None
    ):

        value_grade = "N/A"

    else:
        value_score = 0

        if data["per"] is not None and data["per"] < sector_per:
            value_score += 1

        if data["pbr"] is not None and data["pbr"] < sector_pbr:
            value_score += 1

        if value_score == 2:
            value_grade = "A"

        elif value_score == 1:
            value_grade = "B"

        else:
            value_grade = "C"

# -------------------------

# Quality

# -------------------------

    if data["roe"] is not None:

        roe_gap = (
            ((data["roe"] * 100) - sector_roe)
            / sector_roe
        ) * 100

        if roe_gap > 20:
            quality_grade = "A"
        elif roe_gap > -10:
            quality_grade = "B"

        else:
            quality_grade = "C"

    else:

        quality_grade = "N/A"

# -------------------------
# Growth
# -------------------------

    growth_score = 0

    if (
        data["revenue_growth"] is not None
        and data["revenue_growth"] * 100 > 0
        and data["revenue_growth"] * 100 > sector_revenue_growth
    ):
        growth_score += 1

    if (
        data["earnings_growth"] is not None
        and data["earnings_growth"] * 100 > 0
        and data["earnings_growth"] * 100 > sector_earnings_growth
    ):
        growth_score += 1

    if growth_score == 2:

        growth_grade = "A"

    elif growth_score == 1:

        growth_grade = "B"

    else:

        growth_grade = "C"

# -------------------------

# Safety

# -------------------------

    if data["debt_ratio"] is not None:

        debt_gap = (
            (data["debt_ratio"] - sector_debt)
            / sector_debt
        ) * 100

        if debt_gap < -20:
            safety_grade = "A"

        elif debt_gap < 20:
            safety_grade = "B"

        else:
            safety_grade = "C"

    else:

        safety_grade = "N/A"
    return {

    "value_grade":
        value_grade,

    "quality_grade":
        quality_grade,

    "growth_grade":
        growth_grade,

    "safety_grade":
        safety_grade

    }

def print_profile(
    profile
):

    print(
        "\n===== 투자 프로파일 ====="
    )

    print(
        f"Value (가치)     : {profile['value_grade']}"
    )

    print(
        f"Quality (수익성) : {profile['quality_grade']}"
    )

    print(
        f"Growth (성장성)  : {profile['growth_grade']}"
    )

    print(
        f"Safety (안정성)  : {profile['safety_grade']}"
    )
