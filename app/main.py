import streamlit as st
from prompts import query_llm

WELCOME_MESSAGE = "Hi! I am your Kent Student Assistant. Ask me anything."


def init_session() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": WELCOME_MESSAGE,
            }
        ]


def render_chat() -> None:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def generate_response(user_text: str) -> str:
    try:
        return query_llm(user_text)
    except Exception as exc:
        return (
            "I ran into an issue while generating a response. "
            "Please try again in a moment.\n\n"
            f"Details: {exc}"
        )


def reset_chat() -> None:
    st.session_state.messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]


def chat_input_area() -> tuple[str, bool]:
    with st.form("chat_form", clear_on_submit=True):
        user_text = st.text_input("Message", placeholder="Ask a question...")
        submitted = st.form_submit_button("Send")
    return user_text, submitted


def handle_user_input(user_text: str, submitted: bool) -> None:
    if not submitted or not user_text.strip():
        return

    clean_text = user_text.strip()
    st.session_state.messages.append({"role": "user", "content": clean_text})

    with st.spinner("Thinking..."):
        bot_reply = generate_response(clean_text)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.rerun()


def main() -> None:
    st.set_page_config(page_title="Kent Student Assistant", page_icon="🎓")
    st.title("🎓 Kent Student Assistant")
    st.caption("University of Kent student assistant chatbot")

    init_session()

    if st.button("Clear chat"):
        reset_chat()
        st.rerun()

    render_chat()
    user_text, submitted = chat_input_area()
    handle_user_input(user_text, submitted)


if __name__ == "__main__":
    main()
