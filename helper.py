import streamlit as st
import plotly.graph_objects as go
import datetime
from pymongo import MongoClient

def xml_result(root):
    success = 0
    failure = 0
    tag_count = 0    
    try:
        for node in root[1][1][0].findall("test-method"):
            tag_count += 1        
        for i in range(tag_count):
            st.write("* ", root[1][1][0][i].attrib['signature'])                                
            if(root[1][1][0][i].attrib['status']=='PASS'):
                success += 1
                st.markdown(f'<h1 style="color:#3cd070;font-size:100%;">{"> SUCCEEDED "}</h1>', unsafe_allow_html=True)       
            else:
                failure += 1
                st.markdown(f'<h1 style="color:#e2062c;font-size:100%;">{"> FALIED "}</h1>', unsafe_allow_html=True)    
    except:                                    
        for node in root.findall("testcase"):
            tag_count += 1       
        for i in range(1,tag_count+1):                                        
            st.write("* ", root[i].attrib['name'])                              
            if(root[i][0].tag=='failure'):
                failure += 1
                st.markdown(f'<h1 style="color:#e2062c;font-size:100%;">{"> FALIED "}</h1>', unsafe_allow_html=True)          
            else:
                success += 1
                st.markdown(f'<h1 style="color:#3cd070;font-size:100%;">{"> SUCCEEDED "}</h1>', unsafe_allow_html=True)   
    return [success, failure, tag_count]

def json_result(data):
    success = 0
    failure = 0
    key_count = 0

    for each in data['testSteps']:
        key_count += 1
        st.write("* ", each['description'])
        if each['result'] == "SUCCESS":
            st.markdown(
                f'<h1 style="color:#3cd070;font-size:100%;">{"> SUCCEEDED "}</h1>', unsafe_allow_html=True)
            success += 1
        else:
            st.markdown(
                f'<h1 style="color:#e2062c;font-size:100%;">{"> FALIED "}</h1>', unsafe_allow_html=True)
            failure += 1            
    return [success, failure, key_count]

def plot_donut(labels, values):

    fig = go.Figure()
    fig.add_trace(go.Pie(labels=labels, values=values,
                         hole=0.4))

    st.header('Test cases success-rate')
    st.plotly_chart(fig)


def insert_log(file_name, file_type, success, failure):
    try:
        uri = "mongodb+srv://user1:user1.mongo@cluster0.b3z3fnc.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri)
        db = client.Dashboard

        coll = db.files_log
        ct = datetime.datetime.now()

        insert = [{
            'timestamp': ct,
            'file_name': file_name,
            'success': success,
            'failure': failure,
            'file_type': file_type
        }]
        result = coll.insert_many(insert)
        print(result.inserted_ids)
    except Exception as e:
        print("database insert unsuccessful")
        print(e)
        return 0
    else:
        client.close()
    return 1


def fetch_log():
    uri = "mongodb+srv://user1:user1.mongo@cluster0.b3z3fnc.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    db = client.Dashboard
    coll = db.files_log    
    cursor = coll.find().sort('timestamp',-1).limit(5)
    success = 0
    failure = 0
    for doc in cursor:
        st.write(doc['timestamp'], ' - ', doc['file_name'])
        success = doc['success']
        faliure = doc['failure']
        st.markdown(f'<span style="color:#3cd070;font-size:80%;">{" SUCCEEDED - "}{success}</span>\
            <span style="color:#e2062c;font-size:80%;margin-left: 10em;">{" FAILED - "}{faliure}</span>',unsafe_allow_html=True)
    client.close()

def remove_streamlit_tag():
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)