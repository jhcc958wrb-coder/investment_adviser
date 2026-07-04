import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
from data.stock_data import get_stock_info
from report.score import calculate_total_score
from report.profile import calculate_profile
from report.comparison import compare_with_sector
from data.sector_data import get_sector_data
from report.dcf_report import print_dcf_analysis
from report.analyst import print_analyst_target
from valuation.dcf import calculate_discount_rate

def format_market_cap(value):

    if value is None:
        return "N/A"

    if value >= 1_000_000_000_000:
        return f"${value/1_000_000_000_000:.2f}T"

    elif value >= 1_000_000_000:
        return f"${value/1_000_000_000:.2f}B"

    elif value >= 1_000_000:
        return f"${value/1_000_000:.2f}M"

    else:
        return f"${value:,}"

def get_price_chart(symbol):

    df = yf.download(
        symbol,
        period="1y",
        auto_adjust=False,
        progress=False
    )
    print(df.head())

    print(df.columns)

    if df.empty:
        return None

    close = df.xs(
        "Close",
        axis=1,
        level=0
    ).iloc[:, 0]

    ma20 = close.rolling(20).mean()
    ma60 = close.rolling(60).mean()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=close.index,
            y=close,
            name="Close"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=ma20,
            mode="lines",
            name="MA20"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=ma60,
            mode="lines",
            name="MA60"
        )
    )

    fig.update_layout(

        title="",

        xaxis_title="",

        yaxis_title="Price",

        template="plotly_white",

        height=550

    )

    return fig

st.set_page_config(
    page_title="Investment Advisor",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Investment Advisor")
st.caption("Powered by Yahoo Finance")


symbol = st.text_input(
    "종목코드",
    placeholder="AAPL, MSFT, TSLA..."
)

analyze = st.button("🔍 Analyze")

if analyze:
    
    data = get_stock_info(symbol)
    
    sector_data = get_sector_data(
        data["sector"]
    )

    sector_data = get_sector_data(
        data["sector"]
    )

    profile = calculate_profile(
        data,
        sector_data
    )

    dcf_result = print_dcf_analysis(
        data,
        symbol
    )
    
    analyst_result = print_analyst_target(
        data,
        dcf_result["dcf"]["base"]
    )

    score = calculate_total_score(
        profile,
        dcf_result["dcf_score"],
        analyst_result["analyst_score"]
    )

    comparison = compare_with_sector(
        data,
        sector_data
    )

    profile = calculate_profile(
        data,
        sector_data
    )

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏢 Overview",
        "📋 Investment Profile",
        "💰 Valuation",
        "🛡 Economic Moat",
        "📈 Price Chart",
        "🏆 Overall Investment Rating"
    ])

    with tab1:

        st.header(f"🏢 {data['company']}")

        st.caption(
            f"{data['sector']} • {data['industry']}"
        )

        st.divider()

        st.subheader("📈 Market Information")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Current Price",
                f"${data['price']:.2f}"
            )

        with col2:

            st.metric(
                "Market Cap",
                format_market_cap(
                    data["market_cap"]
                )
            )

        with col3:

            st.metric(
                "Beta",
                f"{data['beta']:.2f}"
                if data["beta"] is not None
                else "N/A"
            )

        st.divider()

        st.subheader("📊 Fundamental Metrics")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "PER",
                f"{data['per']:.2f}"
                if data["per"] is not None
                else "N/A"
            )

        with col2:

            st.metric(
                "PBR",
                f"{data['pbr']:.2f}"
                if data["pbr"] is not None
                else "N/A"
            )

        with col3:

            st.metric(
                "ROE",
                f"{data['roe']*100:.2f}%"
                if data["roe"] is not None
                else "N/A"
            )

        col4, col5, col6 = st.columns(3)

        with col4:

            st.metric(
                "EPS",
                f"{data['eps']:.2f}"
                if data["eps"] is not None
                else "N/A"
            )

        with col5:

            st.metric(
                "Debt Ratio",
                f"{data['debt_ratio']:.2f}"
                if data["debt_ratio"] is not None
                else "N/A"
            )

        with col6:

            st.metric(
                "Dividend Yield",
                f"{data['dividend_yield']*100:.2f}%"
                if data["dividend_yield"] is not None
                else "N/A"
            )


    with tab2:

        st.divider()


        st.subheader("📋 Investment Profile")

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "💰 Value",
                profile["value_grade"]
            )

            st.caption(
                "Valuation"
            )

        with col2:

            st.metric(
                "💹 Quality",
                profile["quality_grade"]
            )

            st.caption(
                "Profitability"
            )

        with col3:

            st.metric(
                "📈 Growth",
                profile["growth_grade"]
            )

            st.caption(
                "Growth Potential"
            )

        with col4:

            st.metric(
                "🛡 Safety",
                profile["safety_grade"]
            )

            st.caption(
                "Financial Stability"
            )

        with st.expander("ℹ️ How are these grades determined?"):

            st.markdown("""

        ### 💰 Value
        - Evaluated using **PER** and **PBR**
        - Compared with the industry average
        - Lower PER and PBR generally receive higher grades.

        ---

        ### 💹 Quality
        - Evaluated using **ROE**
        - Compared with the industry average
        - Higher ROE generally receives a higher grade.

        ---

        ### 📈 Growth
        - Evaluated using **Revenue Growth** and **Earnings Growth**
        - Compared with the industry average
        - Higher growth rates receive higher grades.

        ---

        ### 🛡 Safety
        - Evaluated using **Debt Ratio**
        - Compared with the industry average
        - Lower debt ratio receives a higher grade.

        """)

        st.header("")
        st.subheader("📊 Sector Comparison")
        comparison_table = pd.DataFrame({

            "Metric": [

                "PER",

                "PBR",

                "ROE",

                "Revenue Growth",

                "Earnings Growth",

                "Debt Ratio"

            ],

            "Company": [

                f"{data['per']:.2f}" if data["per"] is not None else "N/A",

                f"{data['pbr']:.2f}" if data["pbr"] is not None else "N/A",

                f"{data['roe']*100:.2f}%"
                if data["roe"] is not None else "N/A",

                f"{data['revenue_growth']*100:.1f}%"
                if data["revenue_growth"] is not None else "N/A",

                f"{data['earnings_growth']*100:.1f}%"
                if data["earnings_growth"] is not None else "N/A",

                f"{data['debt_ratio']:.2f}"
                if data["debt_ratio"] is not None else "N/A"

            ],

            "Sector": [

                f"{sector_data['PER']:.2f}",

                f"{sector_data['PBR']:.2f}",

                f"{sector_data['ROE']:.2f}%",

                f"{sector_data['RevenueGrowth']:.1f}%",

                f"{sector_data['EarningsGrowth']:.1f}%",

                f"{sector_data['Debt']:.2f}"

            ],

            "Difference": [

                f"{comparison['per_diff']:+.1f}%",
                f"{comparison['pbr_diff']:+.1f}%",
                f"{comparison['roe_diff']:+.1f}%",
                f"{comparison['revenue_diff']:+.1f}%p",
                f"{comparison['earnings_diff']:+.1f}%p",
                f"{comparison['debt_diff']:+.1f}%"

            ],

            "Status": [

                "🟢 Lower"
                if data["per"] < sector_data["PER"]
                else "🔴 Higher",

                "🟢 Lower"
                if data["pbr"] < sector_data["PBR"]
                else "🔴 Higher",

                "🟢 Higher"
                if data["roe"]*100 > sector_data["ROE"]
                else "🔴 Lower",

                "🟢 Higher"
                if data["revenue_growth"]*100 > sector_data["RevenueGrowth"]
                else "🔴 Lower",

                "🟢 Higher"
                if data["earnings_growth"]*100 > sector_data["EarningsGrowth"]
                else "🔴 Lower",

                "🟢 Lower"
                if data["debt_ratio"] < sector_data["Debt"]
                else "🔴 Higher"

            ]

        })
        st.dataframe(

            comparison_table,

            hide_index=True,

            use_container_width=True

        )
        st.caption(
            "Comparison with industry average."
        )

    with tab3:

        st.header("💰 Valuation")

        st.caption(
            "DCF는 미래 현금흐름을 현재가치로 할인하여 계산한 기업의 내재가치입니다."
        )

        st.subheader("📊 Valuation Summary")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Current Price",
                f"${data['price']:.2f}"
            )

        with col2:

            st.metric(
                "DCF Value",
                f"${dcf_result['dcf']['base']:.2f}"
            )

            if dcf_result["gap"] > 20:

                st.error(
                    f"🔴 DCF Gap : {dcf_result['gap']:+.1f}%"
                )

            elif dcf_result["gap"] < -20:

                st.success(
                    f"🟢 DCF Gap : {dcf_result['gap']:+.1f}%"
                )

            else:

                st.info(
                    f"🟡 DCF Gap : {dcf_result['gap']:+.1f}%"
                )


            with col3:

                if data["target_price"] is not None:

                    st.metric(
                        "Target Price",
                        f"${data['target_price']:.2f}"
                    )

                    upside = (
                        (data["target_price"] - data["price"])
                        / data["price"]
                    ) * 100

                    if upside > 0:

                        st.success(
                            f"📈 Analyst Upside : {upside:.1f}%"
                        )

                    else:

                        st.error(
                            f"📉 Analyst Downside : {upside:.1f}%"
                        )

                else:

                    st.metric(
                        "Target Price",
                        "N/A"
                    )



        st.divider()

        st.subheader("📈 Growth Assumptions")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "DCF Growth Rate",
                f"{dcf_result['base_growth']*100:.1f}%"
            )

        with col2:

            st.metric(
                "Discount Rate",
                f"{dcf_result['discount_rate']*100:.1f}%"
            )

        st.divider()

        st.subheader("📊 DCF Scenarios")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Conservative",
                f"${dcf_result['dcf']['bear']:.2f}"
            )

        with col2:

            st.metric(
                "Base",
                f"${dcf_result['dcf']['base']:.2f}"
            )

        with col3:

            st.metric(
                "Optimistic",
                f"${dcf_result['dcf']['bull']:.2f}"
            )

        st.divider()

        st.subheader("🎯 Analyst View")

        if data["target_price"] is not None:

            upside = (
                (data["target_price"] - data["price"])
                / data["price"]
            ) * 100

            analyst_gap = (
                (data["target_price"]
                - dcf_result["dcf"]["base"])
                / dcf_result["dcf"]["base"]
            ) * 100

            col1, col2, col3 = st.columns(3)
            with col1:

                st.metric(
                    "Target Price",
                    f"${data['target_price']:.2f}"
                )

            with col2:

                st.metric(
                    "Analyst Upside",
                    f"{upside:+.1f}%"
                )

            with col3:

                st.metric(
                    "DCF vs Analyst",
                    f"{analyst_gap:+.1f}%"
                )

        st.divider()

        st.subheader("📝 Interpretation")

        if dcf_result["gap"] > 20:

            st.warning(
                "⚠️ 추정된 DCF는 미래 성장 기대가 거의 반영되지 않은 현재 현금흐름 중심의 추정치입니다."
            )

            st.info(
                "현재 주가는 DCF 기준으로 고평가된 상태로 평가됩니다."
            )

        elif dcf_result["gap"] < -20:

            st.success(
                "현재 주가는 DCF 기준으로 저평가된 상태로 평가됩니다."
            )

        else:

            st.info(
                "현재 주가는 DCF 기준 적정 가치 수준으로 평가됩니다."
            )

        if data["target_price"] is not None:

            if upside > 0:

                st.success(
                    "📈 애널리스트들은 추가 상승 여력이 있다고 평가하고 있습니다."
                )

            else:

                st.error(
                    "📉 애널리스트들은 현재 주가 대비 하락 가능성을 전망하고 있습니다."
                )

                
           


    with tab4:
        st.subheader("🛡 Economic Moat")
        st.caption(
            "Economic Moat는 기업이 장기간 경쟁우위를 유지할 수 있는 능력을 의미합니다."
        )
        st.caption("Economic Moat는 ROE와 Cost of Equity의 차이(Spread)를 기반으로 평가됩니다.")

        discount_rate = calculate_discount_rate(
            data["beta"]
        )*100

        roe = data["roe"] * 100
        spread = roe - discount_rate

        # Moat 등급 계산
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

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "ROE",
                f"{roe:.2f}%"
            )

        with col2:

            st.metric(
                "Cost of Equity",
                f"{discount_rate:.2f}%"
            )

        with col3:

            st.metric(
                "Spread",
                f"{spread:+.2f}%"
            )

        st.divider()

        st.metric(
            "🏰 Economic Moat",
            moat_grade,
            f"{moat_score}/10"
        )


        # 설명
        if moat_grade == "Exceptional":

            st.success(
                "🟢 압도적인 경쟁우위를 보유한 기업으로 자본비용을 크게 초과하는 수익을 창출하고 있습니다."
            )

        elif moat_grade == "Strong":

            st.info(
                "🔵 자본비용을 안정적으로 상회하며 경쟁력을 유지하고 있습니다."
            )

        elif moat_grade == "Moderate":

            st.warning(
                "🟡 자본비용을 소폭 상회하며 평균 이상의 경쟁우위를 유지하고 있습니다."
            )

        elif moat_grade == "Weak":

            st.warning(
                "🟠 경쟁우위는 존재하지만 뚜렷하지 않습니다."
            )

        else:

            st.error(
                "🔴 자본비용보다 낮은 수익성을 보이고 있어 경쟁우위를 확인하기 어렵습니다."
            )

        # 부채비율 평가
        st.divider()

        st.subheader("📊 Leverage Analysis")

        if (
            data["debt_ratio"] is not None
            and data["debt_ratio"] < sector_data["Debt"]
        ):

            st.success(
                "✅ 업종 평균보다 낮은 부채 수준에서도 높은 수익성(ROE)을 유지하고 있습니다."
            )

        elif (
            data["debt_ratio"] is not None
            and data["debt_ratio"] > sector_data["Debt"] * 1.5
        ):

            st.warning(
                "⚠️ 높은 부채가 ROE를 크게 높였을 가능성이 있습니다."
            )

        elif (
            data["debt_ratio"] is not None
            and data["debt_ratio"] > sector_data["Debt"]
        ):

            st.info(
                "ℹ️ 부채 사용이 일부 수익성(ROE) 향상에 기여했을 수 있습니다."
            )

      
        

    with tab5:
        st.subheader("📈 Price Chart")

        st.caption(
            "최근 1년간 주가와 20일·60일 이동평균선을 제공합니다."
        )
        fig = get_price_chart(symbol)

        if fig is not None:

            st.plotly_chart(
                fig,
                width="stretch"
            )
        else:

            st.error("차트를 불러올 수 없습니다.")

    with tab6:
        st.header("🏆 Overall Investment Rating")
        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Overall Score",
                f"{score['total_score']}/100"
            )

        with col2:

            st.metric(
                "Investment Grade",
                score["investment_grade"]
            )

        st.progress(
            score["total_score"] / 100
        )
        st.caption(
            "The score combines Value, Quality, Growth, Safety, DCF valuation and Analyst expectations."
        )

        st.divider()

        st.subheader("📊 Score Breakdown")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "💰 Value",
                f"{score['value_score']}/20"
            )

            st.metric(
                "💹 Quality",
                f"{score['quality_score']}/20"
            )

        with col2:

            st.metric(
                "📈 Growth",
                f"{score['growth_score']}/20"
            )

            st.metric(
                "🛡 Safety",
                f"{score['safety_score']}/20"
            )

        with col3:

            st.metric(
                "💵 DCF",
                f"{score['dcf_score']}/10"
            )

            st.metric(
                "🎯 Analyst",
                f"{score['analyst_score']}/10"
            )

        if score["investment_grade"] == "A" or "A+":

            st.success(
                "🟢 높은 투자 매력도를 보유한 우수 기업입니다."
            )

        elif score["investment_grade"] == "B" or "B+":

            st.info(
                "🔵 장기 투자 관점에서 긍정적으로 검토할 수 있는 기업입니다."
            )

        elif score["investment_grade"] == "C":

            st.warning(
                "🟡 장점과 단점이 공존하는 평균 수준의 투자 매력도를 보입니다."
            )

        else:

            st.error(
                "🔴 투자 매력도가 낮아 추가 검토가 필요합니다."
            )

        st.divider()

        st.subheader("📝 Final Opinion")

        for strength in comparison["strengths"]:

            st.success(
                f"✅ {strength}"
            )

        for weakness in comparison["weaknesses"]:

            st.warning(
                f"⚠️ {weakness}"
            )

        if score["investment_grade"] == "A" or "A+":

            st.success(
                "현재 투자매력도가 높고 장기 경쟁력도 우수한 기업입니다."
            )

        elif score["investment_grade"] == "B" or "B+":

            st.info(
                "현재 투자매력도는 양호하며 장기 경쟁력도 기대할 수 있는 기업입니다."
            )

        elif score["investment_grade"] == "C":

            st.warning(
                "투자 전 추가적인 검토가 필요한 기업입니다."
            )

        else:

            st.error(
                "현재 투자매력도가 낮아 신중한 접근이 필요합니다."
            )