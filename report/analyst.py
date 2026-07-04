def print_analyst_target(
    data,
    dcf_base
):
    
    if not data["target_price"]:

        return {

            "upside": 0,

            "difference": 0,

            "analyst_score": 0,

            "target_price": None

        }
    upside = (

        (
            data["target_price"]
            - data["price"]
        )

        /

        data["price"]

    ) * 100

    print(
        "\n===== 애널리스트 목표주가 ====="
    )

    print(
        f"현재주가 : ${data['price']}"
    )

    print(
        f"DCF 적정가 : ${dcf_base:.2f}"
    )

    print(
        f"애널리스트 목표주가 : ${data['target_price']:.2f}"
    )

    print(
        f"애널리스트 예상 상승여력 : {upside:+.1f}%"
    )

    difference = (
        (
            data["target_price"]
            - dcf_base
        )
        / dcf_base
    ) * 100

    print(
        f"DCF 추정치와의 차이 : {difference:+.1f}%"
    )

    if upside > 20:

        print(
            "애널리스트들은 현재 주가보다 높은 상승 여력을 예상합니다."
        )

    elif upside > 0:

        print(
            "추가 상승 여력이 존재하는 것으로 평가됩니다."
        )

    else:

        print(
            "애널리스트 목표주가가 현재 주가를 하회합니다."
        )

    if difference > 100:

        print(
            "애널리스트들은 DCF보다 훨씬 높은 성장 가능성을 반영하고 있습니다."
        )

    elif difference > 30:

        print(
            "애널리스트 목표주가가 DCF보다 다소 높게 형성되어 있습니다."
        )

    elif difference > -30:

        print(
            "DCF와 애널리스트 의견이 유사한 수준입니다."
        )

    else:

        print(
            "DCF가 애널리스트 목표주가보다 높게 평가됩니다."
        )

    upside = (
        (
            data["target_price"]
            - data["price"]
        )
        / data["price"]
    ) * 100

    if upside > 50:

        analyst_score = 10

    elif upside > 30:

        analyst_score = 8

    elif upside > 15:

        analyst_score = 6

    elif upside > 0:

        analyst_score = 4

    else:

        analyst_score = 0
    
    return {

        "upside": upside,

        "difference": difference,

        "analyst_score": analyst_score,

        "target_price": data["target_price"]

    }
    