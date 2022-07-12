# mongoDB connection string
# mongodb+srv: // user1: < password > @cluster0.b3z3fnc.mongodb.net /?retryWrites = true & w = majority

import helper
import streamlit as st
import json
import xml.etree.ElementTree as ET

def execute_dashboard(user):
    # ---------------------------- header_section ----------------------------
    st.title("Welcome to the dashboard")        
    if(st.sidebar.button('Logout')):
        helper.logout()
    st.sidebar.subheader("Browse to choose your file")    

    uploaded_file = st.sidebar.file_uploader(" ")

    if(uploaded_file):
        st.write("FileName: ", uploaded_file.name)
        st.write("FileType: ", uploaded_file.type)
        st.write("FileSize: ", uploaded_file.size, ' bytes')

    # ---------------------------- For XML file ----------------------------
        if(uploaded_file.type == "text/xml"):
            try:
                tree = ET.parse(uploaded_file)
                root = tree.getroot()
            except Exception as e:
                st.markdown(
                    f'<h1 style="color:#e2062c;font-size:100%;">{"Error : Uploaded file is not Formated Appropriately"}</h1>',
                    unsafe_allow_html=True)
                print(e)
            else:
                try:
                    with st.expander("Displaying All the Test Stages"):
                        values = helper.xml_result(root)
                    helper.show_ss()
                    helper.show_result(user,
                        uploaded_file.name, uploaded_file.type, values[0], values[1], values[2])

                except Exception as e:
                    st.markdown(
                        f'<h1 style="color:#e2062c;font-size:100%;">{"Error : Uploaded XML file is not Formated Appropriately"}</h1>',
                        unsafe_allow_html=True)
                    print(e)

                else:
                    labels = ['Passed', 'Failed', 'Skipped']
                    helper.plot_donut(labels, values)
                    insert_op = helper.insert_log(user, uploaded_file.name, uploaded_file.type,
                                                  values[0], values[1], values[2])

    # ---------------------------- For JSON file ----------------------------
        elif(uploaded_file.type == "application/json"):
            try:
                data = json.load(uploaded_file)
            except Exception as e:
                st.markdown(
                    f'<h1 style="color:#e2062c;font-size:100%;">{"Error : Uploaded file is not Formated Appropriately"}</h1>',
                    unsafe_allow_html=True)
                print(e)
            else:
                try:
                    with st.expander("See test stages"):
                        values = helper.json_result(data)
                    helper.show_result(uploaded_file.name,
                                       uploaded_file.type, values[0], values[1])

                except Exception as e:
                    st.markdown(
                        f'<h1 style="color:#e2062c;font-size:100%;">{"Error : Uploaded file is not Formated Appropriately"}</h1>',
                        unsafe_allow_html=True)
                    print(e)

                else:
                    labels = ['Pass', 'Fail']
                    helper.plot_donut(labels, values)
                    insert_op = helper.insert_log(uploaded_file.name, uploaded_file.type,
                                                  values[0], values[1])

    # ---------------------------- For file is neither JSON nor XML ----------------------------
        else:
            st.markdown(
                f'<h1 style="color:#e2062c;font-size:100%;">{"Error : Uploaded file is not a valid file"}</h1>',
                unsafe_allow_html=True)

    # ---------------------------- For History ----------------------------
    with st.expander("See History"):
        helper.fetch_log(user)
