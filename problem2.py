#pip install boto3 
#pip install pillow

import boto3
import os
import tempfile
from PIL import Image
import argparse

parser = argparse.ArgumentParser(description='Move all image files from one S3 bucket to another S3 bucket, but only if the image has no transparent pixels.')

parser.add_argument('--src',help='a file path to an image to detect faces')

parser.add_argument('--dest',default="/output",
                    help='a directory path to save the headshots')

args = parser.parse_args()
# python problem2.py --src "awsbucket-images" --dest "awsbucket-notransparentpixel"

BUCKET_NAME = args.src

try:
# Connect to S3
    s3 = boto3.client('s3')

    #List all buckets
    buckets_resp = s3.list_buckets()
    for bucket in buckets_resp["Buckets"]:
        print(bucket)

    # list the contents of a bucket
    result = s3.list_objects(Bucket=BUCKET_NAME)

    # print the contents of the bucket
    for item in result.get('Contents'):
        print(item)

    # Set the names of the source and destination buckets
    src_bucket = args.src
    dst_bucket = args.dest

    # Set the name of the file to log transparent images
    transparent_log = 'transparent_images.txt'

    # Create an empty list to store transparent images
    transparent_images = []

    # Get a list of all the image files in the source bucket
    result = s3.list_objects(Bucket=src_bucket)
    image_files = [content['Key'] for content in result.get('Contents', [])]

    for image in image_files:
        # Download the image to a temporary file
        try:
            temp_file = tempfile.NamedTemporaryFile()
            s3.download_file(src_bucket, image, temp_file.name)
        except:
            print("The data could not downloaded")
        # Open the image with PIL
        try:
            with Image.open(temp_file.name) as img:
                # Check if the image has a transparent pixel
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    # If it does, add the image name to the list of transparent images
                    transparent_images.append(image)
                else:
                    # If it doesn't, copy the image to the destination bucket
                    s3.upload_file(temp_file.name, dst_bucket, image)
            temp_file.close()
        except:
            print("Image file could not open")
    # Write the list of transparent images to the log file
    with open(transparent_log, 'w') as f:
        for image in transparent_images:
            f.write(image + '\n')

    print('All images are processed successfully')
except:
    print("Amazon Web Service could not get the bucket")