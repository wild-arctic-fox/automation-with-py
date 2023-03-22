import boto3

# Output all ec2s from all regions
regions_client = boto3.client('lightsail')
regs = regions_client.get_regions()
print(regs)

for reg in regs["regions"]:
    client = boto3.client('ec2', region_name=reg["name"])
    ec2s = client.describe_instances()
    print(reg)
    print(ec2s)
    print("\n")
