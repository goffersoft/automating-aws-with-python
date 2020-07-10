## videobot - s3-lambda-dynamodb integration using the serverless framework

#### Analyze videos posted to an s3 bucket and publish the results to dynamodb

1) Add Videos to a prexisting (configurable) s3 buckt

2) S3 triggeres a lamdba function - start_processing_video
    a) This functions calls AWS Rekognition service to analyze the video for label detection
    b) the lambda function also passes an sns topic to the recoknition service. 

3) After Recoknition Service Analyzes the video, it posts status completion to a SNS topic

4) SNS triggers another lambda function - handle_label_detection
    a) This function gets the label detection results from rekognition service.
    b) writes the label detection data to dynamodb.
    c) configurable Put Threshold which allows for updates to existing Labels.
