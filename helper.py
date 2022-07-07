import streamlit as st
import plotly.graph_objects as go
import datetime
from pymongo import MongoClient

def xml_result(root):
    success = 0
    failure = 0
    skipped = 0
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
                st.write(root[i][0].attrib)                 
                
            elif(root[i][0].tag=='skipped'):
                skipped += 1
                st.markdown(f'<h1 style="color:#87CEEB;font-size:100%;">{"> SKIPPED "}</h1>', unsafe_allow_html=True)                            
                st.write(root[i][0].attrib)                 
            
            else:
                success += 1
                st.markdown(f'<h1 style="color:#3cd070;font-size:100%;">{"> SUCCEEDED "}</h1>', unsafe_allow_html=True)   
    
    return [success, failure, skipped, tag_count]

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


def connect():
    uri = "mongodb+srv://user1:user1.mongo@cluster0.b3z3fnc.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    db = client.Dashboard
    coll = db.files_log
    # returns [0] - client object, [1] - collection to work with.
    return [client, coll]

    

def insert_log(file_name, file_type, success, failure, skipped):
    try:
       
        conn = connect()
        coll = conn[1]
        ct = datetime.datetime.now()

        insert = [{
            'timestamp': ct,
            'file_name': file_name,
            'success': success,
            'failure': failure,
            'skipped': skipped,
            'file_type': file_type
        }]
        result = coll.insert_many(insert)
        print(result.inserted_ids)
    except Exception as e:
        print("database insert unsuccessful")
        print(e)
        return 0
    else:
        conn[0].close()
    return 1


def fetch_log():
   
    conn = connect()
    coll = conn[1]
    success = 0
    faliure = 0 
    skipped = 0
    cursor = coll.find().sort('timestamp',-1).limit(5)    
    for doc in cursor:
        st.write(doc['timestamp'], ' - ', doc['file_name'])
        success = doc['success']
        faliure = doc['failure']
        skipped = doc['skipped']
        st.markdown(f'<span style="color:#3cd070;font-size:80%;">{" SUCCEEDED - "}{success}</span>\
            <span style="color:#e2062c;font-size:80%;margin-left: 10em;">{" FAILED - "}{faliure}</span>\
            <span style="color:#87CEEB;font-size:80%;margin-left: 10em;">{" SKIPPED - "}{skipped}</span>',unsafe_allow_html=True)
    conn[0].close()

def show_result(file_name, file_type, success, failure, skipped):
    conn = connect()
    coll = conn[1]
    cursor = coll.find({"file_name": file_name, "file_type":file_type}).sort("timestamp", -1).limit(1)
    for doc in cursor:
        success_diff = success - doc['success'] 
        failure_diff = failure - doc['failure']
        skipped_diff = skipped - doc['skipped']
        total_diff = (success+failure+skipped) - (doc['success']+doc['failure']+doc['skipped'])
        col1, col2, col3, col4 = st.columns(4)

        
        with col1:             
            if success_diff == 0:
                st.metric(label="Passed", value=success)    
            elif success_diff > 0:
                st.metric(label="Passed", value=success, delta=success_diff) 
            else: 
                st.metric(label="Passed", value=success, delta=success_diff) 

        with col2:   
            if failure_diff == 0:
                st.metric(label="Failed", value=failure)
            elif failure_diff > 0 :  
                st.metric(label="Failed", value=failure, delta=failure_diff)  
            else:
                st.metric(label="Failed", value=failure, delta=failure_diff)

        with col3:
            if skipped_diff == 0:
                st.metric(label="Skipped", value=skipped)
            elif skipped_diff > 0 :  
                st.metric(label="Skipped", value=skipped, delta=failure_diff)  
            else:
                st.metric(label="Skipped", value=skipped, delta=failure_diff)

        with col4:
            if total_diff == 0:
                st.metric(label="Total cases", value=success+failure+skipped)
            elif total_diff > 0:
                st.metric(label="Total cases", value=success+failure+skipped, delta=total_diff)
            else:
                st.metric(label="Total cases", value=success+failure+skipped, delta=total_diff)  
                
    conn[0].close()

def remove_streamlit_tag():
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
