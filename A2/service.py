from concurrent import futures
import os
from urllib.parse import urlparse
import computeandstorage_pb2
import computeandstorage_pb2_grpc

import grpc
import boto3
from botocore.exceptions import ClientError

class EC2OperationService(computeandstorage_pb2_grpc.EC2OperationsServicer):

    bucket_name = "test-frances-1117"

    # def __init__(self):

    #     # s3 client
    #     self.s3client = boto3.client('s3')
    #     self.s3client.create_bucket(EC2OperationService.bucket_name)

    def StoreData(self, request, context):

        s3client = boto3.client('s3')
        data = request.data

        with open("data.txt", "w") as f:
            f.write(data)


        try:
            print("upload file")
            s3client.upload_file("data.txt", EC2OperationService.bucket_name, "data.txt")
            url = "https://%s.s3.%s.amazonaws.com/%s" % (EC2OperationService.bucket_name, "us-east-1","data.txt")

            return computeandstorage_pb2.StoreReply(s3uri=url)
        
        except ClientError as e:
            print(e)



    def AppendData(self, request, context):

        try:

            s3client = boto3.client('s3')

            data = request.data

            response = s3client.get_object(Bucket = EC2OperationService.bucket_name, Key = "data.txt")
            current_data = response['Body'].read().decode('utf-8')
            print("Appending data ...")
            updated_data = current_data + data

            # print("downloading file ...")
            # s3client.download_file(EC2OperationService.bucket_name, "data.txt", "data.txt")

            
            # with open("data.txt", "a") as f:
            #     f.write(data)

            # print("upload file")
            s3client.put_object(Bucket = EC2OperationService.bucket_name, Key = "data.txt", Body = updated_data.encode('utf-8'))

            return computeandstorage_pb2.AppendReply()

        except ClientError as e:
            print(e)
    

    def DeleteFile(self, request, context):

        try:

            s3client = boto3.client('s3')
            url = request.s3uri

            parsed_url = urlparse(url)
            file = os.path.basename(parsed_url.path)

            print("Deleting file ...")
            s3client.delete_object(Bucket = EC2OperationService.bucket_name, Key = file)

            return computeandstorage_pb2.DeleteReply()

        except ClientError as e:
            print(e)


def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    computeandstorage_pb2_grpc.add_EC2OperationsServicer_to_server(EC2OperationService(), server)
    print("Start listening on 50051")
    server.add_insecure_port('[::]:50051')
    print("GRPC starting")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    server()