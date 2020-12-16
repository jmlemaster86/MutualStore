# OSTFinal
## MutualStore
### by Jon LeMaster
### jon.m.lemaster-1@ou.edu

## MutualStore: Goals and focus
* Goal 1: Scalability: MutualStore should work well with a just a few clients or thousands of clients
* Goal 2: Proportional load balancing: MutualStore should distribute the load evenly among clients with respect to each client’s capacity. 
* Goal 3:  Reliable access: MutualStore should be able to serve clients even if multiple nodes are down.
* Primary Focus: Making MutualStore a viable peer-to-peer alternative to cloud storage services

## Distributed systems problems
* Efficient lookup of peers(Chord paper, abstract)
* Uniform distribution of load(Dynamo paper, Section 4.2)
* Failure masking(Distributed Systems textbook pg. 431)

## Efficient Lookup of Peers
Problem: MutualStore being a peer-to-peer system needs a decentralized method of looking up peers that doesn’t require each peer to know all others nor requires a look up time that is linear with respect to the number of peers i.e O(n)
Solution: MutualStore uses the Chord algorithm to efficiently lookup peers, this allows O(log n) look up time and each peer only needs to know about log n peers directly

## Uniform Distribution of Load
Problem: Gaps in the distributed hash table can make a peer responsible for a larger number of keys than other peers, and the distributed hash table does not consider the capacity of any of the peers.
Solution: MutualStore uses virtual nodes, each peer can have many virtual nodes and each virtual node is responsible for one block of local storage.

## Failure Masking
Problem: Peers in this system may be offline at any point, so Mutual store needs a way of recovering data even if some peers are down.
Solution: MutualStore uses a RAID5 like system to create a checksum block, so a single block failure can be recovered from.  

## Testing
* First tested local storage abilities by creating a virtual disk and saving a file to it and retrieving that file and confirming that the file was unchanged
* Second I tested the chord algorithm by first having clients discover eachother, update thier finger tables and print them off so I can verify by hand that they are updating correctly, then I passed a message from each virtual node to others to verify that they are all able to reach eachother.
* Next I tested the ability to store and recover files over the network, by verifying that each block is being routed to the correct node by having it print which node is storing the block, and then verifying that I am able to recover the file by sending a recover block request and rebuilding the file and comparing it to the original.
* Next I tested the ability to recover missing blocks by creating a checksum for a file, removing a block from the file and recreating the block using the checksum and the rest of the file, verified that the recovered block was the same as the original.
* Last I made sure that the encoding of checksums would work over the network by storing a file and its checksum on the network, then I pull the file but force the system to not pull the last block of the file, then verify that it pulls the checksum from the network and is able to restore the last block of the file.

## Source code contents
* disHash.py is all of my code for creating virtual nodes in a distributed hash table, and where the chord algorithm is implemented
* diskUtils.py is where I create the virtual disk, and where I define the methods to save and load blocks locally to each system, block size and block number is defined here as well
* connection.py is where I keep all the GRPC interfacing code, here I create server and client connections and define the behavior of the server. Specifically how and when to forward request.
* mutualStore.proto contains all of the protobuf definitions of the server and messages
* encode.py is where I create checksum blocks for recovery of missing blocks
* mutualStore.py is the main executable file, it forks into a client and server runtime, the client runtime will take a file and breaks it into blocks and sends those blocks to the server runtime of the same system, then the server runtime uses the chord algorithm to determine where to send the block, file retrival and deletion is handled in a similar way here.

