import streamlit as st

def logout():
    if "user" in st.session_state:
        st.session_state.user = None
    # Deleting session state elements
    for key in list(st.session_state.keys()):  # Use list() to avoid runtime error
        print(f'Deleting {key}')
        del st.session_state[key]  # Correct way to delete the session state entry

def authenticated_menu():
    # print(st.session_state.role)
    st.sidebar.button("Log out", on_click=logout)
    st.sidebar.page_link("pages/user.py", label="Your profile")
    st.sidebar.page_link("pages/paper_gen.py", label="Do a paper")
    st.sidebar.page_link("pages/chat.py", label="Chat with LLM")
    st.sidebar.page_link(
        "pages/upload.py",
        label="Upload your data",
        disabled = not (st.session_state.role == "Student" or st.session_state.role == "Admin"),
    )
    st.sidebar.page_link(
        "pages/view.py",
        label="View student summary",
        disabled = not (st.session_state.role == "Teacher" or st.session_state.role == "Admin"),
    )  
    
def unauthenticated_menu():
    st.sidebar.page_link("app.py", label="Log in")
    st.sidebar.page_link("pages/paper_gen.py", label="Do a paper")
    st.sidebar.page_link("pages/chat.py", label="Chat with LLM") 
    
def menu():
    if "user" not in st.session_state or st.session_state.user is None:
        unauthenticated_menu()
        return
    authenticated_menu()
    
def menu_with_redirect():
    if "user" not in st.session_state or st.session_state.user is None:
        print("redirected back to main page")
        st.switch_page("app.py")
    menu() 