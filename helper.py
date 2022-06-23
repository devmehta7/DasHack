import streamlit as st
import plotly.graph_objects as go
import datetime
from pymongo import MongoClient


def testcases_result(data):
    success = 0
    failure = 0

    for each in data['testSteps']:
        st.write("* ", each['description'])
        if each['result'] == "SUCCESS":
            st.markdown(
                f'<h1 style="color:#3cd070;font-size:100%;">{"> SUCCEEDED "}</h1>', unsafe_allow_html=True)
            success += 1
        else:
            st.markdown(
                f'<h1 style="color:#e2062c;font-size:100%;">{"> FALIED "}</h1>', unsafe_allow_html=True)
            failure += 1
    return [success, failure]


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
    cursor = coll.find()
    for doc in cursor:
        st.write(doc['timestamp'], ' - ', doc['file_name'])
        st.write("success", ' - ', doc['success'])
        st.write("failure", ' - ', doc['failure'])
    client.close()
