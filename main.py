import boto3
import datetime
import schedule

ec2_client = boto3.client('ec2', region_name='eu-west-1')
volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'tag:Name',
            'Values': ['prod']
        }
    ]
)


def create_volume_snapshot():
    for attachments in volumes['Volumes']:
        for attachment in attachments['Attachments']:
            print(attachment)
            snapshot = ec2_client.create_snapshot(VolumeId=attachment['VolumeId'],
                                                  Description=f'Created at {datetime.datetime.now():%Y-%m-%d}')
            print(snapshot)


schedule.every(1).day.do(create_volume_snapshot)

while True:
    schedule.run_pending()
