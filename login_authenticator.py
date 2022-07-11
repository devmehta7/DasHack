import streamlit as st
import helper
import app
import streamlit_authenticator as stauth

st.set_page_config(page_title="Dashboard",
                   page_icon="chart_with_upwards_trend", layout="wide")

helper.remove_streamlit_tag()


def fetch_user():
    conn = helper.connect('users')
    coll = conn[1]
    cur = coll.find({})
    return cur


def auth():
    cur = fetch_user()
    usernames = passwords = []
    for each_user in cur:
        # print(each_user['username'])
        # print(each_user['password'])
        usernames.append(each_user['username'])
        passwords.append(each_user['password'])

    hashed_passwords = stauth.hasher(passwords).generate()
    authenticator = stauth.Authenticate(
        [], usernames, hashed_passwords, 'my_cookie', 'my_key')
    authentication_status, username = authenticator.login(
        "Login", "main")

    if authentication_status == False:
        st.error("Incorrect Username/Password")

    if authentication_status == None:
        st.warning("Please enter your username and password")

    if authentication_status:
        print("login successful")


auth()

# with st.container():
#     menu = ["Login", "SignUP"]
#     choice = st.selectbox("Menu", menu)
#     if choice == "Login":
#         st.subheader("Login Section")

#         username = st.text_input("User Name")
#         password = st.text_input("Password", type='password')

#         if st.button("Login"):
#             conn = helper.connect('users')
#             coll = conn[1]
#             login = coll.find_one(
#                 {"username": username, "password": password})
#             if login:
#                 st.success("Logged In as {}".format(username))
#                 app.execute_dashboard()
#             else:
#                 st.warning("Incorrect Username/Password")

#             conn[0].close()

#     elif choice == "SignUP":
#         st.subheader("Create New Account ")
#         new_user = st.text_input("Username")
#         new_password = st.text_input("Password", type='password')

#         if st.button("SignUp"):
#             conn = helper.connect('users')
#             coll = conn[1]
#             signup = coll.insert_one(
#                 {"username": new_user, "password": new_password})
#             if signup:
#                 st.success(
#                     "You have Successfully created an Valid Account")
#                 st.info("Go to Login Menu to Login")
#             else:
#                 st.warning("please try again")
#             conn[0].close()
