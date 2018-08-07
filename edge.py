'''
@filename: edge.py
@author: Karthikeyan Vaideswaran, Aditya Joshi, Sachin Saligram
@desciption: This script runs in the edge server when invoked by the client application (client.py) and ensures a return of the latest version 
				of the requested file.
'''

# Import libraries
import os, sys, subprocess, pipes, logging, paramiko
from kazoo.client import KazooClient


# Function to return the path to a file if it exists
def path_name(filename):
	for root, dirs, files in os.walk('<localhost data directory>'):
		print "searching", root
		if filename in files:
			path =  os.path.join(root, filename)
			return path


# Function to pull the latest version of the requested file from a core server (chosen via round robin) via rsync.
def read(filename, host, user, address, loc):
	os.system("rsync -azvv --delete --include="+filename+ " \'--exclude=*\' -e \"ssh -o \'StrictHostKeyChecking no\' -i <core-filename.pem>\" " + /
										user + "@" + host + ":<remote data directory> <localhost data directory>")
	path = path_name(filename)
	os.system("scp -o \'StrictHostKeyChecking no\' -i <client-filename.pem> " +'%s ' % path + ' %s' % user + "@" + '%s' % address + ':' + '%s' % loc)


# Function to delete a file in both edge and core servers. This employs lazy delete. The current edge server deletes a file (if it exists) 
# from its directory and deletes the file a the core server (deletion is replicated across remaining core servers). But the file on other 
# edge servers is deleted only when a client requests the file via them. Hence, lazy delete.
def delete(filename, host, user, address, loc):
	path = path_name(filename)
		if path != '' and path != None:
			os.system("rm -f "+ path)
			os.system("rsync -rv --delete --include=\""+filename+ "\" \'--exclude=*\' -e \"ssh -o \'StrictHostKeyChecking no\' -i <core-filename.pem>\" <localhost data directory> " + /
										user + "@" + host + ":<remote data directory>")


# Function to write the latest version of a file to a core server (chosen via round robin) via rsync.
def write(filename, host, user, address, loc):
	os.system("scp -o \'StrictHostKeyChecking no\' -i <client-filename.pem> " + user + "@" + address+ ":"  + loc + "/" + filename + " <localhost data directory>")
	os.system("rsync -azvv -e  \"ssh -o \'StrictHostKeyChecking no\' -i <core-filename.pem>\" <localhost data directory>" /
										+ filename + " " + user + "@" + host + ":<remote data directory>")


# Main function, excution starts here.
if __name__ == '__main__':
	path = ''
	filename, operation, return_address, location, username, password = /
						sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
	
	# List of core/zookeeper servers
	hosts = '<list of core/zookeeper servers>'
	
	# Start kazoo client to connect to zookeeper
	zk = KazooClient(hosts=hosts)                                                   
	zk.start()
	
	# Based on round robin, choose the core server to perform the action in and save the next server to be chosen.
	data, stat = zk.get('/server_val')
	val = int(data)
	server_name = username+"@"+hosts[val]
	zk.set('/core/server', server_name)
	new_val = str((val+1)%3)
	zk.set('/server_val',new_val)
	
	# If operation to be done is a 'read', call the read function
	if operation == "read":
		path = read(filename, hosts[val], username, return_address, location)
	
	# If the operation to be done is a 'delete', call the delete function
	elif operation == "delete":
		delete(filename, hosts[val], username, return_address, location)

	# If the operation to be done is a 'write' or 'update', call the write function
	elif operation == "write" or operation == 'update':
		write(filename, hosts[val], username, return_address, location)


