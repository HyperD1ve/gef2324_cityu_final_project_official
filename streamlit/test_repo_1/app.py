import streamlit as st
from menu import menu

import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
cred = credentials.Certificate("your_json_file_here")
if "initialised" not in st.session_state:
    st.session_state.initialised = True
    st.session_state.user = None
    st.session_state.role = None
    firebase_admin.initialize_app(cred)

from firebase_admin import firestore
db = firestore.client()
# it is ok that db is not recognised / gives warning. initialise_app and firestore.client() are only needed on the initial run, and must be commented out for successive reruns.


   
#tentative addition of Teacher as a selectable user type 
USER_TYPES = [None, "Student", "Teacher", "Admin"]
CLASSES = [None, "6A", "6B", "6C", "6D", "6E"]
id = ""

print("rerun")

def login_app(input = "", is_email = True, pwd = ""): 
    if role != None:
        # if role == "Student":
        #     #check for student id in firebase
        # else:
        #     #check for teacher id in firebase
        try:
            if is_email:
                user = auth.get_user_by_email(input)
            else:
                user = auth.get_user(input)
            print(user.uid)
            user_ref = db.collection('users').document(user.uid)
            user_doc = user_ref.get()
            
            if user_doc.exists:
                user_info = user_doc.to_dict() 
                
                print("user data found")
                st.success("user data found!", icon="🎉")
                # print(user.uid[0])
                # print(role[0])
                if user.uid[0] != role[0].lower():
                    st.warning("wrong permissions", icon="⚠")
                    return None
            else:
                print("user data not found")
                st.warning("user data not found", icon="⚠")
                st.session_state.user = None
                return None
            try:
                import requests
                url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyABG0m7zNWI87SIFs3Q_kbHyZ-ab7f8SxI"
                payload = {
                    "email": user.email,
                    "password": pwd,
                    "returnSecureToken": True
                }
                response = requests.post(url, json=payload)
                response_data = response.json()
                if "idToken" in response_data:
                    st.session_state.user = user_info['name']
                    st.session_state.id = user.uid
                    st.session_state.role = role
                    st.success("password authenticated!", icon="🎉") 
                    print("password authenticated, user ID Token:", response_data["idToken"])
                    st.switch_page("pages/user.py")
                    # You can now use the ID token to authenticate requests
                    return response_data
                else:
                    st.warning(f'Error signing in:, {response_data["error"]["message"]}', icon="⚠")
                    print("pwd error, couldn't sign in")
                    st.session_state.user = None
                    return None
            except Exception as e:
                print(f'firebase error: {e}') 
            
        except Exception as e:
            print(f'login error: {e}')
            print("login failed")
            st.warning(f'Login error: {e}', icon="⚠") 
    else:
        print("no role")
        st.error("No role selected!")
    print("didn't log in")


st.header("Log In")
role = st.selectbox("Choose your role", USER_TYPES)
is_email = True
if role != None:
    method = st.selectbox("Choose login method", ["Email", "ID"])
    st.session_state.method = method
    with st.form("user_form"): 
        if st.session_state.method == "Email":
            input = st.text_input("Enter your email:", "Email")
            is_email = True
        else:
            input = st.text_input(f'Enter your {role} ID', "ID")
            is_email = False
        pwd = st.text_input("Enter your password", "", type="password")

        if st.form_submit_button("Log in"):
            print("attempting login")
            login_app(input, is_email, pwd) 
             
menu()