import streamlit as st
from streamlit_chat import message
from request_handler import request_handler


st.set_page_config(
    page_title="FIS Chatbot - Demo",
    page_icon=":robot:"
)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

deepl_api_key = st.secrets['deepl_api_key']

st.title("FIS Chatbot")

st.write("Hey, welcome to the FIS chatbot beta! You can ask me a question below.")

translate = st.checkbox("Other than Czech?")


def get_text():
    input_text = st.text_input("You: ", key="input")
    return input_text


user_input = get_text()

if user_input:
    # output = query({
    #    "inputs": {
    #        "past_user_inputs": st.session_state.past,
    #        "generated_responses": st.session_state.generated,
    #        "text": user_input,
    #    },"parameters": {"repetition_penalty": 1.33},
    # })

    st.session_state.past.append(user_input)

    # payload = {'id': 123, 'question': user_input}
    # response = requests.post(API_URL, headers=headers, json=payload)
    # answer = response.json()['answer']

    answer = request_handler(user_input, deepl_api_key, translate=translate)

    st.session_state.generated.append(f'You asked: {user_input}, Answer is: {answer}')

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
