import os
import socket
from datetime import datetime
from subprocess import getstatusoutput
import boto3
from botocore.exceptions import ClientError
from realcamera import camerascaning
from realrecord import record


AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')  # 
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY') #
AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET') # detectus

if not (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_S3_BUCKET):
    raise Exception('set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY and AWS_S3_BUCKET environment vars')


def _get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("192.168.35.23", 3389))
    result = s.getsockname()[0]
    s.close()
    return result


AWS_S3_CLIENT = boto3.client('s3')
LOCAL_IP_ADDRESS = _get_ip()
HOSTNAME = os.uname().nodename



def get_metadata():
    result = {
        'local_ip_address': LOCAL_IP_ADDRESS,
        'hostname': HOSTNAME,
        'date_day': datetime.utcnow().strftime('%Y%m%d'),
        'upload_timestamp': str(int(datetime.utcnow().timestamp() * 1000000)),
    }
    return result



def upload_aws(filepath):
    file_basename = os.path.basename(filepath)
    s3_path = f'{file_basename}'
    try:
        AWS_S3_CLIENT.upload_file(filepath, AWS_S3_BUCKET, s3_path,
            ExtraArgs={'Metadata': get_metadata()}) 
    except ClientError as e:
        print(f'> error: {e}')
        return False

    print(f'> uploaded {s3_path}')

    return s3_path


def main():
    while True:
        upload_aws(filepath)

if __name__ == '__main__':
    main()
