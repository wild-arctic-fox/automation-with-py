import boto3
import schedule
import time

ec2_client = boto3.client('ec2', region_name='eu-central-1')
ec2_resource = boto3.resource('ec2', region_name='eu-central-1')


def check_instance_status():
    reservations = ec2_client.describe_instances()
    for reservation in reservations["Reservations"]:
        instances = reservation['Instances']
        for instance in instances:
            print(instance['InstanceId'], instance['State'])

    statuses = ec2_client.describe_instance_status()
    for status in statuses["InstanceStatuses"]:
        print(status['InstanceId'], status['InstanceStatus'], status['SystemStatus'])


schedule.every(10).seconds.do(check_instance_status)

while True:
    schedule.run_pending()
    time.sleep(1)
