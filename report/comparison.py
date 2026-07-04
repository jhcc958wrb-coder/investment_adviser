

def compare_with_sector(
    data,
    sector_data
):

    

    score = 0

    strengths = []

    weaknesses = []
    per_diff = None
    pbr_diff = None
    roe_diff = None
    revenue_diff = None
    earnings_diff = None
    debt_diff = None

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

    score = 0

    strengths = []
    weaknesses = []

# PER
    if data["per"] is not None:

        per_diff = (
            (data["per"] - sector_per)
            / sector_per
        ) * 100

        print(f"PER : {per_diff:+.1f}%")

        if data["per"] < sector_per:
            score += 25
            strengths.append(
                "낮은 PER"
            )
        else:
            weaknesses.append(
                "높은 PER"
            )

# PBR
    if data["pbr"] is not None:

        pbr_diff = (
            (data["pbr"] - sector_pbr)
            / sector_pbr
        ) * 100

        print(f"PBR : {pbr_diff:+.1f}%")

        if data["pbr"] < sector_pbr:
            score += 25
            strengths.append(
                "낮은 PBR"
            )
        else:
            weaknesses.append(
                "높은 PBR"
            )

# ROE
    if data["roe"] is not None:

        roe_diff = (
            ((data["roe"] * 100) - sector_roe)
            / sector_roe
        ) * 100

        print(f"ROE : {roe_diff:+.1f}%")

        if (data["roe"] * 100) > sector_roe:
            score += 25
            strengths.append(
                "높은 ROE"
            )
        else:
            weaknesses.append(
                "낮은 ROE"
            )

#Growth
    if data["revenue_growth"] is not None:

        revenue_diff = (
            (data["revenue_growth"] * 100)
            - sector_revenue_growth
        )

        print(
            f"Revenue Growth : {revenue_diff:+.1f}%p"
        )

    if data["earnings_growth"] is not None:

        earnings_diff = (
            (data["earnings_growth"] * 100)
            - sector_earnings_growth
        )

        print(
            f"Earnings Growth : {earnings_diff:+.1f}%p"
        )

# Debt
    if data["debt_ratio"] is not None:

        debt_diff = (
            (data["debt_ratio"] - sector_debt)
            / sector_debt
        ) * 100

        print(f"Debt : {debt_diff:+.1f}%")

        if data["debt_ratio"] < sector_debt:
            score += 25
            strengths.append(
                "낮은 부채비율"
            )
        else:
            weaknesses.append(
                "높은 부채비율"
            )

# Revenue Growth
    if data["revenue_growth"] is not None:

        revenue_growth = data["revenue_growth"] * 100

        if (
            revenue_growth > 0
            and revenue_growth > sector_revenue_growth
        ):

            strengths.append(
                "업종 평균을 상회하는 매출 성장률"
            )

        elif revenue_growth < 0:

            weaknesses.append(
                "매출 감소"
            )


# Earnings Growth
    if data["earnings_growth"] is not None:

        earnings_growth = data["earnings_growth"] * 100

        if (
            earnings_growth > 0
            and earnings_growth > sector_earnings_growth
        ):

            strengths.append(
                "업종 평균을 상회하는 이익 성장률"
            )

        elif earnings_growth < 0:

            weaknesses.append(
                "이익 감소"
            )

    return {

        "score": score,

        "strengths": strengths,

        "weaknesses": weaknesses,

        "per_diff": per_diff,

        "pbr_diff": pbr_diff,

        "roe_diff": roe_diff,

        "revenue_diff": revenue_diff,

        "earnings_diff": earnings_diff,

        "debt_diff": debt_diff

    }