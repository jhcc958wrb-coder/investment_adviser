def print_economic_moat(
    data,
    discount_rate,
    sector_data
):

    print("\n===== Economic Moat =====")

    if (
        data["roe"] is None
        or discount_rate is None
    ):

        print("Economic Moat : 평가 불가")

        return {
            "score": 0,
            "grade": "N/A"
        }

    roe = data["roe"] * 100
    cost_of_equity = discount_rate * 100

    spread = roe - cost_of_equity

    if spread >= 40:

        moat_grade = "Exceptional"
        moat_score = 10

    elif spread >= 20:

        moat_grade = "Strong"
        moat_score = 8

    elif spread >= 10:

        moat_grade = "Moderate"
        moat_score = 6

    elif spread >= 3:

        moat_grade = "Weak"
        moat_score = 4

    else:

        moat_grade = "None"
        moat_score = 0

    print(f"ROE : {roe:.2f}%")
    print(f"Cost of Equity : {cost_of_equity:.2f}%")
    print(f"Spread : {spread:+.2f}%")

    print(
        f"Economic Moat : {moat_grade} ({moat_score}/10)"
    )

    if moat_grade == "Exceptional":

        print(
            "기업이 자본비용을 크게 초과하는 수익을 창출하고 있습니다."
        )
        print("강한 경쟁우위를 유지할 가능성이 있습니다.")

    elif moat_grade == "Strong":

        print(
            "자본비용을 안정적으로 상회하는 우수한 경쟁력을 보입니다."
        )

    elif moat_grade == "Moderate":

        print(
            "자본비용을 소폭 상회하며 경쟁우위를 유지하고 있습니다."
        )

    elif moat_grade == "Weak":

        print(
            "자본비용을 약간 상회하지만 경쟁우위는 제한적입니다."
        )

    else:

        print(
            "ROE가 자본비용보다 낮아 지속적인 경쟁우위를 확인하기 어렵습니다."
        )

    if data["debt_ratio"] is not None:

        if data["debt_ratio"] > sector_data["Debt"]:

            print(
                "※ 높은 ROE에는 부채 사용의 영향이 일부 포함될 수 있습니다."
            )

        else:

            print(
                "※ 낮은 부채 수준에서도 높은 수익성을 유지하고 있습니다."
            )

    return {

        "score": moat_score,

        "grade": moat_grade,

        "spread": spread

    }