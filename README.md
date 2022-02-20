## WORKFLOW:
OpenSky -> AWS Lambda -> Amazon DynamoDB -> AWS Lambda -> Amazon S3 -> Mapbox

## STAGES:
1. Request data from OpenSky with use of Lambda, select the ones that meet the requirements and store them in DynamoDB.
2. Request data stored in DynamoDB and send them to S3 bucket to share them as a static website.
3. Copy data from URL of shared website and visualise them with use of Mapbox.
4. Repeat every 30 seconds.

## Used technologies:
- Python - First Lambda function and data visualisation
- Node.js - Second Lambda function
- AWS services:
  - AWS Lambda - Data Processing <!-- (Downloading data, Uploading to DB and Refreshing the website content) -->
  - Amazon DynamoDB - Data storage <!-- in a Table -->
  - Amazon S3 - Hosting of a static website <!-- containing parameters of flights that meet the requirements (we are looking for flights above Poland) in form of JSON file -->
- External resources:
  - OpenSky - source of flights data
  - Mapbox -  data visualisation 
