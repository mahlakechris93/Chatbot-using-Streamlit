import streamlit as st
import requests
import json

def get_ai_response(messages_payload, model):
    api_key = "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" 
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        data=json.dumps({
            "model": model,
            "messages": messages_payload,
            "max_tokens": 1000,
            "temperature": 0.7,
        })
    )
    if response.status_code != 200:
        st.error("Error: " + response.text)
        return None
    answer = response.json()["choices"][0]["message"]["content"]
    return answer

st.title("Chatbot Assistant (Lunga)")

model_options = {
    "Mistral 7B (Free)": "mistralai/mistral-7b-instruct:free",
    "DeepSeek V3 (Free)": "deepseek/deepseek-chat-v3-0324:free",
    "Llama 3.1 8B (Free)": "meta-llama/llama-3.1-8b-instruct:free"
}

#Model Selector
selected_model_name = st.selectbox(
    "Made by Chris Mahlake",
    options=list(model_options.keys()),
    index=0,
)
selected_model = model_options[selected_model_name]


if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

        #Get AI Response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Create API Request
                messages_for_api = st.session_state.messages.copy()
                #  HIT FUNCTION API
                ai_response = get_ai_response(messages_for_api, selected_model)
                if ai_response:
                    st.markdown(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                else:
                    st.error("Error")
