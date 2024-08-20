1.Install docker on your laptop
2.Make sure you have python.3.9 
3.Install  Java 8 and  set it up 
4. Run docker-compose build up


Note : This project (that  I have named smart-city) is collection information from vehicles from central london to Birmingham , 
the vehicles information , the gps ,camera information,the weather information , the incident
through kafka controlled by zookeeper consumed by apache spark then streamed to aws s3 then it can be processed through AWS
using  aws catalog , through aws Athena or AWs Redshift will be our end journey
which can be visualized with powerbi .

this project is a real time project with apache spark , it's an  IOT extaction , the data here is simulated  as 
I don't have real access data  .

As a bonus  , I have added a simple tweeter ETL  project but I have encoutered with an issue my tweeter developer 
have exhausted the record for that reason I could not proceed with testing 
but the code is working if u have an upgraded tweeter account


Steven Murhula Kahomboshi