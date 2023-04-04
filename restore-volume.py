import boto3
import datetime
import schedule

ec2_client = boto3.client('ec2', region_name='eu-west-1')
ec2_resource = boto3.resource('ec2', region_name='eu-west-1')

instance_id = 'i-0b1d93ce9fcbcd382'

volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'attachment.instance-id',
            'Values': [instance_id]
        }
    ]
)

instance_volume = volumes['Volumes'][0]
print(instance_volume)

snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'],
    Filters=[
        {
            'Name': 'volume-id',
            'Values': [instance_volume['VolumeId']]
        }
    ]
)

print(snapshots)

new_volume = ec2_client.create_volume(
    SnapshotId=snapshots['Snapshots'][0]['SnapshotId'],
    AvailabilityZone='eu-west-1b',
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'prod'
                }
            ]
        }
    ]
)

while True:
    vol = ec2_resource.Volume(new_volume['VolumeId'])
    print(vol.state)
    if vol.state == 'available':
        ec2_resource.Instance(instance_id).attach_volume(
            VolumeId=new_volume['VolumeId'],
            Device='/dev/xvdb'
        )
        break
