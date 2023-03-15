# import boto3
# import uuid
#
#
#
# def create_bucket_name(bucket_prefix):
#     return ''.join([bucket_prefix,str(uuid.uuid4())])
#
#
# def create_bucket(bucket_prefix,s3_connection):
#     session=boto3.session.Session()
#     current_region=session.region_name
#     if current_region=='us-east-1':
#         bucket_name=create_bucket_name(bucket_prefix)
#         bucket_response=s3_connection.create_bucket(
#         Bucket=bucket_name)
#     else:
#         bucket_name = create_bucket_name(bucket_prefix)
#         bucket_response = s3_connection.create_bucket(
#             Bucket=bucket_name,
#             CreateBucketConfiguration={
#                 'LocationConstraint': current_region
#
#             }
#         )
#
#
#
#     print(bucket_name,current_region)
#     return bucket_name,bucket_response
#
# s3_resource=boto3.resource('s3')
# a,b=create_bucket("test",s3_resource)
# print(a)
# print(b)
