# CSC4303 Exam Source

## CMU 15-440/640 Distributed Systems

### Mid Fall 2021

> PDF: <https://www.synergylabs.org/courses/15-440/assignments/Midterm1-Fall2021-solutions.pdf>

1(b) A text messaging application would best be implemented using UDP. (✅/❌)

> False. Text messaging necessitates reliable, in-order service, so TCP should be used.

1(d) A Remote Procedure Call (RPC) enables a computer program to execute a subroutine in its own memory address space. (✅/❌)

> False. RPCs enable subroutine execution in a remote address space.

1(f) DHCP is used to translate hostnames into IP addresses. (✅/❌)

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

   > 44 is the only possible Lamport clock value for event h. Therefore, its totally ordered value is $M \cdot L_i(e) + i = 10 \cdot 44 + 2 = 442$.

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

1.7 Transmission delay is proportional to the packet size, while propagation delay is proportional to the length of the link.

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

1(b) Over a wide area network it is better to use TCP to implement Voice-over-IP telephony rather than UDP given the potential for packet losses. (✅/❌)

> False. UDP is still going to be better for the VoIP app since VoIP is real time and the delays caused by TCP retransmission would make things worse. What’s more, VoIP is loss-tolerant.

2(a) Can you implement an RPC system using UDP connections, instead of TCP? Answer yes/no and explain why or why not in at most two sentences.

> Yes. It does not matter what transport-layer protocol you choose for the RPC system. You can choose to implement over an unreliable network connection and rely on the RPC system to detect and tolerate failures.

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

   - The running time of AR2’s algorithm is $M(N) = 3N$ ms on a mobile phone. On the server, its $S(N) = N/3$ ms.
   - Marshalling and unmarshalling take $(N/6 + 20)$ ms in total.
   - The average RTT between a user and the server is 80 ms.
   - Bandwidth is infinite between the user and the server.

   3(a) For what value of N is Jaine right, i.e., AR2 should be using an RPC instead of a local call?

   > When $3N \ge 80\text{ ms} + (N/6 + 20)\text{ ms} + N/3\text{ ms} = 100\text{ ms} + (N/2)\text{ ms}$. So, $N \ge 40$.

   3(b) With geo-replication, AR2 is able to reduce the average RTT. How will N change? (Give a qualitative answer)

   > It decreases, because the server’s computation becomes as fast as the phone’s for a lower value of N .

   3(c) As AR2 acquires

   1. more and more powerful servers and
   2. places them closer to users,

   you notice that the total RPC time does not improve very much. Explain why, by pointing out the bottleneck, in two sentences or less.

   > The bottleneck is the marshalling time. No matter how much everything else is improved, the marshalling time will keep the RPC time high.

6. BergerNet is a new social network started by the TAs and Professors of 15440 providing almost the same functionality as social networks do today. As a new engineering lead, it is your job to make some crucial design decisions that are either going to make or break BergerNet. BergerNet uses RPCs. Identify the easiest-to-implement RPC semantic (at-least-once, at-most-once, exactly-once) for each of the following features. Give a *one sentence* reason for your choice. (1 point for the semantic, 1 point for the reason only if the semantic is correct.)

   6(a) Transferring money to your friend on BergerNet

   > At-most-once. Easiest to implement, and the user can retry on failure.

   6(c) Deleting a friend on BergerNet

   > At-least-once. Delete is idempotent. At-most-once does not work because it is not the easiest to implement.

### Fall 2016

> PDF: <https://www.synergylabs.org/courses/15-440/assignments/Fall2016-Midterm-II-WithSolutions.pdf>

1(b) In case of system virtualization, the hypervisor (or VMM) can only allocate and assign the actual number of physical processor resources it has available at its disposal to individual virtual machines (VMs). (✅/❌)

> False. Virtualization allows you to overcommit resources and provide more virtual resources than actual physical resources, for example by time-multiplexing the same set of CPUs across multiple VMs.

2(a) Consistent hashing is used in a variety of distributed systems over more traditional hashing algorithms.

   2(a.A) Describe one way that consistent hashing performs better when failures occur (e.g. in DHTs or in CDNs).

   > Less content needs to be moved between nodes.

   2(a.B) Describe one way that consistent hashes perform better when nodes have differing views on the availability of servers.

   > Consistent hashing reduces the spread of requests across nodes when views are different.

2(b) You are working on a MAC laptop and using it to develop and test a new Linux OS/kernel. You are worried about bugs since they will cause the Linux kernel to crash. Explain how the ’Isolation’ property of hosted Virtualization solution like VMWare Workstation running on your MAC can help in this case.

> Fault Isolation: We can run the new Linux kernel in a VM. If this VM kernel contains a bug, and crashes it will not crash the main host (OSX) thereby providing fault isolation and allow development and testing to continue.

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

   Srini decides to move the content to a Chord DHT. He splits the lectures into 10-second chunks, which results in 65,536 ($2^{16}$) files. He uses SHA3-256, a 256-bit hash, to generate the identifiers used in his DHT. Finally, he recruits 1,024 ($2^{10}$) users to participate in the Chord DHT as storage nodes.

   4(d)  How many hops does it typically take to lookup a single chunk?

   > log2(1024) = 10 hops

   4(e) How many different hosts are typically in the Chord finger table at any node?

   > log2(1024) = 10 hosts

### Mid 2012

> PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/midterm2012-solve.pdf>

1(d) UDP is better than TCP for streaming voice-over-IP data. (✅/❌)

> True. Losing some audio bits isn’t as bad as dealing with the delays from TCP’s retransmission.

1(e) UDP is better than TCP for RPCs that return medium-sized (100 KB) results. (✅/❌)

> False. 100KB is too big to fit in a single packet (64KB). The RPC system would just end up re-implementing much of what TCP does to split this data into packets and ensure that it is received reliably and reassembled. This would therefore be a poor idea.

1(f) RPCs provide different semantics from local calls because RPCs introduce a different class of errors. (✅/❌)

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

A. Spin loop

**B. Race condition**

C. Deadlock

Correct Explain briefly (1-2 sentences) where the bug is.

> bytes corresponds to some memory that is reused by ReadFromUDP. Thus, the slice to ProcessPacket could be overwritten while it is being processed.

4(h) LSP could be extended to be robust, with high probability, in the presence of corrupted UDP packets by appending a checksum to each message and dropping any that are received with an incorrect checksum. (✅/❌)

> True. The resending of messages will ensure that (eventually) a valid packet will be sent.

4(i) If a UDP packet gets delayed by several seconds, then the message it contains could be mistaken for one that occurs much later in the message sequence. (✅/❌)

> True. This can happen because sequence numbers wrap around.

6. (14 points) Three computers at CMU (A, B, and C) communicate using a protocol that implements the idea of Lamport clocks (they include their clock time stamp in messages). For reference, if you need a reminder, recall that the three rules of Lamport’s algorithm are:

   1. At process $i$, increment $L_i$ before each event.
   2. To send message $m$ at process $i$, apply Rule 1 and then include the current local time in the message, i.e., $\mathrm{send}(m, L_i)$.
   3. To receive a message $(m, t)$ at process $j$, set $L_j = \max(L_j, t)$ and then apply Rule 1 before time-stamping the receive event.

   At the beginning of time, all three computers begin with their logical clock set to zero (0). Later, the following sequence of events occurs:

   - A sends message $M_1$ to B: “hi”.
   - After sending $M_1$, A sends message $M_2$ to C: “hi”.
   - After receiving $M_1$, B sends message $M_3$ to C: “A told me hi”.
   - After receiving $M_3$ first and then $M_2$, C sends message $M_4$ to A: “B is boring”.

   6(a) Indicate the time included with the messages as they are sent at each step.

   ```
   Send(M1, _)
   Send(M2, _)
   Send(M3, _)
   Send(M4, _)
   ```

   > ```
   > Send(M1, 1)
   > Send(M2, 2)
   > Send(M3, 3)
   > Send(M4, 6)
   > ```

   6(b) Maintaining all clock states from the previous question, three ADDITIONAL messages are sent:

   - After receiving $M_4$, A sends message $M_5$ to B: “C is kind of random!”
   - After receiving $M_5$, B sends message $M_6$ to A: “C is boring”.
   - A receives message $M_6$.

   After all of these messages have been sent and received, what time does each computer think it is?

   | A    | 11   |
   | ---- | ---- |
   | B    | 10   |
   | C    | 6    |

   > Remember, receiving and sending are different events.
   >
   > ```text
   > initially: A=0, B=0, C=0
   > send(M1): A=1
   > send(M2): A=2
   > send(M3): A=2, B=3
   > send(M4): A=2, B=3, C=6
   > send(M5): A=8, B=3, C=6
   > send(M6): A=8, B=10, C=6
   > recv(M6): A=11, B=10, C=6
   > ```

   6(c) Is this a relatively or totally ordered system?

   > Solution: This is a relatively ordered system.

   6(d) Write out the vector time representation with the following messages as they are sent at each step.

   ```
   Send(M1, [ ])
   Send(M2, [ ])
   Send(M3, [ ])
   Send(M4, [ ])
   ```

   > ```text
   > Send(M1, [1, 0, 0])
   > Send(M2, [2, 0, 0])
   > Send(M3, [1, 2, 0])
   > Send(M4, [2, 2, 3])
   > ```

### Mid 2011

> PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/midterm2011_solve.pdf>

1(b) The checksum portion of an IP packet allows the receiver to both detect and correct a single-bit error in the packet. (✅/❌)

> False. Checksums can be used to detect errors, but not to correct them.

1(c) TCP’s reliable in-order byte stream abstraction can add unpredictable latency to messages under high packet loss. (✅/❌)

> True. Retransmission and in-order delivery can delay later bytes behind lost earlier bytes.

1(d) When creating a UDP connection to a server, the client and server will engage in a handshake protocol. (✅/❌)

> False. There is no setup phase with UDP

1(h) When making a synchronous RPC call, the caller will not return until after the requested operation has been completed, assuming no error is encountered. (✅/❌)

> True. A synchronous RPC blocks the caller until the remote call completes or an error is reported.

1(i) If the Lamport clock of event $e_1$ is less than the Lamport clock of event $e_2$, then there must be a chain of causal events by which $e_1$ precedes $e_2$. (✅/❌)

> False. Lamport clocks preserve the happens-before implication only in the forward direction; smaller timestamps do not prove causal ordering.

1(j) Global Positioning System (GPS) satellites use NTP to keep their clocks synchronized. (✅/❌)

> Solution: GPS satellites have their own atomic clocks. NTP would not provide sufficient accuracy for this application.

6. Three computers at CMU, A, B, and C communicate using a protocol that implements the idea of Lamport clocks (they include their clock timestamp in messages). For reference, if you need a reminder, recall that the three rules of Lamport’s algorithm are:

   1. At process $i$, increment $L_i$ before each event.
   2. To send message $m$ at process $i$, apply Rule 1 and then include the current local time in the message, i.e., $\mathrm{send}(m, L_i)$.
   3. To receive a message $(m, t)$ at process $j$, set $L_j = \max(L_j, t)$ and then apply Rule 1 before time-stamping the receive event.

   At the beginning of time, all three computers begin with their logical clock set to zero (0). Later, the following sequence of events occurs:

   - A sends message $M_1$ to B: “hi”.
   - After receiving $M_1$, B sends message $M_2$ to C: “A told me hi”.
   - After receiving $M_2$, C sends message $M_3$ to A: “B is boring”.

   6(a) Indicate the time included with the messages as they are sent at each step.

   ```
   Send(M1, _)
   Send(M2, _)
   Send(M3, _)
   Send(M4, _)
   ```

   > ```text
   > Send(M1, 1)
   > Send(M2, 3)
   > Send(M3, 5)
   > ```

   6(b) Maintaining all clock states from the previous question, three ADDITIONAL messages are sent:

   - After receiving $M_3$, A sends message $M_4$ to B: “C is kind of random!”
   - After receiving $M_4$, B sends message $M_5$ to A: “C is boring”.
   - A receives message $M_5$.

   After all of these messages have been sent and received, what time does each computer think it is?

   > A=10, B=9, C=5. Remember, receiving and sending are different events.

   6(c) Is this a relatively or totally ordered system?

   > This is a relatively ordered system.

   6(d) Reset all clocks to zero. This time:

   - A sends message $M_1$ to B.
   - The user of machine A is talking on the phone with the user of machine B. She tells him “I just sent you a message online. Please send a message to C right now.”
   - B sends message $M_2$ to C.

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

2. (8) For which of the following applications would UDP be preferable over TCP, ignoring annoying concerns such as firewalls that might block some protocols?

   A. Streaming a live video over the internet

   B. Instant messaging/email

   C. Logging in to your bank website

   D. Voice over IP

   E. Large file transfers

   F. Looking up a very small value from a directory service TCP / UDP

   > UDP, TCP, TCP, UDP, TCP, UDP

3. (11) Suppose each computer in a distributed system keeps an approximate real-time clock $R_i$ in addition to a Lamport-like clock $L_i$.

   A computer's real-time clock $R_i$ is an always-increasing integer (i.e., for any two reads $r_1$, $r_2$ of $R_i$ such that $r_1 \to_i r_2$, we have $r_2 > r_1$), but the real-time clocks at different computers may drift relative to each other (i.e., $R_j - R_i$ is non-constant for $j \ne i$).

   Consider the following modification, Shamport, to Lamport's partial-ordering algorithm:

   **Rule 1:** Before each event at computer $i$, set $L_i = \min(L_i + 1, R_i)$.

   **Rule 2:** When sending a message $m$, apply Rule 1 and include the time $L_i$ as part of the message (i.e., send $(m, L_i)$ instead of just $m$).

   **Rule 3:** When receiving a message $(m, t)$ at computer $j$, set $L_j = \max(L_j, t)$ and then apply Rule 1 before timestamping the message-arrival event.

   Let the Shamport global time of an event $e$ at computer $i$ be $S(e) = L_i(e)$.

   11(a) In the algorithm above, underline the difference between Shamport and Lamport's algorithm. (Underline as little as possible.)

   > Shamport's algorithm uses $L_i = \min(L_i + 1, R_i)$ in Rule 1 instead of $L_i = L_i + 1$. Otherwise the two algorithms are the same.

   11(b) Let $e, e'$ be two events at computer $i$ such that $e \to_i e'$. Prove that $S(e') > S(e)$.

   > The key observation is that any new event advances the logical clock.
   >
   > There are a couple common pitfalls to avoid:
   >
   > (1) $e$ and $e'$ are not necessarily consecutive events; other intervening events can affect the Shamport clock.
   >
   > (2) Events at computer $i$ include the local side of send and receive events, so you need to include possible applications of Rule 2 and Rule 3 in your proof.
   >
   > (3), reading the problem correctly to understand that the logical clocks $L_i$ here are not Lamport clocks, and thus you cannot blindly apply the rules for Lamport clocks from class.
   >
   > ---
   >
   > It suffices to prove the claim for two consecutive events \(f \to_i f'\) on computer \(i\), since the general case follows by chaining.
   >
   > > **Why?**
   > >
   > > Consider the sequence of all events $e \ldots e'$ at computer $i$.
   > >
   > > If $S(e') \le S(e)$ then there must exist at least one pair of $f \to_i f'$ such that $S(f') \le S(f)$; otherwise each new event would advance the logical clock $L_i$, which would yield $L_i(e') > L_i(e)$ and thus $S(e') > S(e)$.
   >
   > Let \(S(f)=t\), and let the real-time clock values at \(f,f'\) be \(r,r'\).
   >
   > Since every event timestamp is obtained after applying Rule 1, we have \(t \le r\).
   >
   > Since \(R_i\) is always increasing and \(f \to_i f'\), we have \(r'>r\), hence \(r'>t\).
   >
   > (1) If \(f'\) is a local or send event, then
   > $$
   > S(f')=\min(t+1,r').
   > $$
   > Both \(t+1\) and \(r'\) are \(>t\), so \(S(f')>t=S(f)\).
   >
   > (2) If \(f'\) is a receive event with message timestamp \(t_m\), then
   > $$
   > S(f')=\min(\max(t,t_m)+1,r').
   > $$
   > Here \(\max(t,t_m)+1>t\) and \(r'>t\), so again \(S(f')>S(f)\).
   >
   > Thus every consecutive event increases \(S\), so for any \(e\to_i e'\), \(S(e')>S(e)\).

   11(c) Draw a time-series diagram in which $S(\mathrm{send}(m)) > S(\mathrm{receive}(m))$ for some message $m$. Be sure to compute the Shamport-time and label the values of the real-time clocks at all computers for any events in your diagram. Explain in 1-2 sentences why this unwanted behavior occurs.

   <img src="assets/image-20260504010119299.png" alt="image-20260504010119299" style="zoom:50%;" />

   >  **The fundamental problem is that the logical clock will never advance past the real-time clock** at each computer, so skew in the real-time clocks can cause the receive to be timestamped earlier than the send.

   11(d) Suppose we know that the one-way latency of any message between any two computers $i, j$ is at least $x$ clock-ticks by any local clock. Also suppose we can synchronize $R_i$ and $R_j$ using an external time-source such that $|R_i - R_j| \le y$, always, for some integer $y$. Is there a value of $y$ small enough to guarantee that $S(\mathrm{send}(m)) < S(\mathrm{receive}(m))$ for any message $m$ between $i$ and $j$? If yes, compute the largest possible value of $y$ to guarantee this property, and explain why your answer is correct. If no, explain why.

   > Yes, if $y < x$.
   >
   > Consider a diagram similar to the part above, but with $\mathrm{send}(m)$ at $(t, r)$ and $\mathrm{receive}(m)$ at $(t', r')$.
   >
   > To prove: $$t' > t$$
   >
   > Because the propagation delay of $m$ is at least $x$ clock-ticks and the clock-skew is at most $y$, we have $r' \ge (r - y) + x$ and therefore that $r' > r \ge t$ if $x - y > 0$. Rule 3 is applied to timestamp the receive event, yielding $t' = \min(\max(l, t) + 1, r')$, where $l$ was the value of the logical clock before receiving $m$. Because $\max(x, t) + 1 > t$ and $r' > t$, we have $t' > t$ and therefore that $S(\mathrm{receive}(m)) > S(\mathrm{send}(m))$.

### Final 2009

> PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/final2009-solve.pdf>

1. Which techniques are used in DNS to improve scalability?

   A. Replication

   B. Recursive queries

   C. Caching / Soft-State

   D. Partitioning of namespace

   > A, C, D

2. Which of the following are true about the Chord distributed hash table?

   A. Has $O(\log N)$ lookup latency.

   B. Directly supports fuzzy or wildcard lookups for content.

   C. Uses content-based naming.

   D. Provides anonymity.

   > A, C

3. Which of the following are commonly provided in RPC libraries?

   A. Application-level failure handling

   B. Data marshalling/unmarshalling

   C. Asynchronous function calls

   D. Exactly-once semantics

   E. At-most-once semantics

   > B, E

4. Which of the following are advantages of using content-based naming for P2P file transfers?

   A. The receiver can download a chunk using parallel TCP streams.

   B. The receiver can route around failed links.

   C. The receiver can download a chunk of data from any source, not just the original seed.

   D. The receiver can verify that it received the correct data.

   > C, D

5. Which of the following statements are true? Please circle True or False:

   6(a) In Google File System (GFS), when a client needs to access data, it contacts the master and gets the data from the master. (✅/❌)

   > False

   6(h) Recall the global “happens-before” relationship ($\to$) that captured the logical notions of time using both the local happens-before relationship at each server and the fact that a message must be sent before it can be received.

   For a Lamport logical clock $L$, if $e_1 \to e_2$ then $L(e_1) < L(e_2)$. (✅/❌)

   > True

### Final 2010

> PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/final2010-solve.pdf>

1.

   Threads and Processes

   - It is less expensive to create a process than a thread.  (✅/ ❌ )
     > False. Creating a process is usually more expensive because it needs a separate address space and more OS bookkeeping.

   - Switching between threads is faster than switching between processes.  (✅/ ❌ )
     > True. Thread switches are usually cheaper because threads in the same process share the same address space.

   - In order to switch between user threads, you need to enter the kernel.  (✅/ ❌ )
     > False. User-level threads can be switched entirely by a user-space thread library without entering the kernel.

   - Threads share a heap and a stack.  (✅/ ❌ )
     > False. Threads share the heap, but each thread has its own stack.

   Networking

   - The TCP initial handshake must be completed between the sender and every router on the path to the destination before communication can take place.  (✅/ ❌ )
     > False. TCP is end-to-end between the sender and receiver; routers only forward packets.

   - The Internet service model allows a small amount of packet loss.  (✅/ ❌ )
     > True. The Internet provides best-effort delivery, so end hosts must tolerate packet loss.

   - Domain Name Service (DNS) servers remember which clients have cached DNS replies so that the servers can send invalidation messages when name bindings change.  (✅/ ❌ )
     > False. DNS cache consistency is mainly handled using TTLs, not server-pushed invalidations.

2. Which of the following design assumptions apply to HDFS/GFS? (Circle all that apply)

   A. Only amazingly powerful servers can handle the size and complexity of the workload.

   B. Any use of a centralized server would cause too much of a bottleneck.

   C. Component failures are expected.

   D. Files are huge by traditional standards.

   E. File contents are often updated and overwritten.

   > C, D.

4. (4) Suppose the above Chord setup:

   <img src="assets/image-20260504013038008.png" alt="image-20260504013038008" style="zoom:67%;" />

   - At what node do you expect to find key 10?
   - At what node do you expect to find key 9?
   - On average, how many hops are there when searching for a key?
   - What route will a search for key 11 take, starting at node 3?

   > Key 10 maps to $n_0$, and key 9 maps to $n_9$. Chord lookups take $O(\log N)$ hops on average. Starting at $n_3$ for key 11, the lookup goes $n_3 \to n_9 \to n_0$.

4. (5) Suppose you want to build a large distributed system to store cookie recipes. Each cookie is stored using the recipe’s name (“Grandma’s Arsenic Cookie Surprise”). Unlike many P2P systems, in this one, the recipe data is small, so you wanted to store the actual data in the P2P system instead of leaving it on the original nodes. A friend says “Hey, I hear that Chord is very efficient – it doesn’t take many lookups to find the node containing the data.” Explain to your friend why directly throwing this data into a DHT such as chord, with `key = recipe name, value = recipe data`, is a really bad design decision. Brief - two sentences or so.

   > Chord only supports exact-key lookup well, while recipe users are likely to search by partial names, ingredients, or categories. Hashing recipe names also destroys locality, so related recipes cannot be found together without building a separate index.

   (6) Tell us what style of P2P system you would use, and what assumptions you think are reasonable for your cookie-storing-system:

   - Number of nodes
   - Number of recipes
   - Number of queries/second
   - What do queries look like?

   Style of system AND a brief rationale for this decision:

   > I would use a **Gnutella/KaZaA-style two-level P2P system**.
   >
   > Assumptions: tens of thousands of nodes, millions of small recipes, moderate query load, and queries are mostly keyword/ingredient/category searches rather than exact recipe-name lookups.
   >
   > Ordinary peers store replicated recipe data and report their recipes to supernodes. Supernodes maintain temporary indexes and search among themselves, which supports flexible recipe search better than Chord while avoiding the cost of flooding every query to all peers.

11. (11) Consider a system with four machines that uses Lamport timestamps for logical ordering. Let $L_i(m_j,\mathrm{send})$ be the Lamport logical time for machine $i$ sending message $j$, and let $L_i(m_j,\mathrm{recv})$ be the Lamport logical time for machine $i$ receiving message $j$. Each local clock is initialized to $0$. Answer the questions below based on these timestamps:

    ```text
    L_1(m_1, send) = 1
    L_1(m_2, send) = 2
    L_2(m_1, recv) = 2
    L_3(m_2, recv) = 3
    L_2(m_3, send) = 3
    L_3(m_4, send) = 4
    L_3(m_3, recv) = 5
    L_4(m_4, recv) = 5
    L_4(m_5, send) = 6
    L_1(m_5, recv) = x
    L_4(m_6, send) = 7
    L_1(m_7, send) = 8
    L_3(m_7, recv) = 9
    L_3(m_6, recv) = 10
    ```

    What is the value of $x$? If it cannot be determined, write "unknown".

    > $x = 7$. Message $m_5$ is sent by machine 4 with Lamport time 6, and machine 1's local clock before receiving it is 2, so the receive timestamp is $\max(2, 6) + 1 = 7$.

12. (12) For the following, circle which event happened first. If it cannot be determined, circle "unknown."

    | Option 1 | Option 2 | Unknown |
    | -------- | -------- | ------- |
    | $L_1(m_1,\mathrm{send})$ | $L_4(m_5,\mathrm{send})$ | unknown |
    | $L_2(m_3,\mathrm{send})$ | $L_3(m_4,\mathrm{send})$ | unknown |
    | $L_3(m_4,\mathrm{send})$ | $L_3(m_3,\mathrm{recv})$ | unknown |
    | $L_2(m_3,\mathrm{send})$ | $L_4(m_6,\mathrm{send})$ | unknown |
    | $L_4(m_6,\mathrm{send})$ | $L_1(m_7,\mathrm{send})$ | unknown |

    > <img src="assets/lamport_sequence_equal_spacing_clear2.png" alt="lamport_sequence_equal_spacing_clear2" style="zoom: 33%;" />
    >
    > $L_1(m_1,\mathrm{send})$; unknown; $L_3(m_4,\mathrm{send})$; unknown; unknown.

### Final 2011

> PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/final2011-solve.pdf>

1. (8 points) Circle True or False as appropriate. If you don’t know the answer, come back at the end and GUESS; a blank answer is the same as a wrong answer, so guessing can only help.

   1(a) DNS is delegated hierarchically by having the root nodes tell resolvers which servers to query for `.com`, and so on, until the client’s query can be answered. (✅/❌)

   > True.

   1(b) DNS resolvers use Paxos and invalidation messages to maintain the consistency of cached records. (✅/❌)

   > False.

   1(c) Some Content Delivery Networks (CDNs) use DNS responses to direct clients to the closest CDN cache. (✅/❌)

   > True.

2. Peer to Peer

   6(a) In a centralized P2P network (such as Napster), how many indices must be searched if a client wants to locate a particular file?

   > 1

   6(b) Name one major disadvantage of the centralized P2P system (from a distributed principles point of view)

   > - Single point of failure
   > - Server processes everything
   > - Server must keep track of a potentially very large number of clients
   > - more? (Copyright, no scalability)

   6(c) Query flooding is an alternative design that solves some of the problems of centralized P2P and eliminates the central server. However, it changes the mechanics of peer interactions significantly. Explain, in one sentence each, how a newly joining node publishes the files they wish to make available:

   - In a centralized P2P network
   - In a query-flooding P2P network

   > They send their list of files and metadata to the server.
   >
   > A query flooding p2p network: They don’t do anything - queries come to them.
   >

   6(d) One popular improvement upon query flooding is to move to a “supernode” flooding architecture. Using $N$ as the number of nodes in the network and $S$ as the number of supernodes, where $S \ll N$, explain the benefit of moving to this supernode architecture.

   > Queries now require $O(S)$ messages instead of $O(N)$. In addition, if the nodes used as supernodes are more stable or have higher capacity, they can further improve the performance or stability of the network.

   6(e) What is a common mechanism used to limit the propagation of queries in a flooding network?

   > TTL - time to live - scoping. Also known as hop count limits, etc.

   6(f) List one typical criterion for selecting a node to be promoted to a supernode. Explain in one sentence why such a choice would improve network stability.

   > How long a node has been part of the network (time), because how long a node has been around is a good predictor of how long it will be around.

7. Consistent Hashing

   7(a) In a distributed hash table (DHT) using a ring mapping, explain how a key is mapped to a specific node?

   > Keys and nodes map to points in a ring space. A node handles all keys mapped between Predecessor and it.

   7(b) In the most basic form of DHT systems, nodes simply track their predecessor and successor. Very briefly state what problem this leads to as the network grows larger.

   > Performance problems as nodes forward a key resolution request to larger chains of neighbors.

   7(c) The Chord scheme overcomes this problem by having each node maintain a “finger table”. Given starting node $j$ and destination node $k$, where $k > j$, how much is the distance between the two nodes reduced with each hop?

   > It decreases exponentially, or it is cut in half

   7(d) In a Chord structured DHT with $N$ nodes, how many hops would a lookup operation require?

   > $O(\log N)$.

   7(e) Assume a Chord network in which node $q$ is the successor of node $p$. During operation, node $p$ discovers that its successor link is no longer consistent because $q$ has updated its predecessor link. What does this change imply must have happened in the network?

   > A new node joined the network ’between’ p and q.

   7(f) An optimization to Chord involves storing several nodes for each entry in the finger table instead of just one. Explain an important benefit this optimization confers in a globally distributed DHT.

   > (1) This allows routing based on proximity, which would reduce slow routes that criss-cross the globe.
   > (2) It provides a fallback in case one of the nodes in the finger table is unreachable.

## UW CSE 461 Computer Networks

### Sample Mid 2

> PDF: <https://courses.cs.washington.edu/courses/cse461/23sp/samples/sample-midterm2-key.pdf>

1(a) How are hosts with two different link layers (e.g., WiFi and Ethernet) able to communicate?

> Layering lets the IP layer decapsulate data from one link layer and encapsulate it in another.

1(d) What is the primary approach used to divide network functionality in the Internet?

> Layering.

1(e) Consider a protocol stack composed of WiFi, IP, TCP, and HTTP. Illustrate what the packet on the wire looks like for this stack.

> HTTP is encapsulated by TCP, then by IP, then by WiFi.

3(a) What is ICMP used for?

> Sending back error reports.

3(b) Describe two advantages and two disadvantages of NAT.

> Advantages: NAT counters IPv4 address shortage and can filter some unwanted inbound packets.
>
> Disadvantages: outside hosts cannot directly connect to inside hosts without a table entry or explicit forwarding rule, and NAT breaks or complicates peer-to-peer applications and protocols that embed IP addresses in payloads.

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

> Distance-vector routing exchanges shortest-path information with neighbors.
>
> Link-state routing exchanges topology information.
>
> Distance-vector converges more slowly but is computationally simpler.

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

12-13 Bandwidth Allocation. Four flows A, B, C, and D share a 10 Mbps link.

Demands are A=1 Mbps, B=2 Mbps, C=10 Mbps, and D=infinite.

What is the max-min fair allocation?

> Flow A: 1 Mbps. Flow B: 2 Mbps. Flow C: 3.5 Mbps. Flow D: 3.5 Mbps.

15-16: AIMD. A 10 Mbps link is shared by flow A, capped at 3 Mbps, and flow B, with infinite demand. Each RTT increases rate by 1 Mbps if uncongested and halves the rate if congested. Starting from A=2 Mbps and B=20 Mbps, what are the rates after 1, 2, and 3 RTTs?

> After 1 RTT: A = 1 Mbps, B = 10 Mbps. After 2 RTTs: A = 0.5 Mbps, B = 5 Mbps. After 3 RTTs: A = 1.5 Mbps, B = 6 Mbps.

53-54: Link-State Routing. C receives contradictory LSPs: one from A says the A-B link is down, but one from B says the A-B link is up.

<img src="assets/image-20260504102610677.png" alt="image-20260504102610677" style="zoom:25%;" />

How could this happen, and what should C do?

> This can happen if one LSP was sent before the A-B link changed and the other was sent after it changed.
>
> C should keep flooding and recomputing from the newest LSPs; eventually the old LSP will be superseded and both sides will agree again.

## Princeton COS 461 Computer Networks

### Spring 2012 Mid

> PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring12-cos461-exam1-answers.pdf>

1 A router has a 100,000-byte FIFO buffer, with an upload bandwidth of 1 Mbps or 125,000 bytes per second. MTU = 1000 bytes.

1(a) If the buffer is completely full of TCP acknowledgment packets, how many packets are queued in the buffer? Assume **the TCP segment has no payload**, and the packet headers do not contain any IPv4 or TCP options. (3 points)

> Ignoring the link-layer header and any minimum size restriction on the link-layer frame, a TCP ACK packet is 40 bytes long, consisting of a 20-byte IP header and a 20-byte TCP header. A 100,000-byte buffer can hold $100000/40 = 2500$ ACK packets.
> **Why the TCP segment has no payload?**
>
> TCP header already has a Sequence Number (32) and an Acknowledgment Number (32).

1(b) Suppose the buffer is completely full. How long does it take the router to transmit all of the bytes in the buffer? (3 points)

> Sending 100,000 bytes at 125,000 bytes/sec requires $100000/125000 = 0.8$ seconds, or 800 msec.

1(c) Suppose the router supports two first-in first-out queues, one for interactive applications (like Voice over IP) and the other for all remaining traffic, with static priority for the queue handling interactive traffic. If a VoIP packet arrives when the queue for interactive applications is empty, what is the maximum time before the router starts transmitting the VoIP packet? (Assume that the router does not preempt any ongoing packet transmission.) (4 points)

> At worst, the VoIP packet arrives just as the router starts transmitting a full-sized (i.e., 1000-byte) non-VoIP packet, forcing the VoIP packet to wait for $1000/125000 = 0.008$ seconds, or 8 msec.

2. Host A initiates a TCP connection with host B by sending a SYN packet, and B responds with a SYN-ACK packet. Upon receiving the SYN-ACK packet, A responds with an ACK packet.

2(a) What is the earliest time that A can start sending data to B?

A. Immediately after sending the SYN packet to B

B. Immediately after receiving the SYN-ACK packet from B

C. Immediately after receiving data from B

> B. Once the SYN-ACK arrives, A knows that B has A's initial sequence number and is ready to accept data packets from A.

2(b) What is the earliest time that B can start sending data to A?

A. Immediately after receiving the SYN packet from A

B.  Immediately after sending the SYN-ACK packet to A

C.  Immediately after receiving the ACK packet from A

D. Immediately after receiving data from A

> C. Once the ACK arrives, B knows that A has B's initial sequence number and is ready to accept data packets from B.

2(c) Suppose the ACK packet from A gets lost. What ultimately triggers A to retransmit the lost ACK packet? Assume no other packets get lost and no data packets are sent.

A. A retransmission timeout at A

B. A retransmission timeout at B, triggering a retransmission of the SYN-ACK packet

> B. ACK packets are not retransmitted by themselves, so A does not experience a retransmission timeout for the lost ACK. If B does not receive an ACK for the SYN-ACK, then B will retransmit the presumed-lost SYN-ACK after the retransmission timeout expires.

3. A small university campus is assigned a large address block 12.1.0.0/17, but is only using a portion of these addresses (in 12.1.1.0/24) to number its computers. The campus uses a single Internet Service Provider (ISP) to reach the rest of the Internet. This picture shows the forwarding tables on the ISP’s router (on the left) and the campus edge router (on the right):

   <img src="assets/image-20260504105204357.png" alt="image-20260504105204357" style="zoom:33%;" />

   For example, the ISP forwards all packets with destination addresses in 12.1.0.0/17 out link #2 toward the campus edge router. Both routers include a default forwarding entry 0.0.0.0/0 that can match any destination IP address.

3(a) How many IP addresses does the campus “own” in its 12.1.0.0/17 block? You can represent your answer as a power of two. (2 points)

> The 17-bit mask leaves $32 - 17 = 15$ bits to identify the addresses within the block. As such, the block contains $2^{15} = 32{,}768$ addresses.

3(b) What are the smallest and largest IP addresses that the campus owns in the block?

> 12.1.0.0 through 12.1.127.255.

3(c) Suppose the ISP router receives a packet with destination IP address 12.1.1.1? What path does this packet follow? (2 points)

> The packet flows over the path $1 \to 2 \to 3 \to 4$.

3(d) Suppose the ISP router receives a packet with destination IP address 12.1.20.1? What path does this packet follow? (2 points)

> The packet flows over the path $1 \to 2 \to 3 \to 2 \to 3 \to \cdots$.

3(e) What ultimately happens to a packet with destination IP address 12.1.20.1? Where does it go? (2 points)

> The looping packet is discarded once its IP TTL expires.

4(b) Consider the network below that runs a link-state routing protocol that computes shortest paths as a sum of link weights. The number on each link is the weight of the link in each direction (e.g., links b-c and c-b both have weight 2). Suppose nodes a, b, and d send packets to destination node c. If link d-c (and c-d) fails, which of nodes a, b, and d could conceivably see their packets stuck in a temporary forwarding loop? Which ones would not? (3 points)

<img src="assets/image-20260504105555525.png" alt="image-20260504105555525" style="zoom:33%;" />

> a and d can loop, but not b

4(c) Using the same figure as 4(b), suppose the network operator is taking link d-c (and c-d) down for planned maintenance. The network operator wants to temporarily set the weight of the link to a higher value, to coax nodes to move away from paths that use the link without creating any blackholes or loops. What minimum sequence of weight settings for link d-c avoids blackholes or loops during planned maintenance?

> First change the d-c cost to 3 so node a shifts to the upper path.
>
> Then change the cost to 5 or higher so node d shifts to the upper path.
>
> Finally shut down d-c after nobody is using it.

5. This question concerns the relationship between socket calls at the application layer and the behavior of the transport layer. Consider a reliable stream (i.e., TCP) socket between application processes A and B running on two different hosts.

5(a) Suppose process A calls send() to send 10,000 bytes of data, and the operating system begins sending the data as a sequence of packets destined to B. If process A calls close() on the socket before the operating system finishes transmitting the data, will the remaining data be sent to B? Why or why not? (3 points)

> Yes. The operating system continues transmitting the remaining data to B to ensure ordered, reliable delivery of the byte stream.
>
> 因为`close()` 的语义是“我（进程 A）没有更多数据要发送了”

5(b) Suppose process A calls close() after the operating system has transmitted all of the outstanding data. What kind of packet does the operating system send in response to A’s call to close()? (2 points)

> TCP FIN packet

5(c) Explain why B may need to perform multiple calls to `recv()` to receive all 10,000 bytes of data from A. (3 points)

> The data may not reach B in its entirety at the same time, since it is split into multiple packets. These packets may experience different delays due to congestion, retransmission, and receive-window constraints.
>
> 因为`recv(10000)` 的意思是“我最多想读 10,000 字节”，但如果此时内核里只有 500 字节，它会立即返回这 500 字节，剩下的需要再次调用 `recv()` 去拿。

5(d) Suppose B’s operating system has learned that A has closed its end of the connection. Once process B has read all of the data from A, what does B’s next call to `recv()` return? (2 points)

> A 0, indicating the end of the stream.

6. An IP address relates to a host’s location in the Internet topology, but is not easily translated to a precise geographic location. This question concerns mapping an IP address to a location.

6a) Give two examples of how knowing a client’s rough geographic location can improve an Internet service.

> - Customizing the content to the user’s location (e.g., showing weather, advertisements, traffic reports, etc. related to the user’s presumed location)
> - Blacking out access to sites disallowed in certain geographic regions (e.g., due to local laws, commercial restrictions on showing sporting events in the local area, etc.)
> - CDN: Directing clients to the closest Web server offering a given service.

6b) Propose a technique to infer the geographic location associated with an IP address, without cooperation from the end user. Explain how your technique works, and what assumptions it makes.

> - Performing a traceroute to the client address, and looking for geographically-meaningful names late in the traceroute path (e.g., “yale-univer.car2.stamford1.level3.net”)
> - Performing pings to measure latency to reach the client from multiple vantage points with known geographic locations, and triangulating to infer the client’s location - Altering the design of the routing system to include geographic information (though this requires substantial control over the entire Internet, making this approach unrealistic in practice)
> - Performing a reverse DNS lookup on the client IP address (though most client’s don’t have DNS names, and these names often don’t reveal location information), or performing a “whois” query to find the address of the organization that owns the IP address

6c) Give an example where your technique will not produce accurate results.

> - If the client lies at the end of a high-latency link (e.g., a satellite)
> - If routers near the client do not participate in traceroute (e.g., do not send ICMP responses)
> - If the client’s machine does not respond to ping requests
> - If the organization in whois covers a very large geographic region (e.g., the address of corporate headquarters may not reveal the client’s location all that accurately)
> - Tunnelling like VPN 1)  Encapsulate the client’s traffic in a tunnel to a server in a different location 2) false the ping measurement 3) hide from traceroute 4) false the whois information

7. Some WiFi hotspots offer wireless access for a fee. When a user connects to the access point, a DHCP server assigns them an IP address, network mask, gateway router, and local DNS server. When the user tries to access a Web site, the hotspot directs the HTTP request to a “pay wall” where the user can enter credit card information, and only then can the user access the requested Web site. These hotpots typically allow DNS queries through the pay wall, though, since the user’s Web browser needs to use DNS to map domain names to IP addresses.

7(a) Suppose, before the user pays, the hotspot only allows the user to send and receive UDP packets with source or destination port 53 (the port number used for DNS). Assume the hotspot allows any such traffic to travel to and from the user, independent of the destination IP address. Briefly describe the design of a system that would allow the user to access arbitrary sites on the Internet via the hotspot without paying. The user may need to deploy parts of the system ahead of time. Include a picture. (5 points)

> The user can run a proxy that listens on UDP port 53. The client can encapsulate an IP packet (say, containing a TCP segment) inside UDP packets sent to the proxy, and the proxy can send the traffic to arbitrary Internet services at the client’s request. The responses can be encapsulated and sent back to the client using UDP packets with port 53.
>
> To ensure reliability, the client and the proxy can acknowledge received UDP packets and retransmit unacknowledged packets.
>
> ```
> Before payment:
>
> User laptop
> +-------------------+
> | Browser           |
> | wants google.com  |
> +---------+---------+
>           |
>           | TCP/IP packet
>           v
> +-------------------+
> | Local tunnel app  |
> | encapsulate TCP   |
> | into UDP dst 53   |
> +---------+---------+
>           |
>           | UDP packet, dst port 53
>           v
> ================================================
>  Hotspot pay wall
>  Allows UDP traffic with src/dst port 53
> ================================================
>           |
>           v
> +--------------------------+
> | User's proxy on Internet |
> | listens on UDP port 53   |
> | decapsulates packet      |
> | forwards to real site    |
> +------------+-------------+
>              |
>              | normal TCP/HTTP/HTTPS
>              v
>         Arbitrary website
> ```

7(b) Now suppose that the hotspot only allows DNS queries (i.e., correctly formed DNS requests sent to UDP port 53) destined to the IP address of its own local DNS server, and DNS responses from that server. Design a new solution that allows the user to access arbitrary Internet sites without paying. Include a picture. Note that you should not use this technique in real life to evade paying for Internet service! (5 points)

> The user can run a proxy that acts as an authoritative DNS server for a domain the user has registered (say, jrex.com). To communicate with the proxy, the client sends a DNS request to the hotspot’s local DNS server, with the contents of the message embedded in the domain name (e.g., here-is-my-message.jrex.com). This will trigger the local DNS server to direct the query to the jrex.com authoritative server, which can encode a message in the DNS response (e.g., using the four bytes of the IP address to encode four characters, or using DNS TXT records to encode more information. As in the previous question, the client and the proxy need to acknowledge and retransmit the UDP packets to ensure reliable delivery. The domain names could even embed sequence and acknowledgment information (e.g., here-is-mymessage-X.jrex.com, where X is a number). This class of solutions is known as “DNS tunneling.”
>
> ```
> User laptop
> +-------------------+
> | Local tunnel app  |
> | encodes message   |
> | into domain name  |
> +---------+---------+
>           |
>           | DNS query:
>           | abc123.seq5.jrex.com
>           v
> ================================================
>  Hotspot pay wall
>  Only allows DNS query to local DNS server
> ================================================
>           |
>           v
> +-----------------------+
> | Hotspot local DNS     |
> | does recursive lookup |
> +----------+------------+
>            |
>            | query for *.jrex.com
>            v
> +-----------------------------+
> | User's authoritative DNS    |
> | server for jrex.com         |
> | decodes message             |
> | acts as proxy               |
> +-------------+---------------+
>               |
>               | normal Internet access
>               v
>         Arbitrary website
> ```
>
> 问题：
>
> - 低带宽，高延迟，DNS cache，异常流量
>
> Several students offered a different answer that was also valid. The idea is to hijack the hotspot’s local DNS server by sending a forged ARP response for the DNS server’s IP address, learned by the client in DHCP bootstrapping. Now the client can send UDP port 53 packets, and follow the approach in part 7a of the question. Note that this approach may be easier for the hotspot administrators to detect, since the local DNS server would suddenly be carrying no traffic. (That said, even the solution above is relatively easy to detect if the hotspot administrators are monitoring DNS query/response loads on a per-client basis.)
>
> 其他假设：
>
> - 不检查 source IP 是否属于这个 MAC
>
>   > ```
>   > Ethernet src MAC = attacker MAC M_A
>   > IP src           = DNS server IP D
>   > UDP port         = 53
>   > ```
>   >
>   > gateway 检查 `IP D 是否真的属于 MAC M_A？` 就完蛋了
>
> - 不启用 DHCP snooping / IP source guard / dynamic ARP inspection
>
> - firewall 只粗略看 IP/port，而不严格验证 DNS 语义
>
>   > 若
>   >
>   > ```
>   > 1. 必须是合法 DNS query / response
>   > 2. query name 长度和字符正常
>   > 3. response 必须对应之前的 query
>   > 4. 不允许异常大的 TXT record
>   > 5. 不允许高频率、长随机子域名
>   > ```
>
> ```
> Before attack:
>
> +----------------+                      +----------------+
> | Unpaid client  |                      | Real DNS server|
> | IP = C         |                      | IP = D         |
> | MAC = M_C      |                      | MAC = M_D      |
> +-------+--------+                      +-------+--------+
>         |                                       ^
>         | DNS query to D                        |
>         v                                       |
> +----------------+                             |
> | Hotspot gateway|-----------------------------+
> | ARP: D -> M_D  |
> | Policy:        |
> | only allow DNS |
> | with server D  |
> +-------+--------+
>         |
>         v
>      Internet
>
> ---
>
> ARP spoofing:
>
> Attacker tells gateway:
> "DNS server IP D is at my MAC M_C"
>
> +----------------+
> | Unpaid client  |
> | MAC = M_C      |
> | spoofs IP = D  |
> +-------+--------+
>         |
>         | IP src = D
>         | UDP src/dst port = 53
>         | dst = remote proxy P
>         v
> +----------------+
> | Hotspot gateway|
> | ARP: D -> M_C  |
> | thinks packet  |
> | is from DNS D  |
> | so allows it   |
> +-------+--------+
>         |
>         v
> +----------------+
> | Remote proxy P |
> | on Internet    |
> +----------------+
> ```
>
> Other students offered another answer that was also valid. The client could snoop on DHCP, ARP, or flooded packets to learn the IP addresses of other users who have (presumably) paid for service. The client can then send a forged ARP response for another client’s IP address, and be able to receive packets sent to that address. The client can start sending packets from that address, too, allowing free communication. (This might be detected by the other user, and in fact that user may sometimes send traffic, causing the switches to shift traffic back to the old client. As such, the crafty client would need to repeatedly hijack the original client.)
>
> ```
> Normal case:
>
> Paid user
> +-------------+
> | IP = P      |
> | MAC = M_P   |
> +------+------+
>        |
>        | normal traffic
>        v
> +----------------+
> | Hotspot gateway|
> | P has paid     |
> +----------------+
>        |
>        v
>    Internet
>
> ---
>
> ARP spoofing:
>
> Attacker says to gateway:
> "paid user's IP P is at my MAC M_A"
>
> +----------------+
> | Hotspot gateway|
> | ARP table:     |
> | P -> M_A       |
> +-------+--------+
>         |
>         | packets for paid user IP P
>         v
> +----------------+
> | Attacker laptop|
> | MAC = M_A      |
> | spoofs IP = P  |
> +-------+--------+
>         |
>         | traffic appears to come from paid IP P
>         v
>     Internet
> ```

### Spring 2012 Final

> PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring12-cos461-exam2-answer.pdf>

1(a) The Skype peer-to-peer IP telephony application sometimes has a user machine serve as a “super node” to support communication between two other users. When are super nodes needed, and why? (3 points)

> Traversing NATs and firewalls, particularly when both peers lie behind a NAT/firewall that blocks unsolicited traffic from external hosts. Super nodes are also useful for discovering the remote peer.

1(b) Microsoft recently bought Skype. Earlier this month, Microsoft announced that they will replace the classic super nodes with their own super nodes running in Microsoft data centers. Give one reason why Microsoft might have made this decision? (2 points)

> To improve performance and reliability by ensuring super nodes have sufficient resources and predictable operation.

1(c) To prevent free-riding, a BitTorrent peer rates other peers in terms of the download rate they offer, and then decides how much to offer in return. Suppose six users offer data at rates of 10, 4, 8, 3, 7, and 5 Mbps, respectively, and the peer has 15 Mbps of upload bandwidth. What upload rate does it offer to each of the six peers? (3 points)

> The peer uploads with $1/N$ of its bandwidth to the top $N$ peers, where $N=4$ by default. So, the upload rates are $15/4$, 0, $15/4$, 0, $15/4$, $15/4$ Mbps.

1(d) Under the same scenario as question 1(c), suppose peer #1 (currently offering a download rate of 10 Mbps) decides to be more strategic. What is the minimum rate that peer #1 could offer and still achieve the same upload rate it received in question 1(c)? (2 points)

> Just slightly above the fifth peer, or just above 4 Mbps.

3a) Traceroute can sometimes return a path that does not even exist in the Internet topology. E.g., hop i may not be connected to hop i+1. Give one reason why this might happen.

> A routing change during the traceroute probe
>
> Load balancers that spread traffic over multiple paths

4(a) Many enterprise networks only allow registered machines to access the local area network. Some of these networks configure the DHCP server to assign a computer (or MAC address) the same IP address every time it connects to the network. Give one reason why. (3 points)

> Tracking traffic by IP address is much easier if an IP address corresponds to the same user at all time.

4(b) What is the disadvantage of associating each registered MAC address with a pre-determined IP address? (3 points)

> Running out of IP addresses when the number of potential users grows large, even if these users are not active at the same time. Less opportunity for subdividing the topology into separate IP prefixes for more scalable routing.

4(c) To send an IP packet to another host on the same local area network, the sending host first checks its local ARP cache to determine the MAC address associated with the destination IP address. On a “miss” in the ARP cache, the sending host sends an ARP request for the destination IP address and buffers the packet, awaiting a response. Suppose, instead, the host issues the ARP request and simultaneously drops the IP packet. Name one advantage of this approach? (2 points)

> The sending host does not need to buffer the packet until receiving the ARP response. This reduces the memory requirements on the sender, and obviates the need to match the ARP response with some arbitrary packet sitting in a buffer.

4(d) What is one disadvantage of the approach in 4(c)? (2 points)

> The dropped packets must be retransmitted at a higher layer (e.g., TCP). E.g., a dropped SYN packet, in particular, would have a long retransmission timeout.

### Spring 2011 Mid

> PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring11-cos461-exam1-answers.pdf>

1. Routing, addressing, and tunneling

<img src="assets/image-20260504115546375.png" alt="image-20260504115546375" style="zoom:50%;" />

The above figure shows a network topology. The LAN on the left uses a NAT to connect to the Internet and includes a client host H1. The LAN on the right includes a webserver H2. Packets between the two endpoints are routed along the path shown by a heavy dark lines, which includes two IPv4 tunnels. All packets which traverse the path use both tunnels. The various network interfaces have IP and MAC addresses as shown.

H1 has established an HTTP session with web server H2 and data packets are flowing between the two machines. As an example, we have filled in the headers for packet 1 (traveling from the server H2 to the client H1). Note that you should order your headers from “outermost” in, as shown: Ethernet should be listed before IP, because the Ethernet packet exists first on the wire.

| Header Type | Source  | Destination |
| ----------- | ------- | ----------- |
| Ethernet    | MAC 16  | MAC 15      |
| IP          | 3.0.1.2 | 1.2.3.4     |

You only have to fill in the header type and the source and destination address for the network and datalink layer headers for packets 2, 3, and 4 (these packets are all traveling from the client H1 to the server H2, as marked on the figure with heavy black arrows and numbers). Note: You might not need to use all the rows supplied.

1(a) Header for packet 2.

| Header Type | Source   | Destination |
| ----------- | -------- | ----------- |
| Ethernet    | MAC 1    | MAC 2       |
| IP          | 10.0.0.2 | 3.0.1.2     |

1(b) Header for packet 3.

| Header Type | Source  | Destination |
| ----------- | ------- | ----------- |
| Ethernet    | MAC 3   | MAC 4       |
| IP          | 1.2.3.4 | 3.0.1.2     |

1(c) Header for packet 4.

| Header Type | Source  | Destination |
| ----------- | ------- | ----------- |
| Ethernet    | MAC 9   | MAC 10      |
| IP          | 1.2.3.8 | 1.2.4.3     |
| IP          | 1.2.3.6 | 2.0.0.1     |
| IP          | 1.2.3.4 | 3.0.1.2     |

2. QUESTION 2: TCP and Congestion Control (10 points)

Consider the following graph of TCP throughput (NOT DRAWN TO SCALE), where the y-axis describes the TCP window size of the sender. We will later ask you to describe what happens on the right side of the graph as the sender continues to transmit.

<img src="assets/image-20260504121147007.png" alt="image-20260504121147007" style="zoom:50%;" />

2.1 [5 points - 1 for each] The window size of the TCP sender decreases at several points in the graph, including those marked by B and D.

2.1(a) Name the event at B which occurs that causes the sender to decrease its window.

> Triple duplicate ACK.

2.1(b) Does the event at B necessitate that the network discarded a packet (Yes or No)? Why or why not?

> No. It could be due to reordering due to queuing or asymmetric paths.

2.1(c) Name the event at D which occurs that causes the sender to decrease its window.

> Timeout.

2.1(d) Does the event at D necessitate that the network discarded a packet (Yes or No)? Why or why not?

> No. Congestion in either direction could cause RTT > RTO (retrans. timeout).

2.1(e) For a lightly-loaded network, is the event at D MORE likely or LESS likely to occur when the sender has multiple TCP segments outstanding (in-flight) ? (Write "MORE" or "LESS")

> LESS.

2.2 [1 point] Consider the curved slope labeled by point A. Why does the TCP window behave in such a manner, rather than have a linear slope? Put another way, why would it be bad if region A had a linear slope?

> This "slow-start" period quickly discovers the maximum acceptable throughput that the path supports. Otherwise, AI (additive increase) could take too long, each a full RTT.

2.3 [3 points - 1 for each] Assume that the network has an MSS of 1000 bytes and the round-trip-time between sender and receiver of 100 mils. Assume at time 0 the sender attempts to open the connection. Also assume that the sender can "write" a full window's worth of data instantaneously, so the only latency you need to worry about is the actual propagation delay of the network.

2.3(a) How much time has progressed by point B?

> It depends if you interpret B as before or after you received the triple duplicate ACK, so we will accept both answers: 1 RTT (TCP handshake) + 3-4 RTT in slow-start (1, 2, 4, (8) MSS) = 4 or 5 RTT = 400 or 500 ms.

2.3(b) How much time has progressed between points C and D?

> 4 MSS to 16 MSS = 12 periods of RTT = 1.2 s.

2.3(c) How much time has progressed between points E and F?

> First: slow start to 8K window size (1 -> 2, 2 -> 4, 4 -> 8 MSS), then AI from 8 to 10 MSS window size (8 -> 9 -> (10) MSS). Similar question about where F exists as question (a), so we will accept either 5 or 6 RTT = 500 or 600 ms.

2.4 [1 point] If the sender shares its network with other clients whose traffic traverses the same IP routers, give one explanation for why point D is higher than point B?

> Changing cross-traffic by other concurrent senders across same routers.

4. QUESTION 4: Short Answers (15 points)

4.1 [3 points] Ethernet and IP

4.1(a) [2 points] Suppose Ethernet was the only existing LAN technology, so every host in the Internet was part of a local Ethernet and thus had a globally-unique Ethernet address. Your friend suggests that IP isn't necessary anymore, and the entire Internet could just be one large, switched Ethernet instead. Give two reasons why using existing Ethernet protocols for this is a bad idea from a networking perspective.

> Accepted answer examples:
> 1. Flooding does not scale for broadcast transmission when an address has not been learned by a switch.
> 2. Even with switched Ethernet, flooding does not scale for ARP or spanning tree.
> 3. MAC addresses are not hierarchical, so switches could not aggregate addresses into compact routing tables like IP prefixes.

4.1(b) [1 point] What about the other way around: why do we not simply assign IP addresses to network adaptors, instead of dealing with both MAC and IP addresses? Give one reason.

> Accepted answer examples:
> 1. This would give up topological addressing and aggregation, leading to large routing tables.
> 2. End hosts would need to announce addresses when they migrate, or the Internet would need something equivalent to global ARP for IP addresses.

4.2 [4 points] NAT and bidirectional firewall

4.2(a) [1 point] The corporate network has about 100,000 machines simultaneously using port-based NAT. What problem could arise if the network only has one public IP address?

> There are more machines wanting external communication than available ports, roughly 65K. NAT requests may fail, or port mappings may be reassigned in a way that breaks ongoing connections.

4.2(b) [1 point] The company wants one web server behind the NAT, and only this server, accessible from the public Internet. What do you need to set up?

> Manually configure port forwarding: public NAT address port 80 maps to the internal web server's private address port 80.

4.2(c) [2 points] The corporate network is not NATted, owns prefix `1.0.0.0/8`, and the web server is `1.2.3.4:80`. Fill in firewall rules so the server, and only the server, can accept incoming TCP connections.

| Source IP   | Source Port | Dest IP       | Dest Port | TCP Flags | Allow/Deny  |
| ----------- | ----------- | ------------- | --------- | --------- | ----------- |
| `*`         | `*`         | **`1.2.3.4`** | **`80`**  | `SYN`     | `ALLOW`     |
| `*`         | `*`         | `*`           | `*`       | `SYN-ACK` | `ALLOW`     |
| `1.0.0.0/8` | `*`         | `*`           | `*`       | `SYN`     | **`ALLOW`** |
| `*`         | `*`         | `*`           | `*`       | `SYN`     | **`DENY`**  |
| `*`         | `*`         | `*`           | `*`       | `*`       | `ALLOW`     |

4.3 [4 points] TCP ACKs

Using TCP, a sender has sent ten data segments, each 1000 bytes. The sender's ISN is 5000. A segment containing sequence numbers 20001 through 21000 may be called "segment 21000".

4.3(a) [1 point] After receiving `ACK 8001`, how many TCP segments does the sender know the receiver definitely received?

> 3 packets: 6000, 7000, 8000.

4.3(b) [1 point] The sender subsequently receives two more packets with `ACK 8001`. Which segment might be lost and should be retransmitted?

> Packet 8001-9000.

4.3(c) [1 point] After retransmitting this segment, the sender receives `ACK 12001`. Which original segments might still be lost?

> None.

4.3(d) [1 point] Which original segments were definitely received?

> 7 packets, bytes 5001-12000.

4.4 [4 points] UNIX socket programming

4.4(a) A proxy is downloading a web object from an origin webserver through an open TCP connection. Its latest `read()` call returns 0.

4.4(a.1) [0.5 points] What does this signify in general about a UNIX file descriptor?

> End of file (EOF) was reached; nothing more to read.

4.4(a.2) [1 point] What network event occurred to cause this?

> The remote peer closed its socket, and the remote network stack sent a FIN.

4.4(b) The proxy is sending a 5000-byte object back to the client through TCP file descriptor `fd`. The object is in a contiguous buffer `buf` of length 5000. The code calls `write(fd, buf + 2000, 1000)`.

4.4(b.1) [0.5 points] Which byte range are you trying to transfer?

> Bytes 2000-2999 inclusive in `buf`.

4.4(b.2) [1 point] If this `write()` call returns 500, what does this signify?

> Only bytes 2000-2499 were written.

4.4(b.3) [1 point] Why might this occur?

> The socket buffer only had space for 500 bytes, not the full 1000. The application should call `write(fd, buf + 2500, 500)`.

### 2010 Mid

> PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring10-cos461-exam1-answers.pdf>

| PDF page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                                                                  |
| ----------: | -------------------------------- | ------------------------------------------------------------------------------------------------ |
|         2-4 | Question 1.1, 1.2, 1.3           | DHCP, ARP, DNS, HTTP/TCP connection workflow and packet headers                                  |
|         5-6 | Question 2.1, 2.2, 2.3, 2.4, 2.5 | TCP congestion control, slow start, AIMD/window calculation                                      |
|         7-8 | Question 3.1, 3.2                | Socket call ordering and looping on send/partial writes                                          |
|        9-11 | Question 4.1(a), 4.1(b), 4.1(c), 4.2(a), 4.2(b), 4.3, 4.4, 4.5 | IP-prefix aggregation, IP/MAC addressing, TCP ACK/loss, ARP-cache conflict, TCP vs UDP selection |
|       12-13 | Question 5.2, 5.3, 5.6           | UDP/TCP socket demultiplexing fields; RED/drop-tail/congestion                                   |

QUESTION 1: Protocols and Addressing (19 points)

In the topology shown below, a client A (on the left side) joins a network and wants to download the webpage for http://example.net/ from the webserver H (on the right side). All wires/links are Ethernet segments. In this question, you will be asked what packets are on the wire (and the addresses in those packets’ headers) for this to occur. When asked to provide the addresses of machines, you can refer to them abstractly: IP-H is the IP address of the webserver H, MAC-H is the MAC address of H. If a packet is being sent to a broadcast address, use “BR” as the destination (e.g., IP-BR or MAC-BR).

<img src="assets/image-20260504134247520.png" alt="image-20260504134247520" style="zoom:33%;" />

Assume the following: 

- All the machines, except the client, already have their ARP caches full. 
- DNS resolver C has an empty DNS cache. • http://example.net/index.html fits in a single packet. 
- Client just joined the network and so all of its caches are empty (DNS, ARP, DHCP)

When you are asked to write a packet with its headers, you should include both network and link-layer addresses. So a DNS query from client A to server C and the response should look like the following. Note that other packets may be involved with a full DNS lookup that we are not showing in this example. 

| Order | Link Src | Link Dst | Network Src | Network Dst | Protocol Description |
| ----- | -------- | -------- | ----------- | ----------- | -------------------- |
| 1     | MAC-A    | MAC-C    | IP-A        | IP-C        | DNS query            |
| 2     | MAC-C    | MAC-A    | IP-C        | IP-A        | DNS resp.            |

1. [4 points] As it just joined the network, the first thing the client needs to do is get an IP address and other related network state. Write the packets on the network involved in that step, including their header information.

| Order | Link Src | Link Dst | Network Src | Network Dst | Protocol Description |
| ----: | -------- | -------- | ----------- | ----------- | -------------------- |
| 1 | MAC-A | MAC-BR | -- | -- | DHCP Discover |
| 2 | MAC-B | MAC-A | -- | -- | DHCP Offer |
| 3 | MAC-A | MAC-BR | -- | -- | DHCP Request |
| 4 | MAC-B | MAC-A | -- | -- | DHCP Acknowledgment |

2. [10 points] Now that the client has an IP address for itself, it wants to resolve the IP address of `example.com`, which will be IP_H. Write down all the packets involved in this phase. Remember that the client just joined the network.

| Order | Link Src | Link Dst | Network Src | Network Dst | Protocol Description |
| ----: | -------- | -------- | ----------- | ----------- | -------------------- |
| 1 | MAC-A | MAC-BR | | | ARP Request |
| 2 | MAC-C | MAC-A | | | ARP Reply |
| 3 | MAC-A | MAC-C | IP-A | IP-C | DNS Request |
| 4 | MAC-C | MAC-G | IP-C | IP-E | DNS Request (to .) |
| 5 | MAC-G | MAC-E | IP-C | IP-E | DNS Request |
| 6 | MAC-E | MAC-G | IP-E | IP-C | DNS Reply |
| 7 | MAC-G | MAC-C | IP-E | IP-C | DNS Reply |
| 8 | MAC-C | MAC-G | IP-C | IP-F | DNS Request (to .net) |
| 9 | MAC-G | MAC-F | IP-C | IP-F | DNS Request |
| 10 | MAC-F | MAC-G | IP-F | IP-C | DNS Reply |
| 11 | MAC-G | MAC-C | IP-F | IP-C | DNS Reply |
| 12 | MAC-C | MAC-G | IP-C | IP-I | DNS Request (to example.net) |
| 13 | MAC-G | MAC-I | IP-C | IP-I | DNS Request |
| 14 | MAC-I | MAC-G | IP-I | IP-C | DNS Reply |
| 15 | MAC-G | MAC-C | IP-I | IP-C | DNS Reply |
| 16 | MAC-C | MAC-A | IP-C | IP-A | DNS Reply |

3. [5 points] Now that the client has IP_H, it wants to download the web page `http://example.net/index.html`. The webpage fits in one data packet. Write down all network-layer packets that are sent on the wire in order to complete this process. Remember to clean up any transfers.

| Order | Network Src | Network Dst | Description |
| ----: | ----------- | ----------- | ----------- |
| 1 | IP-A | IP-H | TCP SYN |
| 2 | IP-H | IP-A | TCP SYN-ACK |
| 3 | IP-A | IP-H | TCP ACK |
| 4 | IP-A | IP-H | HTTP Request |
| 5 | IP-H | IP-A | TCP ACK |
| 6 | IP-H | IP-A | HTTP Reply |
| 7 | IP-A | IP-H | TCP ACK |
| 8 | IP-H | IP-A | TCP FIN |
| 9 | IP-A | IP-H | TCP FIN-ACK |
| 10 | IP-H | IP-A | TCP ACK |

> Note: The answer key also accepted 8 as IP-A to IP-H (close initialized by client), and also accepted a 4-way handshake of FIN, ACK, FIN, ACK.

QUESTION 2: TCP and Congestion Control (19 points)

Consider the following graph of TCP throughput (NOT DRAWN TO SCALE), where the y-axis describes the TCP window size of the sender. We will later ask you to describe what happens on the right side of the graph as the sender continues to transmit. 

<img src="assets/image-20260504135115369.png" alt="image-20260504135115369" style="zoom:33%;" />

1. [3 points] The window size of the TCP sender decreases at the points marked by A, C, and D on the graph, which happens when a packet belonging to the stream is lost. Name the event which occurs that causes the sender to decrease its window.

> A: Triple Duplicate ACK
> C: Triple Duplicate ACK
> D: Timeout

2. [4 points] Assume that the network has an MSS of 1000 bytes. If point A occurs 1 second after the sender begins its transfer, and the sender has written 15,000 bytes to the network by that time, what is the RTT of the network?

> 1 RTT for client handshake (SYN -> SYN-ACK). Then window size grows during slow start: 1 MSS, 2 MSS, 4 MSS, 8 MSS = 15 MSS = 15,000 bytes. 
>
> Note that A occurs at the point of detecting triple duplicate ACK, and therefore the client must have seen at least some ACKs from the 8 MSS windows. 
>
> Hence a total of 5 RTTs over 1 second = 200 ms.

3. [4 points] What is the sender's window size in bytes at point B?

> After triple duplicate ACK, the sender halves its window size as part of multiplicative decrease of AIMD, leaving 1/2 cwnd of A = 4 MSS = 4,000 bytes.

4. [4 points] If point C occurs 2 seconds after point B, what is the sender's window size in bytes at point C?

> Network RTT = 200 ms, so 2 seconds = 10 RTT. The sender's window is growing linearly in additive increase, increasing by 1 MSS every RTT. Prior cwnd was 4 MSS + 10 MSS = 14 MSS = 14,000 bytes.

5. [4 points] Assume that the window size at point D is 16,000 bytes, at which time it drops to 1,000 bytes. How much time will it take for the sender to return to a window size of 16,000 bytes, assuming no further packet loss?

> After a timeout, the window drops to 1 MSS. It grows via slow start until it reaches 1/2 of the cwnd at timeout, then grows linearly. Slow start to 8 MSS takes 3 RTT. Linear increase from 8 MSS to 16 MSS takes 8 more RTT, for 11 RTT total.

QUESTION 3: Socket Programming (16 points)

1. [5 points] Write the basic system calls needed to transfer a file from the client to the server using TCP. The client already has the server IP address, and the file can be written/read in a single call to `send`/`recv`.

| Order | Client | Server |
| ----: | ------ | ------ |
| 1 | | socket |
| 2 | | bind |
| 3 | | listen |
| 4 | | accept |
| 5 | socket | |
| 6 | bind | |
| 7 | connect | |
| 8 | send | |
| 9 | | recv |
| 10 | close | |
| 11 | | close |

> Note: There are multiple different acceptable answers.

2. [10 points] Write C-like pseudocode for how you would transmit a 100,000B file using `send`.

```c
// buf points to a buffer of size len
//   that you want to transmit in its entirety
// fd is an open file descriptor connected to server
// RETURN 0 ON SUCCESS, -1 ON FAILURE

int sendall(int fd, char *buf, int len) {
    int sent = 0;

    while (sent < len) {
        int bytes_sent = send(fd, buf + sent, len - sent);

        if (bytes_sent < 0)
            return -1;
        sent += bytes_sent;
    }

    return 0;
}
```

> Note: There are multiple other correct solutions here.

QUESTION 4: Short answers (29 points)

1. [6 points] IP Address Aggregation

Suppose you are network operator for an ISP, and your ISP has two customer networks, MIT and Princeton. MIT hosts: `18.0.0.1`, `18.0.0.254`, `18.255.255.254`. Princeton hosts: `128.112.0.1`, `128.112.255.254`.

1(a) Give the IP prefix notation that your colleague uses to represent these two networks.

> `18.0.0.0/8` and `128.112.0.0/16`.

1(b) After installing that forwarding table entry, you still see traffic for `18.255.255.254`, but stop seeing traffic for `18.0.0.1` and `18.0.0.254`. What three IP prefixes cause you to receive traffic for all five hosts?

> `18.0.0.0/8`, `18.0.0.0/24`, and `128.112.0.0/16`.

1(c) Give one possible explanation why this change is needed.

> `18.0.0.0/24` is multi-homed from another provider and, given longest prefix matching for preferred traffic, all traffic was going through its other provider. Similarly, some other ISP could be announcing any prefix longer than 8 bits, e.g. `18.0.0.0/16`.

2. [4 points] Ethernet and IP

2(a) Suppose Ethernet was the only existing LAN technology, so every host in the Internet was part of a local Ethernet and thus had a globally-unique Ethernet address. Would you recommend getting rid of IP addresses by simply using Ethernet addresses instead of IP addresses? Why or why not?

> No. It would not scale due to the need for broadcast for discovery, and forwarding tables would be large because MAC addresses are not topologically assigned and thus cannot be aggregated.

2(b) What about the other way around, why do we not simply assign IP addresses to network adaptors, instead of dealing with both Ethernet and IP addresses?

> No. Either you keep topological aggregation but require adaptors to get manually reassigned an IP address whenever moving, or adaptors have static IP addresses but then you sacrifice routing table aggregation.

3. [8 points] Using TCP, a sender has sent out packets 1 through 20. The sender receives an ACK for packet 10, then three ACKs for packet 11.

3(a) Which of the 20 packets can the sender assume are lost?

> 12.

3(b) Which of the 20 packets can the sender assume were definitely received?

> 1-11.

Now, the same sender resends the next missing packet and receives an ACK for packet 16.

3(c) Which packets of the original 20 can the sender assume are still lost, if any?

> None.

3(d) Which of the original 20 can the sender assume were definitely received?

> 1-16.

4. [5 points] A, B, and C are directly connected to the same switch. A opens a TCP connection to B and adds an ARP cache entry with TTL 60 seconds. B transfers a large file to A. A new host D connects with the same IP address as A. At time 55 seconds, D opens a TCP connection to C. A few seconds later, the TCP transfer between A and B breaks. What steps led to this connection breaking?

> At time 60, B's ARP cache expires. When B re-issues an ARP request for the IP address shared by A and D, D's answer is cached by B. B's TCP packet gets sent to MAC-D, which does not have such an open TCP connection and replies with TCP-RST, causing B's connection to break. Similar for A and its ARP cache.

5. [6 points] What transport layer protocol (TCP or UDP) would you use if your application needed each property, and why?

> (a) Speed: UDP - no connection setup or sender-side buffering.
> (b) Long messages: TCP - stream-of-bytes abstraction supports arbitrarily long messages; many stacks limit UDP messages to some maximum size, e.g. 64KB.
> (c) Short-duration interactions: UDP - no connection setup delay.
> (d) Fairness between competing flows: TCP - fairness through congestion control.
> (e) Flooding: UDP - no connection state needed.
> (f) Flexibility: UDP - more application-level control.

QUESTION 5: Multiple choice (17 points)

2. When a UDP segment arrives at a host, in order to direct the segment to the appropriate socket, the OS network stack uses which fields?

> (b) the destination IP address; (d) the destination port number.

3. When a TCP segment belonging to an existing connection arrives at a host, in order to direct the segment to the appropriate socket, the OS network stack uses which fields?

> (a) source IP address; (b) destination IP address; (c) source port number; (d) destination port number.

6. Which of the following are advantages that RED has over drop-tail queuing?

> (a) has fewer burst losses; (b) has shorter queuing delays.

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

> No official solution text is available in the cited source; prompt retained only.

1(B) DNS server-selection

> No official solution text is available in the cited source; prompt retained only.

1(C) IP anycast

> No official solution text is available in the cited source; prompt retained only.

1(D) NAT + load-balancer

> No official solution text is available in the cited source; prompt retained only.

1(E) ARP spoofing (unsolicited announcement of your MAC with other’s IP address)

> No official solution text is available in the cited source; prompt retained only.

QUESTION 2: More network system engineering (13 points)

2(a) You graduated from Princeton (yay!) and joined a social media startup that wants to rival Facebook (at least you hope). The startup doesn’t have any funding, so you took your implementation of simple router and are running it on a Linux box, using it as a router for your servers (instead of paying $$ to Cisco). As your company scaled, you started seeing some clients that use IPv6. Your servers understand IPv6, but your router doesn’t. Describe two ways in which you can extend your router to handle IPv6 traffic:

> No official solution text is available in the cited source; prompt retained only.

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

What is going wrong? Or, explain why this information is useless. (Answer in at most two lines.)

> No official solution text is available in the cited source; prompt retained only.

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

Figure transcription: the topology has links $A-B=21$, $A-D=15$, $B-C=18$, $B-D=12$, $C-D=5$, $C-E=11$, and $D-E=17$.

3(a) Show the initial routing table of node E:

> No official solution text is available in the cited source; prompt retained only.

3(b) Show the routing table of node E after one iteration of the algorithm:

> No official solution text is available in the cited source; prompt retained only.

3(c) Show the routing table of node E after two iterations of the algorithm:

> No official solution text is available in the cited source; prompt retained only.

3(d.i) In some failure situations, the administrator notices that it takes an exceptionally long time for the routing protocol to stabilize in this network. What problem with the distance vector protocol is the cause?

> No official solution text is available in the cited source; prompt retained only.

3(d.ii) The administrator is told that BGP does not suffer from this problem. What prevents BGP from having this problem?

> No official solution text is available in the cited source; prompt retained only.

QUESTION 4: Routing, addressing, and tunneling (9 points)

The above figure shows a network topology connecting two LANs. The LAN on the left uses a NAT to connect to the Internet and includes a client host H1. The LAN on the right includes a webserver H2. Packets between the two LANs are routed along the path shown by a heavy dark lines, which includes both an IP tunnel and an MPLS tunnel. All packets which traverse the path use both tunnels. The various network interfaces have IP and MAC addresses as shown.

Source figure labels retained in text form:

```text
H1: 10.0.0.2 / MAC 1
NAT inside: 10.0.0.1 / MAC 2
NAT outside: 1.2.3.4 / MAC 3
Left-side router-facing link: 1.2.3.5 / MAC 4
IP/MPLS path labels: 1.2.3.6 / MAC 5, 1.2.3.7 / MAC 6, 1.2.3.8 / MAC 7,
                  1.2.4.1 / MAC 8, 1.2.4.2 / MAC 9, 1.2.4.3 / MAC 10,
                  1.2.4.4 / MAC 11, 2.0.0.1 / MAC 12, 2.0.0.2 / MAC 13
Right-side LAN/router labels: 3.0.0.1 / MAC 14, 3.0.0.2 / MAC 15,
                              3.0.0.3 / MAC 16, 3.0.0.4 / MAC 17
H2: 3.0.1.2 / MAC 18
```

H1 has established an HTTP session with web server H2 and data packets are flowing between the two machines. As an example, we have filled in the headers for packet 1 (traveling from the server H2 to the client H1). If there shouldn't be any source or destination field for the header type, write an "X" in that table entry.

| Header Type | Source | Destination |
| ----------- | ------ | ----------- |
| Ethernet | MAC 16 | MAC 15 |
| IP | 3.0.1.2 | 1.2.3.4 |

You have to fill in the header type and the source and destination address for the network and data-link layer headers for packets 2, 3, 4, and 5 (these packets are all traveling from the client H1 to the server H2). Note: You might not need to use all the rows supplied.

4(a) Header for packet 2:

> No official solution text is available in the cited source; prompt retained only.

4(b) Header for packet 3:

> No official solution text is available in the cited source; prompt retained only.

4(c) Header for packet 4:

> No official solution text is available in the cited source; prompt retained only.

4(d) Header for packet 5:

> No official solution text is available in the cited source; prompt retained only.

### 2009 Mid

> PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring09-cos461-exam1-answers.pdf>

| PDF page(s) | Problem / subpart ID(s) retained                              | CSC4303 overlap                                                                              |
| ----------: | ------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
|         2-3 | Question 1(A), 1(B), 1(C), 1(D)                               | Transmission delay, TCP slow start, duplicate ACK vs timeout loss detection                  |
|         4-6 | Question 2(A), 2(B), 2(C)                                     | TCP socket call ordering, TCP stream packetization, UDP datagram packetization               |
|         7-8 | Question 3(A), 3(B)                                           | Web browser request flow with DHCP/ARP/DNS/TCP/HTTP/cache                                    |
|        9-10 | Question 4(B), 4(C), 4(D), 4(E)                               | Layer-2 next-hop MAC, layer-3 source addressing, ARP                                          |
|       11-12 | Question 5(F), 5(G), 5(H)                                     | DNS TTL/records, web caches, persistent HTTP                                                 |
|       13-15 | Question 6(A), 6(B), 6(C), 6(D), 6(E), 6(F), 6(G), 6(H)       | Soft state, exponential backoff, TCP SYN retransmissions, DNS/UDP, NAT, ECN, protocol layers |


QUESTION 1: Transporting a file (15 points)

1A. [2 points] Assuming that all bandwidth is consumed by your data, and that you can immediately start sending data at the maximum rate, how long will it take to transmit a 250,000 byte file over a 2 million bits/second connection?

> `250,000 bytes * (8 bits / 1 byte) * 1/2,000,000 bits/s = 1 second`.

1B. [5 points] Now assume that you are sending the file via TCP, with a maximum segment size of 1000 bytes. How many network RTTs will it take to transmit the entire file?

> TCP first establishes a connection via SYN/SYN-ACK: 1 RTT. Then slow start transmits 1, 2, 4, 8, 16, 32, 64, 128 MSS. The sum is 255 MSS = 255,000 bytes > 250,000 bytes, so the file finishes after the 8th RTT of slow start. Total: `1 + 8 = 9 RTT`. The key also accepted 7.5 RTTs for slow start and did not take off points for including 1 RTT for FINs.

1C. [4 points] After TCP reaches an instantaneous transmission rate of 32,000 bytes/s, a single packet is lost. Assuming no other packets are in transmission, what is the next instantaneous rate and how long in RTTs to reach 32,000 bytes/s again?

> This was meant to seek how TCP reacts to detecting loss via triple duplicate ACK. TCP reacts by MD, cutting the window size by half, and continues by AI. The next transmission rate is 16,000 bytes/s, and it takes 16 RTTs to recover, increasing by 1 MSS = 1000 bytes each RTT.

1D. [4 points] Would anything be different if all packets were lost after reaching 32,000 bytes/s? If so, what is the next instantaneous rate and how long in RTTs to reach 32,000 bytes/s again?

> Because all packets are lost, loss is detected through timeout. The sender's window is reduced to one MSS and enters slow-start restart. Assuming RTT = 1s, the next rate is 1000 bytes/s. Slow-start from 1 MSS to 16 MSS takes 4 RTTs, then additive increase from 16 to 32 MSS takes 16 RTTs. Total = 20 RTTs; the key also accepted 21 RTTs.

QUESTION 2: Sockets (16 points)

2A. [10 points] For each scenario, can the server ever get the data sent by the client?

> i) No. `connect()` would not successfully return, allowing `send()`, before the server accepts.
> ii) No. Same explanation as (i). Also valid: the server is not listening when the client attempts to connect.
> iii) Yes.
> iv) No. `accept()` would not return with a valid file descriptor until the client has connected.
> v) Yes.

2B. [3 points] Application A uses a stream TCP socket and calls `send()` ten times.

> i) Can the underlying stack transmit more than ten data packets? Yes. If a write is larger than MSS, TCP might transmit it in two packets; retransmission from loss was also accepted.
> ii) Can it transmit fewer than ten data packets? Yes. Small writes can be coalesced into single data packets using Nagle's algorithm.

2C. [3 points] Application A uses a datagram UDP socket and calls `sendto()` ten times.

> i) Can the underlying stack transmit more than ten data packets? Yes. UDP packets larger than the network MTU will experience IP fragmentation.
> ii) Can it transmit fewer than ten data packets? No.

QUESTION 3: Your Web Browser in action (17 points)

3A. [12 points] The user on machine A requests `http://S/index.html`. List the proper order of packet IDs that are sent on the network.

> `11, 7, 2, 3, 12, 9, 4, 5, 10, 8`.

3B. [5 points] On a subsequent request for `http://S/index.html`, A has no local Web or DNS cache and C has no DNS cache, but all other cacheable things are cached. Which items from 3A are eliminated?

> `11, 7, 3, 12, 9, 4, 5, 10`. The trickiest number was 9: although C has no DNS cache, if it has the object cached, it can serve it directly without going to server S, so it never needs DNS for S.

QUESTION 4: A routed and bridged network (14 points)

4B. Just before the packet reaches bridge B1, what is its layer 2 destination?

> `R2a.mac`.

4C. Just before the packet reaches bridge B2, what is its layer 2 source?

> `R2c.mac`.

4D. Just after the packet leaves router R2, what is its layer 3 source?

> `H1.ip`.

4E. When H1 sends out an ARP query, what is the reply to that query?

> `R2a.mac` has `R2a.ip`, or just `R2a.mac`.

QUESTION 5: Multiple choice (16 points)

5F. Which of the following is/are true about DNS?

> A. A query for an A record may return multiple IP addresses in the response.
> C. A short TTL on an NS record reply runs the risk of increasing traffic at the root or GTLD nameservers.

5G. Which of the following is/are true about web caches?

> A. A web cache, or proxy server, is a network entity that satisfies HTTP requests from clients.
> B. A web cache is both a client and a server at the same time.

5H. Which of the following is/are true about persistent HTTP connections?

> B. Only one TCP connection must be opened for downloading a "page", if that page does not include any embedded objects served by other servers. The key also marked A correct because the question was overly confusing.

QUESTION 6: Short Answer (22 points)

6A. [2 points] Explain the principle of soft state. Provide two examples of a network protocol or technology that abides by soft state.

> Soft state refers to stored state that is not "hard" (persistent, consistent, explicit, etc.). It is often stored temporarily, refreshed to survive network changes/failures or persist over time, and is often an optimization. Accepted answers: ARP tables, DNS caches, DHCP addresses that persist over leases.

6B. [2 points] List two protocols that use exponential backoff, and describe what/where problems would occur if each protocol did not backoff.

> TCP congestion control uses exponential backoff/multiplicative decrease. Without backoff, congestion would build up at routers, queues would remain full and drop packets, leading to low throughput. Ethernet CSMA/CD uses exponential backoff; without it, collisions would continue on the shared medium, leading to low goodput.

6C. [3 points] List three possible explanations for why host A would need to retransmit the SYN packet as part of establishing the TCP connection with B.

> SYN from A to B dropped by router on path; SYN dropped by B because B's receive backlog is full; SYN-ACK from B to A dropped by router; SYN-ACK not received by A before timeout; SYN dropped by firewall or NAT in front of B.

6D. [1 point] Give one reason that DNS lookups are run over UDP rather than TCP.

> DNS is a simple query/response protocol, so UDP avoids TCP connection setup and state overhead. DNS queries/responses are usually small and fit in one packet. UDP is also amenable to anycast DNS servers, and UDP headers are smaller.

6E. [2 points] Give two reasons that sites use NATs.

> NATs allow multiple private addresses behind a single public address, help with IPv4 address-space pressure, provide privacy about internal deployments, allow internal renumbering without changing external addresses, and can act as firewalls when explicit forwarding rules are not configured.

6F. [3 points] When a packet is going from a LAN onto the wider Internet, what header fields might an on-path NAT change?

> Source IP address, source port, IP checksum, transport TCP/UDP checksum.

6G. [3 points] How does ECN differ from traditional congestion detection? Give one benefit and one reason it might not be widely used today.

> ECN signals congestion by explicitly marking packets, rather than by dropped packets. It lets end hosts react to congestion without unnecessary loss. It is not widely used because sender, recipient, and routers all need ECN support, creating a deployment challenge.

6H. [4 points] For several OSI layers, give examples of associated protocols.

> Application: FTP, HTTP, SMTP, telnet, SIP.
> Transport: TCP, UDP, DCCP.
> Network: IPv4, IPv6.
> Data link: Ethernet, PPP, token ring, FDDI, 802.11.
> Physical: twisted pairs, CAT5, fiber, Manchester, NRZ.

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


QUESTION 1: Big MAC (15 points)

1(a) In today's Internet, why is it difficult to support continuous communication with a host while it moves? Why would an Internet based on MAC addresses have the potential to make mobile hosts easier to support?

> Mobility is difficult because a host's IP address changes as it moves, since IP addresses are allocated to institutions hierarchically. Dynamic IP changes make it difficult to sustain a connection, e.g. TCP or UDP socket, with another host. An Internet based on MAC addresses would allow the host's identifier to stay the same as it moves.

1(b) Today's LANs have boot-strapping techniques such as DHCP, ARP, and MAC learning. In a world without IP addresses, which would still be necessary?

> DHCP would no longer be needed to assign an IP address or network mask, though a similar mechanism may still configure the local DNS server and gateway router. ARP would no longer be necessary because there would be no need to map IP to MAC. MAC learning would still be necessary so switches learn how to forward frames to a host based on MAC address.

1(c) How would moving to an Internet based on MAC addresses affect forwarding-table size?

> Forwarding tables could grow quite large because MAC addresses are not hierarchical. Today routers store about 200K IP prefixes representing many more hosts. Within a LAN, switch forwarding tables could likely stay the same size, since hosts could direct external traffic to the gateway router.

QUESTION 3: Going With the Flow (10 points)

3(a) A home user upgrades from dial-up to broadband but does not see much improvement visiting a Web site. Give one reason, even if the network and server have ample capacity.

> The receiver window may limit throughput: throughput is limited by RWIN/RTT. Also, most Web transfers are short; their download time is dominated by RTT because the TCP connection does not leave slow start and does not fill the receive window.

3(b) When an Internet path becomes overloaded, total goodput can decrease. Explain why.

> When congested, many packets travel partway through the network only to be lost and retransmitted. The wasted bandwidth can cause other packets to hit congestion, suffer loss, and need retransmission, reducing successful delivery.

3(c) Why are many wireless losses detected by timeout rather than triple duplicate ACKs? What are the performance implications?

> Wireless networks tend to have bursty losses due to interference. This reduces the chance that some packets in the same TCP window are delivered while earlier ones are lost; those successful deliveries are needed to trigger duplicate ACKs. Small wireless congestion windows and small transfers can make this worse, so timeout recovery is more common and slower.

3(d) A router maintains a queue of packets awaiting transmission. Give one reason a large buffer is desirable and two reasons it may be undesirable.

> A larger buffer can temporarily accommodate bursts without drops. However, it increases RTT and delay unpredictability, increases the time for TCP senders to learn of congestion, and makes the router more expensive.

QUESTION 4: Caught in the Web (15 points)

4(a) In the TCP three-way handshake, host A sends SYN, B sends SYN-ACK, and A sends ACK. When can A start sending data packets? When can B start? Explain why they cannot start sooner.

> Host A can start sending upon receiving SYN-ACK, because that signals B is willing to accept traffic and knows A's initial sequence number. Host B can start sending upon receiving the ACK, because that signals A is willing to accept traffic and knows B's initial sequence number.

4(b) HTTP/1.1 supports persistent connections and pipelining. How does the server know where one request ends and the next begins?

> The server identifies request boundaries by parsing HTTP requests, e.g. based on CRLF and/or `Content-Length`.

4(c) Why can't the TCP implementation ensure each `read()` or `recv()` returns one complete HTTP request? Give two reasons/examples.

> TCP provides a stream-of-bytes abstraction with no knowledge of application syntax. The application message may be larger than the OS receive buffer or application buffer. The full request may also not have arrived yet, causing `read`/`recv` to return only data received so far.

4(d) Give two reasons persistent connections and pipelining were added to HTTP/1.1. Why do browsers typically disable pipelining by default?

> They avoid extra TCP traffic for opening/closing many connections, avoid repeating slow start and relearning congestion state, improve fairness across Web clients on the same path, and reduce RTT delays in downloading a Web page. Browsers often disable pipelining because parallel connections can give higher throughput, possibly at others' expense, and enable simultaneous download/display of embedded images.

QUESTION 5: Losing Control (15 points)

5(a) Active-mode FTP can cause problems when the client host is behind a NAT box. Why?

> The NAT maps the client's data-connection IP/port to new values, so the PORT command arguments do not match the NAT's values. The server also has trouble initiating a data connection to a NATted client without an existing NAT table entry, and the PORT command may contain a private non-routable address.

5(b) What actions would a NAT box need to perform on FTP control messages to correctly handle active-mode FTP?

> It must parse FTP control messages on port 21 to extract PORT arguments, create a table entry for the data connection, and modify the PORT message arguments so the FTP server can create and use the data connection.

5(c) Why might these operations change the size of underlying IP packets, and how could NAT handle that?

> The NAT's IP address and port may have a different number of decimal digits in the PORT command. The NAT must change packet sizes and adjust TCP sequence numbers and acknowledgment numbers. If the packet grows beyond MTU, the NAT may fragment IP packets.

5(d) What challenges arise if other applications use port 21, or if FTP client/server encrypt communications?

> Another application on port 21 may be mistaken for FTP control; if it sends `PORT`, the NAT may modify packet contents unpredictably. With encryption, the NAT cannot parse the PORT command in the TCP payload and cannot correctly map the IP/port.

5(e) Why is passive mode easier than active mode with client-side NAT?

> In passive mode the server selects an address and port and sends them to the client. The client-side NAT does not need to modify the remote server's address and port. Passive mode can still be challenging with server-side NAT.

QUESTION 6: A Rose by Any Other Name (15 points)

6(e) A local DNS server usually discards cached name-to-address mappings when TTL expires. Alternatively, it could optimistically issue a new query for the cached domain name. Give one advantage and one disadvantage.

> Prefetching the mapping can hide DNS lookup delay and improve user performance. However, it introduces extra DNS queries and network load for mappings that may never be needed.

QUESTION 7: For Good Measure (15 points)

7(a) Traceroute uses IP TTL. Give two reasons why a hop might show `*`.

> The probe packet may be lost on the forward path. The TIME_EXCEEDED packet may be lost on the reverse path. The router may be configured not to send TIME_EXCEEDED messages. The packet may encounter a firewall or NAT that drops it.

7(b) Traceroute may report a path that does not exist, e.g. A-B-C with no B-C link. Give one example.

> The route may change during measurement. If the route from A to Z changes from A-B-Y-Z to A-D-C-Z, the first probe returns B and the second returns C even though B and C are not directly connected. A middlebox such as a transparent proxy or firewall can also obscure the path.

7(c) SYN/SYN-ACK delay estimates RTT. Give one reason it is often larger than a typical RTT.

> The server may have a listen queue for pending TCP connection requests; the SYN may sit in the queue before the SYN-ACK is sent.

7(d) Propose two techniques to infer an IP host's rough geographic location.

> Reverse DNS names may reveal location. Whois records may reveal location. Probes such as ping from many vantage points can triangulate location. Traceroute router names near the destination may reveal likely location.

### Spring 2008 Final

Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring08-cos461-exam2-answers.doc>

| Page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                           |
| ------: | -------------------------------- | --------------------------------------------------------- |
|     DOC | Question 1(a), 1(b), 1(c), 1(d)  | Link-state routing weights and shortest-path behavior     |
|     DOC | Question 2(a), 2(b), 2(c), 2(d)  | BGP routing policy and RouteViews-style routing reasoning |


QUESTION 1: Weighting it Out (10 points)

1a) How should network operators set link weights if their goal is to minimize the number of hops each packet traverses to reach its destination? (2 points)

> All the weights should be set to the same value, e.g. `1`.

1b) How should operators set link weights to minimize end-to-end delay when the network is lightly loaded and queuing delay is insignificant? (2 points)

> Propagation delay is the only source of delay. The weight of each link should be set proportional to its length, i.e. propagation delay.

1c) In the given topology, put arrows on the edges to show the shortest path from every node to destination node d, i.e. the sink tree. (2 points)

> Nodes a and g take a direct path to d. The other nodes go left until they reach a, d, or g.

1d) Suppose link f-e is overloaded. Identify one weight change on one link that diverts traffic from source f to destination d away from f-e without affecting any other source-destination paths. (4 points)

> The h-i link should be changed to 2. That makes path f-i-h-g-d decrease from 28 to 21, less than the cost 22 of path f-e-d.

QUESTION 2: Route Views (10 points)

2a) Draw all paths to destination AS d, the sink tree leading to d, and circle ASes that do not have any route to d. (2 points)

> The paths are b-a-d, g-d, and h-e-d. Nodes c, f, and i cannot reach d.

2b) What path does e take to reach i? If f terminates the peering relationship with e, can e still reach i? If so, what is the new path? (2 points)

> Node e takes path e-f-i. With e-f removed, the path is e-b-c-f-i. The path e-h-i is not used because e's customer h would not advertise a peer-learned route to its provider.

2c) If ASes a and b dump all BGP routes they learn for every destination, and a researcher extracts all links from all AS paths in those dumps, what inferred topology is missing? (3 points)

> The graph is missing peering edges d-e, d-f, g-h, and h-i. Node a learns only customer-learned routes from customer d and peer b, exposing a-d, a-d-g, a-b, a-b-e, and a-b-e-h. Node b learns those routes plus b-e and b-e-h from e, as well as b-c, b-c-f, and b-c-f-i from c.

2d) What is the minimum set of ASes that must provide dumps of every AS path they learn for every edge to be visible in at least one dump? (3 points)

> Two nodes: b and h, or e and h. Node h reveals all edges except a-d and c-f; those are in a routing-table dump at either e or b.

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


QUESTION 1: Internet Versus Station Wagon (15 points)

1(a) Suppose the station wagon drives 100 km/hour and the link has bandwidth 800,000 bits/second. At what file size does the station-wagon solution start delivering data faster?

> By car, travel time is 2 hours: `200 km * 1 hr/100 km`. During two hours, the link transfers `800,000 bits/sec * 60 sec/min * 60 min/hour * 2 hr * 1 byte/8 bits = 720,000,000 bytes`.

1(b) The sender uses packets with 20-byte IP header, 20-byte TCP header, and MSS 512 bytes. How much more time as a fraction does the data transfer take?

> MSS 512 plus two 20-byte headers gives packet size 552 bytes. Only `512/552` of bandwidth is data, so the transfer takes `552/512` of the time, or `40/512 = 5/64` longer.

1(c) With a 200 km link and electricity speed 200,000,000 m/s, how big must the receive window be to avoid constraining transfer rate?

> One-way delay is `1 sec/200,000 km * 200 km = 0.001 sec`, so RTT is 0.002 sec. The bytes in one RTT are `0.002 sec * 800,000 bits/sec * 1 byte/8 bits = 200 bytes`.

QUESTION 2: Sockets (15 points)

2(a) A stream-socket application writes data ten times. Why might TCP transmit more than ten data packets, excluding retransmissions/control packets?

> If the application writes more than an MSS of data, one `write()` can lead to multiple TCP segments and packet transmissions.

2(b) Why might TCP transmit all the data in fewer than ten data packets?

> If the application writes less than an MSS, data from multiple `write()` calls may be combined into one TCP segment. This is especially true in applications like Telnet when Nagle's algorithm is used.

2(c) Why can A safely call `close()` when done writing, even if B has not received all the data?

> TCP, typically in the OS, buffers the data and continues to retransmit it to the receiver as needed.

2(d) List two possible explanations for retransmitting a TCP SYN.

> The SYN may be lost, discarded due to checksum error, or discarded because the receiver's listen queue is full. The SYN-ACK may be lost. The RTO may be too small, e.g. for a long-haul link.

2(e) Since UDP sockets do not establish a connection, why is a port number necessary?

> For demultiplexing the packet to the correct receiving socket.

QUESTION 3: Demultiplexing (10 points)

3(a) For a NAT, when a packet arrives from the external Internet, what fields determine the internal IP destination? What other IP/TCP/UDP fields does NAT change?

> NAT inspects the destination port number, and address if the NAT has multiple external IPs, to identify the receiving host. It changes destination address and port, as well as checksum.

3(b) How does NAT know what destination MAC address to use on the internal Ethernet?

> It checks its ARP table for the MAC corresponding to the internal destination address; on a miss, it issues an ARP query.

3(c) Once the Ethernet frame reaches the destination host, how does the host know what network-layer protocol parses the payload?

> The Ethernet frame has a `type` field identifying the network-layer protocol.

3(d) How does the OS know if the packet is UDP or TCP?

> The IP header has a `protocol` field identifying the transport-layer protocol.

3(e) How does the OS know which process/socket should receive the packet?

> The protocol field in the IP header and the destination port in the transport-layer header identify the receiving socket.

QUESTION 4: Cheaters Sometimes Win (15 points)

4(a) List one motivation for sending an IP packet with a wrong source IP address, and two ways this can hurt the legitimate owner.

> A denial-of-service attacker may spoof another host's source address to evade detection. The legitimate owner may be blamed or blocked from legitimate traffic, and may receive unwanted return traffic such as SYN-ACK or RST packets.

4(c) Consider TCP that does not reduce sending rate on packet loss. How does this affect other TCP traffic, and can it hurt the offender?

> The rogue sender does not reduce congestion, forcing other packets to be dropped. Well-behaved TCP senders reduce their rates and share what bandwidth the rogue sender is not using, causing unfairness. It can also hurt the rogue flow because excessive load causes loss and retransmissions.

4(d) Many browsers open several TCP connections in parallel for embedded images. How does this affect other TCP traffic? If no other traffic traverses the link, is this still useful?

> Extra TCP connections give the browser an unfair share of bottleneck bandwidth, reducing throughput of well-behaved applications. With no other traffic, the connections share only with each other; it may still help when RTT-limited, during slow start, and because images fill in simultaneously.

4(e) Some ARP implementations update cache on unsolicited replies. If a rogue sends its MAC address with the gateway router IP to another LAN host, what happens when that host sends to an external address?

> The host sends the packet in an Ethernet frame to the rogue machine's MAC address; the rogue may discard it or inspect it before forwarding to the legitimate gateway.

QUESTION 5: Home-Network "Box" (15 points)

5(a) The Box may act as DHCP client and DHCP server. Why?

> It acts as DHCP client to the DSL provider's DHCP server to get a public IP address. It acts as DHCP server to allocate private IP addresses to internal hosts.

5(b) How do home hosts learn the gateway IP? Is this the same as the public provider address?

> Hosts learn the internal-facing gateway address via DHCP. It is not the ISP-assigned external-facing public address; the internal-facing address lies in the private block used inside the home network.

5(c) A home host sends a TCP SYN to an external Web server. Explain ARP and NAT in getting the first IP packet out.

> The host sees the destination is outside the local subnet and directs the IP packet to the Box. It uses ARP to determine the gateway MAC, then sends the Ethernet frame to the Box. The Box maps source address and source port using its NAT table before sending traffic to the Internet; it may also ARP for the ISP gateway MAC.

5(d) Why might it be hard for the end user to determine the public IP directly? How does an external Web site know?

> The end host learns the private internal address of the NAT box, not the public external address. The Web server receives the HTTP request from the NAT box public address and thus knows the public address.

QUESTION 6: Internet Principles (15 points)

6(a) List one advantage and one disadvantage of soft state, and two examples from class.

> Soft state is robust to a device that fails ungracefully and does not relinquish state. It wastes resources in repeated refreshes. Examples include DNS TTLs, DHCP lease time, ARP cache time, and NAT bindings.

6(b) List one advantage and disadvantage of text-based headers. Why does IP use binary?

> Text headers are easier for humans to read/debug and are extensible. They are verbose and harder to parse. IP uses binary to limit header bandwidth and simplify fast router parsing.

6(c) IP allows variable-sized packets. List one advantage and disadvantage of forcing all packets to the same size.

> Fixed-size packets need no packet-length field and are easier to manage with fixed buffers. They waste bandwidth due to padding when data is smaller than packet size.

6(d) List one advantage and disadvantage of CIDR over classful routing.

> CIDR allocates limited address space more efficiently by allowing many block sizes. It requires routers to perform longest-prefix match, which is hard to do quickly.

6(e) List one disadvantage of TCP RTO being too large and one of being too small.

> Too large: sender waits too long to retransmit lost packets, slowing transfers. Too small: sender retransmits packets that were not actually lost, wasting bandwidth.

QUESTION 7: Decentralized Control (15 points)

7(a) Why does TCP decrease rate on loss more aggressively than it increases after successful delivery?

> Overshooting path capacity has dire consequences in congestion collapse, while undershooting only makes the network somewhat less efficient. TCP multiplicative decrease is crucial to stability.

7(b) TCP's reaction to loss depends on how loss is detected. What are the two scenarios and how does the sender adapt?

> Timeout: sender decreases sending rate to 1 MSS and repeats slow start, assuming serious congestion. Triple-duplicate ACK: sender halves sending rate, assuming congestion is not too bad.

7(c) Give two reasons a local DNS server is not configured with TLD server IPs. How does it learn them?

> TLD servers may change, and new TLDs may be added. The local DNS server is configured with root server addresses and contacts a root server to learn the TLD server of interest.

7(d) List two reasons for hierarchical allocation of IP address blocks.

> It reduces administrative overhead by letting registries allocate large blocks to ISPs, which allocate smaller blocks to customers. It improves routing efficiency because smaller customer blocks often need not be globally known when reachable via the provider's aggregate.

7(e) MAC addresses are link-local in significance. Why are they globally unique?

> If two devices had the same MAC and later appeared on the same LAN, switches could not reliably learn where to forward frames; frames could alternate between devices and be very hard to debug.

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


QUESTION 1: Scalability of Peer-to-Peer Systems (15 points)

1(a) What is the minimum time for the server to transmit a 100 kbyte file to 31 receivers in a client-server configuration? (3 points)

> The server must transmit the 100 kbyte = 800 kbit file to 31 receivers at 40 kbits/sec. Total time is `(31 * 100 * 8) / 40 = 620 seconds`.

1(b) Receivers can upload only after receiving the entire file. What is the minimum time? (3 points)

> The number of receivers with a copy doubles after each full 100 kbyte transmission. Each round takes `(100 * 8) / 40 = 20 seconds`; `log2 32 = 5` rounds. Total = `20 * 5 = 100 seconds`.

1(c) Receivers can upload after receiving the first 20 kbyte chunk. How long to deliver to all receivers? (3 points)

> The first 20 kbytes require five rounds, each `(20 * 8) / 40 = 4 seconds`, so after 20 seconds every peer has the first chunk. The last peers then download the remaining 80 kbytes in `(80 * 8) / 40 = 16 seconds`. Total = 36 seconds.

1(d) Why do broadband BitTorrent peers mostly exchange chunks with broadband peers, and dial-up peers with dial-up peers? (2 points)

> Peers exchange with other peers that upload to them at a high rate. Broadband peers therefore exchange mostly with broadband peers, and dial-up peers with dial-up peers.

1(e) Why is BitTorrent vulnerable to incomplete downloads? What steps help prevent it? (2 points)

> After downloading the full file, peers may leave instead of serving chunks. Rarest-chunk-first increases the chance every chunk is available from at least one active peer; random chunk policy also helps distribute chunks across peers.

1(f) Suggest ways to extend BitTorrent to work better for less popular files. (2 points)

> Incentives could apply across files, encouraging peers to store chunks of unpopular files even if they do not want them, e.g. virtual currency usable for faster downloads of desired files.

QUESTION 2: Routing Protocols (20 points)

2(a) Suppose link k-m fails. Before failure, what is the shortest path from i to j? What is the new path after convergence? (2 points)

> Before failure: i-k-m-j, cost 6. After failure: i-r-n-j, cost 8.

2(b) A transient forwarding loop may occur during convergence. Involving what nodes? What can happen to data packets from i to j? (3 points)

> Nodes k and n may loop if k learns the failure first and forwards along k-n-j while n still forwards along old path n-k-m-j. Some packets are discarded when TTL expires; others may escape, see high delay, and arrive out of order.

2(e) Two directly connected BGP routers A and B run BGP over TCP. How can TCP be established before BGP has exchanged routes? (3 points)

> The routers have interfaces on the same subnet, so they know how to reach each other directly, perhaps using ARP to learn the MAC address.

QUESTION 3: Multimedia Streaming and Quality of Service (10 points)

3(a) Frames arrive at times 0, 1.2, 1.99, 4.17, 4.01, 5.03, 8.05, 7.50, 8.90, 8.99. With immediate playout at one frame/sec, which frames are late and how much extra delay is needed? (2 points)

> Starting with frame 0 at time 0, frame i should play at time i. Late frames: 1, 3, 4, 5, 6, 7, and 8. Frames 2 and 9 arrive in time. The worst offender is frame 6, 2.05 seconds late, so 2.05 seconds extra playout delay is enough.

3(b) List three reasons TCP is ill-suited to interactive audio/video. Why is it often used anyway? (3 points)

> TCP retransmits lost packets even when they arrive too late, has a 20-byte header that is wasteful for small audio packets, can drop sending rate dramatically, and withholds later packets after loss due to in-order delivery. It is often used because many firewalls block UDP packets.

3(c) What are similarities and differences between a TCP connection and a virtual circuit? (3 points)

> Similarities: both have setup/teardown phases, and data are delivered reliably and in order. Differences: virtual circuits tend to reserve bandwidth and switches/routers keep forwarding state, while routers do not reserve resources or keep per-TCP-connection forwarding state.

QUESTION 4: Ethernet and Wireless (10 points)

4(a) Ethernet bridging relies on flooding. List two protocols that generate broadcast traffic and explain why. (2 points)

> ARP requests are broadcast to learn the MAC address for an IP address because the sender does not know where the destination is. DHCP requests are broadcast during bootstrapping so a host can find a DHCP server and obtain IP address, subnet mask, gateway, and DNS server.

QUESTION 5: Overlay Networks (15 points)

5(a) Overlay routing can react more quickly to network events than the underlay. How? At what cost? (3 points)

> A small overlay can send active probes aggressively to detect reachability/performance problems quickly, while routers may detect failures conservatively and converge slowly. The cost is probe overhead imposed on the network.

5(b) Why does RON limit paths to two overlay hops, i.e. one intermediate node? Advantage and disadvantage? (4 points)

> One extra hop is usually enough to bypass the direct-path problem, and limiting to one hop simplifies the protocol. Advantage: simplicity. Disadvantage: it may miss the best path if two or more intermediates would help.

5(c) List two underlay changes that could support RON. (4 points)

> Routers could explicitly notify overlay nodes about network-condition changes instead of requiring active probing. Routers could support packet deflections through intermediate points inside the network, avoiding traffic going in and out of intermediate hosts.

5(d) List two advantages and two disadvantages of Napster's central directory over Gnutella query flooding. (4 points)

> Advantages: simpler protocol and lower query-processing overhead because queries go directly to a central server. Disadvantages: central directory is a single point of failure/attack, does not scale well, and was a legal vulnerability.

QUESTION 6: Application-Layer Protocols (10 points)

6(a) SMTP is chatty. Why is this bad for wireless mobile devices, and what can fix it without changing all email servers? (3 points)

> The wireless device may not remain connected long enough for many RTTs to the mail server. An intermediate server can let the mobile use a less chatty protocol, while the intermediate server speaks SMTP to the email server.

6(b) Why are official RFC standards useful? What are the advantages of skipping standardization, and how can a new application still be widely deployed? (2 points)

> Standards provide interoperability between independently written software. Skipping standardization saves time and can help new entrants move faster. Wide deployment is possible if one developer provides all necessary software, e.g. peer software or both client and server.

6(c) YouTube uses Flash, HTTP, and TCP. How did each help success? (3 points)

> Flash was widely installed on end hosts, avoiding new plug-ins. HTTP clients are widely available in browsers. TCP under HTTP works well through firewalls and NATs.

6(d) Why have CDNs been more widely deployed than web proxy caches? (2 points)

> Content providers can contract with CDNs to deliver their content, improving performance, reducing cost, and handling demand surges. Providers cannot force many sites to deploy proxy servers. Proxies also cannot cache all dynamic content; CDNs can run server software that generates it.

QUESTION 7: Layering (10 points)

7(a) Why does TCP perform badly on wireless links? What can improve performance without upgrading all wired hosts? (2 points)

> Wireless loss is not necessarily congestion, but TCP treats packet loss as congestion and reduces rate. A TCP proxy at the wireless/wired boundary can improve performance.

7(b) CNN reduced a page to around 1000 characters after 9/11. Why this size? (2 points)

> 1000 bytes plus the HTTP response header fits in a single 1500-byte IP packet, reducing server load and load on CNN's Internet connection.

7(c) IP routers are network-layer devices but sometimes inspect transport headers. Give two reasons. (2 points)

> Filtering or queueing by port number; NAT requiring port inspection/remapping; measurement/logging of port numbers or per-flow stats; punishing non-TCP-friendly flows.

7(d) What protocol layer does BGP operate at? What about DNS? (2 points)

> BGP and DNS are application-layer protocols. BGP runs over TCP; DNS runs over TCP or UDP.

QUESTION 8: Source Routing (10 points)

8(3a) List three advantages of source routing relative to today's routing protocols.

> Sender can exploit performance/reliability knowledge, choose paths matching application requirements, avoid untrusted links or ASes, and react quickly to failures by rerouting.

8(3b) List three disadvantages of source routing.

> Sender must do extra work, packets cannot easily adapt route midstream, packets are larger due to path information, sender must learn Internet connectivity, ISPs lose traffic-control ability, and DoS attacks are easier.

8(3c) Source routing exists in IP routers but is usually disabled. List three reasons.

> Operators lose control over traffic flow, risking congestion and lost revenue; source routing increases DoS vulnerability; it requires extra router processing overhead.

### Spring 2006 Mid

Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring06-cos461-exam1-answers.doc>
Answer DOC: <https://www.cs.princeton.edu/courses/archive/spr06/cos461/exams/midterm-answers.doc>

| Page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                                   |
| ------: | -------------------------------- | ----------------------------------------------------------------- |
|     DOC | Question 1(a), 1(b), 1(c)        | transmission overhead, packetization, TCP/IP headers, ACK traffic |
|     DOC | Question 2(a), 2(b), 2(c)        | socket programming and networked-application behavior             |


QUESTION 1: Transmission Overhead (15 points)

1(a) MSS is 472 bytes, and each data packet and ACK has TCP/IP headers plus a 20-byte link-layer header/trailer. What fraction of bandwidth is consumed by TCP segment data?

> Each TCP packet has link, network, and transport headers: 20 + 20 + 20 = 60 bytes. An ACK has no payload and is 60 bytes. A full data packet is 472 + 60 = 532 bytes. Sending 472 bytes of TCP segment data incurs 532 bytes for the data packet and 60 bytes for the ACK: `472/592 = 59/74`, about 79.7%.

1(b) What if MSS is increased to 1460 bytes?

> As before, the equation is `MSS/(MSS + 60 + 60)`. With MSS 1460, the fraction is `1460/1580 = 73/79`, about 92.4%.

1(c) What if MSS is 1460 and receivers use delayed ACKs for every other data packet?

> Only half of data packets incur an ACK. Two data packets transfer `2*MSS` bytes and incur `2*(MSS+60)` bytes in data packets plus one 60-byte ACK. Fraction: `2*1460/(2*1460 + 120 + 60) = 2920/3100 = 146/155`, about 94.2%.

QUESTION 2: Sockets (15 points)

2(a) Early Web servers generated HTTP response-header lines one at a time and used a separate `write`/`send` for each line. Why is this inefficient for the end host?

> The server makes a separate system call for each line, causing high overhead switching between user process and OS. Small packets at the client may also require many browser receive calls if packets do not arrive close together.

2(b) Why is this inefficient for the network?

> The resulting TCP segments are very small, comparable to link/IP/TCP headers, so much bandwidth is headers. The receiver must also send ACKs for these data packets, producing many ACK packets.

2(c) How could a programmer fix this?

> Create a large user-space buffer, e.g. at least 1460 bytes, build the response header there, and make a single socket call to send the full header. The OS can then generate larger packets containing multiple lines.

### Spring 2006 Second Mid

Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring06-cos461-exam2-answers.doc>
Answer DOC: <https://www.cs.princeton.edu/courses/archive/spr06/cos461/exams/midterm2-answers.doc>

| Page(s) | Problem / subpart ID(s) retained  | CSC4303 overlap                                                               |
| ------: | --------------------------------- | ----------------------------------------------------------------------------- |
|     DOC | Question 1, undergraduate version | router state, forwarding/routing behavior, QoS/resource-reservation reasoning |
|     DOC | Question 1, graduate version      | router state, forwarding/routing behavior, QoS/resource-reservation reasoning |


QUESTION 1, UNDERGRADUATE STUDENTS: VNS Router (15 points)

1(a) Describe three different scenarios when an IP router would drop packets that arrive on one of its interfaces.

> Insufficient buffer space; no route for the destination; badly formed packet such as checksum error; TTL expiry.

1(b) List four fields of a packet that an IP router must modify before forwarding to its next hop.

> Source MAC address; destination MAC address; IP time-to-live field; IP header checksum.

1(c) What state does an IP router maintain about directly-connected neighbors? How does it maintain this state?

> ARP cache, i.e. table of neighboring Ethernet/IP mappings. Maintained using ARP, with refresh and responses to ARP requests.

QUESTION 1, GRADUATE STUDENTS: Quality of Service (15 points)

1(a) With token-bucket depth 10 cells and token rate 100 cells/s, how many cells can the virtual circuit transmit in one second? In ten seconds?

> Burst of 10 cells plus token rate: 110 cells in one second, 1010 cells in ten seconds.

1(b) A link has propagation delay P and transmits R cells/s. A cell arrives when Q other cells await transmission and the link just started transmitting the first. What delay does the new cell experience?

> Propagation delay P plus waiting for Q+1 transmissions at one every 1/R seconds: `P + (Q+1)/R`.

1(c) FIFO link carries two token-bucket virtual circuits: bucket depths 9 and 1, token rates 100 each, propagation 60 ms. What smallest R satisfies the 100 ms delay constraint?

> If link rate is below sum of token rates, backlog can grow arbitrarily. Otherwise burst backlog is at most 10 cells. If the delay-sensitive cell arrives just after the other nine, delay is `P + 10/R`. Need `60 ms + 10/R <= 100 ms`, so `R >= 250 cells/s`.

1(d) Why would a different link scheduler allow a smaller R?

> A shared FIFO queue makes the delay-sensitive circuit vulnerable to bursts from the other circuit. Separate queues with strict priority or weighted fair scheduling limit that impact.


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

Problem 1, item 14: Why is `gethostbyname` not thread safe?

> (c) It returns a pointer to global shared memory.

Problem 1, item 18: When requested to send 20 bytes over a network socket, execution will block until all 20 bytes have been sent. (✅/❌)

> False.

Problem 1, item 21: Which tool would you first use to debug a network application that never appears to accept any connections?

> (b) `strace`.

### Fall 2010 Final

> PDF: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f10.pdf>
Model solution TXT: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f10-sol.txt>

| Page(s) | Problem / subpart ID(s) retained | CSC4303 overlap                                        |
| ------: | -------------------------------- | ------------------------------------------------------ |
|       2 | Problem 1, item 1                | socket/listen/connect/accept/socket/bind call ordering |

Problem 1, item 1: Label the networking system calls `listen`, `connect`, `accept`, `socket`, and `bind` in the order they should be called. Mark unused calls with `X`.

| Call | Client | Server |
| ---- | ------ | ------ |
| `listen` | X | 3 |
| `connect` | 2 | X |
| `accept` | X | 4 |
| `socket` | 1 | 1 |
| `bind` | X | 2 |

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

| Server | Client |
| ------ | ------ |
| `socket` | |
| `bind` | |
| `listen` | |
| `accept` | |
| | `socket` |
| | `connect` |
| `read` | |
| | `write` |
| | `close` |

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
