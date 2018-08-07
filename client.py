'''
@filename: connect.py
@author: Karthikeyan Vaideswaran, Aditya Joshi
@desciption: This script runs in on the client side to carry out a read, update, write or delete operation on a specified file.
'''

# Import libraries
import paramiko, os, boto3, botocore, sys, boto.ec2
from time import sleep

# Parameters to access edge servers
key = paramiko.RSAKey.from_private_key_file("<edge-filename.pem>")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
auth = {"aws_access_key_id": "<aws_access_key_id>", "aws_secret_access_key": "<aws_secret_access_key>"}
myip = "<localhost IP>" 

# File with edge server ids (one per line)
r = open("server_list.txt", "r")
flag = 0

# Continuous loop to connect to an edge server and read, update or delete a file. Exit if operation suceeds.
while (1):

    # Read a line and get hostname and instance id
    string = r.readline()
    hostname, instance_id = string.split(' ')

    # If you've checked all servers, go back to the first and check again after 10 counts
    if not hostname:
        r.seek(0)
        sleep(10)
    
    # If instance is running, check number of connections and proceed. Else start instance and proceed.
    else:
        try:
            ec2 = boto.ec2.connect_to_region("<aws-instance-region>", **auth)
            instance = ec2.get_all_instances(instance_ids=[instance_id.strip()])

            # Check if instance is not running. Start instance and wait for initialization.
            if instance[0].instances[0].state == "stopped":
                instance[0].instances[0].start()
                sleep(20)

            # Connet to instance
            client.connect(hostname=hostname.strip(), username="<username>", pkey=key)

            stdin, stdout, stderr = client.exec_command("ps -aux | grep \'scp\|rsync\'")
            stdin, stdout, stderr = client.exec_command("ps -aux | grep \'scp\|rsync\' | wc -l")

            # Find the number of connections
            op = int(stdout.read().strip())

            # Check the number of connections to ensure load balancing
            if op > 2:
                client.close()
            else:
                stdin, stdout,stderr = client.exec_command("python ~/edge.py " + sys.argv[1] + " " + sys.argv[2] + " " + myip)
                flag = 1
                break

        except Exception, error:
            print error

    if flag == 1:
        break
