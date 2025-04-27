import streamlit as st
from generator import generate_answer

def main():
    st.set_page_config(page_title="Nugget AI", page_icon="💬", layout="centered")
    st.title("💬Zomato - Nugget AI Assistant")

    if "chat_session_id" not in st.session_state:
        st.session_state.chat_session_id = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        # Add initial bot welcome message
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "🍽️ Hello! I'm your AI Food Assistant. Ask me about restaurants, menus, dishes, or prices — I'll help you find the best options to satisfy your cravings!"
        })

    # --- Display existing chat history ---
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Type your message...")  # Input box stays at bottom

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.spinner("Thinking..."):
            bot_response, session_id = generate_answer(
                user_input, session_id=st.session_state.chat_session_id
            )

        if st.session_state.chat_session_id is None:
            st.session_state.chat_session_id = session_id

        st.session_state.chat_history.append(
            {"role": "assistant", "content": bot_response}
        )
        with st.chat_message("assistant"):
            st.markdown(bot_response)

if __name__ == "__main__":
    main()
