# CSC4303 Exam Source

## CMU 15-440/640 Distributed Systems

### Mid Fall 2021

> PDF: <https://www.synergylabs.org/courses/15-440/assignments/Midterm1-Fall2021-solutions.pdf>

1(b) A text messaging application would best be implemented using UDP. (✅/❌ ) 

> False. Text messaging necessitates reliable, in-order service, so TCP should be used.

1(d) A Remote Procedure Call (RPC) enables a computer program to execute a subroutine in its own memory address space. (✅/❌ ) 

> False. RPCs enable subroutine execution in a remote address space.

1(f) DHCP is used to translate hostnames into IP addresses. (✅/❌ )

> False. Domain Name Service (DNS) is used for name-address translation, while DHCP (Dynamic Host Configuration Protocol) is used for dynamically assigning IP addresses to networked end-hosts.

2(b)  Which layer(s) of the network stack do UDP and TCP operate at? If you were implementing an RPC service, what would be the benefit of building it atop UDP and TCP, respectively? Answer in one or two sentences for each protocol.

> UDP and TCP are Layer 4 (Transport) protocols. Building an RPC service atop UDP will impose little communication overhead, and is suitable when the underlying network is already fairly reliable. Building it over TCP allows the system to benefit from the reliability, congestion control, and flow control provided by TCP.

2(c) Process p attempts to set its clock using Cristian’s Time Sync. At $p$’s local time `10:00:13.14 AM`, it sends a request to the time server. At local time `10:00:14.21 AM`, $p$ receives a response from the server indicating that the ‘real’ time is `10:00:13.18 AM`. $p$ estimates the minimum one-way delay to be $0.40s$. Assuming no clock drift for p, what are the earliest and latest possible ‘real’ times at which p receives the response?

> Earliest: 10:00:13.58 AM, Latest: 10:00:13.85 AM

4. The following figure depicts the timeline of multiple events happening across several different processes. The number at each event corresponds to its Lamport clock value.

   <img src="assets/image-20260503173948068.png" alt="image-20260503173948068" style="zoom: 20%;" />

   (a) Based on their Lamport clock values, what is the relationship between events labelled b and c? Which event happened earlier?

   > No relationship, events b and c are parallel (L(b) < L(c) does not imply that b precedes c).

   (b) Ignore the Lamport clock values for this subpart. Han proposes a much simpler algorithm to determine event ordering: each time two processes communicate, the sender attaches a log of all events it has seen so far, along with their corresponding local timestamps. For example, when P3 sends event c to P2, it also sends event a’s timestamp. When P2 receives the message (event e), it can reconstruct a global view of event history across both P2 and P3. Based on these logs, can P2 determine the ordering between events a and b? If so, what is the correct ordering from P2’s perspective up to event e? If not, why not?

   > No, because it is futile to compare timestamps across different processes. Since the machine clocks are not precisely synchronized, it is not meaningful to compare the resulting timestamps either. In this example, event a is recorded in terms of P3’s clock while b is recorded in terms of P2’s. Alternative explanations based on Lamport time will also be accepted.

   (c) As you may have noticed, event h is missing a Lamport clock value. What are the possible values for the Lamport clock of event h? What are their corresponding total-ordered Lamport clock values? Assume that the maximum number of processes is 10, and that process P2 has ID 2.

   > 44 is the only possible Lamport clock value for event h. Therefore, its totally-ordered value is $M ∗ Li(e) + i = 10 ∗ 44 + 2 = 442$.

5. Eunice has decided that Gradescope is too slow, and wants to implement her own autograding system, Dotolab, where students submit their code via RPCs. Since she wants students to be sure that they have submitted, she wants to implement RPCs using at-least-once semantics. Note, however, that students still have a limited number of submissions for their projects!

   (a) Eunice wrote the following code to implement the ‘Submit’ RPC (for submitting code to Dotolab). Why does it violate at-least-once semantics, and how can she fix it? (Please keep your answer brief, and do not write code).

   ```go
   func (client *Client) Submit(data []byte) {
   	msg, _ := json.Marshal(data)
   	client.send(msg) // Send message to Dotolab
   	ackMsg := client.ReadFromServer() // Wait for Ack from Dotolab
   	ack := json.Unmarshal(ackMsg)
   }
   ```

   > Solution: Since send is called just once when the student submits, the message may get dropped along the way, and the server may never receive the submission. In order to fix it, Eunice should send the message in a for loop until some sort of acknowledgement is received from the server.
   >
   > ```go
   > func (client *Client) Submit(data []byte) {
   >  msg, _ := json.Marshal(data)
   > 	for {
   > 		client.send(msg) // Send message to Dotolab
   > 		ackMsg := client.ReadFromServer() // Wait for Ack from Dotolab
   > 		if ackMsg != nil {
   > 			ack := json.Unmarshal(ackMsg)
   > 			break
   > 		}
   > 	}
   > }
   > ```

   (b) Eunice has fixed the code such that student submissions now follow at-least-once semantics. However, students are now complaining that they are running out of submissions because of query duplication. What additional information can Eunice include in her messages to make sure that Dotolab discards duplicate submissions?

   > Solution: Eunice should include a submission ID (sequence number) with each message. If Dotolab receives a message with a submission ID matching a previous value, it should simply discard the duplicate message.

   (c) Eunice decides to augment her RPC implementation by providing exactly-once semantics. She pays extra for a better network, `CMU_SUPER_SECURE`, which guarantees that messages are always delivered in-order and will never be dropped in transit. Is this sufficient to guarantee exactly-once semantics? Why or why not?

   > No. The server could still crash between the time the client sends the message and the time the server would have received it (i.e. while the message is in transit), so she cannot guarantee that the message will be delivered.

### Mid Fall 2020 

> PDF: <https://www.composablesystems.org/15-440/fa2022/assets/midterm1_2020.pdf>

1.6 It's better to use UDP rather than TCP to send game updates in fast-paced multiplayer games where low latency is a high priority.

> True. TCP’s retries and ordering cause latency spikes in case of packet loss.

1.7 Transmission delay is proportional to the packet size, while propagation delay is portional to the length of the link.

> Transmission delay is the time spent sending the packet by the router, while the propagation delay is the time it spends travelling on the link.

2.1 Explain two major differences between standard TCP and UDP. (Remember that P1 was a UDP protocol that added some functionalities of TCP.)

> TCP: reliable, slower delivery, handles error, have ack
>
> UDP: non-reliable delivery, faster delivery, discards erroneous packets, does not have ack

3. Time Synchronization

   3.1 First, John wants to calculate the estimated minimum one way delay of sending a time sync request to the server. Assuming store-and-forward routing as well as the following scenarios listed below, please help John with the calculation (consider only one request message for one way): 
   - The link from John's PC to the router has a bandwidth of 5Mbps, and a latency of 10ms.
   - The link from the router to the server has a bandwidth of 2Mbps, and a latency of 100ms. 
   - The time sync request has a size of 20Kb.
   > 20Kb/5Mbps + 10ms + 20Kb/2Mbps + 100ms = 4ms + 10ms + 10ms + 100ms = 124ms

   3.2 John now decides to use Cristian's Time Sync algorithm to synchronize the clock on his PC with the server. He sends a sync request at `08:06:00.000`. Then, at `08:06:00.400` his PC receives a response from the server, saying that the time is `08:08:10:000`. What time should John set his PC to?

   > 08:08:10.200

   3.3 Based on your answers to the above two sub-questions, what is the accuracy of the time estimate made in 3.2?

   > ±(200 - 124) = ±76ms

   3.4 However, after using Cristian's Time Sync algorithm several days, John realizes that this algorithm may not be very accurate if it the RTT is large. Therefore, John decides to use NTP instead. 

   Consider the following diagram:

   <img src="assets/image-20260503181943994.png" alt="image-20260503181943994" style="zoom:33%;" />

   The four timestamps show when John sends the request, when the request is received at the server, when the server sends the response, and when John receives the response. 

   What is the RTT in this diagram (does NOT include server process time)?

   > 200ms

   Calculate the estimated time offset of NTP

   > -1min 4s

   Besides algorithms dealing with real-world time, John also wants to try logical clocks, which only care about relative order of different events. John thinks that regular Lamport clocks have some drawbacks, so he'd like to choose between total-order Lamport clocks and vector clocks. Help him by clarifying some details about each algorithm. How do total-order Lamport clocks achieve a "total-order"? Explain in 1-2 sentences.

   > Potential ties (possible due to concurrency) are broken using process ID, so that they become totally ordered.

   What shortcoming of Lamport logical clocks do vector clocks overcome?

   > If one Lamport timestamp is less than another, it did not necessarily happen before the other (it may be concurrent). Vector clocks do not have this ambiguity

7. RPC

   7.1 In the test environment for p0partA, we expected your implementation to have an exactly-once semantics because there are no packet drops and kvstore actions always succeed. However, in a real environment, packet drops, action failures, etc. are common. Assuming our clients wait for results indefinitely and don’t retry in case of failures, what are the actual semantics of the implementation? Explain your answer.

   At-most-once. Because the client and the server don't have a failure detection and retry mechanism, each request is executed at most once.

   7.2 In p0partA it is possible to associate duplicate values to the same key. Bob doesn’t like duplicate values and decided to rewrite the implementation for kvstore with the following pseudocode.   

   ```go
   /* a map from string to int array */
   map[string]int[] kvs
   
   void put(string key, int value):
   	for v in kvs[key]:
   		if v == value:
   			return
   	kvs[key].append(value)
   	return
   
   int[] get(string key):
   	return kvs[key]
   
   void delete(string key):
   	kvs.delete(key)
   	return
   ```

   Bob wants to publish this new kvstore to clients using a RPC framework without writing a server by himself. Which RPC semantics should he choose? Why?

   > At-least-once. With the new implementation, all three operations are idempotent because we disallowed duplicates. Putting the same values multiple times will result in the same final state.

   7.3 After publishing his kvstore service, Bob notices that the get(key) function is often slow when it has a large array to return. Bob remembers the pass-by-reference trick he often uses and changes his get() function to return the memory address of the result array:

   ```go
   *int[] get(string key):
   	return &kvs[key]
   ```

   Will his approach work? Why or why not?

   > No, because the client machine doesn’t share the address space with kvstore and can’t access the memory location returned.

### Mid Fall 2019

> PDF: <https://www.synergylabs.org/courses/15-440/assignments/Fall2019-Midterm-I-WithSolutions.pdf>

1(b) Over a wide area network it is better to use TCP to implement Voice-over-IP telephony rather than UDP given the potential for packet losses. (✅/❌ )

> False. UDP is still going to be better for the VoIP app since VoIP is real time and the delays caused with TCP retransmision would make things worse. What’s more, VoIP is loss-tolerant.

2(a) Can you implement an RPC system using UDP connections, instead of TCP? Answer yes/no and explain why or why not in at most two sentences.

> Yes. It doesnt matter what transport layer protocol you choose for the RPC system. You can choose to implement over an unreliable network connection and rely on RPC system to detect and tolerate the failures.

2(b) A developer decides to use RPCs to remotely invoke the function `Sum_LinkedList(ListItem *head)`. What problem might they encounter?

> RPC systems don’t handle pointer structures well. The marshalling system would need to figure out how to follow the linked list structure and include all the needed memory locations.

(f) Nodes A and B wish to time synchronize. The link from A to B takes 40ms, and the link from B to A takes 20ms but these numbers are not known to the computers. They synchronize using Cristian’s algorithm in one round. Node A’s time is 500 and Node B’s time is 632. Node A starts the protocol.

1. At the completion of the protocol what time does Node A believe it is?

   > It takes 40ms for the packet to reach B, so B timestamps it as 632+40 = 672. The response reaches node A with an RTT of 60ms, so node A sets its time to 672+60/2=702.

2. What, if any, error is in this value and why?

   > At the end of the protocol Node B will think it is 692. The error is 10ms. It arose because of the asymmetry in the links.

### Fall 2018

> PDF: <https://www.synergylabs.org/courses/15-440/assignments/Fall2018-Midterm-I-WithSolutions.pdf>

2(a) You are responsible for building the successor to the popular Skype Voice-over-IP protocol that works across the internet (high RTTs). Your boss went to CMU but did not take 441 or 440, and thinks you should use TCP due to its reliable delivery feature. Can you explain to him why this is not a good idea?

> Use UDP (as discussed in class). Reliability is less important than reducing delay and jitter. TCP can cause delays for longer RTT links due to reliable delivery and need for ACKs. (One point for mentioning one of packet loss/UDP, delay and jitter).

2(b) NoSQL systems like Amazon’s Dynamo allows writes to continue to all machines during a network partition. Once reconnected, Dynamo nodes seek to reconcile inconsistent file versions. Which technique would you choose to detect and flag parallel events? Briefly explain why.

> Vector clocks. Only algorithm that can properly preserve causality, so Dynamo would know that two events happened in parallel. Lamport clocks can’t do this, as they create arbitrarily ordered timestamps, which might give two parallel events different timestamps.
>
> Note: Totally Ordered Lamport clocks is incorrect

2(c) Name and briefly describe two differences between the time synchronization algorithm used in NTP and Cristian’s algorithm.

> NTP accounts for server processing time using a different equation. NTP also takes multiple measurements to several time servers in parallel and is organized hierarchically, while Cristian’s algorithm assumes a single time server.

3. You are hired by the augmented reality startup AR2 that needs to perform a complex image processing algorithm. Because mobile phones have little computing power, AR2 ’s algorithm gets unacceptably slow as image sizes increase. Your manager, Jaine, proposes to use RPC to perform the work on a remote, more powerful server. You measure the following numbers, assuming a base image scaling factor of N.

   - The running time of AR2 ’s algorithm is $M (N ) = 3N$ ms on a mobile phone. On the server, its $S(N ) = N/3$ ms. 
   - Marshalling and unmarshalling take $(N/6 + 20)$ ms in total. 
   - The average RTT between a user and the server is 80 ms. 
   - Bandwidth is infinite between the user and the server.

   3(a) For what value of N is Jaine right, i.e., AR2 should be using an RPC instead of a local call?

   > When $3N ≥ 80ms + (N/6 + 20)ms + N/3 = 100ms + N/2$. So, $N ≥ 40$. 

   3(b) With geo-replication, AR2 is able to reduce the average RTT. How will N change? (Give a qualitative answer)

   > It decreases, because the server’s computation becomes as fast as the phone’s for a lower value of N .

   3(c) As AR2 acquires 

   1. more and more powerful servers and 
   2. places them closer to users, 

   you notice that the total RPC time does not improve very much. Explain why, by pointing out the bottleneck, in two sentences or less.

   > The bottleneck is the marshalling time. No matter how much everything else is improved, the marshalling time will keep the RPC time high.

6. BergerNet is a new social network started by the TAs and Professors of 15440 providing almost the same functionality as social networks do today. As a new engineering lead, it is your job to make some crucial design decisions that are either going to make or break the BergerNet. BergerNet uses RPCs. Identify the easiest-to-implement RPC semantic (at-leastonce, at-most-once, exactly-once) for each of the following features. Give a *one sentence* reason for your choice. (1pt for semantic, 1pt for reason only if semantic correct).

   6(a) Transferring money to your friend on BergerNet

   > At-most once. Easiest to implement and can always retry sending on failure.

   6(c) Deleting a friend on BergerNet

   > At-least once. Delete is idempotent. At-most once does not work because it is not the easiest to implement.

### Fall 2016

> PDF: <https://www.synergylabs.org/courses/15-440/assignments/Fall2016-Midterm-II-WithSolutions.pdf>

| PDF page(s) | Problem / subpart ID(s) retained      | CSC4303 overlap                                                             |
| ----------: | ------------------------------------- | --------------------------------------------------------------------------- |
|           2 | Question 1(a), 1(b)                   | MapReduce reducer key-space partitioning; virtualization overcommit         |
|           3 | Question 2(a.A), 2(a.B)               | Consistent hashing and failure/view divergence                              |
|         3-4 | Question 2(b), 2(c.A), 2(c.B), 2(e)   | Virtualization isolation; MapReduce stragglers/master failure; DNS resilience |
|         6-7 | Question 4(a), 4(b), 4(c), 4(d), 4(e) | DNS/CDN hierarchy; Chord lookup and finger-table reasoning                  |

1(a) For a particular Map-Reduce Phase with ‘M’ and ’R’ nodes respectively, each reducer node handles 1/R of the intermediate key-values by default. (✅/❌ )

> true. Each Reducer node handles 1/R of the possible keyspace and fetches them from each of the M Mappers.

1(b) In case of System Virtualization, the hypervisor (or VMM) can only allocate and assign the actual number of physical processor resources it has available at its disposal to individual Virtual Machines (VMs). (✅/❌ )

> false. Virtualization allows you to overcommit resources and provide more virtual resources than actual physical resources, for example by time multiplexing the same set of CPU/processors across multiple VMs.

2(a) Consistent hashing is used in a variety of distributed systems over more traditional hashing algorithms.

   2(a.A) Describe one way that consistent hashing performs better when failures occur (e.g. in DHTs or in CDNs).

   > Less content needs to be moved between nodes.

   2(a.B) Describe one way that consistent hashes perform better when nodes have differing views on the availability of servers.

   > Consistent hashing reduces the spread of requests across nodes when views are different.

2(b) You are working on a MAC laptop and using it to develop and test a new Linux OS/kernel. You are worried about bugs since they will cause the Linux kernel to crash. Explain how the ’Isolation’ property of hosted Virtualization solution like VMWare Workstation running on your MAC can help in this case.

> Fault Isolation: We can run the new Linux kernel in a VM. If this VM kernel contains a bug, and crashes it will not crash the main host (OSX) thereby providing fault isolation and allow development and testing to continue.

2(c) We studied the MapReduce programming paradigm for large scale data analysis on clusters, and compared and contrasted that to the more traditional Bulk Synchronous Programming (BSP) methods.

   2(c.A) Explain what the problem with ‘stragglers’ is when using MapReduce and how is it addressed?

   > Solution: Stragglers mean that some Map/Reduce computations may take much longer than others, delaying the entire phase. Solution is to rerun the tasks on nodes that have finished first and then take the result for that task from whoever finishes first.

   2(c.B) Under the MapReduce programming model, how does one deal with a single master node failure? (Assume there is a single master node).

   > Solution: Master failure (discussed in class and also in the paper assigned for readin). 1. Master writes periodic checkpoints such that a new copy can be started from the last checkpointed state when master fails. 2. If only a single master, that particular MapReduce task is aborted and has to be restarted with a new master.

2(e) The DNS root and GTLD servers often come under attack. Give 2 reasons that we don’t notice when they are under attack.

> Solution: The records from the root and GTLD have long TTLs and are cached widely. The root and GTLD zones are replicated very widely and it is difficult to attack all locations at the same time.


4. As the CMU’s Distributed Systems class graduates ventured into the world, they spread their description of class lectures. As a result, the popularity of video recordings of the lectures skyrocketed (unfortunately, mostly for the jokes rather than the technical content) and now Srini needs your help in managing the storage and delivery of the files. Srini starts by building an Akamai-like CDN to deliver the files for his web site www.srinilectures.com. As a first step, Srini:

   1. registers the domain srini-lectures.com with two name servers ns1.srini-lectures.com and ns2.srini-lectures.com.
   2. sets up two regional, low-level DNS servers - east-ns.srini-lectures.com and westns.srini-lectures.com - for clients on the east and west coast.
   3. sets up two servers to deliver cached content with IP addresses 1.1.1.1 and 2.2.2.2. Srini expects users to get the 1.1.1.1 address for www.srini-lectures.com if they are on the east coast and 2.2.2.2 if they are on the west coast.

   4(a) There are 6 name servers involved in the system: 

   - a.root-servers.net 

   - a.gtld-servers.net 

   - ns1.srini-lectures.com 
   - ns2.srini-lectures.com 
   - east-ns.srini-lectures.com 
   - west-ns.srini-lectures.com

   For each of the following DNS records: 

   1) list *ALL* servers where the DNS record stored (do not list cached locations), 
   2) what will its TTL be (assume that the TTL can only be 1 minute or 1 day) and 
   3) why you chose that TTL (1-2 sentences)

   A. NS record that points to ns1.srini-lectures.com

   > on a.gtld-servers.net with TTL 1 day

   B. NS record that points to east-ns.srini-lectures.com

   > on ns1.srini-lectures.com and ns2.srini-lectures.com with TTL 1 day

    C. A record for www.srini-lectures.com

   > on east-ns.srini-lectures.com and west-ns.srini-lectures.com with TTL 1 min

   4(b) On the first query (i.e. no cached information at the local name server) for www.srini-lectures.com from New York - which of the 6 name servers listed are contacted?

   > a.root-servers.net 
   >
   > a.gtld-servers.net 
   >
   > ns1.srini-lectures.com or ns2.srini-lectures.com 
   >
   > east-ns.srini-lectures.com

   4(c) On a second query, 5 minutes after the previous query, for www.srinilectures.com from New York - which of the 6 name servers listed are contacted?

   > east-ns.srini-lectures.com

   Srini decides to move the content to a Chord DHT. He splits the lectures in 10 second chunks, which results in 65536 ($2^{16}$) files. He uses SHA3-256 (256bit long hash) to generate the identifiers used in his DHT. Finally, he recruits 1024 (210) users to participate in the Chord DHT as storage nodes.

   4(d)  How many hops does it typically take to lookup a single chunk?

   > log2(1024) = 10 hops

   4(e) How many different hosts are typically in the Chord finger table at any node?

   > log2(1024) = 10 hosts

### Mid 2012

> PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/midterm2012-solve.pdf>

1(d) UDP is better than TCP for streaming voice-over-IP data. (✅/❌ )

> True. Losing some audio bits isn’t as bad as dealing with the delays from TCP’s retransmission.

1(e)  UDP is better than TCP for RPCs that return medium-sized (100KB) results. (✅/❌ )

> False. 100KB is too big to fit in a single packet (64KB). The RPC system would just end up re-implementing much of what TCP does to split this data into packets and ensure that it is received reliably and reassembled. This would therefore be a poor idea.

1(f) RPCs provide different semantics from local calls because RPCs introduce a different class of errors. (✅/❌ )

> True. RPCs can suffer from network or server failures, so callers need to deal with those additional failure modes.

3(a)  Debugging Concurrency and Synchronization Bugs

```go
func `ReadHandler(conn *net.UDPConn)` { 
    bytes:= make([]byte, 2000) 
    for { 
        n, _, _:= conn.ReadFromUDP(bytes)
     	go ProcessPacket(bytes[0:n]) 
    }   
} 
```

A. Spin loop **B. Race condition** C. Deadlock 

Correct Explain briefly (1-2 sentences) where the bug is. 

> bytes corresponds to some memory that is reused by ReadFromUDP. Thus, the slice to ProcessPacket could be overwritten while it is being processed.

4(h) LSP could be extended to be robust, with high probability, in the presence of corrupted UDP packets by appending a checksum to each message and dropping any that are received with an incorrect checksum. (✅/❌ )

> True. The resending of messages will ensure that (eventually) a valid packet will be sent.

4(i) If a UDP packet gets delayed by several seconds, then the message it contains could be mistaken for one that occurs much later in the message sequence. (✅/❌ )

> True. Due the the wrapping around of sequence numbers.

6. (14 points) Three computers at CMU (A, B, and C) communicate using a protocol that implements the idea of Lamport clocks (they include their clock time stamp in messages). For reference, if you need a reminder, recall that the three rules of Lamport’s algorithm are:

   1. At process i, increment Li before each event
   2. To send message m at process i, apply rule 1 and then include the current local time in the message, i.e., $send(m, Li)$.
   3. To receive a message $(m, t)$ at process j, set $L_j = max(L_j, t)$ and then apply rule 1 before time-stamping the receive event.

   At the beginning of time, all three computers begin with their logical clock set to zero (0). Later, the following sequence of events occurs:

   - A sends message M1 to B: “hi”.
   - After sending M1, A sends message M2 to C: “hi”
   - After receiving M1, B sends message M3 to C: “A told me hi”
   - After receiving M3 first and then M2, C sends message M4 to A: “B is boring”

   6(a) Indicate the time included with the messages as they are sent at each step.

   ```
   Send (M1, _ )
   Send (M2, _ )
   Send (M3, _ )
   Send (M4, _ )
   ```
   
   > ```
   > Send (M1, 1)
   > Send (M2, 2)
   > Send (M3, 3)
   > Send (M4, 6)
   > ```
   
   6(b) Maintaining all clock states from the previous question, three ADDITIONAL messages are sent:
   
   - After receiving M4, A sends message M5 to B: “C is kind of random!”
   - After receiving M5, B sends message M6 to A: “C is boring”
   - A receives message M6
   
   After all of these messages have been sent and received, what time does each computer think it is?
   
   | A    | 11   |
   | ---- | ---- |
   | B    | 10   |
   | C    | 6    |
   
   > (Remember, receiving and sending are different events!)
   > initially: A=0, B=0, C=0
   > send(M1): A=1
   >send(M2): A=2
   > send(M3): A=2, B=3
   > send(M4): A=2, B=3, C=6
   > send(M5): A=8, B=3, C=6
   > send(M6): A=8, B=10, C=6
   > recv(M6): A=11, B=10, C=6.

   6(c) Is this a relatively or totally ordered system?

   > Solution: This is a relatively ordered system.
   
   6(d) Write out the vector time representation with the following messages as they are sent at each step.
   
   ```
   Send (M1, [ ] )
   Send (M2, [ ] )
   Send (M3, [ ] )
   Send (M4, [ ] )
   ```
   
   > Send (M1, [1 ,0 ,0] )
   > Send (M2, [2 ,0 ,0] )
   > Send (M3, [1 ,2 ,0] )
   > Send (M4, [2 ,2 ,3] )

### Mid 2011

> PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/midterm2011_solve.pdf>

1(b) The checksum portion of an IP packet allows the receiver to both detect and correct a single-bit error in the packet. (✅/❌ )

> False. Checksums can be used to detect errors, but not to correct them.

1(c) TCP’s reliable in-order byte stream abstraction can add unpredictable latency to messages under high packet loss. (✅/❌ )

> True. Retransmission and in-order delivery can delay later bytes behind lost earlier bytes.

1(d) When creating a UDP connection to a server, the client and server will engage in a handshake protocol. (✅/❌ )

> False. There is no setup phase with UDP

1(h) When making a synchronous RPC call, the caller will not return until after the requested operation has been completed, assuming no error is encountered. (✅/❌ )

> True. A synchronous RPC blocks the caller until the remote call completes or an error is reported.

1(i) If the Lamport clock of event e1 is less than the Lamport clock of event e2, then there must be a chain of causal events by which e1 precedes e2. (✅/❌ )

> False. Lamport clocks preserve the happens-before implication only in the forward direction; smaller timestamps do not prove causal ordering.

1(j) Global Positioning System (GPS) satellites use NTP to keep their clocks synchronized. (✅/❌ )

> Solution: GPS satellites have their own atomic clocks. NTP would not provide sufficient accuracy for this application.

6. Three computers at CMU, A, B, and C communicate using a protocol that implements the idea of lamport clocks (they include their clock time stamp in messages). For reference, if you need a reminder, recall that the three rules of Lamport’s algorithm are:

   1. At process i, increment Li before each event
   2. To send message m at process i, apply rule 1 and then include the current local time in the message, i.e., $send(m, Li)$.
   3. To receive a message $(m, t)$ at process j, set $L_j = max(L_j, t)$ and then apply rule 1 before time-stamping the receive event.

   At the beginning of time, all three computers begin with their logical clock set to zero (0). Later, the following sequence of events occurs:

   - A sends message M1 to B: “hi”.
   - After receiving M1, B sends message M2 to C: “A told me hi”
   - After receiving M2, C sends message M3 to A: “B is boring”

   6(a) Indicate the time included with the messages as they are sent at each step.

   ```
   Send (M1, _ )
   Send (M2, _ )
   Send (M3, _ )
   Send (M4, _ )
   ```

   > Send (M1, 1)
   > Send (M2, 3)
   > Send (M3, 5)

   6(b) Maintaining all clock states from the previous question, three ADDITIONAL messages are sent:

   - After receiving M3, A sends message M4 to B: “C is kind of random!”
   - After receiving M4, B sends message M5 to A: “C is boring”
   - A receives message M5

   After all of these messages have been sent and received, what time does each computer think it is?

   >  A=10, B=9, C=5.
   > (Remember, receiving and sending are different events!)

   6(c) Is this a relatively or totally ordered system?

   > This is a relatively ordered system.

   6(d) Reset all clocks to zero. This time:

   - A sends message M1 to B.
   - The user of machine A is talking on the phone with the user of machine B. She tells him “I just sent you a message online. Please send a message to C right now.”
   - B sends message M2 to C.

   Once all of the messages have been sent and received, what times might C’s clock be set to under which circumstance?

   > If B received the message before sending the message to C, then C’s clock would read 4.
   > Otherwise, C’s clock would read 2.

### Mid 2010

> PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/midterm2010_solve.pdf>

| PDF page(s) | Problem / subpart ID(s) retained    | CSC4303 overlap                         |
| ----------: | ----------------------------------- | --------------------------------------- |
|           2 | Question 1                          | RPC vs local procedure-call differences |
|           4 | Question 8                          | Application-level choice of UDP or TCP  |
|       11-13 | Question 11(a), 11(b), 11(c), 11(d) | Lamport/Shamport clock ordering         |

1. RPC tries to make remote procedure calls look the same as local procedure calls. But the illusion isn’t perfect. Circle all of the options that correctly describe differences between a local function call and an RPC: 

   A. RPC calls require an extra parameter to identify the server. 

   B. RPC calls may have higher or variable latency. 

   C. RPC calls are limited to call-by-value. 

   D. RPC calls have different (more) failure modes. E. Local function calls require a malloc of a heap object to represent the return pointer.

   > A,B,D

   8. For which of the following applications would UDP be preferable over TCP, ignoring annoying concerns such as firewalls that might block some protocols? 

   A. Streaming a live video over the internet 

   B. Instant messaging/email

   C. Logging in to your bank website

   D. Voice over IP 

   E. Large file transfers 

   F. Looking up a very small value from a directory service TCP / UDP

   > UDP, TCP, TCP, UDP, TCP, UDP

   11. Suppose each computer in a distributed system keeps an approximate real-time clock $Ri$ in addition to a Lamport-like clock $Li$. 

       A computer’s real-time clock $Ri$ is an always-increasing integer (i.e., for any two reads $r_1$, $r_2$ of $R_i$ such that $r1 →_i r2$, we have r2 > r1), but the real-time clocks at different computers may drift relative to each other (i.e., $R_j − R_i$ is non-constant for j ≠ i). 

   Consider the following modification, Shamport, to Lamport’s partial-ordering algorithm: 

   **Rule 1:** before each event at computer i, set $L_i = min(Li + 1, Ri)$. 

   **Rule 2:** when sending a message m, apply Rule 1 and include the time Li as part of the message. 

   **Rule 3:** when receiving a message $(m, t)$ at computer j, set $L_j = max(Lj, t)$ and then apply Rule 1 before timestamping the message-arrival event. 

   Let the Shamport global time of an event e at computer i be $S(e) = L_i(e)$.

   11(a) In the algorithm above, underline the difference between Shamport and Lamport’s algorithm. (Underline as little as possible).

   > Shamport’s algorithm uses $L_i = min(L_i + 1, R_i )$ in Rule 1 instead of $L_i = L_i + 1$. Otherwise the two algorithms are the same.

   11(b) Let $e, e'$ be two events at computer i such that $e →_i e’$. Prove that $S(e' ) > S(e)$.

   > The key observation is that any new event advances the logical clock. There are a couple common pitfalls to avoid: 
   >
   > (1) e and e’ are not necessarily consecutive events; other intervening events can affect the Shamport clock. 
   >
   > (2) Events at computer i include the local side of send and receive events, so you need to include possible applications of Rule 2 and Rule 3 in your proof. And (3), reading the problem correctly to understand that the logical clocks Li here are not Lamport clocks, and thus you cannot blindly apply the rules for Lamport clocks from class. One proof is: Consider the sequence of all events e . . . e0 at computer i. If S(e0 ) ≤ S(e) then there must exist at least one pair of consecutive events f, f 0 (WLOG f →i f 0 ) such that S(f 0 ) ≤ S(f ); otherwise each new event would advance the logical clock Li , which would yield Li (e0 ) > Li (e0 ) and thus S(e0 ) > S(e). To show S(e0 ) > S(e), therefore, it suffices to show that Li (f 0 ) > Li (f ) for any two consecutive events f →i f 0 . Let (t, r) be the logical and real-time clock times for event f and (t0 , r0 ) be the times for f 0 . We must show that t0 > t for any events f and f 0 . We break this into three cases based on whether f 0 is a normal local event, a send event, or a receive event. (In each of these cases we allow f to be any type of event.) Notice that in every case we have r0 > r because $Ri$ is always-increasing and f →i f 0 . Case 1: f 0 is a normal local event. This causes a single application of Rule 1, yielding t0 = min(t + 1, r0 ). Briefly consider the rule that set the logical clock for f . Because all three rules last-affect the logical clock with an application of Rule 1, we have that t = min(,̇r) and thus that t ≤ r, yielding t < r0 . Because t + 1 > t and r0 > t we therefore have that t0 > t regardless of which term of the min-operation is lesser, yielding that S(f 0 ) > S(f ) as desired if f 0 is a local-only event. Case 2: f 0 is a send event. This causes an application of Rule 2, which affects the logical clock only with an application of Rule 1. Thus, Case 2 reduces directly to Case 1.

   11(c) Draw a time-series diagram in which S(send(m)) > S(receive(m)) for some message m. Explain in 1-2 sentences why this unwanted behavior occurs.

   > This can happen when the receiver’s real-time clock is behind the sender’s. On receive, the node first raises Lj using the message timestamp, but Rule 1 then caps the logical clock at its slower real-time clock, so the receive event can be timestamped earlier than the send.

   11(d) Suppose every one-way message latency is at least x clock ticks by any local clock, and external synchronization guarantees |Ri − Rj| ≤ y. Is there a value of y small enough to guarantee S(send(m)) < S(receive(m)) for any message?

   > Yes. It is enough to have y < x: the minimum propagation delay then exceeds the maximum real-clock skew, so the receiver’s real-time clock is still ahead of the sender’s timestamp when Rule 1 is applied.

### Final 2009

> PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/final2009-solve.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                                                |
| ----------: | -------------------------------- | ------------------------------------------------------------------------------ |
|           2 | Question 1, 2, 3, 4              | DNS scalability; Chord; RPC library responsibilities; content-based P2P naming |
|           3 | Question 6(a), 6(h)              | GFS data path; Lamport happens-before implication                              |
|        8-11 | Question 14                      | MapReduce-style distributed data processing                                    |

1. Which techniques are used in DNS to improve scalability? A. Replication B. Recursive queries C. Caching / Soft-State D. Partitioning of Namespace

   > A, C, D

2. Which of the following are true about the Chord distributed hash table? A. Has O(log(N)) lookup latency B. Directly supports fuzzy or wildcard lookups for content C. Uses content-based naming D. Provides anonymity

   > A, C

3. Which of the following are commonly provided in RPC libraries? A. Application-level failure handling B. Data marshalling/unmarshalling C. Asynchronous function calls D. Exactly-once semantics E. At-most-once semantics

   > B, E

4. Which of the following are advantages of using content-based naming for p2p file transfers? A. The receiver can download a chunk using parallel TCP streams. B. The receiver can route around failed links. C. The receiver can download a chunk of data from any source, not just the original seed. D. The receiver can verify that it received the correct data.

   > C, D

6. Which of the following statements are true? Please circle True or False:

   6(a) In Google File System (GFS), when a client needs to access data, it contacts the master and gets the data from the master. (✅/❌ )

   > False

   6(h) Recall the global “happens-before” relationship (→) that captured the logical notions of time using both the local happens-before relationship at each server and the fact that a message must be sent before it can be received. True or false: For a Lamport logical clock L, if e1 → e2 then L(e1 ) < L(e2 ). (✅/❌ )

   > True

14. Recall the statuses twitter dataset we provided for Project 3, which contained data of the form:

   ```text
   postid <tab> status-message
   ```

   In Twitter, some status-messages are repeats of earlier status messages. These repeated messages are preceded by “RT” followed by the original status message. For example:

   ```text
   142412141      I need puppies but youtube is blocked.
   584923144      Puppies are awesome!
   929483834      RT Puppies are awesome!
   872935923      RT Puppies are awesome!
   423135125      Meow mix meow mix please retwitter
   723917388      RT I need puppies but youtube is blocked.
   629359237      RT Puppies are awesome!
   562983948      RT Meow mix meow mix please retwitter
   729385724      RT Meow mix meow mix please retwitter
   912383444      Taking 15-440 final exam, lolol.
   ```

   In this problem, your goal is to identify the most “retweeted” status messages using the MapReduce style of programming. You must write one or more Map and Reduce functions whose final output contains a sorted list of post ids that have been “retweeted”/repeated, sorted by the number of times they have been retweeted. If run on the above example, the output would be:

   ```text
   1        I need puppies but youtube is blocked.
   2        Meow mix meow mix please retwitter
   3        Puppies are awesome!
   ```

   Only retweeted statuses should appear in the output. The output should be sorted by the number of retweets from fewest to most. You can use any reasonable pseudocode you choose (Java-like or C++-like); we will grade based on the algorithm, not having semicolons correct. You can use two types: Integers and Strings. You can assume the existence of STL-like string functions for your convenience. You can iterate over lists using the for construct as shown below:

   ```text
   for item in list {
      (do something with item)
   }
   ```

   You should use the “emit(key,value)” pseudocode for the output of functions.

   ```text
   // Assume line has been parsed into post id and status already
   Map(int postid, String status) {

   }

   // Fill in the appropriate types in the brackets
   Reduce(<          > key, List<          > values) {

   }
   ```

   Use the page below should you need more Map and Reduce functions. Declare them as above.

   > Solution:
   >
   > ```text
   > Map(int postid, String status) {
   >   if (status.substring(0,2) == "RT") {
   >     emit(v.substring(3), 1);
   >   }
   > }
   >
   > Reduce(String key, List<int> values) {
   >   int sum = 0;
   >   for value in values {
   >      sum += value;
   >   }
   >
   >   if (sum > 0) {
   >     emit(key, sum);
   >   }
   > }
   >
   > Map2(String status, int count) {
   >   emit(count, status);
   > }
   >
   > Reduce2(int count, String status) {
   >   emit(count, status);
   > }
   > ```

### Final 2010

> PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/final2010-solve.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                                                               |
| ----------: | -------------------------------- | --------------------------------------------------------------------------------------------- |
|           2 | Question 1, 2                    | TCP handshake misconception; Internet best effort; DNS TTL/invalidation; GFS/HDFS assumptions |
|         5-6 | Question 4, 5, 6                 | Chord/P2P lookup and design trade-offs                                                        |
|           9 | Question 11, 12                  | Lamport timestamp ordering                                                                    |

1. (22 points) True/False: Circle the one that best applies. Grading is 2 points for every correct answer. That means that at the end of the exam, if you don’t know the right answer, come back here and guess randomly!

   Threads and Processes

   - True, False It is less expensive to create a process than a thread.
   - True, False Switching between threads is faster than switching between processes.
   - True, False In order to switch between user threads, you need to enter the kernel.
   - True, False Threads share a heap and a stack.

   Networking

   - True, False The TCP initial handshake must be completed between the sender and every router on the path to the destination before communication can take place.
   - True, False The Internet service model allows a small (a percent or two) amount of packet loss. (In other words, end-hosts must be able to deal with a small amount of loss)
   - True, False Domain Name Service (DNS) servers remember which clients have cached DNS replies so that the servers can send invalidation messages when name bindings change.

   Distributed Mutual Exclusion

   - True, False Ring-based distributed mutual exclusion is a great solution for a latency-sensitive application running on 10,000 nodes.

   Logging

   - True, False Write-ahead logging is a useful technique for providing persistence for random updates without needing to write to a random location on disk.
   - True, False For correctness, all write-ahead log records must specify how to both undo and redo the operation they describe.

   Tor

   - True, False The onion routing scheme used by Tor is resilient to an attacker that can simultaneously compromise every node in the Tor network.

2. Which of the following design assumptions apply to HDFS/GFS? (Circle all that apply) A. Only amazingly powerful servers can handle the size and complexity of the workload. B. Any use of a centralized server would cause too much of a bottleneck. C. Component failures are expected. D. Files are huge by traditional standards. E. File contents are often updated and overwritten. (✅/❌ )

   > C, D

4. Suppose the above Chord setup: • At what node do you expect to find key 10? • At what node do you expect to find key 9? • On average, how many hops are there when searching for a key? • What route will a search for key 11 take, starting at node 3?

   > Key 10 maps to node 0, and key 9 maps to node 9. Chord lookups take O(log N) hops on average. Starting at node 3 for key 11, the lookup goes 3 → 9 → 0.

5. Suppose you want to build a large distributed system to store cookie recipes. Each cookie is stored using the recipe’s name (“Grandma’s Arsenic Cookie Surprise”). Unlike many P2P systems, in this one, the recipe data is small, so you wanted to store the actual data in the P2P system instead of leaving it on the original nodes. A friend says “Hey, I hear that Chord is very efficient – it doesn’t take many lookups to find the node containing the data.” Explain to your friend why directly throwing this data into a DHT such as chord, with key = recipe name, value = recipe data, is a really bad design decision. Brief - two sentences or so.

   > Chord only supports exact-key lookup well, while recipe users are likely to search by partial names, ingredients, or categories. Hashing recipe names also destroys locality, so related recipes cannot be found together without building a separate index.

6. Tell us what style of P2P system you would use, and what assumptions you think are reasonable for your cookie-storing-system: • Number of nodes • Number of recipes • Number of queries/second • What do queries look like? Style of system AND a brief rationale for this decision:

   > A centralized or replicated index is a better fit than a pure DHT if the recipe corpus is moderate and queries are keyword/category searches rather than exact-key lookups. The recipe data is small enough to replicate or cache, while the index can support richer search over names, ingredients, and tags.

11. What is the value of x? If it cannot be determined, write “unknown”.

    > x = 7. Message m5 is sent by machine 4 with Lamport time 6, and machine 1’s local clock before receiving it is 2, so the receive timestamp is max(2, 6) + 1 = 7.

12. For the following, circle which event happened first. If it cannot be determined, circle “unknown.” • L1 (m1, send) L4 (m5, send) U nknown • L2 (m3, send) L3 (m4, send) U nknown • L3 (m4, send) L3 (m3, recv) U nknown • L2 (m3, send) L4 (m6, send) U nknown • L4 (m6, send) L1 (m7, send) U nknown

    > L1(m1, send); Unknown; L3(m4, send); Unknown; Unknown.

### Final 2011

> PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/final2011-solve.pdf>

| PDF page(s) | Problem / subpart ID(s) retained            | CSC4303 overlap                                                     |
| ----------: | ------------------------------------------- | ------------------------------------------------------------------- |
|         2-3 | Question 1(a), 1(b), 1(c), 1(d)            | DNS hierarchy; DNS caching; CDN via DNS; MapReduce map semantics    |
|       10-11 | Question 6(a), 6(b), 6(c), 6(d), 6(e), 6(f) | Napster, query flooding, supernodes, flooding limits                |
|       12-13 | Question 7(a), 7(b), 7(c), 7(d), 7(e), 7(f) | DHT/Chord ring mapping, finger table, successor, fallback/proximity |
|       15-16 | Question 9(a), 9(b), 9(c), 9(d)             | MapReduce/GFS failure handling and stragglers                       |

1. (8 points) Circle True or False as appropriate. If you don’t know the answer, come back at the end and GUESS; a blank answer is the same as a wrong answer, so guessing can only help.

   1(a) DNS is delegated hierarchically by having the root nodes tell resolvers which servers to query for `.com`, and so on, until the client’s query can be answered. (✅/❌ )

   > True.

   1(b) DNS resolvers use Paxos and invalidation messages to maintain the consistency of cached records. (✅/❌ )

   > False.

   1(c) Some Content Delivery Networks (CDNs) use DNS responses to direct clients to the closest CDN cache. (✅/❌ )

   > True.

   1(d) The Map step of MapReduce provides a way to store and retrieve items according to their keys. (✅/❌ )

   > False.

6. Peer to Peer

   6(a) In a centralized p2p network (such as the old Napster), how many indices must be searched if a client wants to locate a particular file?

   > 1

   6(b) Name one major disadvantage of the centralized p2p system (from a distributed principles point of view)

   > - Single point of failure - Server processes everything - Server must keep track of a potentially very large number of clients - more?

   6(c) Query flooding is an alternative design that solves some of the problems of centralized p2p and eliminates the central server. However, it changes the mechanics of peer interactions significantly. Explain (1 sentence each) how a newly-joining node publishes the files they wish to make available, in... A centralized p2p network:

   > They send their list of files and metadata to the server.
   >
   > A query flooding p2p network:
   >
   > They don’t do anything - queries come to them.

   6(d) One popular improvement upon query flooding is to move to a “supernode” flooding architecture. Using N as the number of nodes in the network and, S as the number of supernodes (S << N ), explain the benefit of moving to this supernode architecture.

   > Queries require now O(S) messages instead of O(N ). In addition, if the nodes used as supernodes are more stable or have higher capacity, can further improve the performance or stability of the network.

   6(e) What is a common mechanism used to limit the propagation of queries in a flooding network?

   > TTL - time to live - scoping. Also known as hop count limits, etc.

   6(f) List one typical criterion for selecting a node to be promoted to a supernode. Explain in one sentence why such a choice would improve network stability.

   > How long a node has been part of the network (time), because how long a node has been around is a good predictor of how long it will be around.

7. Consistent Hashing

   7(a) In a distributed hash table (DHT) using a ring mapping, explain how a key is mapped to a specific node?

   > Keys and nodes map to points in a ring space. A node handles all keys mapped between it and its successor.

   7(b) In the most basic form of DHT systems, nodes simply track their predecessor and successor. Very briefly state what problem this leads to as the network grows larger.

   > Performance problems as nodes forward a key resolution request to larger chains of neighbors.

   7(c) The Chord scheme overcomes this problem by having each node maintain a “finger table”. Given starting node j and destination node k, where k > j, how much is the distance between the two nodes reduced with each hop?

   > It decreases exponentially, or it is cut in half

   7(d) In a Chord structured DHT with N nodes, how many hops would a lookup operation require?

   > log(N )

   7(e) Assume a Chord network in which node q is the successor of node p. During operation, node p discovers that its successor link is no longer consistent because q has updated its predecessor link. What does this change imply must have happened in the network?

   > A new node joined the network ’between’ p and q.

   7(f) An optimization to Chord involves storing several nodes for each entry in the finger table instead of just one. Explain an important benefit this optimization confers in a globally distributed DHT.

   > (1) This allows routing based on proximity, which would reduce slow routes that criss-cross the globe.
   > (2) It provides a fallback in case one of the nodes in the finger table is unreachable.

9. MapReduce has proved an extremely popular framework for distributed computation on large clusters, because it masks many of the painful parts of ganging together thousands of nodes to accomplish a task.

   9(a) In general high-performance computing (HPC), programmed using message passing, what is the technique used to provide fault tolerance? (Very short answer)

   > Checkpoint/restore

   9(b) Identify two important limitations that MapReduce places upon the Map functions so that the framework can hide failures from the programmer.

   > They must be side-effect free, deterministic, and idempotent.

   9(c) What advantage does this give MapReduce over MPI for failure handling and recovery? (There are several—list the one(s) you think is most important)

   > Recovery can be done by only executing the work that was being handled on the failed machine, not the entire cluster. There is no need to take snapshots or to barrier sync the cluster.

   9(d) How does MapReduce handle “straggler” tasks that take longer than all of the others (e.g., perhaps they’re running on a slower machine or one with buggy hardware)?

   > It executes them in duplicate on another machine towards the end of execution. (Not needed for answer: It can do so because of the same properties of the tasks above - namely, that they can be freely re-executed and produce the same result.)


## UW CSE 461 Computer Networks

### Sample Mid 2

> PDF: <https://courses.cs.washington.edu/courses/cse461/23sp/samples/sample-midterm2-key.pdf>

| PDF page(s) | Problem / subpart ID(s) retained     | CSC4303 overlap                                                                               |
| ----------: | ------------------------------------ | --------------------------------------------------------------------------------------------- |
|           2 | Question 1(a), 1(d), 1(e)             | Layering, internetworking, encapsulation                                                      |
|         3-4 | Question 3(a), 3(b), 3(c), 3(d)       | ICMP, NAT, IPv6 motivation, tunneling                                                         |
|           5 | Question 4(a), 4(b), 4(c), 4(d)       | Routing vs forwarding, longest-prefix matching, local/gateway forwarding, routing scalability |
|           6 | Question 5(a), 5(b), 5(c), 5(d), 5(e) | Distance-vector vs link-state routing, convergence, RIP, OSPF/IS-IS                           |

1(a) How are hosts with two different link layers (e.g., WiFi and Ethernet) able to communicate?

> Layering lets the IP layer decapsulate data from one link layer and encapsulate it in another.

1(d) What is the primary approach used to divide network functionality in the Internet?

> Layering.

1(e) Consider a protocol stack composed of WiFi, IP, TCP, and HTTP. Illustrate what the packet on the wire looks like for this stack.

> HTTP is encapsulated by TCP, then by IP, then by WiFi.

3(a) What is ICMP used for?

> Sending back error reports.

3(b) Describe two advantages and two disadvantages of NAT.

> Advantages: NAT counters IPv4 address shortage and can filter some unwanted inbound packets. Disadvantages: outside hosts cannot directly connect to inside hosts without a table entry or explicit forwarding rule, and NAT breaks or complicates peer-to-peer applications and protocols that embed IP addresses in payloads.

3(c) What was the primary motivation for developing IPv6?

> Shortage of IPv4 addresses.

3(d) How can IPv6 traffic be carried over a network that does not support IPv6?

> Tunneling.

4(a) What is the difference between routing and forwarding?

> Routing figures out where packets should go; forwarding sends packets according to the chosen forwarding entry.

4(b) What is longest matching prefix?

> A forwarding strategy where the router uses the longest prefix that matches the packet’s destination IP address.

4(c) A host has IP address 10.10.10.10, prefix 10.10.10.0/24, and gateway 10.10.10.1. How will it forward packets to 10.10.10.11, 10.10.11.10, and 10.11.10.10?

> 10.10.10.11 is sent on the local network. 10.10.11.10 and 10.11.10.10 are sent to the gateway.

4(d) Describe three ideas that help routing in the Internet scale.

> Subnetting, hierarchical routing, and aggregation.

5(a) Describe how distance-vector and link-state routing algorithms differ.

> Distance-vector routing exchanges shortest-path information with neighbors. Link-state routing exchanges topology information. Distance-vector converges more slowly but is computationally simpler.

5(b) Which of the two algorithms converges faster?

> Link-state routing.

5(c) Which of the two algorithms requires more computation?

> Link-state routing.

5(d) Give an example of a routing protocol that uses the distance-vector algorithm.

> RIP.

5(e) Give an example of a routing protocol that uses the link-state algorithm.

> OSPF or IS-IS.

### Mid Review Practice, Section 4

> PDF: <https://courses.cs.washington.edu/courses/cse461/23sp/section/4-midterm-review.pdf>

| PDF page(s) | Problem / subpart ID(s) retained                                 | CSC4303 overlap                                           |
| ----------: | ---------------------------------------------------------------- | --------------------------------------------------------- |
|       12-16 | Practice Problems: Bandwidth Allocation; Practice Problems: AIMD | Max-min fairness and AIMD calculations                    |
|       53-54 | Practice Problems: Link-State Routing                            | Link-state routing convergence and inconsistent LSP views |

Practice Problems: Bandwidth Allocation. Four flows A, B, C, and D share a 10 Mbps link. Demands are A=1 Mbps, B=2 Mbps, C=10 Mbps, and D=infinite. What is the max-min fair allocation?

> Flow A: 1 Mbps. Flow B: 2 Mbps. Flow C: 3.5 Mbps. Flow D: 3.5 Mbps.

Practice Problems: AIMD. A 10 Mbps link is shared by flow A, capped at 3 Mbps, and flow B, with infinite demand. Each RTT increases rate by 1 Mbps if uncongested and halves the rate if congested. Starting from A=2 Mbps and B=20 Mbps, what are the rates after 1, 2, and 3 RTTs?

> After 1 RTT: A = 1 Mbps, B = 10 Mbps. After 2 RTTs: A = 0.5 Mbps, B = 5 Mbps. After 3 RTTs: A = 1.5 Mbps, B = 6 Mbps.

Practice Problems: Link-State Routing. C receives contradictory LSPs: one from A says the A-B link is down, but one from B says the A-B link is up. How could this happen, and what should C do?

> This can happen if one LSP was sent before the A-B link changed and the other was sent after it changed. C should keep flooding and recomputing from the newest LSPs; eventually the old LSP will be superseded and both sides will agree again.

### Winter 2017 Mid

> PDF: <https://courses.cs.washington.edu/courses/cse461/22wi/practice-materials/midterm-2.3.17.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                                |
| ----------: | -------------------------------- | -------------------------------------------------------------- |
|         4-5 | Question 3(a), 3(b)              | Spanning-tree convergence and loop-free bridged topology       |

3(a) For the given topology, fill out each step of the spanning tree algorithm until it reaches steady state. Ties are broken by lowest address.

> Root A wins. The steady-state tree uses edges A-B, A-C, B-D, C-E, C-F, E-G, and E-H. One round-by-round set of best tuples is: Round 1: A=(A,A,0), B=(A,A,1), C=(A,A,1), D=(B,B,1), E=(C,C,1), F=(C,C,1), G=(E,E,1), H=(E,E,1). Round 2: D=(A,B,2), E=(A,C,2), F=(A,C,2), G=(C,E,2), H=(C,E,2). Round 3: G=(A,E,3), H=(A,E,3), with the other nodes unchanged.

3(b) Draw the resultant spanning tree on the network.

> Keep links A-B, A-C, B-D, C-E, C-F, E-G, and E-H; disable the remaining links D-F and F-G.


## Princeton COS 461 Computer Networks

### Spring 2012 Mid

> PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring12-cos461-exam1-answers.pdf>

| PDF page(s) | Problem / subpart ID(s) retained                           | CSC4303 overlap                                                                 |
| ----------: | ---------------------------------------------------------- | ------------------------------------------------------------------------------- |
|           2 | Question 1(a), 1(b), 1(c)                                  | TCP ACK size, bufferbloat/queueing, VoIP priority                               |
|           3 | Question 2(a), 2(b), 2(c)                                  | TCP three-way handshake timing and lost final ACK                               |
|         4-5 | Question 3(a), 3(b), 3(c), 3(d), 3(e); Question 4(b), 4(c) | IP prefix/default forwarding/TTL; temporary link-state loops and metric changes |
|           6 | Question 5(a), 5(b), 5(c), 5(d)                            | Socket close/FIN, TCP byte stream receive, EOF handling                         |
|        9-10 | Question 7(a), 7(b)                                        | DNS/web redirection/captive-portal flow                                         |


1(a) If the router’s buffer is completely full of TCP acknowledgment packets, how many packets are queued in the buffer? Assume the TCP segment has no payload, and the packet headers do not contain any IPv4 or TCP options. (3 points)

> Ignoring the link-layer header and any minimum size restriction on the link-layer frame, a TCP ACK packet is 40 bytes long, consisting of a 20-byte IP header and a 20-byte TCP header. A 100,000-byte buffer can hold 100000/40 or 2500 ACK packets.

1(b) Suppose the buffer is completely full. How long does it take the router to transmit all of the bytes in the buffer? (3 points)

> Sending 100,000 bytes at 125,000 bytes/sec requires 100000/125000 or 0.8 seconds, or 800 msec.

1(c) Suppose the router supports two first-in first-out queues, one for interactive applications (like Voice over IP) and the other for all remaining traffic, with static priority for the queue handling interactive traffic. If a VoIP packet arrives when the queue for interactive applications is empty, what is the maximum time before the router starts transmitting the VoIP packet? (Assume that the router does not preempt any ongoing packet transmission.) (4 points)

> At worst, the VoIP packets arrives just as the router starts transmitting a full-sized (i.e., 1000-byte) non-VoIP packet, forcing the VoIP packet to wait for 1000/125000 or 0.008 seconds, or 8 msec.

2(a) What is the earliest time that A can start sending data to B? (3 points)

> _____ Immediately after sending the SYN packet to B __X__ Immediately after receiving the SYN-ACK packet from B _____ Immediately after receiving data from B Once the SYN-ACK arrives, A knows that B has A’s initial sequence number and is ready to accept data packets from A.

2(b) What is the earliest time that B can start sending data to A? (3 points)

> _____ Immediately after receiving the SYN packet from A _____ Immediately after sending the SYN-ACK packet to A __X__ Immediately after receiving the ACK packet from A _____ Immediately after receiving data from A Once the ACK arrives, B knows that A has B’s initial sequence number and is ready to accept data packets from B.

2(c) Suppose the ACK packet from A gets lost. What ultimately triggers A to retransmit the lost ACK packet? Assume no other packets get lost and no data packets are sent. (4 points)

> _____ A retransmission timeout at A __X__ A retransmission timeout at B, triggering a retransmission of the SYN-ACK packet ACK packets are not retransmitted, so A does not experience a retransmission timeout. If B does not receive an ACK for the SYN-ACK, then B will retransmit the (presumed lost) SYN-ACK after the retransmission timeout expires.

3(a) How many IP addresses does the campus “own” in its 12.1.0.0/17 block? You can represent your answer as a power of two. (2 points)

> The 17-bit mask leaves 32-17, or 15 bits to identify the addresses within the block. As such, the block contains 215 or 32,768 addresses.

3(b) What are the smallest and largest IP addresses that the campus owns in the block?

> 12.1.0.0 through 12.1.127.255.

3(c) Suppose the ISP router receives a packet with destination IP address 12.1.1.1? What path does this packet follow? (2 points)

> The packet flows over the path 1 -> 2 -> 3 -> 4.

3(d) Suppose the ISP router receives a packet with destination IP address 12.1.20.1? What path does this packet follow? (2 points)

> The packet flows over the path 1 -> 2 -> 3 -> 2 -> 3 ...

3(e) What ultimately happens to a packet with destination IP address 12.1.20.1? Where does it go? (2 points)

> The looping packet is discarded once its IP TTL expires.

4(b) Consider the network below that runs a link-state routing protocol that computes shortest paths as a sum of link weights. The number on each link is the weight of the link in each direction (e.g., links b-c and c-b both have weight 2). Suppose nodes a, b, and d send packets to destination node c. If link d-c (and c-d) fails, which of nodes a, b, and d could conceivably see their packets stuck in a temporary forwarding loop? Which ones would not? (3 points)

> a and d can loop, but not b

4(c) Using the same figure as 4(b), what minimum sequence of weight settings for link d-c avoids blackholes or loops during planned maintenance?

> First change the d-c cost to 3 so node a shifts to the upper path. Then change the cost to 5 or higher so node d shifts to the upper path. Finally shut down d-c after nobody is using it.

5(a) Suppose process A calls send() to send 10,000 bytes of data, and the operating system begins sending the data as a sequence of packets destined to B. If process A calls close() on the socket before the operating system finishes transmitting the data, will the remaining data be sent to B? Why or why not? (3 points)

> Yes, the Operating System continues transmitted the remaining data to B, to ensure the ordered, reliable delivery of the byte stream.

5(b) Suppose process A calls close() after the operating system has transmitted all of the outstanding data. What kind of packet does the operating system send in response to A’s call to close()? (2 points)

> TCP FIN packet

5(c) Explain why B may need to perform multiple calls to recv() to receive all 10,000 bytes of data from A. (3 points)

> The data may not reach B in its entirety at the same time, since it is split into multiple packets. These packets may experience different delays due to congestion, retransmission and receivewindow constraints.

5(d) Suppose B’s operating system has learned that A has closed its end of the connection. Once process B has read all of the data from A, what does B’s next call to recv() return? (2 points)

> A 0, indicating the end of the stream.

7(a) Suppose, before the user pays, the hotspot only allows the user to send and receive UDP packets with source or destination port 53 (the port number used for DNS). Assume the hotspot allows any such traffic to travel to and from the user, independent of the destination IP address. Briefly describe the design of a system that would allow the user to access arbitrary sites on the Internet via the hotspot without paying. The user may need to deploy parts of the system ahead of time. Include a picture. (5 points)

> The user can run a proxy that listens on UDP port 53. The client can encapsulate an IP packet (say, containing a TCP segment) inside UDP packets sent to the proxy, and the proxy can send the traffic to arbitrary Internet services at the client’s request. The responses can be encapsulated and sent back to the client using UDP packets with port 53. To ensure reliability, the client and the proxy can acknowledge received UDP packets and retransmit unacknowledged packets.

7(b) Now suppose that the hotspot only allows DNS queries (i.e., correctly formed DNS requests sent to UDP port 53) destined to the IP address of its own local DNS server, and DNS responses from that server. Design a new solution that allows the user to access arbitrary Internet sites without paying. Include a picture. Note that you should not use this technique in real life to evade paying for Internet service! (5 points)

> The user can run a proxy that acts as an authoritative DNS server for a domain the user has registered (say, jrex.com). To communicate with the proxy, the client sends a DNS request to the hotspot’s local DNS server, with the contents of the message embedded in the domain name (e.g., here-is-my-message.jrex.com). This will trigger the local DNS server to direct the query to the jrex.com authoritative server, which can encode a message in the DNS response (e.g., using the four bytes of the IP address to encode four characters, or using DNS TXT records to encode more information. As in the previous question, the client and the proxy need to acknowledge and retransmit the UDP packets to ensure reliable delivery. The domain names could even embed sequence and acknowledgment information (e.g., here-is-mymessage-X.jrex.com, where X is a number). This class of solutions is known as “DNS tunneling.” Several students offered a different answer that was also valid. The idea is to hijack the hotspot’s local DNS server by sending a forged ARP response for the DNS server’s IP address, learned by the client in DHCP bootstrapping. Now the client can send UDP port 53 packets, and follow the approach in part 7a of the question. Note that this approach may be easier for the hotspot administrators to detect, since the local DNS server would suddenly be carrying no traffic. (That said, even the solution above is relatively easy to detect if the hotspot administrators are monitoring DNS query/response loads on a per-client basis.) Other students offered another answer that was also valid. The client could snoop on DHCP, ARP, or flooded packets to learn the IP addresses of other users who have (presumably) paid for service. The client can then send a forged ARP response for another client’s IP address, and be able to receive packets sent to that address. The client can start sending packets from that address, too, allowing free communication. (This might be detected by the other user, and in fact that user may sometimes send traffic, causing the switches to shift traffic back to the old client. As such, the crafty client would need to repeatedly hijack the original client.)

### Spring 2012 Final

> PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring12-cos461-exam2-answer.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                           |
| ----------: | -------------------------------- | --------------------------------------------------------- |
|           2 | Question 1(a), 1(b), 1(c), 1(d)  | Skype/P2P supernodes; BitTorrent tit-for-tat              |
|           5 | Question 4(a), 4(b), 4(c), 4(d)  | DHCP registration, IP/MAC binding, ARP miss handling      |
|           6 | Question 5(a)                    | Longest-prefix matching and prefix-priority routing rules |


1(a) The Skype peer-to-peer IP telephony application sometimes has a user machine serve as a “super node” to support communication between two other users. When are super nodes needed, and why? (3 points)

> Traversing NATs and firewalls, particularly when both peers lie behind a NAT/firewall that blocks unsolicited traffic from external hosts. Super nodes are also useful for discovering the remote peer.

1(b) Microsoft recently bought Skype. Earlier this month, Microsoft announced that they will replace the classic super nodes with their own super nodes running in Microsoft data centers. Give one reason why Microsoft might have made this decision? (2 points)

> To improve performance and reliability by ensuring super nodes have sufficient resources and predictable operation.

1(c) To prevent free-riding, a BitTorrent peer rates other peers in terms of the download rate they offer, and then decides how much to offer in return. Suppose six users offer data at rates of 10, 4, 8, 3, 7, and 5 Mbps, respectively, and the peer has 15 Mbps of upload bandwidth. What upload rate does it offer to each of the six peers? (3 points)

> The peer uploads with 1/N of its bandwidth to the top N peers, where N is 4 by default. So, the upload rates are 15/4, 0, 15/4, 0, 15/4, 15/4.

1(d) Under the same scenario as question 1(c), suppose peer #1 (currently offering a download rate of 10 Mbps) decides to be more strategic. What is the minimum rate that peer #1 could offer and still achieve the same upload rate it received in question 1(c)? (2 points)

> Just slightly above the fifth peer, or just above 4 Mbps.

4(a) Many enterprise networks only allow registered machines to access the local area network. Some of these networks configure the DHCP server to assign a computer (or MAC address) the same IP address every time it connects to the network. Give one reason why. (3 points)

> Tracking traffic by IP address is much easier if an IP address corresponds to the same user at all time.

4(b) What is the disadvantage of associating each registered MAC address with a pre-determined IP address? (3 points)

> Running out of IP addresses when the number of potential users grows large, even if these users are not active at the same time. Less opportunity for subdividing the topology into separate IP prefixes for more scalable routing.

4(c) To send an IP packet to another host on the same local area network, the sending host first checks its local ARP cache to determine the MAC address associated with the destination IP address. On a “miss” in the ARP cache, the sending host sends an ARP request for the destination IP address and buffers the packet, awaiting a response. Suppose, instead, the host issues the ARP request and simultaneously drops the IP packet. Name one advantage of this approach? (2 points)

> The sending host does not need to buffer the packet until receiving the ARP response. This reduces the memory requirements on the sender, and obviates the need to match the ARP response with some arbitrary packet sitting in a buffer.

4(d) What is one disadvantage of the approach in 4(c)? (2 points)

> The dropped packets must be retransmitted at a higher layer (e.g., TCP). E.g., a dropped SYN packet, in particular, would have a long retransmission timeout.

5(a) An OpenFlow switch can serve as an IP router. Suppose the “IP router” OpenFlow application has forwarding rules for three IP prefixes: (i) 12.1.2.0/24 forwards out link 1, (ii) 12.0.0.0/8 forwards out link 2, and (iii) 12.1.0.0/16 forwards out link 3. What priority order should these rules have in the OpenFlow switch, starting with the highest priority? (2 points)

> The highest priority should go to the longest prefixes. That is, rule 1 should have priority over rule 3, which should have priority over rule 2.

### Spring 2011 Mid

> PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring11-cos461-exam1-answers.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                                 |
| ----------: | -------------------------------- | --------------------------------------------------------------- |
|         2-3 | Question 1(a), 1(b), 1(c)        | NAT/tunneling and packet-header fields                          |
|         4-5 | Question 2(a), 2(b), 2(c), 2(d)  | TCP ACK arithmetic, FIN/close, window/congestion behavior       |
|        8-10 | Question 4                       | IP headers, prefix filters, and routing/filtering rule behavior |


1(a) Header for packet 2 traveling from H1 to H2.

> Ethernet: MAC 1 to MAC 2. IP: 10.0.0.2 to 3.0.1.2.

1(b) Header for packet 3 traveling from H1 to H2.

> Ethernet: MAC 3 to MAC 4. IP: 1.2.3.4 to 3.0.1.2.

1(c) Header for packet 4 traveling from H1 to H2 through the tunnels.

> Ethernet: MAC 9 to MAC 10. Outer IP tunnel: 1.2.3.8 to 1.2.4.3. Inner IP tunnel: 1.2.3.6 to 2.0.0.1. Original IP packet: 1.2.3.4 to 3.0.1.2.

2(a) What event at B causes the TCP sender to decrease its window, and does it prove the network discarded a packet?

> The event is triple duplicate ACK. It does not prove a packet was discarded, because reordering from queuing or asymmetric paths can also create duplicate ACKs.

2(b) What event at D causes the TCP sender to decrease its window, and does it prove the network discarded a packet?

> The event is a timeout. It does not prove packet loss, because congestion in either direction can make RTT exceed the retransmission timeout.

2(c) Why does the TCP window grow with a curved slow-start slope at A instead of a linear slope?

> Slow start quickly discovers the path's usable throughput; pure additive increase would take too many RTTs to reach an efficient window.

2(d) Why might point D be higher than point B when other clients share the same routers?

> Cross traffic from other senders can change over time, so the amount of congestion and the sender's window at later loss points can differ.

4. Short answers on Ethernet/IP, NAT/firewall rules, TCP ACKs, and socket writes.

   > Ethernet-only Internet designs do not scale because flooding/ARP/spanning tree do not scale and MAC addresses are not hierarchical. Assigning IP addresses directly to adapters would lose topological aggregation or require renumbering on movement. With one public NAT address and about 100,000 simultaneous hosts, the NAT can run out of ports. A public web server behind NAT needs port forwarding from public port 80 to the internal server. The firewall should allow SYNs to 1.2.3.4:80, allow SYN-ACKs, allow outbound SYNs from 1.0.0.0/8, deny other inbound SYNs, and allow the rest. ACK 8001 proves three 1000-byte segments were received; duplicate ACKs suggest segment 8001-9000 may be lost; ACK 12001 means none of the original ten are still suspected lost and seven segments were definitely received. A socket read returning 0 means EOF from a remote FIN; a short write of 500 means only part of the requested buffer was accepted, so the program must write the remaining bytes.

### 2010 Mid

> PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring10-cos461-exam1-answers.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                                                                  |
| ----------: | -------------------------------- | ------------------------------------------------------------------------------------------------ |
|         2-4 | Question 1.1, 1.2, 1.3           | DHCP, ARP, DNS, HTTP/TCP connection workflow and packet headers                                  |
|         5-6 | Question 2.1, 2.2, 2.3, 2.4      | TCP congestion control, slow start, AIMD/window calculation                                      |
|         7-8 | Question 3.1, 3.2                | Socket call ordering and looping on send/partial writes                                          |
|        9-11 | Question 4.1(a), 4.1(b), 4.1(c), 4.2(a), 4.2(b), 4.3, 4.4, 4.5 | IP-prefix aggregation, IP/MAC addressing, TCP ACK/loss, ARP-cache conflict, TCP vs UDP selection |
|       12-13 | Question 5.2, 5.3, 5.6           | UDP/TCP socket demultiplexing fields; RED/drop-tail/congestion                                   |

1.1 As the client just joined the network, write the packets used to get an IP address and related network state.

> DHCP Discover: MAC-A to MAC-BR. DHCP Offer: MAC-B to MAC-A. DHCP Request: MAC-A to MAC-BR. DHCP Acknowledgment: MAC-B to MAC-A.

1.2 Now that the client has an IP address, it wants to resolve the IP address of `example.net`, which will be IP-H. Write the packets involved.

> The client first ARPs for the resolver C, then sends a DNS request to C. Resolver C queries the root, `.net`, and `example.net` name servers through gateway G and receives replies from E, F, and I. C then sends the DNS reply back to A.

1.3 Now that the client has IP-H, it wants to download `http://example.net/index.html`. Write the network-layer packets sent to complete this process.

> IP-A to IP-H TCP SYN; IP-H to IP-A TCP SYN-ACK; IP-A to IP-H TCP ACK; IP-A to IP-H HTTP request; IP-H to IP-A TCP ACK; IP-H to IP-A HTTP reply; IP-A to IP-H TCP ACK; then TCP FIN/ACK cleanup. The solution accepted either host initiating close and accepted a four-way FIN/ACK teardown.

2.1 The TCP sender decreases its window at A, C, and D. Name the loss-detection event at each point.

> A: triple duplicate ACK. C: triple duplicate ACK. D: timeout.

2.2 If point A occurs 1 second after the sender begins and the sender has written 15,000 bytes by then with MSS 1000 bytes, what is the RTT?

> 200 ms. The transfer takes 1 RTT for the handshake and 4 RTTs of slow start to send 1+2+4+8 MSS = 15,000 bytes, so 5 RTTs total in 1 second.

2.3 What is the sender's window size at point B?

> 4,000 bytes. After a triple duplicate ACK, AIMD halves the 8 MSS window at A to 4 MSS.

2.4 If point C occurs 2 seconds after point B, what is the sender's window size at point C?

> 14,000 bytes. With 200 ms RTT, 2 seconds is 10 RTTs, so additive increase grows from 4 MSS to 14 MSS.

3.1 Write the basic system calls needed to transfer a file from a TCP client to a server.

> One accepted order is: server `socket`, `bind`, `listen`, `accept`; client `socket`, `bind`, `connect`, `send`; server `recv`; then client `close` and server `close`.

3.2 Write pseudocode for transmitting a 100,000B file using `send`.

> Loop until `sent == len`: call `send(fd, buf + sent, len - sent)`, return failure on a negative result, and add the positive byte count to `sent`. Return success after all bytes have been sent.

4.1(a) Give the IP prefixes for the MIT and Princeton customer networks using as few forwarding-table entries as possible.

> `18.0.0.0/8` and `128.112.0.0/16`.

4.1(b) After the two-entry solution misses some MIT hosts, what three prefixes receive all five hosts?

> `18.0.0.0/8`, `18.0.0.0/24`, and `128.112.0.0/16`.

4.1(c) Give one possible explanation why the change in part (b) is needed.

> `18.0.0.0/24` may be multihomed and announced by another provider; longest-prefix matching can send those hosts through the other provider unless the ISP also installs the more-specific prefix.

4.2(a) Would you recommend replacing IP addresses with globally unique Ethernet addresses? Why or why not?

> No. Broadcast-based discovery would not scale, and MAC addresses are not topologically assigned, so forwarding tables could not be aggregated compactly.

4.2(b) Why not assign IP addresses directly to network adapters and avoid Ethernet addresses?

> Either adapters would need renumbering whenever they move, or static adapter IPs would sacrifice topological aggregation and make routing tables too large.

4.3 Given ACK 10 and then three ACKs for packet 11 after packets 1 through 20 were sent, which packets can be assumed lost and received? After retransmitting the next missing packet and receiving ACK 16, what remains lost and received?

> The sender can infer packet 12 is lost and packets 1-11 were received. After the ACK for 16, no original packets are still assumed lost, and packets 1-16 were definitely received.

4.4 A host D joins with the same IP as A, and a few seconds later B's TCP transfer to A breaks. What steps led to the break?

> When B's ARP cache expires, B ARPs for the shared IP and caches D's MAC address. B's TCP packets then go to D, which has no matching connection and replies with a TCP RST, breaking the connection.

4.5 What transport protocol should be used for speed, long messages, short interactions, fairness, flooding, and flexibility?

> Speed: UDP, because it avoids connection setup and sender-side buffering. Long messages: TCP, because the byte stream supports arbitrarily long data. Short interactions: UDP, because it avoids setup delay. Fairness: TCP, because congestion control shares capacity. Flooding: UDP, because it needs no connection state. Flexibility: UDP, because the application controls more behavior.

5.2 When a UDP segment arrives, what fields does the network stack use to direct it to the appropriate socket?

> Destination IP address and destination port number.

5.3 When a TCP segment belonging to an existing connection arrives, what fields does the network stack use to direct it to the appropriate socket?

> Source IP address, destination IP address, source port number, and destination port number.

5.6 Which advantages does RED have over drop-tail queuing?

> RED has fewer burst losses and shorter queuing delays.

### Spring 2010 Final

> PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring10-cos461-exam2.pdf>

| PDF page(s) | Problem / subpart ID(s) retained                                 | CSC4303 overlap                                                                                                                                  |
| ----------: | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
|         2-3 | Question 1(A), 1(B), 1(C), 1(D), 1(E); Question 2(a), 2(b), 2(c) | HTTP redirection, DNS server selection, IP anycast, NAT/load balancer, ARP spoofing; IPv6; flow-table TCP/UDP filters; IP-header troubleshooting |
|         5-6 | Question 3(a), 3(b), 3(c), 3(d.i), 3(d.ii)                       | Distance-vector routing tables, count-to-infinity, path-vector loop avoidance                                                                    |
|         7-8 | Question 4(a), 4(b), 4(c), 4(d)                                  | Routing/addressing/tunneling headers, NAT, IP/MAC/MPLS                                                                                           |


Source note: the URL is an exam PDF, not an official answer key; retained items in this section have no official solution text in the source.

QUESTION 1: Network system engineering (13 points)

You have recently been hired by FinBook, the online social network for fish. FinBook currently runs on a single server. To support future growth, you hope to deploy multiple servers in multiple datacenters located at different points in the Internet, with a special focus on providing good performance and failure recovery. List some of the pros and cons of using each of the following technologies. Try to give the “best answer” and be specific. Vague comments such as “low overhead” will not get credit (overhead in terms of what?).

1(A) HTTP redirection

> 1 advantage:
>
> 1 disadvantage:

1(B) DNS server-selection

> 1 advantage:
>
> 2 disadvantages:

1(C) IP anycast

> 2 advantage:
>
> 2 disadvantages:

1(D) NAT + load-balancer

> 1 advantage:
>
> 1 disadvantage:

1(E) ARP spoofing (unsolicited announcement of your MAC with other’s IP address)

> 1 advantage:
>
> 1 disadvantage:

QUESTION 2: More network system engineering (13 points)

2(a) You graduated from Princeton (yay!) and joined a social media startup that wants to rival Facebook (at least you hope). The startup doesn’t have any funding, so you took your implementation of simple router and are running it on a Linux box, using it as a router for your servers (instead of paying $$ to Cisco). As your company scaled, you started seeing some clients that use IPv6. Your servers understand IPv6, but your router doesn’t. Describe two ways in which you can extend your router to handle IPv6 traffic:

> Option 1: (answer <= 2 lines)
>
> Option 2: (answer <= 2 lines)

2(b) You are at Princeton for reunions and get a work phone call saying that the servers are running extremely slow and they believe the servers are under a DOS attack. You think this is your competitors (maybe Facebook is afraid of you after all!) and use your iPhone to ssh into your Linux machine. You remember that while implementing a flow table, 0 meant block and 1 meant allow. TCP’s protocol # is 6 and UDP’s is 17. What entries will you add in the flow table to do the following:

> - Allow all TCP traffic from Princeton (128.112.0.0/16)
> - Ban all traffic from 66.220.0.0/16
> - Allow UDP traffic to server 69.65.28.126:3333
>
> Your entries should have the following format:
> `<source IP, destination IP, protocol number, src Port, dst Port, 0 or 1>`

2(c) Your company has grown and now has a couple of thousand users. You said farewell to the your simple router implementation and finally paid some $$ to Cisco. You have multiple servers and routers in your (small) datacenter now. One day you show up at work and find that some clients cannot connect to your servers. In a panic, you start dumping traffic on the ingress gateway router of the problematic servers and see the following packets (partial headers):

| Ver | Length | TOS | TTL | Protocol | Source Addr | Destination Addr |
| --- | -----: | --: | --: | -------: | ----------- | ---------------- |
| 4 | 38 | 0 | 250 | 17 | 139.133.217.110 | 69.65.28.126 |
| 4 | 40 | 0 | 214 | 06 | 121.69.24.120 | 69.65.28.126 |
| 4 | 84 | 0 | 249 | 01 | 18.69.204.150 | 69.65.28.126 |
| 4 | 55 | 0 | 250 | 06 | 192.0.0.15 | 192.0.0.0 |
| 4 | 84 | 0 | 243 | 01 | 18.69.204.150 | 69.65.28.126 |
| 4 | 84 | 0 | 249 | 01 | 128.109.24.10 | 69.65.28.127 |
| 4 | 84 | 0 | 237 | 01 | 18.69.204.150 | 69.65.28.126 |
| 4 | 40 | 0 | 208 | 06 | 121.69.24.120 | 69.65.28.126 |

What is going wrong? Or, explain why this information is useless. (answer <= 2 lines)

QUESTION 3: Distance-Vector Routing (9 points)

The CS department at Princeton bought new Sun Fire V210 servers. They decided to run a distance-vector protocol for routing between these servers (even though it is a rather small network). They are currently configured as the picture below, with respective edge costs.

The CS staff asked for your help. Write down each step of building the distance-vector routing table for ‘Eve’ so they can compare it to the output of their implementation. You can use abbreviations e.g., ‘A’ for Adam and ‘E’ for Eve.

The initial routing table at node A is:

| Destination | Cost | Next Hop |
| ----------- | ---: | -------- |
| B | 21 | B |
| C | ∞ | --- |
| D | 15 | D |
| E | ∞ | --- |

3(a) Show the initial routing table of node E:

> Destination / Cost / Next Hop: A, B, C, D

3(b) Show the routing table of node E after one iteration of the algorithm:

> Destination / Cost / Next Hop: A, B, C, D

3(c) Show the routing table of node E after two iterations of the algorithm:

> Destination / Cost / Next Hop: A, B, C, D

3(d.i) In some failure situations, the administrator notices that it takes an exceptionally long time for the routing protocol to stabilize in this network. What problem with the distance vector protocol is the cause?

3(d.ii) The administrator is told that BGP does not suffer from this problem. What prevents BGP from having this problem?

QUESTION 4: Routing, addressing, and tunneling (9 points)

The above figure shows a network topology connecting two LANs. The LAN on the left uses a NAT to connect to the Internet and includes a client host H1. The LAN on the right includes a webserver H2. Packets between the two LANs are routed along the path shown by a heavy dark lines, which includes both an IP tunnel and an MPLS tunnel. All packets which traverse the path use both tunnels. The various network interfaces have IP and MAC addresses as shown.

H1 has established an HTTP session with web server H2 and data packets are flowing between the two machines. As an example, we have filled in the headers for packet 1 (traveling from the server H2 to the client H1). If there shouldn't be any source or destination field for the header type, write an "X" in that table entry.

| Header Type | Source | Destination |
| ----------- | ------ | ----------- |
| Ethernet | MAC 16 | MAC 15 |
| IP | 3.0.1.2 | 1.2.3.4 |

You have to fill in the header type and the source and destination address for the network and data-link layer headers for packets 2, 3, 4, and 5 (these packets are all traveling from the client H1 to the server H2). Note: You might not need to use all the rows supplied.

4(a) Header for packet 2:

> Header Type / Source / Destination

4(b) Header for packet 3:

> Header Type / Source / Destination

4(c) Header for packet 4:

> Header Type / Source / Destination

4(d) Header for packet 5:

> Header Type / Source / Destination

### 2009 Mid

> PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring09-cos461-exam1-answers.pdf>

| PDF page(s) | Problem / subpart ID(s) retained                              | CSC4303 overlap                                                                              |
| ----------: | ------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
|         2-3 | Question 1(A), 1(B), 1(C), 1(D)                               | Transmission delay, TCP slow start, duplicate ACK vs timeout loss detection                  |
|         4-6 | Question 2(A), 2(B), 2(C)                                     | TCP socket call ordering, TCP stream packetization, UDP datagram packetization               |
|         7-8 | Question 3(A), 3(B)                                           | Web browser request flow with DHCP/ARP/DNS/TCP/HTTP/cache                                    |
|        9-10 | Question 4(A), 4(B), 4(C), 4(D), 4(E), 4(F), 4(G)             | Routing vs bridging, layer-2/layer-3 addressing, ARP                                         |
|       11-12 | Question 5(C), 5(F), 5(G), 5(H)                               | ARP/bridges, DNS TTL/records, web caches, persistent HTTP                                    |
|       13-15 | Question 6(A), 6(B), 6(C), 6(D), 6(E), 6(F), 6(G), 6(H)       | Soft state, exponential backoff, TCP SYN retransmissions, DNS/UDP, NAT, ECN, protocol layers |


1(A) Assuming the full link bandwidth is consumed by a 250,000 byte file over a 2 Mbit/s link, how long does transmission take?

> 1 second: 250,000 bytes * 8 bits/byte / 2,000,000 bits/s.

1(B) Sending the same file via TCP with MSS 1000 bytes, how many RTTs are needed under slow start?

> 9 RTTs: 1 RTT for the SYN/SYN-ACK handshake, then 8 slow-start RTTs sending 1+2+4+8+16+32+64+128 MSS, which exceeds 250,000 bytes.

1(C) If one packet is lost at an instantaneous rate of 32,000 bytes/s, what is the next rate and recovery time?

> With triple duplicate ACK loss detection, TCP halves the rate to 16,000 bytes/s and needs 16 RTTs of additive increase to return to 32,000 bytes/s.

1(D) If all packets are lost at 32,000 bytes/s, what changes?

> Loss is detected by timeout, so TCP drops to one MSS and restarts slow start. Assuming RTT=1s, it takes about 20 RTTs to return to 32,000 bytes/s.

2(A) For the five TCP client/server socket-call orders, can the server ever receive the client data?

> i: No, `connect()` would not return before the server accepts. ii: No, the server is not listening when the client connects. iii: Yes. iv: No, `accept()` cannot return a valid descriptor before the client connects. v: Yes.

2(B) If application A writes to a TCP socket ten times, can the network stack transmit more or fewer than ten packets?

> More than ten: yes, if writes exceed the MSS or packets are retransmitted. Fewer than ten: yes, small writes can be coalesced, for example by Nagle's algorithm.

2(C) If application A calls `sendto()` on a UDP socket ten times, can the network stack transmit more or fewer than ten packets?

> More than ten: yes, a large UDP datagram can be fragmented at IP. Fewer than ten: no, UDP preserves datagram boundaries at the send operation level.

3(A) In the web-cache topology, list the proper order of the packet IDs sent for the first request.

> 11, 7, 2, 3, 12, 9, 4, 5, 10, 8.

3(B) On a subsequent request with all cacheable things cached except A's local web/DNS cache and C's DNS cache, which IDs are eliminated?

> 11, 7, 3, 12, 9, 4, 5, and 10 are eliminated.

4(A) In the routed and bridged network, how many datalink networks are shown?

> 3, corresponding to the networks hanging off router R2.

4(B) Just before the packet reaches bridge B1, what is its layer-2 destination?

> `R2a.mac`.

4(C) Just before the packet reaches bridge B2, what is its layer-2 source?

> `R2c.mac`.

4(D) Just after the packet leaves router R2, what is its layer-3 source?

> `H1.ip`.

4(E) When H1 sends out an ARP query, what is the reply to that query?

> `R2a.mac` has `R2a.ip`.

4(F) Does the entry `B2a.mac` appear in B1’s forwarding table?

> No. `B2a.mac` is on a different datalink network than B1.

4(G) Will SRC’s Ethernet device receive packets with destination `R2a.mac`? Why or why not?

> The official solution accepted both yes and no with correct reasoning. No, if B1 has learned the relevant MAC locations and filters the frame; yes, if SRC is in the same local broadcast domain as the sender or if B1 has not yet learned the addresses and floods the frame.

5(C) Which statements are true about ARP and learning bridges?

> C only: a host's ARP table maps IP addresses to MAC addresses.

5(F) Which statements are true about DNS?

> A and C: an A-record query may return multiple IP addresses, and a short TTL on an NS-record reply can increase traffic at root or GTLD name servers.

5(G) Which statements are true about web caches?

> A and B: a web cache satisfies HTTP requests from clients and acts as both client and server.

5(H) Which statements are true about persistent HTTP connections?

> B is the intended answer: one TCP connection can serve a page if it has no embedded objects from other servers. The solution also accepted A because the wording was confusing.

6(A) Explain soft state and give examples.

> Soft state is temporary state that is refreshed rather than permanently committed; examples include ARP tables, DNS caches, and DHCP leases.

6(B) List two protocols that use exponential backoff and why.

> TCP congestion control backs off to avoid persistent router congestion and drops. Ethernet CSMA/CD backs off to avoid repeated collisions on the shared medium.

6(C) Give three explanations for retransmitting a TCP SYN.

> The SYN may be dropped on path, dropped by B because its receive backlog is full, dropped by a firewall/NAT, or the SYN-ACK may be dropped or delayed past the timeout.

6(D) Why are DNS lookups commonly run over UDP rather than TCP?

> DNS is usually a small query/response exchange, so UDP avoids TCP connection setup, connection state, and larger headers.

6(E) Give two reasons sites use NATs.

> NAT lets multiple private hosts share limited public IPv4 addresses and can hide or firewall internal hosts unless explicit forwarding is configured.

6(F) What header fields might a NAT change on outbound packets?

> Source IP address, source port, IP checksum, and TCP/UDP checksum.

6(G) How does ECN differ from traditional congestion detection, and why is it useful or hard to deploy?

> ECN marks packets instead of relying on packet drops, allowing senders to react without unnecessary loss. Deployment is hard because senders, receivers, and routers all need ECN support.

6(H) Give examples of protocols at OSI layers.

> Application: FTP, HTTP, SMTP, Telnet, SIP. Transport: TCP, UDP, DCCP. Network: IPv4 or IPv6.

### Spring 2008 Mid

Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring08-cos461-exam1-answers.doc>

| Page(s) | Problem / subpart ID(s) retained      | CSC4303 overlap                                                                                                 |
| ------: | ------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
|     DOC | Question 1(a), 1(b), 1(c)             | IP addressing vs MAC addressing; host mobility; DHCP/ARP/MAC learning; hierarchical vs flat forwarding tables   |
|     DOC | Question 3(a), 3(b), 3(c), 3(d)       | TCP receive window, goodput/congestion, retransmission timeout vs duplicate ACK, router queueing/buffering      |
|     DOC | Question 4(a), 4(b), 4(c), 4(d)       | TCP three-way handshake, HTTP persistent connections, HTTP pipelining, TCP byte-stream read behavior            |
|     DOC | Question 5(a), 5(b), 5(c), 5(d), 5(e) | NAT and FTP active/passive mode, payload rewriting, sequence/ACK adjustment, MTU fragmentation                  |
|     DOC | Question 6(e)                         | DNS caching and DNS prefetching                                                                                 |
|     DOC | Question 7(a), 7(b), 7(c), 7(d)       | traceroute TTL/ICMP behavior, route changes during measurement, TCP SYN/SYN-ACK RTT measurement, IP geolocation |


1(a) Why is mobility difficult with today's IP addressing, and why could MAC-only addressing help?

> Today, a host's IP address changes as it moves because IP addresses are hierarchically allocated. A MAC-address Internet would let the host identifier stay the same across moves.

1(b) In a world without IP addresses, which of DHCP, ARP, and MAC learning would still be necessary?

> DHCP would no longer assign IP addresses, though a similar mechanism may configure DNS and gateway information. ARP would not be needed to map IP to MAC. MAC learning would still be needed by switches.

1(c) How would moving to MAC-address forwarding affect forwarding-table size?

> Forwarding tables would grow very large because MAC addresses are not hierarchical and cannot be aggregated like IP prefixes.

3(a) Why might broadband not improve web performance even when the path and server have ample capacity?

> The receiver window may limit throughput, and many web transfers are short enough that RTT and slow start dominate download time.

3(b) Why can total goodput decrease when a path is overloaded?

> Congested networks waste capacity carrying packets that are later dropped and retransmitted, increasing loss and lowering successful delivery rate.

3(c) Why are wireless losses often detected by timeout rather than triple duplicate ACKs?

> Wireless losses are often bursty, so too few later packets arrive to trigger duplicate ACKs; small congestion windows can make this worse. Timeout recovery is slower and hurts performance.

3(d) Give one benefit and two drawbacks of large router buffers.

> Large buffers absorb bursts without drops, but they increase RTT and delay variability and can hide congestion from TCP for longer.

4(a) When can A and B start sending data in the TCP three-way handshake?

> A can send after receiving SYN-ACK. B can send after receiving A's ACK, because only then does B know A is ready and knows B's initial sequence number.

4(b) With HTTP/1.1 pipelining, how does the server know where one request ends and the next begins?

> It parses HTTP request syntax, including CRLF-delimited headers and Content-Length where needed.

4(c) Why cannot TCP guarantee each `read()` or `recv()` returns exactly one HTTP request?

> TCP exposes a byte stream and does not know HTTP message syntax. A request may be larger than buffers or may not have fully arrived when the call returns.

4(d) Why were persistent connections and pipelining added to HTTP/1.1, and why is pipelining usually disabled?

> They avoid repeated TCP setup/teardown and let requests share a connection. Browsers often disable pipelining because head-of-line blocking and buggy intermediaries/servers can hurt reliability or performance.

5(a) Why does active-mode FTP cause problems behind client-side NAT?

> The client sends a private IP and port in the FTP PORT command, while the NAT maps those values externally and may not yet have a data-connection table entry for the server's inbound SYN.

5(b) What must a NAT do to support active-mode FTP?

> It must parse FTP control messages, create a data-connection mapping, and rewrite the PORT command's IP address and port.

5(c) Why can rewriting FTP control messages change IP packet sizes, and how can the NAT handle it?

> Rewritten decimal IP/port strings may have different lengths, so packet sizes and TCP sequence/ACK numbers must be adjusted; if the packet grows beyond MTU, the NAT may fragment it.

5(d) What problems arise if other applications use port 21 or if FTP control traffic is encrypted?

> Other applications can be mistakenly parsed and modified as FTP. Encryption prevents the NAT from seeing and rewriting the PORT command.

5(e) Why is passive-mode FTP easier with client-side NAT?

> The client initiates the data connection to the server's advertised address and port, so the client-side NAT does not need to accept an unsolicited inbound connection or rewrite the client's private address in a PORT command.

6(e) What is one advantage and one disadvantage of DNS cache prefetching before TTL expiry?

> Prefetching can hide DNS lookup delay for users, but it adds DNS queries and network load for mappings that may never be used.

7(a) Give two reasons a traceroute hop might show `*`.

> The probe or the TIME_EXCEEDED response may be lost, the router may suppress TIME_EXCEEDED messages, or a firewall/NAT may drop the packet.

7(b) How can traceroute report a path that does not exist?

> The route can change during measurement, so one probe sees an old hop and the next sees a new hop that is not adjacent to the old one. A middlebox can also obscure the real hop sequence.

7(c) Why is SYN/SYN-ACK delay often larger than a typical RTT?

> The server may queue the SYN in its listen backlog before sending SYN-ACK.

7(d) Give two techniques for inferring an IP host's rough location.

> Reverse DNS and whois records can expose locations. Latency probes from multiple vantage points or traceroute router names near the destination can also provide geographic hints.

### Spring 2008 Final

Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring08-cos461-exam2-answers.doc>

| Page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                           |
| ------: | -------------------------------- | --------------------------------------------------------- |
|     DOC | Question 1(a), 1(b), 1(c), 1(d)  | Link-state routing weights and shortest-path behavior     |
|     DOC | Question 2(a), 2(b), 2(c), 2(d)  | BGP routing policy and RouteViews-style routing reasoning |


1(a) How should link-state routing weights be set to minimize hop count?

> Set all link weights to the same value, such as 1.

1(b) How should weights be set to minimize end-to-end delay when queuing delay is insignificant?

> Set each link weight proportional to its propagation delay or physical length.

1(c) For the given topology, show the sink tree to destination d.

> Nodes a and g take direct paths to d. The other nodes go left until reaching a, d, or g.

1(d) What single weight change diverts traffic from f to d away from edge f-e without affecting other source-destination pairs?

> Change link h-i to weight 2. This makes path f-i-h-g-d cost 21, which is less than the f-e-d path cost 22.

2(a) Draw all paths to destination AS d and identify ASes without a route.

> The paths are b-a-d, g-d, and h-e-d. Nodes c, f, and i cannot reach d.

2(b) What path does e take to i, and what happens if f terminates peering with e?

> Initially e takes e-f-i. Without e-f, e can still reach i via e-b-c-f-i; e-h-i is not used because h would not advertise a peer-learned route to its provider.

2(c) If ASes a and b dump learned BGP paths, what inferred topology is missing?

> The inferred graph misses peering edges d-e, d-f, g-h, and h-i. The dumps expose customer-learned and exportable paths but not all peer edges.

2(d) What minimum set of ASes must dump routes for every edge to be visible?

> Two ASes are enough: b and h, or e and h. h's dump reveals most edges, while b or e exposes the remaining a-d and c-f edges.

### Spring 2007 Mid

Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring07-cos461-exam1-answers.doc>

| Page(s) | Problem / subpart ID(s) retained      | CSC4303 overlap                                                                                             |
| ------: | ------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
|     DOC | Question 1(a), 1(b), 1(c)             | bandwidth-delay product, TCP/IP header overhead, TCP receive-window limiting                                |
|     DOC | Question 2(a), 2(b), 2(c), 2(d), 2(e) | stream sockets, TCP byte stream vs message boundaries, close behavior, SYN retransmission, UDP port binding |
|     DOC | Question 3(a), 3(b), 3(c), 3(d), 3(e) | NAT, ARP/MAC, network-layer protocol demultiplexing, UDP/TCP demultiplexing, socket demultiplexing          |
|     DOC | Question 4(a), 4(c), 4(d), 4(e)       | source-IP spoofing, TCP congestion-response incentives, parallel HTTP/TCP connections, ARP-cache poisoning  |
|     DOC | Question 5(a), 5(b), 5(c), 5(d)       | DHCP client/server behavior, gateway configuration, ARP plus NAT, public vs private IP address discovery    |
|     DOC | Question 6(a), 6(b), 6(c), 6(d), 6(e) | soft state, HTTP vs IP header format, packet-size/fragmentation issues, CIDR, TCP retransmission timeout    |
|     DOC | Question 7(a), 7(b), 7(c), 7(d), 7(e) | TCP AIMD, loss detection/adaptation, DNS hierarchy, hierarchical IP allocation, MAC/link-local addressing   |


1(a) At what file size does the station-wagon solution start delivering data faster than an 800 kbit/s link over 200 km?

> The car takes 2 hours, during which the link can send 720,000,000 bytes, so larger files favor the station wagon.

1(b) With MSS 512 bytes plus 20-byte IP and 20-byte TCP headers, how much more time does the transfer take as a fraction?

> The transfer grows by `552/512`, so it takes `40/512 = 5/64` more time.

1(c) For a 200 km link with propagation speed 200,000,000 m/s, how large must the receive window be to avoid limiting an 800 kbit/s transfer?

> The RTT is 2 ms, so the bandwidth-delay product is 200 bytes.

2(a) Why might TCP transmit more than ten data packets if an application writes to a stream socket ten times?

> A single write can exceed the MSS and be split into multiple TCP segments.

2(b) Why might TCP transmit fewer than ten data packets for ten writes?

> Small writes can be coalesced into fewer segments, for example by Nagle’s algorithm.

2(c) Why can application A safely call `close()` after writing even if application B has not received all data?

> TCP buffers outstanding data and continues retransmitting until the reliable byte stream is delivered or the connection fails.

2(d) List two possible explanations for retransmitting a TCP SYN.

> The SYN may be lost or corrupted, the receiver’s listen queue may be full, the SYN-ACK may be lost, or the RTO may be too small.

2(e) Why is a UDP port number necessary if UDP does not establish a connection?

> The port is needed to demultiplex the packet to the correct receiving socket.

3(a) For inbound traffic through a NAT, what fields determine the internal destination, and what fields does the NAT change?

> The NAT uses the destination port, and possibly the external destination IP address, to find the internal host; it rewrites the destination IP/port and checksums.

3(b) How does the NAT know which destination MAC address to use on the internal Ethernet?

> It looks up the internal destination IP in its ARP table or sends an ARP query.

3(c) How does the destination host know what network-layer protocol parses an Ethernet payload?

> The Ethernet type field identifies the network-layer protocol.

3(d) How does the operating system know whether the packet is UDP or TCP?

> The IP protocol field identifies the transport-layer protocol.

3(e) How does the operating system know which process and socket should receive the packet?

> The IP protocol plus destination transport port identify the receiving socket.

4(a) Why might a cheating host spoof source IP addresses?

> Spoofing can hide the attacker and cause the legitimate address owner to be blamed or receive unwanted return traffic.

4(c) What happens if a TCP sender ignores packet loss and does not reduce its rate?

> It can take unfair bandwidth and may also harm itself through excessive loss and retransmissions.

4(d) Why can parallel browser TCP connections help, and why are they unfair?

> Parallel connections take a larger share during congestion and can improve RTT-limited or slow-start transfers, but they defeat per-flow fairness.

4(e) How can an unsolicited ARP reply be used to cheat?

> A forged ARP reply for the gateway IP can redirect a victim’s external traffic to the rogue machine.

5(a) What DHCP roles does a home-network box play?

> It is a DHCP client to the ISP and a DHCP server for internal hosts.

5(b) What gateway address do home hosts learn?

> They learn the box’s private inside address as their gateway, not the ISP-facing public address.

5(c) What happens when a home host sends a SYN to an external site?

> The host ARPs for the gateway MAC, sends the SYN to the box, and the box NATs the source IP/port before forwarding.

5(d) What address do external sites see for home-host traffic?

> They see the public NAT address because the TCP connection arrives from that address.

6(a) Give one advantage and one disadvantage of soft state, plus examples.

> Soft state tolerates ungraceful failures but needs refresh traffic; examples include DNS TTLs, DHCP leases, ARP caches, and NAT bindings.

6(b) Give one advantage and one disadvantage of text headers, and explain why IP uses binary headers.

> Text headers are readable and extensible but verbose and slower to parse; IP uses compact binary headers to reduce bandwidth and parsing cost.

6(c) Give one advantage and one disadvantage of forcing all packets to be the same size.

> Fixed packet sizes simplify buffering and can avoid length fields, but they waste bandwidth through padding.

6(d) Give one advantage and one disadvantage of CIDR over classful routing.

> CIDR improves allocation and route aggregation, but it requires longest-prefix matching.

6(e) What happens if TCP’s retransmission timeout is too large or too small?

> Too-large RTO delays recovery; too-small RTO causes spurious retransmissions.

7(a) Why does TCP decrease its rate faster than it increases?

> TCP backs off quickly to avoid congestion collapse, then probes capacity cautiously.

7(b) How do timeout loss and triple-duplicate-ACK loss affect TCP’s rate?

> Timeout loss drops the sender to one MSS and restarts slow start; triple-duplicate ACK halves the rate.

7(c) How does a local DNS server learn the TLD servers?

> It learns TLD servers from the root servers because TLD server mappings can change.

7(d) Why does hierarchical IP address allocation help?

> It reduces administration and enables route aggregation.

7(e) Why are MAC addresses globally unique?

> Global uniqueness prevents two devices from colliding when placed on the same LAN.

### Spring 2007 Final

Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring07-cos461-exam2-answers.doc>

| Page(s) | Problem / subpart ID(s) retained            | CSC4303 overlap                                                                                                                            |
| ------: | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
|     DOC | Question 1(a), 1(b), 1(c), 1(d), 1(e), 1(f) | P2P distribution scalability, client/server vs peer-assisted transfer, BitTorrent incentives, incomplete downloads, rare-file availability |
|     DOC | Question 2(a), 2(b), 2(e)                   | link-state routing convergence, transient forwarding loops, BGP over TCP with directly connected peers                                     |
|     DOC | Question 3(a), 3(b), 3(c)                   | multimedia streaming playout delay, TCP vs UDP for interactive media, TCP connections vs virtual circuits                                  |
|     DOC | Question 4(a)                               | broadcast-generating protocols such as ARP and DHCP                                                                                        |
|     DOC | Question 5(a), 5(b), 5(c), 5(d)             | overlay networks, RON-style routing, Napster, Gnutella                                                                                     |
|     DOC | Question 6(a), 6(b), 6(c), 6(d)             | application-layer protocol design, HTTP/TCP delivery, proxies, CDNs                                                                        |
|     DOC | Question 7(a), 7(b), 7(c), 7(d)             | TCP over wireless, page-load performance, transport-header inspection by middleboxes, DNS/BGP layer placement                              |
|     DOC | Question 8(3a), 8(3b), 8(3c)                | source routing vs distributed routing and path control                                                                                     |


1(a) What is the minimum time for one server to transmit a 100 kbyte file to 31 receivers when receivers do not upload?

> Client-server delivery takes 620 seconds.

1(b) If receivers can upload only after receiving the whole file, what is the minimum delivery time?

> Whole-file peer upload takes 100 seconds: five 20-second doubling rounds deliver the file to 31 receivers.

1(c) If receivers can upload after receiving the first 20 kbyte chunk, what is the minimum delivery time?

> Chunked pipelining takes 36 seconds.

1(d) Why do broadband BitTorrent peers mostly exchange chunks with broadband peers, and dial-up peers with dial-up peers?

> BitTorrent peers favor peers that upload to them at high rates, so similar-speed peers tend to cluster.

1(e) Why is BitTorrent vulnerable to incomplete downloads, and what helps prevent it?

> Complete peers may leave after downloading; rarest-first, random chunk selection, and encouraging peers to stay help preserve availability.

1(f) Suggest ways to extend BitTorrent to work better for less popular files.

> Add incentives for peers to store or upload chunks of less popular files, such as cross-file credit or virtual currency usable for faster downloads.

2(a) After link `k-m` fails, what is the path from `i` to `j` before and after convergence?

> Before the failure, `i` reaches `j` via `i-k-m-j` at cost 6; after convergence it uses `i-r-n-j` at cost 8.

2(b) What transient forwarding loop can occur during convergence, and what can happen to data packets?

> Nodes `k` and `n` may loop packets; packets can be dropped by TTL expiry, delayed, or delivered out of order.

2(e) How can two directly connected BGP routers establish TCP before BGP has exchanged routes?

> The routers have directly connected interfaces on the same subnet, so they can reach each other locally, using ARP if needed.

3(a) Which video frames arrive too late with immediate playout, and how much extra playout delay is needed?

> Frames 1, 3, 4, 5, 6, 7, and 8 arrive too late. A 2.05-second extra playout delay covers all shown arrivals.

3(b) List three reasons TCP is ill-suited to interactive audio/video, and why it is often used anyway.

> TCP retransmissions can arrive too late, in-order delivery blocks later data, and congestion control can sharply reduce rate; it is often used because TCP passes firewalls/NATs and is widely supported.

3(c) Why are TCP connections not virtual circuits?

> Routers keep no per-connection path state for TCP; the connection state is at the endpoints.

4(a) Broadcast-generating protocols.

> ARP broadcasts to find the MAC address for an IP address. DHCP broadcasts so a bootstrapping host can find a DHCP server and obtain network configuration.

5(a) What advantages can overlay networks have over the underlying routing system?

> Overlays can probe aggressively, choose application-specific paths, and route around failures faster than the underlay, at the cost of probe overhead.

5(b) Why does RON limit paths to one intermediate hop?

> It keeps routing and probing simple, though it may miss better multi-hop overlay paths.

5(c) What could underlay support expose to overlays?

> The underlay could expose failures, path quality, policy information, or other signals that help overlays choose paths.

5(d) How do Napster and Gnutella differ?

> Napster centralizes indexing; Gnutella floods queries and avoids a central index.

6(a) Why is chatty SMTP bad for mobile wireless, and what can fix it without changing all email servers?

> Many RTTs may not finish before disconnection; a proxy can accept a compact mobile protocol and speak SMTP onward.

6(b) Why are official RFC standards useful, and why might developers skip standardization?

> RFCs provide interoperability, while skipping standardization can move faster if one party controls all deployed software.

6(c) How did Flash, HTTP, and TCP help YouTube succeed?

> Flash was widely deployed on clients, HTTP worked naturally in browsers and through intermediaries, and TCP provided reliable delivery through firewalls and NATs.

6(d) Why have CDNs been more widely deployed than web proxy caches?

> CDNs are controlled by content providers, can be provisioned near users, and do not require clients or ISPs to rely on transparent proxy caching.

7(a) Why does TCP perform poorly over wireless loss, and what can help without changing all wired hosts?

> TCP mistakes wireless loss for congestion; a proxy at the wired/wireless boundary can hide or repair wireless loss.

7(b) Why does a small 1000-character page help web performance?

> It fits in one packet with headers, reducing server work, link load, and transfer latency.

7(c) Why might routers inspect transport headers?

> Routers or middleboxes may inspect transport headers for filtering, NAT, queuing, or measurement.

7(d) Why do DNS and BGP belong at different layers?

> DNS maps names to addresses at the application layer, while BGP distributes interdomain reachability at the routing layer.

8(3a) Give advantages of source routing.

> It lets applications choose paths, react quickly to failures, and avoid untrusted or poor-performing links.

8(3b) Give disadvantages of source routing.

> It can require larger packets, extra sender work, scalable topology knowledge, and can conflict with ISP traffic-engineering policy.

8(3c) Why do operators disable source routing?

> It can bypass policy and security controls, enable abuse, and destabilize traffic engineering.

### Spring 2006 Mid

Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring06-cos461-exam1-answers.doc>
Answer DOC: <https://www.cs.princeton.edu/courses/archive/spr06/cos461/exams/midterm-answers.doc>

| Page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                                   |
| ------: | -------------------------------- | ----------------------------------------------------------------- |
|     DOC | Question 1(a), 1(b), 1(c)        | transmission overhead, packetization, TCP/IP headers, ACK traffic |
|     DOC | Question 2(a), 2(b), 2(c)        | socket programming and networked-application behavior             |


1(a) With MSS 472 and 60 bytes of headers/ACK overhead per data packet, what fraction of bandwidth carries useful data?

> Each data packet is 532 bytes and each ACK is 60 bytes, so useful data consumes `472/592 = 59/74` of bandwidth.

1(b) With MSS 1460, what fraction of bandwidth carries useful data?

> The useful-data fraction is `1460/1580 = 73/79`.

1(c) With delayed ACKs for every other data packet, what fraction of bandwidth carries useful data?

> The useful-data fraction is `2920/3100 = 146/155`.

2(a) Why is sending HTTP response headers one line per socket write inefficient for the end host?

> Each line causes a system call and may force more browser reads.

2(b) Why is sending HTTP response headers one line per socket write inefficient for the network?

> Tiny TCP segments waste bandwidth on headers and generate many ACKs.

2(c) How should the server send the response headers instead?

> It should build the response header in a larger user-space buffer and send it with one socket call.

### Spring 2006 Second Mid

Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring06-cos461-exam2-answers.doc>
Answer DOC: <https://www.cs.princeton.edu/courses/archive/spr06/cos461/exams/midterm2-answers.doc>

| Page(s) | Problem / subpart ID(s) retained  | CSC4303 overlap                                                               |
| ------: | --------------------------------- | ----------------------------------------------------------------------------- |
|     DOC | Question 1, undergraduate version | router state, forwarding/routing behavior, QoS/resource-reservation reasoning |
|     DOC | Question 1, graduate version      | router state, forwarding/routing behavior, QoS/resource-reservation reasoning |


Question 1, graduate version: QoS/token-bucket calculations.

> With bucket depth 10 and token rate 100 cells/s, a circuit can send 110 cells in one second and 1010 cells in ten seconds. A cell arriving behind Q queued cells on a link with propagation P and rate R sees delay P + (Q+1)/R. With bucket depths 9 and 1, token rates 100 each, and propagation 60 ms, the FIFO link needs at least 250 cells/s so 60 ms + 10/R <= 100 ms. Separate queues with strict priority or weighted fair scheduling would reduce the delay-sensitive circuit's exposure to the other circuit's burst.

Question 1, undergraduate version: router state and forwarding/routing behavior.

> The retained source text overlaps the graduate QoS prompt in the extracted DOC; the official DOC source was fetched, but the snippet cache does not contain a separate clean undergraduate solution. The usable retained answer is the QoS/resource-reservation calculation above.


## CMU 15-213 Introduction to Computer Systems

### Fall 2012 Final

> PDF: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f12.pdf>
Model solution TXT: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f12-sol.txt>

| Page(s) | Problem / subpart ID(s) retained          | CSC4303 overlap                                                                                        |
| ------: | ----------------------------------------- | ------------------------------------------------------------------------------------------------------ |
|       3 | Problem 1, item 8                         | short counts in Unix/network I/O; read/write edge cases relevant to socket programming                 |
|       4 | Problem 1, item 10                        | listening-socket readiness vs signals; write on disconnected socket                                    |
|   18-20 | Problem 10(A), 10(B), 10(C), 10(D), 10(E) | race conditions, thread argument passing, synchronization patterns relevant to threaded socket servers |

Problem 1, item 8: When can short counts occur?

> (a) When an EOF is encountered during a read.

Problem 1, item 10: Which of the following events does not generate a signal?

> (b) A new connection arrives on a listening socket.

Problem 10(A): Does program A contain a race on `myid`?

> No. Each thread has its own heap variable for `myid`.

Problem 10(B): Does program B contain a race on `myid`?

> Yes. Both threads can point to the same `myid`.

Problem 10(C): Does program C contain a race on `myid`?

> No. `myid` is passed on the stack.

Problem 10(D): Does program D contain a race on `myid`?

> Yes. The mutex does not protect `myid`.

Problem 10(E): Does program E contain a race on `myid`?

> No. The mutex protects the assignment of `myid`.

### Spring 2011 Final

> PDF: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-s11.pdf>
Model solution TXT: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-s11-sol.txt>

| Page(s) | Problem / subpart ID(s) retained       | CSC4303 overlap                                                                             |
| ------: | -------------------------------------- | ------------------------------------------------------------------------------------------- |
|       5 | Problem 1, item 9; Problem 1, item 14  | gethostbyname network failure and thread-safety                                             |
|       7 | Problem 1, item 18; Problem 1, item 21 | socket send blocking/short writes; debugging a network application with system-call tracing |

Problem 1, item 9: Which of the following system calls can fail due to a network failure?

> (d) `gethostbyname(...)`.

Problem 1, item 14: Which function is not thread-safe?

> (c). The retained source is a multiple-choice answer key; the key lists item 14 as answer (c).

Problem 1, item 18: When requested to send 20 bytes over a network socket, execution will block until all 20 bytes have been sent. (✅/❌ )

> False.

Problem 1, item 21: Which tool would you first use to debug an application that is exiting with an error from a system call?

> (b) `strace`.

### Fall 2010 Final

> PDF: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f10.pdf>
Model solution TXT: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f10-sol.txt>

| Page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                        |
| ------: | -------------------------------- | ------------------------------------------------------ |
|       2 | Problem 1, item 1                | socket/listen/connect/accept/socket/bind call ordering |

Problem 1, item 1: Fill in the client/server network call order for `listen`, `connect`, `accept`, `socket`, and `bind`.

> Client: `socket` = 1, `bind` = 2, `connect` = 3. Server: `socket` = 1, `bind` = 2, `listen` = 3, `accept` = 4.

### Fall 2009 Final

> PDF: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f09.pdf>
Model solution TXT: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f09-sol.txt>

| Page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                                   |
| ------: | -------------------------------- | ----------------------------------------------------------------- |
|       3 | Problem 1, item E                | listening-socket events and signal misconceptions                 |
|   12-13 | Problem 6(A), 6(B)               | TCP client/server call sequence; short recv/partial-read behavior |

Problem 1, item E: A new connection arrives on a listening socket. Does this generate a signal?

> No. A listening-socket readiness event is handled by socket APIs such as `accept`; it is not delivered as a Unix signal.

Problem 6(A): List the network-related calls for the logging server and client, in call order.

> Server: `socket`, `bind`, `listen`, `accept`, `read`, `close`. Client: `socket`, `connect`, `write`, `close`.

Problem 6(B): What short-read/partial-read behavior should the program handle?

> `recv`/`read` may return fewer bytes than requested, so the program must loop until it has received the full message or sees EOF/error.

### Spring 2009 Final

> PDF: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-s09.pdf>
Model solution TXT: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-s09-sol.txt>

| Page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                               |
| ------: | -------------------------------- | ------------------------------------------------------------- |
|   13-15 | Problem 6(A), 6(B)               | socket server error paths; threaded server/network logic bugs |

Problem 6(A): Fill in error handling for `socket`, `recv`, and `send`.

> On `socket` error: `exit(-1)`. On `recv` error: break out of the connection-handling loop. On `send` error: break out of the connection-handling loop.

Problem 6(B): Identify the network/concurrency bugs in the server.

> Bug 1: `buffer` is global and shared by all threads, causing a race; it should be local to `handleConnection()`. Bug 2: `send()` can return a short count, so positive return values must be checked and any remaining bytes resent.

## Topic filter used

Retained: CSC4303-relevant networking and distributed-systems material. Filtered out: transactions/WAL/ARIES, Paxos/consensus/BFT, distributed mutual exclusion, security protocols, assembly, caches, virtual memory, malloc, and other topics outside the CSC4303 review/sample scope.
