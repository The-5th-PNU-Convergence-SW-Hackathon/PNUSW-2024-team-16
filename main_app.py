import streamlit as st
# from web_demo2 import show_financial_advisor  # Importing the function
from survey import save_results, show_survey
from web_demo2 import show_financial_advisor

def main():
    show_financial_advisor()
    
    # if 'current_question' not in st.session_state:
    #     st.session_state.current_question = 0
    # if 'answers' not in st.session_state:
    #     st.session_state.answers = {}
    # if 'submitted' not in st.session_state:
    #     st.session_state.submitted = False
    # if 'show_submit_button' not in st.session_state:
    #     st.session_state.show_submit_button = False
    
    # if st.session_state.submitted:
    #     save_results()
    #     #fin_calender()
    #     show_financial_advisor()
    # elif st.session_state.show_submit_button:
    #     if st.button("Submit"):
    #         st.session_state.submitted = True
    #     if st.button("Go back to the last question"):
    #         st.session_state.show_submit_button = False
    #         # st.session_state.current_question = len(questions) - 1
    # else:
    #    show_survey