def print_sector_comparison(
    sector_data
):

    print(
        "\n===== 업종 비교 ====="
    )

    print(
        f"업종 평균 PER : {sector_data['PER']}"
    )

    print(
        f"업종 평균 PBR : {sector_data['PBR']}"
    )

    print(
        f"업종 평균 ROE : {sector_data['ROE']}%"
    )

    print(
        f"업종 평균 부채비율 : {sector_data['Debt']}"
    )

    print(
        f"업종 평균 매출성장률 : {sector_data['RevenueGrowth']}%"
    )

    print(
        f"업종 평균 이익성장률 : {sector_data['EarningsGrowth']}%"
    )