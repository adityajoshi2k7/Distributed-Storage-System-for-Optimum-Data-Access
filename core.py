'''
@filename: core.py
@author: Sachin Saligram
@desciption: This script runs in background in each core server and ensures replication using rsync and md5 hash.
'''

# Import libraries
import os, logging, kazoo, time
from kazoo.client import KazooClient
from checksumdir import dirhash


# Start kazoo client to connect to zookeeper
zk = KazooClient(hosts= '<list of zookeeper servers>')
zk.start()


# Begin loop to continuously check for changes and perform replication
while(1):

	try:
		directory = '<source data directory>'							# directory to read and write data
		md5hash = dirhash(directory, 'md5')								# compute hash of the directory

		if zk.ensure_path("/core"):										
			data, stat = zk.get("/core/data")							# extract hash data from zookeeper node
			server, stat = zk.get("/core/server")						# extract server data from zookeeper node

		if data != md5hash:
			if server == "<localhost>":
				zk.set("/core/data", md5hash)							# set new md5 hash
			else:														# rsync from server with updated data
				os.system("rsync -azvv --delete -e \"ssh -o \'StrictHostKeyChecking no\' -i <core-filename.pem>\" --exclude=\'.*\' "+ /
					server + ":<source data directory> <destination data directory>")

	except:
		print "error"
		continue
