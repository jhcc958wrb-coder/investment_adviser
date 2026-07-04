from valuation.dcf import (
    calculate_growth_rate,
    calculate_discount_rate,
    calculate_dcf_range
)

def print_dcf_analysis(
    data,
    symbol
):

    base_growth = calculate_growth_rate(

        data["revenue_growth"] * 100,

        data["earnings_growth"] * 100,

    )

    print("\n===== 성장률 추정 =====")

    print(
        f"DCF 적용 성장률 : {base_growth*100:.1f}%"
    )

    discount_rate = calculate_discount_rate(
        data["beta"]
    )

    print(
        f"CAPM 할인율 : {discount_rate*100:.1f}%"
    )

    dcf = calculate_dcf_range(
        symbol,
        base_growth,
        data["beta"]
    )

    if dcf:

        print("\n===== DCF 가치평가 =====")

        print(
            f"보수적 시나리오 : ${dcf['bear']}"
        )

        print(
            f"기준 시나리오 : ${dcf['base']}"
        )

        print(
            f"낙관적 시나리오 : ${dcf['bull']}"
        )

    gap = None
    dcf_score = 0

    if dcf["base"] is not None:

        gap = (
            (
                data["price"]
                - dcf["base"]
            )
            / dcf["base"]
        ) * 100

        if gap > 200:
            dcf_score = 0

        elif gap > 100:
            dcf_score = 2

        elif gap > 50:
            dcf_score = 4

        elif gap > 20:
            dcf_score = 6

        elif gap > -20:
            dcf_score = 8

        else:
            dcf_score = 10

        print(
            f"DCF 대비 괴리율 : {gap:+.1f}%"
        )

        if gap > 100:

            print("⚠️ 추정된 DCF는 미래 성장 기대가 거의 반영되지 않은, 현재 현금흐름을 중심으로 한 추정치입니다.")
            print(
                "시장 기대가 상당히 높게 반영된 상태입니다."
            )
        elif gap > 20:
            print(
                "시장 기대가 상당히 높게 반영된 상태입니다."
            )
        elif gap < -20:

            print(
                "DCF 기준 저평가 가능성이 있습니다."
            )

        else:

            print(
                "DCF 기준 적정 가치 수준입니다."
            )

    return {
        "dcf": dcf,
        "gap": gap,
        "dcf_score": dcf_score,
        "base_growth": base_growth,
        "discount_rate": discount_rate
    }