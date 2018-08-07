# exploring-replicated-systems
Distributed and Replicated Storage System For Data Access

We had 3 core servers which run Zookeeper in the background. We used 3 edge servers where one was in stop state to show the implementation of load balancing. We used 3 clients
to demonstrate the above-mentioned features along with read, write, update and delete operations.
Here are the test cases that we demonstrated:
1. Write/Update a file: The client writes a file. This file is written to one of the edge servers
which pushes the file to one of the core servers. Subsequently replication occurs among the
core servers.
2. Delete a file: The client deletes a file. This file is deleted from the edge server (if it exists)
and a core server (deletion is replicated). The file is deleted from other edge servers when
a client requests that file from them.
3. Read a file: The client reads a file. The edge server checks if it has the latest version of a
file and serves the clients request.
4. Load Balancing: Client-1 requests a large file from edge-server-1. When client-2 requests
a file, it is directed to edge-server-2 due to load balancing (we have chosen one connection
per edge server).
5. Dynamic Allocation: When client-1 and client-2 requests large files from edge-server-1 and
edge-server-2, client-3’s request is kept on hold till a new server is initiated. Subsequently,
client-3’s request is served.
