# mongoDB connection string
# mongodb+srv: // user1: < password > @cluster0.b3z3fnc.mongodb.net /?retryWrites = true & w = majority

import streamlit as st
import json
import plotly.graph_objects as go
import helper
# import plotly as plt
# import plotly.express as px

st.set_page_config(page_title="Dashboard", page_icon=":tada:", layout="wide")

data = {}

# ---- values = pass and fail value after iterating through file ----
values = []

# -------header_section------

st.title("Welcome to the dashboard")
st.sidebar.subheader("Browse to choose your file")
# ,type=['xml', 'json']
with st.container():
    uploaded_file = st.sidebar.file_uploader("Upload file")
    
if uploaded_file:
    st.write("FileName: ", uploaded_file.name)
    st.write("FileType: ", uploaded_file.type)
    st.write("FileSize: ", uploaded_file.size)
    
    try:
        data = json.load(uploaded_file)

    except Exception as e:
        st.write('Error : Uploaded file is not Formated Appropriately')
        print(e)

    else:
        try:
            with st.expander("See test stages"):
                values = helper.testcases_result(data)

        except Exception as e:
            st.write('Error : Uploaded JSON file is not Formated Appropriately')
            print(e)

        else:
            labels = ['Pass', 'Fail']
            helper.plot_donut(labels, values)
            insert_op = helper.insert_log(uploaded_file.name, uploaded_file.type,
                                          values[0], values[1])

helper.fetch_log()


# ------- Removed Made with streamlit -------
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
