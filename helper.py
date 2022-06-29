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


def connect():
    uri = "mongodb+srv://user1:user1.mongo@cluster0.b3z3fnc.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    db = client.Dashboard
    coll = db.files_log
    # returns [0] - client object, [1] - collection to work with.
    return [client, coll]

    

def insert_log(file_name, file_type, success, failure):
    try:
       
        conn = connect()
        coll = conn[1]
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
        conn[0].close()
    return 1


def fetch_log():
   
    conn = connect()
    coll = conn[1]

    cursor = coll.find().sort('timestamp',-1).limit(5)
    for doc in cursor:
        st.write(doc['timestamp'], ' - ', doc['file_name'])
        result =  f"success - {doc['success']}" + " "*10 + f"failure - {doc['failure']}"        
        st.write(result)        
    conn[0].close()

def show_result(file_name, file_type, success, failure):
    conn = connect()
    coll = conn[1]
    cursor = coll.find({"file_name": file_name, "file_type":file_type}).sort("timestamp", -1).limit(1)
    for doc in cursor:
        success_diff = success - doc['success'] 
        failure_diff = failure - doc['failure']
        total_diff = (success+failure) - (doc['success']+doc['failure'])
        col1, col2, col3 = st.columns(3)
            
        with col1:
            st.header('Passed')               
            if success_diff == 0:
                st.title(success)
                # st.subheader(success_diff)  
                st.markdown(
                    f'<h1 style="color:#00FF00;font-size:35px;">{success_diff}</h1>',
                    unsafe_allow_html=True)        
                # st.write('Passed: ',success, ' in Normal, ', success_diff)   
            elif success_diff > 0:
                st.title(success)
                st.markdown(
                    f'<h1 style="color:#00FF00;font-size:35px;">{success_diff}</h1>',
                    unsafe_allow_html=True)  
                # st.subheader(success_diff)
                
                # st.write('Passed: ',success, ' in Green, +', success_diff)
            else: 
                st.title(success)
                # st.subheader(success_diff)
                st.markdown(
                    f'<h1 style="color:#FF0000;font-size:35px;">{success_diff}</h1>',
                    unsafe_allow_html=True)  
                # st.write('Passed: ',success, ' in Red, ', success_diff)

        with col2:
            st.header('Failed')    
            if failure_diff == 0:
                st.title(failure)
                # st.subheader(failure_diff)
                st.markdown(
                    f'<h1 style="color:#00FF00;font-size:35px;">{failure_diff}</h1>',
                    unsafe_allow_html=True)  
                # st.write('Failed: ',failure, ' in Normal, ', failure_diff) 
            elif failure_diff > 0 :
                st.title(failure)
                # st.subheader(failure_diff)
                st.markdown(
                    f'<h1 style="color:#00FF00;font-size:35px;">{failure_diff}</h1>',
                    unsafe_allow_html=True)  
                # st.write('Failed: ',failure, ' in Green, +', failure_diff)
            else:
                st.title(failure)
                # st.subheader(failure_diff)
                st.markdown(
                    f'<h1 style="color:#FF0000;font-size:35px;">{failure_diff}</h1>',
                    unsafe_allow_html=True)  
                # st.write('Failed: ',failure, ' in Red, ', failure_diff)
        
        with col3:
            st.header('Total Cases')
            st.title(success+failure)
            if total_diff >= 0:
                st.markdown(
                    f'<h1 style="color:#00FF00;font-size:35px;">{total_diff}</h1>',
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<h1 style="color:#FF0000;font-size:35px;">{total_diff}</h1>',
                    unsafe_allow_html=True)

    conn[0].close()



def remove_streamlit_tag():
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
