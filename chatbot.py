import streamlit as st
import requests
import openai
from streamlit_chat import message
from get_user_data import user_data
import time
from streamlit_extras.streaming_write import write

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
API_TOKEN = st.secrets["secrets"]['API_TOKEN']  # Replace with your actual token
headers = {"Authorization": f"Bearer {API_TOKEN}"}
openai.api_key = st.secrets["secrets"]['OPENAI_API_KEY']

def chatwrite(texttowrite):
    lines = texttowrite.split('\n')
    for line in lines:
        yield line + "\n"
        time.sleep(0.05)

def chatbot():
    # App Header
    st.header("🤖 AI 챗봇 산지니")

    # Session State for Messages
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []
    
    # Function to Query API (you need to replace this with your actual implementation)
    # def query(payload):
    #     response = requests.post(API_URL, headers=headers, json=payload)
    #     return response.json()

    # Form and User Input
    with st.form('form', clear_on_submit=True):
        user_input = st.text_input('"Hi, 산지니" 버튼을 눌러 산지니에게 인사해보세요! ', '', key='input', placeholder="질문을 입력하세요")
        submitted = st.form_submit_button('Hi, 산지니')

    user_info = user_data()
    system_message = f"너는 산지니이고, 나의 금융 조언가야. 나의 정보는 다음과 같아: {user_info}"
    # Initial message from the chatbot on first interaction
    if not user_input:
        user_input = "안녕 산지니, 나의 정보에 기반해서, 금융 전문가로서의 조언을 제공해줄 수 있어?"
        pass

    andy_message = "이제부터 너는 똑똑하고 표현력이 풍부하며 친근한 전지전능한 인공지능 비서 산지니를 연기하도록 해. 나의 금융 상황을 명확히 인지하고, 앞으로의 계획에 따라 조언을 해줘."\
     "너는 은행 어플리케이션에 탑재돼있어.."\
     "그리고 부족한 정보가 있으면 적극적으로 질문해. 그리고 처음 말할 때: 안녕하세요👋, 저는 산지니입니다. 물어봐주셔서 감사합니다😊\" 라고 인사해." \
     "그리고 다음 질문에 대답해."
    
    ending_message = """
     (질문이 영어로 되어 있어도 한글로 대답하세요. 기억하세요. 잘못된 정보는 피하세요. 의심스러우면 사과하고 계속 대답하지 마세요.)
     """
    
    prompt = andy_message + user_input + ending_message
    
    # If User Input is Provided
    if submitted and user_input:
        
        with st.spinner("산지니가 꼼꼼한 조언을 위해 열심히 고민하고있어요... 조금만 기다려주세요!"):
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ]
            )
            response = completion.choices[0].message.content
        
        #with st.chat_message("assistant", avatar="https://github.com/JinukHong/shadowFunk/assets/45095330/eceff742-486e-46d8-b501-72efede31c25"):
            # st.write(f"{response}")
            #write(chatwrite(response))
            # st.divider()
            # write(chatwrite(translated_response))

        # Update Session States
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)

        # Displaying past interactions and responses
        # for message, resp in zip(st.session_state.past, st.session_state.generated):
        #     st.write(f"You: {message}")
        #     st.write(f"Chatbot: {resp}")

    # Display Past Messages and Responses
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            #st.sidebar.write(f"You: {st.session_state['past'][i]}")
            #st.sidebar.write(f"AI Secretary: {st.session_state['generated'][i]}")
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
