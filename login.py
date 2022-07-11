import streamlit as st
import helper
import app

# ---------------------------- permenant dashboard configuration ----------------------------                   
st.set_page_config(page_title="Dashboard",
                   page_icon="chart_with_upwards_trend", layout="wide")

# ---------------------------- Removed the tag: Made with streamlit  ----------------------------                   
helper.remove_streamlit_tag()

# ---------------------------- Initialize the screen to login page ----------------------------                   
if 'login_status' not in st.session_state:
	st.session_state.login_status = False

user = ""
authenticateTheUser = st.container()

with authenticateTheUser:
    menu = ["Home", "Login", "SignUP"]
    choice = st.selectbox("MENU", menu)    

    if choice == "Login":   
        user = helper.login()
        if(user!=False):                        
            st.session_state.login_status = True
        else:            
            st.session_state.login_status = False        

    elif choice == "SignUP":
        st.subheader("Create New Account ")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("SignUp"):
            conn = helper.connect('users')
            coll = conn[1]
            check_user = coll.find({"username": new_user})
            result = list(check_user)
            if(len(result)!=0):
                user = f"_{new_user}_"
                st.warning('select a different username, ' + user + ' already exists !')  
            else:
                signup = coll.insert_one(
                    {"username": new_user, "password": new_password})
                if signup:
                    st.success(
                        "You have Successfully created a Valid Account")
                    st.info("Go to Login Menu to Login")
                else:
                    st.warning("please try again")
            conn[0].close()
            
    elif choice == "Home":           
        if(st.session_state.login_status):
            app.execute_dashboard(user)
        else:
            st.title("Welcome to the dashboard")
            st.warning('please log in first to access the dashboard')        
