import boto3
import logging 
from botocore.exceptions import ClientError

def detect_labels_rekognition(path):
    with open(path, "rb") as f:
        Image_bytes = f.read()
        session = boto3.Session(profile_name='csloginstudent')
        s3_client = session.client("rekognition")
        response = s3_client.detect_labels(
            Image={"Bytes": Image_bytes}, MaxLabels=10, MinConfidence=95
        )
        return response
