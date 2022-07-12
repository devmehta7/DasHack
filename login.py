import streamlit as st
import helper
import app

# ---------------------------- permenant dashboard configuration ----------------------------                   
# st.set_page_config(page_title="Dashboard",
#                 page_icon="chart_with_upwards_trend", layout="wide")

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
        if(user!=None and user!=False):                        
            st.session_state.login_status = True
        else:            
            st.session_state.login_status = False        

    elif choice == "SignUP":
        helper.signup(user)
            
    elif choice == "Home":                  
        if(st.session_state.login_status):
            app.execute_dashboard(user)
        else:
            st.title("Welcome to the dashboard")
            st.warning('please log in first to access the dashboard')        
