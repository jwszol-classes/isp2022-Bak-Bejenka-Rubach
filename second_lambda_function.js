var AWS = require('aws-sdk');

exports.handler = async (event, context, call) => {
    
    let S3 = new AWS.S3({ region: process.env.AWS_REGION });
    
    const db = new AWS.DynamoDB.DocumentClient({region: 'us-east-1'}); 

    const db_params = {
        TableName : 'Flights'
    }

    const data_from_db = await db.scan(db_params).promise()

    const nr_of_elements = data_from_db.Items.length

    var del = 0

    if(nr_of_elements < 9){
        del = -28
    } else if (nr_of_elements < 99) {
        del = -30
    }else if (nr_of_elements < 999) {
        del = -32
    }

    var params = {
        Bucket: 'planes-data',
        Key: 'new_data.json',
        Body: JSON.stringify(data_from_db).slice(9,del),
        ContentType: 'text/plain',
    }
     
    try {
        let s3Response = await S3.upload(params).promise();

        let res = {
            'statusCode': 200,
            'headers': { 'Content-Type': 'application/json' },
            'body': JSON.stringify({

                "s3Path":s3Response.Location
            })
        }
        
        return res; 

    } catch (error){
        
        let fail = {
            'statusCode': 200,
            'headers': { 'Content-Type': 'application/json' },
            'body': JSON.stringify({
                "error":error
            })
        }

        return fail;
    }
};