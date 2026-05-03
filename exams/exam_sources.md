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

PDF: <https://www.synergylabs.org/courses/15-440/assignments/Fall2019-Mid-I-WithSolutions.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap |
|---:|---|---|
| 2 | Question 1(b) | VoIP transport choice |
| 3 | Question 2(a), 2(b) | RPC over UDP; RPC marshalling of pointer/linked data structures |
| 4 | Question 2(f)(a), 2(f)(b) | Cristian-style time synchronization with asymmetric delays |

### Fall 2018 

PDF: <https://www.synergylabs.org/courses/15-440/assignments/Fall2018-Mid-I-WithSolutions.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap |
|---:|---|---|
| 4 | Question 2(a), 2(b), 2(c) | VoIP/UDP; vector clocks in Dynamo-style systems; NTP vs Cristian |
| 6 | Question 3(a), 3(b), 3(c) | RPC performance, latency sensitivity, and marshalling bottlenecks |
| 11 | Question 6(a), 6(c) | RPC semantics for non-idempotent and idempotent operations |

### Fall 2016 

PDF: <https://www.synergylabs.org/courses/15-440/assignments/Fall2016-Mid-II-WithSolutions.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap |
|---:|---|---|
| 2 | Question 1(A) | MapReduce reducer key-space partitioning |
| 3 | Question 2(a.A), 2(a.B) | Consistent hashing and failure/view divergence |
| 4 | Question 2(c.A), 2(c.B), 2(e) | MapReduce stragglers/master failure; DNS caching and replication resilience |
| 6-7 | Question 4(a), 4(b), 4(c), 4(d), 4(e) | DNS/CDN hierarchy; Chord lookup and finger-table reasoning |

### Mid 2012

PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/midterm2012-solve.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap |
|---:|---|---|
| 2-3 | Question 1(d), 1(e), 1(f) | UDP for VoIP; TCP vs UDP for large RPC results; RPC failure modes |
| 5 | Question 3(a) | UDP buffer reuse and concurrency race conditions |
| 9 | Question 4(h), 4(i) | UDP checksum behavior; sequence-number wrap and delayed packets |
| 13-14 | Question 6(a), 6(b), 6(c), 6(d) | Lamport and vector-clock message timestamps |

### Mid 2011 

PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/midterm2011_solve.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap |
|---:|---|---|
| 2-3 | Question 1(b), 1(c), 1(d), 1(h), 1(i), 1(j) | Checksums; TCP latency; UDP connection setup; synchronous RPC; Lamport clocks; GPS vs NTP |
| 13-15 | Question 6(a), 6(b), 6(c), 6(d) | Lamport timestamps and causal ordering |

### Mid 2010 

PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/midterm2010_solve.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap |
|---:|---|---|
| 2 | Question 1 | RPC vs local procedure-call differences |
| 4 | Question 8 | Application-level choice of UDP or TCP |
| 11-13 | Question 11(a), 11(b), 11(c), 11(d) | Lamport/Shamport clock ordering |

### Final 2009 

PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/final2009-solve.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap |
|---:|---|---|
| 2 | Question 1, 2, 3, 4 | DNS scalability; Chord; RPC library responsibilities; content-based P2P naming |
| 3 | Question 6(a), 6(h) | GFS data path; Lamport happens-before implication |
| 8-11 | Question 14 | MapReduce-style distributed data processing |

### Final 2010 

PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/final2010-solve.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap |
|---:|---|---|
| 2 | Question 1, 2 | TCP handshake misconception; Internet best effort; DNS TTL/invalidation; GFS/HDFS assumptions |
| 5-6 | Question 4, 5, 6 | Chord/P2P lookup and design trade-offs |
| 9 | Question 11, 12 | Lamport timestamp ordering |

### Final 2011 

PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/final2011-solve.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap |
|---:|---|---|
| 2-3 | Question 1 | DNS hierarchy; DNS caching; CDN via DNS |
| 10-11 | Question 6(a), 6(b), 6(c), 6(d), 6(e), 6(f) | Napster, query flooding, supernodes, flooding limits |
| 12-13 | Question 7(a), 7(b), 7(c), 7(d), 7(e), 7(f) | DHT/Chord ring mapping, finger table, successor, fallback/proximity |
| 15-16 | Question 9(a), 9(b), 9(c), 9(d) | MapReduce/GFS failure handling and stragglers |

## UW CSE 461 Computer Networks

### Sample Mid 2 

PDF: <https://courses.cs.washington.edu/courses/cse461/23sp/samples/sample-midterm2-key.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap |
|---:|---|---|
| 2 | Problem 1(a), 1(d), 1(e) | Layering, internetworking, encapsulation |
| 3-4 | Problem 3(a), 3(b), 3(c), 3(d) | ICMP, NAT, IPv6 motivation, tunneling |
| 5 | Problem 4(a), 4(b), 4(c), 4(d) | Routing vs forwarding, longest-prefix matching, local/gateway forwarding, routing scalability |
| 6 | Problem 5(a), 5(b), 5(c), 5(d), 5(e) | Distance-vector vs link-state routing, convergence, RIP, OSPF/IS-IS |

### Mid Review Practice, Section 4

PDF: <https://courses.cs.washington.edu/courses/cse461/23sp/section/4-Mid-review.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap |
|---:|---|---|
| 12-16 | Practice Problems: Bandwidth Allocation; Practice Problems: AIMD | Max-min fairness and AIMD calculations |
| 53-54 | Practice Problems: Link-State Routing | Link-state routing convergence and inconsistent LSP views |

### Winter 2017 Mid

PDF: <https://courses.cs.washington.edu/courses/cse461/22wi/practice-materials/Mid-2.3.17.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap |
|---:|---|---|
| 4-5 | Problem 3 | Distance-vector routing table updates and forwarding decisions |

## Princeton COS 461 Computer Networks

### Spring 2012 Mid 

PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring12-cos461-exam1-answers.pdf>

| Page(s) | Problem / subpart ID(s) retained                           | CSC4303 overlap                                              |
| ------: | ---------------------------------------------------------- | ------------------------------------------------------------ |
|       2 | Question 1(a), 1(b), 1(c)                                  | TCP ACK size, bufferbloat/queueing, VoIP priority            |
|       3 | Question 2(a), 2(b), 2(c)                                  | TCP three-way handshake timing and lost final ACK            |
|     4-5 | Question 3(a), 3(b), 3(c), 3(d), 3(e); Question 4(b), 4(c) | IP prefix/default forwarding/TTL; temporary link-state loops and metric changes |
|       6 | Question 5(a), 5(b), 5(c), 5(d)                            | Socket close/FIN, TCP byte stream receive, EOF handling      |
|    9-10 | Question 7                                                 | DNS/web redirection/captive-portal flow                      |

### Spring 2012 Final 

PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring12-cos461-exam2-answer.pdf>

| Page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                           |
| ------: | -------------------------------- | --------------------------------------------------------- |
|       2 | Question 1(a), 1(b), 1(c), 1(d)  | Skype/P2P supernodes; BitTorrent tit-for-tat              |
|       5 | Question 4(a), 4(b), 4(c), 4(d)  | DHCP registration, IP/MAC binding, ARP miss handling      |
|       6 | Question 5(a)                    | Longest-prefix matching and prefix-priority routing rules |

### Spring 2011 Mid 

PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring11-cos461-exam1-answers.pdf>

| Page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                              |
| ------: | -------------------------------- | ------------------------------------------------------------ |
|     2-3 | Question 1(a), 1(b), 1(c)        | NAT/tunneling and packet-header fields                       |
|     4-5 | Question 2(a), 2(b), 2(c), 2(d)  | TCP ACK arithmetic, FIN/close, window/congestion behavior    |
|    8-10 | Question 4                       | IP headers, prefix filters, and routing/filtering rule behavior |

### 2010 Mid 

PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring10-cos461-exam1-answers.pdf>

| Page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                              |
| ------: | -------------------------------- | ------------------------------------------------------------ |
|     2-4 | Question 1.1, 1.2, 1.3           | DHCP, ARP, DNS, HTTP/TCP connection workflow and packet headers |
|     5-6 | Question 2.1, 2.2, 2.3, 2.4      | TCP congestion control, slow start, AIMD/window calculation  |
|     7-8 | Question 3.1, 3.2                | Socket call ordering and looping on send/partial writes      |
|    9-11 | Question 4.1, 4.2, 4.3, 4.4, 4.5 | IP-prefix aggregation, IP/MAC addressing, TCP ACK/loss, ARP-cache conflict, TCP vs UDP selection |
|   12-13 | Question 5.2, 5.3, 5.6           | UDP/TCP socket demultiplexing fields; RED/drop-tail/congestion |

### Spring 2010 Final

PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring10-cos461-exam2.pdf>

| Page(s) | Problem / subpart ID(s) retained                             | CSC4303 overlap                                              |
| ------: | ------------------------------------------------------------ | ------------------------------------------------------------ |
|     2-3 | Question 1(A), 1(B), 1(C), 1(D), 1(E); Question 2(a), 2(b), 2(c) | HTTP redirection, DNS server selection, IP anycast, NAT/load balancer, ARP spoofing; IPv6; flow-table TCP/UDP filters; IP-header troubleshooting |
|     5-6 | Question 3(a), 3(b), 3(c), 3(d.i), 3(d.ii)                   | Distance-vector routing tables, count-to-infinity, path-vector loop avoidance |
|     7-8 | Question 4(a), 4(b), 4(c), 4(d)                              | Routing/addressing/tunneling headers, NAT, IP/MAC/MPLS       |

### 2009 Mid

PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring09-cos461-exam1-answers.pdf>

| Page(s) | Problem / subpart ID(s) retained        | CSC4303 overlap                                              |
| ------: | --------------------------------------- | ------------------------------------------------------------ |
|     2-3 | Question 1A, 1B, 1C, 1D                 | Transmission delay, TCP slow start, duplicate ACK vs timeout loss detection |
|     4-6 | Question 2A, 2B, 2C                     | TCP socket call ordering, TCP stream packetization, UDP datagram packetization |
|     7-8 | Question 3A, 3B                         | Web browser request flow with DHCP/ARP/DNS/TCP/HTTP/cache    |
|    9-10 | Question 4A, 4B, 4C, 4D, 4E, 4F, 4G     | Routing vs bridging, layer-2/layer-3 addressing, ARP         |
|   11-12 | Question 5C, 5F, 5G, 5H                 | ARP/bridges, DNS TTL/records, web caches, persistent HTTP    |
|   13-15 | Question 6A, 6B, 6C, 6D, 6E, 6F, 6G, 6H | Soft state, exponential backoff, TCP SYN retransmissions, DNS/UDP, NAT, ECN, protocol layers |

### Spring 2008 Mid 

DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring08-cos461-exam1.doc>  
Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring08-cos461-exam1-answers.doc>

| Page(s) | Problem / subpart ID(s) retained      | CSC4303 overlap                                              |
| ------: | ------------------------------------- | ------------------------------------------------------------ |
|     DOC | Question 1(a), 1(b), 1(c)             | IP addressing vs MAC addressing; host mobility; DHCP/ARP/MAC learning; hierarchical vs flat forwarding tables |
|     DOC | Question 3(a), 3(b), 3(c), 3(d)       | TCP receive window, goodput/congestion, retransmission timeout vs duplicate ACK, router queueing/buffering |
|     DOC | Question 4(a), 4(b), 4(c), 4(d)       | TCP three-way handshake, HTTP persistent connections, HTTP pipelining, TCP byte-stream read behavior |
|     DOC | Question 5(a), 5(b), 5(c), 5(d), 5(e) | NAT and FTP active/passive mode, payload rewriting, sequence/ACK adjustment, MTU fragmentation |
|     DOC | Question 6(e)                         | DNS caching and DNS prefetching                              |
|     DOC | Question 7(a), 7(b), 7(c), 7(d)       | traceroute TTL/ICMP behavior, route changes during measurement, TCP SYN/SYN-ACK RTT measurement, IP geolocation |

### Spring 2008 Final 

DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring08-cos461-exam2.doc>  
Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring08-cos461-exam2-answers.doc>

| Page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                           |
| ------: | -------------------------------- | --------------------------------------------------------- |
|     DOC | Question 1                       | Link-state routing weights and shortest-path behavior     |
|     DOC | Question 2                       | BGP routing policy and RouteViews-style routing reasoning |

### Spring 2007 Mid 

DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring07-cos461-exam1.doc>  
Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring07-cos461-exam1-answers.doc>

| Page(s) | Problem / subpart ID(s) retained      | CSC4303 overlap                                              |
| ------: | ------------------------------------- | ------------------------------------------------------------ |
|     DOC | Question 1(a), 1(b), 1(c)             | bandwidth-delay product, TCP/IP header overhead, TCP receive-window limiting |
|     DOC | Question 2(a), 2(b), 2(c), 2(d), 2(e) | stream sockets, TCP byte stream vs message boundaries, close behavior, SYN retransmission, UDP port binding |
|     DOC | Question 3(a), 3(b), 3(c), 3(d), 3(e) | NAT, ARP/MAC, network-layer protocol demultiplexing, UDP/TCP demultiplexing, socket demultiplexing |
|     DOC | Question 4(a), 4(c), 4(d), 4(e)       | source-IP spoofing, TCP congestion-response incentives, parallel HTTP/TCP connections, ARP-cache poisoning |
|     DOC | Question 5(a), 5(b), 5(c), 5(d)       | DHCP client/server behavior, gateway configuration, ARP plus NAT, public vs private IP address discovery |
|     DOC | Question 6(a), 6(b), 6(c), 6(d), 6(e) | soft state, HTTP vs IP header format, packet-size/fragmentation issues, CIDR, TCP retransmission timeout |
|     DOC | Question 7(a), 7(b), 7(c), 7(d), 7(e) | TCP AIMD, loss detection/adaptation, DNS hierarchy, hierarchical IP allocation, MAC/link-local addressing |

### Spring 2007 Final 

Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring07-cos461-exam2-answers.doc>

| Page(s) | Problem / subpart ID(s) retained            | CSC4303 overlap                                              |
| ------: | ------------------------------------------- | ------------------------------------------------------------ |
|     DOC | Question 1(a), 1(b), 1(c), 1(d), 1(e), 1(f) | P2P distribution scalability, client/server vs peer-assisted transfer, BitTorrent incentives, incomplete downloads, rare-file availability |
|     DOC | Question 2(a), 2(b), 2(e)                   | link-state routing convergence, transient forwarding loops, BGP over TCP with directly connected peers |
|     DOC | Question 3(a), 3(b), 3(c)                   | multimedia streaming playout delay, TCP vs UDP for interactive media, TCP connections vs virtual circuits |
|     DOC | Question 4(a)                               | broadcast-generating protocols such as ARP and DHCP          |
|     DOC | Question 5(a), 5(b), 5(c), 5(d)             | overlay networks, RON-style routing, Napster, Gnutella       |
|     DOC | Question 6(a), 6(b), 6(c), 6(d)             | application-layer protocol design, HTTP/TCP delivery, proxies, CDNs |
|     DOC | Question 7(a), 7(b), 7(c), 7(d)             | TCP over wireless, page-load performance, transport-header inspection by middleboxes, DNS/BGP layer placement |
|     DOC | Question 8(3a), 8(3b), 8(3c)                | source routing vs distributed routing and path control       |

### Spring 2006 Mid 

Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring06-cos461-exam1-answers.doc>  
Original course answer DOC: <https://www.cs.princeton.edu/courses/archive/spr06/cos461/exams/Mid-answers.doc>

| Page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                              |
| ------: | -------------------------------- | ------------------------------------------------------------ |
|     DOC | Question 1                       | transmission overhead, packetization, TCP/IP headers, ACK traffic |
|     DOC | Question 2                       | socket programming and networked-application behavior        |

### Spring 2006 Second Mid 

Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring06-cos461-exam2-answers.doc>  
Original course answer DOC: <https://www.cs.princeton.edu/courses/archive/spr06/cos461/exams/midterm2-answers.doc>

| Page(s) | Problem / subpart ID(s) retained  | CSC4303 overlap                                              |
| ------: | --------------------------------- | ------------------------------------------------------------ |
|     DOC | Question 1, undergraduate version | router state, forwarding/routing behavior, QoS/resource-reservation reasoning |
|     DOC | Question 1, graduate version      | router state, forwarding/routing behavior, QoS/resource-reservation reasoning |

## CMU 15-213 Introduction to Computer Systems

### Fall 2012 Final

PDF: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f12.pdf>  
Model solution TXT: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f12-sol.txt>

| Page(s) | Problem / subpart ID(s) retained          | CSC4303 overlap                                              |
| ------: | ----------------------------------------- | ------------------------------------------------------------ |
|       3 | Problem 1, item 8                         | short counts in Unix/network I/O; read/write edge cases relevant to socket programming |
|       4 | Problem 1, item 10                        | listening-socket readiness vs signals; write on disconnected socket |
|   18-20 | Problem 10(A), 10(B), 10(C), 10(D), 10(E) | race conditions, thread argument passing, synchronization patterns relevant to threaded socket servers |

### Spring 2011 Final

PDF: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-s11.pdf>  
Model solution TXT: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-s11-sol.txt>

| Page(s) | Problem / subpart ID(s) retained       | CSC4303 overlap                                              |
| ------: | -------------------------------------- | ------------------------------------------------------------ |
|       5 | Problem 1, item 9; Problem 1, item 14  | gethostbyname network failure and thread-safety              |
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

| Page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                              |
| ------: | -------------------------------- | ------------------------------------------------------------ |
|       3 | Problem 1, item E                | listening-socket events and signal misconceptions            |
|   12-13 | Problem 6(A), 6(B)               | TCP client/server call sequence; short recv/partial-read behavior |

### Spring 2009 Final

PDF: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-s09.pdf>  
Model solution TXT: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-s09-sol.txt>

| Page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                              |
| ------: | -------------------------------- | ------------------------------------------------------------ |
|   13-15 | Problem 6(A), 6(B)               | socket server error paths; threaded server/network logic bugs |

## Topic filter used

Retained: CSC4303-relevant networking and distributed-systems material. Filtered out: transactions/WAL/ARIES, Paxos/consensus/BFT, distributed mutual exclusion, security protocols, assembly, caches, virtual memory, malloc, and other topics outside the CSC4303 review/sample scope.
