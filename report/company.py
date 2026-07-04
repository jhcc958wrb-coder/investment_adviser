def print_company_info(data):

    print("\n")
    print("=" * 50)

    print(f"기업명 : {data['company']}")

    currency = data.get("currency")

    if currency == "KRW":
        print(f"현재주가 : {data['price']:,.0f}원")
    else:
        print(f"현재주가 : ${data['price']}")

    if data["per"] is not None:
        print(f"PER : {data['per']:.2f}")
    else:
        print("PER : N/A")

    if data["pbr"] is not None:
        print(f"PBR : {data['pbr']:.2f}")
    else:
        print("PBR : N/A")

    if data["roe"] is not None:
        print(f"ROE : {data['roe']*100:.2f}%")
    else:
        print("ROE : N/A")

    if data["debt_ratio"] is not None:
        print(f"부채비율 : {data['debt_ratio']:.2f}")
    else:
        print("부채비율 : N/A")

    print(f"EPS : {data['eps']}")

    if data["dividend_yield"] is not None:
        print(
            f"배당수익률 : {data['dividend_yield']:.2f}%"
        )
    else:
        print("배당수익률 : N/A")