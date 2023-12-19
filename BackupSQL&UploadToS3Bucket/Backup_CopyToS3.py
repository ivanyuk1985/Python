import subprocess
import datetime as d
import boto3
import os

server = 'SASHAPC\SQLEXPRESS'
databases = ['DB1', 'DB2', 'DB3', 'DB4', 'DB5']
username = 'test'
password = 'Gfhjkm+1'
backup_dir = r'C:\Temp'
s3_bucket_name = 'ivanyuk1985itstep'
aws_region = "eu-north-1"
#os.environ['AWS_ACCESS_KEY_ID'] = 'key'
#os.environ['AWS_SECRET_ACCESS_KEY'] = 'key'


s3_client = boto3.client("s3", region_name=aws_region)

time = d.datetime.now()
time_str = time.strftime("%Y-%m-%d-%H")
print(time_str)

for database in databases:
    backup_file = f"{backup_dir}\\{database}_{time_str}.bak"
    
    # Construct the sqlcmd command
    command = [
        'sqlcmd',
        '-S', server,
        '-U', username,
        '-P', password,
        '-d', database,
        '-Q', f'BACKUP DATABASE {database} TO DISK = \'{backup_file}\''
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Backup for {database} completed successfully.")

        # Upload the backup file to S3
        #s3_key = f"{database}/{database}_{time_str}.bak"
        s3_key = f"{database}_{time_str}.bak"
        s3_client.upload_file(backup_file, s3_bucket_name, s3_key)
        print(f"Backup file uploaded to S3: {s3_key}")

    except subprocess.CalledProcessError as e:
        print(f"Error for {database}: {e}")
    except Exception as e:
        print(f"Error uploading to S3 for {database}: {e}")
