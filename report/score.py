def calculate_total_score(
    profile,
    dcf_score=0,
    analyst_score=0
):

    grade_score = {

        "A": 20,
        "B": 15,
        "C": 10,
        "D": 5,
        "N/A": 0

    }

    value_score = grade_score.get(
        profile["value_grade"],
        0
    )

    quality_score = grade_score.get(
        profile["quality_grade"],
        0
    )

    growth_score = grade_score.get(
        profile["growth_grade"],
        0
    )

    safety_score = grade_score.get(
        profile["safety_grade"],
        0
    )

    total_score = (

        value_score

        + quality_score

        + growth_score

        + safety_score

        + dcf_score

        + analyst_score

    )

    if total_score >= 85:

        investment_grade = "A+"

    elif total_score >= 75:

        investment_grade = "A"

    elif total_score >= 65:

        investment_grade = "B+"

    elif total_score >= 55:

        investment_grade = "B"

    elif total_score >= 45:

        investment_grade = "C"

    else:

        investment_grade = "D"

    return {

        "total_score": total_score,

        "investment_grade": investment_grade,

        "value_score": value_score,

        "quality_score": quality_score,

        "growth_score": growth_score,

        "safety_score": safety_score,

        "dcf_score": dcf_score,

        "analyst_score": analyst_score,


    }