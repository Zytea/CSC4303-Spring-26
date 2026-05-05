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

1(6) It's better to use UDP rather than TCP to send game updates in fast-paced multiplayer games where low latency is a high priority. (✅/❌)

> True. TCP’s retries and ordering cause latency spikes in case of packet loss.

1(7) Transmission delay is proportional to the packet size, while propagation delay is proportional to the length of the link. (✅/❌)

> True. Transmission delay is the time spent sending the packet by the router, while the propagation delay is the time it spends travelling on the link.

2(1) Explain two major differences between standard TCP and UDP. (Remember that P1 was a UDP protocol that added some functionalities of TCP.)

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

> At-most-once. Because the client and the server don't have a failure detection and retry mechanism, each request is executed at most once.

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

> Solution: The records from the root and GTLD have long TTLs and are cached widely. The root and GTLD zones are replicated very widely and it is difficult to attack all locations at the same time. (Anycast)


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

1) list *ALL* servers where the DNS record stored (do not list cached locations), 2) what will its TTL be (assume that the TTL can only be 1 minute or 1 day) and 3) why you chose that TTL (1-2 sentences)

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

   > If B received the message before sending the message to C, then C’s clock would read 4. Otherwise, C’s clock would read 2.

### Mid 2010

> PDF: <https://www.cs.cmu.edu/~dga/15-440/F12/midterm2010_solve.pdf>

1. RPC tries to make remote procedure calls look the same as local procedure calls. But the illusion isn’t perfect. Circle all of the options that correctly describe differences between a local function call and an RPC:

A. RPC calls require an extra parameter to identify the server.

B. RPC calls may have higher or variable latency.

C. RPC calls are limited to call-by-value.

D. RPC calls have different (more) failure modes. 

E. Local function calls require a malloc of a heap object to represent the return pointer.

   > A,B,D

8. For which of the following applications would UDP be preferable over TCP, ignoring annoying concerns such as firewalls that might block some protocols?

A. Streaming a live video over the internet

B. Instant messaging/email

C. Logging in to your bank website

D. Voice over IP

E. Large file transfers

F. Looking up a very small value from a directory service TCP / UDP

   > UDP, TCP, TCP, UDP, TCP, UDP

11. Suppose each computer in a distributed system keeps an approximate real-time clock $R_i$ in addition to a Lamport-like clock $L_i$.

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
   > > **Why?** > > Consider the sequence of all events $e \ldots e'$ at computer $i$. > > If $S(e') \le S(e)$ then there must exist at least one pair of $f \to_i f'$ such that $S(f') \le S(f)$; otherwise each new event would advance the logical clock $L_i$, which would yield $L_i(e') > L_i(e)$ and thus $S(e') > S(e)$.
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

   > **The fundamental problem is that the logical clock will never advance past the real-time clock** at each computer, so skew in the real-time clocks can cause the receive to be timestamped earlier than the send.

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

C. Asynchronous function calls （要选，现在是2026）

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

   > (1) This allows routing based on proximity, which would reduce slow routes that criss-cross the globe. (2) It provides a fallback in case one of the nodes in the finger table is unreachable.

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

1. A router has a 100,000-byte FIFO buffer, with an upload bandwidth of 1 Mbps or 125,000 bytes per second. MTU = 1000 bytes.

1(a) If the buffer is completely full of TCP acknowledgment packets, how many packets are queued in the buffer? Assume **the TCP segment has no payload**, and the packet headers do not contain any IPv4 or TCP options. (3 points)

> Ignoring the link-layer header and any minimum size restriction on the link-layer frame, a TCP ACK packet is 40 bytes long, consisting of a 20-byte IP header and a 20-byte TCP header. A 100,000-byte buffer can hold $100000/40 = 2500$ ACK packets. 
>
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

6(a) Give two examples of how knowing a client’s rough geographic location can improve an Internet service.

> - Customizing the content to the user’s location (e.g., showing weather, advertisements, traffic reports, etc. related to the user’s presumed location)
> - Blacking out access to sites disallowed in certain geographic regions (e.g., due to local laws, commercial restrictions on showing sporting events in the local area, etc.)
> - CDN: Directing clients to the closest Web server offering a given service.

6(b) Propose a technique to infer the geographic location associated with an IP address, without cooperation from the end user. Explain how your technique works, and what assumptions it makes.

> - Performing a traceroute to the client address, and looking for geographically-meaningful names late in the traceroute path (e.g., “yale-univer.car2.stamford1.level3.net”)
> - Performing pings to measure latency to reach the client from multiple vantage points with known geographic locations, and triangulating to infer the client’s location - Altering the design of the routing system to include geographic information (though this requires substantial control over the entire Internet, making this approach unrealistic in practice)
> - Performing a reverse DNS lookup on the client IP address (though most client’s don’t have DNS names, and these names often don’t reveal location information), or performing a “whois” query to find the address of the organization that owns the IP address

6(c) Give an example where your technique will not produce accurate results.

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
>        |
>        | DNS query:
>        | abc123.seq5.jrex.com
>        v
> ================================================
> Hotspot pay wall
> Only allows DNS query to local DNS server
> ================================================
>        |
>        v
> +-----------------------+
> | Hotspot local DNS     |
> | does recursive lookup |
> +----------+------------+
>         |
>         | query for *.jrex.com
>         v
> +-----------------------------+
> | User's authoritative DNS    |
> | server for jrex.com         |
> | decodes message             |
> | acts as proxy               |
> +-------------+---------------+
>            |
>            | normal Internet access
>            v
>      Arbitrary website
> ```
>
> 问题：
>
> - 低带宽，高延迟，DNS cache，异常流量
>
> Several students offered a different answer that was also valid. The idea is to hijack the hotspot’s local DNS server by sending a forged ARP response for the DNS server’s IP address, learned by the client in DHCP bootstrapping. Now the client can send UDP port 53 packets, and follow the approach in part 7(a) of the question. Note that this approach may be easier for the hotspot administrators to detect, since the local DNS server would suddenly be carrying no traffic. (That said, even the solution above is relatively easy to detect if the hotspot administrators are monitoring DNS query/response loads on a per-client basis.)
>
> 其他假设：
>
> - 不检查 source IP 是否属于这个 MAC
>
> > ``` 
> > > Ethernet src MAC = attacker MAC M_A 
> > > IP src = DNS server IP D 
> > > UDP port = 53 
> > ```
> >
> > gateway 检查 `IP D 是否真的属于 MAC M_A？` 就完蛋了
>
> - 不启用 DHCP snooping / IP source guard / dynamic ARP inspection
>
> - firewall 只粗略看 IP/port，而不严格验证 DNS 语义
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

3(a) Traceroute can sometimes return a path that does not even exist in the Internet topology. E.g., hop i may not be connected to hop i+1. Give one reason why this might happen.

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

The above figure shows a network topology. The LAN on the left uses a NAT to connect to the Internet and includes a client host H1. The LAN on the right includes a webserver H2. Packets between the two endpoints are routed along the path shown by a heavy dark lines, which includes two IPv4 tunnels. All packets which traverse the path use bSoth tunnels. The various network interfaces have IP and MAC addresses as shown.

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

2. TCP and Congestion Control (10 points)

Consider the following graph of TCP throughput (NOT DRAWN TO SCALE), where the y-axis describes the TCP window size of the sender. We will later ask you to describe what happens on the right side of the graph as the sender continues to transmit.

<img src="assets/image-20260504121147007.png" alt="image-20260504121147007" style="zoom:50%;" />

2(1) [5 points - 1 for each] The window size of the TCP sender decreases at several points in the graph, including those marked by B and D.

2(1)(a) Name the event at B which occurs that causes the sender to decrease its window.

> Triple duplicate ACK.

2(1)(b) Does the event at B necessitate that the network discarded a packet (Yes or No)? Why or why not?

> No. It could be due to reordering due to queuing or asymmetric paths.

2(1)(c) Name the event at D which occurs that causes the sender to decrease its window.

> Timeout.

2(1)(d) Does the event at D necessitate that the network discarded a packet (Yes or No)? Why or why not?

> No. Congestion in either direction could cause RTT > RTO (retrans. timeout).

2(1)(e) For a lightly-loaded network, is the event at D MORE likely or LESS likely to occur when the sender has multiple TCP segments outstanding (in-flight) ? (Write "MORE" or "LESS")

> LESS.

2(2) [1 point] Consider the curved slope labeled by point A. Why does the TCP window behave in such a manner, rather than have a linear slope? Put another way, why would it be bad if region A had a linear slope?

> This "slow-start" period quickly discovers the maximum acceptable throughput that the path supports. Otherwise, AI (additive increase) could take too long, each a full RTT.

2(3) [3 points - 1 for each] Assume that the network has an MSS of 1000 bytes and the round-trip-time between sender and receiver of 100 mils. Assume at time 0 the sender attempts to open the connection. Also assume that the sender can "write" a full window's worth of data instantaneously, so the only latency you need to worry about is the actual propagation delay of the network.

2(3)(a) How much time has progressed by point B?

> It depends if you interpret B as before or after you received the triple duplicate ACK, so we will accept both answers: 1 RTT (TCP handshake) + 3-4 RTT in slow-start (1, 2, 4, (8) MSS) = 4 or 5 RTT = 400 or 500 ms.

2(3)(b) How much time has progressed between points C and D?

> 4 MSS to 16 MSS = 12 periods of RTT = 1.2 s.

2(3)(c) How much time has progressed between points E and F?

> First: slow start to 8K window size (1 -> 2, 2 -> 4, 4 -> 8 MSS), then AI from 8 to 10 MSS window size (8 -> 9 -> (10) MSS). Similar question about where F exists as question (a), so we will accept either 5 or 6 RTT = 500 or 600 ms.

2(4) [1 point] If the sender shares its network with other clients whose traffic traverses the same IP routers, give one explanation for why point D is higher than point B?

> Changing cross-traffic by other concurrent senders across same routers.

4. Short Answers (15 points)

4(1) [3 points] Ethernet and IP

4(1)(a) [2 points] Suppose Ethernet was the only existing LAN technology, so every host in the Internet was part of a local Ethernet and thus had a globally-unique Ethernet address. Your friend suggests that IP isn't necessary anymore, and the entire Internet could just be one large, switched Ethernet instead. Give two reasons why using existing Ethernet protocols for this is a bad idea from a networking perspective.

> Accepted answer examples:
> 1. Flooding does not scale for broadcast transmission when an address has not been learned by a switch.
> 2. Even with switched Ethernet, flooding does not scale for ARP or spanning tree.
> 3. MAC addresses are not hierarchical, so switches could not aggregate addresses into compact routing tables like IP prefixes.

4(1)(b) [1 point] What about the other way around: why do we not simply assign IP addresses to network adaptors, instead of dealing with both MAC and IP addresses? Give one reason.

> Accepted answer examples:
> 1. This would give up topological addressing and aggregation, leading to large routing tables.
> 2. End hosts would need to announce addresses when they migrate, or the Internet would need something equivalent to global ARP for IP addresses.

4(2) [4 points] NAT and bidirectional firewall

4(2)(a) [1 point] The corporate network has about 100,000 machines simultaneously using port-based NAT. What problem could arise if the network only has one public IP address?

> There are more machines wanting external communication than available ports, roughly 65K. NAT requests may fail, or port mappings may be reassigned in a way that breaks ongoing connections.

4(2)(b) [1 point] The company wants one web server behind the NAT, and only this server, accessible from the public Internet. What do you need to set up?

> Manually configure port forwarding: public NAT address port 80 maps to the internal web server's private address port 80.

4(2)(c) [2 points] The corporate network is not NATted, owns prefix `1.0.0.0/8`, and the web server is `1.2.3.4:80`. Fill in firewall rules so the server, and only the server, can accept incoming TCP connections.

| Source IP   | Source Port | Dest IP       | Dest Port | TCP Flags | Allow/Deny  |
| ----------- | ----------- | ------------- | --------- | --------- | ----------- |
| `*`         | `*`         | **`1.2.3.4`** | **`80`**  | `SYN`     | `ALLOW`     |
| `*`         | `*`         | `*`           | `*`       | `SYN-ACK` | `ALLOW`     |
| `1.0.0.0/8` | `*`         | `*`           | `*`       | `SYN`     | **`ALLOW`** |
| `*`         | `*`         | `*`           | `*`       | `SYN`     | **`DENY`**  |
| `*`         | `*`         | `*`           | `*`       | `*`       | `ALLOW`     |

4(3) [4 points] TCP ACKs

Using TCP, a sender has sent ten data segments, each 1000 bytes. The sender's ISN is 5000. A segment containing sequence numbers 20001 through 21000 may be called "segment 21000".

4(3)(a) [1 point] After receiving `ACK 8001`, how many TCP segments does the sender know the receiver definitely received?

> 3 packets: 6000, 7000, 8000.

4(3)(b) [1 point] The sender subsequently receives two more packets with `ACK 8001`. Which segment might be lost and should be retransmitted?

> Packet 8001-9000.

4(3)(c) [1 point] After retransmitting this segment, the sender receives `ACK 12001`. Which original segments might still be lost?

> None.

4(3)(d) [1 point] Which original segments were definitely received?

> 7 packets, bytes 5001-12000.

4(4) [4 points] UNIX socket programming

4(4)(a) A proxy is downloading a web object from an origin webserver through an open TCP connection. Its latest `read()` call returns 0.

4(4)(a)(1) [0.5 points] What does this signify in general about a UNIX file descriptor?

> End of file (EOF) was reached; nothing more to read.

4(4)(a)(2) [1 point] What network event occurred to cause this?

> The remote peer closed its socket, and the remote network stack sent a FIN.

4(4)(b) The proxy is sending a 5000-byte object back to the client through TCP file descriptor `fd`. The object is in a contiguous buffer `buf` of length 5000. The code calls `write(fd, buf + 2000, 1000)`.

4(4)(b)(1) [0.5 points] Which byte range are you trying to transfer?

> Bytes 2000-2999 inclusive in `buf`.

4(4)(b)(2) [1 point] If this `write()` call returns 500, what does this signify?

> Only bytes 2000-2499 were written.

4(4)(b)(3) [1 point] Why might this occur?

> The socket buffer only had space for 500 bytes, not the full 1000. The application should call `write(fd, buf + 2500, 500)`.

### 2010 Mid

> PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring10-cos461-exam1-answers.pdf>

1. Protocols and Addressing (19 points)

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

1(1) [4 points] As it just joined the network, the first thing the client needs to do is get an IP address and other related network state. Write the packets on the network involved in that step, including their header information.

| Order | Link Src | Link Dst | Network Src | Network Dst | Protocol Description |
| ----: | -------- | -------- | ----------- | ----------- | -------------------- |
| 1 | MAC-A | MAC-BR | -- | -- | DHCP Discover |
| 2 | MAC-B | MAC-A | -- | -- | DHCP Offer |
| 3 | MAC-A | MAC-BR | -- | -- | DHCP Request |
| 4 | MAC-B | MAC-A | -- | -- | DHCP Acknowledgment |

1(2) [10 points] Now that the client has an IP address for itself, it wants to resolve the IP address of `example.com`, which will be IP_H. Write down all the packets involved in this phase. Remember that the client just joined the network.

| Order | Link Src | Link Dst | Network Src | Network Dst | Protocol Description |
| ----: | -------- | -------- | ----------- | ----------- | -------------------- |
| 1 | MAC-A | MAC-BR | | | ARP Request |
| 2 | MAC-C | MAC-A | | | ARP Reply |
| 3 | MAC-A | MAC-C | IP-A | IP-C | DNS Request |
|  |  |  |  |  |  |
| 4 | MAC-C | MAC-G | IP-C | IP-E | DNS Request (to .) |
| 5 | MAC-G | MAC-E | IP-C | IP-E | DNS Request |
| 6 | MAC-E | MAC-G | IP-E | IP-C | DNS Reply |
| 7 | MAC-G | MAC-C | IP-E | IP-C | DNS Reply |
|  |  |  |  |  |  |
| 8 | MAC-C | MAC-G | IP-C | IP-F | DNS Request (to .net) |
| 9 | MAC-G | MAC-F | IP-C | IP-F | DNS Request |
| 10 | MAC-F | MAC-G | IP-F | IP-C | DNS Reply |
| 11 | MAC-G | MAC-C | IP-F | IP-C | DNS Reply |
|  |  |  |  |  |  |
| 12 | MAC-C | MAC-G | IP-C | IP-I | DNS Request (to example.net) |
| 13 | MAC-G | MAC-I | IP-C | IP-I | DNS Request |
| 14 | MAC-I | MAC-G | IP-I | IP-C | DNS Reply |
| 15 | MAC-G | MAC-C | IP-I | IP-C | DNS Reply |
|  |  |  |  |  |  |
| 16 | MAC-C | MAC-A | IP-C | IP-A | DNS Reply |

1(3) [5 points] Now that the client has IP_H, it wants to download the web page `http://example.net/index.html`. The webpage fits in one data packet. Write down all network-layer packets that are sent on the wire in order to complete this process. Remember to clean up any transfers.

| Order | Network Src | Network Dst | Description |
| ----: | ----------- | ----------- | ----------- |
| 1 | IP-A | IP-H | TCP SYN |
| 2 | IP-H | IP-A | TCP SYN-ACK |
| 3 | IP-A | IP-H | TCP ACK |
|  |  |  |  |
| 4 | IP-A | IP-H | HTTP Request |
| 5 | IP-H | IP-A | TCP ACK |
| 6 | IP-H | IP-A | HTTP Reply |
| 7 | IP-A | IP-H | TCP ACK |
|  |  |  |  |
| 8 | IP-H | IP-A | TCP FIN |
| 9 | IP-A | IP-H | TCP FIN-ACK |
| 10 | IP-H | IP-A | TCP ACK |

> Note: The answer key also accepted 8 as IP-A to IP-H (close initialized by client), and also accepted a 4-way handshake of FIN, ACK, FIN, ACK.

2. TCP and Congestion Control (19 points)

Consider the following graph of TCP throughput (NOT DRAWN TO SCALE), where the y-axis describes the TCP window size of the sender. We will later ask you to describe what happens on the right side of the graph as the sender continues to transmit.

<img src="assets/image-20260504135115369.png" alt="image-20260504135115369" style="zoom:33%;" />

2(1) [3 points] The window size of the TCP sender decreases at the points marked by A, C, and D on the graph, which happens when a packet belonging to the stream is lost. Name the event which occurs that causes the sender to decrease its window.

> A: Triple Duplicate ACK C: Triple Duplicate ACK D: Timeout

2(2) [4 points] Assume that the network has an MSS of 1000 bytes. If point A occurs 1 second after the sender begins its transfer, and the sender has written 15,000 bytes to the network by that time, what is the RTT of the network?

> 1 RTT for client handshake (SYN -> SYN-ACK). Then window size grows during slow start: 1 MSS, 2 MSS, 4 MSS, 8 MSS = 15 MSS = 15,000 bytes.
>
> Note that A occurs at the point of detecting triple duplicate ACK, and therefore the client must have seen at least some ACKs from the 8 MSS windows.
>
> Hence a total of 5 RTTs over 1 second = 200 ms.

2(3) [4 points] What is the sender's window size in bytes at point B?

> After triple duplicate ACK, the sender halves its window size as part of multiplicative decrease of AIMD, leaving 1/2 cwnd of A = 4 MSS = 4,000 bytes.

2(4) [4 points] If point C occurs 2 seconds after point B, what is the sender's window size in bytes at point C?

> Network RTT = 200 ms, so 2 seconds = 10 RTT. The sender's window is growing linearly in additive increase, increasing by 1 MSS every RTT. Prior cwnd was 4 MSS + 10 MSS = 14 MSS = 14,000 bytes.

2(5) [4 points] Assume that the window size at point D is 16,000 bytes, at which time it drops to 1,000 bytes. How much time will it take for the sender to return to a window size of 16,000 bytes, assuming no further packet loss?

> After a timeout, the window drops to 1 MSS. It grows via slow start until it reaches 1/2 of the cwnd at timeout, then grows linearly. Slow start to 8 MSS takes 3 RTT. Linear increase from 8 MSS to 16 MSS takes 8 more RTT, for 11 RTT total.

3. Socket Programming (16 points)

You are implementing a simple application to transfer a file from the client to the server using TCP.

3(1) [ 5 points ] In the following, write the basic system calls you need to use in order to transfer the file. Assume that the client already has the IP address of the server. You don't need to show arguments, i.e., name resolution could have just been written as gethostbyname (not struct hostent * gethostbyname(const char *name)) and you don't need to show any other programmatic logic. Assume that the file can be written/read in a single call to send/recv.

In the below table, provide a set of system calls in an appropriate order. Each line should have a single call at the client or server, not both. Some calls at the client and server can happen concurrently; just list them in a reasonable order (i.e., the write at the client should occur before the read at the server). Note: You might not need to use all the rows supplied. Remember to cleanup after you transmit the file.

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

> Note there are multiple different acceptable answers.

3(2) [10 points] Now consider the pseudocode of the client's send call in a bit more depth. Write some pseudocode (it doesn't need to compile, but should look C-like), how you would transmit a 100,000B file. In this code snippet, you should use arguments and return values to express the logic flow.

Your code should only be a few lines long; we're only interested in the logic immediately surrounding your use of the send system call.

```c
// buf points to a buffer of size len
//   that you want to transmit in its entirety
// fd is an open file descriptor connected to server
// RETURN 0 ON SUCCESS, -1 ON FAILURE

int sendall (int fd, char *buf, int len) {
        int sent = 0;
        while (sent < len) {
           int bytes_sent = send (fd, buf+sent, len-sent);
           if (bytes_sent < 0)
                return -1;
           sent += bytes_sent;
       }
       return 0;
  }
```

> There are multiple other correct solutions here.

4. Short answers (29 points)

4(1) [6 points] IP Address Aggregation

Suppose you are network operator for an ISP, and your ISP has two customer networks (MIT and Princeton). For the sake of simplicity, let’s assume that MIT only has 3 hosts with the following IP addresses, and Princeton only has 2 hosts:

MIT:    18.0.0.1, 18.0.0.254, 18.255.255.254

Princeton: 128.112.0.1, and 128.112.255.254

You’ve heard that memory in router line cards is expensive, so you’d like to use as few entries as possible in your line cards. Your colleague at work says he has a solution that only requires two forwarding-table entries.

(a) Give the IP prefix notation that your colleague uses to represent these two networks.

> `18.0.0.0/8` and `128.112.0.0/16`

(b) After you install the forwarding table entry your colleague suggests, you notice that you still see traffic for host 18.255.255.254, but you’ve stopped seeing any traffic for hosts 18.0.0.1 and 18.0.0.254. So, you come up with a new set of forwarding-table entries – three this time – that, once installed, causes you to receive traffic for all five hosts. What are these three IP prefixes?

> `18.0.0.0/8`, `18.0.0.0/24`, and `128.112.0.0./16`

(c) Give one possible explanation why this change in part (b) is needed.

> 18.0.0.0/24 is multi-homed from another provider and, given longest prefix matching for preferred traffic, all traffic was going through its other provider.
>
> Similarly, some other ISP (perhaps again for multi-homing) could be announcing any prefix > 8 bits, e.g., 18.0.0.0/16

4(2) [ 4 points ] Ethernet and IP

(a) Suppose Ethernet was the only existing LAN technology, so every host in the Internet was part of a local Ethernet and thus had a globally-unique Ethernet address. Would you recommend getting rid of IP addresses by simply using Ethernet addresses instead of IP addresses? Why or why not?

> No. It would not scale due to (1) the need for broadcast for discovery and (2) forwarding tables would be large as MAC addresses are not topologically assigned and thus cannot be aggregated.

(b) What about the other way around, why do we not simply assign IP addresses to network adaptors, instead of dealing with both Ethernet and IP addresses?

> No. Either you keep topological aggregation but then require adaptors to get manually reassigned an IP address whenever moving (a configuration nightmare), or adaptors have static IP addresses but then you would sacrifice routing table aggregation (a scalability nightmare).

4(3) Using TCP, a sender has sent out packets 1 through 20. The sender receives an ACK for packet 10, then it receives three ACKS for packet 11 (i.e., if the final byte of packet 11 was byte no. 5000, then these ACKs were for byte 5001). Given this result:

(a) Which of the 20 packets can the sender assume are lost?

> 12

(b) Which of the 20 packets can the sender assume were definitely received?

> 1 - 11

Now, the same sender resends the next missing packet and receives an ACK for packet 16 in response. Based on this information:

(c) Which packets of the original 20 can the sender assume are still lost, if any?

> None

(d) Which of the original 20 can the sender assume were definitely received?

> 1-16

4(4) [ 5 points ] Assume you have a network with three hosts – A, B, and C – all directly connected to the same switch. Host A first attempts to open a TCP connection to B at time 0, during which time he adds an entry to his ARP cache with a TTL of 60 seconds. Host B begins transferring a large file to host A. A new host D connects to the network, but is configured with the same IP address as already being used by A.

<img src="assets/image-20260504150341701.png" alt="image-20260504150341701" style="zoom: 33%;" />

At time 55 seconds, an application running on host D opens a TCP connection to an application on C. A few seconds later, the TCP transfer between hosts A and B breaks. What were the steps that led to this connection breaking?

> At time 60, host B’s ARP cache expires, so when it re-issues an ARP request for the IP address shared by A and D, D’s answer is cached by B. Thus, B’s TCP packet gets sent to MAC-D, who, not having such an open TCP connection, will reply with a TCP-RST, causing B’s connection to break. (Similar for A and its ARP cache)

4(5) [ 6 points ] What transport layer protocol (TCP or UDP) you would use if your application needed one of the following properties and then give one succinct reason why. Be specific.

> (a) Speed - UDP – no connection setup or sender-side buffering
>
> (b) Long messages – TCP – as stream-of-bytes abstraction supports arbitrarily long messages. Many stacks limit UDP messages to some maximum size (e.g., 64KB)
>
> (c) Short-duration interactions – UDP – No connection setup delay
>
> (d) Fairness between competing flows – TCP – Fairness through congestion control
>
> (e) Flooding – UDP – No connection state needed
>
> (f) Flexibility – UDP – More application-level control

5. Multiple choice (17 points)

5(2) When a UDP segment arrives at a host, in order to direct the segment to the appropriate socket, the operating system’s network stack uses the following fields: (circle ALL that are true – 2 points)

(a) the source IP address.
***(b) the destination IP address***
(c) the source port number
***(d) the destination port number***

5(3) When a TCP segment belonging to an existing connection arrives at a host, in order to direct the segment to the appropriate socket the operating system’s network stack uses the following fields (circle ALL that are true – 2 points)

***(a) the source IP address.***
***(b) the destination IP address***
***(c) the source port number***
***(d) the destination port number***

### Spring 2010 Final

> PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring10-cos461-exam2.pdf>


Derived answers are supplied below based on the exam prompt and figures.

1. Network system engineering (13 points)

You have recently been hired by FinBook, the online social network for fish. FinBook currently runs on a single server. To support future growth, you hope to deploy multiple servers in multiple datacenters located at different points in the Internet, with a special focus on providing good performance and failure recovery. List some of the pros and cons of using each of the following technologies. Try to give the “best answer” and be specific. Vague comments such as “low overhead” will not get credit (overhead in terms of what?).

1(a) HTTP redirection

1 advantage:

1 disadvantage:

> Advantage: HTTP redirection can choose a server on a per-request basis using current load, failure state, or client location.
>
> Disadvantage: The client must first contact the redirecting server, which adds an extra HTTP round trip and makes that server a dependency.

1(b) DNS server-selection

1 advantage:

2 disadvantages:

> Advantage: DNS server-selection is transparent to clients and can direct the client to a nearby or available datacenter before the TCP connection is opened.
>
> Disadvantages: DNS caching makes failover and load changes slow unless TTLs are short, and the DNS server often sees the recursive resolver rather than the true client, so location-based selection can be inaccurate.

1(c) IP anycast

2 advantage:

2 disadvantages:

> Advantages: IP anycast is transparent to clients and can work for multiple application protocols; routing naturally directs traffic to a topologically close live site.
>
> Disadvantages: routing changes can move a TCP/session flow to a different replica, and operators have only coarse control over load balancing and debugging because selection follows routing policy.

1(d) NAT + load-balancer

1 advantage:

1 disadvantage:

> Advantage: a NAT/load-balancer can expose one public address while spreading connections across multiple backend servers without client changes.
>
> Disadvantage: the NAT/load-balancer is stateful and can become a bottleneck or single point of failure.

1(e) ARP spoofing (unsolicited announcement of your MAC with other’s IP address)

1 advantage:

1 disadvantage:

> Advantage: ARP spoofing can move a service IP to a different machine on the same LAN without changing DNS or routing.
>
> Disadvantage: it only works on the local layer-2 network and can confuse ARP caches, hijack traffic, or blackhole connections.

2. More network system engineering (13 points)

2(a) You graduated from Princeton (yay!) and joined a social media startup that wants to rival Facebook (at least you hope). The startup doesn’t have any funding, so you took your implementation of simple router and are running it on a Linux box, using it as a router for your servers (instead of paying $$ to Cisco). As your company scaled, you started seeing some clients that use IPv6. Your servers understand IPv6, but your router doesn’t. Describe two ways in which you can extend your router to handle IPv6 traffic:

Option 1: (answer <= 2 lines)

Option 2: (answer <= 2 lines)

> Option 1: add native IPv6 forwarding support: recognize IPv6 frames, parse IPv6 headers, and maintain a forwarding table over 128-bit IPv6 prefixes.
>
> Option 2: tunnel IPv6 through IPv4 across the IPv4-only router, with encapsulation before the router and decapsulation after it.

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

> Packets are caught in a routing loop: identical packets for `69.65.28.126` appear multiple times with lower TTL values. They will keep looping until their TTL expires.

3. Distance-Vector Routing (9 points)

The CS department at Princeton bought new Sun Fire V210 servers. They decided to run a distance-vector protocol for routing between these servers (even though it is a rather small network). They are currently configured as the picture below, with respective edge costs.

<img src="assets/image-20260504155906734.png" alt="Figure transcription: the topology has links $A-B=21$, $A-D=15$, $B-C=18$, $B-D=12$, $C-D=5$, $C-E=11$, and $D-E=17$." style="zoom:50%;" />

The CS staff asked for your help. Write down each step of building the distance-vector routing table for ‘Eve’ so they can compare it to the output of their implementation. You can use abbreviations e.g., ‘A’ for Adam and ‘E’ for Eve.

The initial routing table at node A is:

| Destination | Cost | Next Hop |
| ----------- | ---: | -------- |
| B | 21 | B |
| C | ∞ | --- |
| D | 15 | D |
| E | ∞ | --- |

> Distance-vector 的更新公式是：
>
> $$
> D_E(X) = \min_{v \in N(E)} \{ c(E,v) + D_v(X) \}
> $$
>
> 其中 $N(E)=\{C,D\}$，因为 Eve 只直接连到 C 和 D。

3(a) Show the initial routing table of node E:

> | Destination | Cost | Next Hop |
> | ----------- | ---: | -------- |
> | A | ∞ | --- |
> | B | ∞ | --- |
> | C | 11 | C |
> | D | 17 | D |

3(b) Show the routing table of node E after one iteration of the algorithm:

> | Destination | Cost | Next Hop |
> | ----------- | ---: | -------- |
> | A | 32 | D |
> | B | 29 | C or D |
> | C | 11 | C |
> | D | 16 | C |

3(c) Show the routing table of node E after two iterations of the algorithm:

> | Destination | Cost | Next Hop |
> | ----------- | ---: | -------- |
> | A | 31 | C |
> | B | 28 | C |
> | C | 11 | C |
> | D | 16 | C |

3(d) In some failure situations, the administrator notices that it takes an exceptionally long time for the routing protocol to stabilize in this network.

3(d)(1) What problem with the distance vector protocol is the cause?

> The count-to-infinity problem.

3(d)(2) The administrator is told that RIP does not suﬀer from this problem. Do you agree? Why or why not?

> No. RIP can still suffer from count-to-infinity; it only **limits** the damage by defining infinity as 16 and using techniques like split horizon / poison reverse, which reduce but do not completely eliminate the problem.

4. Routing, addressing, and tunneling (9 points)

The above figure shows a network topology connecting two LANs. The LAN on the left uses a NAT to connect to the Internet and includes a client host H1. The LAN on the right includes a webserver H2. Packets between the two LANs are routed along the path shown by a heavy dark lines, which includes both an IP tunnel and an MPLS tunnel. All packets which traverse the path use both tunnels. The various network interfaces have IP and MAC addresses as shown.

<img src="assets/image-20260504160632777.png" alt="H1: 10.0.0.2 / MAC 1
NAT inside: 10.0.0.1 / MAC 2
NAT outside: 1.2.3.4 / MAC 3
Left-side router-facing link: 1.2.3.5 / MAC 4
IP/MPLS path labels: 1.2.3.6 / MAC 5, 1.2.3.7 / MAC 6, 1.2.3.8 / MAC 7,
                  1.2.4.1 / MAC 8, 1.2.4.2 / MAC 9, 1.2.4.3 / MAC 10,
                  1.2.4.4 / MAC 11, 2.0.0.1 / MAC 12, 2.0.0.2 / MAC 13
Right-side LAN/router labels: 3.0.0.1 / MAC 14, 3.0.0.2 / MAC 15,
                              3.0.0.3 / MAC 16, 3.0.0.4 / MAC 17
H2: 3.0.1.2 / MAC 18" />

H1 has established an HTTP session with web server H2 and data packets are flowing between the two machines. As an example, we have filled in the headers for packet 1 (traveling from the server H2 to the client H1). If there shouldn't be any source or destination field for the header type, write an "X" in that table entry.

| Header Type | Source | Destination |
| ----------- | ------ | ----------- |
| Ethernet | MAC 16 | MAC 15 |
| IP | 3.0.1.2 | 1.2.3.4 |

You have to fill in the header type and the source and destination address for the network and data-link layer headers for packets 2, 3, 4, and 5 (these packets are all traveling from the client H1 to the server H2). Note: You might not need to use all the rows supplied.

4(a) Header for packet 2:

> | Header Type | Source | Destination |
> | ----------- | ------ | ----------- |
> | Ethernet | MAC 1 | MAC 2 |
> | IP | 10.0.0.2 | 3.0.1.2 |

4(b) Header for packet 3:

> | Header Type | Source | Destination |
> | ----------- | ------ | ----------- |
> | Ethernet | MAC 3 | MAC 4 |
> | IP | 1.2.3.4 | 3.0.1.2 |

4(c) Header for packet 4:

> | Header Type | Source | Destination |
> | ----------- | ------ | ----------- |
> | Ethernet | MAC 9 | MAC 10 |
> | MPLS | X | X |
> | IP | 1.2.3.6 | 2.0.0.1 |
> | IP | 1.2.3.4 | 3.0.1.2 |

4(d) Header for packet 5:

> | Header Type | Source | Destination |
> | ----------- | ------ | ----------- |
> | Ethernet | MAC 11 | MAC 12 |
> | IP | 1.2.3.6 | 2.0.0.1 |
> | IP | 1.2.3.4 | 3.0.1.2 |

> ```
> Ethernet header: 每一跳都会变，因为它只负责当前链路上的 next hop。
> IP header: 端到端的内层 IP 通常不变；NAT 会改源 IP。
> Tunnel header: 外层 IP / MPLS 是为了穿过 tunnel 临时加的。
> ```

### 2009 Mid

> PDF: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring09-cos461-exam1-answers.pdf>


1. Transporting a file (15 POINTS)

Suppose your boss calls you up while visiting a client and says he left a 250,000 byte file on a server at the office, and he needs you to send it to him. The connection between the office and his current site is 2 million bits/second.

1(a) [2 points] Assuming that all bandwidth is consumed by your data (e.g., there aren’t any packet headers, there’s no other traffic on the link, etc.) and that you can immediately start sending data at the maximum rate, how long will it take to transmit the file? (Easy)

> 250,000 bytes * (8 bits / 1 byte) / 2,000,000 bits/s = 1 second

1(b) [5 points] Now assume that you are sending the file via TCP, with a maximum segment size of 1000 bytes. You have to follow TCP’s transport algorithm, so you start transmitting the file at a low rate. How many network round trip times (RTTs) will it take to transmit the entire file? Again assume that all bandwidth is consumed by your data.

> TCP needs to first establish a connection via a handshake (SYN/SYN-ACK) - **1 RTT** 
>
> TCP then enters slow-start to transmit the file, so we run slow-start either until we've transmitted the file or until we experience a loss (at 2Mbps). In slow-start, TCP will initially transmit a window of 1 MSS (=1000 bytes) per RTT, then double the window size each round (RTT). So, we have:
>
> 1 MSS, 2 MSS, 4, 8, 16, 32, 64, 128
>
> The sum of the above 8 transfers is 255 MSS = 255,000 bytes > 250,000 byte file, so we declare ourselves finished after the 8th RTT.
>
> Thus, the total time to transmit the file would be 1 + 8 = 9 RTT.
>
> Note: One might debate what "transfer" means, so we also accepted 7.5 RTTs for the number of runs in slow-start, as the final transfer of 128 might not strictly need to ACK. We did not take off any points if people also included 1 RTT for FINs.

1(c) [4 points] Let’s now consider how TCP reacts when it encounters packet loss (the “basic” variant we learned in class). Your boss now wants you to transmit a much larger file (say, 1 GB). This time around, after TCP reaches an instantaneously transmission rate of 32,000 bytes per second, you notice that a single packet is lost. Assuming that you don’t currently have any other packets in transmission, what is the instantaneous rate TCP will send at after noticing that loss? How long (in terms of RTTs) will it take to reach 32,000 bytes per second again?

> This question was meant to seek how TCP reacts to detecting loss via a triple duplicate ACK. In that case, TCP reacts by "MD" -- multiplicative decrease -- cutting its window size by half and continuing by "AI" -- additive increase.
>
> So the next transmission rate is 16,000 bytes per second, and it will take **16 RTTs** to recover to its prior levels (each RTT increases by 1 MSS = 1000 bytes).

1(d) [4 points] In the previous example of 1(c), would anything be different if all packets were lost after you reached 32,000 bytes per second, instead of just a single packet? If so, what is the next instantaneous rate TCP will send at in this example, and how long (in terms of RTTs) would it now take to reach 32,000 bytes per second again?

> Because all packets are lost, we only detect loss through a timeout. This causes the sender's window to be reduced to a single MSS (1000 bytes / RTT), at which time it enters "slow-start restart". Namely, it will perform slowstart until half of its prior cwnd (16,000 bytes/second), then do additive-increase from 16,000 to 32,000 bytes/second.
>
> (In fact, the question as written didn't include quite enough information, as you actually do need to know the RTT in this example in order to calculate the window size for "16,000 bytes / seconds", i.e., if RTT is 500ms, window size is 8 MSS/RTT, while window size would be 16 MSS/RTT if RTT is 1s. Everybody just assumed implicitly that RTT=1s, and that the next rate after the timeout was 1000 bytes/sec. We initially had written these questions with an explicit RTT and asked you to solve the question in terms of time, rather than RTTs, but subsequently removed this information to reduce needed calculations.)
>
> That said, assuming RTT=1s, then the answer is: Slow-start from 1 MSS to 16 MSS = 4 RTTs, then additive increase 16-32 MSS = 16 RTTs Total = **20 RTTs** (we also accepted 21 RTTs given various ways to "count" these values)

2. Sockets (16 POINTS)

2(a) [10 points] In the first assignment, you used the socket API to write a simple client/server. For this question, there is a single client communicating with a single server using TCP. The client sends a very small amount of data using the send() function, and the server receives the data with a recv() call. Each of the following scenarios shows a diﬀerent order in which the socket calls are called on both the client and the server.

Assume all system calls are blocking, and there may be some latency between the client and server. We write the system call when it is initiated by the client and/or server; it returns sometime between then and when the next local system call is executed.

For each scenario, answer the following: Can the server ever get the data sent by the client? (Yes or No). If not, explain why not.

```text
i)
Client      Server
            socket()
socket()
            bind()
connect()
            listen()
send()
            accept()
close()
            recv()
            close()
```

> No. connect() wouldn't successfully return, allowing you to send(), before client accepts().

```text
ii)
Client      Server
socket()
connect()
send()
            socket()
            bind()
            listen()
            accept()
            recv()
close()
            close()
```

> No. Same explanation as (i). Also valid reason is that server isn't listening() when client attempts to connect().

```text
iii)
Client      Server
            socket()
socket()
            bind()
            listen()
            accept()
connect()
send()
            recv()
close()
            close()
```

> Yes.

```text
iv)
Client      Server
socket()
            socket()
            bind()
            listen()
            accept()
            recv()
connect()
send()
close()
            close()
```

> No. Accept() wouldn't return with a valid file descriptor until client has connected().

```text
v)
Client      Server
socket()
            socket()
connect()
            bind()
            listen()
            accept()
            recv()
send()
close()
            close()
```

> Yes.

2(b) [3 points] Suppose application A is using a stream (TCP) socket to transfer data to application B on a remote host. Suppose application A writes (sends()) data into the socket buffer ten times.

i) Can the underlying network stack transmit more than ten data packets? If so, why?

> Yes. If a write is larger than the MSS, then TCP might transmit it within two packets. Certainly if your total number of written data is larger than 10 MSSs, you are guarnateed to have more than 10 TCP packets. (Also accepted as a valid answer, though not what we were expecting, was that additional packets could be caused by packet retransmission from loss.)

ii) Can the underlying network stack transmit fewer than ten data packets? If so, why?

> Yes. Small writes can be coalesced into single data packets using Nagle's algorithm.

2(c) [3 points] Suppose application A is using a datagram (UDP) socket to transfer data to application B on a remote host. Suppose application A calls sendto() ten times.

i) Can the underlying network stack transmit more than ten data packets? If so, why?

> Yes. UDP packets larger than the network MTU will experience IP fragmentation.

ii) Can the underlying network stack transmit fewer than ten data packets? If so, why?

> No.

3. Your Web Browser in action (17 POINTS)

In the topology shown below, machine A is a desktop client, D is a local DHCP server, R is A's gateway router, S is a Web server, and C is a Web cache. $N_L$ is C's local nameserver, while $N_A$ is the nameserver authoritative for S. Client A is configured to use Web cache C for all requests (assume that the Web cache resolves the name for any Web server and that the client is configured with the IP address of the cache). All wires/links are Ethernet segments.

<img src="assets/image-20260504163834277.png" alt="image-20260504163834277" style="zoom:50%;" />

Assume the following:

- All the machines were just booted and their associated caches (ARP, DNS, Web, persistent connections) are all empty
- http://S/index.html fits in a single packet
- Persistent HTTP connections are used among A, C, and S (i.e. you should assume that once any connection between these hosts is established it is never closed)
- Web caches respond to TCP requests that look like packet two in table 1 below (e.g., GET http://foo/bar/). They reply with the normal web cache contents.

3(a) [12 points] The user on machine A, requests the web page http://S/index.html. The table below shows a number of messages sent/received in servicing this request (this is not necessarily a complete list of all packets). In addition, there are a few bogus packets that are never sent/received. The packets are not listed in temporal order.

| ID | SRC | DST | SRC Port | DST Port | Protocol | Contents |
| -: | --- | --- | -------- | -------- | -------- | -------- |
| 1 | C | DNS root | | DNS | UDP | Query for S |
| 2 | A | C | | Web cache | TCP | GET http://S/index.html |
| 3 | $N_L$ | DNS root | | DNS | UDP | Query for S |
| 4 | C | S | | HTTP | TCP | SYN |
| 5 | C | S | | HTTP | TCP | GET index.html |
| 6 | S | A | HTTP | | TCP | index.html |
| 7 | A | Broadcast | | | ARP | Who is R |
| 8 | C | A | Web cache | | TCP | index.html |
| 9 | $N_L$ | C | DNS | | UDP | Address for S |
| 10 | S | C | HTTP | | TCP | index.html |
| 11 | A | Broadcast | | DHCP | UDP | DHCP Request from A |
| 12 | $N_L$ | $N_A$ | | DNS | UDP | Query for S |

List the proper order of packets (in terms of their IDs) that are sent on the network:

> 11, 7, 2, 3, 12, 9, 4, 5, 10, 8
>
> | ID     | SRC   | DST       | Protocol | Contents                |
> | ------ | ----- | --------- | -------- | ----------------------- |
> | **11** | A     | Broadcast | UDP      | DHCP Request from A     |
> | **7**  | A     | Broadcast | ARP      | Who is R                |
> | **2**  | A     | C         | TCP      | GET http://S/index.html |
> | **3**  | $N_L$ | DNS root  | UDP      | Query for S             |
> | **12** | $N_L$ | $N_A$     | UDP      | Query for S             |
> | **9**  | $N_L$ | C         | UDP      | Address for S           |
> | **4**  | C     | S         | TCP      | SYN                     |
> | **5**  | C     | S         | TCP      | GET index.html          |
> | **10** | S     | C         | TCP      | index.html              |
> | **8**  | C     | A         | TCP      | index.html              |

3(b) [5 points] Assume that the client A has no local Web or DNS cache and that cache C has no DNS cache. However, all other cacheable things are cached. On a subsequent request for http://S/ index.html, which of your items from your list in 3(a) would be eliminated? (Use the ID column to name the messages.)

> 11, 7, 3, 12, 9, 4, 5, 10
>
> (The trickiest number was 9, because we said that C doesn't have a DNS cache. However, if it has the object for http://S/index.html cached, it can serve it directly there without going to server S, hence it never needs to do a DNS lookup on S in the first place.)
>
> | ID    | SRC  | DST  | Protocol | Contents                |
> | ----- | ---- | ---- | -------- | ----------------------- |
> | **2** | A    | C    | TCP      | GET http://S/index.html |
> | **8** | C    | A    | TCP      | index.html              |

4. A routed and bridged network (14 POINTS)

<img src="assets/image-20260504164541738.png" alt="image-20260504164541738" style="zoom:50%;" />

Above is a picture of a network with 2 bridges and 1 router. Each interface is labeled with both an IP address and a MAC address. Imagine that host H1 is sending a packet to host H2. Please answer the following questions about this figure:

> ```
> Bridge/switch 看二层 MAC。
> Router 改二层 next-hop MAC，但不改三层源/目的 IP。
> Host 发往异网段时，二层目的 MAC 是默认网关的 MAC。
> ```

4(b) Just before the packet reaches bridge B1, what is its layer 2 destination?

> R2a.mac

4(c) Just before the packet reaches bridge B2, what is its layer 2 source?

> R2c.mac

4(d) Just after the packet leaves router R2, what is its layer 3 source?

> H1.ip

4(e) When H1 sends out an ARP query, what is the reply to that query?

> R2a.mac has R2a.ip (or just "R2a.mac")

5. Multiple choice (16 points)

Correct answers are marked in bold and underlined.

5(f) Which of the following is/are true about DNS? (Circle ALL that are correct)

**A. A query for an A record may return multiple IP addresses in the response.**
B. A query for an NS record may return multiple IP addresses in the response.
**C. A short TTL on an NS record reply runs the risk of increasing traffic at the root or GTLD nameservers.**
D. A short TTL on an A record reply runs the risk of increasing traffic at the root or GTLD nameservers.

6. Short Answer (22 points)

6(b) [2 points] List a protocol that use exponential backoff, and describe what/where problems would occur if it did not backoff.

> TCP congestion control uses exponential backoff (multiplicative decrease). If it did not backoff, congestion would build up at routers, and queues would continue to be full and continue to drop packets, leading to low throughput.
>

6(c) [3 points] List three possible explanations for why host A would need to retransmit the SYN packet as part of establishing the TCP connection with B.

> SYN packet from A to B dropped by router on path. SYN packet dropped by B because B's receive backlog is full. SYN-ACK packet from B to A dropped by router on path. SYN-ACK not received by A before timeout occurs. SYN dropped by firewall or NAT in front of B.

6(d) [1 point] Give one reason that DNS lookups are run over UDP rather than TCP

> DNS is a simple query/response protocol, thus avoids connection setup (at least 1 RTT) for TCP and its state overhead. This is especially true as DNS queries and responses are typically small and can thus often fit in a single packet. Because its a connectionless protocol, also more amenable to anycast IP addresses for DNS servers, useful for failover. UDP headers are also smaller than TCP headers, which reduced bandwidth overhead for queries.

6(e) [2 points] Give two reasons that sites use Network Address Translators (NATs):

> Allows multiple private addresses behind single public (dedicated) address, which is very helpful if sites lack a sufficient number of public IP addresses (e.g., "space" pressure). In general, NATs have helped "scale" IPv4.
>
> NATs provide privacy about internal deployments.
>
> NATs can allow easily management of internal devices, so that machines can be internally renumbered without changing their external (public) addresses.
>
> If explicit forwarding rules aren't configured in NATs, they often provide some security mechanisms by playing the role of firewalls, e.g., only allowing TCP connections to be initiated from internal nodes, as opposed to allowing external machines to connect to internal machines.
>
> ...

6(f) [3 points] When a packet is going from a local-area network onto the wider Internet, what header fields might a Network Address Translator (NAT) change that is deployed on path?

> source IP address, source port, IP checksum, transport (TCP/UDP) checksum

6(h) [4 points] The OSI model is traditionally seen as a 7-layer stack consisting of the following. For several of the layers, give one or two examples of protocols that are associated with each layer:

| Layer | Examples |
| ----- | -------- |
| Application | 2 examples: FTP, HTTP, SMTP, telnet, SIP, ... |
| Presentation | |
| Session | |
| Transport | 2 examples: TCP, UDP, DCCP, ... |
| Network | 1 example: IPv4, IPv6 |
| Data link | 2 examples: Ethernet, PPP, token ring, FDDI, 802.11 |
| Physical | 1 examples: We accepted both physical techologies (twisted pairs, CAT5, fiber, ...) and encodings (Manchester, NRZ, ...) |

### Spring 2008 Mid

Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring08-cos461-exam1-answers.doc>


1. Big MAC (15 points)

This question explores whether the Internet could be designed using only names (like www.frieswiththat.com) and MAC addresses, without a need for IP addresses.  Suppose each network adapter, for any link technology, has a unique MAC addresses from a single address space (such as 48-bit MAC addresses used for Ethernet devices), and these addresses were used Internet-wide for communication between end hosts.  Suppose that the Domain Name System (DNS) is changed to return MAC addresses rather than IP addresses, in response to queries.

1(a) In today’s Internet, why is it difficult to support continuous communication with a host while it moves?  Why would an Internet based on MAC addresses have the potential to make mobile hosts easier to support?

> Mobility is difficult to support in today’s Internet because a host’s IP address changes as it moves, since IP addresses are allocated to institutions in a hierarchical fashion.  Dynamic changes in the host’s IP address make it difficult to sustain a connection (e.g., TCP or UDP socket) with another host.  An Internet based on MAC addresses would allow the host’s identifier to stay the same as it moves.

1(b) Today’s local area networks have several “boot-strapping” techniques, such as DHCP, ARP, and MAC learning.  In a world without IP addresses, which of these techniques would still be necessary?  Explain your answer.

> DHCP would no longer be needed to assign an IP address or network mask to the host, though a similar mechanism may still be needed to configure the address of the local DNS server and the gateway router.  
>
> ARP would no longer be necessary, as there would be no need to map an IP address to a MAC address.  
>
> MAC learning would still be necessary to enable switches to learn how to forward frames to a host based on its MAC address.

1(c) How would moving to an Internet based on MAC addresses affect the size of the forwarding tables in the network nodes (i.e., routers or switches)?

> Forwarding tables could grow quite large because MAC addresses are not hierarchical.  Today, routers store ~200K IP prefixes that represent a much larger number of hosts.  Within a local area network, switch forwarding tables could likely stay the same size, as hosts could direct external traffic (destined to the rest of the Internet) to the gateway router.

3. Going With the Flow (10 points)

3(a) A home user upgrades from a dial-up connection to high-speed broadband, but does not see much improvement in Internet performance for visiting a Web site.  Give one reason why this might happen, even if the network and the Web server have ample capacity.

> The size of the receiver window (RWIN) may limit the throughput.  In particular, the throughput is limited by the RWIN/RTT, where RTT is the round-trip time between the host and the Web server.  The home user can improve performance by changing the maximum TCP receiver window (e.g., from 16 KB to 64 KB). 
>
> Also, most Web transfers are short (e.g., fewer than 10 packets long).  For these transfers, the download time is typically dominated by the round-trip time, as the TCP connection doesn’t get out of slow start and does not fill the receiver window.

3(b) When a path through the Internet becomes overloaded, the total “goodput” seen by all end users can actually decrease.  Explain why.

> When the network is congested, many packets travel part way through the network, only to be lost and ultimately retransmitted by the sender.  The wasted bandwidth may cause other packets to encounter congestion, and experience packet loss and subsequent retransmission, leading to an overall drop in the rate of successful packet delivery.

3(c) Why are many packet losses in wireless networks detected by a timeout rather than a triple-duplicate acknowledgment?  What are the performance implications?

> Wireless networks tend to experience bursty packet losses due to interference (e.g., signal blocked by a building).  This decreases the likelihood that, in the same TCP sending window, some packets are lost while others are successfully delivered.  The successful deliveries are necessary to trigger the receiver to send duplicate acknowledgments.  
>
> As such, bursty loss tends to require the sender to rely on the retransmission timeout to detect the loss.  
>
> (In addition, many wireless networks have relatively low capacity, leading the sender to have a relatively small congestion window.  This also decreases the likelihood that enough packets are successfully delivered to enable detection of an earlier packet loss by duplicate acknowledgments.  Similarly, wireless users may do smaller transfers, due to limited bandwidth or small screen sizes of PDAs, and small transfers offer less opportunity for multiple packets in flight during the same RTT.)

3(d) A router maintains a queue of packets awaiting transmission on a link.  Selecting the right buffer size is a challenging problem.  Give one reason why a large buffer would be desirable.  Give two reasons why a larger buffer might be undesirable.

> A larger buffer can temporarily accommodate a burst of packets without dropping any of them, avoiding unnecessary retransmissions.  
>
> However, a larger buffer would 
>
> (i) increase the round-trip time leading to higher and more unpredictable delays, 
>
> (ii) increase the time for the TCP senders to learn about impending congestion, and 
>
> (iii) make the router more expensive (due to more memory chips and higher power requirements).

4. Caught in the Web (15 points)

4(a) In the three-way handshake to open a TCP connection, host A sends a SYN, host B sends a SYN-ACK, and host A sends an ACK.  When can the TCP implementation at host A start sending data packets?  When can the TCP implementation at host B start sending data packets?  Explain why they cannot start sending any sooner.

> Host A can start sending upon receiving the SYN-ACK, since that signals to host A that B is willing to accept traffic and knows A’s initial sequence number.  
>
> Host B can start sending traffic upon receiving the ACK, since that signals to host B that A is willing to accept traffic and knows B’s initial sequence number.

4(b) HTTP/1.1 supports persistent connections, where multiple request-response exchanges use the same TCP connection.  With pipelining, the client might send multiple requests before receiving any responses. How does the server know where one request ends and the next begins?

> The server identifies request boundaries by parsing the HTTP requests, e.g., based on the CRLF and/or the Content-Length.

4(c) Following up on question 4(b), the underlying TCP implementation does not ensure that each read() or recv() call returns a single complete HTTP request.  Give two reasons (or examples) why the TCP implementation in the operating system cannot do this.

> The TCP implementation provides a stream-of-bytes abstraction, without any knowledge of the syntax of the application-layer message(s).  
>
> Also, the application-layer message may be larger than the operating system’s receiver buffer and/or the buffer provided by the application, making it impossible for the operating system to provide the entire request in response to a single read() or recv() call.  
>
> Also, it is possible that the full request (even if it could fit in the buffer) has not arrived yet, causing the read/recv call to return only the data that has arrived thus far.

4(d) Give two reasons why persistent connections and pipelining were added to HTTP/1.1.  Why, then, do Web browsers typically disable pipelining by default?

> These features were added to HTTP to 
>
> (i) avoid the extra TCP traffic needed to open and close many TCP connections, 
>
> (ii) avoid repeating slow start and the whole process of relearning the congestion state of the path through the network, 
>
> (iii) to ensure fairness across different Web clients receiving traffic over the same path, and 
>
> (iv) to reduce the number of round-trip delays experienced by the user in downloading a Web page. 
>
> Web browsers often disable pipelining because 
>
> (i) parallel connections may allow the client to experience higher throughput (possibly at the expense of other users) and 
>
> (ii) parallel connections enable the simultaneous download and display of multiple embedded images.

5. Losing Control (15 points)

The File Transfer Protocol (FTP) is an application-layer protocol used to transfer data from one computer to another.  FTP runs over TCP.  The server, by default, listens on port 21 for incoming connections.  The FTP client uses this connection as a “control” connection for sending commands (e.g., to list files, request file transfers, and change directories).  The actual file transfer uses a separate TCP connection.  Hence, unlike HTTP which has a single connection for both control and data, FTP has “out of band” control over a separate connection.

The client and the server need to agree on the port numbers to use for the separate data-transfer connection.  In one solution, called “active mode,” the client opens a socket with a dynamic port and sends the IP address and port number to the server (using the **existing control connection**) so the server knows what client address and port number to use for the data-transfer connection.  (For example, the client on IP address 192.168.0.1 that chose port 49152 for the data connection might send a command like “PORT 192.168.0.1 49152” over the control connection.)

5(a) Active mode can cause problems when the client host resides behind a NAT box.  Why?

> The NAT box maps the IP address and port number of the client’s data connection to new values.  As such, the arguments the client sends in the PORT command (sent over the control connection) would not match the values the NAT box would use.  
>
> In addition, the server would have trouble initiating a data connection to a client lying behind a NAT box, without the NAT box already having a table entry for the associated connection; since the client has not transmitted any packets on the data connection yet, the NAT box would not yet have an entry installed when the server sends the initial SYN packet.  
>
> Worse yet, the IP address in the PORT command is a private, non-routable address, so the FTP server would not be able to direct a packet with this destination address to the appropriate place.

5(b) Suppose a NAT box wanted to correctly handle clients running “active mode” FTP.  What actions would the NAT box need to perform on FTP control messages from the client?

> The NAT box would need to parse the messages sent on the FTP control connection (i.e., on port 21) to extract the arguments of the PORT command.  The NAT box would need to create a table entry for the data connection and modify the arguments in the PORT message accordingly, so the FTP server can successfully create and use the data connection.
>
> FTP-aware NAT:
>
> ```
> 1. 观察 FTP 控制连接，也就是 TCP port 21
> 2. 解析 TCP payload 里的 PORT command
> 3. 找出 client 想开的 data port
> 4. 分配一个公网地址和公网端口
> 5. 在 NAT table 里提前创建 data connection 的映射
> 6. 把 PORT command 改写成公网地址和公网端口
> ```

5(c) Why might these operations change the size of underlying IP packets associated with the control connection?  How could the NAT handle the change in packet sizes?

> The IP address and port numbers used by the NAT box may have a different number of decimal digits, when represented as the arguments in the PORT command.  As such, the NAT box must change the packet sizes, as well as the TCP sequence numbers (when sending to the server) and acknowledgment numbers (when directing return packets to the client) to remain consistent.  
>
> If the packet size increases, the new packet may exceed the MTU, requiring the NAT box to fragment the IP packets.

5(d) What challenges are introduced if other applications (besides FTP control) use port 21?  What challenges are introduced if the FTP client and FTP server encrypt their communications?

> If another application uses port 21, the NAT may mistakenly think the connection is an FTP control connection and try to parse the messages.  If the other application also sends the string “PORT”, the NAT box may mistakenly modify the packet contents, leading to unpredictable affects. If the FTP client and server encrypt their communications, the NAT box cannot parse the PORT command (in the payload of TCP connection) and correctly map the IP address and port number.  This can lead to significant confusion for users, when their FTP client works fine in the absence of encryption and then mysteriously does not work when encryption is enabled.
>
> 问题：它假设 port 21 一定是明文 FTP control traffic。

5(e) FTP has an alternate way to establish the data-transfer connection, called “passive mode,” where the server selects a port number and instructs the client (using the existing control connection) to establish the data-transfer connection.  Why is passive mode easier than active mode in the presence of client-side NAT boxes?

> In passive mode, the server selects an address and port number, and sends them to the client over the control connection.  The client-side NAT does not need to modify the address and port number used by the remote server.  (That said, passive mode is challenging in the presence of a server-side NAT box, though this is a much less common configuration.) If you are curious to learn more about the interaction of FTP and NAT, see http://en.wikipedia.org/wiki/File_Transfer_Protocol#FTP_and_NAT_devices

6. A Rose by Any Other Name (15 points)

This question explores the challenges of the Domain Name System.

6(e) A local DNS server typically discards cached name-to-address mappings when the time-to-live expires.  Alternatively, the local DNS server could optimistically issue a new query for the cached domain name (**prefetch**).  Given one advantage and one disadvantage of that approach.

> By “prefetching” the name-to-address mapping, the local DNS server can hide the DNS look-up delay, improving the performance experienced by the end user.  However, prefetching introduces extra DNS queries and network load to look up name-to-address mappings that may never be needed.

7. For Good Measure (15 points)

7(a) Traceroute capitalizes on the “Time To Live” field in the IP packet header to measure the forwarding path from one host to another.  Give two reasons why a hop in traceroute might show a “*” (i.e., no IP address for the router at that hop in the path).

> The packet may have been lost on the forward path. 
>
> The TIME_EXCEEDED packet may have been lost on the reverse path.
>
> The router may have been configured not to send TIME_EXCEEDED messages.
>
>  The packet may have encountered a firewall or NAT that drops the packet.

7(b) Traceroute may report a path that does not exist.  For example, traceroute could return a path A-B-C (where A, B, and C are IP addresses) when there is no link between routers B and C.  Give one example where that could happen.  (Draw a picture if useful.)

> The route to the remote destination may have changed during the measurement process.  For example, suppose the route from A to Z changed from A-B-Y-Z to A-D-C-Z.  Then, the first traceroute probe would return “B” and the second would return “C”, even though nodes B and C are not directly connected. Another possibility is that a middlebox (such as a transparent proxy or firewall) lies between B and C; these middleboxes do not typically decrement the TTL value or send TIME_EXCEEDED messages.

7(c) The delay between a TCP sender transmitting a SYN packet and receiving the SYN-ACK packet provides an estimate of the round-trip time between a client and a server.  Give one reason why, on average, the SYN/SYN-ACK delay is larger than a typical round-trip delay between a client and server.  Assume all DNS and ARP look-ups have already completed.

> The server may have a listen queue that stores pending requests to establish a TCP connection.  As such, the SYN packet may sit in the queue for some time before the SYN-ACK is sent.

7(d) Determining the geographic location of an Internet host, based on its IP address, is challenging.  Propose two techniques that could be used to infer the rough location.

> The DNS name, found by performing an address-to-name look-up, may reveal the location, e.g., “nslookup(12.122.16.158)” returns “tbr1.n54ny.ip.att.net”, which is at 54th street in Manhattan. 
>
> The whois database may reveal the location, e.g., “whois –h whois.arin.net 128.112.12.58” returns an entry with 87 Prospect Avenue in Princeton, New Jersey. 
>
> Sending probes (such as “ping”) from a host can reveal the round-trip latency to the remote destination.  Sending such probes from many vantage points can be used to “triangulate” the location of the remote host.
>
> Sending a traceroute to the remote host would reveal the names of many of the routers along the path.  The names of the routers near the destination would reveal the likely location of the host.

### Spring 2008 Final

Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring08-cos461-exam2-answers.doc>

| Page(s) | Subpart ID(s) retained | CSC4303 overlap                                           |
| ------: | -------------------------------- | --------------------------------------------------------- |
|     DOC | 1(a), 1(b), 1(c), 1(d)  | Link-state routing weights and shortest-path behavior     |


1. Weighting it Out (10 points)

This question explores how to set the (configurable) link weights in link-state routing protocols like OSPF and IS-IS inside a single Autonomous System (AS) to achieve AS-wide goals.

1(a) How should the network operators set the link weights if their goal is to minimize the number of hops each packet traverses to reach its destination? (2 points)

> All the weights should be set to the same value (e.g., “1”).

1(b) How should the operators set the link weights to minimize the end-to-end delay the traffic experiences?  Assume the network is lightly loaded, so queuing delay is insignificant. (2 points)

> Propagation delay is the only source of delay.  As such, the weight of each link should be set proportional to its length (i.e., its propagation delay).

1(c) In the picture below, the nodes are routers, the edges are links, and the integers correspond to the link weight on each direction of the link.  (That is, the link a-b and the link b-a both have weight 10.)  Put arrows on the edges to show the shortest path from every node to the destination node d.  That is, show the “sink tree” leading to node d. (2 points)

<img src="assets/image-20260504171602296.png" alt="image-20260504171602296" style="zoom:33%;" />

> Nodes a and g take a direct path to d.  The other nodes go left until they reach a, d, or g.

1(d) Suppose the link f-e is overloaded with traffic.  Identify a single weight change (on just one link) that would divert traffic from source f to destination d away from the f-e edge without affecting the path between any other source-destination pairs.  Avoid any reliance on how routers choose between multiple paths with the same (smallest) cost. (4 points)

> The h-i link should be changed to 2.  That makes the cost of path f-i-h-g-d decrease from 28 to 21, which is less than the cost 22 of the path f-e-d.

### Spring 2007 Mid

Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring07-cos461-exam1-answers.doc>


1. Internet Versus Station Wagon (15 POINTS)

A famous maxim, sometimes attributed to Dennis Ritchie, says “Never underestimate the bandwidth of a station wagon full of tapes.”  Suppose you need to deliver a large file between two computers that are 200 km apart and connected by a direct link.  This question analyzes when it is faster to drive the data between the two locations, rather than transmit the data?

1(a) Suppose the station wagon drives 100 km/hour and the link has a bandwidth of 800,000 bits/second.  And, suppose for simplicity that the data transfer can fully consume the link bandwidth, with no additional overhead (e.g., for headers or the TCP sawtooth).  At what file size (in bytes) does the station-wagon solution start delivering the data faster?  Show your work.

> By car, travel time is 2 hours (i.e., 200 km * 1hr/100km).  During two hours, the link could transfer 800,000 bits/sec * 60 sec/min * 60 min/hour * 2hr * 1byte/8bits for 720,000,000 bytes.

1(b) Suppose the sender transmits the data as packets with a 20-byte IP header, and 20-byte TCP header, and a maximum segment size of 512 bytes.  How much more time (as a fraction) would the data transfer take on the link?   (Ignore TCP congestion control and the link-layer header.)

> An MSS of 512 bytes and two 20-byte headers leads to a packet size of 552 bytes.  So, only 512/552 of the bandwidth is used to transmit the actual data, so the transfer takes 552/512 of the time, or 40/512 times longer.  This reduces to a factor of 5/64 longer time.

1(c) Suppose that, like the path traversed by the car, the link is 200 km long.  The speed of electricity in a copper cable is 200,000,000 meters/second.  How big does the receive window need to be to avoid becoming the main constraint on the transfer rate?  (Ignore the effects of header sizes, TCP congestion control, and packet loss, and assume that the receiver immediately sends an ACK packet after receiving each data packet and that there is no congestion.)

> The receive window needs to be large enough to accommodate a round-trip time of data.  The one-way delay is 1sec/200,000km * 200km, or 0.001 seconds (or 1 msec).  So, the round-trip time is 0.002 seconds (or 2 msec).  
>
> Since the link bandwidth is 800,000 bits/sec, the total number of bytes transmitted during a round-trip time is 0.002 sec * 800,000bits/sec * 1byte/8bits, or a grand total of 200 bytes.

2. Sockets (15 POINTS)

2(a) Suppose application A is using a stream socket to transfer data to application B on a remote host.  Suppose application A writes data into the socket buffer ten times.  Why might the underlying TCP implementation transmit more than ten data packets (not including retransmissions of lost packets, or control packets like SYN, ACK, or FIN)?

> If the application writes more than an MSS of data, a single write() call may lead to multiple TCP segments and, hence, multiple packet transmissions.

2(b) Why might the TCP implementation transmit all of the data in fewer than ten data packets?

> If the application writes less than an MSS of data, the data from multiple write() calls may be combined into a single TCP segment and, hence, a single packet transmission.  This is especially true in applications like Telnet, when Nagle’s algorithm is used.

2(c) Why can application A safely perform a close() on the socket when it is done writing the data, even if application B has not yet received all of the data?

> The TCP implementation (typically in the operating system) buffers the data and continues to (re)transmit the data to the receiver as needed.

2(d) List two possible explanations for why host A would need to retransmit the SYN packet as part of establishing the TCP connection with B.

> The SYN packet may have been lost in the network, discarded by the receiver due to a checksum error, or discarded because the receiver’s listen queue is full.  
>
> Or, the SYN-ACK packet may have been lost.  
>
> Or, the RTO might have been too small (e.g., for a very long-haul link to Mars).

2(e) Since a datagram socket (i.e., a UDP socket) does not require establishing a connection, why is a port number necessary?

> For demultiplexing the packet to the correct receiving socket.

3. Demultiplexing (10 points)

3(a) Suppose an organization runs a Network Address Translator.  When a packet arrives from the external Internet, what field(s) determine which internal IP address to use as the destination address for the packet?  What other fields in the IP and TCP/UDP header does the NAT change?

> When a packet arrives from the external Internet, the NAT box inspects the destination port number (and address, if the NAT has multiple external-facing IP addresses) to identify the receiving host.  
>
> The NAT changes the destination address and port, as well as the checksum.

3(b) Suppose the NAT then places the IP packet in an Ethernet frame to send to the receiving host.  How does the NAT know what destination MAC address to use?

> The NAT box checks in its ARP table for the MAC address corresponding to the internal destination address. If no match is found in the ARP table, the NAT box issues an ARP query to learn the associated MAC address.

3(c) Once the Ethernet frame reaches the destination host, how does the host know what network-layer protocol (e.g., IP, IPX, Appletalk) should be used to parse the payload?

> The Ethernet frame has a “type” field that identifies the network-layer protocol.

3(d) How does the operating system know if the packet is a UDP packet or a TCP packet?

> The IP header has a “protocol” field that identifies the transport-layer protocol.

3(e) How does the operating system know which process (and which socket) should receive the packet?

> The protocol field (in the IP header) and the destination port (in the transport-layer header) identify the receiving socket.

4. Cheaters Sometimes Win (15 points)

Many of the protocols underlying the Internet rely on end hosts to faithfully implement the protocols correctly, for the greater good.  This question explores what happens when they don’t.

4(c) Consider a TCP implementation that does not reduce its sending rate in response to packet loss.  Describe how this would affect the other TCP traffic sharing the congested link.  Also, explain whether/how this non-compliant behavior might hurt the performance of the offending TCP connection.

> By not reducing the sending rate in response to packet loss, the rogue TCP sender would not do its part to reduce congestion, forcing other packets to be dropped.  Eventually, well-behaved TCP senders would reduce their sending rates and share whatever bandwidth the rogue sender is not using.  This would lead to unfairness.  It may also hurt the rogue TCP sender because driving the link beyond its capacity may cause loss of the rogue sender’s packets, requiring retransmisisons.

4(d) Many Web browsers open several TCP connections in parallel when downloading multiple embedded images.  How does this affect the other TCP traffic sharing the same congested link?  When no other traffic traverses the links, is using multiple parallel connections still beneficial to the user?  Why or why not?

> The extra TCP connections allow the Web browser to have an unfair share of the bandwidth of the bottleneck link, reducing the throughput of other, well-behaved applications.  When no other traffic traverses the link, the multiple connections share bandwidth only with each other.  
>
> Still, this may be beneficial if the connections are RTT-limited, and because the user likes to see multiple embedded images fill in at the same time; also, the parallel connections collectively get more bandwidth during slow start.

5. Home-Network “Box” (15 points)

Consider a home network with multiple hosts plugged in (via Ethernet cables) to a Box that has a link directly to a residential broadband provider (e.g., via a DSL line).  Suppose the broadband provider assigns a single public address to each home.  This question explores the many functions that the Box implements.

5(a) The Box may, at different times, act as both a DHCP client and a DHCP server.  Why would it act as a client?  Why would it act as a server?

> The Box acts as a DHCP client to the DSL provider’s DHCP server, to get a public IP address.  The Box acts as a DHCP server to allocate private IP addresses to the internal hosts.

5(b) The Box serves as a gateway router for the hosts in the home network.  How do the hosts in the home network learn the IP address of the gateway?  Is this the same address as the single public address the provider allocated to the home?  Why or why not?

> The hosts in the home network learn the internal-facing address of the gateway via DHCP.  This is not the same as the external-facing address assigned by the ISP.  
>
> Typically, the ISP assigns an address from its own (public) address block, whereas the internal-facing address lies in the (private) address block used to number devices in the home network.

5(c) Suppose a host in the home network sends a TCP SYN packet to a Web server in the external Internet.  Explain the role of ARP and NAT in getting the first IP packet from the host through the home network and out the connection to the Internet.

> The host recognizes that the destination IP address of the packet falls outside of the local subnet and, as such, directs the IP packet to the gateway router (i.e., the Box).  
>
> The host uses ARP to determine the MAC address of the gateway, by consulting its ARP cache or, on a cache miss, issuing an ARP query).  
>
> Then, the host sends the Ethernet frame to the gateway (i.e., the Box).  
>
> The Box then maps the source address and source port, using a NAT table, before directing the traffic to the Internet.  (The Box may also use ARP to learn the MAC address of the DSL provider’s gateway router.)

5(d) Some Web sites on the Internet allow a home user to determine the public IP address the broadband provider has assigned to the home.  Why might it be hard for the end user to determine the IP address directly? How does the external Web site know?

> The end host learns the private (internally-facing) address of the NAT box, not the public (externally-facing) address.  In contrast, the Web server receives the HTTP request on a TCP connection from the public address of the NAT box and, as such, knows the public address.

6. Internet Principles (15 POINTS)

6(a) List one advantage and one disadvantage of using soft state over hard state.  Give two examples of the use of soft state from the protocols covered in class.

> Soft state is robust to a device that fails ungracefully and does not relinquish its state.  However, soft state wastes resources in repeatedly refreshing state.  
>
> Examples of soft state include the TTL in DNS caching, the lease time in DHCP, and the caching time for ARP entries and NAT bindings.

6(b) List one advantage and one disadvantage of using a text-based header (as in HTTP) instead of a binary format.  Why does IP use a binary format?

> A text-based header is easier for human beings to read and debug.  Text-based headers are also extensible.  However, they are verbose (i.e., waste bandwidth) and harder to parse.  IP uses a binary format to limit the bandwidth consumed by the header, and to simplify parsing at the router, which much process packets very quickly (e.g., within a few nanoseconds on high-speed links).

6(c) IP allows variable-sized packets.  List one advantage and one disadvantage of forcing all packets to be the same size.

> Fixed-sized packets do not need extra header space for a packet-length field, and they are easier to managed (e.g., fixed-sized buffers).  However, fixed-sized packets waste bandwidth due to padding when the data is smaller than the packet size.

6(d) List one advantage and one disadvantage of classless interdomain routing (CIDR) over the earlier use of classful routing.

> CIDR allows more efficient allocation of the limited address space, by permitting a wide variety of sizes of address blocks.  However, CIDR requires routers to perform longest-prefix-match forwarding, which is hard to do quickly.

6(e) List one disadvantage of having a TCP retransmission timeout (RTO) that is too large.  List one disadvantage of having an RTO this is too small.

> If the RTO is too large, the sender waits too long to retransmit a lost packet, leading to slower data transfers.  If the RTO is too short, the sender unnecessarily retransmits packets that were not actually lost, wasting network bandwidth.

7. Decentralized Control (15 points)

7(a) Why does a TCP sender decrease its sending rate (on a packet loss) more aggressively than it increases the sending rate (after successful packet delivery)?

> Overshooting the capacity of the path has dire consequences in terms of congestion collapse, whereas undershooting just makes the network a little less efficient than it otherwise would be.  The multiplicative decrease algorithm of TCP is crucial to its stability.

7(b) The way a TCP sender reacts to packet loss depends on how the loss was detected.  What are the two scenarios?  How does the TCP sender adapt its rate in each case?  Why are these two cases handled differently?

> When loss is detected by a timeout, the sender decreases the sending rate to 1 MSS and repeats slow start, assuming that network congestion is quite serious.  
>
> When loss is detected by a triple-duplicate ACK, the sender halves the sending rate, assuming that the congestion is not too bad.

7(c) Give two reasons why a local DNS server is not configured with the IP addresses of the top-level domain servers (e.g., for “.com” or “.org”).  How does the local DNS server learn the addresses of the top-level domain servers?

> The top-level domain servers may change over time, and new top-level domains (such as the country codes in recent years) may be added.  
>
> The local DNS server is configured only with the addresses of the 13 root servers, and contacts one of these servers to learn the address of the TLD server of interest.

7(d) List two reasons for the hierarchical allocation of IP address blocks in the Internet, from one institution to another.

> Hierarchical allocation reduces administrative overhead by allowing regional Internet registries to allocate large blocks to ISPs who, in turn, allocate smaller blocks to their customers.  
>
> Hierarchical allocation also improves the efficiency of the routing system since, often, these smaller address blocks do not need to be known globally, since the customers are reachable via their providers that own and announce the containing (larger) address block.

7(e) MAC addresses only have significance within the context of a local-area network.  So, why are MAC addresses globally unique?

> If two devices had the same MAC address, they might sometime reside on the same LAN, leading to mass confusion.  (More specifically, the self-learning switches might go back and forth in determining which way to forward frames, so sometimes one device would receive the frames and sometimes the other.  Bad scene all around, and very hard to debug.)

### Spring 2007 Final

Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring07-cos461-exam2-answers.doc>


1. Scalability of Peer-to-Peer Systems (15 POINTS)

The first three parts of this question explore the scalability of peer-to-peer systems, compared to client-server systems.  For this question, we assume that the interior of the network has ample bandwidth, and that propagation delay is infinitesimal.  The server has a 100 kbyte file that it wants to distribute to a group of 31 receivers. All hosts have bidirectional 40 kilobit/second links to the Internet – that is, they can upload and download 40 kilobits/second – and the core of the Internet is not congested.

1(a) What is the minimum time for the server to transmit the data to all of the receivers in a client-server configuration (i.e., where the receivers do not upload any content)? (3 points)

> The server must transmit the 100 kbyte (800 kbit) file to 31 receivers at a rate of 40 kbits/sec.  The total time is (31*100*8)/40, or a total of 620 seconds.

1(b) Now, suppose that the receivers can upload data, too, but only after receiving an entire copy of the 100 kbyte file.  What is the minimum time for the server and the cooperating peers to transmit the data to all receivers in this configuration? (3 points)

> The number of receivers with a copy of the file doubles after each full 100 kbyte transmission.  Each round takes (100*8)/40 = 20 seconds.  The number of rounds is log232 = 5.  (That is, 1 receiver completes in the first round, 2 in the second, 4 in the third, 8 in the fourth, and 16 in the fifth, for a total of 31 receivers.)  Hence, the total time is 20 * 5, or 100 seconds.

1(c) Now, suppose that a receiver can start uploading data to others after receiving the first 20 kbyte chunk of data.  How long does it take to deliver the data to all receivers? (3 points)

> Similar to question 1(b), the first 20 kbytes require five rounds to complete, where each round requires (20 * 8)/40 = 4 seconds to complete.  
>
> So, by the end of five rounds, 20 seconds (4 * 5) have elapsed, and every peer has the first 20 kbytes of data.  
>
> The remainder of the data transfer is pipelined, where the last peers download the remaining 80 kbytes as quickly as they can.  They need a time of (80 * 8)/40 = 16 seconds to download the rest, for a total of 20 + 16 = 36 seconds.

The remainder of this question focuses on BitTorrent.

1(d) Suppose there are many peers transferring chunks of the same large file – some broadband users with very high bandwidth and some dial-up users with very low bandwidth.  Why would the broadband peers exchange chunks mostly with each other, and similar the dial-up peers exchange mostly with each other? (2 points)

> Peers exchange with other peers that upload to them at a high rate.  Hence, broadband peers will exchange chunks with other broadband peers, leaving dial-up peers to exchange chunks with each other.

1(e) Why is BitTorrent vulnerable to incomplete downloads?  What steps are taken to prevent it? (2 points)

> After downloading the complete file, peers may leave the system rather than remaining to provide chunks to others. 
>
> The “rarest chunk first” policy increases the likelihood that each chunk is available from at least one active peer.  
>
> The “random chunk” policy also helps by distributing the chunks across the peers.

1(f) BitTorrent is primarily useful for popular files.  Suggest ways to extend BitTorrent to work better for less popular files. (2 points)

> Currently, BitTorrent’s incentive mechanisms apply to each file independently.  Instead, BitTorrent could provide incentives for peers to store chunks for less popular files, even if these peers are not interested in these files.  For example, the system could offer virtual currency that could be used to achieve faster downloads on the files these peers actually want.

2. Routing Protocols (20 POINTS)

The first two questions concern a shortest-path, link-state routing protocol running on the following network, where the numbers correspond to link weights:

<img src="assets/image-20260504174842927.png" alt="image-20260504174842927" style="zoom:33%;" />

2(a) Suppose the link between nodes k and m fails.  Before the failure, what is the shortest path from node i to node j?  What is the new path after the failure, when routing-protocol convergence completes? (2 points)

> Before the failure: i-k-m-j (cost 6) After the failure: i-r-n-j (cost 8)

2(b) A transient forwarding-loop might occur during routing-protocol convergence.  Involving what nodes?  List two examples of what would happen to the data packets sent from i to j during this period. (3 points)

> The nodes k and n may experience a forwarding loop, if k learns about the failure first and starts forwarding the packets along the path k-n-j, while n is still forwarding along the (old) path n-k-m-j.
>
> Some packets will be discarded when their TTL expires.  Others may eventually escape the loop, and experience high delay and arrive out of order.

4. Ethernet and Wireless (10 points)

4(a) Ethernet bridging relies heavily on flooding.  For example, broadcast traffic is flooded.  List two protocols that generate broadcast traffic, and explain why broadcasting is done.  (2 points)

> - ARP requests are sent to learn the MAC address associated with a particular IP address.  The machine sending the request has no idea where the destination machine is located and, as such, sends a broadcast packet to ensure the query reaches the machine with the target IP address.
>
> - DHCP: As part of boot-strapping, a host sends a DHCP request in the hope that a DHCP server will respond to assign an IP address, subnet mask, gateway address, and DNS server address.  The host has no idea what machines are serving as DHCP servers and, as such, sends a broadcast traffic to ensure one or more DHCP servers hear the request.

5. Overlay Networks (15 points)

5(d) Napster’s central directory and Gnutella’s query flooding represent two extremes in how to support queries for content in peer-to-peer file-sharing systems.  List two advantages and two disadvantages of the Napster approach over the Gnutella approach.  (4 points)

> Advantages: 
>
> A central directory leads to a simpler protocol, and reduces the overhead for processing queries (since queries go directly to the central server rather than hopping multiple times through an overlay, as in Gnutella). 
>
> Disadvantages: 
>
> The central directory is a single point of failure or attack.  Also, the central directory does not scale.  In addition, the central directory was a point of legal vulnerability for Napster.

6. Application-Layer Protocols (10 POINTS)

6(c) YouTube converts uploaded videos to Flash and makes them available for downloading via HTTP.  How has (i) using Flash format, (ii) using HTTP, and (iii) using TCP helped make YouTube so successful? (3 points)

> Flash is widely available and installed on end-host machines, obviating the need for YouTube users to install a new plug-in.  
>
> HTTP clients are widely available and used in Web browsers.  
>
> TCP runs under HTTP and also allows YouTube to work well through firewalls and NATs.

6(d) Web proxy caches and content distribution networks (CDNs) both reduce the time for a client to download Web pages by moving content closer to the users.  Give two reasons why CDNs have been more widely deployed (and successful) than Web proxy caching. (2 points)

> The content providers can contract with CDNs to deliver their content, which improves performance, reduces cost, and makes their site robust to unexpected surges in demand.  In contrast, the content provider cannot require millions of sites throughout the world to deploy proxy servers. 
>
> Also, proxies cannot cache all content.  Some content is uncacheable because it is dynamically generated.  CDNs can run the server software that generates the dynamic content.

7. Layering (10 points)

7(b) Within 30 minutes of the 9/11 attacks, the www.cnn.com Web site experienced a ten-fold increase in page views.  CNN changed the main page of the web site to text, taking great care to reduce the size to around 1000 characters.   Why this size? (2 points)

> The 1000 bytes would (coupled with the HTTP response header) fit in a single 1500-byte IP packet, reducing the load on the servers and CNN’s connection to the Internet.  This allowed them to satisfy more page-view requests per unit time during the period of heavy load.

7(c) IP routers operate at the network layer, yet sometimes they do inspect the transport-layer header (such as the TCP/UDP port numbers).  Give two reasons why this might be done. (2 points)

> Routers sometimes filter packets (or place them in different queues) based on the port numbers.  
>
> Also, routers may perform NAT functions requiring them to inspect and remap the port numbers.  
>
> The routers might also perform measurement functions that log the port numbers or collect per-flow statistics based on the port numbers.  
>
> Routers could conceivably punish flows that are not “TCP friendly” (i.e., that deviate from the AIMD congestion control rules), and this would require maintaining per-flow state and inspecting the port numbers of packets.

7(d) What protocol “layer” (application, transport, or network) does BGP operate at?  What about DNS?  (2 points)

> BGP and DNS are application-layer protocols.  BGP runs on top of TCP, and DNS runs on top of either TCP or UDP.

### Spring 2006 Mid

> Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring06-cos461-exam1-answers.doc>
> Answer DOC: <https://www.cs.princeton.edu/courses/archive/spr06/cos461/exams/midterm-answers.doc>


1. Transmission Overhead (15 POINTS)

<img src="assets/image-20260504175532826.png" alt="image-20260504175532826" style="zoom:33%;" />

Suppose A has a TCP connection with B, where A sends data packets and B sends ACKs; similarly, suppose D has a TCP connection with C, where D sends data packets and C sends ACKs.  Suppose the Maximum Segment Size (MSS) is 472 bytes, and all packets sent by A and D have this size; suppose also that B and C send an ACK in response to each data packet.  Suppose that all packets have TCP and IP headers, as well as a 20-byte link-layer header/trailer.  Assume the combined data and ACK packets fully utilize the middle link in both directions and no congestion control is applied.

1(a) What fraction of the bandwidth is consumed by data traffic (i.e., the TCP segments, rather than the transport, network, and link-layer information)?  Feel free to express your answer as a reduced fraction (e.g., ½ or ¾) rather than a decimal number.  Show your work.

> Each TCP packet has three headers (at the link, network, and transport layers) and an optional segment.  The link-layer header is 20 bytes, a TCP header is 20 bytes, and an IP header is 20 bytes, leading to 60 bytes of header.  
>
> An ACK packet contains no payload (i.e., no segment) and, as such, is 60-bytes long.  
>
> A full-sized TCP data packet includes MSS bytes (472 bytes in “part a” of the problem), in addition to the 60-byte header, resulting in 532-byte data packets.  
>
> So, sending one TCP segment of 472 bytes incurs 532 bytes for the data packet and 60 bytes for the corresponding ACK packet.  This leads to a ratio of 472/592, which simplifies to 59/74 – about 79.7% of the link bandwidth.

1(b) What if the MSS were increased to 1460 bytes?  What is the new fraction?

> As before, the equation is MSS/(MSS + 60 + 60), but now with an MSS of 1460.  The resulting fraction is 1460/1580, which reduces to 73/79 – about 92.4% of the link bandwidth.  Big savings!

1(c) What if the MSS were increased to 1460 bytes, and the receivers apply the delayed-ACK mechanism to send an ACK for every other data packet?  What is the new fraction?

> Now only half of the data packets incur the overhead of an ACK.  Sending two data packets transfers 2*MSS bytes of data, leading to 2*(MSS+60) bytes in the data packets and one 60-byte ACK packet.  
>
> The resulting fraction is 2*1460/(2*1460+120+60), which is 2920/3100, which reduces to 146/155 – about 94.2% of the link bandwidth.

2. Sockets (15 POINTS)

Consider a Web server that generates and sends HTTP response messages to clients over sockets.  The header of an HTTP response message consists of a collection of lines, each ending with a carriage return and line feed.  For example,

```text
HTTP/1.1 200 OK

Server: Apache/1.2.7-dev

Date: Tue, 07 Jul 1998 18:21:41 GMT

Content-Type: text/html
…
```

Some early Web-server software generated the lines one at a time, and used a separate system call to write (or send) each line to the socket.

2(a) Why is this approach inefficient for the end host?

> The server makes a separate system call for each line, leading to a high overhead for switching between the user-space process and the operating system.  The smaller packets arriving at the client may also require the browser to perform many system calls to receive the full header, if the packets do not arrive close together in time.

2(b) Why is this approach inefficient for the network?

> The resulting TCP segments are very small, in the same ballpark as the link-layer, IP, and TCP headers themselves.  A large fraction of the network bandwidth is consumed by the headers.  Also, the receiver must transmit ACK packets in response to receiving the data packets, leading to a large number of ACK packets.

2(c) Describe how a programmer implementing the Web server software could fix this problem.

> The programmer could create a large user-space buffer (e.g., at least 1460 bytes long, if not longer) and create the response header there.  Then, the programmer could make a single socket call to send the full header.  The operating system will then generate large packets containing multiple lines of data and send these larger packets into the network.

### Spring 2006 Second Mid

Answer DOC: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring06-cos461-exam2-answers.doc>
Answer DOC: <https://www.cs.princeton.edu/courses/archive/spr06/cos461/exams/midterm2-answers.doc>


1. UNDERGRADUATE STUDENTS: VNS Router (15 POINTS)

*** This question is only for the undergraduate students in the class – graduate students should skip this question and proceed to the next page. ***

Assume that the IP router in question is connected to an Ethernet network.

1(a) Describe three different scenarios when an IP router would drop packets that arrive on one of its interfaces.

> - Insufficient buffer space
> - No route for the destination
> - Badly formed packet (e.g., checksum error)
> - TTL expiry

1(b) List four fields of a packet that an IP router must modify before forwarding the packet to its next hop. Briefly describe how the router determines how to update the fields.

> - Source MAC address
> - Destination MAC address
> - IP time-to-live field
> - IP header checksum

1(c) What state does an IP router maintain about its directly-connected neighbors? How does the router maintain this state?

> - ARP cache (table of neighboring Eth/IP mappings)
> - ARP protocol (periodic refresh and in response to ARP requests)

## CMU 15-213 Introduction to Computer Systems

### Fall 2012 Final

> PDF: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f12.pdf>
Model solution TXT: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f12-sol.txt>

1. (18 points):
Multiple choice questions on a variety of stimulating and refreshing topics.

1(8) When can short counts occur?

(a) When an EOF is encountered during a read
(b) When a short int is used as a counter
(c) When reading or writing to disk files
(d) When the kernel runs out of kernel memory

> (a) When an EOF is encountered during a read.

### Spring 2011 Final

> PDF: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-s11.pdf>
Model solution TXT: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-s11-sol.txt>

1(18) True/False: When requested to send 20 bytes over a network socket, execution will block until all 20 bytes have been sent.

(a) True
(b) False

> (b) False.

### Fall 2010 Final

> PDF: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f10.pdf>
Model solution TXT: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f10-sol.txt>

1. (20 points):
Short answer and multiple choice questions on a variety of stimulating and refreshing topics.

1(1) Label the following networking system calls 1,2,3,4 or 5, in the order they should be called. [2 pts] (label with an X if the call is not used; a blank will receive no credit)

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

6. Network Programming (12 points):

6(a) Consider a logging daemon, whose purpose is simply to accept messages from clients and log them to a file. (This is sometimes used in secure networks to ensure that, even if a cracker breaks into one computer, he can’t erase his traces from the logs because they are stored elsewhere.) In the following table, please list the system and/or library calls that each side of the connection would make. Each row should contain the name of a single system or library call, placed in the appropriate column. Please list the calls in the order they are called, not the order they return. Please only include network-related operations (accept, bind, close, connect, listen, read, socket, and write). You should make the following assumptions:

- The server finishes initializing before the client starts.
- The server only serves a single client.
- The client already knows the server’s IP address.
- The client only sends one message before closing the connection.

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

6(b) Consider a simple network protocol for a webcam, in which a client connects to the server, and the server sends back 4096 bytes of image data. Suppose the client contains the following snippet of code to receive data from the server:

```c
#define IMAGE_SIZE 4096
...
char *image_buf = malloc(IMAGE_SIZE);
if (!image_buf) {
  fprintf(stderr, "Out of memory.\n");
  exit(1);
}
...
int err = recv(server_fd, image_buf, IMAGE_SIZE, 0);
if (err < 0) {
  fprintf(stderr, "Error reading from server: %s\n", strerror(errno));
  exit(1);
}
...
/* BUG: Even if malloc and recv succeed, sometimes the data in image_buf
   only partially matches the image the server sent. -- hqbovik */
```

What is the most likely cause of the bug?

> recv (like read) is not guaranteed to read a full 4096 bytes (i.e., it can return less as a "short read").  It needs to be placed in a loop.

### Spring 2009 Final

> PDF: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-s09.pdf>
Model solution TXT: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-s09-sol.txt>

6. (10 points):
Crummy Networks
6(a) Error Handling
Below is some code for a concurrent echo server. We have left out the error handling code for the three functions socket, send, and recv. These blanks are marked with

```text
/**** WRITE CODE BELOW *******/

  <and you have to fill in here>

/***** WRITE CODE ABOVE *****/
```

Please fill in those blanks with appropiate error handling code. Do not print out any messages, just modify the control flow.

```c
#include <stdio.h>
#include <pthread.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <stdio.h>
#include <signal.h>
#include <unistd.h>

#define BUFF_SIZE 512
#define SERVER_PORT 15213

char buffer[BUFF_SIZE];

void * handleConnection(void *);

int main() {
    int server_sock;
    struct sockaddr_in serverAddr, clientAddr;
    pthread_t tid;

    /*ignore the SIGPIPE signal*/
    signal(SIGPIPE, SIG_IGN);

    /*open server_socket */
    if((server_sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0) {
        /**** WRITE CODE BELOW *******/


        /***** WRITE CODE ABOVE *****/
    }

    serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);
    serverAddr.sin_port = htons(SERVER_PORT);
    serverAddr.sin_family = AF_INET;
    if(bind(server_sock, (struct sockaddr *)&serverAddr,
            sizeof(struct sockaddr)) < 0) {
        /*handle bind failing*/
        exit(-1);
    }
}

    if(listen(server_sock, 15) < 0) {
        /*handle listen failing*/
        exit(-1);
    }
    while(1) {
        int client_socket;
        size_t clientLen = sizeof(struct sockaddr);

        if((client_socket = accept(server_sock, (struct sockaddr *)&clientAddr,
            &clientLen)) < 0) {
            /*handle failing of accept*/
            continue;
        }
        pthread_create(&tid, NULL, handleConnection, (void *) client_socket);
    }
}

/*handle data on this socket*/
void * handleConnection(void * sock) {
    int socket = (int) sock;
    int recvSize;

    pthread_detach(pthread_self());

    do {
        if((recvSize = recv(socket, buffer, BUFF_SIZE, 0)) < 0) {
            /***** WRITE CODE BELOW *******/


            /***** WRITE CODE ABOVE *******/
        }

        if(send(socket, buffer, recvSize, 0) < 0) {
            /***** WRITE CODE BELOW *******/


            /***** WRITE CODE ABOVE *******/
        }
    } while(recvSize > 0);
    /*once the code reaches this point, we have received 0 bytes from the recv
     * call*/
    close(socket);
    pthread_exit(NULL);
}

```

> On socket error: exit(-1); On recv error: break; On send error: break;

6(b) Network Bugs
Assuming all system calls succeed (and therefore the error handling code you wrote in part A is never executed), please locate the 2 logic bugs in this code and describe them. (A logic bug is one where the programmer misunderstood the way in which their program will execute and will produce unwanted behavior under certain input conditions).

> Bug 1: buffer is a global variable and shared by all threads, there exists a race condition in reading and writing to the shared buffer.  Solving this race condition would require making buffer a local variable to handleConnection();
>
> Bug 2: send() is not guaranteed to send all of the buffer in one call.  This is referred to as a send short count.  You must examine the positive return values of send to verify that it did send all of the data, and resend if necessary.
