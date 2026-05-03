# Filtered Exam Source Snippets

## CMU 15-440/640 Distributed Systems / Mid Fall 2019

### Question 1(b)
- pages: 2
- overlap: VoIP transport choice
- source: <https://www.synergylabs.org/courses/15-440/assignments/Fall2019-Midterm-I-WithSolutions.pdf>

```text
1. Circle whether each statement below is true or false. ***ALSO***, give a one to two sentence reason for your answer. Each correct answer is worth 3 points (1pt for the T/F and 2pts for the reason).

(b) (3 points) [True, False] Over a wide area network it is better to use TCP to implement Voice-over-IP telephony rather than UDP given the potential for packet losses.

Solution: False - UDP is still going to be better for the VoIP app since VoIP is real time and the delays caused with TCP retransmision would make things worse. What’s more, VoIP is loss-tolerant.
```

### Question 2(a), 2(b)
- pages: 3
- overlap: RPC over UDP; RPC marshalling of pointer/linked data structures
- source: <https://www.synergylabs.org/courses/15-440/assignments/Fall2019-Midterm-I-WithSolutions.pdf>

```text
2. In the following, keep your answers brief and to the point (i.e., 2-3 sentences).

(a) (4 points) Can you implement an RPC system using UDP connections, instead of TCP? Answer yes/no and explain why or why not in at most two sentences.

Solution: Yes. It doesnt matter what transport layer protocol you choose for the RPC system. You can choose to implement over an unreliable network connection and rely on RPC system to detect and tolerate the failures.

(b) (4 points) A developer decides to use RPCs to remotely invoke the function Sum- LinkedList(ListItem *head). What problem might they encounter?

Solution: RPC systems don’t handle pointer structures well. The marshalling system would need to figure out how to follow the linked list structure and include all the needed memory locations.
```

### Question 2(f)(a), 2(f)(b)
- pages: 4
- overlap: Cristian-style time synchronization with asymmetric delays
- source: <https://www.synergylabs.org/courses/15-440/assignments/Fall2019-Midterm-I-WithSolutions.pdf>

```text
[page 4]

(f) (6 points) Nodes A and B wish to time synchronize. The link from A to B takes 40ms, and the link from B to A takes 20ms but these numbers are not known to the computers. They synchronize using Cristian’s algorithm in one round. Node A’s time is 500 and Node B’s time is 632. Node A starts the protocol.

(a) At the completion of the protocol what time does Node A believe it is?

Solution: It takes 40ms for the packet to reach B, so B timestamps it as 632+40 = 672. The response reaches node A with an RTT of 60ms, so node A sets its time to 672+60/2=702.

(b) What, if any, error is in this value and why?

Solution: At the end of the protocol Node B will think it is 692. The error is 10ms. It arose because of the asymmetry in the links.
```

## CMU 15-440/640 Distributed Systems / Fall 2018

### Question 2(a), 2(b), 2(c)
- pages: 4
- overlap: VoIP/UDP; vector clocks in Dynamo-style systems; NTP vs Cristian
- source: <https://www.synergylabs.org/courses/15-440/assignments/Fall2018-Midterm-I-WithSolutions.pdf>

```text
2. In the following, keep your answers brief and to the point (i.e. 2-3 sentences).

(a) (4 points) You are responsible for building the successor to the popular Skype Voice-over-IP protocol that works across the internet (high RTTs). Your boss went to CMU but did not take 441 or 440, and thinks you should use TCP due to its reliable delivery feature. Can you explain to him why this is not a good idea?

Solution: Use UDP (as discussed in class). Reliability is less important than reducing delay and jitter. TCP can cause delays for longer RTT links due to reliable delivery and need for ACKs. (One point for mentioning one of packet loss/UDP, delay and jitter).

(b) (4 points) NoSQL systems like Amazon’s Dynamo allows writes to continue to all machines during a network partition. Once reconnected, Dynamo nodes seek to reconcile inconsistent file versions. Which technique would you choose to detect and flag parallel events? Briefly explain why.

Solution: Vector clocks. Only algorithm that can properly preserve causality, so Dynamo would know that two events happened in parallel. Lamport clocks can’t do this, as they create arbitrarily ordered timestamps, which might give two parallel events different timestamps. (2 points for Vector clocks and 2 points for correct reason. Note: Totally Ordered Lamport clocks is incorrect)

(c) (2 points) Name and briefly describe two differences between the time synchronization algorithm used in NTP and Christian’s algorithm.

Solution:
```

### Question 3(a), 3(b), 3(c)
- pages: 6
- overlap: RPC performance, latency sensitivity, and marshalling bottlenecks
- source: <https://www.synergylabs.org/courses/15-440/assignments/Fall2018-Midterm-I-WithSolutions.pdf>

```text
3. You are hired by the augmented reality startup AR2 that needs to perform a complex image processing algorithm. Because mobile phones have little computing power, AR2 ’s algorithm gets unacceptably slow as image sizes increase. Your manager, Jaine, proposes to use RPC to perform the work on a remote, more powerful server. You measure the following numbers, assuming a base image scaling factor of N .

• The running time of AR2 ’s algorithm is M (N ) = 3N ms on a mobile phone. On the server, its S(N ) = N/3 ms. • Marshalling and unmarshalling take (N/6 + 20) ms in total. • The average RTT between a user and the server is 80 ms. • Bandwidth is infinite between the user and the server.

(a) (4 points) For what value of N is Jaine right, i.e., AR2 should be using an RPC instead of a local call?

Solution: Want 3N ≥ 80ms + (N/6 + 20)ms + N/3 = 100ms + N/2. So, N ≥ 40. We also accepted answers that considered 2(N/6 + 20)ms or 4(N/6 + 20)ms

(b) (2 points) With geo-replication, AR2 is able to reduce the average RTT. How will N change? (Give a qualitative answer)

Solution: It decreases, because the server’s computation becomes as fast as the phone’s for a lower value of N .

(c) (3 points) As AR2 acquires 1) more and more powerful servers and 2) places them closer to users, you notice that the total RPC time does not improve very much. Explain why, by pointing out the bottleneck, in two sentences or less.

Solution: The bottleneck is the marshalling time. No matter how much everything else is improved, the marshalling time will keep the RPC time high.
```

### Question 6(a), 6(c)
- pages: 11
- overlap: RPC semantics for non-idempotent and idempotent operations
- source: <https://www.synergylabs.org/courses/15-440/assignments/Fall2018-Midterm-I-WithSolutions.pdf>

```text
6. BergerNet is a new social network started by the TAs and Professors of 15440 providing almost the same functionality as social networks do today. As a new engineering lead, it is your job to make some crucial design decisions that are either going to make or break the BergerNet.

BergerNet uses RPCs. Identify the easiest-to-implement RPC semantic (at-leastonce, at-most-once, exactly-once) for each of the following features. Give a *one sentence* reason for your choice. (1pt for semantic, 1pt for reason only if semantic correct).

(a) (2 points) Transferring money to your friend on BergerNet

Solution: At-most once. Easiest to implement and can always retry sending on failure.

(c) (2 points) Deleting a friend on BergerNet

Solution: At-least once. Delete is idempotent. At-most once does not work because it is not the easiest to implement.
```

## CMU 15-440/640 Distributed Systems / Fall 2016

### Question 1(A)
- pages: 2
- overlap: MapReduce reducer key-space partitioning
- source: <https://www.synergylabs.org/courses/15-440/assignments/Fall2016-Midterm-II-WithSolutions.pdf>

```text
1. (12 points) Indicate whether each statement below is true or false. ***ALSO****, give a one sentence reason for your answer. Each correct answer is worth 3 points

A. [True, False] For a particular Map-Reduce Phase with ‘M’ and ’R’ nodes respectively, each reducer node handles 1/R of the intermediate key-values by default.

Solution: TRUE. Each Reducer node handles 1/R of the possible keyspace and fetches them from each of the M Mappers.

B. [True, False] In case of System Virtualization, the hypervisor (or VMM) can only allocate and assign the actual number of physical processor resources it has available at its disposal to individual Virtual Machines (VMs).

Solution: FALSE. Virtualization allows you to overcommit resources and provide more virtual resources than actual physical resources, for example by time multiplexing the same set of CPU/processors across multiple VMs.

C. [True, False] DES (symmetric key) is faster than RSA (public-private key)

Solution: Ans: TRUE. Symmetric key ciphers are generally going to be faster than Public-private key ciphers due to the mathematical complexity of the latter.

D. [True, False] When setting up a TOR circuit the sender is guaranteed that the path taken (intermediate routers) to the receiver will be the same as without using TOR.

Solution: Ans: FALSE. There are no guarantees, and the sender decides which path to take when using TOR, which comprises of TOR nodes and not the regular internet routers.
```

### Question 2(a.A), 2(a.B)
- pages: 3
- overlap: Consistent hashing and failure/view divergence
- source: <https://www.synergylabs.org/courses/15-440/assignments/Fall2016-Midterm-II-WithSolutions.pdf>

```text
2. In the following, keep your answers brief and to the point (i.e. 1-2 sentences).
(a) (4 points) Consistent hashing is used in a variety of distributed systems over more traditional hashing algorithms. A. Describe one way that consistent hashing performs better when failures occur (e.g. in DHTs or in CDNs).

Solution: Less content needs to be moved between nodes.

B. Describe one way that consistent hashes perform better when nodes have differing views on the availability of servers.

Solution: Consistent hashing reduces the spread of requests across nodes when views are different

(b) (4 points) You are working on a MAC laptop and using it to develop and test a new Linux OS/kernel. You are worried about bugs since they will cause the Linux kernel to crash. Explain how the ’Isolation’ property of hosted Virtualization solution like VMWare Workstation running on your MAC can help in this case.

Solution: Fault Isolation: We can run the new Linux kernel in a VM. If this VM kernel contains a bug, and crashes it will not crash the main host (OSX) thereby providing fault isolation and allow development and testing to continue.
```

### Question 2(c.A), 2(c.B), 2(e)
- pages: 4
- overlap: MapReduce stragglers/master failure; DNS caching and replication resilience
- source: <https://www.synergylabs.org/courses/15-440/assignments/Fall2016-Midterm-II-WithSolutions.pdf>

```text
[page 4]

(e) (4 points) The DNS root and GTLD servers often come under attack. Give 2 reasons that we don’t notice when they are under attack.

Solution: The records from the root and GTLD have long TTLs and are cached widely. The root and GTLD zones are replicated very widely and it is difficult to attack all locations at the same time.
```

### Question 4(a), 4(b), 4(c), 4(d), 4(e)
- pages: 6-7
- overlap: DNS/CDN hierarchy; Chord lookup and finger-table reasoning
- source: <https://www.synergylabs.org/courses/15-440/assignments/Fall2016-Midterm-II-WithSolutions.pdf>

```text
4. As the CMU’s Distributed Systems class graduates ventured into the world, they spread their description of class lectures. As a result, the popularity of video recordings of the lectures skyrocketed (unfortunately, mostly for the jokes rather than the technical content) and now Srini needs your help in managing the storage and delivery of the files. Srini starts by building an Akamai-like CDN to deliver the files for his web site www.srinilectures.com. As a first step, Srini:
```

## CMU 15-440/640 Distributed Systems / Mid 2012

### Question 1(d), 1(e), 1(f)
- pages: 2-3
- overlap: UDP for VoIP; TCP vs UDP for large RPC results; RPC failure modes
- source: <https://www.cs.cmu.edu/~dga/15-440/F12/midterm2012-solve.pdf>

```text
1. (20 points) Grading is +2 points for a correct answer and 0 points for either blank or incorrect. In other words, at the end of the exam, if you don’t know the answer to any of these, guess, because you’ll get more points in expectation. If you want to be nice to the course staff, mark the ones you guessed on with a “G” so that we have a better idea of what material to go over. We won’t penalize you.

(d) √ True False

Solution: Losing some audio bits isn’t as bad as dealing with the delays from TCP’s retransmission.

√ than TCP for RPCs that return medium-sized (100KB) results.

(e) UDP is better True False

Solution: 100KB is too big to fit in a single packet. The RPC system would just end up re-implementing much of what TCP does to split this data into packets and ensure that it is received reliably and reassembled. This would therefore be a poor idea.

(f) RPCs provide different semantics from local calls because RPCs introduce a different √ of errors. class True False
```

### Question 3(a)
- pages: 5
- overlap: UDP buffer reuse and concurrency race conditions
- source: <https://www.cs.cmu.edu/~dga/15-440/F12/midterm2012-solve.pdf>

```text
3. (25 points) In the following parts, you will debug a small piece of code and identify the bug (if one exists). Assume calls will succeed so that error checking is omitted. You will mark which category the bug falls (Spin loop, Race condition, Deadlock, Correct) AND explain briefly (1-2 sentences) where the bug is. No explanation is necessary if you mark Correct.

(a) func ReadHandler(conn *net.UDPConn) { bytes := make([]byte, 2000) for { n, _, _ := conn.ReadFromUDP(bytes) go ProcessPacket(bytes[0:n]) } } √ Spin loop Race condition Deadlock Correct Explain briefly (1-2 sentences) where the bug is. No explanation is necessary if you mark Correct.

Solution: bytes corresponds to some memory that is reused by ReadFromUDP. Thus, the slice to ProcessPacket could be overwritten while it is being processed.
```

### Question 4(h), 4(i)
- pages: 9
- overlap: UDP checksum behavior; sequence-number wrap and delayed packets
- source: <https://www.cs.cmu.edu/~dga/15-440/F12/midterm2012-solve.pdf>

```text
[page 9]

Solution: Not if the drop occurs just before the epoch event.

√ maximum one-way data throughput is 1/R data messages per second.

(h) LSP could be extended to be robust, with high probability, in the presence of corrupted UDP packets by appending a checksum to each message and dropping any √ that are received with an incorrect checksum. True False

Solution: The resending of messages will ensure that (eventually) a valid packet will be sent.

(i) If a UDP packet gets delayed by several seconds, then the message it contains could be √ mistaken for one that occurs much later in the message sequence. True False

Solution: Due the the wrapping around of sequence numbers.
```

### Question 6(a), 6(b), 6(c), 6(d)
- pages: 13-14
- overlap: Lamport and vector-clock message timestamps
- source: <https://www.cs.cmu.edu/~dga/15-440/F12/midterm2012-solve.pdf>

```text
6. (14 points) Three computers at CMU (A, B, and C) communicate using a protocol that implements the idea of Lamport clocks (they include their clock time stamp in messages). For reference, if you need a reminder, recall that the three rules of Lamport’s algorithm are:
```

## CMU 15-440/640 Distributed Systems / Mid 2011

### Question 1(b), 1(c), 1(d), 1(h), 1(i), 1(j)
- pages: 2-3
- overlap: Checksums; TCP latency; UDP connection setup; synchronous RPC; Lamport clocks; GPS vs NTP
- source: <https://www.cs.cmu.edu/~dga/15-440/F12/midterm2011_solve.pdf>

```text
1. (24 points) Grading is +2 points for a correct answer and 0 points for either blank or incorrect. In other words, at the end of the exam, if you don’t know the answer to any of these, guess, because you’ll get more points in expectation. If you want to be nice to the course staff, mark the ones you guessed on with a “G” so that we have a better idea of what material to go over. We won’t penalize you.

(b) The checksum portion of an IP packet allows√the receiver to both detect and correct a single-bit error in the packet True False

Solution: Checksums can be used to detect errors, but not to correct them.

√ abstraction can add unpredictable latency to

(c) TCP’s reliable in-order byte stream messages under high packet loss. True False to a server, the client and server will engage in a

(d) When creating a UDP connection √ handshake protocol. True False

Solution: There is no setup phase with UDP

(h) When making a synchronous RPC call, the caller will not return until after quested operation has been completed, assuming no error is encountered. True False

(i) If the Lamport clock of event e1 is less than the Lamport clock of event√e2 , then there must be a chain of causal events by which e1 precedes e2 True False
```

### Question 6(a), 6(b), 6(c), 6(d)
- pages: 13-15
- overlap: Lamport timestamps and causal ordering
- source: <https://www.cs.cmu.edu/~dga/15-440/F12/midterm2011_solve.pdf>

```text
6. (14 points) Three computers at CMU, A, B, and C communicate using a protocol that implements the idea of lamport clocks (they include their clock time stamp in messages). For reference, if you need a reminder, recall that the three rules of Lamport’s algorithm are:
```

## CMU 15-440/640 Distributed Systems / Mid 2010

### Question 1
- pages: 2
- overlap: RPC vs local procedure-call differences
- source: <https://www.cs.cmu.edu/~dga/15-440/F12/midterm2010_solve.pdf>

```text
1. (3 points) RPC tries to make remote procedure calls look the same as local procedure calls. But the illusion isn’t perfect. Circle all of the options that correctly describe differences between a local function call and an RPC: A. RPC calls require an extra parameter to identify the server. B. RPC calls may have higher or variable latency. C. RPC calls are limited to call-by-value. D. RPC calls have different (more) failure modes. E. Local function calls require a malloc of a heap object to represent the return pointer.

Solution: A,B,D
```

### Question 8
- pages: 4
- overlap: Application-level choice of UDP or TCP
- source: <https://www.cs.cmu.edu/~dga/15-440/F12/midterm2010_solve.pdf>

```text
8. (3 points) For which of the following applications would UDP be preferable over TCP, ignoring annoying concerns such as firewalls that might block some protocols? A. Streaming a live video over the internet TCP / UDP B. Instant messaging/email TCP / UDP C. Logging in to your bank website TCP / UDP D. Voice over IP TCP / UDP E. Large file transfers TCP / UDP F. Looking up a very small value from a directory service TCP / UDP

Solution: UDP, TCP, TCP, UDP, TCP, UDP
```

### Question 11(a), 11(b), 11(c), 11(d)
- pages: 11-13
- overlap: Lamport/Shamport clock ordering
- source: <https://www.cs.cmu.edu/~dga/15-440/F12/midterm2010_solve.pdf>

```text
e each computer in a distributed system keeps an approximate real-time clock Ri in addition to a Lamport-like clock Li . A computer’s real-time clock Ri is an always-increasing integer (i.e., for any two reads r1 , r2 of Ri such that r1 →i r2 , we have r2 > r1 ), but the real-time clocks at different computers may drift relative to each other (i.e., Rj − Ri is non-constant for j 6= i). Consider the following modification, Shamport, to Lamport’s partial-ordering algorithm:

Rule 1: Before each event at computer i, set Li = min(Li + 1, Ri ). Rule 2: When sending a message m, apply Rule 1 and include the time Li as part of the message (i.e. send (m, Li ) instead of just m). Rule 3: When receiving a message (m, t) at computer j, set Lj = max(Lj , t) and then apply Rule 1 before timestamping the message-arrival event.

Let the Shamport global time of an event e at computer i be S(e) = Li (e).

(a) (2 points) In the algorithm above, underline the difference between Shamport and Lamport’s algorithm. (Underline as little as possible).

Solution: Shamport’s algorithm uses Li = min(Li + 1, Ri ) in Rule 1 instead of Li = Li + 1. Otherwise the two algorithms are the same.

(b) (8 points) Let e, e0 be two events at computer i such that e →i e0 . Prove that S(e0 ) > S(e).

Solution: The key observation is that any new event advances the logical clock. There are a couple common pitfalls to avoid: (1) e and e0 are not necessarily consecutive events; other intervening events can affect the Shamport clock. (2) Events at computer i include the local side of send and receive events, so you need to include possible applications of Rule 2 and Rule 3 in your proof. And (3), reading the problem correctly to understand that the logical clocks Li here are not Lamport clocks, and thus you cannot blindly apply the rules for Lamport clocks from class. One proof is: Consider the sequence of all events e . . . e0 at computer i. If S(e0 ) ≤ S(e) then there must exist at least one pair of consecutive events f, f 0 (WLOG f →i f 0 ) such that S(f 0 ) ≤ S(f ); otherwise each new event would advance the logical clock Li , which would yield Li (e0 ) > Li (e0 ) and thus S(e0 ) > S(e). To show S(e0 ) > S(e), therefore, it suffices to show that Li (f 0 ) > Li (f ) for any two consecutive events f →i f 0 . Let (t, r) be the logical and real-time clock times for event f and (t0 , r0 ) be the times for f 0 . We must show that t0 > t for any events f and f 0 . We break this into three cases based on whether f 0 is a normal local event, a send event, or a receive event. (In each of these cases we allow f to be any type of event.) Notice that in every case we have r0 > r because Ri is always-increasing and f →i f 0 . Case 1: f 0 is a normal local event. This causes a single application of Rule 1, yielding t0 = min(t + 1, r0 ). Briefly consider the rule that set the logical clock for f . Because all three rules last-affect the logical clock with an application of Rule 1, we have that t = min(,̇r) and thus that t ≤ r, yielding t < r0 . Because t + 1 > t and r0 > t we therefore have that t0 > t regardless of which term of the min-operation is lesser, yielding that S(f 0 ) > S(f ) as desired if f 0 is a local-only event. Case 2: f 0 is a send event. This causes an application of Rule 2, which affects the logical clock only with an application of Rule 1. Thus, Case 2 reduces directly to Case 1.
```

## CMU 15-440/640 Distributed Systems / Final 2009

### Question 1, 2, 3, 4
- pages: 2
- overlap: DNS scalability; Chord; RPC library responsibilities; content-based P2P naming
- source: <https://www.cs.cmu.edu/~dga/15-440/F12/final2009-solve.pdf>

```text
1. (4 points) Which techniques are used in DNS to improve scalability? A. Replication B. Recursive queries C. Caching / Soft-State D. Partitioning of Namespace

Solution: A, C, D

---

2. (4 points) Which of the following are true about the Chord distributed hash table? A. Has O(log(N)) lookup latency B. Directly supports fuzzy or wildcard lookups for content C. Uses content-based naming D. Provides anonymity

Solution: A, C

---

3. (4 points) Which of the following are commonly provided in RPC libraries? A. Application-level failure handling B. Data marshalling/unmarshalling C. Asynchronous function calls D. Exactly-once semantics E. At-most-once semantics

Solution: B, E

---

4. (4 points) Which of the following are advantages of using content-based naming for p2p file transfers? A. The receiver can download a chunk using parallel TCP streams. B. The receiver can route around failed links. C. The receiver can download a chunk of data from any source, not just the original seed. D. The receiver can verify that it received the correct data.

Solution: C, D
```

### Question 6(a), 6(h)
- pages: 3
- overlap: GFS data path; Lamport happens-before implication
- source: <https://www.cs.cmu.edu/~dga/15-440/F12/final2009-solve.pdf>

```text
6. (16 points) Which of the following statements are true? Please circle True or False:

(a) True False In Google File System (GFS), when a client needs to access data, it contacts the master and gets the data from the master.

Solution: False

(h) True False Recall the global “happens-before” relationship (→) that captured the logical notions of time using both the local happens-before relationship at each server and the fact that a message must be sent before it can be received. True or false: For a Lamport logical clock L, if e1 → e2 then L(e1 ) < L(e2 ).

Solution: True
```

### Question 14
- pages: 8-11
- overlap: MapReduce-style distributed data processing
- source: <https://www.cs.cmu.edu/~dga/15-440/F12/final2009-solve.pdf>

```text
14. (20 points) Recall the statuses twitter dataset we provided for Project 3, which contained data of the form:

postid <tab> status-message

In Twitter, some status-messages are repeats of earlier status messages. These repeated messages are preceded by “RT” followed by the original status message. For example:

142412141 I need puppies but youtube is blocked. 584923144 Puppies are awesome! 929483834 RT Puppies are awesome! 872935923 RT Puppies are awesome! 423135125 Meow mix meow mix please retwitter 723917388 RT I need puppies but youtube is blocked. 629359237 RT Puppies are awesome! 562983948 RT Meow mix meow mix please retwitter 729385724 RT Meow mix meow mix please retwitter 912383444 Taking 15-440 final exam, lolol.

In this problem, your goal is to identify the most “retweeted” status messages using the MapReduce style of programming. You must write one or more Map and Reduce functions whose final output contains a sorted list of post ids that have been “retweeted”/repeated, sorted by the number of times they have been retweeted. If run on the above example, the output would be:

1 I need puppies but youtube is blocked. 2 Meow mix meow mix please retwitter 3 Puppies are awesome!

Only retweeted statuses should appear in the output. The output should be sorted by the number of retweets from fewest to most. You can use any reasonable pseudocode you choose (Java-like or C++-like); we will grade based on the algorithm, not having semicolons correct. You can use two types: Integers and Strings. You can assume the existence of STL-like string functions for your convenience. You can iterate over lists using the for construct as shown below:

for item in list { (do something with item) }

You should use the “emit(key,value)” pseudocode for the output of functions.
```

## CMU 15-440/640 Distributed Systems / Final 2010

### Question 1, 2
- pages: 2
- overlap: TCP handshake misconception; Internet best effort; DNS TTL/invalidation; GFS/HDFS assumptions
- source: <https://www.cs.cmu.edu/~dga/15-440/F12/final2010-solve.pdf>

```text
1. (22 points) True/False: Circle the one that best applies. Grading is 2 points for every correct answer. That means that at the end of the exam, if you don’t know the right answer, come back here and guess randomly!

Threads and Processes

True, False It is less expensive to create a process than a thread. True, False Switching between threads is faster than switching between processes. True, False In order to switch between user threads, you need to enter the kernel. True, False Threads share a heap and a stack.

Networking

True, False The TCP initial handshake must be completed between the sender and every router on the path to the destination before communication can take place. True, False The Internet service model allows a small (a percent or two) amount of packet loss. (In other words, end-hosts must be able to deal with a small amount of loss) True, False Domain Name Service (DNS) servers remember which clients have cached DNS replies so that the servers can send invalidation messages when name bindings change.

Distributed Mutual Exclusion

True, False Ring-based distributed mutual exclusion is a great solution for a latency-sensitive application running on 10,000 nodes.

Logging

True, False Write-ahead logging is a useful technique for providing persistence for random updates without needing to write to a random location on disk. True, False For correctness, all write-ahead log records must specify how to both undo and redo the operation they describe.

Tor

True, False The onion routing scheme used by Tor is resilient to an attacker that can simultaneously compromise every node in the Tor network.

---

2. (5 points) Which of the following design assumptions apply to HDFS/GFS? (Circle all that apply) A. Only amazingly powerful servers can handle the size and complexity of the workload. B. Any use of a centralized server would cause too much of a bottleneck. C. Component failures are expected. D. Files are huge by traditional standards. E. File contents are often updated and overwritten.

Solution: C, D
```

### Question 4, 5, 6
- pages: 5-6
- overlap: Chord/P2P lookup and design trade-offs
- source: <https://www.cs.cmu.edu/~dga/15-440/F12/final2010-solve.pdf>

```text
4. (6 points) Suppose the above Chord setup: • At what node do you expect to find key 10? • At what node do you expect to find key 9? • On average, how many hops are there when searching for a key? • What route will a search for key 11 take, starting at node 3?

Solution:

---

5. (6 points) Suppose you want to build a large distributed system to store cookie recipes. Each cookie is stored using the recipe’s name (“Grandma’s Arsenic Cookie Surprise”). Unlike many P2P systems, in this one, the recipe data is small, so you wanted to store the actual data in the P2P system instead of leaving it on the original nodes. A friend says “Hey, I hear that Chord is very efficient – it doesn’t take many lookups to find the node containing the data.” Explain to your friend why directly throwing this data into a DHT such as chord, with key = recipe name, value = recipe data, is a really bad design decision. Brief - two sentences or so.

Solution:

---

6. (6 points) Tell us what style of P2P system you would use, and what assumptions you think are reasonable for your cookie-storing-system: • Number of nodes • Number of recipes • Number of queries/second • What do queries look like? Style of system AND a brief rationale for this decision:

Solution:
```

### Question 11, 12
- pages: 9
- overlap: Lamport timestamp ordering
- source: <https://www.cs.cmu.edu/~dga/15-440/F12/final2010-solve.pdf>

```text
11. (6 points) What is the value of x? If it cannot be determined, write “unknown”.

Solution:

---

12. (10 points) For the following, circle which event happened first. If it cannot be determined, circle “unknown.”

• L1 (m1 , send) L4 (m5 , send) U nknown • L2 (m3 , send) L3 (m4 , send) U nknown • L3 (m4 , send) L3 (m3 , recv) U nknown • L2 (m3 , send) L4 (m6 , send) U nknown • L4 (m6 , send) L1 (m7 , send) U nknown

Solution:
```

## CMU 15-440/640 Distributed Systems / Final 2011

### Question 1
- pages: 2-3
- overlap: DNS hierarchy; DNS caching; CDN via DNS
- source: <https://www.cs.cmu.edu/~dga/15-440/F12/final2011-solve.pdf>

```text
1. (8 points) Circle True or False as appropriate. If you don’t know the answer, come back at the end and GUESS; a blank answer is the same as a wrong answer, so guessing can only help.
```

### Question 6(a), 6(b), 6(c), 6(d), 6(e), 6(f)
- pages: 10-11
- overlap: Napster, query flooding, supernodes, flooding limits
- source: <https://www.cs.cmu.edu/~dga/15-440/F12/final2011-solve.pdf>

```text
6. (a) (2 points) In a centralized p2p network (such as the old Napster), how many indices must be searched if a client wants to locate a particular file?

Solution: 1

(b) (2 points) Name one major disadvantage of the centralized p2p system (from a distributed principles point of view)

Solution: - Single point of failure - Server processes everything - Server must keep track of a potentially very large number of clients - more?

(c) (2 points) Query flooding is an alternative design that solves some of the problems of centralized p2p and eliminates the central server. However, it changes the mechanics of peer interactions significantly. Explain (1 sentence each) how a newly-joining node publishes the files they wish to make available, in... A centralized p2p network:

Solution: They send their list of files and metadata to the server.

A query flooding p2p network:

Solution: They don’t do anything - queries come to them.

(d) (2 points) One popular improvement upon query flooding is to move to a “supernode” flooding architecture. Using N as the number of nodes in the network and, S as the number of supernodes (S << N ), explain the benefit of moving to this supernode architecture.

Solution: Queries require now O(S) messages instead of O(N ). In addition, if the nodes used as supernodes are more stable or have higher capacity, can further improve the performance or stability of the network.
```

### Question 7(a), 7(b), 7(c), 7(d), 7(e), 7(f)
- pages: 12-13
- overlap: DHT/Chord ring mapping, finger table, successor, fallback/proximity
- source: <https://www.cs.cmu.edu/~dga/15-440/F12/final2011-solve.pdf>

```text
7. (a) (2 points) In a distributed hash table (DHT) using a ring mapping, explain how a key is mapped to a specific node?

Solution: Keys and nodes map to points in a ring space. A node handles all keys mapped between it and its successor.

(b) (2 points) In the most basic form of DHT systems, nodes simply track their predecessor and successor. Very briefly state what problem this leads to as the network grows larger.

Solution: Performance problems as nodes forward a key resolution request to larger chains of neighbors.

(c) (2 points) The Chord scheme overcomes this problem by having each node maintain a “finger table”. Given starting node j and destination node k, where k > j, how much is the distance between the two nodes reduced with each hop?

Solution: It decreases exponentially, or it is cut in half

(d) (2 points) In a Chord structured DHT with N nodes, how many hops would a lookup operation require?

Solution: log(N )

(e) (2 points) Assume a Chord network in which node q is the successor of node p. During operation, node p discovers that its successor link is no longer consistent because q has updated its predecessor link. What does this change imply must have happened in the network?

Solution: A new node joined the network ’between’ p and q.
```

### Question 9(a), 9(b), 9(c), 9(d)
- pages: 15-16
- overlap: MapReduce/GFS failure handling and stragglers
- source: <https://www.cs.cmu.edu/~dga/15-440/F12/final2011-solve.pdf>

```text
9. (10 points) MapReduce has proved an extremely popular framework for distributed computation on large clusters, because it masks many of the painful parts of ganging together thousands of nodes to accomplish a task.

(a) In general high-performance computing (HPC), programmed using message passing, what is the technique used to provide fault tolerance? (Very short answer)

Solution: Checkpoint/restore

(b) Identify two important limitations that MapReduce places upon the Map functions so that the framework can hide failures from the programmer.

Solution: They must be side-effect free, deterministic, and idempotent.

(c) What advantage does this give MapReduce over MPI for failure handling and recovery? (There are several—list the one(s) you think is most important)

Solution: Recovery can be done by only executing the work that was being handled on the failed machine, not the entire cluster. There is no need to take snapshots or to barrier sync the cluster.

(d) How does MapReduce handle “straggler” tasks that take longer than all of the others (e.g., perhaps they’re running on a slower machine or one with buggy hardware)?

Solution: It executes them in duplicate on another machine towards the end of execution. (Not needed for answer: It can do so because of the same properties of the tasks above - namely, that they can be freely re-executed and produce the same result.)
```

## UW CSE 461 Computer Networks / Sample Mid 2

### Problem 1(a), 1(d), 1(e)
- pages: 2
- overlap: Layering, internetworking, encapsulation
- source: <https://courses.cs.washington.edu/courses/cse461/23sp/samples/sample-midterm2-key.pdf>

```text
Problem 1: Basics (10 points) a) How are hosts with two different link layers (e.g., WiFi and Ethernet) able to communicate? (3 points)

Layering, de-layering and layering through different network.

Alternative: The network layer (IP) does that. It decapsulates the data from one link layer and encapsulates in another.

b) What is a simplex link? (1 point)

One way channel: one is the sender, one is the receiver

c) What is a half-duplex link? (1 point)

Two way channel: can both send to each other but not at the same time

d) What is the primary approach used to divide network functionality in the Internet? (2 points)

Layering (yes)

e) Consider a protocol stack composed of WiFi, IP, TCP, and HTTP. Illustrate what the packet on the wire look like for this stack? (3 points) WIFI - IP - TCP - HTTP .

a drawing of HTTP encapsulated by TCP then by IP then by WIFI
```

### Problem 3(a), 3(b), 3(c), 3(d)
- pages: 3-4
- overlap: ICMP, NAT, IPv6 motivation, tunneling
- source: <https://courses.cs.washington.edu/courses/cse461/23sp/samples/sample-midterm2-key.pdf>

```text
Problem 3: IP primitives (10 points) a) What is ICMP used for? (2 points)

Sending back error messages (reports)

b) Describe two advantages and two disadvantages of NAT (4 points)

[page 4]

Advantages: 1. Counter the shortage of IP address
```

### Problem 4(a), 4(b), 4(c), 4(d)
- pages: 5
- overlap: Routing vs forwarding, longest-prefix matching, local/gateway forwarding, routing scalability
- source: <https://courses.cs.washington.edu/courses/cse461/23sp/samples/sample-midterm2-key.pdf>

```text
Problem 4: Routing and forwarding (10 points) a) What is difference between routing and forwarding (3 points)
```

### Problem 5(a), 5(b), 5(c), 5(d), 5(e)
- pages: 6
- overlap: Distance-vector vs link-state routing, convergence, RIP, OSPF/IS-IS
- source: <https://courses.cs.washington.edu/courses/cse461/23sp/samples/sample-midterm2-key.pdf>

```text
Problem 5: Distance vector and link state (10 points) a) Describe how distance vector and link state routing algorithms differ? (6 points)

Distance vector exchanges shortest path information with neighbors. Link state exchanges topology information.

Distance vector converges slower.

Distance vector is computationally simpler.

b) Which of the two algorithms converges faster? (1 point) Link state routing What is converging faster? -- Computes new shortest paths after changes faster.

c) Which of the two algorithms requires more computation (1 point) Link State Algorithm

d) Give an example of a routing protocol that uses distance vector algorithm (1 point)

RIP

e) Given an example of a routing protocol that uses link state algorithm. (1 points)

OSPF, IS-IS
```

## UW CSE 461 Computer Networks / Mid Review Practice, Section 4

### Practice Problems: Bandwidth Allocation; Practice Problems: AIMD
- pages: 12-16
- overlap: Max-min fairness and AIMD calculations
- source: <https://courses.cs.washington.edu/courses/cse461/23sp/section/4-midterm-review.pdf>

```text
[page 12]

Practice Problems | Bandwidth Allocation Consider a network with four ﬂows A, B, C, and D, all of which pass through the same 10 Mbps bandwidth link. At this moment in time, ﬂow A has a demand of 1 Mbps, ﬂow B has a demand of 2 Mbps, ﬂow C has a demand of 10 Mbps, ﬂow D has an inﬁnite demand. Assuming the link has no other ﬂows, what would be the bandwidth allocation regarding max-min fairness?

12

[page 13]

Practice Problems | Bandwidth Allocation Consider a network with four ﬂows A, B, C, and D, all of which pass through the same 10 Mbps bandwidth link. At this moment in time, ﬂow A has a demand of 1 Mbps, ﬂow B has a demand of 2 Mbps, ﬂow C has a demand of 10 Mbps, ﬂow D has an inﬁnite demand. Assuming the link has no other ﬂows, what would be the bandwidth allocation regarding max-min fairness?

Flow A: 1 Mbps Flow B: 2 Mbps Flow C: 3.5 Mbps Flow D: 3.5 Mbps

13

[page 14]

Max-Min Fair Allocation

1. Start with all ﬂows at rate 0
2. Increase the ﬂows until there is a new bottleneck in the network
3. Hold ﬁxed the rate of the ﬂows that are bottlenecked
4. Go to step 2 for any remaining ﬂows

14

[page 15]

Practice Problems | AIMD Consider a 10 Mbps capacity link shared by two ﬂows A and B. Flow A has a bandwidth of 3 Mbps while ﬂow B has an inﬁnite bandwidth. For each RTT, each ﬂow will increase the rate at which it is sending data by 1 Mbps if the path is not congested, while they will decrease the rate at which they send data by a factor of 2 (ie, cut in half) if the path is congested. Assuming that the ﬂow A starts by sending data at a rate of 2 Mbps and ﬂow B at a rate of 20 Mbps, what will be the rate at which each ﬂow sends data after 1 RTT, 2 RTT, and 3 RTT have elapsed? You may assume that no other links in ﬂow A or B are congested. Answer in Mbps.

15

[page 16]

Practice Problems | AIMD Consider a 10 Mbps capacity link shared by two ﬂows A and B. Flow A has a bandwidth of 3 Mbps while ﬂow B has an inﬁnite bandwidth. For each RTT, each ﬂow will increase the rate at which it is sending data by 1 Mbps if the path is not congested, while they will decrease the rate at which they send data by a factor of 2 (ie, cut in half) if the path is congested. Assuming that the ﬂow A starts by sending data at a rate of 2 Mbps and ﬂow B at a rate of 20 Mbps, what will be the rate at which each ﬂow sends data after 1 RTT, 2 RTT, and 3 RTT have elapsed? You may assume that no other links in ﬂow A or B are congested. Answer in Mbps.

After 1 RTT: Flow A = 1 Mbps, Flow B = 10 Mbps After 2 RTT: Flow A = 0.5 Mbps, Flow B = 5 Mbps After 3 RTT: Flow A = 1.5 Mbps, Flow B = 6 Mbps
```

### Practice Problems: Link-State Routing
- pages: 53-54
- overlap: Link-state routing convergence and inconsistent LSP views
- source: <https://courses.cs.washington.edu/courses/cse461/23sp/section/4-midterm-review.pdf>

```text
[page 53]

Practice Problems | Link-State Routing

Suppose that nodes in the network shown in the ﬁgure below participate in link-state routing, and C receives contradictory LSPs: One from A arrives claiming the A–B link is down, but one from B arrives claiming the A–B link is up.

a) How could this happen? b) What should C do? What can it expect?

53

[page 54]

Practice Problems | Link-State Routing

Suppose that nodes in the network shown in the ﬁgure below participate in link-state routing, and C receives contradictory LSPs: One from A arrives claiming the A–B link is down, but one from B arrives claiming the A–B link is up.

a) How could this happen? This could happen if B sent an LSP packet just before the A-B link was down, followed by A sending an LSP packet after the link was down (or vice-versa)

b) What should C do? What can it expect? In Link-State routing, ﬂooding takes place periodically and new routes are constantly being calculated. Hence, eventually the old LSP would be updated by its sender with a newer version, and reports from the two sides would come to an agreement again.
```

## UW CSE 461 Computer Networks / Winter 2017 Mid

### Problem 3
- pages: 4-5
- overlap: Distance-vector routing table updates and forwarding decisions
- source: <https://courses.cs.washington.edu/courses/cse461/22wi/practice-materials/midterm-2.3.17.pdf>

```text
Problem 3: Spanning Tree (10 Points) For the following network topology, fill out each step of the spanning tree algorithm in a table until it reaches the steady state. Ties broken by lowest address. Use ‘’ if nothing changes in a row between rounds. (7 Points)

B Round 0: A A (A,A,0) B (B,B,0) C (C,C,0) D D (D,D,0) C E (E,E,0) F (F,F,0) G (G,G,0) F H (H,H,0) E A

G H

Round 1: Round 2: A A B B C C D D E E F F G G H H

4

[page 5]
```

## Princeton COS 461 Computer Networks / Spring 2012 Mid

### Question 1(a), 1(b), 1(c)
- pages: 2
- overlap: TCP ACK size, bufferbloat/queueing, VoIP priority
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring12-cos461-exam1-answers.pdf>

```text
QUESTION 1: Waiting to Go (10 points) A home-network router has an upload bandwidth of 1 million bits per second (i.e., 125,000 bytes per second) to the Internet, and a 100,000-byte first-in first-out buffer for packets awaiting transmission. Packets have a maximum transmission unit (MTU) size of 1000 bytes.

1(a) If the router’s buffer is completely full of TCP acknowledgment packets, how many packets are queued in the buffer? Assume the TCP segment has no payload, and the packet headers do not contain any IPv4 or TCP options. (3 points)

Ignoring the link-layer header and any minimum size restriction on the link-layer frame, a TCP ACK packet is 40 bytes long, consisting of a 20-byte IP header and a 20-byte TCP header. A 100,000-byte buffer can hold 100000/40 or 2500 ACK packets.

1(b) Suppose the buffer is completely full. How long does it take the router to transmit all of the bytes in the buffer? (3 points)

Sending 100,000 bytes at 125,000 bytes/sec requires 100000/125000 or 0.8 seconds, or 800 msec.

1(c) Suppose the router supports two first-in first-out queues, one for interactive applications (like Voice over IP) and the other for all remaining traffic, with static priority for the queue handling interactive traffic. If a VoIP packet arrives when the queue for interactive applications is empty, what is the maximum time before the router starts transmitting the VoIP packet? (Assume that the router does not preempt any ongoing packet transmission.) (4 points)

At worst, the VoIP packets arrives just as the router starts transmitting a full-sized (i.e., 1000-byte) non-VoIP packet, forcing the VoIP packet to wait for 1000/125000 or 0.008 seconds, or 8 msec.
```

### Question 2(a), 2(b), 2(c)
- pages: 3
- overlap: TCP three-way handshake timing and lost final ACK
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring12-cos461-exam1-answers.pdf>

```text
QUESTION 2: A Good, Firm Handshake (10 points) Host A initiates a TCP connection with host B by sending a SYN packet, and B responds with a SYN-ACK packet. Upon receiving the SYN-ACK packet, A responds with an ACK packet. For each question, please check one box

2a) What is the earliest time that A can start sending data to B? (3 points)

_____ Immediately after sending the SYN packet to B

__X__ Immediately after receiving the SYN-ACK packet from B

_____ Immediately after receiving data from B

Once the SYN-ACK arrives, A knows that B has A’s initial sequence number and is ready to accept data packets from A.

2b) What is the earliest time that B can start sending data to A? (3 points)

_____ Immediately after receiving the SYN packet from A

_____ Immediately after sending the SYN-ACK packet to A

__X__ Immediately after receiving the ACK packet from A

_____ Immediately after receiving data from A

Once the ACK arrives, B knows that A has B’s initial sequence number and is ready to accept data packets from B.

2c) Suppose the ACK packet from A gets lost. What ultimately triggers A to retransmit the lost ACK packet? Assume no other packets get lost and no data packets are sent. (4 points)

_____ A retransmission timeout at A

__X__ A retransmission timeout at B, triggering a retransmission of the SYN-ACK packet

ACK packets are not retransmitted, so A does not experience a retransmission timeout. If B does not receive an ACK for the SYN-ACK, then B will retransmit the (presumed lost) SYN-ACK after the retransmission timeout expires.
```

### Question 3(a), 3(b), 3(c), 3(d), 3(e); Question 4(b), 4(c)
- pages: 4-5
- overlap: IP prefix/default forwarding/TTL; temporary link-state loops and metric changes
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring12-cos461-exam1-answers.pdf>

```text
QUESTION 3: Defaulting (10 points) A small university campus is assigned a large address block 12.1.0.0/17, but is only using a portion of these addresses (in 12.1.1.0/24) to number its computers. The campus uses a single Internet Service Provider (ISP) to reach the rest of the Internet. This picture shows the forwarding tables on the ISP’s router (on the left) and the campus edge router (on the right):

For example, the ISP forwards all packets with destination addresses in 12.1.0.0/17 out link #2 toward the campus edge router. Both routers include a default forwarding entry 0.0.0.0/0 that can match any destination IP address.

3a) How many IP addresses does the campus “own” in its 12.1.0.0/17 block? You can represent your answer as a power of two. (2 points)

The 17-bit mask leaves 32-17, or 15 bits to identify the addresses within the block. As such, the block contains 215 or 32,768 addresses.

3b) What are the smallest and largest IP addresses that the campus “owns”, whether or not the campus is currently using the address? (2 points)

12.1.0.0-12.1.127.255

3c) Suppose the ISP router receives a packet with destination IP address 12.1.1.1? What path does this packet follow? (2 points)

The packet flows over the path 1 2  3  4.

3d) Suppose the ISP router receives a packet with destination IP address 12.1.20.1? What path does this packet follow? (2 points)

The packet flows over the path 1 2  3  2  3 …

3e) What ultimately happens to a packet with destination IP address 12.1.20.1? Where does it go? (2 points)

The looping packet is discarded once its IP TTL (Time-To-Live) expires.

4

[page 5]

---

QUESTION 4: Stability (10 points)

4b) Consider the network below that runs a link-state routing protocol that computes shortest paths as a sum of link weights. The number on each link is the weight of the link in each direction (e.g., links b-c and c-b both have weight 2). Suppose nodes a, b, and d send packets to destination node c. If link d-c (and c-d) fails, which of nodes a, b, and d could conceivably see their packets stuck in a temporary forwarding loop? Which ones would not? (3 points)

a and d can loop, but not b

4c) Using the same figure as in question 4b), suppose the network operator is taking link d-c (and c-d) down for planned maintenance. The network operator wants to temporarily set the weight of the link to a higher value, to coax nodes to move away from paths that use the link without creating any blackholes or loops. What is the (minimum) sequence of weight settings for the link that ensures no packets destined to node c experience a blackhole or loop? (3 points)
```

### Question 5(a), 5(b), 5(c), 5(d)
- pages: 6
- overlap: Socket close/FIN, TCP byte stream receive, EOF handling
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring12-cos461-exam1-answers.pdf>

```text
QUESTION 5: Sockets (10 points) This question concerns the relationship between socket calls at the application layer and the behavior of the transport layer. Consider a reliable stream (i.e., TCP) socket between application processes A and B running on two different hosts.

5a) Suppose process A calls send() to send 10,000 bytes of data, and the operating system begins sending the data as a sequence of packets destined to B. If process A calls close() on the socket before the operating system finishes transmitting the data, will the remaining data be sent to B? Why or why not? (3 points)

Yes, the Operating System continues transmitted the remaining data to B, to ensure the ordered, reliable delivery of the byte stream.

5b) Suppose process A calls close() after the operating system has transmitted all of the outstanding data. What kind of packet does the operating system send in response to A’s call to close()? (2 points)

TCP FIN packet

5c) Explain why B may need to perform multiple calls to recv() to receive all 10,000 bytes of data from A. (3 points)

The data may not reach B in its entirety at the same time, since it is split into multiple packets. These packets may experience different delays due to congestion, retransmission and receivewindow constraints.

5d) Suppose B’s operating system has learned that A has closed its end of the connection. Once process B has read all of the data from A, what does B’s next call to recv() return? (2 points)

A 0, indicating the end of the stream.
```

### Question 7
- pages: 9-10
- overlap: DNS/web redirection/captive-portal flow
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring12-cos461-exam1-answers.pdf>

```text
QUESTION 7: In Name Only (10 points) Some WiFi hotspots offer wireless access for a fee. When a user connects to the access point, a DHCP server assigns them an IP address, network mask, gateway router, and local DNS server. When the user tries to access a Web site, the hotspot directs the HTTP request to a “pay wall” where the user can enter credit card information, and only then can the user access the requested Web site. These hotpots typically allow DNS queries through the pay wall, though, since the user’s Web browser needs to use DNS to map domain names to IP addresses.

7a) Suppose, before the user pays, the hotspot only allows the user to send and receive UDP packets with source or destination port 53 (the port number used for DNS). Assume the hotspot allows any such traffic to travel to and from the user, independent of the destination IP address. Briefly describe the design of a system that would allow the user to access arbitrary sites on the Internet via the hotspot without paying. The user may need to deploy parts of the system ahead of time. Include a picture. (5 points)

The user can run a proxy that listens on UDP port 53. The client can encapsulate an IP packet (say, containing a TCP segment) inside UDP packets sent to the proxy, and the proxy can send the traffic to arbitrary Internet services at the client’s request. The responses can be encapsulated and sent back to the client using UDP packets with port 53. To ensure reliability, the client and the proxy can acknowledge received UDP packets and retransmit unacknowledged packets.

9

[page 10]

7b) Now suppose that the hotspot only allows DNS queries (i.e., correctly formed DNS requests sent to UDP port 53) destined to the IP address of its own local DNS server, and DNS responses from that server. Design a new solution that allows the user to access arbitrary Internet sites without paying. Include a picture. Note that you should not use this technique in real life to evade paying for Internet service! (5 points)

The user can run a proxy that acts as an authoritative DNS server for a domain the user has registered (say, jrex.com). To communicate with the proxy, the client sends a DNS request to the hotspot’s local DNS server, with the contents of the message embedded in the domain name (e.g., here-is-my-message.jrex.com). This will trigger the local DNS server to direct the query to the jrex.com authoritative server, which can encode a message in the DNS response (e.g., using the four bytes of the IP address to encode four characters, or using DNS TXT records to encode more information. As in the previous question, the client and the proxy need to acknowledge and retransmit the UDP packets to ensure reliable delivery. The domain names could even embed sequence and acknowledgment information (e.g., here-is-mymessage-X.jrex.com, where X is a number). This class of solutions is known as “DNS tunneling.”

Several students offered a different answer that was also valid. The idea is to hijack the hotspot’s local DNS server by sending a forged ARP response for the DNS server’s IP address, learned by the client in DHCP bootstrapping. Now the client can send UDP port 53 packets, and follow the approach in part 7a of the question. Note that this approach may be easier for the hotspot administrators to detect, since the local DNS server would suddenly be carrying no traffic. (That said, even the solution above is relatively easy to detect if the hotspot administrators are monitoring DNS query/response loads on a per-client basis.)

Other students offered another answer that was also valid. The client could snoop on DHCP, ARP, or flooded packets to learn the IP addresses of other users who have (presumably) paid for service. The client can then send a forged ARP response for another client’s IP address, and be able to receive packets sent to that address. The client can start sending packets from that address, too, allowing free communication. (This might be detected by the other user, and in fact that user may sometimes send traffic, causing the switches to shift traffic back to the old client. As such, the crafty client would need to repeatedly hijack the original client.)
```

## Princeton COS 461 Computer Networks / Spring 2012 Final

### Question 1(a), 1(b), 1(c), 1(d)
- pages: 2
- overlap: Skype/P2P supernodes; BitTorrent tit-for-tat
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring12-cos461-exam2-answer.pdf>

```text
QUESTION 1: Peer Pressure (10 points)

1(a) The Skype peer-to-peer IP telephony application sometimes has a user machine serve as a “super node” to support communication between two other users. When are super nodes needed, and why? (3 points)

Traversing NATs and firewalls, particularly when both peers lie behind a NAT/firewall that blocks unsolicited traffic from external hosts.

Super nodes are also useful for discovering the remote peer.

1(b) Microsoft recently bought Skype. Earlier this month, Microsoft announced that they will replace the classic super nodes with their own super nodes running in Microsoft data centers. Give one reason why Microsoft might have made this decision? (2 points)

To improve performance and reliability by ensuring super nodes have sufficient resources and predictable operation.

1(c) To prevent free-riding, a BitTorrent peer rates other peers in terms of the download rate they offer, and then decides how much to offer in return. Suppose six users offer data at rates of 10, 4, 8, 3, 7, and 5 Mbps, respectively, and the peer has 15 Mbps of upload bandwidth. What upload rate does it offer to each of the six peers? (3 points)

The peer uploads with 1/N of its bandwidth to the top N peers, where N is 4 by default. So, the upload rates are 15/4, 0, 15/4, 0, 15/4, 15/4.

1(d) Under the same scenario as question 1(c), suppose peer #1 (currently offering a download rate of 10 Mbps) decides to be more strategic. What is the minimum rate that peer #1 could offer and still achieve the same upload rate it received in question 1(c)? (2 points)

Just slightly above the fifth peer, or just above 4 Mbps.
```

### Question 4(a), 4(b), 4(c), 4(d)
- pages: 5
- overlap: DHCP registration, IP/MAC binding, ARP miss handling
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring12-cos461-exam2-answer.pdf>

```text
QUESTION 4: Enterprising (10 points)

4(a) Many enterprise networks only allow registered machines to access the local area network. Some of these networks configure the DHCP server to assign a computer (or MAC address) the same IP address every time it connects to the network. Give one reason why. (3 points)

Tracking traffic by IP address is much easier if an IP address corresponds to the same user at all time.

4(b) What is the disadvantage of associating each registered MAC address with a pre-determined IP address? (3 points)

Running out of IP addresses when the number of potential users grows large, even if these users are not active at the same time.

Less opportunity for subdividing the topology into separate IP prefixes for more scalable routing.

4(c) To send an IP packet to another host on the same local area network, the sending host first checks its local ARP cache to determine the MAC address associated with the destination IP address. On a “miss” in the ARP cache, the sending host sends an ARP request for the destination IP address and buffers the packet, awaiting a response. Suppose, instead, the host issues the ARP request and simultaneously drops the IP packet. Name one advantage of this approach? (2 points)

The sending host does not need to buffer the packet until receiving the ARP response. This reduces the memory requirements on the sender, and obviates the need to match the ARP response with some arbitrary packet sitting in a buffer.

4(d) What is one disadvantage of the approach in 4(c)? (2 points)

The dropped packets must be retransmitted at a higher layer (e.g., TCP). E.g., a dropped SYN packet, in particular, would have a long retransmission timeout.
```

### Question 5(a)
- pages: 6
- overlap: Longest-prefix matching and prefix-priority routing rules
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring12-cos461-exam2-answer.pdf>

```text
QUESTION 5: Going With the Flow (10 points) An OpenFlow switch has a prioritized list of packet-handling rules, each consisting of a pattern that matches on bits in the packet header and a set of actions to apply to the packets. This question explores applications of OpenFlow switches.

5(a) An OpenFlow switch can serve as an IP router. Suppose the “IP router” OpenFlow application has forwarding rules for three IP prefixes: (i) 12.1.2.0/24 forwards out link 1, (ii) 12.0.0.0/8 forwards out link 2, and (iii) 12.1.0.0/16 forwards out link 3. What priority order should these rules have in the OpenFlow switch, starting with the highest priority? (2 points)

The highest priority should go to the longest prefixes. That is, rule 1 should have priority over rule 3, which should have priority over rule 2.
```

## Princeton COS 461 Computer Networks / Spring 2011 Mid

### Question 1(a), 1(b), 1(c)
- pages: 2-3
- overlap: NAT/tunneling and packet-header fields
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring11-cos461-exam1-answers.pdf>

```text
rse the path use both tunnels. The various network interfaces have IP and MAC addresses as shown.

H1 has established an HTTP session with web server H2 and data packets are flowing between the two machines. As an example, we have filled in the headers for packet 1 (traveling from the server H2 to the client H1). Note that you should order your headers from “outermost” in, as shown: Ethernet should be listed before IP, because the Ethernet packet exists first on the wire.

Header Type Source Destination Ethernet MAC 16 MAC 15 IP 3.0.1.2 1.2.3.4

You only have to fill in the header type and the source and destination address for the network and datalink layer headers for packets 2, 3, and 4 (these packets are all traveling from the client H1 to the server H2, as marked on the figure with heavy black arrows and numbers). Note: You might not need to use all the rows supplied.

2

[page 3]

(a) [1.5 points – 0.5 for MAC, 1 for IP. Split credit equally over fields. i.e., 1/3 point for each IP field; 1/6 point for each MAC field.] Header for packet 2:

Header Type Source Destination Ethernet MAC 1 MAC 2 IP 10.0.0.2 3.0.1.2

(b) [1.5 points – 0.5 for MAC, 1 for IP] Header for packet 3:

Header Type Source Destination Ethernet MAC 3 MAC 4 IP 1.2.3.4 3.0.1.2

(c) [3.5 points – 0.5 for MAC, 1 for each of 3 IP headers] Header for packet 4:

Header Type Source Destination Ethernet MAC 9 MAC 10 IP 1.2.3.8 1.2.4.3 IP 1.2.3.6 2.0.0.1 IP 1.2.3.4 3.0.1.2
```

### Question 2(a), 2(b), 2(c), 2(d)
- pages: 4-5
- overlap: TCP ACK arithmetic, FIN/close, window/congestion behavior
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring11-cos461-exam1-answers.pdf>

```text
QUESTION 2 : TCP and Congestion Control (10 POINTS)

Consider the following graph of TCP throughput (NOT DRAWN TO SCALE), where the y-axis describes the TCP window size of the sender. We will later ask you to describe what happens on the right side of the graph as the sender continues to transmit.
```

### Question 4
- pages: 8-10
- overlap: IP headers, prefix filters, and routing/filtering rule behavior
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring11-cos461-exam1-answers.pdf>

```text
QUESTION 4: Short Answers (15 points) For the following questions, be specific, but you don’t need to be prolific. Answers like “for efficiency” are too vague to receive credit.
```

## Princeton COS 461 Computer Networks / 2010 Mid

### Question 1.1, 1.2, 1.3
- pages: 2-4
- overlap: DHCP, ARP, DNS, HTTP/TCP connection workflow and packet headers
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring10-cos461-exam1-answers.pdf>

```text
[page 2]

QUESTION 1 : Protocols and Addressing (19 POINTS)

In the topology shown below, a client A (on the left side) joins a network and wants to download the webpage for http://example.net/ from the webserver H (on the right side). All wires/links are Ethernet segments. In this question, you will be asked what packets are on the wire (and the addresses in those packets’ headers) for this to occur. When asked to provide the addresses of machines, you can refer to them abstractly: IP-H is the IP address of the webserver H, MAC-H is the MAC address of H. If a packet is being sent to a broadcast address, use “BR” as the destination (e.g., IP-BR or MAC-BR).

Assume the following: • All the machines, except the client, already have their ARP caches full. • DNS resolver C has an empty DNS cache. • http://example.net/index.html fits in a single packet. • Client just joined the network and so all of its caches are empty (DNS, ARP, DHCP)

When you are asked to write a packet with its headers, you should include both network and link-layer addresses. So a DNS query from client A to server C and the response should look like the following. Note that other packets may be involved with a full DNS lookup that we are not showing in this example.

Order Link Src Link Dst Network Src Network Dst Protocol Description 1 MAC-A MAC-C IP-A IP-C DNS query 2 MAC-C MAC-A IP-C IP-A DNS resp. In the following questions, you may not need to use all the lines we provide.

2

[page 3]

1. [4 points] As it just joined the network, the first thing the client needs to do is get an IP address and other related network state. In the next lines, write the packets on the network involved in that step, including their header information.

Order Link Src Link Dst Network Network Protocol Src Dst Description 1 MAC-A MAC-BR -- -- DHCP Discover 2 MAC-B MAC-A -- -- DHCP Offer 3 MAC-A MAC-BR -- -- DHCP Request 4 MAC-B MAC-A -- -- DHCP Acknowledgment 5 6

2. [10 points] Now that the client has an IP address for itself, it wants to resolve the IP address of example.com, which will be IP_H. Write down all the packets involved in this phase. Remember that the client just joined the network.

If a packet’s headers change during transmission (i.e., the IP or MAC address get changed), you should write the packet on two separate lines, corresponding to the two set of headers it sees during transmission. For the description, write the most specific protocol, i.e., “DNS query”, not “UDP”.

Order Link Src Link Dst Network Network Protocol Src Dst Description 1 MAC-A MAC-BR ARP Request 2 MAC-C MAC-A ARP Reply 3 MAC-A MAC-C IP-A IP-C DNS Request 4 MAC-C MAC-G IP-C IP-E DNS Request (to .) 5 MAC-G MAC-E IP-C IP-E DNS Request 6 MAC-E MAC-G IP-E IP-C DNS Reply 7 MAC-G MAC-C IP-E IP-C DNS Reply 8 MAC-C MAC-G IP- C IP-F DNS Request (to .net) 9 MAC-G MAC-F IP-C IP-F DNS Request 10 MAC-F MAC-G IP-F IP-C DNS Reply 11 MAC-G MAC-C IP-F IP-C DNS Reply 12 MAC-C MAC-G IP-C IP-I DNS Request (to example.net) 13 MAC-G MAC-I IP-C IP-I DNS Request 14 MAC-I MAC-G IP-I IP-C DNS Reply 15 MAC-G MAC-C IP-I IP-C DNS Reply 16 MAC-C MAC-A IP-C IP-A DNS Reply 17

3

[page 4]

3. [5 points] Now that the client has IP_H, it wants to download the web page http://example.net/index.html. (Recall that the webpage fits in one data packet.) Write down all network-layer packets that are sent on the wire in order to complete this process. Remember to clean up any transfers.

For the “protocol description”, if the packet is associated with transport layer, you should write something like “TCP SYN”. If it’s inherently an application-level message (i.e., data sent over a TCP connection), you should write something like “HTTP request”. In this example, you should assume that you are running a “basic” TCP implementation, so it’s not doing any fancier optimizations like delayed ACKs or piggybacking.

Order Network Src Network Dst Description 1 IP-A IP-H TCP SYN 2 IP-H IP-A TCP SYN-ACK 3 IP- A IP-H TCP-ACK 4 IP-A IP-H HTTP Request 5 IP-H IP-A TCP ACK 6 IP-H IP-A HTTP Reply 7 IP-A IP-H TCP ACK 8 IP-H IP-A TCP FIN 9 IP-A IP-H TCP FIN-ACK 10 IP-H IP-A TCP ACK 11 12

** Note: We also accepted 8 as IP-A to IP-H (i.e., close initialized by client), and we also accepted a 4-way handshake of FIN, ACK, FIN, ACK.
```

### Question 2.1, 2.2, 2.3, 2.4
- pages: 5-6
- overlap: TCP congestion control, slow start, AIMD/window calculation
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring10-cos461-exam1-answers.pdf>

```text
[page 5]

QUESTION 2 : TCP and Congestion Control (19 POINTS)

Consider the following graph of TCP throughput (NOT DRAWN TO SCALE), where the y-axis describes the TCP window size of the sender. We will later ask you to describe what happens on the right side of the graph as the sender continues to transmit.

1. [ 3 points ] The window size of the TCP sender decreases at the points marked by A, C, and D on the graph, which happens when a packet belonging to the stream is lost. Name the event which occurs that causes the sender to decrease its window.

A: Triple Duplicate ACK

C: Triple Duplicate ACK

D: Timeout

5

[page 6]

2. [ 4 points ] Assume that the network has an MSS of 1000 bytes. If point A occurs 1 second after the sender begins its transfer, and the sender has written 15,000 bytes to the network by that time, what is the round-trip-time (RTT) of the network? Assume at time 0 the sender attempts to open the connection. Also assume that the sender can “write” a full window’s worth of data instantaneously, so the only latency you need to worry about is the actual propagation delay of the network.

First, calculate the number of RTTs needed. 1 RTT for client handshake (SYN  SYN-ACK). Then window size grows during slow start: 1 MSS, 2 MSS, 4 MSS, 8 MSS = 15 MSS = 15,000 bytes. Note that A occurs at the point of detecting triple duplicate ACK, and therefore the client must have seen at least some ACKs from the 8 MSS windows.

Hence a total of 5 RTTs over 1 second = 200 ms

3. [ 4 points ] What is the sender’s window size (in bytes) at point B?

After triple duplicate ACK, the sender halves its window size (part of “multiplicative decrease” of AIMD), thus leaving us at ½ cwnd of A = 4 MSS = 4,000 bytes

4. [ 4 points ] If point C occurs 2 seconds after point B, what is the sender’s window size (in bytes) at point C?

Network RTT = 200 ms, thus 2 seconds = 10 RTT. The sender’s window is currently growing linearly in the “additive increase” part of AIMD, and hence increases by 1MSS every RTT.

Therefore, our prior cwnd was 4 MSS + 10 MSS = 14 MSS = 14,000 bytes

5. [ 4 points] Assume that the window size at point D is 16,000 bytes, at which time it drops to 1,000 bytes. How much time will it take for the sender to return to a window size of 16,000 bytes (assuming that there is no further packet loss in the network)? You can express your answer in terms of the number of RTTs, as opposed to the number of seconds.

After a timeout, the window drops to 1 MSS. It then proceeds to grow via slow-start (i.e., doubling each RTT) until it reaches ½ of the cwnd at the time it detected the timeout. Afterwards, it grows linearly (+1 MSS / RTT).

Thus, we experience slow-start until 8 MSS, which takes 3 RTT. We then increase linearly until 16 MSS, which takes an additional 8 RTT, giving us a total of 11 RTTs.
```

### Question 3.1, 3.2
- pages: 7-8
- overlap: Socket call ordering and looping on send/partial writes
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring10-cos461-exam1-answers.pdf>

```text
[page 7]

QUESTION 3: Socket Programming (16 points) You are implementing a simple application to transfer a file from the client to the server using TCP.

1. [ 5 points ] In the following, write the basic system calls you need to use in order to transfer the file. Assume that the client already has the IP address of the server. You don't need to show arguments, i.e., name resolution could have just been written as gethostbyname (not struct hostent * gethostbyname(const char *name)) and you don't need to show any other programmatic logic. Assume that the file can be written/read in a single call to send/recv.

In the below table, provide a set of system calls in an appropriate order. Each line should have a single call at the client or server, not both. Some calls at the client and server can happen concurrently; just list them in a reasonable order (i.e., the write at the client should occur before the read at the server). Note: You might not need to use all the rows supplied. Remember to cleanup after you transmit the file.

Client Server 1 socket 2 bind 3 listen 4 accept 5 socket 6 bind 7 connect 8 send 9 recv 10 close 11 close 12 13 14 15

*** Note there are multiple different acceptable answers.

7

[page 8]

2. [10 points] Now consider the pseudocode of the client's send call in a bit more depth. Write some pseudocode (it doesn't need to compile, but should look C-like), how you would transmit a 100,000B file. In this code snippet, you should use arguments and return values to express the logic flow.

Your code should only be a few lines long; we're only interested in the logic immediately surrounding your use of the send system call.

// buf points to a buffer of size len // that you want to transmit in its entirety // fd is an open file descriptor connected to server // RETURN 0 ON SUCCESS, -1 ON FAILURE

int sendall (int fd, char *buf, int len) {

int sent = 0;

while (sent < len) {

int bytes_sent = send (fd, buf+sent, len-sent);

if (bytes_sent < 0) return -1; sent += bytes_sent; }

return 0;

}

*** There are multiple other correct solutions here.
```

### Question 4.1, 4.2, 4.3, 4.4, 4.5
- pages: 9-11
- overlap: IP-prefix aggregation, IP/MAC addressing, TCP ACK/loss, ARP-cache conflict, TCP vs UDP selection
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring10-cos461-exam1-answers.pdf>

```text
[page 9]

QUESTION 4: Short answers (29 points)

1. [6 points] IP Address Aggregation

Suppose you are network operator for an ISP, and your ISP has two customer networks (MIT and Princeton). For the sake of simplicity, let’s assume that MIT only has 3 hosts with the following IP addresses, and Princeton only has 2 hosts:

MIT: 18.0.0.1, 18.0.0.254, 18.255.255.254

Princeton: 128.112.0.1, and 128.112.255.254

You’ve heard that memory in router line cards is expensive, so you’d like to use as few entries as possible in your line cards. Your colleague at work says he has a solution that only requires two forwarding-table entries.

(a) Give the IP prefix notation that your colleague uses to represent these two networks.

18.0.0.0/8 and 128.112.0.0/16

(b) After you install the forwarding table entry your colleague suggests, you notice that you still see traffic for host 18.255.255.254, but you’ve stopped seeing any traffic for hosts 18.0.0.1 and 18.0.0.254. So, you come up with a new set of forwarding-table entries – three this time – that, once installed, causes you to receive traffic for all five hosts. What are these three IP prefixes?

18.0.0.0/8, 18.0.0.0/24, and 128.112.0.0./16

(c) Give one possible explanation why this change in part (b) is needed.

18.0.0.0/24 is multi-homed from another provider and, given longest prefix matching for preferred traffic, all traffic was going through its other provider.

Similarly, some other ISP (perhaps again for multi-homing) could be announcing any prefix > 8 bits, e.g., 18.0.0.0/16

9

[page 10]

2. [ 4 points ] Ethernet and IP

(a) Suppose Ethernet was the only existing LAN technology, so every host in the Internet was part of a local Ethernet and thus had a globally-unique Ethernet address. Would you recommend getting rid of IP addresses by simply using Ethernet addresses instead of IP addresses? Why or why not?

No. It would not scale due to (1) the need for broadcast for discovery and (2) forwarding tables would be large as MAC addresses are not topologically assigned and thus cannot be aggregated.

(b) What about the other way around, why do we not simply assign IP addresses to network adaptors, instead of dealing with both Ethernet and IP addresses?

No. Either you keep topological aggregation but then require adaptors to get manually reassigned an IP address whenever moving (a configuration nightmare), or adaptors have static IP addresses but then you would sacrifice routing table aggregation (a scalability nightmare).

3. [ 8 points ] Using TCP, a sender has sent out packets 1 through 20. The sender receives an ACK for packet 10, then it receives three ACKS for packet 11 (i.e., if the final byte of packet 11 was byte no. 5000, then these ACKs were for byte 5001). Given this result:

(a) Which of the 20 packets can the sender assume are lost?

12

(b) Which of the 20 packets can the sender assume were definitely received?

1 - 11

Now, the same sender resends the next missing packet and receives an ACK for packet 16 in response. Based on this information:

(c) Which packets of the original 20 can the sender assume are still lost, if any?

None

(d) Which of the original 20 can the sender assume were definitely received?

1-16

10

[page 11]

4. [ 5 points ] Assume you have a network with three hosts – A, B, and C – all directly connected to the same switch. Host A first attempts to open a TCP connection to B at time 0, during which time he adds an entry to his ARP cache with a TTL of 60 seconds. Host B begins transferring a large file to host A. A new host D connects to the network, but is configured with the same IP address as already being used by A.

At time 55 seconds, an application running on host D opens a TCP connection to an application on C. A few seconds later, the TCP transfer between hosts A and B breaks. What were the steps that led to this connection breaking?

At time 60, host B’s ARP cache expires, so when it re-issues an ARP request for the IP address shared by A and D, D’s answer is cached by B. Thus, B’s TCP packet gets sent to MAC-D, who, not having such an open TCP connection, will reply with a TCP-RST, causing B’s connection to break. (Similar for A and its ARP cache)

5. [ 6 points ] What transport layer protocol (TCP or UDP) you would use if your application needed one of the following properties and then give one succinct reason why. Be specific.

(a) Speed - UDP – no connection setup or sender-side buffering

(b) Long messages – TCP – as stream-of-bytes abstraction supports arbitrarily long messages. Many stacks limit UDP messages to some maximum size (e.g., 64KB)

(c) Short-duration interactions – UDP – No connection setup delay

(d) Fairness between competing flows – TCP – Fairness through congestion control

(e) Flooding – UDP – No connection state needed

(f) Flexibility – UDP – More application-level control
```

### Question 5.2, 5.3, 5.6
- pages: 12-13
- overlap: UDP/TCP socket demultiplexing fields; RED/drop-tail/congestion
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring10-cos461-exam1-answers.pdf>

```text
[page 12]

QUESTION 5: Multiple choice (17 points)

1. What is the name of the forwarding device in the middle of the diagram below? (Circle ONE answer – 1 point)

(a) Switch
(b) Router
(c) Hub
(d) Repeater

2. When a UDP segment arrives at a host, in order to direct the segment to the appropriate socket, the operating system’s network stack uses the following fields: (circle ALL that are true – 2 points)

(a) the source IP address.
(b) the destination IP address
(c) the source port number
(d) the destination port number

3. When a TCP segment belonging to an existing connection arrives at a host, in order to direct the segment to the appropriate socket the operating system’s network stack uses the following fields (circle ALL that are true – 2 points)

(a) the source IP address.
(b) the destination IP address
(c) the source port number
(d) the destination port number

12

[page 13]

4. Which of the following link protocols best describes Ethernet? (circle ONE – 1 point)

(a) frequency-division multiple access (FDMA)
(b) time-division multiple access (TDMA)
(c) token-passing
(d) carrier sense multiple access (CSMA)

5. If you are building a network in which only one host will be sending traffic, which of the following link protocols would give the best throughput? (circle ONE – 1 point)

(a) frequency-division multiple access (FDMA)
(b) time-division multiple access (TDMA)
(c) token-passing
(d) carrier sense multiple access (CSMA)

6. Which of the following are advantages that RED has over drop-tail queuing? (circle ALL that are true – 3 points)

(a) has fewer burst losses
(b) has shorter queuing delays
(c) ensures roughly equal throughput for all flows
(d) ensures roughly equal throughput for all TCP flows

7. Which of the following are true about Ethernet networks? (circle ALL true – 3 points)

(a) Ethernet frames have a minimum size to ensure good utilization of the network (i.e., senders could otherwise have a large overhead to send a small piece of data).
(b) Bridges provide greater scalability for Ethernet networks than hubs.
(c) Hosts on different segments of a switched Ethernet network will only see packets to hosts on their segments or to the broadcast address.
(d) When an Ethernet sender detects that the media is idle, it sends a jam signal onto the media to tell other devices not to transmit, and then it sends its packet.

8. Which is true of the UNIX Socket API? (circle ALL that are true – 3 points)

(a) If a chunk of data written to a TCP socket is smaller than the MSS, it will all be sent in the same packet.
(b) Writing a single message to a UDP socket can result in the network stack sending multiple packets.
(c) The socket allocated by the accept() system call is assigned a new port number
(d) You can call connect() on a UDP socket

9. [1 point] Describe one thing you would like to see changed in the class. (Only wrong answer is "nothing")
```

## Princeton COS 461 Computer Networks / Spring 2010 Final

### Question 1(A), 1(B), 1(C), 1(D), 1(E); Question 2(a), 2(b), 2(c)
- pages: 2-3
- overlap: HTTP redirection, DNS server selection, IP anycast, NAT/load balancer, ARP spoofing; IPv6; flow-table TCP/UDP filters; IP-header troubleshooting
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring10-cos461-exam2.pdf>

```text
QUESTION 1: Network system engineering (13 points) You have recently been hired by FinBook, the online social network for fish. FinBook currently runs on a single server. To support future growth, you hope to deploy multiple servers in multiple datacenters located at different points in the Internet, with a special focus on providing good performance and failure recovery. List some of the pros and cons of using each of the following technologies. Try to give the “best answer” and be specific. Vague comments such as “low overhead” will not get credit (overhead in terms of what?).

A) HTTP redirection 1 advantage:

1 disadvantage:

B) DNS server-selection 1 advantage:

2 disadvantages:

C) IP anycast 2 advantage:

2 disadvantages:

D) NAT + load-balancer 1 advantage:

1 disadvantage:

E) ARP spoofing (unsolicited announcement of your MAC with other’s IP address) 1 advantage:

1 disadvantage:

2

[page 3]

---

QUESTION 2: More network system engineering (13 points)

(a) You graduated from Princeton (yay!) and joined a social media startup that wants to rival Facebook (at least you hope). The startup doesn’t have any funding, so you took your implementation of simple router and are running it on a Linux box, using it as a router for your servers (instead of paying $$ to Cisco). As your company scaled, you started seeing some clients that use IPv6. Your servers understand IPv6, but your router doesn’t. Describe two ways in which you can extend your router to handle IPv6 traffic:

Option 1: (answer <= 2 lines)

Option 2: (answer <= 2 lines)

(b) You are at Princeton for reunions and get a work phone call saying that the servers are running extremely slow and they believe the servers are under a DOS attack. You think this is your competitors (maybe Facebook is afraid of you after all!) and use your iPhone to ssh into your Linux machine. You remember that while implementing a flow table, 0 meant block and 1 meant allow. TCP’s protocol # is 6 and UDP’s is 17. What entries will you add in the flow table to do the following:

‐ Allow all TCP traffic from Princeton (128.112.0.0/16) ‐ Ban all traffic from 66.220.0.0/16 ‐ Allow UDP traffic to server 69.65.28.126:3333

Your entries should have the following format: <source IP, destination IP, protocol number, src Port, dst Port, 0 or 1>
```

### Question 3(a), 3(b), 3(c), 3(d.i), 3(d.ii)
- pages: 5-6
- overlap: Distance-vector routing tables, count-to-infinity, path-vector loop avoidance
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring10-cos461-exam2.pdf>

```text
QUESTION 3: Distance-Vector Routing (9 points) The CS department at Princeton bought new Sun Fire V210 servers. They decided to run a distance-vector protocol for routing between these servers (even though it is a rather small network). They are currently configured as the picture below, with respective edge costs.

The CS staff asked for your help. Write down each step of building the distancevector routing table for ‘Eve’ so they can compare it to the output of their implementation. You can use abbreviations e.g., ‘A’ for Adam and ‘E’ for Eve.

The initial routing table at node A is:

Destination Cost Next Hop B 21 B C ∞ --- D 15 D E ∞ ---

(a) Show the initial routing table of node E:

Destination Cost Next Hop A B C D

5

[page 6]

(b) Show the routing table of node E after one iteration of the algorithm:

Destination Cost Next Hop A B C D

(c) Show the routing table of node E after two iterations of the algorithm:

Destination Cost Next Hop A B C D
```

### Question 4(a), 4(b), 4(c), 4(d)
- pages: 7-8
- overlap: Routing/addressing/tunneling headers, NAT, IP/MAC/MPLS
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring10-cos461-exam2.pdf>

```text
the path shown by a heavy dark lines, which includes both an IP tunnel and an MPLS tunnel. All packets which traverse the path use both tunnels. The various network interfaces have IP and MAC addresses as shown.

H1 has established an HTTP session with web server H2 and data packets are flowing between the two machines. As an example, we have filled in the headers for packet 1 (traveling from the server H2 to the client H1). If there shouldn't be any source or destination field for the header type, write an "X" in that table entry.

Header Type Source Destination Ethernet MAC 16 MAC 15 IP 3.0.1.2 1.2.3.4

You have to fill in the header type and the source and destination address for the network and data-link layer headers for packets 2, 3, 4, and 5 (these packets are all traveling from the client H1 to the server H2). Note: You might not need to use all the rows supplied.

7

[page 8]

(a) Header for packet 2: Header Type Source Destination

(b) Header for packet 3: Header Type Source Destination

(c) Header for packet 4: Header Type Source Destination

(d) Header for packet 5: Header Type Source Destination
```

## Princeton COS 461 Computer Networks / 2009 Mid

### Question 1A, 1B, 1C, 1D
- pages: 2-3
- overlap: Transmission delay, TCP slow start, duplicate ACK vs timeout loss detection
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring09-cos461-exam1-answers.pdf>

```text
QUESTION 1: Transporting a file (15 POINTS)

Suppose your boss calls you up while visiting a client and says he left a 250,000 byte file on a server at the office, and he needs you to send it to him. The connection between the office and his current site is 2 million bits/second.

1A. [2 points] Assuming that all bandwidth is consumed by your data (e.g., there aren’t any packet headers, there’s no other traffic on the link, etc.) and that you can immediately start sending data at the maximum rate, how long will it take to transmit the file? (Easy)

250,000 bytes * (8 bits / 1 byte) * 1/2,000,000 bits/s = 1 second

1B. [5 points] Now assume that you are sending the file via TCP, with a maximum segment size of 1000 bytes. You have to follow TCP’s transport algorithm, so you start transmitting the file at a low rate. How many network round trip times (RTTs) will it take to transmit the entire file? Again assume that all bandwidth is consumed by your data.

TCP needs to first establish a connection via a handshake (SYN/SYN-ACK) - 1 RTT TCP then enters slow-start to transmit the file, so we run slow-start either until we've transmitted the file or until we experience a loss (at 2Mbps). In slow-start, TCP will initially transmit a window of 1 MSS (=1000 bytes) per RTT, then double the window size each round (RTT). So, we have:

1 MSS, 2 MSS, 4, 8, 16, 32, 64, 128

The sum of the above 8 transfers is 255 MSS = 255,000 bytes > 250,000 byte file, so we declare ourselves finished after the 8th RTT.

Thus, the total time to transmit the file would be 1 + 8 = 9 RTT.

Note: One might debate what "transfer" means, so we also accepted 7.5 RTTs for the number of runs in slow-start, as the final transfer of 128 might not strictly need to ACK. We did not take off any points if people also included 1 RTT for FINs.

2

[page 3]

1C. [4 points] Let’s now consider how TCP reacts when it encounters packet loss (the “basic” variant we learned in class). Your boss now wants you to transmit a much larger file (say, 1 GB). This time around, after TCP reaches an instantaneously transmission rate of 32,000 bytes per second, you notice that a single packet is lost. Assuming that you don’t currently have any other packets in transmission, what is the instantaneous rate TCP will send at after noticing that loss? How long (in terms of RTTs) will it take to reach 32,000 bytes per second again?

This question was meant to seek how TCP reacts to detecting loss via a triple duplicate ACK. In that case, TCP reacts by "MD" -- multiplicative decrease -- cutting its window size by half and continuing by "AI" -- additive increase.

So the next transmission rate is 16,000 bytes per second, and it will take 16 RTTs to recover to its prior levels (each RTT increases by 1 MSS = 1000 bytes).

1D. [4 points] In the previous example of 1c, would anything be different if all packets were lost after you reached 32,000 bytes per second, instead of just a single packet? If so, what is the next instantaneous rate TCP will send at in this example, and how long (in terms of RTTs) would it now take to reach 32,000 bytes per second again?

Because all packets are lost, we only detect loss through a timeout. This causes the sender's window to be reduced to a single MSS (1000 bytes / RTT), at which time it enters "slow-start restart". Namely, it will perform slowstart until half of its prior cwnd (16,000 bytes/second), then do additive-increase from 16,000 to 32,000 bytes/second.

(In fact, the question as written didn't include quite enough information, as you actually do need to know the RTT in this example in order to calculate the window size for "16,000 bytes / seconds", i.e., if RTT is 500ms, window size is 8 MSS/RTT, while window size would be 16 MSS/RTT if RTT is 1s. Everybody just assumed implicitly that RTT=1s, and that the next rate after the timeout was 1000 bytes/sec. We initially had written these questions with an explicit RTT and asked you to solve the question in terms of time, rather than RTTs, but subsequently removed this information to reduce needed calculations.)

That said, assuming RTT=1s, then the answer is: Slow-start from 1 MSS to 16 MSS = 4 RTTs, then additive increase 16-32 MSS = 16 RTTs Total = 20 RTTs (we also accepted 21 RTTs given various ways to "count" these values)
```

### Question 2A, 2B, 2C
- pages: 4-6
- overlap: TCP socket call ordering, TCP stream packetization, UDP datagram packetization
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring09-cos461-exam1-answers.pdf>

```text
QUESTION 2: Sockets (16 POINTS)

2A. [10 points] In the first assignment, you used the socket API to write a simple client/server. For this question, there is a single client communicating with a single server using TCP. The client sends a very small amount of data using the send() function, and the server receives the data with a recv() call. Each of the following scenarios shows a diﬀerent order in which the socket calls are called on both the client and the server.

Assume all system calls are blocking, and there may be some latency between the client and server. We write the system call when it is initiated by the client and/or server; it returns sometime between then and when the next local system call is executed.

For each scenario, answer the following: Can the server ever get the data sent by the client? (Yes or No). If not, explain why not.

i) Client Server socket() socket() bind() connect() listen() send() accept() close() recv() close()

No. connect() wouldn't successfully return, allowing you to send(), before client accepts().

ii) Client Server socket() connect() send() socket() bind() listen() accept() recv() close() close()

No. Same explanation as (i). Also valid reason is that server isn't listening() when client attempts to connect().

4

[page 5]

iii) Client Server socket() socket() bind() listen() accept() connect() send() recv() close() close()

Yes.

iv) Client Server socket() socket() bind() listen() accept() recv() connect() send() close() close()

No. Accept() wouldn't return with a valid file descriptor until client has connected().

v) Client Server socket() socket() connect() bind() listen() accept() recv() send() close() close()

Yes.

5

[page 6]

2B. [3 points] Suppose application A is using a stream (TCP) socket to transfer data to application B on a remote host. Suppose application A writes (sends()) data into the socket buffer ten times.

i) Can the underlying network stack transmit more than ten data packets? If so, why?

Yes. If a write is larger than the MSS, then TCP might transmit it within two packets. Certainly if your total number of written data is larger than 10 MSSs, you are guarnateed to have more than 10 TCP packets. (Also accepted as a valid answer, though not what we were expecting, was that additional packets could be caused by packet retransmission from loss.)

ii) Can the underlying network stack transmit fewer than ten data packets? If so, why?

Yes. Small writes can be coalesced into single data packets using Nagle's algorithm.

2C. [3 points] Suppose application A is using a datagram (UDP) socket to transfer data to application B on a remote host. Suppose application A calls sendto() ten times.

i) Can the underlying network stack transmit more than ten data packets? If so, why?

Yes. UDP packets larger than the network MTU will experience IP fragmentation.

ii) Can the underlying network stack transmit fewer than ten data packets? If so, why?

No.
```

### Question 3A, 3B
- pages: 7-8
- overlap: Web browser request flow with DHCP/ARP/DNS/TCP/HTTP/cache
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring09-cos461-exam1-answers.pdf>

```text
QUESTION 3: Your Web Browser in action (17 POINTS)

In the topology shown below, machine A is a desktop client, D is a local DHCP server, R is A's gateway router, S is a Web server, and C is a Web cache. NL is C's local nameserver, while NA is the nameserver authoritative for S. Client A is configured to use Web cache C for all requests (assume that the Web cache resolves the name for any Web server and that the client is configured with the IP address of the cache). All wires/links are Ethernet segments.

Assume the following: • All the machines were just booted and their associated caches (ARP, DNS, Web, persistent connections) are all empty • http://S/index.html fits in a single packet • Persistent HTTP connections are used among A, C, and S (i.e. you should assume that once any connection between these hosts is established it is never closed) • Web caches respond to TCP requests that look like packet two in table 1 below (e.g., GET http://foo/bar/). They reply with the normal web cache contents.

7

[page 8]

3A. [12 points] The user on machine A, requests the web page http://S/index.html. The table below shows a number of messages sent/received in servicing this request (this is not necessarily a complete list of all packets). In addition, there are a few bogus packets that are never sent/received. The packets are not listed in temporal order.

ID SRC DST SRC Port DST Port Protocol Contents 1 C DNS root DNS UDP Query for S 2 A C Web cache TCP GET http://S/index.html 3 NL DNS root DNS UDP Query for S 4 C S HTTP TCP SYN 5 C S HTTP TCP GET index.html 6 S A HTTP TCP index.html 7 A Broadcast ARP Who is R 8 C A Web cache TCP index.html 9 NL C DNS UDP Address for S 10 S C HTTP TCP index.html 11 A Broadcast DHCP UDP DHCP Request from A 12 NL NA DNS UDP Query for S

List the proper order of packets (in terms of their IDs) that are sent on the network:

11, 7, 2, 3, 12, 9, 4, 5, 10, 8

3B. [5 points] Assume that the client A has no local Web or DNS cache and that cache C has no DNS cache. However, all other cacheable things are cached. On a subsequent request for http://S/ index.html, which of your items from your list in 3A would be eliminated? (Use the ID column to name the messages.)

11, 7, 3, 12, 9, 4, 5, 10

(The trickiest number was 9, because we said that C doesn't have a DNS cache. However, if it has the object for http://S/index.html cached, it can serve it directly there without going to server S, hence it never needs to do a DNS lookup on S in the first place.)
```

### Question 4A, 4B, 4C, 4D, 4E, 4F, 4G
- pages: 9-10
- overlap: Routing vs bridging, layer-2/layer-3 addressing, ARP
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring09-cos461-exam1-answers.pdf>

```text
QUESTION 4: A routed and bridged network (14 POINTS)

R2b.ip R2b.mac R2 R2c.ip SRC DST R2c.mac H1.ip R2a.ip H2.ip H1.mac R2a.mac H2.mac

B1.ip B2.ip B1a.mac B1.ip B1c.mac B2b.mac B2.ip B2 B1 B2a.mac B1.ip B1b.mac

Above is a picture of a network with 2 bridges and 1 router. Each interface is labeled with both an IP address and a MAC address. Imagine that host H1 is sending a packet to host H2. Please answer the following questions about this figure:

4A. How many (datalink) networks are shown above?

3 -- The networks hanging off of R2

4B. Just before the packet reaches bridge B1, what is its layer 2 destination?

R2a.mac

4C. Just before the packet reaches bridge B2, what is its layer 2 source?

R2c.mac

4D. Just after the packet leaves router R2, what is its layer 3 source?

H1.ip

4E. When H1 sends out an ARP query, what is the reply to that query?

R2a.mac has R2a.ip (or just "R2a.mac")

9

[page 10]

4F. Does the entry B2a.mac appear in B1’s forwarding table?

No. B2a is on a different datalink network than B1.

4G. Will SRC's Ethernet device receive packets with destination R2a.mac? Why / why not?

This turned out to be a more confusing question than we intended, depending on how you interpreted the question. We accepted both "yes" and "no" answers here, but your explanation why had to be correct:

No -- because B1 is a (learning) bridge and any packets to R2a sent by nodes in on the "B1b.mac" or "B1c.mac" broadcast domains will be filtered by B1, so will only be re-broadcast out the B1c link.

Yes -- if the sender is in the same local broadcast domain (the "B1a.mac" domain) as SRC, then SRC will receive those packets.

Yes -- if B1 or R2 has just come online and B1 hasn't yet learned local MAC addresses of nodes, then it could forward packets out all interfaces.
```

### Question 5C, 5F, 5G, 5H
- pages: 11-12
- overlap: ARP/bridges, DNS TTL/records, web caches, persistent HTTP
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring09-cos461-exam1-answers.pdf>

```text
QUESTION 5: Multiple choice (16 points)

Correct answers are marked in bold and underlined.

5A. Which best describes the Ethernet protocol? (Circle ONE) A. Talk only if you hear no one else talking, but stop as soon as you hear anybody else. B. Pass a ticket around and only talk if you are holding the ticket. C. Raise your hand and wait till a moderator gives you permission to talk. D. Every person is scheduled a time to talk.

5B. Which of the following is/are true about Ethernet: (Circle ALL that are correct) A. CRC error detection, as used in Ethernet, cannot always detect if there is a frame error. B. In the Ethernet CSMA/CD protocol, suppose that an adapter constructs a frame to send and then senses that the channel is busy. The adapter then enters exponential back-off. C. Entries in an Ethernet bridge table must be configured by a network administrator. D. An Ethernet adapter always passes all non-corrupt frames that it receives up to the network layer.

5C. Which of the following is/are true about Address Resolution Protocol (ARP) and learning bridges? (Circle ALL that are correct) A. A learning bridge maintains state that maps IP addresses to hardware (MAC) addresses. B. A learning bridge maintains state that maps MAC addresses to IP addresses. C. A host’s ARP table maintains state that maps IP addresses to hardware (MAC) addresses. D. A host’s ARP table maintains state that maps hardware addresses to IP addresses.

5D. Which of the following is/are true about a communications channel that uses time- division multiplexing? (Circle ALL that are correct) A. There may be times when the channel is idle, even if a sender has data to send on the channel. B. The channel requires the sender’s and receiver’s clocks to be closely synchronized. C. Data in the channel could experience variable delays due to queuing. D. In times of high utilization, a sender could be completely denied access to the channel.

5E. Which of the following is/are true about increase/decrease policies for fairness and

11

[page 12]

efficiency in congestion control? (Circle ALL that are correct) A. Additive increase reduces fairness. B. Additive increase improves efficiency. C. Multiplicative increase improves fairness. D. Multiplicative decrease improves fairness.

5F. Which of the following is/are true about DNS? (Circle ALL that are correct) A. A query for an A record may return multiple IP addresses in the response. B. A query for an NS record may return multiple IP addresses in the response. C. A short TTL on an NS record reply runs the risk of increasing traffic at the root or GTLD nameservers. D. A short TTL on an A record reply runs the risk of increasing traffic at the root or GTLD nameservers.

5G. Which of the following is/are true about web caches? (Circle ALL that are correct) A. A web cache, or proxy server, is a network entity that satisfies HTTP requests from clients. B. A web cache is both a client and a server at the same time. C. HTTP does not explicitly support caching or cache consistency. D. All HTTP objects are cacheable.

5H. Which of the following is/are true about persistent HTTP connections? (Circle ALL that are correct.) A. Persistent HTTP allows a server to track the client’s requests through a persistent session. B. Only one TCP connection must be opened for downloading a "page", if that page does not include any embedded objects served by other servers. C. Persistent HTTP shows the greatest performance advantage over nonpersistent HTTP when downloading a page with large objects. D. When the server has finished sending data for all objects referenced by the initially requested page, the server closes the connection.

For this question, we also marked correct if one circled A, as the question was perhaps overly confusing (and virtually everybody got the answer wrong). Strictly speaking, persistent HTTP does not establish application-layer sessions, that's typically done through cookies. This is the case because "application-level" sessions exist independently of a single TCP connections. It can more obviously be seen through the use of web proxies -- a web proxy can/will multiplex requests from different clients over a single TCP connection with the server. That said, while 5G and 5H should be answerable given assignment 2, this particular question (5H-A) might have been difficult without lecture 16, so we decided to effectively give everybody credit.
```

### Question 6A, 6B, 6C, 6D, 6E, 6F, 6G, 6H
- pages: 13-15
- overlap: Soft state, exponential backoff, TCP SYN retransmissions, DNS/UDP, NAT, ECN, protocol layers
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring09-cos461-exam1-answers.pdf>

```text
QUESTION 6: Short Answer (22 points)

6A. [2 points] Explain the principle of soft state. Provide two examples of a network protocol or technology that abides by soft state.

Soft state refers to some type of stored state that is not "hard" (i.e., persistent, consistent, explicit, etc). In the context of the applications we saw, soft state is often only stored temporarily by some entity, often for only some explicit or implicit time period, and it must often be constantly refreshed to survive network changes or failures or persist over time. Existence of soft state should not be critical from receiving correct service; that is, it is often an optimization.

Accepted answers: ARP tables, DNS caches, DHCP addresses that persist over leases, ...

6B. [2 points] List two protocols that use exponential backoff, and describe what/where problems would occur if each protocol did not backoff.

TCP congestion control uses exponential backoff (multiplicative decrease). If it did not backoff, congestion would build up at routers, and queues would continue to be full and continue to drop packets, leading to low throughput.

Ethernet CSMA/CD uses exponential backoff. If it did not backoff, collisions would continue to occur on the shared medium, leading again to low goodput.

6C. [3 points] List three possible explanations for why host A would need to retransmit the SYN packet as part of establishing the TCP connection with B.

SYN packet from A to B dropped by router on path. SYN packet dropped by B because B's receive backlog is full. SYN-ACK packet from B to A dropped by router on path. SYN-ACK not received by A before timeout occurs. SYN dropped by firewall or NAT in front of B.

6D. [1 point] Give one reason that DNS lookups are run over UDP rather than TCP

DNS is a simple query/response protocol, thus avoids connection setup (at least 1 RTT) for TCP and its state overhead. This is especially true as DNS queries and responses are typically small and can thus often fit in a single packet. Because its a connectionless protocol, also more amenable to anycast IP addresses for DNS servers, useful for failover. UDP headers are also smaller than TCP headers, which reduced bandwidth overhead for queries.

13

[page 14]

6E. [2 points] Give two reasons that sites use Network Address Translators (NATs):

Allows multiple private addresses behind single public (dedicated) address, which is very helpful if sites lack a sufficient number of public IP addresses (e.g., "space" pressure). In general, NATs have helped "scale" IPv4.

NATs provide privacy about internal deployments.

NATs can allow easily management of internal devices, so that machines can be internally renumbered without changing their external (public) addresses.

If explicit forwarding rules aren't configured in NATs, they often provide some security mechanisms by playing the role of firewalls, e.g., only allowing TCP connections to be initiated from internal nodes, as opposed to allowing external machines to connect to internal machines.

...

6F. [3 points] When a packet is going from a local-area network onto the wider Internet, what header fields might a Network Address Translator (NAT) change that is deployed on path?

source IP address, source port, IP checksum, transport (TCP/UDP) checksum

6G. [3 points] How does explicit congestion notification (ECN) differ from traditional ways of detecting congestion on Internet paths? Describe one benefit for using ECN and one reason it might not widely be used today.

ECN signals to senders that congestion has occurred by marking packets explicitly, as opposed to signalling by "dropped" packets. This allows end-hosts to react to congestion without unnecessary loss, especially useful, for example, when routers might be using RED, or for interactive application-level protocols such as telnet and web browsing that are very sensitive to the delay caused by loss and retransmission. ECN is not widely used today, however, in that it requires that both the sender, recipient, and network elements (routers) all support ECN, so it creates a deployment challenge.

14

[page 15]

6H. [4 points] The OSI model is traditionally seen as a 7-layer stack consisting of the following. For several of the layers, give one or two examples of protocols that are associated with each layer:

Application 2 examples: FTP, HTTP, SMTP, telnet, SIP, ...

Presentation

Session

Transport 2 examples: TCP, UDP, DCCP, ...

Network 1 example: IPv4, IPv6

Data link 2 examples: Ethernet, PPP, token ring, FDDI, 802.11

Physical 1 examples: We accepted both physical techologies (twisted pairs, CAT5, fiber, ...) and encodings (Manchester, NRZ, ...)

6I. [1 point] What's the first name of your favorite TA? Why?

Jeff (22 votes) and Wyatt (15 votes)

6J. [1 point] Describe one thing you would like to see changed in the class. (Only wrong answer is "nothing".)
```

## Princeton COS 461 Computer Networks / Spring 2008 Mid

### Question 1(a), 1(b), 1(c)
- pages: DOC
- overlap: IP addressing vs MAC addressing; host mobility; DHCP/ARP/MAC learning; hierarchical vs flat forwarding tables
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring08-cos461-exam1-answers.doc>

```text
QUESTION 1: Big MAC (15 points)

This question explores whether the Internet could be designed using only names (like HYPERLINK "http://www.frieswiththat.com" www.frieswiththat.com ) and MAC addresses, without a need for IP addresses. Suppose each network adapter, for any link technology, has a unique MAC addresses from a single address space (such as 48-bit MAC addresses used for Ethernet devices), and these addresses were used Internet-wide for communication between end hosts. Suppose that the Domain Name System (DNS) is changed to return MAC addresses rather than IP addresses, in response to queries.

(1a) In todays Internet, why is it difficult to support continuous communication with a host while it moves? Why would an Internet based on MAC addresses have the potential to make mobile hosts easier to support?

Mobility is difficult to support in todays Internet because a hosts IP address changes as it moves, since IP addresses are allocated to institutions in a hierarchical fashion. Dynamic changes in the hosts IP address make it difficult to sustain a connection (e.g., TCP or UDP socket) with another host. An Internet based on MAC addresses would allow the hosts identifier to stay the same as it moves.

(1b) Todays local area networks have several boot-strapping techniques, such as DHCP, ARP, and MAC learning. In a world without IP addresses, which of these techniques would still be necessary? Explain your answer.

DHCP would no longer be needed to assign an IP address or network mask to the host, though a similar mechanism may still be needed to configure the address of the local DNS server and the gateway router. ARP would no longer be necessary, as there would be no need to map an IP address to a MAC address. MAC learning would still be necessary to enable switches to learn how to forward frames to a host based on its MAC address.

(1c) How would moving to an Internet based on MAC addresses affect the size of the forwarding tables in the network nodes (i.e., routers or switches)?

Forwarding tables could grow quite large because MAC addresses are not hierarchical. Today, routers store ~200K IP prefixes that represent a much larger number of hosts. Within a local area network, switch forwarding tables could likely stay the same size, as hosts could direct external traffic (destined to the rest of the Internet) to the gateway router.
```

### Question 3(a), 3(b), 3(c), 3(d)
- pages: DOC
- overlap: TCP receive window, goodput/congestion, retransmission timeout vs duplicate ACK, router queueing/buffering
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring08-cos461-exam1-answers.doc>

```text
QUESTION 3: Going With the Flow (10 points)

(3a) A home user upgrades from a dial-up connection to high-speed broadband, but does not see much improvement in Internet performance for visiting a Web site. Give one reason why this might happen, even if the network and the Web server have ample capacity.

The size of the receiver window (RWIN) may limit the throughput. In particular, the throughput is limited by the RWIN/RTT, where RTT is the round-trip time between the host and the Web server. The home user can improve performance by changing the maximum TCP receiver window (e.g., from 16 KB to 64 KB).

Also, most Web transfers are short (e.g., fewer than 10 packets long). For these transfers, the download time is typically dominated by the round-trip time, as the TCP connection doesnt get out of slow start and does not fill the receiver window.

(3b) When a path through the Internet becomes overloaded, the total goodput seen by all end users can actually decrease. Explain why.

When the network is congested, many packets travel part way through the network, only to be lost and ultimately retransmitted by the sender. The wasted bandwidth may cause other packets to encounter congestion, and experience packet loss and subsequent retransmission, leading to an overall drop in the rate of successful packet delivery.

(3c) Why are many packet losses in wireless networks detected by a timeout rather than a triple-duplicate acknowledgment? What are the performance implications?

Wireless networks tend to experience bursty packet losses due to interference (e.g., signal blocked by a building). This decreases the likelihood that, in the same TCP sending window, some packets are lost while others are successfully delivered. The successful deliveries are necessary to trigger the receiver to send duplicate acknowledgments. As such, bursty loss tends to require the sender to rely on the retransmission timeout to detect the loss. (In addition, many wireless networks have relatively low capacity, leading the sender to have a relatively small congestion window. This also decreases the likelihood that enough packets are successfully delivered to enable detection of an earlier packet loss by duplicate acknowledgments. Similarly, wireless users may do smaller transfers, due to limited bandwidth or small screen sizes of PDAs, and small transfers offer less opportunity for multiple packets in flight during the same RTT.)

(3d) A router maintains a queue of packets awaiting transmission on a link. Selecting the right buffer size is a challenging problem. Give one reason why a large buffer would be desirable. Give two reasons why a larger buffer might be undesirable.

A larger buffer can temporarily accommodate a burst of packets without dropping any of them, avoiding unnecessary retransmissions. However, a larger buffer would (i) increase the round-trip time leading to higher and more unpredictable delays, (ii) increase the time for the TCP senders to learn about impending congestion, and (iii) make the router more expensive (due to more memory chips and higher power requirements).
```

### Question 4(a), 4(b), 4(c), 4(d)
- pages: DOC
- overlap: TCP three-way handshake, HTTP persistent connections, HTTP pipelining, TCP byte-stream read behavior
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring08-cos461-exam1-answers.doc>

```text
QUESTION 4: Caught in the Web (15 POINTS)

(4a) In the three-way handshake to open a TCP connection, host A sends a SYN, host B sends a SYN-ACK, and host A sends an ACK. When can the TCP implementation at host A start sending data packets? When can the TCP implementation at host B start sending data packets? Explain why they cannot start sending any sooner.

Host A can start sending upon receiving the SYN-ACK, since that signals to host A that B is willing to accept traffic and knows As initial sequence number. Host B can start sending traffic upon receiving the ACK, since that signals to host B that A is willing to accept traffic and knows Bs initial sequence number.

(4b) HTTP/1.1 supports persistent connections, where multiple request-response exchanges use the same TCP connection. With pipelining, the client might send multiple requests before receiving any responses. How does the server know where one request ends and the next begins?

The server identifies request boundaries by parsing the HTTP requests, e.g., based on the CRLF and/or the Content-Length.

(4c) Following up on question 4b, the underlying TCP implementation does not ensure that each read() or recv() call returns a single complete HTTP request. Give two reasons (or examples) why the TCP implementation in the operating system cannot do this.

The TCP implementation provides a stream-of-bytes abstraction, without any knowledge of the syntax of the application-layer message(s). Also, the application-layer message may be larger than the operating systems receiver buffer and/or the buffer provided by the application, making it impossible for the operating system to provide the entire request in response to a single read() or recv() call. Also, it is possible that the full request (even if it could fit in the buffer) has not arrived yet, causing the read/recv call to return only the data that has arrived thus far.

(4d) Give two reasons why persistent connections and pipelining were added to HTTP/1.1. Why, then, do Web browsers typically disable pipelining by default?

These features were added to HTTP to (i) avoid the extra TCP traffic needed to open and close many TCP connections, (ii) avoid repeating slow start and the whole process of relearning the congestion state of the path through the network, (iii) to ensure fairness across different Web clients receiving traffic over the same path, and (iv) to reduce the number of round-trip delays experienced by the user in downloading a Web page.

Web browsers often disable pipelining because (i) parallel connections may allow the client to experience higher throughput (possibly at the expense of other users) and (ii) parallel connections enable the simultaneous download and display of multiple embedded images.
```

### Question 5(a), 5(b), 5(c), 5(d), 5(e)
- pages: DOC
- overlap: NAT and FTP active/passive mode, payload rewriting, sequence/ACK adjustment, MTU fragmentation
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring08-cos461-exam1-answers.doc>

```text
ient uses this connection as a control connection for sending commands (e.g., to list files, request file transfers, and change directories). The actual file transfer uses a separate TCP connection. Hence, unlike HTTP which has a single connection for both control and data, FTP has out of band control over a separate connection.

The client and the server need to agree on the port numbers to use for the separate data-transfer connection. In one solution, called active mode, the client opens a socket with a dynamic port and sends the IP address and port number to the server (using the existing control connection) so the server knows what client address and port number to use for the data-transfer connection. (For example, the client on IP address 192.168.0.1 that chose port 49152 for the data connection might send a command like PORT 192.168.0.1 49152 over the control connection.)

(5a) Active mode can cause problems when the client host resides behind a NAT box. Why?

The NAT box maps the IP address and port number of the clients data connection to new values. As such, the arguments the client sends in the PORT command (sent over the control connection) would not match the values the NAT box would use. In addition, the server would have trouble initiating a data connection to a client lying behind a NAT box, without the NAT box already having a table entry for the associated connection; since the client has not transmitted any packets on the data connection yet, the NAT box would not yet have an entry installed when the server sends the initial SYN packet. Worse yet, the IP address in the PORT command is a private, non-routable address, so the FTP server would not be able to direct a packet with this destination address to the appropriate place.

(5b) Suppose a NAT box wanted to correctly handle clients running active mode FTP. What actions would the NAT box need to perform on FTP control messages from the client?

The NAT box would need to parse the messages sent on the FTP control connection (i.e., on port 21) to extract the arguments of the PORT command. The NAT box would need to create a table entry for the data connection and modify the arguments in the PORT message accordingly, so the FTP server can successfully create and use the data connection.

(5c) Why might these operations change the size of underlying IP packets associated with the control connection? How could the NAT handle the change in packet sizes?

The IP address and port numbers used by the NAT box may have a different number of decimal digits, when represented as the arguments in the PORT command. As such, the NAT box must change the packet sizes, as well as the TCP sequence numbers (when sending to the server) and acknowledgment numbers (when directing return packets to the client) to remain consistent. If the packet size increases, the new packet may exceed the MTU, requiring the NAT box to fragment the IP packets.

(5d) What challenges are introduced if other applications (besides FTP control) use port 21? What challenges are introduced if the FTP client and FTP server encrypt their communications?

If another application uses port 21, the NAT may mistakenly think the connection is an FTP control connection and try to parse the messages. If the other application also sends the string PORT, the NAT box may mistakenly modify the packet contents, leading to unpredictable affects.

If the FTP client and server encrypt their communications, the NAT box cannot parse the PORT command (in the payload of TCP connection) and correctly map the IP address and port number. This can lead to significant confusion for users, when their FTP client works fine in the absence of encryption and then mysteriously does not work when encryption is enabled.

(5e) FTP has an alternate way to establish the data-transfer connection, called passive mode, where the server selects a port number and instructs the client (using the existing control connection) to establish the data-transfer connection. Why is passive mode easier than active mode in the presence of client-side NAT boxes?

In passive mode, the server selects an address and port number, and sends them to the client over the control connection. The client-side NAT does not need to modify the address and port number used by the remote server. (That said, passive mode is challenging in the presence of a server-side NAT box, though this is a much less common configuration.)

If you are curious to learn more about the interaction of FTP and NAT, see http://en.wikipedia.org/wiki/File_Transfer_Protocol#FTP_and_NAT_devices
```

### Question 6(e)
- pages: DOC
- overlap: DNS caching and DNS prefetching
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring08-cos461-exam1-answers.doc>

```text
QUESTION 6: A Rose by Any Other Name (15 points)

This question explores the challenges of the Domain Name System.

(6e) A local DNS server typically discards cached name-to-address mappings when the time-to-live expires. Alternatively, the local DNS server could optimistically issue a new query for the cached domain name. Given one advantage and one disadvantage of that approach.

By prefetching the name-to-address mapping, the local DNS server can hide the DNS look-up delay, improving the performance experienced by the end user. However, prefetching introduces extra DNS queries and network load to look up name-to-address mappings that may never be needed.
```

### Question 7(a), 7(b), 7(c), 7(d)
- pages: DOC
- overlap: traceroute TTL/ICMP behavior, route changes during measurement, TCP SYN/SYN-ACK RTT measurement, IP geolocation
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring08-cos461-exam1-answers.doc>

```text
QUESTION 7: For Good Measure (15 points)

(7a) Traceroute capitalizes on the Time To Live field in the IP packet header to measure the forwarding path from one host to another. Give two reasons why a hop in traceroute might show a * (i.e., no IP address for the router at that hop in the path).

The packet may have been lost on the forward path. The TIME_EXCEEDED packet may have been lost on the reverse path. The router may have been configured not to send TIME_EXCEEDED messages. The packet may have encountered a firewall or NAT that drops the packet.

(7b) Traceroute may report a path that does not exist. For example, traceroute could return a path A-B-C (where A, B, and C are IP addresses) when there is no link between routers B and C. Give one example where that could happen. (Draw a picture if useful.)

The route to the remote destination may have changed during the measurement process. For example, suppose the route from A to Z changed from A-B-Y-Z to A-D-C-Z. Then, the first traceroute probe would return B and the second would return C, even though nodes B and C are not directly connected.

Another possibility is that a middlebox (such as a transparent proxy or firewall) lies between B and C; these middleboxes do not typically decrement the TTL value or send TIME_EXCEEDED messages.

(7c) The delay between a TCP sender transmitting a SYN packet and receiving the SYN-ACK packet provides an estimate of the round-trip time between a client and a server. Give one reason why, on average, the SYN/SYN-ACK delay is larger than a typical round-trip delay between a client and server. Assume all DNS and ARP look-ups have already completed.

The server may have a listen queue that stores pending requests to establish a TCP connection. As such, the SYN packet may sit in the queue for some time before the SYN-ACK is sent.

(7d) Determining the geographic location of an Internet host, based on its IP address, is challenging. Propose two techniques that could be used to infer the rough location.

The DNS name, found by performing an address-to-name look-up, may reveal the location, e.g., nslookup(12.122.16.158) returns tbr1.n54ny.ip.att.net, which is at 54th street in Manhattan.

The whois database may reveal the location, e.g., whois h whois.arin.net 128.112.12.58 returns an entry with 87 Prospect Avenue in Princeton, New Jersey.

Sending probes (such as ping) from a host can reveal the round-trip latency to the remote destination. Sending such probes from many vantage points can be used to triangulate the location of the remote host.

Sending a traceroute to the remote host would reveal the names of many of the routers along the path. The names of the routers near the destination would reveal the likely location of the host.
```

## Princeton COS 461 Computer Networks / Spring 2008 Final

### Question 1
- pages: DOC
- overlap: Link-state routing weights and shortest-path behavior
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring08-cos461-exam2-answers.doc>

```text
1 (10 points) 2 (10 points) 3 (15 points) 4 (10 points) 5 (15 points) 6 (15 points) 7 (20 points) 8 (5 points) Total
```

### Question 2
- pages: DOC
- overlap: BGP routing policy and RouteViews-style routing reasoning
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring08-cos461-exam2-answers.doc>

```text
QUESTION 2: Route Views (10 POINTS)

This question explores the role of routing policy on BGP routing. In the picture below, the nodes are Autonomous Systems (ASes). Dotted lines correspond to peer-peer relationships, and solid arrows correspond to provider-customer relationships, with the arrow pointing from provider to customer. Every node prefers customer-learned routes over routes through peer ASes, and peer-learned routes over routes through provider ASes. Among routes through the same kind of neighbor, each AS prefers shorter AS paths over longer ones. An AS does not export routes learned from one peer or provider to other peers or providers.

2a) Draw all of the paths to destination AS d. That is, draw the sink tree leading to d. Circle any ASes that do not have any route to d. (2 points)

SHAPE \* MERGEFORMAT

The paths are b-a-d, g-d, and h-e-d. Nodes c, f , and i cannot reach d.

2b) What path does e take to reach i? Suppose f decides to terminate the peering relationship with AS e. Can AS e still reach destination i? If so, what is the new path? (2 points)

Node e takes the path e-f-i. With the e-f link removed, the path is e-b-c-f-i. The path e-h-i is not used because es customer h would not advertise a peer-learned route to its provider.

2c) In the original picture from 2a, suppose ASes a and b provide a dump of all BGP routes they learn for every destination to a public measurement repository. Suppose a researcher extracts all links from all AS paths in those dumps and uses them to construct a view of the AS-level topology of the network. Draw a picture of the resulting inferred topology. (3 points)

The graph is missing the peering edges d-e, d-f, g-h, and h-i. Node a learns only customer-learned routes from its customer d and peer b, allowing it to learn a-d, a-d-g, a-b, a-b-e, and a-b-e-h. Node b learns only customer learned routes from its two peers a and b, and its customer c, allowing it to learn the routes that a learned, plus b-e and b-e-h from e, as well as b-c, b-c-f, and b-c-f-i from c.

2d) What is the minimum set of ASes that must provide dumps of every AS path they learn for every edge in the graph to be visible in at least one dump? List the ASes. (3 points)

Two nodes: b and h (or e and h). Node h has paths h-g (to g), h-i (to i), h-e (to e). It learns the paths h-e-d, h-e-f, h-e-b, h-e-b-a, and h-e-b-c from e. However, since e is using the path e-d to reach d and the path e-f to reach f, e does not announce the paths e-b-a-d or e-b-c-f, even though e does learn those paths. As such, the dump for node h reveals all edges except a-d and c-f, which are in a routing-table dump at either e or b.
```

## Princeton COS 461 Computer Networks / Spring 2007 Mid

### Question 1(a), 1(b), 1(c)
- pages: DOC
- overlap: bandwidth-delay product, TCP/IP header overhead, TCP receive-window limiting
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring07-cos461-exam1-answers.doc>

```text
QUESTION 1: Internet Versus Station Wagon (15 POINTS)

A famous maxim, sometimes attributed to Dennis Ritchie, says Never underestimate the bandwidth of a station wagon full of tapes. Suppose you need to deliver a large file between two computers that are 200 km apart and connected by a direct link. This question analyzes when it is faster to drive the data between the two locations, rather than transmit the data?

(1a) Suppose the station wagon drives 100 km/hour and the link has a bandwidth of 800,000 bits/second. And, suppose for simplicity that the data transfer can fully consume the link bandwidth, with no additional overhead (e.g., for headers or the TCP sawtooth). At what file size (in bytes) does the station-wagon solution start delivering the data faster? Show your work.

By car, travel time is 2 hours (i.e., 200 km * 1hr/100km). During two hours, the link could transfer 800,000 bits/sec * 60 sec/min * 60 min/hour * 2hr * 1byte/8bits for 720,000,000 bytes.

(1b) Suppose the sender transmits the data as packets with a 20-byte IP header, and 20-byte TCP header, and a maximum segment size of 512 bytes. How much more time (as a fraction) would the data transfer take on the link? (Ignore TCP congestion control and the link-layer header.)

An MSS of 512 bytes and two 20-byte headers leads to a packet size of 552 bytes. So, only 512/552 of the bandwidth is used to transmit the actual data, so the transfer takes 552/512 of the time, or 40/512 times longer. This reduces to a factor of 5/64 longer time.

(1c) Suppose that, like the path traversed by the car, the link is 200 km long. The speed of electricity in a copper cable is 200,000,000 meters/second. How big does the receive window need to be to avoid becoming the main constraint on the transfer rate? (Ignore the effects of header sizes, TCP congestion control, and packet loss, and assume that the receiver immediately sends an ACK packet after receiving each data packet and that there is no congestion.)

The receive window needs to be large enough to accommodate a round-trip time of data. The one-way delay is 1sec/200,000km * 200km, or 0.001 seconds (or 1 msec). So, the round-trip time is 0.002 seconds (or 2 msec). Since the link bandwidth is 800,000 bits/sec, the total number of bytes transmitted during a round-trip time is 0.002 sec * 800,000bits/sec * 1byte/8bits, or a grand total of 200 bytes.
```

### Question 2(a), 2(b), 2(c), 2(d), 2(e)
- pages: DOC
- overlap: stream sockets, TCP byte stream vs message boundaries, close behavior, SYN retransmission, UDP port binding
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring07-cos461-exam1-answers.doc>

```text
QUESTION 2: Sockets (15 POINTS)

(2a) Suppose application A is using a stream socket to transfer data to application B on a remote host. Suppose application A writes data into the socket buffer ten times. Why might the underlying TCP implementation transmit more than ten data packets (not including retransmissions of lost packets, or control packets like SYN, ACK, or FIN)?

If the application writes more than an MSS of data, a single write() call may lead to multiple TCP segments and, hence, multiple packet transmissions.

(2b) Why might the TCP implementation transmit all of the data in fewer than ten data packets?

If the application writes less than an MSS of data, the data from multiple write() calls may be combined into a single TCP segment and, hence, a single packet transmission. This is especially true in applications like Telnet, when Nagles algorithm is used.

(2c) Why can application A safely perform a close() on the socket when it is done writing the data, even if application B has not yet received all of the data?

The TCP implementation (typically in the operating system) buffers the data and continues to (re)transmit the data to the receiver as needed.

(2d) List two possible explanations for why host A would need to retransmit the SYN packet as part of establishing the TCP connection with B.

The SYN packet may have been lost in the network, discarded by the receiver due to a checksum error, or discarded because the receivers listen queue is full. Or, the SYN-ACK packet may have been lost. Or, the RTO might have been too small (e.g., for a very long-haul link to Mars).

(2e) Since a datagram socket (i.e., a UDP socket) does not require establishing a connection, why is a port number necessary?

For demultiplexing the packet to the correct receiving socket.
```

### Question 3(a), 3(b), 3(c), 3(d), 3(e)
- pages: DOC
- overlap: NAT, ARP/MAC, network-layer protocol demultiplexing, UDP/TCP demultiplexing, socket demultiplexing
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring07-cos461-exam1-answers.doc>

```text
QUESTION 3: Demultiplexing (10 points)

(3a) Suppose an organization runs a Network Address Translator. When a packet arrives from the external Internet, what field(s) determine which internal IP address to use as the destination address for the packet? What other fields in the IP and TCP/UDP header does the NAT change?

When a packet arrives from the external Internet, the NAT box inspects the destination port number (and address, if the NAT has multiple external-facing IP addresses) to identify the receiving host. The NAT changes the destination address and port, as well as the checksum.

(3b) Suppose the NAT then places the IP packet in an Ethernet frame to send to the receiving host. How does the NAT know what destination MAC address to use?

The NAT box checks in its ARP table for the MAC address corresponding to the internal destination address. If no match is found in the ARP table, the NAT box issues an ARP query to learn the associated MAC address.

(3c) Once the Ethernet frame reaches the destination host, how does the host know what network-layer protocol (e.g., IP, IPX, Appletalk) should be used to parse the payload?

The Ethernet frame has a type field that identifies the network-layer protocol.

(3d) How does the operating system know if the packet is a UDP packet or a TCP packet?

The IP header has a protocol field that identifies the transport-layer protocol.

(3e) How does the operating system know which process (and which socket) should receive the packet?

The protocol field (in the IP header) and the destination port (in the transport-layer header) identify the receiving socket.
```

### Question 4(a), 4(c), 4(d), 4(e)
- pages: DOC
- overlap: source-IP spoofing, TCP congestion-response incentives, parallel HTTP/TCP connections, ARP-cache poisoning
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring07-cos461-exam1-answers.doc>

```text
QUESTION 4: Cheaters Sometimes Win (15 points)

Many of the protocols underlying the Internet rely on end hosts to faithfully implement the protocols correctly, for the greater good. This question explores what happens when they dont.

(4a) List one motivation for a host to send an IP packet with the wrong source IP address. List two ways that this can adversely affect the legitimate owner of that IP address.

A host launching a denial-of-service attack may send packets with a spoofed source address that corresponds to another host, in order to evade detection. The legitimate owner may be blamed for the attack (and perhaps also blocked from sending legitimate traffic to the victim destination), and may also receive unwanted return traffic (e.g., SYN-ACK or RST packets).

(4c) Consider a TCP implementation that does not reduce its sending rate in response to packet loss. Describe how this would affect the other TCP traffic sharing the congested link. Also, explain whether/how this non-compliant behavior might hurt the performance of the offending TCP connection.

By not reducing the sending rate in response to packet loss, the rogue TCP sender would not do its part to reduce congestion, forcing other packets to be dropped. Eventually, well-behaved TCP senders would reduce their sending rates and share whatever bandwidth the rogue sender is not using. This would lead to unfairness. It may also hurt the rogue TCP sender because driving the link beyond its capacity may cause loss of the rogue senders packets, requiring retransmisisons.

(4d) Many Web browsers open several TCP connections in parallel when downloading multiple embedded images. How does this affect the other TCP traffic sharing the same congested link? When no other traffic traverses the links, is using multiple parallel connections still beneficial to the user? Why or why not?

The extra TCP connections allow the Web browser to have an unfair share of the bandwidth of the bottleneck link, reducing the throughput of other, well-behaved applications. When no other traffic traverses the link, the multiple connections share bandwidth only with each other. Still, this may be beneficial if the connections are RTT-limited, and because the user likes to see multiple embedded images fill in at the same time; also, the parallel connections collectively get more bandwidth during slow start.

(4e) Some implementations of ARP process an ARP reply (by updating the local ARP cache) even when there are no ARP requests pending. Suppose a rogue computer sends an unsolicited ARP reply message, with its own MAC address and the IP address of the LAN gateway router, to another host on the LAN. What will happen when this host (i.e., the host who believed the bogus ARP reply) transmits an IP packet destined to an external Internet address?

The host would send the packet in an Ethernet frame destined to the MAC address of the rogue machine, which may discard the traffic, or may inspect the contents before directing the packet to the legitimate gateway.
```

### Question 5(a), 5(b), 5(c), 5(d)
- pages: DOC
- overlap: DHCP client/server behavior, gateway configuration, ARP plus NAT, public vs private IP address discovery
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring07-cos461-exam1-answers.doc>

```text
QUESTION 5: Home-Network Box (15 points)

Consider a home network with multiple hosts plugged in (via Ethernet cables) to a Box that has a link directly to a residential broadband provider (e.g., via a DSL line). Suppose the broadband provider assigns a single public address to each home. This question explores the many functions that the Box implements.

(5a) The Box may, at different times, act as both a DHCP client and a DHCP server. Why would it act as a client? Why would it act as a server?

The Box acts as a DHCP client to the DSL providers DHCP server, to get a public IP address. The Box acts as a DHCP server to allocate private IP addresses to the internal hosts.

(5b) The Box serves as a gateway router for the hosts in the home network. How do the hosts in the home network learn the IP address of the gateway? Is this the same address as the single public address the provider allocated to the home? Why or why not?

The hosts in the home network learn the internal-facing address of the gateway via DHCP. This is not the same as the external-facing address assigned by the ISP. Typically, the ISP assigns an address from its own (public) address block, whereas the internal-facing address lies in the (private) address block used to number devices in the home network.

(5c) Suppose a host in the home network sends a TCP SYN packet to a Web server in the external Internet. Explain the role of ARP and NAT in getting the first IP packet from the host through the home network and out the connection to the Internet.

The host recognizes that the destination IP address of the packet falls outside of the local subnet and, as such, directs the IP packet to the gateway router (i.e., the Box). The host uses ARP to determine the MAC address of the gateway, by consulting its ARP cache or, on a cache miss, issuing an ARP query). Then, the host sends the Ethernet frame to the gateway (i.e., the Box). The Box then maps the source address and source port, using a NAT table, before directing the traffic to the Internet. (The Box may also use ARP to learn the MAC address of the DSL providers gateway router.)

(5d) Some Web sites on the Internet allow a home user to determine the public IP address the broadband provider has assigned to the home. Why might it be hard for the end user to determine the IP address directly? How does the external Web site know?

The end host learns the private (internally-facing) address of the NAT box, not the public (externally-facing) address. In contrast, the Web server receives the HTTP request on a TCP connection from the public address of the NAT box and, as such, knows the public address.
```

### Question 6(a), 6(b), 6(c), 6(d), 6(e)
- pages: DOC
- overlap: soft state, HTTP vs IP header format, packet-size/fragmentation issues, CIDR, TCP retransmission timeout
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring07-cos461-exam1-answers.doc>

```text
QUESTION 6: Internet Principles (15 POINTS)

(6a) List one advantage and one disadvantage of using soft state over hard state. Give two examples of the use of soft state from the protocols covered in class.

Soft state is robust to a device that fails ungracefully and does not relinquish its state. However, soft state wastes resources in repeatedly refreshing state. Examples of soft state include the TTL in DNS caching, the lease time in DHCP, and the caching time for ARP entries and NAT bindings.

(6b) List one advantage and one disadvantage of using a text-based header (as in HTTP) instead of a binary format. Why does IP use a binary format?

A text-based header is easier for human beings to read and debug. Text-based headers are also extensible. However, they are verbose (i.e., waste bandwidth) and harder to parse. IP uses a binary format to limit the bandwidth consumed by the header, and to simplify parsing at the router, which much process packets very quickly (e.g., within a few nanoseconds on high-speed links).

(6c) IP allows variable-sized packets. List one advantage and one disadvantage of forcing all packets to be the same size.

Fixed-sized packets do not need extra header space for a packet-length field, and they are easier to managed (e.g., fixed-sized buffers). However, fixed-sized packets waste bandwidth due to padding when the data is smaller than the packet size.

(6d) List one advantage and one disadvantage of classless interdomain routing (CIDR) over the earlier use of classful routing.

CIDR allows more efficient allocation of the limited address space, by permitting a wide variety of sizes of address blocks. However, CIDR requires routers to perform longest-prefix-match forwarding, which is hard to do quickly.

(6e) List one disadvantage of having a TCP retransmission timeout (RTO) that is too large. List one disadvantage of having an RTO this is too small.

If the RTO is too large, the sender waits too long to retransmit a lost packet, leading to slower data transfers. If the RTO is too short, the sender unnecessarily retransmits packets that were not actually lost, wasting network bandwidth.
```

### Question 7(a), 7(b), 7(c), 7(d), 7(e)
- pages: DOC
- overlap: TCP AIMD, loss detection/adaptation, DNS hierarchy, hierarchical IP allocation, MAC/link-local addressing
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring07-cos461-exam1-answers.doc>

```text
QUESTION 7: Decentralized Control (15 points)

(7a) Why does a TCP sender decrease its sending rate (on a packet loss) more aggressively than it increases the sending rate (after successful packet delivery)?

Overshooting the capacity of the path has dire consequences in terms of congestion collapse, whereas undershooting just makes the network a little less efficient than it otherwise would be. The multiplicative decrease algorithm of TCP is crucial to its stability.

(7b) The way a TCP sender reacts to packet loss depends on how the loss was detected. What are the two scenarios? How does the TCP sender adapt its rate in each case? Why are these two cases handled differently?

When loss is detected by a timeout, the sender decreases the sending rate to 1 MSS and repeats slow start, assuming that network congestion is quite serious. When loss is detected by a triple-duplicate ACK, the sender halves the sending rate, assuming that the congestion is not too bad.

(7c) Give two reasons why a local DNS server is not configured with the IP addresses of the top-level domain servers (e.g., for .com or .org). How does the local DNS server learn the addresses of the top-level domain servers?

The top-level domain servers may change over time, and new top-level domains (such as the country codes in recent years) may be added. The local DNS server is configured only with the addresses of the 13 root servers, and contacts one of these servers to learn the address of the TLD server of interest.

(7d) List two reasons for the hierarchical allocation of IP address blocks in the Internet, from one institution to another.

Hierarchical allocation reduces administrative overhead by allowing regional Internet registries to allocate large blocks to ISPs who, in turn, allocate smaller blocks to their customers. Hierarchical allocation also improves the efficiency of the routing system since, often, these smaller address blocks do not need to be known globally, since the customers are reachable via their providers that own and announce the containing (larger) address block.

(7e) MAC addresses only have significance within the context of a local-area network. So, why are MAC addresses globally unique?

If two devices had the same MAC address, they might sometime reside on the same LAN, leading to mass confusion. (More specifically, the self-learning switches might go back and forth in determining which way to forward frames, so sometimes one device would receive the frames and sometimes the other. Bad scene all around, and very hard to debug.)
```

## Princeton COS 461 Computer Networks / Spring 2007 Final

### Question 1(a), 1(b), 1(c), 1(d), 1(e), 1(f)
- pages: DOC
- overlap: P2P distribution scalability, client/server vs peer-assisted transfer, BitTorrent incentives, incomplete downloads, rare-file availability
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring07-cos461-exam2-answers.doc>

```text
QUESTION 1: Scalability of Peer-to-Peer Systems (15 POINTS)

The first three parts of this question explore the scalability of peer-to-peer systems, compared to client-server systems. For this question, we assume that the interior of the network has ample bandwidth, and that propagation delay is infinitesimal. The server has a 100 kbyte file that it wants to distribute to a group of 31 receivers. All hosts have bidirectional 40 kilobit/second links to the Internet that is, they can upload and download 40 kilobits/second and the core of the Internet is not congested.

(1a) What is the minimum time for the server to transmit the data to all of the receivers in a client-server configuration (i.e., where the receivers do not upload any content)? (3 points)

The server must transmit the 100 kbyte (800 kbit) file to 31 receivers at a rate of 40 kbits/sec. The total time is (31*100*8)/40, or a total of 620 seconds.

(1b) Now, suppose that the receivers can upload data, too, but only after receiving an entire copy of the 100 kbyte file. What is the minimum time for the server and the cooperating peers to transmit the data to all receivers in this configuration? (3 points)

The number of receivers with a copy of the file doubles after each full 100 kbyte transmission. Each round takes (100*8)/40 = 20 seconds. The number of rounds is log232 = 5. (That is, 1 receiver completes in the first round, 2 in the second, 4 in the third, 8 in the fourth, and 16 in the fifth, for a total of 31 receivers.) Hence, the total time is 20 * 5, or 100 seconds.

(1c) Now, suppose that a receiver can start uploading data to others after receiving the first 20 kbyte chunk of data. How long does it take to deliver the data to all receivers? (3 points)

Similar to question 1(b), the first 20 kbytes require five rounds to complete, where each round requires (20 * 8)/40 = 4 seconds to complete. So, by the end of five rounds, 20 seconds (4 * 5) have elapsed, and every peer has the first 20 kbytes of data. The remainder of the data transfer is pipelined, where the last peers download the remaining 80 kbytes as quickly as they can. They need a time of (80 * 8)/40 = 16 seconds to download the rest, for a total of 20 + 16 = 36 seconds.

The remainder of this question focuses on BitTorrent.

(1d) Suppose there are many peers transferring chunks of the same large file some broadband users with very high bandwidth and some dial-up users with very low bandwidth. Why would the broadband peers exchange chunks mostly with each other, and similar the dial-up peers exchange mostly with each other? (2 points)

Peers exchange with other peers that upload to them at a high rate. Hence, broadband peers will exchange chunks with other broadband peers, leaving dial-up peers to exchange chunks with each other.

(1e) Why is BitTorrent vulnerable to incomplete downloads? What steps are taken to prevent it? (2 points)

After downloading the complete file, peers may leave the system rather than remaining to provide chunks to others.

The rarest chunk first policy increases the likelihood that each chunk is available from at least one active peer. The random chunk policy also helps by distributing the chunks across the peers.

(1f) BitTorrent is primarily useful for popular files. Suggest ways to extend BitTorrent to work better for less popular files. (2 points)

Currently, BitTorrent s incentive mechanisms apply to each file independently. Instead, BitTorrent could provide incentives for peers to store chunks for less popular files, even if these peers are not interested in these files. For example, the system could offer virtual currency that could be used to achieve faster downloads on the files these peers actually want.
```

### Question 2(a), 2(b), 2(e)
- pages: DOC
- overlap: link-state routing convergence, transient forwarding loops, BGP over TCP with directly connected peers
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring07-cos461-exam2-answers.doc>

```text
QUESTION 2: Routing Protocols (20 POINTS)

The first two questions concern a shortest-path, link-state routing protocol running on the following network, where the numbers correspond to link weights:

SHAPE \* MERGEFORMAT

(2a) Suppose the link between nodes k and m fails. Before the failure, what is the shortest path from node i to node j? What is the new path after the failure, when routing-protocol convergence completes? (2 points)

Before the failure: i-k-m-j (cost 6) After the failure: i-r-n-j (cost 8)

(2b) A transient forwarding-loop might occur during routing-protocol convergence. Involving what nodes? List two examples of what would happen to the data packets sent from i to j during this period. (3 points)

The nodes k and n may experience a forwarding loop, if k learns about the failure first and starts forwarding the packets along the path k-n-j, while n is still forwarding along the (old) path n-k-m-j.

Some packets will be discarded when their TTL expires. Others may eventually escape the loop, and experience high delay and arrive out of order. The remaining parts of the question focus on interdomain routing using BGP.

(2e) Suppose two directly-connected routers A and B have a BGP session between them, running over a TCP connection. BGP is used to propagate routing information, yet BGP relies on establishing a TCP connection before exchanging any update messages. TCP, in turn, relies on the routing system to deliver TCP segments. How is this apparently circularity resolved? How do the two TCP end-points know how to reach each other? (3 points)

Since the two routers are directly connected, they have interfaces on the same subnet (i.e., the two BGP speakers have IP addresses in the same subnet). As such, they know how to reach each other, perhaps requiring a simple ARP query to learn the associated MAC address.
```

### Question 3(a), 3(b), 3(c)
- pages: DOC
- overlap: multimedia streaming playout delay, TCP vs UDP for interactive media, TCP connections vs virtual circuits
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring07-cos461-exam2-answers.doc>

```text
QUESTION 3: Multimedia Streaming and Quality of Service (10 points)

(3a) Suppose a server transmits one frame of a video every second, and the client starts playing the video at one frame per second as soon as the first frame arrives. Suppose the first ten frames arrive at times 0, 1.2, 1.99, 4.17, 4.01, 5.03, 8.05, 7.50, 8.90, 8.99, all in seconds. Which frames reach the client too late for playout? How much extra playout delay is needed to ensure that all frames have arrived by the time the client needs to play them? (2 points)

Starting with frame 0 at time 0, frame i should play at time i. Hence, the frames arriving too late to play are frame 1 (1.2 instead of 1), 3 (4.17 instead of 3), 4 (4.01 instead of 4), 5 (5.03 instead of 5), 6 (8.05 instead of 6), 7 (7.50 instead of 7), and 8 (8.90 instead of 8). Only frames 2 (1.99 instead of 2) and 9 (8.99 instead of 9) arrive in time.

The worse offender is frame 6 that arrive 2.05 seconds early. A playout time of 2.05 seconds is enough to ensure that all frames arrive in time for playout.

(3b) List three reasons why TCP is ill-suited to transmitting interactive audio and video? Why is it often used anyway? (3 points)

TCP retransmits lost packets, even when the retransmitted packets would arrive too late to be useful. TCP has a large (20-byte) header that is wasteful in small audio packets. TCP sometimes drops its sending rate dramatically, which may cause the transmission to fall behind. When packet loss occurs, TCP does not deliver subsequent packets to the application, even though the data may be necessary for playout.

TCP is often used anyway because many firewalls block UDP packets.

(3c) What are the similarities between a TCP connection and a virtual circuit? What are the differences? (3 points)

Similarities: Both have a connection set-up and tear-down phase Data are delivered reliably and in-order

Differences: Virtual circuits tend to reserve bandwidth to offer performance guarantees, whereas routers/switches do not reserve resources for TCP connections. Routers/switches have state for forwarding packets on behalf of each virtual circuit, but not for TCP connections.
```

### Question 4(a)
- pages: DOC
- overlap: broadcast-generating protocols such as ARP and DHCP
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring07-cos461-exam2-answers.doc>

```text
QUESTION 4: Ethernet and Wireless (10 points)

(4a) Ethernet bridging relies heavily on flooding. For example, broadcast traffic is flooded. List two protocols that generate broadcast traffic, and explain why broadcasting is done. (2 points)

ARP: ARP requests are sent to learn the MAC address associated with a particular IP address. The machine sending the request has no idea where the destination machine is located and, as such, sends a broadcast packet to ensure the query reaches the machine with the target IP address. DHCP: As part of boot-strapping, a host sends a DHCP request in the hope that a DHCP server will respond to assign an IP address, subnet mask, gateway address, and DNS server address. The host has no idea what machines are serving as DHCP servers and, as such, sends a broadcast traffic to ensure one or more DHCP servers hear the request.
```

### Question 5(a), 5(b), 5(c), 5(d)
- pages: DOC
- overlap: overlay networks, RON-style routing, Napster, Gnutella
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring07-cos461-exam2-answers.doc>

```text
QUESTION 5: Overlay Networks (15 points)

(5a) Overlay routing can sometimes react more quickly to network events (such as equipment failures) than the underlying routing system. How is this possible? At what cost? (3 points)

The small number of nodes in an overlay can send active probes aggressively, allowing them to identify performance and reachability problems quickly. In contrast, the routers may be somewhat conservative in detecting failures, and routing-protocol convergence can be slow in a large topology. The cost is the overhead the active probes impose on the network.

(5b) In a Resilient Overlay Network (RON), an overlay node may direct traffic through a single intermediate node to circumvent a performance or reachability problem on the direct path to the destination node. That is, RON decided to limit paths to two overlay hops. Why does RON impose this restriction? What is one advantage and one disadvantage of this design decision? (4 points)

RON imposes this restriction because one extra hop is usually enough to circumvent the problem on the direct path, and limiting to one hop makes the protocol simpler. The advantage is protocol simplicity, and the disadvantage is the lost opportunity to find the very best path (which might, on rare occasion, involve two or more intermediate hops).

(5c) Routing overlays like Resilient Overlay Networks (RONs) can, by definition, be deployed without requiring the support of the underlying network. Yet, support from the underlying network could undoubtedly help RON run better. List two ideas for changes to the underlay to support RON. (4 points)

Active probing wastes network resources. Instead, the routers could explicitly notify the overlay nodes about changes in network conditions.

Forwarding packets through intermediate hosts wastes bandwidth going in and out of the intermediate hosts network, and the processing of the packets on the intermediate host can add unnecessary latency. Instead, the routers could support packet deflections that forward packets through intermediate points inside the network, without traveling in and out of the intermediate host.

(5d) Napsters central directory and Gnutellas query flooding represent two extremes in how to support queries for content in peer-to-peer file-sharing systems. List two advantages and two disadvantages of the Napster approach over the Gnutella approach. (4 points)

Advantages: A central directory leads to a simpler protocol, and reduces the overhead for processing queries (since queries go directly to the central server rather than hopping multiple times through an overlay, as in Gnutella).

Disadvantages: The central directory is a single point of failure or attack. Also, the central directory does not scale. In addition, the central directory was a point of legal vulnerability for Napster.
```

### Question 6(a), 6(b), 6(c), 6(d)
- pages: DOC
- overlap: application-layer protocol design, HTTP/TCP delivery, proxies, CDNs
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring07-cos461-exam2-answers.doc>

```text
QUESTION 6: Application-Layer Protocols (10 POINTS)

(6a) The Simple Mail Transfer Protocol (SMTP) is very chatty. That is, sending an e-mail message requires numerous short, back-and-forth messages between the user agent and the e-mail server. Explain why this is a problem for sending e-mail from a wireless mobile device. What could be done to solve this problem without changing all of the e-mail servers? (3 points)

The wireless mobile device may not remain connected long enough to complete many round-trip times to the mail server. Sending all of the information in one shot would be more likely to succeed. This would be possible with an intermediate server that allows the mobile to use a less chatty protocol, while having this intermediate server speak SMTP to the e-mail server for backwards compatibility.

(6b) Why is it useful to have official standards (i.e., RFCs) for application-layer protocols? What are the advantages of forgoing the standardization process? How is it possible to forego the standardization process and still have a wide deployment of a new application? (2 points)

Official standards allow for interoperability between software written by different parties. However, standardization takes time, and makes established players vulnerable to new entrants who can build software that interoperates. An application-developer can forego the standardization process by making all of the necessary software available (e.g., peer software, or both the client and server software) for purchase, or free of charge.

(6c) YouTube converts uploaded videos to Flash and makes them available for downloading via HTTP. How has (i) using Flash format, (ii) using HTTP, and (iii) using TCP helped make YouTube so successful? (3 points)

Flash is widely available and installed on end-host machines, obviating the need for YouTube users to install a new plug-in. HTTP clients are widely available and used in Web browsers. TCP runs under HTTP and also allows YouTube to work well through firewalls and NATs.

(6d) Web proxy caches and content distribution networks (CDNs) both reduce the time for a client to download Web pages by moving content closer to the users. Give two reasons why CDNs have been more widely deployed (and successful) than Web proxy caching. (2 points)

The content providers can contract with CDNs to deliver their content, which improves performance, reduces cost, and makes their site robust to unexpected surges in demand. In contrast, the content provider cannot require millions of sites throughout the world to deploy proxy servers.

Also, proxies cannot cache all content. Some content is uncacheable because it is dynamically generated. CDNs can run the server software that generates the dynamic content.
```

### Question 7(a), 7(b), 7(c), 7(d)
- pages: DOC
- overlap: TCP over wireless, page-load performance, transport-header inspection by middleboxes, DNS/BGP layer placement
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring07-cos461-exam2-answers.doc>

```text
QUESTION 7: Layering (10 points)

(7a) Why does TCP perform badly on wireless links? What can be done to improve performance without requiring all wired hosts to upgrade to a new protocol? (2 points)

In contrast to wired networks, packet loss in wireless networks is not necessarily a sign of congestion; rather, inference and fading may be the cause. Yet, TCP treats packet loss as an implicit sign of congestion and decreases the sending rate. The performance could be improved by employing a TCP proxy at the wireless/wired boundary.

(7b) Within 30 minutes of the 9/11 attacks, the www.cnn.com Web site experienced a ten-fold increase in page views. CNN changed the main page of the web site to text, taking great care to reduce the size to around 1000 characters. Why this size? (2 points)

The 1000 bytes would (coupled with the HTTP response header) fit in a single 1500-byte IP packet, reducing the load on the servers and CNNs connection to the Internet. This allowed them to satisfy more page-view requests per unit time during the period of heavy load.

(7c) IP routers operate at the network layer, yet sometimes they do inspect the transport-layer header (such as the TCP/UDP port numbers). Give two reasons why this might be done. (2 points)

Routers sometimes filter packets (or place them in different queues) based on the port numbers. Also, routers may perform NAT functions requiring them to inspect and remap the port numbers. The routers might also perform measurement functions that log the port numbers or collect per-flow statistics based on the port numbers. Routers could conceivably punish flows that are not TCP friendly (i.e., that deviate from the AIMD congestion control rules), and this would require maintaining per-flow state and inspecting the port numbers of packets.

(7d) What protocol layer (application, transport, or network) does BGP operate at? What about DNS? (2 points)

BGP and DNS are application-layer protocols. BGP runs on top of TCP, and DNS runs on top of either TCP or UDP.
```

### Question 8(3a), 8(3b), 8(3c)
- pages: DOC
- overlap: source routing vs distributed routing and path control
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring07-cos461-exam2-answers.doc>

```text
QUESTION 8: Source Routing (10 POINTS)

In source routing, the end host or edge router computes the path through the network, and the packet carries the list of hops along the path. The routers, in turn, forward the packet as instructed. This question explores the advantages and disadvantages of source routing.

(3a) List three advantages of source routing, relative to todays intradomain and interdomain routing protocols. (3 points)

The sender could exploit knowledge of the performance or reliability of the links. The sender could pick a path that matches the application requirements (e.g., low delay vs. high throughput) The sender could pick paths that avoid untrusted links or ASes. The sender could react quickly to changes in network conditions (e.g., failure) by rerouting to a new path.

(3b) List three disadvantages of source routing, relative to todays routing system. (3 points)

The sender would need to perform extra work. The packet could not easily adapt its route in mid stream. The packets would be larger, because of needing to carry the path information. The sender would need to learn the connectivity information for the Internet, which might not be scalable. ISPs would lose control over how traffic flows through their networks. Denial-of-service attacks would be easier to launch.

(3c) Source routing is implemented in todays IP routers, but network operators almost always disable the feature. List three reasons why network operators disable source routing. (4 points)

Otherwise, they would lose control over the flow of traffic, leading to congestion and lost revenue (when customers pick paths that contradict the ISPs business incentives). The ISP would be much more vulnerable to denial-of-service attacks. Source routing requires extra processing on the routers, leading to extra overhead.
```

## Princeton COS 461 Computer Networks / Spring 2006 Mid

### Question 1
- pages: DOC
- overlap: transmission overhead, packetization, TCP/IP headers, ACK traffic
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring06-cos461-exam1-answers.doc>

```text
QUESTION 1: Transmission Overhead (15 POINTS)

SHAPE \* MERGEFORMAT

Suppose A has a TCP connection with B, where A sends data packets and B sends ACKs; similarly, suppose D has a TCP connection with C, where D sends data packets and C sends ACKs. Suppose the Maximum Segment Size (MSS) is 472 bytes, and all packets sent by A and D have this size; suppose also that B and C send an ACK in response to each data packet. Suppose that all packets have TCP and IP headers, as well as a 20-byte link-layer header/trailer. Assume the combined data and ACK packets fully utilize the middle link in both directions and no congestion control is applied.

(1a) What fraction of the bandwidth is consumed by data traffic (i.e., the TCP segments, rather than the transport, network, and link-layer information)? Feel free to express your answer as a reduced fraction (e.g., ½ or ¾) rather than a decimal number. Show your work.

Each TCP packet has three headers (at the link, network, and transport layers) and an optional segment. The link-layer header is 20 bytes, a TCP header is 20 bytes, and an IP header is 20 bytes, leading to 60 bytes of header. An ACK packet contains no payload (i.e., no segment) and, as such, is 60-bytes long. A full-sized TCP data packet includes MSS bytes (472 bytes in part a of the problem), in addition to the 60-byte header, resulting in 532-byte data packets. So, sending one TCP segment of 472 bytes incurs 532 bytes for the data packet and 60 bytes for the corresponding ACK packet. This leads to a ratio of 472/592, which simplifies to 59/74  about 79.7% of the link bandwidth.

(1b) What if the MSS were increased to 1460 bytes? What is the new fraction?

As before, the equation is MSS/(MSS + 60 + 60), but now with an MSS of 1460. The resulting fraction is 1460/1580, which reduces to 73/79  about 92.4% of the link bandwidth. Big savings!

(1c) What if the MSS were increased to 1460 bytes, and the receivers apply the delayed-ACK mechanism to send an ACK for every other data packet? What is the new fraction?

Now only half of the data packets incur the overhead of an ACK. Sending two data packets transfers 2*MSS bytes of data, leading to 2*(MSS+60) bytes in the data packets and one 60-byte ACK packet. The resulting fraction is 2*1460/(2*1460+120+60), which is 2920/3100, which reduces to 146/155  about 94.2% of the link bandwidth.
```
- source: <https://www.cs.princeton.edu/courses/archive/spr06/cos461/exams/midterm-answers.doc>

```text
QUESTION 1: Transmission Overhead (15 POINTS)

SHAPE \* MERGEFORMAT

Suppose A has a TCP connection with B, where A sends data packets and B sends ACKs; similarly, suppose D has a TCP connection with C, where D sends data packets and C sends ACKs. Suppose the Maximum Segment Size (MSS) is 472 bytes, and all packets sent by A and D have this size; suppose also that B and C send an ACK in response to each data packet. Suppose that all packets have TCP and IP headers, as well as a 20-byte link-layer header/trailer. Assume the combined data and ACK packets fully utilize the middle link in both directions and no congestion control is applied.

(1a) What fraction of the bandwidth is consumed by data traffic (i.e., the TCP segments, rather than the transport, network, and link-layer information)? Feel free to express your answer as a reduced fraction (e.g., ½ or ¾) rather than a decimal number. Show your work.

Each TCP packet has three headers (at the link, network, and transport layers) and an optional segment. The link-layer header is 20 bytes, a TCP header is 20 bytes, and an IP header is 20 bytes, leading to 60 bytes of header. An ACK packet contains no payload (i.e., no segment) and, as such, is 60-bytes long. A full-sized TCP data packet includes MSS bytes (472 bytes in part a of the problem), in addition to the 60-byte header, resulting in 532-byte data packets. So, sending one TCP segment of 472 bytes incurs 532 bytes for the data packet and 60 bytes for the corresponding ACK packet. This leads to a ratio of 472/592, which simplifies to 59/74  about 79.7% of the link bandwidth.

(1b) What if the MSS were increased to 1460 bytes? What is the new fraction?

As before, the equation is MSS/(MSS + 60 + 60), but now with an MSS of 1460. The resulting fraction is 1460/1580, which reduces to 73/79  about 92.4% of the link bandwidth. Big savings!

(1c) What if the MSS were increased to 1460 bytes, and the receivers apply the delayed-ACK mechanism to send an ACK for every other data packet? What is the new fraction?

Now only half of the data packets incur the overhead of an ACK. Sending two data packets transfers 2*MSS bytes of data, leading to 2*(MSS+60) bytes in the data packets and one 60-byte ACK packet. The resulting fraction is 2*1460/(2*1460+120+60), which is 2920/3100, which reduces to 146/155  about 94.2% of the link bandwidth.
```

### Question 2
- pages: DOC
- overlap: socket programming and networked-application behavior
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring06-cos461-exam1-answers.doc>

```text
QUESTION 2: Sockets (15 POINTS)

Consider a Web server that generates and sends HTTP response messages to clients over sockets. The header of an HTTP response message consists of a collection of lines, each ending with a carriage return and line feed. For example,

HTTP/1.1 200 OK Server: Apache/1.2.7-dev Date: Tue, 07 Jul 1998 18:21:41 GMT Content-Type: text/html

Some early Web-server software generated the lines one at a time, and used a separate system call to write (or send) each line to the socket.

(2a) Why is this approach inefficient for the end host?

The server makes a separate system call for each line, leading to a high overhead for switching between the user-space process and the operating system. The smaller packets arriving at the client may also require the browser to perform many system calls to receive the full header, if the packets do not arrive close together in time.

(2b) Why is this approach inefficient for the network?

The resulting TCP segments are very small, in the same ballpark as the link-layer, IP, and TCP headers themselves. A large fraction of the network bandwidth is consumed by the headers. Also, the receiver must transmit ACK packets in response to receiving the data packets, leading to a large number of ACK packets.

(2c) Describe how a programmer implementing the Web server software could fix this problem.

The programmer could create a large user-space buffer (e.g., at least 1460 bytes long, if not longer) and create the response header there. Then, the programmer could make a single socket call to send the full header. The operating system will then generate large packets containing multiple lines of data and send these larger packets into the network.
```
- source: <https://www.cs.princeton.edu/courses/archive/spr06/cos461/exams/midterm-answers.doc>

```text
QUESTION 2: Sockets (15 POINTS)

Consider a Web server that generates and sends HTTP response messages to clients over sockets. The header of an HTTP response message consists of a collection of lines, each ending with a carriage return and line feed. For example,

HTTP/1.1 200 OK Server: Apache/1.2.7-dev Date: Tue, 07 Jul 1998 18:21:41 GMT Content-Type: text/html

Some early Web-server software generated the lines one at a time, and used a separate system call to write (or send) each line to the socket.

(2a) Why is this approach inefficient for the end host?

The server makes a separate system call for each line, leading to a high overhead for switching between the user-space process and the operating system. The smaller packets arriving at the client may also require the browser to perform many system calls to receive the full header, if the packets do not arrive close together in time.

(2b) Why is this approach inefficient for the network?

The resulting TCP segments are very small, in the same ballpark as the link-layer, IP, and TCP headers themselves. A large fraction of the network bandwidth is consumed by the headers. Also, the receiver must transmit ACK packets in response to receiving the data packets, leading to a large number of ACK packets.

(2c) Describe how a programmer implementing the Web server software could fix this problem.

The programmer could create a large user-space buffer (e.g., at least 1460 bytes long, if not longer) and create the response header there. Then, the programmer could make a single socket call to send the full header. The operating system will then generate large packets containing multiple lines of data and send these larger packets into the network.
```

## Princeton COS 461 Computer Networks / Spring 2006 Second Mid

### Question 1, undergraduate version
- pages: DOC
- overlap: router state, forwarding/routing behavior, QoS/resource-reservation reasoning
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring06-cos461-exam2-answers.doc>

```text
QUESTION 1, GRADUATE STUDENTS: Quality of Service (15 POINTS)

*** This question is only for the graduate students in the class  undergraduate students should skip this question and proceed to the next page. ***

(1a) Consider an ATM network with a leaky-bucket policer (also known as a token-bucket filter) that ensures a virtual circuit does not send more cells than expected. If the policer has a bucket depth of 10 cells and a token rate of 100 cells/second, how many cells can the virtual circuit transmit during a one-second period? In a ten-second period?

Burst of 10 cells plus the token rate. So, 110 for one second. And 1010 for ten seconds.

(1b) Suppose a link has a propagation delay of P seconds and transmits R cells per second. Suppose a cell arrives when the link has Q other cells awaiting transmission, and has just started transmitting the first cell. What delay does the new cell experience, as a function of P, R, and Q?

Propagation delay of P seconds With Q other packets in the queue, must wait for Q+1 transmissions at one every 1/R seconds.

So, the total delay is P + (Q+1)/R

(1c) Suppose a link has a first-in-first-out queue and carries traffic for two virtual circuits. The traffic on the first virtual circuit obeys a token-bucket filter with a bucket depth of 9 cells and a token rate of 100 cells/second, and can settle for best-effort service. The traffic on the second virtual circuit obeys a token-bucket filter with a bucket depth of one cell and a token rate of 100 cells/second, and cannot tolerate more than 100 msec of delay in delivering each cell. Suppose the propagation delay on the link is 60 msec. What is the smallest transmission rate R, in cells per second, that can satisfy the delay constraint, given that the link serves cells in first-in-first-out order?

If the link rate is less than the sum of the two token-bucket rates, then an arbitrarily long backlog can develop. Otherwise, the link can drain the queue as fast as cells arrive, except for a burst of cells that arrive at the same time. This burst size is limited by the sum of the two bucket depths, allowing a backlog of at most 10 (i.e., 9 + 1) cells.

If the one cell from the delay-sensitive virtual circuit arrives just after the other nine, it experiences delay P + 10/R, where P is 60 msec. For the total to be less than or equal to 100 msec, we must have 10/R less than or equal to 40 msec. Thus, R must be at least 250 cells/second.

(1d) Explain why a different kind of link scheduler would allow a smaller value of R to suffice.

Forcing both virtual circuits to share the same queue makes the delay-sensitive virtual subject vulnerable to bursty traffic from the other virtual circuit. Having separate queues, with strict priority or weighted fair scheduling, would limit the impact the burst virtual circuit would have on the performance experienced by the cells in the delay-sensitive virtual circuit. QUESTION 2: Intradomain Routing (15 POINTS) (2a) The picture below shows a network with 8 routers, where each link has an integer weight (e.g., the link between u and v has weight 2). Add arrowheads to the picture to illustrate the shortest-path tree rooted at u. For example, the edge from u to v would be marked with an arrow head where the line meets node v. Please draw neatly.

SHAPE

All but three nodes are reached along the clockwise path starting at node u, with costs of 2, 4, 5, and 7, respectively. The other three nodes, down and to the right of u, are reached with costs of 2, 3, and 6, respectively, through us downward neighbor. (2b) Suppose node u sends a large amount of traffic to node v, consuming most of the bandwidth on the (u,v) link. The traffic from u to w also traverses the (u,v) link. To alleviate congestion on the (u,v) edge, the network administrator plans to change the weight of the (v,w) edge to divert the traffic from u to w onto another path. What is the minimum weight the (v,w) edge would need to force all of the traffic from u to w to take a different path? What is the maximum weight the link could have while still ensuring the traffic from v to w goes directly over the (v,w) link?

The next shortest path from u to w goes down from node u and has a cost of 5 (= 2 + 1 + 2). To make the path (u,v,w) strictly longer, it needs to have a length of 6 (i.e., 2 + 4). So, the answer is 4.

If the cost of edge (v,w) is too large, even traffic from v to w would choose a different path. The next shortest path from v to w goes through u and has a cost of 7 (= 2 + 2 + 1 + 2). So, the cost of the (v,w) edge should not exceed 6.

(2c) Why would a network administrator change the link weight, rather than simply relying on the end hosts (connected to node u) to adapt their sending rates in the presence of congestion?

Although TCP senders slow down in the presence of congestion, this does not ensure that network resources are used efficiently. Two TCP senders might each send at half the rate of a shared link while another path lies idle. By changing the link weights, the network operators can change the paths the traffic traverses  something TCP cannot do  allowing the TCP senders to transmit at higher rates and offer better performance to users. QUESTION 3: Interdomain Routing (15 POINTS)

(3a) How does the Border Gateway Protocol (BGP) avoid the count-to-infinity problem that plagues distance-vector protocols?

BGF is a path-vector protocol. That is, BGP announcements include the entire path traversed by the message, not simply a total cost. A router, upon receiving a BGP announcement, can check for its own AS number in the path; if the AS number is present, the path has a loop and is immediately discarded.

(3b) A tier-1 Internet Service Provider (ISP) is an Autonomous System (AS) that offers transit service to its customers but has no upstream providers of its own. The small collection of tier-1 ISPs (e.g., UUNET, Sprint, AT&T, and Level3) all connect directly to each other, with peer-peer relationships. Why does a tier-1 ISP need a peer-peer relationship with every other tier-1 ISPs?

Having no upstream providers of its own, a tier-1 ISP must rely on its peers and customers to reach remote destinations. However, the ISP can only reach its own customers (and its customers customers, recursively) through the connections to customers. A tier-1 ISP must peer with another tier-1 ISP so they can reach each others respective customers. The peering is full mesh because a peer does not provide transit service, meaning that two ISPs cannot communicate through a mutual peer.

(3c) Give two examples of filtering policies applied to BGP sessions, one for an import policy (filtering routes sent by a neighbor) and another for an export policy (filtering routes sent to a neighbor).

- Import filtering: discarding prefixes that a customer advertises but does not own - Export filtering: not announcing peer-learned routes to another peer
```
- source: <https://www.cs.princeton.edu/courses/archive/spr06/cos461/exams/midterm2-answers.doc>

```text
QUESTION 1, GRADUATE STUDENTS: Quality of Service (15 POINTS)

*** This question is only for the graduate students in the class  undergraduate students should skip this question and proceed to the next page. ***

(1a) Consider an ATM network with a leaky-bucket policer (also known as a token-bucket filter) that ensures a virtual circuit does not send more cells than expected. If the policer has a bucket depth of 10 cells and a token rate of 100 cells/second, how many cells can the virtual circuit transmit during a one-second period? In a ten-second period?

Burst of 10 cells plus the token rate. So, 110 for one second. And 1010 for ten seconds.

(1b) Suppose a link has a propagation delay of P seconds and transmits R cells per second. Suppose a cell arrives when the link has Q other cells awaiting transmission, and has just started transmitting the first cell. What delay does the new cell experience, as a function of P, R, and Q?

Propagation delay of P seconds With Q other packets in the queue, must wait for Q+1 transmissions at one every 1/R seconds.

So, the total delay is P + (Q+1)/R

(1c) Suppose a link has a first-in-first-out queue and carries traffic for two virtual circuits. The traffic on the first virtual circuit obeys a token-bucket filter with a bucket depth of 9 cells and a token rate of 100 cells/second, and can settle for best-effort service. The traffic on the second virtual circuit obeys a token-bucket filter with a bucket depth of one cell and a token rate of 100 cells/second, and cannot tolerate more than 100 msec of delay in delivering each cell. Suppose the propagation delay on the link is 60 msec. What is the smallest transmission rate R, in cells per second, that can satisfy the delay constraint, given that the link serves cells in first-in-first-out order?

If the link rate is less than the sum of the two token-bucket rates, then an arbitrarily long backlog can develop. Otherwise, the link can drain the queue as fast as cells arrive, except for a burst of cells that arrive at the same time. This burst size is limited by the sum of the two bucket depths, allowing a backlog of at most 10 (i.e., 9 + 1) cells.

If the one cell from the delay-sensitive virtual circuit arrives just after the other nine, it experiences delay P + 10/R, where P is 60 msec. For the total to be less than or equal to 100 msec, we must have 10/R less than or equal to 40 msec. Thus, R must be at least 250 cells/second.

(1d) Explain why a different kind of link scheduler would allow a smaller value of R to suffice.

Forcing both virtual circuits to share the same queue makes the delay-sensitive virtual subject vulnerable to bursty traffic from the other virtual circuit. Having separate queues, with strict priority or weighted fair scheduling, would limit the impact the burst virtual circuit would have on the performance experienced by the cells in the delay-sensitive virtual circuit. QUESTION 2: Intradomain Routing (15 POINTS) (2a) The picture below shows a network with 8 routers, where each link has an integer weight (e.g., the link between u and v has weight 2). Add arrowheads to the picture to illustrate the shortest-path tree rooted at u. For example, the edge from u to v would be marked with an arrow head where the line meets node v. Please draw neatly.

SHAPE

All but three nodes are reached along the clockwise path starting at node u, with costs of 2, 4, 5, and 7, respectively. The other three nodes, down and to the right of u, are reached with costs of 2, 3, and 6, respectively, through us downward neighbor. (2b) Suppose node u sends a large amount of traffic to node v, consuming most of the bandwidth on the (u,v) link. The traffic from u to w also traverses the (u,v) link. To alleviate congestion on the (u,v) edge, the network administrator plans to change the weight of the (v,w) edge to divert the traffic from u to w onto another path. What is the minimum weight the (v,w) edge would need to force all of the traffic from u to w to take a different path? What is the maximum weight the link could have while still ensuring the traffic from v to w goes directly over the (v,w) link?

The next shortest path from u to w goes down from node u and has a cost of 5 (= 2 + 1 + 2). To make the path (u,v,w) strictly longer, it needs to have a length of 6 (i.e., 2 + 4). So, the answer is 4.

If the cost of edge (v,w) is too large, even traffic from v to w would choose a different path. The next shortest path from v to w goes through u and has a cost of 7 (= 2 + 2 + 1 + 2). So, the cost of the (v,w) edge should not exceed 6.

(2c) Why would a network administrator change the link weight, rather than simply relying on the end hosts (connected to node u) to adapt their sending rates in the presence of congestion?

Although TCP senders slow down in the presence of congestion, this does not ensure that network resources are used efficiently. Two TCP senders might each send at half the rate of a shared link while another path lies idle. By changing the link weights, the network operators can change the paths the traffic traverses  something TCP cannot do  allowing the TCP senders to transmit at higher rates and offer better performance to users. QUESTION 3: Interdomain Routing (15 POINTS)

(3a) How does the Border Gateway Protocol (BGP) avoid the count-to-infinity problem that plagues distance-vector protocols?

BGF is a path-vector protocol. That is, BGP announcements include the entire path traversed by the message, not simply a total cost. A router, upon receiving a BGP announcement, can check for its own AS number in the path; if the AS number is present, the path has a loop and is immediately discarded.

(3b) A tier-1 Internet Service Provider (ISP) is an Autonomous System (AS) that offers transit service to its customers but has no upstream providers of its own. The small collection of tier-1 ISPs (e.g., UUNET, Sprint, AT&T, and Level3) all connect directly to each other, with peer-peer relationships. Why does a tier-1 ISP need a peer-peer relationship with every other tier-1 ISPs?

Having no upstream providers of its own, a tier-1 ISP must rely on its peers and customers to reach remote destinations. However, the ISP can only reach its own customers (and its customers customers, recursively) through the connections to customers. A tier-1 ISP must peer with another tier-1 ISP so they can reach each others respective customers. The peering is full mesh because a peer does not provide transit service, meaning that two ISPs cannot communicate through a mutual peer.

(3c) Give two examples of filtering policies applied to BGP sessions, one for an import policy (filtering routes sent by a neighbor) and another for an export policy (filtering routes sent to a neighbor).

- Import filtering: discarding prefixes that a customer advertises but does not own - Export filtering: not announcing peer-learned routes to another peer
```

### Question 1, graduate version
- pages: DOC
- overlap: router state, forwarding/routing behavior, QoS/resource-reservation reasoning
- source: <https://www.cs.princeton.edu/courses/archive/spring23/cos461/exams/spring06-cos461-exam2-answers.doc>

```text
QUESTION 1, GRADUATE STUDENTS: Quality of Service (15 POINTS)

*** This question is only for the graduate students in the class  undergraduate students should skip this question and proceed to the next page. ***

(1a) Consider an ATM network with a leaky-bucket policer (also known as a token-bucket filter) that ensures a virtual circuit does not send more cells than expected. If the policer has a bucket depth of 10 cells and a token rate of 100 cells/second, how many cells can the virtual circuit transmit during a one-second period? In a ten-second period?

Burst of 10 cells plus the token rate. So, 110 for one second. And 1010 for ten seconds.

(1b) Suppose a link has a propagation delay of P seconds and transmits R cells per second. Suppose a cell arrives when the link has Q other cells awaiting transmission, and has just started transmitting the first cell. What delay does the new cell experience, as a function of P, R, and Q?

Propagation delay of P seconds With Q other packets in the queue, must wait for Q+1 transmissions at one every 1/R seconds.

So, the total delay is P + (Q+1)/R

(1c) Suppose a link has a first-in-first-out queue and carries traffic for two virtual circuits. The traffic on the first virtual circuit obeys a token-bucket filter with a bucket depth of 9 cells and a token rate of 100 cells/second, and can settle for best-effort service. The traffic on the second virtual circuit obeys a token-bucket filter with a bucket depth of one cell and a token rate of 100 cells/second, and cannot tolerate more than 100 msec of delay in delivering each cell. Suppose the propagation delay on the link is 60 msec. What is the smallest transmission rate R, in cells per second, that can satisfy the delay constraint, given that the link serves cells in first-in-first-out order?

If the link rate is less than the sum of the two token-bucket rates, then an arbitrarily long backlog can develop. Otherwise, the link can drain the queue as fast as cells arrive, except for a burst of cells that arrive at the same time. This burst size is limited by the sum of the two bucket depths, allowing a backlog of at most 10 (i.e., 9 + 1) cells.

If the one cell from the delay-sensitive virtual circuit arrives just after the other nine, it experiences delay P + 10/R, where P is 60 msec. For the total to be less than or equal to 100 msec, we must have 10/R less than or equal to 40 msec. Thus, R must be at least 250 cells/second.

(1d) Explain why a different kind of link scheduler would allow a smaller value of R to suffice.

Forcing both virtual circuits to share the same queue makes the delay-sensitive virtual subject vulnerable to bursty traffic from the other virtual circuit. Having separate queues, with strict priority or weighted fair scheduling, would limit the impact the burst virtual circuit would have on the performance experienced by the cells in the delay-sensitive virtual circuit. QUESTION 2: Intradomain Routing (15 POINTS) (2a) The picture below shows a network with 8 routers, where each link has an integer weight (e.g., the link between u and v has weight 2). Add arrowheads to the picture to illustrate the shortest-path tree rooted at u. For example, the edge from u to v would be marked with an arrow head where the line meets node v. Please draw neatly.

SHAPE

All but three nodes are reached along the clockwise path starting at node u, with costs of 2, 4, 5, and 7, respectively. The other three nodes, down and to the right of u, are reached with costs of 2, 3, and 6, respectively, through us downward neighbor. (2b) Suppose node u sends a large amount of traffic to node v, consuming most of the bandwidth on the (u,v) link. The traffic from u to w also traverses the (u,v) link. To alleviate congestion on the (u,v) edge, the network administrator plans to change the weight of the (v,w) edge to divert the traffic from u to w onto another path. What is the minimum weight the (v,w) edge would need to force all of the traffic from u to w to take a different path? What is the maximum weight the link could have while still ensuring the traffic from v to w goes directly over the (v,w) link?

The next shortest path from u to w goes down from node u and has a cost of 5 (= 2 + 1 + 2). To make the path (u,v,w) strictly longer, it needs to have a length of 6 (i.e., 2 + 4). So, the answer is 4.

If the cost of edge (v,w) is too large, even traffic from v to w would choose a different path. The next shortest path from v to w goes through u and has a cost of 7 (= 2 + 2 + 1 + 2). So, the cost of the (v,w) edge should not exceed 6.

(2c) Why would a network administrator change the link weight, rather than simply relying on the end hosts (connected to node u) to adapt their sending rates in the presence of congestion?

Although TCP senders slow down in the presence of congestion, this does not ensure that network resources are used efficiently. Two TCP senders might each send at half the rate of a shared link while another path lies idle. By changing the link weights, the network operators can change the paths the traffic traverses  something TCP cannot do  allowing the TCP senders to transmit at higher rates and offer better performance to users. QUESTION 3: Interdomain Routing (15 POINTS)

(3a) How does the Border Gateway Protocol (BGP) avoid the count-to-infinity problem that plagues distance-vector protocols?

BGF is a path-vector protocol. That is, BGP announcements include the entire path traversed by the message, not simply a total cost. A router, upon receiving a BGP announcement, can check for its own AS number in the path; if the AS number is present, the path has a loop and is immediately discarded.

(3b) A tier-1 Internet Service Provider (ISP) is an Autonomous System (AS) that offers transit service to its customers but has no upstream providers of its own. The small collection of tier-1 ISPs (e.g., UUNET, Sprint, AT&T, and Level3) all connect directly to each other, with peer-peer relationships. Why does a tier-1 ISP need a peer-peer relationship with every other tier-1 ISPs?

Having no upstream providers of its own, a tier-1 ISP must rely on its peers and customers to reach remote destinations. However, the ISP can only reach its own customers (and its customers customers, recursively) through the connections to customers. A tier-1 ISP must peer with another tier-1 ISP so they can reach each others respective customers. The peering is full mesh because a peer does not provide transit service, meaning that two ISPs cannot communicate through a mutual peer.

(3c) Give two examples of filtering policies applied to BGP sessions, one for an import policy (filtering routes sent by a neighbor) and another for an export policy (filtering routes sent to a neighbor).

- Import filtering: discarding prefixes that a customer advertises but does not own - Export filtering: not announcing peer-learned routes to another peer
```
- source: <https://www.cs.princeton.edu/courses/archive/spr06/cos461/exams/midterm2-answers.doc>

```text
QUESTION 1, GRADUATE STUDENTS: Quality of Service (15 POINTS)

*** This question is only for the graduate students in the class  undergraduate students should skip this question and proceed to the next page. ***

(1a) Consider an ATM network with a leaky-bucket policer (also known as a token-bucket filter) that ensures a virtual circuit does not send more cells than expected. If the policer has a bucket depth of 10 cells and a token rate of 100 cells/second, how many cells can the virtual circuit transmit during a one-second period? In a ten-second period?

Burst of 10 cells plus the token rate. So, 110 for one second. And 1010 for ten seconds.

(1b) Suppose a link has a propagation delay of P seconds and transmits R cells per second. Suppose a cell arrives when the link has Q other cells awaiting transmission, and has just started transmitting the first cell. What delay does the new cell experience, as a function of P, R, and Q?

Propagation delay of P seconds With Q other packets in the queue, must wait for Q+1 transmissions at one every 1/R seconds.

So, the total delay is P + (Q+1)/R

(1c) Suppose a link has a first-in-first-out queue and carries traffic for two virtual circuits. The traffic on the first virtual circuit obeys a token-bucket filter with a bucket depth of 9 cells and a token rate of 100 cells/second, and can settle for best-effort service. The traffic on the second virtual circuit obeys a token-bucket filter with a bucket depth of one cell and a token rate of 100 cells/second, and cannot tolerate more than 100 msec of delay in delivering each cell. Suppose the propagation delay on the link is 60 msec. What is the smallest transmission rate R, in cells per second, that can satisfy the delay constraint, given that the link serves cells in first-in-first-out order?

If the link rate is less than the sum of the two token-bucket rates, then an arbitrarily long backlog can develop. Otherwise, the link can drain the queue as fast as cells arrive, except for a burst of cells that arrive at the same time. This burst size is limited by the sum of the two bucket depths, allowing a backlog of at most 10 (i.e., 9 + 1) cells.

If the one cell from the delay-sensitive virtual circuit arrives just after the other nine, it experiences delay P + 10/R, where P is 60 msec. For the total to be less than or equal to 100 msec, we must have 10/R less than or equal to 40 msec. Thus, R must be at least 250 cells/second.

(1d) Explain why a different kind of link scheduler would allow a smaller value of R to suffice.

Forcing both virtual circuits to share the same queue makes the delay-sensitive virtual subject vulnerable to bursty traffic from the other virtual circuit. Having separate queues, with strict priority or weighted fair scheduling, would limit the impact the burst virtual circuit would have on the performance experienced by the cells in the delay-sensitive virtual circuit. QUESTION 2: Intradomain Routing (15 POINTS) (2a) The picture below shows a network with 8 routers, where each link has an integer weight (e.g., the link between u and v has weight 2). Add arrowheads to the picture to illustrate the shortest-path tree rooted at u. For example, the edge from u to v would be marked with an arrow head where the line meets node v. Please draw neatly.

SHAPE

All but three nodes are reached along the clockwise path starting at node u, with costs of 2, 4, 5, and 7, respectively. The other three nodes, down and to the right of u, are reached with costs of 2, 3, and 6, respectively, through us downward neighbor. (2b) Suppose node u sends a large amount of traffic to node v, consuming most of the bandwidth on the (u,v) link. The traffic from u to w also traverses the (u,v) link. To alleviate congestion on the (u,v) edge, the network administrator plans to change the weight of the (v,w) edge to divert the traffic from u to w onto another path. What is the minimum weight the (v,w) edge would need to force all of the traffic from u to w to take a different path? What is the maximum weight the link could have while still ensuring the traffic from v to w goes directly over the (v,w) link?

The next shortest path from u to w goes down from node u and has a cost of 5 (= 2 + 1 + 2). To make the path (u,v,w) strictly longer, it needs to have a length of 6 (i.e., 2 + 4). So, the answer is 4.

If the cost of edge (v,w) is too large, even traffic from v to w would choose a different path. The next shortest path from v to w goes through u and has a cost of 7 (= 2 + 2 + 1 + 2). So, the cost of the (v,w) edge should not exceed 6.

(2c) Why would a network administrator change the link weight, rather than simply relying on the end hosts (connected to node u) to adapt their sending rates in the presence of congestion?

Although TCP senders slow down in the presence of congestion, this does not ensure that network resources are used efficiently. Two TCP senders might each send at half the rate of a shared link while another path lies idle. By changing the link weights, the network operators can change the paths the traffic traverses  something TCP cannot do  allowing the TCP senders to transmit at higher rates and offer better performance to users. QUESTION 3: Interdomain Routing (15 POINTS)

(3a) How does the Border Gateway Protocol (BGP) avoid the count-to-infinity problem that plagues distance-vector protocols?

BGF is a path-vector protocol. That is, BGP announcements include the entire path traversed by the message, not simply a total cost. A router, upon receiving a BGP announcement, can check for its own AS number in the path; if the AS number is present, the path has a loop and is immediately discarded.

(3b) A tier-1 Internet Service Provider (ISP) is an Autonomous System (AS) that offers transit service to its customers but has no upstream providers of its own. The small collection of tier-1 ISPs (e.g., UUNET, Sprint, AT&T, and Level3) all connect directly to each other, with peer-peer relationships. Why does a tier-1 ISP need a peer-peer relationship with every other tier-1 ISPs?

Having no upstream providers of its own, a tier-1 ISP must rely on its peers and customers to reach remote destinations. However, the ISP can only reach its own customers (and its customers customers, recursively) through the connections to customers. A tier-1 ISP must peer with another tier-1 ISP so they can reach each others respective customers. The peering is full mesh because a peer does not provide transit service, meaning that two ISPs cannot communicate through a mutual peer.

(3c) Give two examples of filtering policies applied to BGP sessions, one for an import policy (filtering routes sent by a neighbor) and another for an export policy (filtering routes sent to a neighbor).

- Import filtering: discarding prefixes that a customer advertises but does not own - Export filtering: not announcing peer-learned routes to another peer
```

## CMU 15-213 Introduction to Computer Systems / Fall 2012 Final

### Problem 1, item 8
- pages: 3
- overlap: short counts in Unix/network I/O; read/write edge cases relevant to socket programming
- source: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f12.pdf>

```text
[page 3]

5. Suppose an int A is stored at virtual address 0xff987cf0, while another int B is stored at virtual address 0xff987d98. If the size of a page is 0x1000 bytes, then A’s physical address is numerically less than B’s physical address.

(a) Always true
(b) Always false
(c) Sometimes true, sometimes false
(d) Not enough information

6. Assuming no errors, which one of the following functions returns exactly once?

(a) fork()
(b) execve()
(c) exit()
(d) longjmp()
(e) waitpid()

7. On a 64-bit system, which of the following C expressions is equivalent to the C expression (x[2] + 4)[3]? Assume x is declared as int **x.

(a) *((*(x + 16)) + 28)
(b) *((*(x + 2)) + 7)
(c) **(x + 28)
(d) *(((*x) + 2) + 7)
(e) (**(x + 2) + 7)

8. When can short counts occur?

(a) When an EOF is encountered during a read
(b) When a short int is used as a counter
(c) When reading or writing to disk files
(d) When the kernel runs out of kernel memory

(more)
```
- source: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f12-sol.txt>

```text
Problem 1 ********* 01-b 02-a 03-c 04-d 05-a 06-e 07-b 08-a 09-c 10-b 11-d 12-d 13-b 14-(d or e) 15-c 16-d 17-a 18-b

1pt each

For 1.14, we allowed e, even though it's not strictly true, because if appears in the lecture notes and textbook.

*********
```

### Problem 1, item 10
- pages: 4
- overlap: listening-socket readiness vs signals; write on disconnected socket
- source: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f12.pdf>

```text
[page 4]

9. A program blocks SIGCHLD and SIGUSR1. It is then sent a SIGCHLD, a SIGUSR1, and another SIGCHLD, in that order. What signals does the program receive after it unblocks both of those signals (you may assume the program does not receive any more signals after)?

(a) None, since the signals were blocked they are all discarded.
(b) Just a single SIGCHLD, since all subsequent signals are discarded.
(c) Just a single SIGCHLD and a single SIGUSR1, since the extra SIGCHLD is discarded.
(d) All 3 signals, since no signals are discarded.

10. Which of the following events does not generate a signal?

(a) Division by zero
(b) A new connection arrives on a listening socket
(c) A write is attempted on a disconnected socket
(d) NULL is dereferenced
(e) A process whose parent has already terminated exits

11. In an x86-64 system, how many integers can be stored in a cache line if your cache is 4KB, is 4-way set-associative, and contains 4 sets?

(a) 8
(b) 16
(c) 32
(d) 64
(e) 128

12. Which types of locality are leveraged by virtual memory?

(a) Spatial locality
(b) Temporal locality
(c) Prime locality
(d) Both (a) and (b)
(e) Both (b) and (c)

13. Which of the following is not a section of an ELF file?

(a) .text
(b) .static
(c) .rodata
(d) .data
(e) .bss

(more)
```
- source: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f12-sol.txt>

```text
Problem 1 ********* 01-b 02-a 03-c 04-d 05-a 06-e 07-b 08-a 09-c 10-b 11-d 12-d 13-b 14-(d or e) 15-c 16-d 17-a 18-b

1pt each

For 1.14, we allowed e, even though it's not strictly true, because if appears in the lecture notes and textbook.

*********
```

### Problem 10(A), 10(B), 10(C), 10(D), 10(E)
- pages: 18-20
- overlap: race conditions, thread argument passing, synchronization patterns relevant to threaded socket servers
- source: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f12.pdf>

```text
Problem 10. (10 points): Concurrency, races, and synchronization. Consider a simple concurrent program with the following specification: The main thread creates two peer threads, passing each peer thread a unique integer thread ID (either 0 or 1), and then waits for each thread to terminate. Each peer thread prints its thread ID and then terminates.

Each of the following programs attempts to implement this specification. However, some are incorrect because they contain a race on the value of myid that makes it possible for one or more peer threads to print an incorrect thread ID. Except for the race, each program is otherwise correct.

You are to indicate whether or not each of the following programs contains such a race on the value of myid. You will be graded on each subproblem as follows:

• If you circle no answer, you get 0 points.

• If you circle the right answer, you get 2 points.

• If you circle the wrong answer, you get −1 points (so don’t just guess wildly).

A. Does the following program contain a race on the value of myid? Yes No

void *foo(void *vargp) { int myid; myid = *((int *)vargp); Free(vargp); printf("Thread %d\n", myid); }

int main() { pthread_t tid[2]; int i, *ptr;

for (i = 0; i < 2; i++) { ptr = Malloc(sizeof(int)); *ptr = i; Pthread_create(&tid[i], 0, foo, ptr); } Pthread_join(tid[0], 0); Pthread_join(tid[1], 0); }
```
- source: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f12-sol.txt>

```text
Problem 10 ********** A. No, each thread has its own heap variable for myid. B. Yes, both threads can point to myid. C. No, myid is passed in on the stack. D. Yes, the mutex doesn't protect myid. E. No, the mutex protects the assignment of myid.
```

## CMU 15-213 Introduction to Computer Systems / Spring 2011 Final

### Problem 1, item 9; Problem 1, item 14
- pages: 5
- overlap: gethostbyname network failure and thread-safety
- source: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-s11.pdf>

```text
[page 5]

7. Consider the following piece of code, where out.txt’s contents are “abc”:

int main(int argc, char** argv) { int fd = open("out.txt", O_RDWR); char str[] = "xyz"; char c;

write(fd1, str, 1); read(fd1, &c, 1); write(fd1, &c, 1); return 0; }

What is the contents of out.txt after the code is run? Assume all system calls succeed.

(a) xbb
(b) xba
(c) xac
(d) boat

8. Which of the following is the best reason to choose FastCGI over CGI?

(a) Superior support by web servers like Apache
(b) Lower process creation costs
(c) Lower process communication costs
(d) Better process locality (all tasks can be executed locally)

9. Which of the following system calls can fail due to a network failure?

(a) socket(...)
(b) listen(...)
(c) bind(...)
(d) gethostbyname(...)

10. Which of the following are copied on fork and preserved on exec?

(a) Global variables.
(b) File descriptor tables.
(c) Open file entry structs.
(d) None of the above.
```
- source: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-s11-sol.txt>

```text
Problem 1 *********

1. d
```

### Problem 1, item 18; Problem 1, item 21
- pages: 7
- overlap: socket send blocking/short writes; debugging a network application with system-call tracing
- source: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-s11.pdf>

```text
[page 7]

16. What is the function of the TLB?

(a) Caches data
(b) Caches instructions
(c) Caches translation of virtual addresses
(d) Translates physical addresses to virtual addresses

17. What is distinctive about superscalar processors?

(a) Can run at frequencies over 3.5GHz
(b) Can address over 4GB of memory
(c) Can perform more than one instruction per cycle
(d) Can have more than 2 levels of cache
(e) Have more than one core per processor

18. True/False: When requested to send 20 bytes over a network socket, execution will block until all 20 bytes have been sent.

(a) True
(b) False

19. True/False: When printf returns, the programmer cannot be guaranteed that the data has appeared on the user’s terminal.

(a) True
(b) False

20. Which of the following tools would you first use to debug an application which is exiting with the error “Segmentation fault”?

(a) gdb
(b) strace
(c) strings
(d) objdump
```
- source: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-s11-sol.txt>

```text
Problem 1 *********

1. d
```

## CMU 15-213 Introduction to Computer Systems / Fall 2010 Final

### Problem 1, item 1
- pages: 2
- overlap: socket/listen/connect/accept/socket/bind call ordering
- source: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f10.pdf>

```text
Problem 1. (20 points): Short answer and multiple choice questions on a variety of stimulating and refreshing topics.
```
- source: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f10-sol.txt>

```text
Problem 1 *********
1. client server listen x 3 connect 2 x accept x 4 socket 1 1 bind x 2

2-d 3-a 4-b 5-c 6-b 7-c 8-a 9-d 10-d

11-c 12-a 13-b 14-c 15-d 16-d 17-b 18-b 19-d

*********
```

## CMU 15-213 Introduction to Computer Systems / Fall 2009 Final

### Problem 1, item E
- pages: 3
- overlap: listening-socket events and signal misconceptions
- source: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f09.pdf>

```text
Problem 1. Multiple Choice (18 points): A. Which of these uses of caching is not crucial to program performance?

(e) None of the above (i.e., they are all crucial) B. For which values can X not be equal to Z in the code below (circle all that apply): int X = CONSTANT; float Y = X; int Z = Y;
```
- source: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f09-sol.txt>

```text
Problem 1 *********

1. c
```

### Problem 6(A), 6(B)
- pages: 12-13
- overlap: TCP client/server call sequence; short recv/partial-read behavior
- source: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f09.pdf>

```text
Problem 6. Network Programming (12 points):

A. Consider a logging daemon, whose purpose is simply to accept messages from clients and log them to a file. (This is sometimes used in secure networks to ensure that, even if a cracker breaks into one computer, he can’t erase his traces from the logs because they are stored elsewhere.) In the following table, please list the system and/or library calls that each side of the connection would make. Each row should contain the name of a single system or library call, placed in the appropriate column. Please list the calls in the order they are called, not the order they return. Please only include network-related operations (accept, bind, close, connect, listen, read, socket, and write). You should make the following assumptions:

• The server finishes initializing before the client starts. • The server only serves a single client. • The client already knows the server’s IP address. • The client only sends one message before closing the connection.

Server: Client:
```
- source: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-f09-sol.txt>

```text
6. b

*********
Problem 2 *********

VA_GET_PPO: (virtual & 0xfff) VA_GET_PTI: ((virtual >> 12) & 0x3ff) VA_GET_PDI: ((virtual >> 22) & 0x3ff) PDE_GET_PTBA: (pde & 0xfffff000) PTE_GET_PBA: (pde & 0xfffff000) IS_PRESENT: (pte & 0x1) IS_WRITABLE: ((pte & 0x2) >> 1) SET_PRESENT: (((pte >> 1) << 1) + pres) SET_WRITABLE: ((pte & 0x1) + ((pte >> 2) << 2) + (write << 1))

*********
```

## CMU 15-213 Introduction to Computer Systems / Spring 2009 Final

### Problem 6(A), 6(B)
- pages: 13-15
- overlap: socket server error paths; threaded server/network logic bugs
- source: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-s09.pdf>

```text
Problem 6. (10 points): Crummy Networks Error Handling Below is some code for a concurrent echo server. We have left out the error handling code for the three functions socket, send, and recv. These blanks are marked with

/**** WRITE CODE BELOW *******/

<and you have to fill in here>

/***** WRITE CODE ABOVE *****/

Please fill in those blanks with appropiate error handling code. Do not print out any messages, just modify the control flow.
```
- source: <https://www.cs.cmu.edu/afs/cs/academic/class/15213-f15/www/oldexams/final-s09-sol.txt>

```text
Problem 6

**************

On socket error: exit(-1);

On recv error: break;

On send error: break;

Bug 1: buffer is a global variable and shared by all

threads, there exists a race condition in reading and writing

to the shared buffer. Solving this race condition would

require making buffer a local variable to handleConnection();

Bug 2: send() is not guaranteed to send all of the buffer in one

call. This is referred to as a send short count. You must examine

the positive return values of send to verify that it did send all

of the data, and resend if necessary.

**************
```
