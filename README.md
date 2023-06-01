<h1 style="text-align:center;font-family:'Times New Roman';color:darkblue;font-weight:700;font-size:40px">Spotify etl pipeline using Airflow and EC2</h1>

<hr style="border: 0.001px solid black">

<body>
    <h1>Abstract:</h1>
    <p style ="font-weight:400;font-size:18.5px">This project demonstrates the creation of an ETL pipeline using Apache Airflow and an Ubuntu EC2 instance to extract and transform data from Spotify and upload it to an S3 bucket. Apache Airflow is an open-source platform for developing, scheduling, and monitoring batch-oriented workflows. Its extensible Python framework enables you to build workflows connecting with virtually any technology </p>
    <h2>Key Features:</h2>
    <ul>
        <li style ="font-weight:400;font-size:18.5px"> Setting up an Ubuntu EC2 instance with the necessary security group and IAM role.</li>
        <li style ="font-weight:400;font-size:18.5px">Installing required software such as Python and Apache Airflow on the EC2 instance.</li>
        <li style ="font-weight:400;font-size:18.5px">Writing Python code to create a DAG for the Spotify ETL process</li>
        <li style ="font-weight:400;font-size:18.5px">Extracting and transforming data from Spotify using the Spotipy library.</li>
        <li style ="font-weight:400;font-size:18.5px">Uploading the transformed data to an S3 bucket.</li>
    </ul>
    <p style ="font-weight:400;font-size:18.5px">This pipeline enables efficient and automated data extraction and transformation from Spotify, allowing for easy analysis and insights. The successful implementation of this project showcases the power of using Apache Airflow for ETL processes.</p>
</body>
</html>

---

# The Process Architecture  👇

![Process Architecture](https://github.com/DURGESH99P/Spotify-data-engineering-project/assets/94096617/bc36a15e-e8ca-4fe0-b2f7-41ef1a0ed8e5)


---

# 1️⃣ Create Ubuntu Ec2 instance

![Launching ubuntu instance](https://github.com/DURGESH99P/Spotify-data-engineering-project/assets/94096617/cb77f2d4-a538-4eca-97ca-62dfc68c634b)


---

# 2️⃣ Edit Security group

## ⇨ For demonstration purpose we are allowing All traffic in the inbound of the Security group

![Security groups](https://github.com/DURGESH99P/Spotify-data-engineering-project/assets/94096617/127bd363-7f87-4a65-a5aa-848e146b5b71)


---

# 3️⃣ Create IAM role for Ec2 instane to access bucket

![IAM1](https://github.com/DURGESH99P/Spotify-data-engineering-project/assets/94096617/001ef692-18a6-456f-934b-9d6ec4a7fa11)

![IAM2](https://github.com/DURGESH99P/Spotify-data-engineering-project/assets/94096617/3d83a0b2-a1af-4e03-93d1-5728cb0b03c9)



---

# 4️⃣ Attach IAM Role to Ec2 instance

![add_s3_role](https://github.com/DURGESH99P/Spotify-data-engineering-project/assets/94096617/0e095fe3-1439-4a0b-8ff6-47e4780f288a)


---

# 5️⃣Create S3 Bucket to store data from the Spotify

![Create s3 bucket](https://github.com/DURGESH99P/Spotify-data-engineering-project/assets/94096617/fbd8b81e-254e-4721-8e5b-9a4fb3c99cd8)


---

## 6️⃣ Connect to EC2 Instance using Putty

### • Put your instances public ip into the session.

![connecting ec2 instance using putty1](https://github.com/DURGESH99P/Spotify-data-engineering-project/assets/94096617/c27f8bfd-474e-4f7c-9fbf-8dd38e61622a)


### • Choose key used while creating instance from your local system and click open you will be logged to your instance.

![connecting ec2 instance using putty2](https://github.com/DURGESH99P/Spotify-data-engineering-project/assets/94096617/b34e1ba2-32f0-4cb8-ab10-15bd128ba1f1)


---


<h2>✒️ Required content in the EC2 instance :</h2>
    <ul>
        <li style ="font-weight:400;font-size:18.5px"><strong>Python</strong></li>        
        <li style ="font-weight:400;font-size:18.5px"><strong>Apache Airflow</strong></li>

---

<h2> ⏸️ Run following commands in sequence to download the requirements</h2>
    <ul>
        <li style ="font-weight:400;font-size:18.5px"><strong>sudo apt-get update</strong> (will update the ubuntu Ec2 instance)</li>        
        <li style ="font-weight:400;font-size:18.5px"><strong>sudo apt install python3-pip</strong> (will download python3)</li>    
        <li style ="font-weight:400;font-size:18.5px"><strong>sudo pip install apache-airflow</strong> (will download the apache airflow using pip installer)</li>        
        <li style ="font-weight:400;font-size:18.5px"><strong>sudo pip install pandas</strong> (will download python pandas library)</li>
        <li style ="font-weight:400;font-size:18.5px"><strong>sudo pip install s3fs</strong> (will download the pyhton s3fs library)</li>
        <li style ="font-weight:400;font-size:18.5px"><strong>sudo pip install spotipy</strong> (will download the pyhton spotipy library used to access the spotify api)</li>






---

# 7️⃣ Tasks to perform to create dag

## ⇨ Run following commands in sequence.


### 1. cd airflow (you will enter into directory airflow )

<h3>2. sudo vi airflow.cfg (To edit the airflow.cfg file)</h3>
    <ul>
        <li style ="font-weight:400;font-size:18.5px"><strong>in the file change the dags_folder object content from "/home/ubuntu/airflow/dags" to "/home/ubuntu/airflow/spotify_dag"</strong></li>


![updated_changing dags in the dag_folder to spotify_dag](https://github.com/DURGESH99P/Spotify-data-engineering-project/assets/94096617/cad5cf56-27ce-417b-b743-9a03ab4ce38b)


### 3. sudo mkdir spotify_dag (will create directory named spotify_dag)

### 4. cd spotify_dag (you will enter into directory spotify_dag)

### 5. sudo vi spotify_etl.py (write python code to extract & transform data using spotify api & upload the datasets to S3 buckets)


```python
import spotipy
import pandas as pd 
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime
import s3fs 

def run_spotify_etl():

    client_id = "b8db1f5e394149a69d57283ea2e75761"
    client_secret = "93425fac35e94d59b6a90f6714443668"
# Provide details for authentication to extract data from spotify
    client_credentials_mgr = SpotifyClientCredentials(client_id=client_id,
                                                      client_secret=client_secret)
    

    # Create an object to provides authorization to access data to extract
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_mgr)

    playlist_link = "https://open.spotify.com/playlist/7oFbQJn36KPaMHEwgT1XF4"
    playlist_URI = playlist_link.split('/')[-1]

    # To extract all the info related to tracks
    data = sp.playlist_tracks(playlist_URI)

    album_list = []
    for row in data['items']:
        album_id = row['track']['album']['id']
        album_name = row['track']['album']['name']
        album_release_date = row['track']['album']['release_date']
        album_total_tracks = row['track']['album']['total_tracks']
        album_url = row['track']['album']['external_urls']['spotify']
        
        album_element = {'album_id':album_id,'name':album_name,'release_date':album_release_date,
                        'total_tracks':album_total_tracks,'url':album_url}
        album_list.append(album_element)
    album_df = pd.DataFrame.from_dict(album_list)

    artist_list = []
    for row in data['items']:
        for key,value in row.items():
            if key == 'track':
                for artist in value['artists']:
                    artist_dict = {'artist_id':artist['id'],'artist_name':artist['name'],'externam_url':artist['external_urls']['spotify']}
                    artist_list.append(artist_dict)
    artist_df = pd.DataFrame.from_dict(artist_list)
    
    song_list = []
    for row in data['items']:
        song_id = row['track']['id']
        song_name = row['track']['name']
        song_duration = row['track']['duration_ms']
        song_url = row['track']['external_urls']['spotify']
        song_popularity = row['track']['popularity']
        song_added = row['added_at']
        album_id = row['track']['album']['id']
        artist_id = row['track']['album']['artists'][0]['id']
        song_dict = {'song_id':song_id,'song_name':song_name,'duration_ms':song_duration,'url':song_url,
                    'popularity':song_popularity,'song_added':song_added,'album_id':album_id,'artist_id':artist_id}
        song_list.append(song_dict)
    song_df = pd.DataFrame.from_dict(song_list)


    album_df = album_df.drop_duplicates(subset='album_id')
    artist_df = artist_df.drop_duplicates(subset='artist_id')
    song_df = song_df.drop_duplicates(subset='song_id')

    album_df.to_csv("s3://spotifydatabucket/album.csv")
    artist_df.to_csv("s3://spotifydatabucket/artist_df.csv")
    song_df.to_csv("s3://spotifydatabucket/song_df.csv")
```

### 6. sudo vi spotify_dag.py (write python code to create dag for the spotify etl process)


```python
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from spotify_etl import run_spotify_etl

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 11, 8),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'spotify_dag',
    default_args=default_args,
    description='Our first DAG with ETL process!',
    schedule_interval=timedelta(days=1),
)

run_etl = PythonOperator(
    task_id='complete_spotify_etl',
    python_callable=run_spotify_etl,
    dag=dag, 
)

run_etl
```

---

# 8️⃣ Starting the Airflow server 

<h2>⏸️ Run the following command to start the Airflow server</h2>
    <ul>
        <li style ="font-weight:400;font-size:18.5px"><strong>airflow standlone</strong> (will start the Airflow server)</li>

### ⇨ After successful run you will see as in the below image 👇

![airflow standalone](https://github.com/DURGESH99P/Spotify-data-engineering-project/assets/94096617/1e0cd8e0-07a7-4c76-ab1c-bcccc3566f0c)


### • You will get Airflow login credentials along with it

![airflow running](https://github.com/DURGESH99P/Spotify-data-engineering-project/assets/94096617/9dee45ad-a318-4647-b751-64c5fd01507d)


---

# 9️⃣ Copy DNS address of the Ec2 instance and add ":8080" at end of it as our Airflow is running on port 8080

![dns](https://github.com/DURGESH99P/Spotify-data-engineering-project/assets/94096617/a0d91d1c-502e-452e-ba5a-ea2c3e3b0d19)


---

### ⇨ You will see as in the below image 👇, now login to the airflow using the credentials obtained

![airflow login page](https://github.com/DURGESH99P/Spotify-data-engineering-project/assets/94096617/ac80826d-1b32-4631-8495-34123e069aea)

---

### ⇨ After Logged in you will find the spotify_dag which you added to the Dags as shown in below image 👇

![new Spotifydag  appered in airflow](https://github.com/DURGESH99P/Spotify-data-engineering-project/assets/94096617/18308c4e-9845-49ad-b26e-261279e79f80)


### ⇨ After Opening the dag you can see code you created for the etl process within the dag as shown in image below 👇

![spotify_dag file open](https://github.com/DURGESH99P/Spotify-data-engineering-project/assets/94096617/04f0abe8-12d4-4768-993f-e55ea1b9c5e8)


### ⇨ Run the Dag using Trigger DAG 👇

![Run Trigger dag](https://github.com/DURGESH99P/Spotify-data-engineering-project/assets/94096617/1b3fc063-712c-4106-8c95-bb3e61eaf462)


---

# ⇨ After successful run you will see the extracted & transformed data loaded to the S3 bucket

![you will see the etl run successful,as it has added the data to s3 bucket](https://github.com/DURGESH99P/Spotify-data-engineering-project/assets/94096617/a474fd3c-7dab-47ca-9af5-4b3858b09bed)


# 
