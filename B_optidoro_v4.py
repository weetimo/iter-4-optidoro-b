
import streamlit as st

import time
import pandas as pd
from datetime import datetime
# import numpy as np

from gspread_pandas import Spread,Client
from google.oauth2 import service_account


import random

if 'user' not in st.session_state:
    st.session_state['user'] = random.random()

# Disable certificate verification
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# if 'scope' not in st.session_state:
#     st.session_state['scope'] = []

# if 'credentials' not in st.session_state:
#     st.session_state['credentials'] = None

# if 'spread' not in st.session_state:
#     st.session_state['spread'] = None

# if 'sh' not in st.session_state:
#     st.session_state['sh'] = None

# @st.cache()
# def init_connection():

#     st.session_state['scope'] = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']


#     # The above code is creating a scope for the Google API.

#     st.session_state['credentials'] = service_account.Credentials.from_service_account_info(
#                     st.secrets["gcp_service_account"], scopes = st.session_state['scope'])
#     client = Client(scope=st.session_state['scope'],creds=st.session_state['credentials'])
#     spreadsheetname = "HCI and AI"
#     st.session_state['spread'] = Spread(spreadsheetname,client = client)

#     st.write(st.session_state['spread'].url)

#     st.session_state['sh'] = client.open(spreadsheetname)
#     global worksheet_list
#     worksheet_list = sh.worksheets()
#     return

# Create a Google Authentication connection object

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)
client = Client(scope=scope,creds=credentials)
spreadsheetname = "HCI and AI"
spread = Spread(spreadsheetname,client = client)

# Check the connection
# st.write(spread.url)

sh = client.open(spreadsheetname)
worksheet_list = sh.worksheets()

# Spreadsheet (database) Functions 
@st.cache()
# Get our worksheet names
def worksheet_names():
    sheet_names = []   
    for sheet in worksheet_list:
        sheet_names.append(sheet.title)  
    return sheet_names

# Get the sheet as dataframe
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

#get a list of all keys in st.session_state


# Update to Sheet
def update_the_spreadsheet(spreadsheetname,dataframe):
    col = ['Timestamp','User', 'session_type', 'Effort', 'Fatigue', 'minutes_today',
    'cancel_clicked', 'break_minutes', 'extend_counter', 'countdown_time', 'form_on',
    'extend_clicked', 'cycle_counter', 'extend', 'time_minutes', 'begin_clicked',
    'daily_focus_score', 'daily_effort_score', 'dev_mode'
    
    
    ]
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)

from gsheetsdb import connect
gsheet_url = "https://docs.google.com/spreadsheets/d/19xhszrZtww1Z-x3WeOSm2zW9D8TqqIAHWNzH8En9IY4/edit?usp=sharing"

@st.cache()
def begin_connection():
    global conn
    conn = connect()
    return

begin_connection()


if 'csv_filepath' not in st.session_state:
    st.session_state['csv_filepath'] = "/Users/timothywee/Documents/SUTD Term 5/HCI and AI/Week 10/Smart Pomodoro/HCI-and-AI-smart-pomodoro/optidoro-production copy/actual_HCI_data.csv"
#     st.session_state['csv_filepath'] = "actual_HCI_data.csv"

#CHANGE THIS TO LOCAL FILEPATH
# local_CSV_filepath = st.session_state['csv_filepath']

if 'disable_begin' not in st.session_state:
    st.session_state['disable_begin'] = False

if 'run_finished' not in st.session_state:
    st.session_state['run_finished'] = False

if 'begin_clicked' not in st.session_state:
    st.session_state['begin_clicked'] = False

if 'extend' not in st.session_state:
    st.session_state['extend'] = False

if 'session_type' not in st.session_state:
    st.session_state['session_type'] = 'Standard Pomodoro'

# st.write(st.session_state)

def begin_callback():
    # st.session_state['break_minutes'] += 5
    st.session_state['countdown_time'] = time_minutes * 60
    st.session_state.run_finished = False
    st.session_state.cancel_clicked = False
    st.session_state.begin_clicked = True 
    st.session_state['minutes_today'] += 25
    st.session_state['extend_counter'] = 0



if 'cancel_clicked' not in st.session_state:
    st.session_state['cancel_clicked'] = False

def cancel_callback():
    #st.session_state['break_minutes'] -= 5 + st.session_state['extend_counter'] * 5
    st.session_state.run_finished = True
    st.session_state.begin_clicked = False
    st.session_state.cancel_clicked = True 
    #st.session_state['extend_counter'] = 0
    #st.session_state['disable_begin'] = False
    st.session_state['minutes_today'] -= (25 * st.session_state['extend_counter'] + 25)


if 'extend_clicked' not in st.session_state:
    st.session_state['extend_clicked'] = False

def extend_callback():
    st.session_state['countdown_time'] += 1500
    st.session_state.run_finished = False
    st.session_state.cancel_clicked = False
    st.session_state.begin_clicked = True 
    st.session_state['extend'] = True
    st.session_state['extend_counter'] += 1
    st.session_state['minutes_today'] += 25 #check this
    #combined_count_down(st.session_state['countdown_time'])

if 'countdown_time' not in st.session_state:
    st.session_state['countdown_time'] = 0

if 'break_minutes' not in st.session_state: 
    st.session_state['break_minutes'] = 2700

if 'time_minutes' not in st.session_state:
    st.session_state['time_minutes'] = 0

if 'minutes_today' not in st.session_state:
    st.session_state['minutes_today'] = 0

if 'form_on' not in st.session_state:
    st.session_state.form_on = False

if 'dev_mode' not in st.session_state:
    st.session_state.dev_mode = False

if 'cycle_counter' not in st.session_state: 
    st.session_state['cycle_counter'] = 0

# if 'break_counter' not in st.session_state: 
#     st.session_state['break_counter'] = 0

# if 'subject_array' not in st.session_state:
#     st.session_state['subject_array'] = subject_array = ["Machine Learning", "HCI and AI", "Service Design Studio", "HASS"]

if 'multiplier' not in st.session_state:
    st.session_state['multiplier'] = 1 #change this to 1 in deployment

# if 'suggested_cycle_value' not in st.session_state:
#     st.session_state['suggested_cycle_value'] = 25

# if 'suggested_break_value' not in st.session_state:
#     st.session_state['suggested_break_value'] = 5

if 'daily_focus_score' not in st.session_state:
    st.session_state['daily_focus_score'] = 0

if 'daily_effort_score' not in st.session_state:
    st.session_state['daily_effort_score'] = 0

if 'extend_counter' not in st.session_state:
    st.session_state['extend_counter'] = 0

# if 'autopilot_work' not in st.session_state:
#     st.session_state['autopilot_work'] = False

# st.write(st.session_state)

def get_keys():
    keys = []
    for key in st.session_state:
        keys.append(key)
    return keys

# st.write(get_keys())

# df = pd.read_csv(local_CSV_filepath) 

# graph_df = df[['subject', 'time_minutes']]
# # graph_df['time_now'] = pd.to_datetime(graph_df['time_now'])

# #st.line_chart(graph_df)

# st.write(st.session_state)

def combined_count_down(ts):
    
    # if st.button("CANCEL"): #fix later
    #     st.session_state['break_minutes'] -= 5 #idk why this does not work
    #     #ts = 0

    # if st.button("EXTEND"):
    #     st.session_state['break_minutes'] += 5
    #     st.session_state['countdown_time'] += 1500  
    #     ts += 1500  
    
    # with st.empty():
        
    #     while st.session_state['countdown_time']:
    #         mins, secs = divmod(st.session_state['countdown_time'], 60)
    #         time_now = '{:02d}:{:02d}'.format(mins, secs)
    #         st.header(f"{time_now}")
    #         time.sleep(float(st.session_state['multiplier']))
    #         st.session_state['countdown_time'] -= 1
    #time_minutes = int(ts/60) #save this somewhere

    # if st.session_state['autopilot_work'] == True:
    #     ts = 6000 - 60 * st.session_state['minutes_today']

    with st.empty():
        
        while ts:
            mins, secs = divmod(ts, 60)
            time_now = '{:02d}:{:02d}'.format(mins, secs)
            st.header(f"{time_now}")
            time.sleep(float(st.session_state['multiplier']))
            ts -= 1
            st.session_state['countdown_time'] -= 1

        # if st.session_state['autopilot_work'] == True:
        #     st.session_state['autopilot_work'] = False
        #     st.session_state['minutes_today'] = 100
        #     st.experimental_rerun()
        
        st.session_state.run_finished = True

        #st.session_state['disable_begin'] = False
        st.success("Work cycle over! Time for a break!")

        #begin break counter
        
        global form_on
        form_on = True
        # st.session_state['minutes_today'] += 25
        st.session_state['cycle_counter'] += 1
        st.session_state.form_on = True
        st.experimental_rerun()
    return

st.title("Optidoro Timer")

if st.session_state['minutes_today'] <= 100:
    progress_bar = st.session_state['minutes_today']
else:
    progress_bar = 100

st.progress(progress_bar)
st.caption("Learning Faster & Greater")
#st.write(st.session_state)

#st.line_chart(df)
time_minutes = 25
#time_minutes = st.number_input('Enter the study time in minutes ', min_value=0, max_value=50, value=st.session_state['suggested_cycle_value'])
global break_time_minutes
break_time_minutes = 5
#break_time_minutes = st.number_input('Enter the break time in minutes ', min_value=0, max_value=50, value=st.session_state['suggested_break_value'])

# global subject
# subject = st.selectbox('Subject: ', st.session_state.subject_array)
#st.write(st.session_state)

# cancel_placeholder = st.empty()
# with cancel_placeholder.container():
#     if st.button("CANCEL"): #fix later
#         st.session_state['break_minutes'] -= 5 #idk why this does not work
#         #ts = 0


# st.write(st.session_state)
mins, secs = divmod(st.session_state['break_minutes'], 60)
time_now = '{:02d}:{:02d}'.format(mins, secs)

# time_now = '{:02d}:{:02d}'.format(divmod(st.session_state['break_minutes'], 60))
#col1, col2 = st.columns(2)

break_mins, break_secs = divmod(st.session_state['break_minutes'], 60)
break_time_now = '{:02d}:{:02d}'.format(break_mins, break_secs)
st.metric("Remaining break time", break_time_now)

# with col1:
#     break_mins, break_secs = divmod(st.session_state['break_sec'], 60)
#     break_time_now = '{:02d}:{:02d}'.format(break_mins, break_secs)
#     st.metric("Remaining break time", break_time_now)

# with col2: 
#     break_mins, break_secs = divmod(st.session_state['break_sec'], 60)
#     break_time_now = '{:02d}:{:02d}'.format(break_mins, break_secs)
#     st.metric("Remaining study time", time_now)


if (st.button("Begin work cycle", on_click=begin_callback, disabled=st.session_state['disable_begin']) or st.session_state['extend']): #or st.session_state['autopilot_work']: #how to hide begin button when timer is running?
    if st.session_state['countdown_time'] != 0:
        #st.session_state['disable_begin'] = True
        st.write("Work cycle in progress")
    # st.metric("Upcoming break time", st.session_state['break_minutes'])
    
    # if st.session_state['countdown_time'] == 0: #idk what this is, check again
    #     st.session_state['countdown_time'] = time_minutes * 60
    
    

    if not st.session_state.run_finished:
        
        
        # if st.button("Extend your current cycle", help="Extends current work cycle by 25 minutes.", on_click=extend_callback):
        #     #combined_count_down(st.session_state['countdown_time'])
        #     pass

            # st.empty()
            # # st.write(st.session_state['countdown_time'])
            # # st.write(st.session_state['break_minutes'])
            # combined_count_down(st.session_state['countdown_time'])
        if st.button("End current cycle", help="By clicking this button, you will end your current work cycle. Time spent on this cycle will not be counted.", on_click=cancel_callback): #fix 
            pass

    
    # if st.session_state['countdown_time'] == 0:
    #     st.session_state['cancel_clicked'] = True

    if not st.session_state.cancel_clicked:
        st.session_state['extend'] = False
        #st.session_state['disable_begin'] = True
        combined_count_down(st.session_state['countdown_time'])
        

if st.session_state.cancel_clicked:
    st.session_state.cancel_clicked = False
    st.experimental_rerun()

if not st.session_state['disable_begin']:
    st.session_state['disable_begin'] = False


    

#st.write(df)

if st.session_state.form_on: #triggers when timer is up

    with st.form("How was the session?"):
        effort_score = st.slider("Effort score: ", min_value=1, max_value=10, value=5)
        focus_score = st.slider("Fatigue score: ", min_value=1, max_value=10, value=5)
        st.write("Click the begin button to start your next session.")
        submitted = st.form_submit_button("Save and start break", help='This will start counting down your remaining break time.') #submit

        if submitted:
        #import CSV as a dataframe
            st.session_state['daily_focus_score'] += focus_score
            st.session_state['daily_effort_score'] += effort_score
            st.session_state.form_on = False
            now = datetime.now()
            opt = {'Timestamp': now, 'User': st.session_state['user'], 'session_type': st.session_state['session_type'], 
                    'Effort': effort_score, 'Fatigue': focus_score, 'minutes_today': st.session_state['minutes_today'], 
                    'cancel_clicked': st.session_state['cancel_clicked'], 'break_minutes': st.session_state['break_minutes'],
                    'extend_counter': st.session_state['extend_counter'], 'countdown_time': st.session_state['countdown_time'],
                    'form_on': st.session_state['form_on'], 'extend_clicked': st.session_state['extend_clicked'],'cycle_counter': st.session_state['cycle_counter'],
                    'extend': st.session_state['extend'], 'time_minutes': st.session_state['time_minutes'], 
                    'begin_clicked': st.session_state['begin_clicked'], 'daily_focus_score': st.session_state['daily_focus_score'], 'daily_effort_score': st.session_state['daily_effort_score'],
                    'dev_mode': st.session_state['dev_mode']


                    }
            opt_df = pd.DataFrame(opt, index=[0])
            df = load_the_spreadsheet('data')
            new_df = df.append(opt_df, ignore_index=True)
            update_the_spreadsheet('data', new_df)
            # df.loc[len(df)] = [str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), subject, time_minutes, effort_score, focus_score]
            
            #private gsheets implementation
            # now = datetime.now()
            # opt = {'Timestamp': [now], 'Effort': [effort_score], 'Focus': [focus_score]}
            # opt_df = pd.DataFrame(opt)
            # df = load_the_spreadsheet('HCI and AI')
            # new_df = df.append(opt_df, ignore_index=True)
            # update_the_spreadsheet('HCI and AI', new_df)


            # df.to_csv(local_CSV_filepath, index=False) 
            st.session_state.form_on = False
            st.success('Your effort score and focus score have been recorded. Please wait while we start your break.')
            #st.write(df)
            
            time.sleep(2)
            # st.experimental_rerun()

            st.header("Break time!")
            # ts = break_time_minutes * 60
            if st.session_state['cycle_counter'] == 4:
                ts = 1800 * st.session_state['multiplier']
            else:    
                ts = 300 * st.session_state['multiplier']

            with st.empty():
                while ts:
                    mins, secs = divmod(ts, 60)
                    time_now = '{:02d}:{:02d}'.format(mins, secs)
                    st.header(f"{time_now}")
                    time.sleep(float(st.session_state['multiplier']))
                    #st.session_state['']
                    ts -= 1
                    st.session_state['break_minutes'] -= 1

                    # if st.session_state['break_minutes'] == 0:
                    #     st.session_state['autopilot_work'] = True





            
            st.success("Break cycle over! ")
            time.sleep(2)
            st.experimental_rerun()

#create a dataframe called graph_df from df, with only the timestamp, subject, and minutes_today columns

st.metric("Minutes today", st.session_state['minutes_today'])

#st.metric("Pomodoro cycles today", st.session_state['cycle_counter'])
# st.metric("Upcoming break time", st.session_state['break_minutes'])
# if st.session_state['minutes_today'] >= 100: 
#     st.write("You win chicken drumstick!")

# if st.button("Tired scenario"):
#     st.warning("You seem to be tired. Let the AI determine the best cycles for you.")
#     time.sleep(4)
#     st.session_state['suggested_cycle_value'] = 20
#     st.session_state['suggested_break_value'] = 10
#     st.experimental_rerun()

# st.session_state.dev_mode = st.checkbox('dev mode')
# st.caption("Makes timer run faster, displays CSV")
# if st.session_state.dev_mode == True:
#     st.session_state['multiplier'] = 0.001
#     st.write(df)

# if st.session_state.dev_mode == False:
#     st.session_state['multiplier'] = 1

dev_mode = st.checkbox('dev mode', value=st.session_state.dev_mode)
st.caption("Makes timer run faster for testing purposes.")

if dev_mode == True:
    st.session_state.dev_mode == True
    st.session_state['multiplier'] = 0.005
    #display CSV file
    # df = pd.read_csv(st.session_state.csv_filepath)
    # st.write(df)
    # st.write(st.experimental_user)    

if dev_mode == False:
    st.session_state['multiplier'] = 1
    st.session_state.dev_mode == False

if st.session_state['minutes_today'] >= 100:
    st.write("You have completed the study! Congratulations! Submit your scores if you haven't, and enjoy the remainder of your break!")
    st.write("Complete the post-study survey here to finish the session:")
    link = '[Here](https://forms.gle/dY5VJVyzKEVWMV1w9)'
    st.markdown(link, unsafe_allow_html=True)



