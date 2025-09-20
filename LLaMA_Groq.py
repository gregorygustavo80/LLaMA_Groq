import streamlit as st
from groq import Groq

st.title("💬 Chatbot com Groq + LLaMA 3")
st.write(
    "This is a simple chatbot that uses Groq's LLaMA 3 model to generate responses. "
    "You need to provide a Groq API key to use this app."
)

# Ask user for their Groq API key
groq_api_key = st.text_input("Groq API Key", type="password")
if not groq_api_key:
    st.info("Please add your Groq API key to continue.", icon="🗝️")
else:
    # Create a Groq client
    client = Groq(api_key=groq_api_key)

    # Session state to store chat messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Digite sua mensagem..."):
        # Store and display the user's message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Call LLaMA 3 via Groq
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )
            reply = response.choices[0].message.content

            # Display assistant's reply
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.markdown(reply)

        except Exception as e:
            st.error(f"Erro ao chamar o modelo: {e}")
