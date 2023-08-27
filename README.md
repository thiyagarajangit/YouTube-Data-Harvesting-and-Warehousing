**YouTube Data Harvesting and Warehousing using SQL, MongoDB and Streamlit**
---------------------------------------------------------------------------
**Problem Statement:-**
----------------------
The problem statement is to create a Streamlit application that allows users to access and analyze data from multiple YouTube channels. The application should have the following features:
1.	  Ability to input a YouTube channel ID and retrieve all the relevant data (Channel name, subscribers, total video count, playlist ID, video ID, likes, dislikes, comments of each video) using Google API.
2.	 Option to store the data in a MongoDB database as a data lake.
3.	 Ability to collect data for up to 10 different YouTube channels and store them in the data lake by clicking a button.
4.	 Option to select a channel name and migrate its data from the data lake to a SQL database as tables.
5.	Ability to search and retrieve data from the SQL database using different search options, including joining tables to get channel details.

**Technology Used:-**
----------------------
1.  **Scripting Language** - ***Python***
2.  **GUI** - ***Streamlit***
3.  **Libraries** - ***googleapiclient, pandas, mysql-connector***
4.  **Database** - ***MongoDB, MySQL***

**Links:-**
---------
1.  Github - https://github.com/thiyagarajangit/YouTube-Data-Harvesting-and-Warehousing
2.  linkedin - https://www.linkedin.com/in/thiyagarajan-ms-a92ab0289/
3.  Project Demo Video - 

**Approach:-**
-------------
1.	Set up a Streamlit app: Streamlit is a great choice for building data visualization and analysis tools quickly and easily. You can use Streamlit to create a simple UI where users can enter a YouTube channel ID, view the channel details, and select channels to migrate to the data warehouse.
2.	Connect to the YouTube API: You'll need to use the YouTube API to retrieve channel and video data. You can use the Google API client library for Python to make requests to the API.
3.	Store data in a MongoDB data lake: Once you retrieve the data from the YouTube API, you can store it in a MongoDB data lake. MongoDB is a great choice for a data lake because it can handle unstructured and semi-structured data easily.
4.	Migrate data to a SQL data warehouse: After you've collected data for multiple channels, you can migrate it to a SQL data warehouse. You can use a SQL database such as MySQL or PostgreSQL for this.
5.	Query the SQL data warehouse: You can use SQL queries to join the tables in the SQL data warehouse and retrieve data for specific channels based on user input. You can use a Python SQL library such as SQLAlchemy to interact with the SQL database.
6.	Display data in the Streamlit app: Finally, you can display the retrieved data in the Streamlit app. You can use Streamlit's data visualization features to create charts and graphs to help users analyze the data.
Overall, this approach involves building a simple UI with Streamlit, retrieving data from the YouTube API, storing it in a MongoDB data lake, migrating it to a SQL data warehouse, querying the data warehouse with SQL, and displaying the data in the Streamlit app.

**Results:-**
-----------
This project aims to develop a user-friendly Streamlit application that utilizes the Google API to extract information on a YouTube channel, stores it in a MongoDB database, migrates it to a SQL data warehouse, and enables users to search for channel details and join tables to view data in the Streamlit app.

**GUI Sample Output:-**
-------------------
![image](https://github.com/thiyagarajangit/YouTube-Data-Harvesting-and-Warehousing/assets/142799337/db55b3d2-239b-4269-85a4-127c2f771e8e)
![image](https://github.com/thiyagarajangit/YouTube-Data-Harvesting-and-Warehousing/assets/142799337/e3626740-e698-4ccd-aca9-4bf55845b850)
![image](https://github.com/thiyagarajangit/YouTube-Data-Harvesting-and-Warehousing/assets/142799337/70534083-afbd-4977-8b83-ca5e99413e86)
![image](https://github.com/thiyagarajangit/YouTube-Data-Harvesting-and-Warehousing/assets/142799337/c1e31635-362a-422d-9a72-0d7a648111ff)
![image](https://github.com/thiyagarajangit/YouTube-Data-Harvesting-and-Warehousing/assets/142799337/9a244fcb-09b2-496a-96cb-bc3feb842fb2)
![image](https://github.com/thiyagarajangit/YouTube-Data-Harvesting-and-Warehousing/assets/142799337/384c7258-0da6-464d-a88e-01ae15cfe385)
![image](https://github.com/thiyagarajangit/YouTube-Data-Harvesting-and-Warehousing/assets/142799337/64499369-08bd-4112-a024-022d379626ef)
![image](https://github.com/thiyagarajangit/YouTube-Data-Harvesting-and-Warehousing/assets/142799337/2261530a-d0d0-4e40-9100-b6a82eef647e)








