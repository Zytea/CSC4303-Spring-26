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

   func (client *Client) Submit(data []byte) {
   	msg, _ := json.Marshal(data)
   	client.send(msg) // Send message to Dotolab
   	ackMsg := client.ReadFromServer() // Wait for Ack from Dotolab
   	ack := json.Unmarshal(ackMsg)
   }

   > Solution: Since send is called just once when the student submits, the message may get dropped along the way, and the server may never receive the submission. In order to fix it, Eunice should send the message in a for loop until some sort of acknowledgement is received from the server.
   >
   > func (client *Client) Submit(data []byte) {
   >     msg, _ := json.Marshal(data)
   > 	for {
   > 		client.send(msg) // Send message to Dotolab
   > 		ackMsg := client.ReadFromServer() // Wait for Ack from Dotolab
   > 		if ackMsg != nil {
   > 			ack := json.Unmarshal(ackMsg)
   > 			break
   > 		}
   > 	}
   > }
   
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

   Bob wants to publish this new kvstore to clients using a RPC framework without writing a server by himself. Which RPC semantics should he choose? Why?

   > At-least-once. With the new implementation, all three operations are idempotent because we disallowed duplicates. Putting the same values multiple times will result in the same final state.

   7.3 After publishing his kvstore service, Bob notices that the get(key) function is often slow when it has a large array to return. Bob remembers the pass-by-reference trick he often uses and changes his get() function to return the memory address of the result array:

   *int[] get(string key):
   	return &kvs[key]

   Will his approach work? Why or why not?

   > No, because the client machine doesn’t share the address space with kvstore and can’t access the memory location returned.

### Mid Fall 2019

PDF: <https://www.synergylabs.org/courses/15-440/assignments/Fall2019-Midterm-I-WithSolutions.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                                 |
| ----------: | -------------------------------- | --------------------------------------------------------------- |
|           2 | Question 1(b)                    | VoIP transport choice                                           |
|           3 | Question 2(a), 2(b)              | RPC over UDP; RPC marshalling of pointer/linked data structures |
|           4 | Question 2(f)(a), 2(f)(b)        | Cristian-style time synchronization with asymmetric delays      |

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

PDF: <https://www.synergylabs.org/courses/15-440/assignments/Fall2018-Midterm-I-WithSolutions.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                                   |
| ----------: | -------------------------------- | ----------------------------------------------------------------- |
|           4 | Question 2(a), 2(b), 2(c)        | VoIP/UDP; vector clocks in Dynamo-style systems; NTP vs Cristian  |
|           6 | Question 3(a), 3(b), 3(c)        | RPC performance, latency sensitivity, and marshalling bottlenecks |
|          11 | Question 6(a), 6(c)              | RPC semantics for non-idempotent and idempotent operations        |

2(a) You are responsible for building the successor to the popular Skype Voice-over-IP protocol that works across the internet (high RTTs). Your boss went to CMU but did not take 441 or 440, and thinks you should use TCP due to its reliable delivery feature. Can you explain to him why this is not a good idea?

> Use UDP (as discussed in class). Reliability is less important than reducing delay and jitter. TCP can cause delays for longer RTT links due to reliable delivery and need for ACKs. (One point for mentioning one of packet loss/UDP, delay and jitter).

2(b) NoSQL systems like Amazon’s Dynamo allows writes to continue to all machines during a network partition. Once reconnected, Dynamo nodes seek to reconcile inconsistent file versions. Which technique would you choose to detect and flag parallel events? Briefly explain why.

> Vector clocks. Only algorithm that can properly preserve causality, so Dynamo would know that two events happened in parallel. Lamport clocks can’t do this, as they create arbitrarily ordered timestamps, which might give two parallel events different timestamps. (2 points for Vector clocks and 2 points for correct reason. Note: Totally Ordered Lamport clocks is incorrect)

2(c) Name and briefly describe two differences between the time synchronization algorithm used in NTP and Christian’s algorithm.

> [Solution missing in source snippet.]

3. You are hired by the augmented reality startup AR2 that needs to perform a complex image processing algorithm. Because mobile phones have little computing power, AR2 ’s algorithm gets unacceptably slow as image sizes increase. Your manager, Jaine, proposes to use RPC to perform the work on a remote, more powerful server. You measure the following numbers, assuming a base image scaling factor of N. • The running time of AR2 ’s algorithm is M (N ) = 3N ms on a mobile phone. On the server, its S(N ) = N/3 ms. • Marshalling and unmarshalling take (N/6 + 20) ms in total. • The average RTT between a user and the server is 80 ms. • Bandwidth is infinite between the user and the server.

3(a) For what value of N is Jaine right, i.e., AR2 should be using an RPC instead of a local call?

> Want 3N ≥ 80ms + (N/6 + 20)ms + N/3 = 100ms + N/2. So, N ≥ 40. We also accepted answers that considered 2(N/6 + 20)ms or 4(N/6 + 20)ms

3(b) With geo-replication, AR2 is able to reduce the average RTT. How will N change? (Give a qualitative answer)

> It decreases, because the server’s computation becomes as fast as the phone’s for a lower value of N .

3(c) As AR2 acquires 1) more and more powerful servers and 2) places them closer to users, you notice that the total RPC time does not improve very much. Explain why, by pointing out the bottleneck, in two sentences or less.

> The bottleneck is the marshalling time. No matter how much everything else is improved, the marshalling time will keep the RPC time high.

6. BergerNet is a new social network started by the TAs and Professors of 15440 providing almost the same functionality as social networks do today. As a new engineering lead, it is your job to make some crucial design decisions that are either going to make or break the BergerNet. BergerNet uses RPCs. Identify the easiest-to-implement RPC semantic (at-leastonce, at-most-once, exactly-once) for each of the following features. Give a *one sentence* reason for your choice. (1pt for semantic, 1pt for reason only if semantic correct).

6(a) Transferring money to your friend on BergerNet

> At-most once. Easiest to implement and can always retry sending on failure.

6(c) Deleting a friend on BergerNet

> At-least once. Delete is idempotent. At-most once does not work because it is not the easiest to implement.

### Fall 2016

PDF: <https://www.synergylabs.org/courses/15-440/assignments/Fall2016-Midterm-II-WithSolutions.pdf>

| PDF page(s) | Problem / subpart ID(s) retained      | CSC4303 overlap                                                             |
| ----------: | ------------------------------------- | --------------------------------------------------------------------------- |
|           2 | Question 1(A)                         | MapReduce reducer key-space partitioning                                    |
|           3 | Question 2(a.A), 2(a.B)               | Consistent hashing and failure/view divergence                              |
|           4 | Question 2(c.A), 2(c.B), 2(e)         | MapReduce stragglers/master failure; DNS caching and replication resilience |
|         6-7 | Question 4(a), 4(b), 4(c), 4(d), 4(e) | DNS/CDN hierarchy; Chord lookup and finger-table reasoning                  |

1(A) For a particular Map-Reduce Phase with ‘M’ and ’R’ nodes respectively, each reducer node handles 1/R of the intermediate key-values by default. (✅/❌ )

> TRUE. Each Reducer node handles 1/R of the possible keyspace and fetches them from each of the M Mappers.

1(B) In case of System Virtualization, the hypervisor (or VMM) can only allocate and assign the actual number of physical processor resources it has available at its disposal to individual Virtual Machines (VMs). (✅/❌ )

> FALSE. Virtualization allows you to overcommit resources and provide more virtual resources than actual physical resources, for example by time multiplexing the same set of CPU/processors across multiple VMs.

1(C) DES (symmetric key) is faster than RSA (public-private key) (✅/❌ )

> TRUE. Symmetric key ciphers are generally going to be faster than Public-private key ciphers due to the mathematical complexity of the latter.

1(D) When setting up a TOR circuit the sender is guaranteed that the path taken (intermediate routers) to the receiver will be the same as without using TOR. (✅/❌ )

> FALSE. There are no guarantees, and the sender decides which path to take when using TOR, which comprises of TOR nodes and not the regular internet routers.

2(a) Consistent hashing is used in a variety of distributed systems over more traditional hashing algorithms. A. Describe one way that consistent hashing performs better when failures occur (e.g. in DHTs or in CDNs).

> Less content needs to be moved between nodes.

2(B) Describe one way that consistent hashes perform better when nodes have differing views on the availability of servers.

> Consistent hashing reduces the spread of requests across nodes when views are different

2(b) You are working on a MAC laptop and using it to develop and test a new Linux OS/kernel. You are worried about bugs since they will cause the Linux kernel to crash. Explain how the ’Isolation’ property of hosted Virtualization solution like VMWare Workstation running on your MAC can help in this case.

> Fault Isolation: We can run the new Linux kernel in a VM. If this VM kernel contains a bug, and crashes it will not crash the main host (OSX) thereby providing fault isolation and allow development and testing to continue.

2(e) The DNS root and GTLD servers often come under attack. Give 2 reasons that we don’t notice when they are under attack.

> The records from the root and GTLD have long TTLs and are cached widely. The root and GTLD zones are replicated very widely and it is difficult to attack all locations at the same time.

### Mid 2012

PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/midterm2012-solve.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                                   |
| ----------: | -------------------------------- | ----------------------------------------------------------------- |
|         2-3 | Question 1(d), 1(e), 1(f)        | UDP for VoIP; TCP vs UDP for large RPC results; RPC failure modes |
|           5 | Question 3(a)                    | UDP buffer reuse and concurrency race conditions                  |
|           9 | Question 4(h), 4(i)              | UDP checksum behavior; sequence-number wrap and delayed packets   |
|       13-14 | Question 6(a), 6(b), 6(c), 6(d)  | Lamport and vector-clock message timestamps                       |

1(d) (✅/❌ )

> Losing some audio bits isn’t as bad as dealing with the delays from TCP’s retransmission.

1(e) UDP is better (✅/❌ )

> 100KB is too big to fit in a single packet. The RPC system would just end up re-implementing much of what TCP does to split this data into packets and ensure that it is received reliably and reassembled. This would therefore be a poor idea.

1(f) RPCs provide different semantics from local calls because RPCs introduce a different of errors. class (✅/❌ )

> [Solution missing in source snippet.]

3(a) func `ReadHandler(conn *net.UDPConn)` { bytes:= make([]byte, 2000) for { n, _, _:= conn.ReadFromUDP(bytes) go ProcessPacket(bytes[0:n]) } } Spin loop Race condition Deadlock Correct Explain briefly (1-2 sentences) where the bug is. No explanation is necessary if you mark Correct.

> bytes corresponds to some memory that is reused by ReadFromUDP. Thus, the slice to ProcessPacket could be overwritten while it is being processed.

4(h) LSP could be extended to be robust, with high probability, in the presence of corrupted UDP packets by appending a checksum to each message and dropping any that are received with an incorrect checksum. (✅/❌ )

> The resending of messages will ensure that (eventually) a valid packet will be sent.

4(i) If a UDP packet gets delayed by several seconds, then the message it contains could be mistaken for one that occurs much later in the message sequence. (✅/❌ )

> Due the the wrapping around of sequence numbers.

### Mid 2011

PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/midterm2011_solve.pdf>

| PDF page(s) | Problem / subpart ID(s) retained            | CSC4303 overlap                                                                           |
| ----------: | ------------------------------------------- | ----------------------------------------------------------------------------------------- |
|         2-3 | Question 1(b), 1(c), 1(d), 1(h), 1(i), 1(j) | Checksums; TCP latency; UDP connection setup; synchronous RPC; Lamport clocks; GPS vs NTP |
|       13-15 | Question 6(a), 6(b), 6(c), 6(d)             | Lamport timestamps and causal ordering                                                    |

1(b) The checksum portion of an IP packet allowsthe receiver to both detect and correct a single-bit error in the packet (✅/❌ )

> Checksums can be used to detect errors, but not to correct them.

1(c) TCP’s reliable in-order byte stream messages under high packet loss. to a server, the client and server will engage in a (✅/❌ )

> [Solution missing in source snippet.]

1(d) When creating a UDP connection handshake protocol. (✅/❌ )

> There is no setup phase with UDP

1(h) When making a synchronous RPC call, the caller will not return until after quested operation has been completed, assuming no error is encountered. (✅/❌ )

> [Solution missing in source snippet.]

1(i) If the Lamport clock of event e1 is less than the Lamport clock of evente2, then there must be a chain of causal events by which e1 precedes e2 (✅/❌ )

> [Solution missing in source snippet.]

### Mid 2010

PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/midterm2010_solve.pdf>

| PDF page(s) | Problem / subpart ID(s) retained    | CSC4303 overlap                         |
| ----------: | ----------------------------------- | --------------------------------------- |
|           2 | Question 1                          | RPC vs local procedure-call differences |
|           4 | Question 8                          | Application-level choice of UDP or TCP  |
|       11-13 | Question 11(a), 11(b), 11(c), 11(d) | Lamport/Shamport clock ordering         |

1. RPC tries to make remote procedure calls look the same as local procedure calls. But the illusion isn’t perfect. Circle all of the options that correctly describe differences between a local function call and an RPC: A. RPC calls require an extra parameter to identify the server. B. RPC calls may have higher or variable latency. C. RPC calls are limited to call-by-value. D. RPC calls have different (more) failure modes. E. Local function calls require a malloc of a heap object to represent the return pointer.

> A,B,D

8. For which of the following applications would UDP be preferable over TCP, ignoring annoying concerns such as firewalls that might block some protocols? A. Streaming a live video over the internet TCP / UDP B. Instant messaging/email TCP / UDP C. Logging in to your bank website TCP / UDP D. Voice over IP TCP / UDP E. Large file transfers TCP / UDP F. Looking up a very small value from a directory service TCP / UDP

> UDP, TCP, TCP, UDP, TCP, UDP

e each computer in a distributed system keeps an approximate real-time clock Ri in addition to a Lamport-like clock Li. A computer’s real-time clock Ri is an always-increasing integer (i.e., for any two reads r1, r2 of Ri such that r1 →i r2, we have r2 > r1 ), but the real-time clocks at different computers may drift relative to each other (i.e., Rj − Ri is non-constant for j 6= i). Consider the following modification, Shamport, to Lamport’s partial-ordering algorithm: Rule 1: Before each event at computer i, set Li = min(Li + 1, Ri ). Rule 2: When sending a message m, apply Rule 1 and include the time Li as part of the message (i.e. send (m, Li ) instead of just m). Rule 3: When receiving a message (m, t) at computer j, set Lj = max(Lj, t) and then apply Rule 1 before timestamping the message-arrival event. Let the Shamport global time of an event e at computer i be S(e) = Li (e).

11(a) In the algorithm above, underline the difference between Shamport and Lamport’s algorithm. (Underline as little as possible).

> Shamport’s algorithm uses Li = min(Li + 1, Ri ) in Rule 1 instead of Li = Li + 1. Otherwise the two algorithms are the same.

11(b) Let e, e0 be two events at computer i such that e →i e0. Prove that S(e0 ) > S(e).

> The key observation is that any new event advances the logical clock. There are a couple common pitfalls to avoid: (1) e and e0 are not necessarily consecutive events; other intervening events can affect the Shamport clock. (2) Events at computer i include the local side of send and receive events, so you need to include possible applications of Rule 2 and Rule 3 in your proof. And (3), reading the problem correctly to understand that the logical clocks Li here are not Lamport clocks, and thus you cannot blindly apply the rules for Lamport clocks from class. One proof is: Consider the sequence of all events e . . . e0 at computer i. If S(e0 ) ≤ S(e) then there must exist at least one pair of consecutive events f, f 0 (WLOG f →i f 0 ) such that S(f 0 ) ≤ S(f ); otherwise each new event would advance the logical clock Li , which would yield Li (e0 ) > Li (e0 ) and thus S(e0 ) > S(e). To show S(e0 ) > S(e), therefore, it suffices to show that Li (f 0 ) > Li (f ) for any two consecutive events f →i f 0 . Let (t, r) be the logical and real-time clock times for event f and (t0 , r0 ) be the times for f 0 . We must show that t0 > t for any events f and f 0 . We break this into three cases based on whether f 0 is a normal local event, a send event, or a receive event. (In each of these cases we allow f to be any type of event.) Notice that in every case we have r0 > r because Ri is always-increasing and f →i f 0 . Case 1: f 0 is a normal local event. This causes a single application of Rule 1, yielding t0 = min(t + 1, r0 ). Briefly consider the rule that set the logical clock for f . Because all three rules last-affect the logical clock with an application of Rule 1, we have that t = min(,̇r) and thus that t ≤ r, yielding t < r0 . Because t + 1 > t and r0 > t we therefore have that t0 > t regardless of which term of the min-operation is lesser, yielding that S(f 0 ) > S(f ) as desired if f 0 is a local-only event. Case 2: f 0 is a send event. This causes an application of Rule 2, which affects the logical clock only with an application of Rule 1. Thus, Case 2 reduces directly to Case 1.

### Final 2009

PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/final2009-solve.pdf>

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

### Final 2010

PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/final2010-solve.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                                                               |
| ----------: | -------------------------------- | --------------------------------------------------------------------------------------------- |
|           2 | Question 1, 2                    | TCP handshake misconception; Internet best effort; DNS TTL/invalidation; GFS/HDFS assumptions |
|         5-6 | Question 4, 5, 6                 | Chord/P2P lookup and design trade-offs                                                        |
|           9 | Question 11, 12                  | Lamport timestamp ordering                                                                    |

1. Circle the one that best applies. Grading is 2 points for every correct answer. That means that at the end of the exam, if you don’t know the right answer, come back here and guess randomly! Threads and Processes True, False It is less expensive to create a process than a thread. True, False Switching between threads is faster than switching between processes. True, False In order to switch between user threads, you need to enter the kernel. True, False Threads share a heap and a stack. Networking True, False The TCP initial handshake must be completed between the sender and every router on the path to the destination before communication can take place. True, False The Internet service model allows a small (a percent or two) amount of packet loss. (In other words, end-hosts must be able to deal with a small amount of loss) True, False Domain Name Service (DNS) servers remember which clients have cached DNS replies so that the servers can send invalidation messages when name bindings change. Distributed Mutual Exclusion True, False Ring-based distributed mutual exclusion is a great solution for a latency-sensitive application running on 10,000 nodes. Logging True, False Write-ahead logging is a useful technique for providing persistence for random updates without needing to write to a random location on disk. True, False For correctness, all write-ahead log records must specify how to both undo and redo the operation they describe. Tor True, False The onion routing scheme used by Tor is resilient to an attacker that can simultaneously compromise every node in the Tor network. --- 2. Which of the following design assumptions apply to HDFS/GFS? (Circle all that apply) A. Only amazingly powerful servers can handle the size and complexity of the workload. B. Any use of a centralized server would cause too much of a bottleneck. C. Component failures are expected. D. Files are huge by traditional standards. E. File contents are often updated and overwritten. (✅/❌ )

> C, D

4. Suppose the above Chord setup: • At what node do you expect to find key 10? • At what node do you expect to find key 9? • On average, how many hops are there when searching for a key? • What route will a search for key 11 take, starting at node 3?

> [Solution missing in source snippet.]

5. Suppose you want to build a large distributed system to store cookie recipes. Each cookie is stored using the recipe’s name (“Grandma’s Arsenic Cookie Surprise”). Unlike many P2P systems, in this one, the recipe data is small, so you wanted to store the actual data in the P2P system instead of leaving it on the original nodes. A friend says “Hey, I hear that Chord is very efficient – it doesn’t take many lookups to find the node containing the data.” Explain to your friend why directly throwing this data into a DHT such as chord, with key = recipe name, value = recipe data, is a really bad design decision. Brief - two sentences or so.

> [Solution missing in source snippet.]

6. Tell us what style of P2P system you would use, and what assumptions you think are reasonable for your cookie-storing-system: • Number of nodes • Number of recipes • Number of queries/second • What do queries look like? Style of system AND a brief rationale for this decision:

> [Solution missing in source snippet.]

11. What is the value of x? If it cannot be determined, write “unknown”.

> [Solution missing in source snippet.]

12. For the following, circle which event happened first. If it cannot be determined, circle “unknown.” • L1 (m1, send) L4 (m5, send) U nknown • L2 (m3, send) L3 (m4, send) U nknown • L3 (m4, send) L3 (m3, recv) U nknown • L2 (m3, send) L4 (m6, send) U nknown • L4 (m6, send) L1 (m7, send) U nknown

> [Solution missing in source snippet.]

### Final 2011

PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/final2011-solve.pdf>

| PDF page(s) | Problem / subpart ID(s) retained            | CSC4303 overlap                                                     |
| ----------: | ------------------------------------------- | ------------------------------------------------------------------- |
|         2-3 | Question 1                                  | DNS hierarchy; DNS caching; CDN via DNS                             |
|       10-11 | Question 6(a), 6(b), 6(c), 6(d), 6(e), 6(f) | Napster, query flooding, supernodes, flooding limits                |
|       12-13 | Question 7(a), 7(b), 7(c), 7(d), 7(e), 7(f) | DHT/Chord ring mapping, finger table, successor, fallback/proximity |
|       15-16 | Question 9(a), 9(b), 9(c), 9(d)             | MapReduce/GFS failure handling and stragglers                       |

6. (a) In a centralized p2p network (such as the old Napster), how many indices must be searched if a client wants to locate a particular file?

> 1

6(b) Name one major disadvantage of the centralized p2p system (from a distributed principles point of view)

> - Single point of failure - Server processes everything - Server must keep track of a potentially very large number of clients - more?

6(c) Query flooding is an alternative design that solves some of the problems of centralized p2p and eliminates the central server. However, it changes the mechanics of peer interactions significantly. Explain (1 sentence each) how a newly-joining node publishes the files they wish to make available, in... A centralized p2p network:

> They send their list of files and metadata to the server.
>
> A query flooding p2p network:

6(d) One popular improvement upon query flooding is to move to a “supernode” flooding architecture. Using N as the number of nodes in the network and, S as the number of supernodes (S << N ), explain the benefit of moving to this supernode architecture.

> Queries require now O(S) messages instead of O(N ). In addition, if the nodes used as supernodes are more stable or have higher capacity, can further improve the performance or stability of the network.

7. (a) In a distributed hash table (DHT) using a ring mapping, explain how a key is mapped to a specific node?

> Keys and nodes map to points in a ring space. A node handles all keys mapped between it and its successor.

7(b) In the most basic form of DHT systems, nodes simply track their predecessor and successor. Very briefly state what problem this leads to as the network grows larger.

> Performance problems as nodes forward a key resolution request to larger chains of neighbors.

7(c) The Chord scheme overcomes this problem by having each node maintain a “finger table”. Given starting node j and destination node k, where k > j, how much is the distance between the two nodes reduced with each hop?

> It decreases exponentially, or it is cut in half

7(d) In a Chord structured DHT with N nodes, how many hops would a lookup operation require?

> log(N )

7(e) Assume a Chord network in which node q is the successor of node p. During operation, node p discovers that its successor link is no longer consistent because q has updated its predecessor link. What does this change imply must have happened in the network?

> A new node joined the network ’between’ p and q.

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

PDF: <https://courses.cs.washington.edu/courses/cse461/23sp/samples/sample-midterm2-key.pdf>

| PDF page(s) | Problem / subpart ID(s) retained     | CSC4303 overlap                                                                               |
| ----------: | ------------------------------------ | --------------------------------------------------------------------------------------------- |
|           2 | Problem 1(a), 1(d), 1(e)             | Layering, internetworking, encapsulation                                                      |
|         3-4 | Problem 3(a), 3(b), 3(c), 3(d)       | ICMP, NAT, IPv6 motivation, tunneling                                                         |
|           5 | Problem 4(a), 4(b), 4(c), 4(d)       | Routing vs forwarding, longest-prefix matching, local/gateway forwarding, routing scalability |
|           6 | Problem 5(a), 5(b), 5(c), 5(d), 5(e) | Distance-vector vs link-state routing, convergence, RIP, OSPF/IS-IS                           |

### Mid Review Practice, Section 4

PDF: <https://courses.cs.washington.edu/courses/cse461/23sp/section/4-midterm-review.pdf>

| PDF page(s) | Problem / subpart ID(s) retained                                 | CSC4303 overlap                                           |
| ----------: | ---------------------------------------------------------------- | --------------------------------------------------------- |
|       12-16 | Practice Problems: Bandwidth Allocation; Practice Problems: AIMD | Max-min fairness and AIMD calculations                    |
|       53-54 | Practice Problems: Link-State Routing                            | Link-state routing convergence and inconsistent LSP views |

### Winter 2017 Mid

PDF: <https://courses.cs.washington.edu/courses/cse461/22wi/practice-materials/midterm-2.3.17.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                                |
| ----------: | -------------------------------- | -------------------------------------------------------------- |
|         4-5 | Problem 3                        | Distance-vector routing table updates and forwarding decisions |


## Princeton COS 461 Computer Networks

### Spring 2012 Mid

PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring12-cos461-exam1-answers.pdf>

| PDF page(s) | Problem / subpart ID(s) retained                           | CSC4303 overlap                                                                 |
| ----------: | ---------------------------------------------------------- | ------------------------------------------------------------------------------- |
|           2 | Question 1(a), 1(b), 1(c)                                  | TCP ACK size, bufferbloat/queueing, VoIP priority                               |
|           3 | Question 2(a), 2(b), 2(c)                                  | TCP three-way handshake timing and lost final ACK                               |
|         4-5 | Question 3(a), 3(b), 3(c), 3(d), 3(e); Question 4(b), 4(c) | IP prefix/default forwarding/TTL; temporary link-state loops and metric changes |
|           6 | Question 5(a), 5(b), 5(c), 5(d)                            | Socket close/FIN, TCP byte stream receive, EOF handling                         |
|        9-10 | Question 7                                                 | DNS/web redirection/captive-portal flow                                         |

### Spring 2012 Final

PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring12-cos461-exam2-answer.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                           |
| ----------: | -------------------------------- | --------------------------------------------------------- |
|           2 | Question 1(a), 1(b), 1(c), 1(d)  | Skype/P2P supernodes; BitTorrent tit-for-tat              |
|           5 | Question 4(a), 4(b), 4(c), 4(d)  | DHCP registration, IP/MAC binding, ARP miss handling      |
|           6 | Question 5(a)                    | Longest-prefix matching and prefix-priority routing rules |

### Spring 2011 Mid

PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring11-cos461-exam1-answers.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                                 |
| ----------: | -------------------------------- | --------------------------------------------------------------- |
|         2-3 | Question 1(a), 1(b), 1(c)        | NAT/tunneling and packet-header fields                          |
|         4-5 | Question 2(a), 2(b), 2(c), 2(d)  | TCP ACK arithmetic, FIN/close, window/congestion behavior       |
|        8-10 | Question 4                       | IP headers, prefix filters, and routing/filtering rule behavior |

### 2010 Mid

PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring10-cos461-exam1-answers.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                                                                  |
| ----------: | -------------------------------- | ------------------------------------------------------------------------------------------------ |
|         2-4 | Question 1.1, 1.2, 1.3           | DHCP, ARP, DNS, HTTP/TCP connection workflow and packet headers                                  |
|         5-6 | Question 2.1, 2.2, 2.3, 2.4      | TCP congestion control, slow start, AIMD/window calculation                                      |
|         7-8 | Question 3.1, 3.2                | Socket call ordering and looping on send/partial writes                                          |
|        9-11 | Question 4.1, 4.2, 4.3, 4.4, 4.5 | IP-prefix aggregation, IP/MAC addressing, TCP ACK/loss, ARP-cache conflict, TCP vs UDP selection |
|       12-13 | Question 5.2, 5.3, 5.6           | UDP/TCP socket demultiplexing fields; RED/drop-tail/congestion                                   |

### Spring 2010 Final

PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring10-cos461-exam2.pdf>

| PDF page(s) | Problem / subpart ID(s) retained                                 | CSC4303 overlap                                                                                                                                  |
| ----------: | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
|         2-3 | Question 1(A), 1(B), 1(C), 1(D), 1(E); Question 2(a), 2(b), 2(c) | HTTP redirection, DNS server selection, IP anycast, NAT/load balancer, ARP spoofing; IPv6; flow-table TCP/UDP filters; IP-header troubleshooting |
|         5-6 | Question 3(a), 3(b), 3(c), 3(d.i), 3(d.ii)                       | Distance-vector routing tables, count-to-infinity, path-vector loop avoidance                                                                    |
|         7-8 | Question 4(a), 4(b), 4(c), 4(d)                                  | Routing/addressing/tunneling headers, NAT, IP/MAC/MPLS                                                                                           |

### 2009 Mid

PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring09-cos461-exam1-answers.pdf>

| PDF page(s) | Problem / subpart ID(s) retained        | CSC4303 overlap                                                                              |
| ----------: | --------------------------------------- | -------------------------------------------------------------------------------------------- |
|         2-3 | Question 1A, 1B, 1C, 1D                 | Transmission delay, TCP slow start, duplicate ACK vs timeout loss detection                  |
|         4-6 | Question 2A, 2B, 2C                     | TCP socket call ordering, TCP stream packetization, UDP datagram packetization               |
|         7-8 | Question 3A, 3B                         | Web browser request flow with DHCP/ARP/DNS/TCP/HTTP/cache                                    |
|        9-10 | Question 4A, 4B, 4C, 4D, 4E, 4F, 4G     | Routing vs bridging, layer-2/layer-3 addressing, ARP                                         |
|       11-12 | Question 5C, 5F, 5G, 5H                 | ARP/bridges, DNS TTL/records, web caches, persistent HTTP                                    |
|       13-15 | Question 6A, 6B, 6C, 6D, 6E, 6F, 6G, 6H | Soft state, exponential backoff, TCP SYN retransmissions, DNS/UDP, NAT, ECN, protocol layers |

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

### Spring 2008 Final

Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring08-cos461-exam2-answers.doc>

| Page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                           |
| ------: | -------------------------------- | --------------------------------------------------------- |
|     DOC | Question 1                       | Link-state routing weights and shortest-path behavior     |
|     DOC | Question 2                       | BGP routing policy and RouteViews-style routing reasoning |

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

### Spring 2006 Mid

Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring06-cos461-exam1-answers.doc>
Answer DOC: <https://www.cs.princeton.edu/courses/archive/spr06/cos461/exams/midterm-answers.doc>

| Page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                                   |
| ------: | -------------------------------- | ----------------------------------------------------------------- |
|     DOC | Question 1                       | transmission overhead, packetization, TCP/IP headers, ACK traffic |
|     DOC | Question 2                       | socket programming and networked-application behavior             |

### Spring 2006 Second Mid

Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring06-cos461-exam2-answers.doc>
Answer DOC: <https://www.cs.princeton.edu/courses/archive/spr06/cos461/exams/midterm2-answers.doc>

| Page(s) | Problem / subpart ID(s) retained  | CSC4303 overlap                                                               |
| ------: | --------------------------------- | ----------------------------------------------------------------------------- |
|     DOC | Question 1, undergraduate version | router state, forwarding/routing behavior, QoS/resource-reservation reasoning |
|     DOC | Question 1, graduate version      | router state, forwarding/routing behavior, QoS/resource-reservation reasoning |


## CMU 15-213 Introduction to Computer Systems

### Fall 2012 Final

PDF: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f12.pdf>
Model solution TXT: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f12-sol.txt>

| Page(s) | Problem / subpart ID(s) retained          | CSC4303 overlap                                                                                        |
| ------: | ----------------------------------------- | ------------------------------------------------------------------------------------------------------ |
|       3 | Problem 1, item 8                         | short counts in Unix/network I/O; read/write edge cases relevant to socket programming                 |
|       4 | Problem 1, item 10                        | listening-socket readiness vs signals; write on disconnected socket                                    |
|   18-20 | Problem 10(A), 10(B), 10(C), 10(D), 10(E) | race conditions, thread argument passing, synchronization patterns relevant to threaded socket servers |

### Spring 2011 Final

PDF: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-s11.pdf>
Model solution TXT: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-s11-sol.txt>

| Page(s) | Problem / subpart ID(s) retained       | CSC4303 overlap                                                                             |
| ------: | -------------------------------------- | ------------------------------------------------------------------------------------------- |
|       5 | Problem 1, item 9; Problem 1, item 14  | gethostbyname network failure and thread-safety                                             |
|       7 | Problem 1, item 18; Problem 1, item 21 | socket send blocking/short writes; debugging a network application with system-call tracing |

### Fall 2010 Final

PDF: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f10.pdf>
Model solution TXT: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f10-sol.txt>

| Page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                        |
| ------: | -------------------------------- | ------------------------------------------------------ |
|       2 | Problem 1, item 1                | socket/listen/connect/accept/socket/bind call ordering |

### Fall 2009 Final

PDF: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f09.pdf>
Model solution TXT: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f09-sol.txt>

| Page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                                   |
| ------: | -------------------------------- | ----------------------------------------------------------------- |
|       3 | Problem 1, item E                | listening-socket events and signal misconceptions                 |
|   12-13 | Problem 6(A), 6(B)               | TCP client/server call sequence; short recv/partial-read behavior |

### Spring 2009 Final

PDF: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-s09.pdf>
Model solution TXT: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-s09-sol.txt>

| Page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                               |
| ------: | -------------------------------- | ------------------------------------------------------------- |
|   13-15 | Problem 6(A), 6(B)               | socket server error paths; threaded server/network logic bugs |

## Topic filter used

Retained: CSC4303-relevant networking and distributed-systems material. Filtered out: transactions/WAL/ARIES, Paxos/consensus/BFT, distributed mutual exclusion, security protocols, assembly, caches, virtual memory, malloc, and other topics outside the CSC4303 review/sample scope.
