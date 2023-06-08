from concurrent import futures
import logging
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
            logging.info("upload file")
            s3client.upload_file("data.txt", EC2OperationService.bucket_name, "data.txt")
            url = "https://%s.s3.amazonaws.com/%s" % (EC2OperationService.bucket_name, "data.txt")

            return computeandstorage_pb2.StoreReply(s3uri=url)
        
        except ClientError as e:
            logging.error(e)



    def AppendData(self, request, context):

        try:

            s3client = boto3.client('s3')

            data = request.data

            logging.info("downloading file ...")
            s3client.download_file(EC2OperationService.bucket_name, "data.txt", "data.txt")

            logging.info("Appending data ...")
            with open("data.txt", "a") as f:
                f.write(data)

            logging.info("upload file")
            s3client.upload_file("data.txt", EC2OperationService.bucket_name, "data.txt")

            return computeandstorage_pb2.AppendReply()

        except ClientError as e:
            logging.error(e)
    

    def DeleteFile(self, request, context):

        try:

            s3client = boto3.client('s3')
            url = request.s3uri

            parsed_url = urlparse(url)
            file = os.path.basename(parsed_url.path)

            logging.info("Deleting file ...")
            s3client.delete_object(Bucket = EC2OperationService.bucket_name, Key = file)

            return computeandstorage_pb2.DeleteReply()

        except ClientError as e:
            logging.error(e)


def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    computeandstorage_pb2_grpc.add_EC2OperationsServicer_to_server(EC2OperationService(), server)
    logging.info("Start listening on 50051")
    server.add_insecure_port('[::]:50051')
    logging.info("GRPC starting")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    server()