from report.company import (
    print_company_info
)
from report.sector import (
    print_sector_comparison
)
from report.comparison import (
    compare_with_sector
)

from report.profile import (calculate_profile)

from report.profile import (print_profile)

from report.dcf_report import (
    print_dcf_analysis
)

from report.analyst import (
    print_analyst_target
)

from report.moat import (
    print_economic_moat
)

from report.trend import print_trend

from report.score import calculate_total_score

from data.stock_data import get_stock_info
from valuation.dcf import (
    calculate_dcf_range,
    calculate_growth_rate,
    calculate_discount_rate
)
import json
from data.stock_data import (
    get_stock_info,
    get_news
)

symbol = input(
"종목코드 입력 (예: AAPL, 005930.KS): "
)

data = get_stock_info(symbol)


print_company_info(data)

print("=" * 50)

print(f"업종 : {data['sector']}")
print(f"세부업종 : {data['industry']}")

from data.sector_data import (
    get_sector_data
)

sector_data = get_sector_data(
    data["sector"]
)


print_sector_comparison(
    sector_data
)

print("\n===== 상대 비교 =====")
comparison = compare_with_sector(
    data,
    sector_data
)

profile = calculate_profile(
    data,
    sector_data
)

print_profile(
    profile
)

trend_result = print_trend(symbol)

#beta
if data["beta"] is not None:
    print(
        f"\nBeta : {data['beta']:.2f}"
    )
else:
    print("Beta : N/A")



#dcf
dcf_result = print_dcf_analysis(
    data,
    symbol
)


#애널리스트 목표 주가
print_analyst_target(
    data,
    dcf_result["dcf"]["base"]
)
analyst_score = 0


if data["target_price"]:

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

    


# 투자매력도 계산

score = calculate_total_score(

    profile,

    dcf_result["dcf_score"],

    analyst_score

)

print(
    "\n===== 투자 매력도 ====="
)

print(
    f"총점 : {score['total_score']}/100"
)

print(
    f"등급 : {score['investment_grade']}"
)

print(
    f"Value : {score['value_score']}/20"
)
print(
    f"Quality    : {score['quality_score']}/20"
)

print(
    f"Growth     : {score['growth_score']}/20"
)

print(
    f"Safety     : {score['safety_score']}/20"
)

print(
    f"DCF Value  : {score['dcf_score']}/10"
)

print(
    f"Analyst View : {score['analyst_score']}/10"
)


#moat
moat_result = print_economic_moat(
    data,
    dcf_result["discount_rate"],
    sector_data
)

print(
    "\n===== 최종 투자 리포트 ====="
)

print("\n[강점]")

for item in comparison["strengths"]:
    print(
        f"• {item}"
    )

print("\n[약점]")

for item in comparison["weaknesses"]:

    print(
        f"• {item}"
    )


if dcf_result["dcf_score"] <= 5:

    print(
        "• DCF 기준 고평가 상태"
    )

elif dcf_result["dcf_score"] >= 16:

    print(
        "• DCF 기준 저평가 상태"
    )



if score["total_score"] >= 75:

    if moat_result["grade"] in ["Strong", "Exceptional"]:

        print(
            "\n결론 : 우수한 기업이며 장기적인 경쟁우위(Economic Moat)도 확인됩니다."
        )

    else:

        print(
            "\n결론 : 우수한 기업이지만 경쟁우위의 지속성은 추가 확인이 필요합니다."
        )

elif score["total_score"] >= 55:

    if moat_result["grade"] in ["Strong", "Exceptional"]:

        print(
            "\n결론 : 현재 투자매력도는 보통 수준이지만 장기 경쟁력은 우수한 기업입니다."
        )

    else:

        print(
            "\n결론 : 강점과 약점이 공존하는 종목으로 추가 분석이 필요합니다."
        )

elif score["total_score"] >= 45:

    if moat_result["grade"] in ["Strong", "Exceptional"]:

        print(
            "\n결론 : 단기 투자매력은 제한적이지만 경쟁우위는 유지되고 있습니다."
        )

    else:

        print(
            "\n결론 : 투자 매력도는 보통 수준입니다."
        )

else:

    if moat_result["grade"] in ["Strong", "Exceptional"]:

        print(
            "\n결론 : 경쟁우위는 존재하지만 현재 투자매력은 낮아 신중한 접근이 필요합니다."
        )

    else:

        print(
            "\n결론 : 재무 및 밸류에이션 측면에서 신중한 접근이 필요합니다."
        )


#News

    
print("\n===== 최근 뉴스 =====")

news_list = get_news(symbol)

for i, news in enumerate(
    news_list[:3],
    start=1
):

    title = news["content"]["title"]

    summary = news["content"]["summary"]
    
    print(
        f"\n{i}. {title}"
    )

    print(
        f"   {summary}"
    )

