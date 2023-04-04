import boto3

ec2_client = boto3.client('ec2', region_name='eu-west-1')
snapshots = ec2_client.describe_snapshots(OwnerIds=['self'])


class SnapShots:
    def __init__(self, snap, datetime):
        self.snap = snap
        self.datetime = datetime


my_snaps = []

for snapshot in snapshots['Snapshots']:
    print(snapshot['SnapshotId'])
    print('\n')
    my_snaps.append(SnapShots(snapshot['SnapshotId'], snapshot['StartTime']))

my_snaps_sorted = sorted(my_snaps, key=lambda x: x.datetime)

for obj in my_snaps_sorted:
    print(obj.snap, obj.datetime)

del my_snaps_sorted[-2:]

for my_snap in my_snaps_sorted:
    ec2_client.delete_snapshot(
        SnapshotId=my_snap.snap
    )
