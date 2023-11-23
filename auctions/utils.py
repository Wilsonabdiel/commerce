import boto3

def upload_image_to_s3(image_file, image_name):
    s3_client = boto3.client('s3', region_name='us-east-1')
    bucket_name = 'my-auction-images'

    image_data = image_file.read()
    s3_client.put_object(Bucket=bucket_name, Key=image_name, Body=image_data)

    return f'https://s3.amazonaws.com/{bucket_name}/{image_name}'