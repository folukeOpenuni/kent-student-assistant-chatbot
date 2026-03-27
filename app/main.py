import streamlit as st
from config import OPENAI_API_KEY
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
    if "is_generating" not in st.session_state:
        st.session_state.is_generating = False
    if "last_error" not in st.session_state:
        st.session_state.last_error = None


def render_chat() -> None:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def generate_response(user_text: str) -> str:
    return query_llm(user_text)


def render_status() -> None:
    if st.session_state.is_generating:
        st.info("Generating response...")
    if st.session_state.last_error:
        st.error(f"Last error: {st.session_state.last_error}")


def ensure_required_config() -> None:
    """Show a clear setup message for missing required secrets."""
    if OPENAI_API_KEY:
        return

    st.error("Missing configuration: `OPENAI_API_KEY` is not set.")
    st.markdown(
        "Set `OPENAI_API_KEY` in Streamlit Cloud app secrets "
    )
    st.stop()


def reset_chat() -> None:
    st.session_state.messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]
    st.session_state.is_generating = False
    st.session_state.last_error = None


def style_chat_input() -> None:
    st.markdown(
        """
        <style>
        div[data-testid="stChatInput"] textarea {
            border-radius: 24px !important;
            border: 1px solid #d9d9d9 !important;
            padding: 14px 48px 14px 16px !important;
            box-shadow: none !important;
        }

        div[data-testid="stChatInput"] button {
            border-radius: 999px !important;
            width: 36px !important;
            height: 36px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def chat_input_area() -> str | None:
    return st.chat_input("Type your message here...")


def handle_user_input(user_text: str | None) -> None:
    if not user_text or not user_text.strip():
        return

    clean_text = user_text.strip()
    st.session_state.last_error = None
    st.session_state.messages.append({"role": "user", "content": clean_text})
    st.session_state.is_generating = True

    try:
        with st.spinner("Thinking..."):
            bot_reply = generate_response(clean_text)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    except Exception as exc:
        st.session_state.last_error = str(exc)
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": ("I ran into an issue while generating a response. Please try again in a moment."),
            }
        )
    finally:
        st.session_state.is_generating = False

    st.rerun()


def main() -> None:
    st.set_page_config(page_title="Kent Student Assistant", page_icon="🎓")
    st.title("🎓 Kent Student Assistant")
    st.caption("University of Kent student assistant chatbot")
    ensure_required_config()
    style_chat_input()

    init_session()
    render_status()

    if st.button("Clear chat"):
        reset_chat()
        st.rerun()

    render_chat()
    user_text = chat_input_area()
    handle_user_input(user_text)


if __name__ == "__main__":
    main()
