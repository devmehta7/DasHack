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
st.subheader("Browse to choose your JSON file")

with st.container():
    uploaded_file = st.sidebar.file_uploader(
        "Upload File", type=['xml', 'json'])

if uploaded_file:
    st.write("FileName: ", uploaded_file.name)
    st.write("FileType: ", uploaded_file.type)
    st.write("FileSize: ", uploaded_file.size)
    try:
        data = json.load(uploaded_file)

    except Exception as e:
        st.write('Error : Uploaded JSON file is not Formated Appropriately')
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

# ------- Removed Made with streamlit -------
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
