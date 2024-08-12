import json


def read_data():
    with open('./data/answers.json', 'r', encoding='utf-8') as file:
        content = file.read()

    # Parse the JSON content into a Python dictionary
    answers = json.loads(content)
    return answers

def user_data():
    answers = read_data()
    

    job = answers.get("job", None)
    if job == "전문직":
        income = 76120000
    elif job == "사무직":
        income = 36700000
    elif job == "자영업자":
        income = 37280000
    elif job == "공무권":
        income = 65271607
    else:
        income = 0

    has_house_plan = answers.get("has_house_plan", None)
    desired_house_time = answers.get("desired_house_time", None)
    house_target_amount = answers.get("house_target_amount", None)
    desired_region = answers.get("desired_region", None)

    if desired_region:
        if desired_region == '서울특별시':
            house_target_amount = 982740000
        elif desired_region == '경기도':
            house_target_amount = 69960000
        elif desired_region == '부산광역시' or "대구광역시" or "인천광역시" or "광주광역시" or "대전광역시" or "울산광역시" or "세종특별자치시":
            house_target_amount = 53262000
        else:
            house_target_amount = 42207000
    else:
        if house_target_amount == "1억 이하":
            house_target_amount = 100000000
        elif house_target_amount == "1억 ~ 3억":
            house_target_amount = 200000000
        elif house_target_amount == "3억 ~ 5억":
            house_target_amount = 400000000
        elif house_target_amount == "5억 ~ 7억":
            house_target_amount = 600000000
        elif house_target_amount == "7억 이상":
            house_target_amount = 800000000

    has_car_plan = answers.get("has_car_plan", None)
    desired_car_time = answers.get("desired_car_time", None)
    car_target_amount = answers.get("car_target_amount", None)
    marital_status = answers.get("marital_status", None)
    has_marriage_plan = answers.get("has_marriage_plan", None)
    marriage_plan_time = answers.get("marriage_plan_time", None)
    has_children = answers.get("has_children", None)
    num_children = answers.get("num_children", None)
    children_ages = answers.get("children_ages", None)
    plan_more_children = answers.get("plan_more_children", None)
    plan_more_children = answers.get("plan_more_children", None)
    num_more_children = answers.get("num_more_children", None)
    has_child_plan = answers.get("has_child_plan", None)
    planned_num_children = answers.get("planned_num_children", None)
    desired_retirement_age = answers.get("desired_retirement_age", None)
    expected_retirement_funds = answers.get("expected_retirement_funds", None)
    post_retirement_plan = answers.get("post_retirement_plan", None)
    desired_monthly_expenses_post_retirement = answers.get("desired_monthly_expenses_post_retirement", None)

    # User's age isn't provided in the questions. Assuming it's available as `age`.

    # Generating future plans based on answers.
    future_plan = []
    if has_house_plan == "네":
        future_plan.append(f"Plan to secure housing by age {desired_house_time} with target amount {house_target_amount} in region {desired_region}")
    if has_car_plan == "네":
        future_plan.append(f"Plan to acquire a car by age {desired_car_time} with a budget of {car_target_amount}")
    if marital_status == "미혼" and has_marriage_plan == "네":
        future_plan.append(f"Plan to get married by age {marriage_plan_time}")
    if (has_children == "네" or has_child_plan == "네"):
        future_plan.append(f"Plans related to children: Currently has {num_children} child(ren) aged {children_ages}, " +
                        f"Plans for more children: {plan_more_children}, Planned number of children: {planned_num_children}")
    future_plan.append(f"Desires to retire by age {desired_retirement_age} with an expected retirement fund of {expected_retirement_funds}. " +
                    f"Post retirement plan: {post_retirement_plan}, Desired monthly expenses post retirement: {desired_monthly_expenses_post_retirement}")

    # Concatenate future plans into a string.
    future_plan_str = ', '.join(future_plan)

    # Create user_info string.
    user_info = f"User's Job: {job}, Monthly Income(krw): {income*10000}, Future Plan: {future_plan_str}"

    # Display user_info string.
    return user_info
