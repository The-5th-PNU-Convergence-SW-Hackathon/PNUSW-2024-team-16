import streamlit as st
import json

questions = [
    {"question": "당신의 직업은?", "answers": ["전문직", "사무직", "자영업자", "공무원", "학생", "무직"], "type": "choice"}, #1
    {"question": "주택 마련 계획이 있나요?", "answers": ["네", "아니오"], "type": "choice"}, #2
        {"question": "희망하는 주택 마련 시점이 언제인가요?", "answers": None, "type": "text"}, #2-1
        {"question": "구체적인 목표 금액이 있나요?", "answers": ["1억 이하", "1억 ~ 3억", "3억 ~ 5억", "5억 ~ 7억", "7억 이상", "생각해본적 없음"], "type": "choice"}, # 2-2
            {"question": "원하는 지역이 있나요?", "answers": ["서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시", "대전광역시", "울산광역시", "세종특별자치시", "경기도", "강원도", "충청북도", "충청남도", "전라북도", "전라남도", "경상북도", "경상남도", "제주특별자치도"], "type": "choice"},  # 2-2-1

    {"question": "차량 마련 계획이 있나요?", "answers": ["네", "아니오"], "type": "choice"}, #2
        {"question": "희망하는 차량 마련 시점이 언제인가요?", "answers": None, "type": "text"}, #2-1
        {"question": "구체적인 목표 금액이 있나요?", "answers": ["1,000만 이하", "1,000만 ~ 3,000만", "3,000만 ~ 5,000만", "5,000만 ~ 7,000만", "7,000만 ~ 9,000만", "9,000만 이상"], "type": "choice"}, # 2-2

    {"question": "결혼 유무?", "answers": ["미혼", "기혼"], "type": "choice"}, #2-3
        {"question": "결혼 계획이 있나요?", "answers": ["네", "아니오"], "type": "choice"}, # 미혼 선택시 2-3-1
            {"question": "결혼 계획이 있다면 언제인가요?", "answers": None, "type": "text"}, # 예 선택시 2-3-1-1
    {"question": "자녀가 있나요?", "answers": ["네", "아니오"], "type": "choice"}, # 기혼 선택시 2-3-2
        {"question": "자녀가 있다면 몇 명인가요?", "answers": None, "type": "text"}, # 예 선택시 2-3-2-1
            {"question": "자녀의 나이가 몇 세인가요? ex) 2세, 6세", "answers": None, "type": "text"}, # 예 선택시 2-3-2-2
        {"question": "추가 자녀 계획이 있나요?", "answers": ["네", "아니오"], "type": "choice"}, # 2-3-2-3
            {"question": "추가 자녀 계획이 있다면 몇 명인가요?", "answers": None, "type": "text"}, # 2-3-2-3-1
        {"question": "자녀 계획이 있나요?", "answers": ["네", "아니오"], "type": "choice"},
            {"question": "자녀 계획이 있다면 몇 명인가요?", "answers": None, "type": "text"},

    {"question": "희망 은퇴 연령은 몇 세인가요?", "answers": None, "type": "text"},
    {"question": "예상 퇴직금은 얼마인가요?", "answers": None, "type": "text"},
    {"question": "은퇴 후 계획이 무엇인가요?", "answers": ["자영업", "재취업", "여가생활"], "type": "choice"},
    {"question": "은퇴 후 희망하는 월 생활비가 얼마인가요?", "answers": None, "type": "text"},
]
 
def show_survey():
    st.title(f"Question {st.session_state.current_question + 1}")
    current_q = questions[st.session_state.current_question]
    st.write(current_q["question"])
    
    answer = None
    if current_q["type"] == "choice":
        answer = st.radio("Your answer", current_q["answers"], key=str(st.session_state.current_question))
    elif current_q["type"] == "text":
        answer = st.text_input("Your answer", key=str(st.session_state.current_question))
    
    if st.button("Next") and answer is not None:
        # Add the answer to the dictionary
        st.session_state.answers[current_q["question"]] = answer
        if st.session_state.current_question == 1:
            if answer == "네":  # 주택
                st.session_state.current_question += 1  # Go on
            else:
                st.session_state.current_question += 4  # Skip to question 6

        elif st.session_state.current_question == 3:  # If at question 4
            if answer == "생각해본적 없음":
                st.session_state.current_question += 1  # Go on
            else:
                st.session_state.current_question += 2  # Skip to question 6

        elif st.session_state.current_question == 5:
            if answer == "네":  # 차량
                st.session_state.current_question += 1  # Go on
            else: 
                st.session_state.current_question += 3
        
        elif st.session_state.current_question == 8:
            if answer == "미혼":  # 결혼
                st.session_state.current_question += 1  # Go on
            else:
                st.session_state.current_question += 3
        
        elif st.session_state.current_question == 9:
            if answer == "네":  # 결혼
                st.session_state.current_question += 1  # Go on
            else:
                st.session_state.current_question += 2

        
        elif st.session_state.current_question == 11:
            if answer == "네":  # 자녀
                st.session_state.current_question += 1  # Go on
            else:
                st.session_state.current_question += 5

        elif st.session_state.current_question == 14:
            if answer == "네":  # 자녀
                st.session_state.current_question += 1  # Go on
            else:
                st.session_state.current_question += 4
        
        elif st.session_state.current_question == 16:
            if answer == "네":  # 자녀
                st.session_state.current_question += 1  # Go on
            else:
                st.session_state.current_question += 2



        elif st.session_state.current_question < len(questions) - 1:
            st.session_state.current_question += 1  # Normal flow
        else:
            st.session_state.show_submit_button = True
        st.experimental_rerun()

        
    if st.button("Previous") and st.session_state.current_question > 0:
        st.session_state.answers.pop()
        st.session_state.current_question -= 1
        st.experimental_rerun()


questions_mapping = {
    "job": "당신의 직업은?",
    "has_house_plan": "주택 마련 계획이 있나요?",
    "desired_house_time": "희망하는 주택 마련 시점이 언제인가요?",
    "house_target_amount": "구체적인 목표 금액이 있나요?",
    "desired_region": "원하는 지역이 있나요?",
    "has_car_plan": "차량 마련 계획이 있나요?",
    "desired_car_time": "희망하는 차량 마련 시점이 언제인가요?",
    "car_target_amount": "구체적인 목표 금액이 있나요?",
    "marital_status": "결혼 유무?",
    "has_marriage_plan": "결혼 계획이 있나요?",
    "marriage_plan_time": "결혼 계획이 있다면 언제인가요?",
    "has_children": "자녀가 있나요?",
    "num_children": "자녀가 있다면 몇 명인가요?",
    "children_ages": "자녀의 나이가 몇 세인가요? ex) 2세, 6세",
    "plan_more_children": "추가 자녀 계획이 있나요?",
    "num_more_children": "추가 자녀 계획이 있다면 몇 명인가요?",
    "has_child_plan": "자녀 계획이 있나요?",
    "planned_num_children": "자녀 계획이 있다면 몇 명인가요?",
    "desired_retirement_age": "희망 은퇴 연령은 몇 세인가요?",
    "expected_retirement_funds": "예상 퇴직금은 얼마인가요?",
    "post_retirement_plan": "은퇴 후 계획이 무엇인가요?",
    "desired_monthly_expenses_post_retirement": "은퇴 후 희망하는 월 생활비가 얼마인가요?"
}

def save_results():
    # Invert the mapping to use questions as keys for lookup
    questions_mapping_inv = {v: k for k, v in questions_mapping.items()}

    # Convert answers to use simple keys
    simple_key_answers = {questions_mapping_inv[question]: answer for question, answer in st.session_state.answers.items()}

    # Save the answers using simple keys to JSON file
    with open("./data/answers.json", "w", encoding='utf-8') as f:
        json.dump(simple_key_answers, f, ensure_ascii=False)

    #st.title("Survey Results")
    # for q in questions:
    #     # Ensure the answer key exists in the answers dictionary
    #     if q['question'] in st.session_state.answers:
    #         st.write(f"{q['question']} : {st.session_state.answers[q['question']]}")
