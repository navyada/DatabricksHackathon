import streamlit as st
from streamlit_chat import message
from streamlit.components.v1 import html
from model import baseModel


model = baseModel()
def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.past.append(user_input)
    st.session_state.generated.append(model.respond(user_input))

def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]


st.session_state.setdefault(
    'past', 
    []
)
st.session_state.setdefault(
    'generated', 
    []
)

st.title("Please input your product description:")

chat_placeholder = st.empty()

with chat_placeholder.container():    
    for i in range(len(st.session_state['generated'])):  

        message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
        message(
            st.session_state['generated'][i], 
            key=f"{i}", 
            allow_html=True,
            is_table=False
        )
    
    # st.button("Post Now!", on_click=post_twitter)
    st.button("Clear message", on_click=on_btn_click)
    

with st.container():
    st.text_input("User Input:", on_change=on_input_change, key="user_input")
