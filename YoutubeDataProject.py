import googleapiclient.discovery
import mysql.connector
import pymongo
import streamlit as st
import datetime
from PIL import Image
import pandas as pd

# Google API details
api_service_name = "youtube"
api_version = "v3"
# MongoDB database and connection details
database = 'myyoutubeproject'
myMDBclient = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
# creating/selecting database and collections
my_mdb = myMDBclient[database]

#mysql connection deatils
#mySqldb = mysql.connector.connect(host="127.0.0.1",port=3306,user="root",password="Mysql123@",database= "guviyoutube")
mySqldb = mysql.connector.connect(user='root', password='Mysql123@',host='127.0.0.1', database='guviyoutube',auth_plugin='mysql_native_password')
myCursor = mySqldb.cursor()


# --------------Retrieve channel Data from youtube---------------
# FUNCTION TO GET CHANNEL DETAILS
def collect_channel_details(channel_id):
    try:
        #st.success('YouTube Data Extraction Started!!!')  
        channel_data = []
        response = youtube.channels().list(part = 'snippet,contentDetails,statistics',id= channel_id).execute()
        for i in range(len(response['items'])):
            data = dict(#Channel_id = response['items'][0]['id'],
                        channelId =  response['items'][i]['id'],
                        channelName = response['items'][i]['snippet']['title'],
                        description = response['items'][i]['snippet']['description'],
                        country = response['items'][i]['snippet'].get('country'),
                        #Playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'],
                        subscribers_Count = response['items'][i]['statistics']['subscriberCount'],
                        channel_ViewCount = response['items'][i]['statistics']['viewCount'],
                        videos_Count = response['items'][i]['statistics']['videoCount']             
                        )
            channel_data.append(data)
            collect_channel_playlist(response['items'][i]['id'])
        my_mdb.channel.insert_many(channel_data)
        return channel_data
    except:
        st.error('Error from collect_channel_details!!!')

# FUNCTION TO COLLECT CHANNEL PLAY/VIDEOS LIST
def collect_channel_playlist(channel_id):
    response = youtube.channels().list(id=channel_id, part='contentDetails').execute()
    playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    playlist_details = []
    try:
        for i in response['items']:
            #playlist_id = i['id']
            playlist_items = []
            playlistitem_details =youtube.playlistItems().list(part="snippet,contentDetails",maxResults=50,playlistId=playlist_id).execute()       
            for j in playlistitem_details['items']:
                #st.success('SIX!!!')
                #st.text(j)
                playlist_items.append({'channelId': j['snippet']['channelId'],
                             #'channelName': j['snippet']['channelTitle'],
                              'playlistName': j['snippet']['title'],
                             #'playlistId': j['snippet']['playlistId']
                             'playlistId':j['id'],
                             #'Playlist_video_count': j['contentDetails']['itemCount']
                             'videoId':j['contentDetails']['videoId']
                             })
                collect_video_details(j['contentDetails']['videoId'])
            #playlist_details.append({
            #    'playlistId': i['id'],
            #   'channelId': i['snippet']['channelId'],
            #    'playlistName': i['snippet']['title'],
            #    'Playlist_video_count': i['contentDetails']['itemCount']
            #    #'playlistitem_details': playlist_items
            #})
            #my_mdb.playlist.insert_many(playlist_details)
            result_playlistitem_details=my_mdb.playlistitems.insert_many(playlist_items)
            return result_playlistitem_details.inserted_ids
    except:
        st.error('Error from collect_channel_playlist !!!')

# To Convert Duration(PT1H5M32S) value to H:mi:ss
def time_duration(apiDuration):
        outputTimedelta = pd.Timedelta(apiDuration)
        strduration = str(outputTimedelta).split()[-1]
        return strduration

# FUNCTION TO COLLECT VIDEOS DETAILS
def collect_video_details(video_id):
    try:
        video_items = []
        video_details = youtube.videos().list(part="snippet,contentDetails,statistics",maxResults=50,id=video_id).execute()  
        for each_item in video_details['items']:
            #st.success('EIGHT ONE!!!')
            #st.text(video_details)
            try:
                video_item_details = dict({
                        'videoId': each_item['id'],
                        'videoPublishedAt': each_item['snippet']['publishedAt'],
                        'channelId': each_item['snippet']['channelId'],
                        'videoName': each_item['snippet']['title'],
                        'videoDescription': each_item['snippet']['description'],
                        'thumbnailURL': each_item['snippet']['thumbnails']['default']['url'],
                        'channelName': each_item['snippet']['channelTitle'],
                        'videoDuration': time_duration(each_item['contentDetails']['duration']),
                        'viewCount': each_item['statistics']['viewCount'],
                        'likeCount': each_item['statistics']['likeCount'],
                        #Note: The statistics.dislikeCount property was made private as of December 13, 2021. 
                        #This means that the property is included in an API response only if the API request was authenticated by the video owner. 
                        #'dislikeCount': each_item['statistics']['dislikeCount'],
                        'dislikeCount': -1,
                        'favoriteCount': each_item['statistics']['favoriteCount'],
                        'commentCount': each_item['statistics']['commentCount']
                        #'commentDetails': collect_video_comment_details(each_item['id'])
                        })
            except:
                video_item_details = dict({
                        'videoId': each_item['id'],
                        'videoPublishedAt': each_item['snippet']['publishedAt'],
                        'channelId': each_item['snippet']['channelId'],
                        'videoName': each_item['snippet']['title'],
                        'videoDescription': each_item['snippet']['description'],
                        'thumbnailURL': each_item['snippet']['thumbnails']['default']['url'],
                        'channelName': each_item['snippet']['channelTitle'],
                        'videoDuration': time_duration(each_item['contentDetails']['duration']),
                        'viewCount': each_item['statistics']['viewCount'],
                        'likeCount': -1,
                        #Note: The statistics.dislikeCount property was made private as of December 13, 2021. 
                        #This means that the property is included in an API response only if the API request was authenticated by the video owner. 
                        #'dislikeCount': each_item['statistics']['dislikeCount'],
                        'dislikeCount': -1,
                        'favoriteCount': each_item['statistics']['favoriteCount'],
                        'commentCount': -1
                        #'commentDetails': collect_video_comment_details(each_item['id'])
                        })
            video_items.append(video_item_details)
            collect_video_comment_details(each_item['id'])
        result_video_item_details =my_mdb.video.insert_many(video_items)
    except:
        st.error('Error from collect_channel_playlist !!!')

def collect_video_comment_details(video_id):
    try:
        comment_details = youtube.commentThreads().list(part="snippet",maxResults=50,videoId=video_id).execute()
        comments_items = []
        #st.text(comment_details)
        comments = comment_details['items']
        if(len(comments) >0):
            for i in comment_details['items']:
                #st.success('EIGHT ONE1!!!')
                #st.text(i)
                comments_items.append({
                    'commentId': i['id'],
                    'videoId': i['snippet']['topLevelComment']['snippet']['videoId'],
                    'textDisplay': i['snippet']['topLevelComment']['snippet']['textDisplay'],
                    'authorDisplayName': i['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    'publishedAt': i['snippet']['topLevelComment']['snippet']['publishedAt']
                })
            #st.success('EIGHT TWO2!!!')
            my_mdb.comments.insert_many(comments_items)
    except:
        st.error('Error from collect_video_comment_details !!!')

def channel_names():   
    ch_name = []
    channel_db = my_mdb['channel']
    for i in channel_db.find():
        ch_name.append(i['channelName'])
    return ch_name

def mongodb_to_sql_migration():
    try:
        #st.success('mongodb to sql migration Starting...!!!')
        myCursor.execute("drop table if exists comments")
        myCursor.execute("drop table if exists video")
        myCursor.execute("drop table if exists playlistitems")
        myCursor.execute("drop table if exists channel")

        #channel table migration
        channel_db = my_mdb['channel']
        myCursor.execute("create table if not exists channel(channel_id VARCHAR(255) PRIMARY KEY, channel_name VARCHAR(255), channel_description TEXT, country VARCHAR(50), subscribers_count BIGINT, channel_viewcount BIGINT, videos_count INT)")
        channel_SqlQuery = "insert into channel values (%s,%s,%s,%s,%s,%s,%s)"
        #st.text('TEST MONGO')
        #st.text(channel_db.find({},{'_id':0}))
        for i in channel_db.find({},{'_id':0}):
        #for i in channel_db.find({},{'_id':0}).sort({'channelId' : 1}).distinct('channelId'):
            myCursor.execute(channel_SqlQuery,tuple(i.values()))
            mySqldb.commit()
        st.success('mongodb to sql migration Done for Channel table...!!!')
        
        #playlistitems table migration
        playlistitems_db = my_mdb['playlistitems']
        myCursor.execute("create table if not exists playlistitems(channel_id VARCHAR(255), playlist_id VARCHAR(255), playlist_name VARCHAR(255), video_id VARCHAR(255), FOREIGN KEY (channel_id) REFERENCES channel(channel_id))")
        #myCursor.execute("create table if not exists playlistitems(channel_id VARCHAR(255), playlist_id VARCHAR(255), playlist_name VARCHAR(255))")#, FOREIGN KEY (channel_id) REFERENCES channel(channel_id))")
        playlistitems_SqlQuery = "insert into playlistitems values (%s,%s,%s,%s)"
        for i in playlistitems_db.find({},{'_id':0}):
            #v1 = [str(val).replace("'", "''").replace('"', '""') if isinstance(val, str) else val for val in i.values()]
            myCursor.execute(playlistitems_SqlQuery,tuple(i.values()))
            mySqldb.commit()
        st.success('mongodb to sql migration Done for playlistitems table...!!!')

        #video table migration
        video_db = my_mdb['video']
        myCursor.execute("create table if not exists video(video_id VARCHAR(255) PRIMARY KEY, published_date VARCHAR(255), channel_id VARCHAR(255), video_name TEXT, video_description TEXT, thumbnail VARCHAR(255), channel_name VARCHAR(255), duration time, view_count INT,like_count INT, dislike_count INT, favorite_count INT, comment_count INT)")
        video_SqlQuery = "insert into video values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #st.success('video ONE1!!!') 
        for i in video_db.find({},{'_id':0}):
            #st.success('video ONE2!!!')
            #st.text(i)
            #st.text(i.values())
            v1 = [str(val).replace("'", "''").replace('"', '""') if isinstance(val, str) else val for val in i.values()]
            #myCursor.execute(video_SqlQuery,tuple(i.values()))
            myCursor.execute(video_SqlQuery,tuple(v1))
            mySqldb.commit()
        st.success('mongodb to sql migration Done for video table...!!!')

        #comments table migration
        comments_db = my_mdb['comments']
        myCursor.execute("create table if not exists comments(comment_id VARCHAR(255) PRIMARY KEY, video_id VARCHAR(255), comment_text TEXT, comment_author VARCHAR(255),comment_published_date VARCHAR(255), FOREIGN KEY (video_id) REFERENCES video(video_id))")
        comments_SqlQuery = "insert into comments values (%s,%s,%s,%s,%s)"
        for i in comments_db.find({},{'_id':0}):
            v1 = [str(val).replace("'", "''").replace('"', '""') if isinstance(val, str) else val for val in i.values()]
            #myCursor.execute(comments_SqlQuery,tuple(i.values()))
            myCursor.execute(comments_SqlQuery,tuple(v1))
            mySqldb.commit()
        st.success('mongodb to sql migration Done for comments table...!!!')


        #st.balloons()
        return 0
    except:
        #mySqldb.rollback()
        st.error('Error during mongodb_to_sql_migration!!!')
        return -1

#======================================================================================================================================
#Steamlit changes starting
icon = Image.open("C:\\Thiyagu\\EPE\\test\\Youtube_logo.png")
st.set_page_config(page_title= "Youtube Data Harvesting and Warehousing",
                   page_icon= icon,
                   layout= "wide")

pd.set_option('display.max_columns', None)
image0 = Image.open('C:\\Thiyagu\\EPE\\test\\Youtube_logo.png')
#image0 = Image.open('Youtube_logo.png')
st.image(image0, caption='', width=40, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
st.header(':blue[YouTube Data Harvesting and Warehousing]')  
#st.header(':violet[YouTube Data Harvesting and Warehousing]')           
#st.subheader(':blue[==============================================]')
image1 = Image.open('C:\\Thiyagu\\EPE\\test\\guvilogo.png')
#image1 = Image.open('guvilogo.png')
st.sidebar.image(image1, caption=None, width=90, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
st.sidebar.header(':green[Please select the option below:]')
list_options = ['--MIGRATION OPTIONS--', 'Retrieving data and Store data to MongoDB',
                'Migrating data to SQL data warehouse', 'SQL Query Output Needs To Be Displayed', 'Exit']
option = st.sidebar.selectbox('', list_options)
channel_details =''
playlist_details=''
video_details =''
comment_details=''
if option:
    try:
        if option == 'Retrieving data and Store data to MongoDB':
            channel_id = st.text_input("Enter Channel ID:")  # get a input from user
            api_key = st.text_input("Enter Your API Key:")  # get a API key from user
            youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
            submit_c = st.button(':blue[Retrieve Data]')
            if submit_c:
                #st.text('THIYAGU')
                with st.spinner(':blue[YouTube Data Extraction Started! Wait for it...]'):
                    channel_details = collect_channel_details(channel_id)
                    if len(channel_details) <=0:
                        datetime.sleep(5)
                    
                #st.success('Before Display channel table!!!')
                   
                st.write(f'#### Extracted data from :green["{channel_details[0]["channelName"]}"] channel')
                st.table(channel_details)
                st.success('YouTube Data Extraction Completed Successfully!!!')     
                #video_id= collect_channel_playlist(channel_id)
                #video_details = collect_video_details(video_id)           
        elif option == 'Store data to MongoDB':
            #my_mdb.channel.insert_many(channel_details)
            #my_mdb.playlist.insert_many(channel_details)
            #my_mdb.playlistitems.insert_many(channel_details)
            #my_mdb.video.insert_many(channel_details)
            #my_mdb.comment.insert_many(channel_details)  
            #st.text(my_mdb.channel.find({},{'_id':0}))          
            st.warning("Store data to MongoDB")
        elif option == 'Migrating data to SQL data warehouse':
            #st.info("Data Migration Started.....")
            st.subheader(':orange[Data Migration Started.....!!]')
            migration_result= mongodb_to_sql_migration()
            if migration_result == 0:
                st.subheader(':green[Data Migration Successfully Completed!!]')
            else:
                st.error("Data Migration not Completed!!")                
        elif option == 'SQL Query Output Needs To Be Displayed': 
            #st.markdown("*Streamlit* is **really** ***cool***.")
            #st.markdown('''
            #    :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
            #   :gray[pretty] :rainbow[colors].''')

            SQL_question = st.selectbox('***Select Your Question From Dropdown***',
                                        ('--QUESTIONS--',
                                         '1.What are the names of all the videos and their corresponding channels?',
                                         '2.Which channels have the most number of videos, and how many videos do they have?',
                                         '3.What are the top 10 most viewed videos and their respective channels?',
                                         '4.How many comments were made on each video, and what are their corresponding video names?',
                                         '5.Which videos have the highest number of likes, and what are their corresponding channel names?',
                                         '6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
                                         '7.What is the total number of views for each channel, and what are their corresponding channel names?',
                                         '8.What are the names of all the channels that have published videos in the year 2022?',
                                         '9.What is the average duration of all videos in each channel, and what are their corresponding channel names?',
                                         '10.Which videos have the highest number of comments, and what are their corresponding channel names?'),
                                        key='sql_query')  
            if SQL_question == '1.What are the names of all the videos and their corresponding channels?':
                st.write("### :orange[List of Videos & Relevant Channels:]")
                myCursor.execute("select video_name as 'Video Name', channel_name as 'Channel Name' from video order by channel_name")
                df1 = pd.DataFrame(myCursor.fetchall(),columns=myCursor.column_names)
                st.write(df1)
            elif SQL_question == '2.Which channels have the most number of videos, and how many videos do they have?':
                myCursor.execute("select channel_name, videos_count from channel order by videos_count desc")
                st.write("### :orange[List of the channels have the most number of videos:]")
                result2 = myCursor.fetchall()
                df2 = pd.DataFrame(result2, columns=['Channel Name', 'Videos Count']).reset_index(drop=True)
                df2.index += 1
                st.dataframe(df2)
            elif SQL_question == '3.What are the top 10 most viewed videos and their respective channels?':
                myCursor.execute("select video_name as 'Video Name', channel_name as 'Channel Name', view_count as Views FROM video order by views desc limit 10")
                result3 = myCursor.fetchall()
                st.write("### :orange[Top 10 most viewed videos :]")
                df3 = pd.DataFrame(result3, columns=['Video Name', 'Channel Name','Views']).reset_index(drop=True)
                df3.index += 1
                st.dataframe(df3)
            elif SQL_question == '4.How many comments were made on each video, and what are their corresponding video names?':
                myCursor.execute("select video_name as 'Video Name', comment_count as 'Comment Count' from video order by comment_count desc")
                result4 = myCursor.fetchall()
                st.write("### :orange[Videos & Relevant Comment Count Deatils:]")
                df4 = pd.DataFrame(result4, columns=['Video Name', 'Comment Count']).reset_index(drop=True)
                df4.index += 1
                st.dataframe(df4)
            elif SQL_question == '5.Which videos have the highest number of likes, and what are their corresponding channel names?':
                myCursor.execute("select channel_name as 'Channel Name', video_name as 'Video Name',  like_count as 'Like Count' from video order by like_count desc limit 25")
                result5 = myCursor.fetchall()
                st.write("### :orange[Videos & Relevant Like Count Deatils:]")
                df5 = pd.DataFrame(result5, columns=['Channel Name','Video Name', 'Like Count']).reset_index(drop=True)
                df5.index += 1
                st.dataframe(df5)
            elif SQL_question == '6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
                myCursor.execute("select video_name as 'Video Name',  like_count as 'Like Count',  dislike_count as 'Dislike Count' from video order by like_count desc limit 25")
                result6 = myCursor.fetchall()
                st.write("### :orange[Videos & Relevant Like/DisLike Count Deatils:]")
                df6 = pd.DataFrame(result6, columns=['Video Name', 'Like Count', 'Dislike Count']).reset_index(drop=True)
                df6.index += 1
                st.dataframe(df6)
            elif SQL_question == '7.What is the total number of views for each channel, and what are their corresponding channel names?':
                myCursor.execute("select channel_name as 'Channel Name', channel_viewcount as 'Total No. Views' from channel order by channel_viewcount desc limit 25")
                result7 = myCursor.fetchall()
                st.write("### :orange[Channel Name & Total No. Views:]")
                df7 = pd.DataFrame(result7, columns=['Channel Name', 'Total No. Views']).reset_index(drop=True)
                df7.index += 1
                st.dataframe(df7)
            elif SQL_question == '8.What are the names of all the channels that have published videos in the year 2022?':
                myCursor.execute("select channel_name as 'Channel Name', video_name as 'Video Name',  published_date as 'Published Year' from video where YEAR(published_date) = 2023 order by published_date desc")
                result8 = myCursor.fetchall()
                st.write("### :orange[Videos & Relevant Like Count Deatils:]")
                df8 = pd.DataFrame(result8, columns=['Channel Name','Video Name', 'Like Count']).reset_index(drop=True)
                df8.index += 1
                st.dataframe(df8)
            elif SQL_question == '9.What is the average duration of all videos in each channel, and what are their corresponding channel names?':
                myCursor.execute("select channel_name as 'Channel Name',  substring(avg(duration) , 1, 8) as 'Average_Video_Duration' from video  group by channel_name  order by Average_Video_Duration;")
                result9 = myCursor.fetchall()
                st.write("### :orange[Channel Name & Average Duration:]")
                df9 = pd.DataFrame(result9, columns=['Channel Name','Average Duration (sec)']).reset_index(drop=True)
                df9.index += 1
                st.dataframe(df9)
            elif SQL_question == '10.Which videos have the highest number of comments, and what are their corresponding channel names?':
                myCursor.execute("select channel_name as 'Channel Name', video_name as 'Video Name', comment_count as 'Comment Count' from video order by comment_count desc limit 50")
                result10 = myCursor.fetchall()
                st.write("### :orange[List of videos which has highest number of comments:]")
                df10 = pd.DataFrame(result10, columns=['Channel Name','Video Name', 'Comment Count']).reset_index(drop=True)
                df10.index += 1
                st.dataframe(df10)   
                #st.write("Select next question and see the details")
            #else:
                #st.info('Please select valid questions...')
        elif option == 'Exit':         
            st.success('Thank you for your time. Closing the application!!!')
        else:
            st.warning("Please select the option from sidebar")
    except:
        st.error("Please enter the valid Channel ID and API key")
