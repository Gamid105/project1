
import openai
import streamlit as st
import os
#os.environ["HTTP_PROXY"] = "http://146.19.25.207:1080"  # Укажите порт вашего прокси-сервера
#os.environ["HTTPS_PROXY"] = "http://146.19.25.207:1080"

# Диагностика версии и пути библиотеки
st.write(f"OpenAI module path: {openai.__file__}")
st.write(f"OpenAI version: {openai.__version__}")

st.title("ChatGPT-like clone")

api_key = st.secrets["general"]["OPENAI_API_KEY"]
openai.api_key = api_key

# Проверка состояния сессии
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Показать сообщения
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Получить ввод пользователя
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Новый способ использования chat API в OpenAI >=1.0.0
        response = openai.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        )
        
        assistant_reply = response['choices'][0]['message']['content']
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

        with st.chat_message("assistant"):
            st.markdown(assistant_reply)

    except openai.OpenAIError as e:  # Обработка ошибок OpenAI API
        st.error(f"OpenAI API error: {e}")
    except Exception as e:  # Общая обработка ошибок
        st.error(f"An unexpected error occurred: {e}")


