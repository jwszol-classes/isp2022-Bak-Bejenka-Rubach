## WORKFLOW:
OpenSky -> AWS Lambda -> Amazon DynamoDB -> AWS Lambda -> Amazon S3 -> Mapbox

## STAGES:
1. Request data from OpenSky with use of Lambda, select the ones that meet the requirements and store them in DynamoDB.
2. Request data stored in DynamoDB and send them to S3 bucket to share them as a static website.
3. Copy data from URL of shared website and visualise them with use of Mapbox.
4. Repeat every minute.

## Used technologies:
- Python - First Lambda function and data visualisation
- Node.js - Second Lambda function
- AWS services:
  - AWS Lambda - Data Processing (downloading data, uploading them to DB and refreshing the json file content)
  - Amazon DynamoDB - Data storage in a Table
  - Amazon S3 - Hosting of a static website containing parameters of flights that meet the requirements (we are looking for flights above Poland) in form of json file
- External resources:
  - OpenSky - source of flights data
  - Mapbox -  tool improving data visualisation 

## Program description:
First lambda function is triggered every minute with use of EventBridge (CloudWatch Events), collects data from OpenSky API and stores them in DynamoDB table. Then second lambda function is triggerd by updates in DynamoDB table. It's reading data from the database and saving in S3 bucket in form of json file. The bucket is set to be publicly accessible and its content is available under given URL.</br>
The next part of the project is visualisation of the data. The program is reading json file from the URL and with use of Mapbox and planes coordinates displays their current position on the map. Program works with Plotly Express and Dash libraries provided in Python. It refreshes every 60 seconds, checking new data and updating coordinates.
  
## Example of the final effect:
![image](https://user-images.githubusercontent.com/40249412/155287064-26bb79b4-06b1-4bca-a809-7497534a28f2.png)

## Open Sky API
The OpenSky Network is a non-profit community-based receiver network which has been continuously collecting air traffic surveillance data since 2013. To use this API there is no need to create account and it is free. 
In used method called get_states(bbox), bbox is a boundries of coordinates. The function get_states returns information about flights bounded by this coordinates. All the data is stored in list of points. 

