# CSC4303 Exam Practice Questions with Answers

This English-only practice set is based on `review.pdf`, lecture PDFs `02` through `18`, the style of `CSC4303_exam_sample.pdf`, and the filtered topic patterns in `exam_sources.md`. The questions are rewritten practice questions, not verbatim copies of public exams. Each question is followed immediately by its answer.

Total questions: 419.


## Network Fundamentals

### Q001. Five-layer model

**Question:** List the five Internet layers from top to bottom and name the PDU at each layer.

**Answer:** Application/message, Transport/segment, Network/packet, Link/frame, Physical/bit.

### Q002. Layer responsibilities

**Question:** For each of the five Internet layers, briefly state its main responsibility.

**Answer:** Application: programs that use network service. Transport: end-to-end delivery between processes. Network: packet delivery across multiple networks. Link: frame delivery over one or more local links. Physical: bit transmission using signals.

### Q003. Why layering

**Question:** Give two benefits and one cost of network layering.

**Answer:** Benefits: modularity and abstraction; each layer can change implementation while preserving its interface. Cost: extra headers/processing and sometimes lost cross-layer optimization opportunities.

### Q004. Protocol definition

**Question:** What does a protocol define? Give at least four items.

**Answer:** A protocol defines message syntax and semantics, message order, actions on send/receive, peer interaction, error handling, termination behavior, and the API exposed to higher layers.

### Q005. Multiplexing

**Question:** Explain multiplexing and demultiplexing in a layered network.

**Answer:** Multiplexing lets multiple upper-layer users share a lower-layer service. Demultiplexing uses header fields, such as protocol numbers or ports, to deliver incoming data to the correct upper-layer object.

### Q006. Circuit switching versus packet switching

**Question:** Compare circuit switching and packet switching. Why is packet switching attractive for bursty Internet traffic?

**Answer:** Circuit switching reserves a fixed path and capacity, which wastes resources during idle periods. Packet switching sends self-contained packets and statistically multiplexes many bursty users, improving average utilization.

### Q007. Store and forward

**Question:** What does store-and-forward mean in packet switching?

**Answer:** A switch or router receives the full packet, stores it temporarily, examines the header, and then forwards it to the next hop.

### Q008. Communication-channel metrics

**Question:** Name four metrics used to model a communication channel.

**Answer:** Latency, capacity or bandwidth, jitter, and loss or reliability.

### Q009. Delay components

**Question:** Name the four common components of packet delay.

**Answer:** Propagation delay, transmission delay, processing delay, and queueing delay.

### Q010. Propagation delay calculation

**Question:** A signal travels 900 km in fiber at 2 x 10^8 m/s. What is the one-way propagation delay?

**Answer:** 900 km = 900,000 m. Delay = 900,000 / (2 x 10^8) = 0.0045 s = 4.5 ms.

### Q011. Transmission delay calculation

**Question:** A 15,000-bit packet is sent on a 5 Mbps link. What is the transmission delay?

**Answer:** 15,000 / 5,000,000 = 0.003 s = 3 ms.

### Q012. Two-hop store-and-forward delay

**Question:** A packet crosses two links. Each link has 6 ms propagation delay and 2 ms transmission delay. Ignore queueing and processing. What is the store-and-forward delay?

**Answer:** For two store-and-forward hops: 2 x (6 + 2) = 16 ms.

### Q013. Two-hop cut-through delay

**Question:** A packet crosses two cut-through links. Each link has 6 ms propagation delay and 2 ms transmission delay. Ignore queueing and processing. What is the approximate delay?

**Answer:** Approximate cut-through delay = 2 x propagation + one transmission = 2 x 6 + 2 = 14 ms.

### Q014. Path throughput

**Question:** A long stream crosses links of 10 Mbps, 6 Mbps, and 20 Mbps. What is the sustained throughput?

**Answer:** The sustained throughput is limited by the bottleneck link: 6 Mbps.

### Q015. Bottleneck link

**Question:** Why is the slowest link the bottleneck during sustained packet streaming?

**Answer:** Once the pipeline is full, all links can work in parallel, but the slowest stage determines how quickly completed packets can leave the path.

### Q016. Queue usefulness

**Question:** Why can buffers help with short bursts but not solve persistent overload?

**Answer:** Buffers absorb temporary input bursts. If the long-term input rate exceeds output capacity, the queue grows until packets are delayed excessively or dropped.

### Q017. Congestion symptom

**Question:** What happens to delay and loss when offered load approaches or exceeds capacity?

**Answer:** Queues fill, delay rises sharply, packet loss increases, retransmissions increase load, and useful goodput can fall.

### Q018. Throughput versus goodput

**Question:** Define throughput and goodput. Why can goodput be much lower under congestion?

**Answer:** Throughput counts all delivered traffic, including retransmissions. Goodput counts useful new application data. Under congestion, losses and spurious retransmissions waste capacity, lowering goodput.

### Q019. Bandwidth-delay product

**Question:** A path has bandwidth 40 Mbps and one-way delay 25 ms. What is the one-way bandwidth-delay product in bytes?

**Answer:** 40 x 10^6 x 0.025 = 1,000,000 bits = 125,000 bytes.

### Q020. RTT in-flight data

**Question:** A TCP sender sees RTT = 80 ms and wants to fill a 25 Mbps path. How many bits should be in flight?

**Answer:** Bandwidth x RTT = 25 x 10^6 x 0.08 = 2,000,000 bits.

### Q021. Header overhead

**Question:** With MTU 1500 bytes, IPv4 header 20 bytes, and TCP header 20 bytes, what is the maximum TCP payload in one Ethernet frame?

**Answer:** 1500 - 20 - 20 = 1460 bytes.

### Q022. Header overhead ratio

**Question:** Using MTU 1500 bytes, IPv4 header 20 bytes, and TCP header 20 bytes, what fraction of the frame is TCP/IP header overhead?

**Answer:** 40 / 1500 = 0.0267, or about 2.67%.

### Q023. Black-box abstraction

**Question:** What is meant by black-box abstraction in layering?

**Answer:** A layer exposes a stable service interface while hiding its internal implementation from higher layers.

### Q024. Layer replacement

**Question:** Give an example of how layering lets one part of the network change without changing applications.

**Answer:** An application using TCP can run over Ethernet, Wi-Fi, or cellular links because the lower layers hide link-specific details.

### Q025. Packet switching analogy

**Question:** Why are packets often compared to postal letters?

**Answer:** Each packet carries an address and can be forwarded independently by intermediate nodes toward its destination.

### Q026. Loss and reliability

**Question:** If a channel may drop packets, which higher-level mechanisms can recover from loss?

**Answer:** Acknowledgments, retransmissions, sequence numbers, timers, and congestion/flow-control policies can recover or adapt to loss.

### Q027. Jitter

**Question:** What is jitter, and why does it matter for voice or video?

**Answer:** Jitter is variation in delay. Real-time media needs smooth playback, so high jitter can cause glitches unless buffered.

### Q028. Processing delay

**Question:** Give two examples of work included in router processing delay.

**Answer:** Checking packet headers/checksums and looking up the next hop in the forwarding table.

### Q029. Queueing delay

**Question:** What determines queueing delay at a router output port?

**Answer:** Traffic load, output-link service rate, buffer occupancy, and burstiness of arrivals.


## Transport Layer, TCP/UDP, Flow Control, and Congestion Control

### Q030. Transport-layer purpose

**Question:** What service does the transport layer provide to applications?

**Answer:** It provides process-to-process, end-to-end data delivery over the network layer.

### Q031. TCP versus UDP

**Question:** Compare TCP and UDP in terms of connection model, reliability, data boundaries, flow control, and congestion control.

**Answer:** TCP is connection-oriented, reliable, in-order, byte-stream based, and includes flow and congestion control. UDP is connectionless, datagram-based, and may lose, duplicate, or reorder messages; it has no built-in flow or congestion control.

### Q032. Choosing UDP

**Question:** Would you use TCP or UDP for a real-time multiplayer game? Briefly justify.

**Answer:** Often UDP, because low latency matters and occasional loss can be tolerated or handled by application-specific logic.

### Q033. Choosing TCP

**Question:** Would you use TCP or UDP for an email service? Briefly justify.

**Answer:** TCP, because reliable and ordered delivery is more important than tolerating packet loss.

### Q034. DNS transport

**Question:** Why is UDP commonly used for DNS queries?

**Answer:** DNS queries are typically small and latency-sensitive. UDP avoids connection setup overhead; retransmission can be handled by retrying the query.

### Q035. Ports

**Question:** What identifies an application process endpoint in Internet transport?

**Answer:** The tuple of IP address, transport protocol, and port number identifies an endpoint.

### Q036. Well-known port

**Question:** What is the usual port for HTTP and HTTPS?

**Answer:** HTTP uses TCP port 80. HTTPS uses TCP port 443.

### Q037. Ephemeral ports

**Question:** Why do clients often use ephemeral ports?

**Answer:** The OS temporarily assigns a port to distinguish the client's connection or datagram flow from other local flows.

### Q038. UDP maximum payload

**Question:** IPv4 total length is at most 65,535 bytes. With 20-byte IPv4 header and 8-byte UDP header, what is the maximum UDP application payload?

**Answer:** 65,535 - 20 - 8 = 65,507 bytes.

### Q039. TCP payload under Ethernet MTU

**Question:** With Ethernet MTU 1500 bytes and 20-byte IPv4 and TCP headers, what is the maximum TCP payload per segment without IP fragmentation?

**Answer:** 1500 - 20 - 20 = 1460 bytes.

### Q040. TCP phases

**Question:** Name the three primary phases of TCP.

**Answer:** Connection establishment, sliding-window data transfer with flow control, and connection release.

### Q041. Three-way handshake

**Question:** In TCP, client ISN is x and server ISN is y. Write the three main handshake messages and ACK values.

**Answer:** Client sends SYN seq=x. Server sends SYN seq=y and ACK=x+1. Client sends ACK=y+1, usually with seq=x+1.

### Q042. Why three-way handshake

**Question:** Why does TCP use a three-way handshake instead of only two messages?

**Answer:** It lets both sides confirm bidirectional reachability and fresh sequence numbers, making the connection robust against delayed duplicates.

### Q043. Connection release

**Question:** Why does TCP connection release need one FIN for each direction?

**Answer:** A TCP connection is full-duplex. Each FIN closes one direction of data transfer, so both directions must be closed separately.

### Q044. TCP byte stream

**Question:** What does it mean that TCP is a byte stream rather than a message protocol?

**Answer:** TCP preserves byte order but not application message boundaries; the application must define framing if it needs messages.

### Q045. UDP message boundaries

**Question:** Does UDP preserve application message boundaries?

**Answer:** Yes. Each UDP datagram is delivered as a separate message if it is delivered at all.

### Q046. Flow-control goal

**Question:** State the goal of TCP flow control.

**Answer:** To match the sender's transmission rate or outstanding data to the receiver's available buffer capacity.

### Q047. Receiver window

**Question:** What is the advertised receive window in TCP used for?

**Answer:** It tells the sender how much buffer space the receiver has available, limiting the amount of unacknowledged data in flight.

### Q048. Stop-and-wait throughput

**Question:** A stop-and-wait sender uses 10 Kbit packets and RTT is 100 ms. How many packets per second can it send successfully?

**Answer:** One packet per RTT, so 1 / 0.1 = 10 packets per second.

### Q049. Stop-and-wait utilization

**Question:** With 10 Kbit packets, RTT 100 ms, and link bandwidth 1 Mbps, what is stop-and-wait utilization?

**Answer:** The sender delivers 10 packets/s x 10 Kbit = 100 Kbit/s. Utilization = 100 Kbit/s / 1 Mbit/s = 10%.

### Q050. Stop-and-wait at higher bandwidth

**Question:** With the same 10 Kbit packets and RTT 100 ms, what is utilization on a 10 Mbps link?

**Answer:** Throughput is still 100 Kbit/s. Utilization = 100 Kbit/s / 10 Mbit/s = 1%.

### Q051. Sliding-window idea

**Question:** How does a sliding window improve on stop-and-wait?

**Answer:** It allows multiple packets to be outstanding during one RTT, using pipelining to keep the path busy.

### Q052. Window to fill path

**Question:** A path has bandwidth 1 Mbps, one-way delay 50 ms, and packet size 10 Kbit. What window size fills the path?

**Answer:** RTT = 100 ms. In-flight data needed = 1 Mbps x 0.1 s = 100 Kbit. Window = 100 Kbit / 10 Kbit = 10 packets.

### Q053. Window with larger bandwidth

**Question:** A path has bandwidth 10 Mbps, one-way delay 50 ms, and packet size 10 Kbit. What window size fills the path?

**Answer:** RTT = 100 ms. In-flight data = 10 Mbps x 0.1 s = 1 Mbit. Window = 1 Mbit / 10 Kbit = 100 packets.

### Q054. Sender window variables

**Question:** If LFS is last frame sent, LAR is last ACK received, and window size is W, what condition must the sender maintain?

**Answer:** The sender maintains LFS - LAR <= W.

### Q055. Go-Back-N receiver

**Question:** In Go-Back-N, what does the receiver do with an out-of-order packet?

**Answer:** It discards the out-of-order packet and usually repeats the ACK for the last in-order packet received.

### Q056. Go-Back-N retransmission

**Question:** Packets 42, 43, 44, and 45 are sent using Go-Back-N. Packet 43 is lost. What must be retransmitted after timeout?

**Answer:** Packet 43 and later unacknowledged packets, such as 44 and 45, must be retransmitted.

### Q057. Selective Repeat receiver

**Question:** How does Selective Repeat handle out-of-order packets?

**Answer:** It buffers out-of-order packets within the receiver window and delivers data to the application only when earlier missing packets arrive.

### Q058. Selective Repeat timers

**Question:** How do retransmission timers differ between Go-Back-N and Selective Repeat?

**Answer:** Go-Back-N commonly uses one timer for the oldest unacknowledged packet. Selective Repeat uses a timer per unacknowledged segment.

### Q059. Sequence-number wraparound

**Question:** Why must sequence-number space be large enough in sliding-window protocols?

**Answer:** Delayed old packets must not be mistaken for new packets after sequence numbers wrap around.

### Q060. TCP uses which style

**Question:** TCP is closer to Go-Back-N or Selective Repeat?

**Answer:** TCP uses a selective-repeat-like design because it can buffer out-of-order data and can use selective acknowledgments in modern implementations.

### Q061. Congestion definition

**Question:** Define network congestion.

**Answer:** Congestion occurs when traffic offered to network resources persistently exceeds available capacity, causing queues, delay, and loss.

### Q062. Congestion versus flow control

**Question:** What is the difference between TCP flow control and congestion control?

**Answer:** Flow control protects the receiver from buffer overflow. Congestion control protects the network from overload.

### Q063. Congestion collapse

**Question:** Why can congestion collapse happen even when links are busy?

**Answer:** The network may carry many retransmissions and dropped packets, so link utilization is high but useful delivered application data is low.

### Q064. Offered load effect

**Question:** As offered load increases toward congestion, what happens to delay, loss, throughput, and goodput?

**Answer:** Delay and loss rise sharply. Throughput may stop increasing or decline due to loss. Goodput can be much lower due to retransmissions.

### Q065. Efficiency and fairness

**Question:** What are efficiency and fairness in bandwidth allocation?

**Answer:** Efficiency means using network capacity without causing congestion. Fairness means giving each sender or flow a reasonable share and avoiding starvation.

### Q066. Max-min fairness definition

**Question:** Give the intuition for max-min fairness.

**Answer:** Flows bottlenecked at the same saturated resource share it equally; increasing one flow's rate would require decreasing a flow with an equal or smaller rate.

### Q067. Max-min simple

**Question:** Two flows share a 10 Mbps bottleneck and have no other bottleneck. What is the max-min allocation?

**Answer:** Each flow receives 5 Mbps.

### Q068. Max-min with demand

**Question:** Three flows share a 12 Mbps bottleneck. Flow A demands at most 2 Mbps; B and C are unlimited. What is the max-min allocation?

**Answer:** Give A its 2 Mbps demand. The remaining 10 Mbps is split between B and C, so B = 5 Mbps and C = 5 Mbps.

### Q069. AIMD

**Question:** What do additive increase and multiplicative decrease do?

**Answer:** Additive increase slowly probes for more capacity. Multiplicative decrease rapidly backs off after congestion and tends to improve fairness.

### Q070. AIMD numeric

**Question:** A TCP flow has congestion window 20 MSS. After a loss with multiplicative decrease by half, what is the new congestion window?

**Answer:** 10 MSS.

### Q071. Slow start

**Question:** Why is TCP slow start called slow start even though the window grows exponentially?

**Answer:** It starts from a small congestion window to avoid immediately overloading the network, then grows quickly until it reaches a threshold or detects loss.

### Q072. Fast retransmit

**Question:** What event triggers TCP fast retransmit?

**Answer:** Typically, receiving multiple duplicate ACKs for the same sequence number suggests a missing segment and triggers retransmission before timeout.

### Q073. Fast recovery

**Question:** What is the purpose of fast recovery?

**Answer:** It avoids returning all the way to slow start after certain losses, keeping the pipe partially full while reducing the congestion window.

### Q074. Fair queuing

**Question:** At a high level, why can fair queuing help fairness?

**Answer:** It separates traffic into flows or classes and schedules them so one aggressive flow cannot monopolize the output queue.

### Q075. UDP and congestion

**Question:** Why can UDP applications be dangerous if they send at any rate they want?

**Answer:** UDP has no built-in congestion control, so uncontrolled sending can overload queues, cause loss, and harm other flows.

### Q076. Reliable UDP

**Question:** If an application wants reliable messages over UDP, what must it implement?

**Answer:** It must implement mechanisms such as sequence numbers, acknowledgments, retransmissions, timers, duplicate detection, and possibly congestion control.

### Q077. TCP connection state

**Question:** Name two TCP states a socket kernel object may hold during its lifetime.

**Answer:** Examples include LISTEN, SYN_SENT, SYN_RCVD, ESTABLISHED, FIN_WAIT, CLOSE_WAIT, and TIME_WAIT.

### Q078. Delayed duplicates

**Question:** How do fresh ISNs help TCP handle delayed duplicate segments?

**Answer:** Fresh sequence-number spaces make old duplicate segments unlikely to be accepted as valid data for a new connection.


## Network Layer, Addressing, Fragmentation, and Routing

### Q079. Network-layer goal

**Question:** What is the main goal of the network layer?

**Answer:** To deliver packets from a source host to a destination host, possibly across many hops and heterogeneous link-layer networks.

### Q080. Why network layer

**Question:** Give three reasons we need a network layer.

**Answer:** Internetworking across different link technologies, global addressing, and routing/forwarding across multiple hops.

### Q081. Datagram model

**Question:** In the datagram model, what information does each packet carry and how do routers use it?

**Answer:** Each packet carries a destination address. Each router uses a forwarding table to select the next hop independently for that packet.

### Q082. Virtual circuit model

**Question:** How is a virtual-circuit network different from a datagram network?

**Answer:** A virtual circuit sets up connection state along a path before data transfer; datagrams are forwarded independently without per-flow setup state in the network.

### Q083. IP as narrow waist

**Question:** What does it mean that IP is the narrow waist of the Internet?

**Answer:** Many applications and transports run above IP, and many link technologies run below it. IP provides a common minimal service between them.

### Q084. IPv4 address size

**Question:** How many bits are in an IPv4 address? How many in an IPv6 address?

**Answer:** IPv4 uses 32-bit addresses. IPv6 uses 128-bit addresses.

### Q085. CIDR prefix size

**Question:** How many addresses are in an IPv4 /24 prefix?

**Answer:** 2^(32-24) = 256 addresses.

### Q086. CIDR /16

**Question:** What address range is represented by 128.13.0.0/16?

**Answer:** 128.13.0.0 through 128.13.255.255.

### Q087. Single-host prefix

**Question:** Which IPv4 prefix length represents exactly one address?

**Answer:** /32.

### Q088. Default route

**Question:** What does the route 0.0.0.0/0 represent?

**Answer:** It is the default route. It matches all IPv4 destinations if no more-specific prefix matches.

### Q089. Longest-prefix matching 1

**Question:** A forwarding table has 0.0.0.0/0 -> A, 192.168.0.0/16 -> B, and 192.168.32.0/20 -> C. Where does destination 192.168.40.1 go?

**Answer:** 192.168.40.1 matches /16 and /20. The longest match is 192.168.32.0/20, so next hop C.

### Q090. Longest-prefix matching 2

**Question:** Using the same table, where does destination 192.168.8.2 go?

**Answer:** It matches 192.168.0.0/16 but not 192.168.32.0/20, so next hop B.

### Q091. Longest-prefix matching 3

**Question:** Using the same table, where does destination 192.24.1.1 go?

**Answer:** It only matches the default route 0.0.0.0/0, so next hop A.

### Q092. LPM with /25

**Question:** A table has 10.0.0.0/8 -> X, 10.1.0.0/16 -> Y, 10.1.2.0/24 -> Z, and 10.1.2.128/25 -> W. Which next hop is used for 10.1.2.200?

**Answer:** It matches all four prefixes, and /25 is longest, so next hop W.

### Q093. LPM with no specific match

**Question:** Using the previous table, which next hop is used for 10.1.3.7?

**Answer:** It matches /8 and /16 but not 10.1.2.0/24 or /25, so next hop Y.

### Q094. MTU

**Question:** What is MTU?

**Answer:** MTU is the maximum transfer unit, the largest frame or packet payload that a link can carry without fragmentation at that layer.

### Q095. IP fragmentation

**Question:** What happens when an IPv4 datagram is larger than the next link's MTU and fragmentation is allowed?

**Answer:** The datagram is split into multiple IP fragments, each with its own IP header and fragment offset information.

### Q096. Fragment reassembly

**Question:** Where are IPv4 fragments reassembled?

**Answer:** They are reassembled only at the final destination, not at intermediate routers.

### Q097. Fragment fields

**Question:** Name three IPv4 fields used for fragmentation.

**Answer:** Identification, fragment offset, and flags such as DF and MF.

### Q098. Fragmentation overhead

**Question:** Why can fragmentation hurt performance?

**Answer:** It adds header overhead, increases loss sensitivity because losing one fragment loses the whole original datagram, and adds reassembly work.

### Q099. DF bit

**Question:** What is the purpose of the IPv4 DF flag?

**Answer:** DF means Don't Fragment. If a datagram cannot be forwarded without fragmentation, it should be dropped and an error may be returned.

### Q100. DHCP bootstrap

**Question:** How can a host contact a DHCP server before it has an IP address?

**Answer:** It sends a link-layer and IP broadcast, such as to 255.255.255.255, so all local nodes including a DHCP server can receive it.

### Q101. DHCP purpose

**Question:** What does DHCP provide to a newly joining host?

**Answer:** It can provide an IP address, subnet information, default gateway, DNS server addresses, and lease information.

### Q102. ARP purpose

**Question:** What problem does ARP solve?

**Answer:** ARP maps a local IP address to a link-layer address such as an Ethernet MAC address.

### Q103. ARP locality

**Question:** Why is ARP used only on the local link?

**Answer:** Link-layer addresses are meaningful only on the local network segment; remote delivery is handled through routers and next-hop link addresses.

### Q104. ICMP purpose

**Question:** What is ICMP used for?

**Answer:** ICMP carries network-layer control and error messages, such as destination unreachable and time exceeded.

### Q105. Traceroute

**Question:** How does traceroute discover routers along a path?

**Answer:** It sends probes with increasing TTL values. Each router that decrements TTL to zero sends an ICMP time-exceeded message, revealing one hop.

### Q106. TTL

**Question:** What is the purpose of the IPv4 TTL field?

**Answer:** TTL limits packet lifetime and prevents packets from looping forever.

### Q107. NAT basic

**Question:** What does NAT do?

**Answer:** NAT rewrites IP addresses, often also transport ports, to map private internal endpoints to one or more public external endpoints.

### Q108. NAT table

**Question:** Why does a NAT need a mapping table?

**Answer:** It must remember which internal address and port correspond to each external translated address and port so return traffic can be delivered.

### Q109. NAT benefit

**Question:** Give one benefit and one drawback of NAT.

**Answer:** Benefit: conserves public IPv4 addresses and hides internal addressing. Drawback: breaks end-to-end reachability and complicates inbound connections and some protocols.

### Q110. Routing versus forwarding

**Question:** Distinguish routing and forwarding.

**Answer:** Routing computes paths and forwarding-table entries. Forwarding uses the table to send each packet to the next hop.

### Q111. Shortest path

**Question:** If path A-B-E has cost 8 and path A-B-C-E has cost 7, which path is shorter?

**Answer:** A-B-C-E is shorter because total cost 7 is lower than 8.

### Q112. Optimal substructure

**Question:** What is the optimality property of shortest paths?

**Answer:** Subpaths of a shortest path are also shortest paths between their endpoints.

### Q113. Sink tree

**Question:** What is a sink tree for a destination?

**Answer:** It is the union of shortest paths from all nodes toward that destination.

### Q114. Forwarding table

**Question:** Why does a forwarding table usually store only the next hop rather than the full path?

**Answer:** Each router only needs to decide where to send the packet next; subsequent routers make their own next-hop decisions.

### Q115. Distance-vector initialization

**Question:** How does a distance-vector node initialize distances?

**Answer:** Distance to itself is 0, distance to direct neighbors is the link cost once known, and unknown destinations start at infinity.

### Q116. Distance-vector update

**Question:** In distance-vector routing, how does node A compute a route to destination D through neighbor B?

**Answer:** It adds the cost of link A-B to B's advertised distance to D, then chooses the neighbor with the lowest total cost.

### Q117. Count-to-infinity

**Question:** What is the count-to-infinity problem?

**Answer:** After a failure, nodes may repeatedly believe a neighbor has a route through them, causing route metrics to increase slowly before converging to infinity.

### Q118. Split horizon

**Question:** How does split horizon help distance-vector routing?

**Answer:** A router does not advertise a route back to the neighbor from which it learned that route, reducing certain loops.

### Q119. Poisoned reverse

**Question:** How does poisoned reverse differ from split horizon?

**Answer:** Instead of omitting the route, the router advertises it back with infinite cost, explicitly saying not to use it through this router.

### Q120. Link-state idea

**Question:** What information is flooded in link-state routing?

**Answer:** Each node floods the state and cost of its local links, allowing all nodes to build a topology map.

### Q121. Dijkstra

**Question:** What algorithm is commonly used after link-state flooding to compute shortest paths?

**Answer:** Dijkstra's shortest-path algorithm.

### Q122. Link-state versus distance-vector

**Question:** Give one advantage and one disadvantage of link-state routing compared with distance-vector routing.

**Answer:** Advantage: faster and more informed convergence with full topology. Disadvantage: more flooding overhead and more per-node computation/state.

### Q123. Hierarchical routing

**Question:** Why is hierarchical routing useful in the Internet?

**Answer:** It improves scalability by aggregating routes and letting different organizations manage internal routing separately.

### Q124. Path cost factors

**Question:** Name four possible factors that can be used in a routing cost metric.

**Answer:** Latency, bandwidth, monetary cost, hop count, reliability, or policy.

### Q125. Broadcast not global

**Question:** Why can we not simply broadcast all packets at global scale?

**Answer:** Broadcasting everything everywhere would waste enormous bandwidth and processing resources and would not scale.


## Socket Programming and Concurrent Servers

### Q126. Socket abstraction

**Question:** What is a socket from an application's perspective?

**Answer:** A socket is an endpoint for network communication and, in Unix-like systems, a file descriptor that can be read, written, and closed.

### Q127. Client call order

**Question:** List the usual high-level call sequence for a TCP client.

**Answer:** socket -> connect -> read/write or send/recv -> close.

### Q128. Server call order

**Question:** List the usual high-level call sequence for a TCP server.

**Answer:** socket -> bind -> listen -> accept -> read/write or send/recv on the accepted connection -> close.

### Q129. socket arguments

**Question:** In `socket(AF_INET, SOCK_STREAM, 0)`, what do the arguments mean?

**Answer:** AF_INET selects IPv4, SOCK_STREAM selects TCP byte-stream service, and 0 asks the OS to choose the default protocol for that type.

### Q130. UDP socket type

**Question:** Which socket type is used for UDP?

**Answer:** SOCK_DGRAM.

### Q131. bind

**Question:** What does `bind` do for a server socket?

**Answer:** It associates a socket descriptor with a local socket address, including local IP address and port.

### Q132. listen

**Question:** What does `listen` do?

**Answer:** It converts a bound TCP socket into a listening socket that can accept incoming connection requests.

### Q133. backlog

**Question:** What does the `backlog` argument of `listen` represent?

**Answer:** It suggests how many pending connection requests the kernel may queue before refusing or delaying new ones.

### Q134. accept

**Question:** What does `accept` return?

**Answer:** It returns a new connected file descriptor, often called `connfd`, for communicating with one client.

### Q135. listenfd versus connfd

**Question:** Distinguish `listenfd` and `connfd`.

**Answer:** `listenfd` is the long-lived listening socket used to accept new connections. Each `connfd` is a per-client connected socket used for data exchange.

### Q136. connect

**Question:** What does `connect` do for a TCP client?

**Answer:** It initiates the TCP connection to the server's socket address and returns after the handshake succeeds or fails.

### Q137. read return 0

**Question:** For a TCP socket, what does `read(fd, buf, len)` returning 0 usually mean?

**Answer:** It means the peer has closed its side of the connection and EOF has been reached.

### Q138. partial reads

**Question:** Why must network programs handle partial reads and writes?

**Answer:** TCP is a stream and system calls may transfer fewer bytes than requested, so applications must loop until their message framing requirements are satisfied.

### Q139. Network byte order

**Question:** What byte order is used in Internet protocol headers, and which functions convert to it?

**Answer:** Network byte order is big-endian. `htons` and `htonl` convert host values to network order; `ntohs` and `ntohl` convert back.

### Q140. inet_pton

**Question:** What does `inet_pton` do?

**Answer:** It converts an IP address from presentation text form to binary network form.

### Q141. inet_ntop

**Question:** What does `inet_ntop` do?

**Answer:** It converts an IP address from binary network form to presentation text form.

### Q142. SO_REUSEADDR

**Question:** Why might a server set `SO_REUSEADDR`?

**Answer:** It helps allow rebinding a recently used local address/port, for example after a server restart while old connections remain in TIME_WAIT.

### Q143. File descriptor table

**Question:** What is a Unix file descriptor table?

**Answer:** It is a per-process table mapping small integer descriptors to kernel objects such as files, pipes, sockets, or ttys.

### Q144. Thread-per-connection

**Question:** Give one advantage and one disadvantage of creating one thread per connection.

**Answer:** Advantage: simple blocking I/O style. Disadvantage: many threads can be expensive, and shared state can cause races or deadlocks.

### Q145. Race condition

**Question:** Define race condition in a concurrent server.

**Answer:** A race condition occurs when multiple threads access shared state concurrently and the result depends on the timing or interleaving of operations.

### Q146. Mutex

**Question:** How does a mutex help in a threaded server?

**Answer:** A mutex protects a critical section so only one thread at a time can access shared state.

### Q147. Deadlock

**Question:** Give a common way a mutex can introduce deadlock.

**Answer:** A thread may forget to unlock a mutex, or multiple threads may acquire locks in inconsistent orders and wait forever.

### Q148. select

**Question:** What does `select` allow a server to do?

**Answer:** It lets a program monitor multiple file descriptors and learn which are ready for I/O.

### Q149. poll

**Question:** How is `poll` conceptually similar to `select`?

**Answer:** Both monitor multiple file descriptors for readiness events; `poll` uses an array of `pollfd` structures rather than bitsets.

### Q150. Event loop

**Question:** Why can an event-loop server avoid many threads?

**Answer:** It waits for readiness across many file descriptors and handles whichever sockets are ready, often in one thread.

### Q151. Blocking accept

**Question:** What does it mean that `accept` blocks?

**Answer:** The call waits until a client connection is available or an error/interrupt occurs.

### Q152. Application framing

**Question:** Why does a TCP application often need its own message framing protocol?

**Answer:** TCP does not preserve application message boundaries, so the application needs delimiters, length prefixes, or fixed-size records.

### Q153. UDP server

**Question:** Does a UDP server need `listen` and `accept`?

**Answer:** No. UDP is connectionless; the server typically binds a datagram socket and uses send/receive operations with peer addresses.

### Q154. Port conflict

**Question:** What happens if two TCP servers try to bind the same IP address and port without special socket options?

**Answer:** The second bind typically fails because the address is already in use.

### Q155. Shared descriptors after fork

**Question:** If a server forks a child after `accept`, what must parent and child often do with file descriptors?

**Answer:** They should close descriptors they do not need, such as the child closing `listenfd` or the parent closing the accepted `connfd`, to avoid leaks and delayed connection teardown.


## Application Layer: HTTP, DNS, Caching, and CDNs

### Q156. HTTP basic

**Question:** What is HTTP's basic communication pattern?

**Answer:** HTTP is a request/response protocol between a client, such as a browser, and a server.

### Q157. HTTP transport

**Question:** Which transport protocol and port does traditional HTTP usually use?

**Answer:** HTTP usually runs over TCP port 80; HTTPS runs over TCP port 443.

### Q158. Fetch steps

**Question:** List the major steps to fetch a web page starting from a URL.

**Answer:** Resolve the server name using DNS, establish a TCP connection, send an HTTP request, receive the HTTP response, fetch embedded resources, render, and clean up idle connections.

### Q159. Static versus dynamic

**Question:** Distinguish static and dynamic web pages.

**Answer:** Static pages are served as files. Dynamic pages are generated based on computation or state, such as server-side code, client-side JavaScript, or database access.

### Q160. HTTP methods

**Question:** What do GET, HEAD, POST, PUT, and DELETE generally mean?

**Answer:** GET reads a resource, HEAD reads headers only, POST submits or appends data, PUT stores/replaces a resource, and DELETE removes a resource.

### Q161. Status codes

**Question:** Classify HTTP status-code ranges 2xx, 3xx, 4xx, and 5xx.

**Answer:** 2xx means success, 3xx means redirection or cache-related response, 4xx means client error, and 5xx means server error.

### Q162. 404

**Question:** What does HTTP 404 mean?

**Answer:** The requested resource was not found.

### Q163. 304

**Question:** What does HTTP 304 mean in caching?

**Answer:** The cached copy is still valid; the client can use it without downloading the full resource again.

### Q164. PLT

**Question:** What is page load time?

**Answer:** It is the time from a user's click or request until the page is visible and usable.

### Q165. PLT factors

**Question:** Name three factors that affect page load time.

**Answer:** Page structure and number of resources, content size, RTT, bandwidth, TCP behavior, HTTP connection behavior, caching, and server/CDN placement.

### Q166. HTTP/1.0 issue

**Question:** Why did one TCP connection per resource give poor page load time?

**Answer:** It caused sequential request/response behavior, repeated TCP handshakes, repeated slow start, and poor network utilization for many small resources.

### Q167. Parallel connections

**Question:** How do parallel HTTP connections improve PLT?

**Answer:** They allow several resources to be fetched at the same time, reducing waiting for sequential responses and better utilizing available capacity.

### Q168. Parallel connection drawback

**Question:** Give one drawback of many parallel connections to the same server.

**Answer:** They compete with each other, may create bursts and loss, and may be unfair to other flows.

### Q169. Persistent connections

**Question:** What is the idea of persistent HTTP connections?

**Answer:** Use one TCP connection for multiple HTTP requests and responses to reduce repeated connection setup and slow-start overhead.

### Q170. Pipelining

**Question:** What does HTTP pipelining try to improve?

**Answer:** It sends multiple requests without waiting for each response, reducing idle RTT gaps, although head-of-line blocking can still occur.

### Q171. Caching

**Question:** How does web caching improve performance?

**Answer:** It avoids fetching unchanged content from the origin, reducing latency, bandwidth use, and server load.

### Q172. Cache correctness

**Question:** Why do caches need validation or expiration mechanisms?

**Answer:** They must avoid serving stale content when the origin has changed.

### Q173. Proxy

**Question:** What is a web proxy cache?

**Answer:** It is an intermediary that can fetch, store, and serve web content on behalf of clients.

### Q174. DNS purpose

**Question:** What problem does DNS solve?

**Answer:** DNS maps human-readable domain names to IP addresses and other records.

### Q175. DNS hierarchy

**Question:** Why is DNS hierarchical?

**Answer:** Hierarchy distributes administration and load, enabling scalable name resolution.

### Q176. DNS caching

**Question:** Why is DNS caching useful, and what is the role of TTL?

**Answer:** Caching reduces lookup latency and server load. TTL limits how long a cached record may be used.

### Q177. Recursive resolver

**Question:** What does a recursive DNS resolver do?

**Answer:** It performs the necessary lookups on behalf of a client and returns the final answer, often caching results.

### Q178. CDN

**Question:** What is a CDN's main goal?

**Answer:** A CDN places content replicas near users to reduce latency, improve throughput, and reduce origin load.

### Q179. CDN redirection

**Question:** How can DNS help a CDN direct users to nearby replicas?

**Answer:** The CDN's DNS response can return an IP address for a cache or edge server selected based on location, load, or policy.

### Q180. CDN versus cache

**Question:** How is a CDN different from a simple browser cache?

**Answer:** A browser cache is local to one client. A CDN is a distributed infrastructure of managed replicas serving many clients from many locations.

### Q181. Dynamic content and caching

**Question:** Why is dynamic content harder to cache than static content?

**Answer:** Dynamic content may depend on user identity, time, database state, or computation, so cached responses may not be valid for all users or times.

### Q182. Reduce content size

**Question:** Give two ways to reduce content transfer size for better PLT.

**Answer:** Compress content, use smaller images, minify resources, avoid unused assets, or use efficient formats.

### Q183. Application-layer protocol text

**Question:** Why are text-based protocols like HTTP easy to debug but sometimes less efficient?

**Answer:** They can be read and tested manually, but textual headers and parsing can add overhead compared with compact binary formats.

### Q184. DNS and first page load

**Question:** Why can DNS resolution affect the first load of a page but not every later load?

**Answer:** The first load may need fresh DNS lookups; later loads can use cached DNS answers until TTL expires.

### Q185. Embedded resources

**Question:** Why can a single HTML page require many HTTP requests?

**Answer:** The HTML may reference images, scripts, stylesheets, fonts, and other embedded resources that must be fetched separately.


## Peer-to-Peer Systems

### Q186. P2P motivation

**Question:** What scalability problem motivates peer-to-peer systems?

**Answer:** A single server can become a bandwidth, processing, and availability bottleneck when serving many clients.

### Q187. P2P resource leverage

**Question:** What resources do P2P systems leverage from peers?

**Answer:** Peers can contribute bandwidth, storage, computation, mobility, sensors, or other resources.

### Q188. P2P storage challenge

**Question:** Why is lookup/search a central challenge in P2P storage networks?

**Answer:** Files may be stored anywhere and membership changes due to churn, so the system must find content without relying on a fixed central location.

### Q189. P2P primitives

**Question:** Name four common P2P primitives.

**Answer:** Join, publish, search or lookup, and fetch.

### Q190. Napster design

**Question:** Describe Napster's design for publish, search, and fetch.

**Answer:** Peers publish file lists to a central server. Searches query the central index. Fetches occur directly from the peer storing the file.

### Q191. Napster pros and cons

**Question:** Give one advantage and two disadvantages of Napster's centralized index.

**Answer:** Advantage: simple and efficient search. Disadvantages: central server stores O(N) state, handles search load, and is a single point of failure or control.

### Q192. Gnutella design

**Question:** How does Gnutella search for files?

**Answer:** It uses decentralized query flooding across neighbor peers, often limited by TTL.

### Q193. Gnutella pros and cons

**Question:** Give one advantage and two disadvantages of Gnutella flooding.

**Answer:** Advantage: no central index. Disadvantages: high message overhead and incomplete search if TTL is limited.

### Q194. TTL in flooding

**Question:** Why is TTL used in Gnutella-style flooding?

**Answer:** TTL bounds the flood to prevent infinite propagation and reduce network overhead.

### Q195. KaZaA hierarchy

**Question:** What problem do supernodes in KaZaA-style systems try to solve?

**Answer:** They reduce search overhead by organizing peers hierarchically, while still avoiding one global central index.

### Q196. BitTorrent pieces

**Question:** Why does BitTorrent split a file into pieces?

**Answer:** Pieces enable parallel downloads from many peers and make it easier to exchange partial progress.

### Q197. Rarest first

**Question:** What is the purpose of rarest-first piece selection in BitTorrent?

**Answer:** It increases availability of scarce pieces and reduces the chance that a piece disappears from the swarm.

### Q198. Tit-for-tat

**Question:** What is the purpose of tit-for-tat in BitTorrent?

**Answer:** It encourages peers to upload by preferentially serving peers that also provide good upload service.

### Q199. Optimistic unchoke

**Question:** Why does BitTorrent use optimistic unchoke?

**Answer:** It discovers potentially better peers and prevents new or unlucky peers from permanent starvation.

### Q200. DHT

**Question:** What is a distributed hash table?

**Answer:** A DHT is a decentralized key-value lookup system that maps keys to responsible nodes using hashing and structured routing.

### Q201. Chord IDs

**Question:** In Chord, how are node IDs and key IDs determined?

**Answer:** They are hashed into the same circular identifier space using the same hash function.

### Q202. Chord successor

**Question:** In Chord with node IDs 1, 4, 8, and 12 on a 4-bit ring, which node stores key 9?

**Answer:** The key is stored at its successor: the first node ID >= 9 on the ring, which is 12.

### Q203. Chord wraparound

**Question:** Using the same Chord ring, which node stores key 14?

**Answer:** The successor wraps around to the smallest node ID, so node 1 stores key 14.

### Q204. Chord finger

**Question:** What is the main purpose of finger tables in Chord?

**Answer:** They let lookups skip around the identifier ring, reducing lookup cost to logarithmic scale under normal conditions.

### Q205. Churn

**Question:** What is churn, and why is it hard for P2P systems?

**Answer:** Churn is frequent peer join and leave behavior. It makes membership, routing, and content availability unstable.

### Q206. Client/server versus P2P distribution

**Question:** A server has upload capacity 100 Mbps and 1000 clients each need a file. Why can P2P scale better?

**Answer:** In client/server, the server's upload is the bottleneck. In P2P, clients that receive pieces can upload them to others, adding aggregate upload capacity.

### Q207. Search expressiveness

**Question:** Why is supporting rich search harder than exact key lookup in P2P?

**Answer:** Exact key lookup can use hashing. Rich search such as keywords, attributes, or full text may require indexes, flooding, or more complex distributed data structures.


## Remote Procedure Call

### Q208. RPC goal

**Question:** What is the programming goal of RPC?

**Answer:** To make client-server communication easier by making a remote operation look similar to a procedure call, while hiding much socket-level detail.

### Q209. RPC layer

**Question:** Where does the RPC layer sit conceptually?

**Answer:** It sits above sockets/transport and below application logic, providing request/response procedure-call abstractions.

### Q210. Stubs

**Question:** What are client and server stubs in RPC?

**Answer:** The client stub marshals arguments and sends requests. The server stub unmarshals arguments, calls the real procedure, marshals results, and sends replies.

### Q211. Marshalling

**Question:** What is marshalling?

**Answer:** Marshalling converts in-memory arguments or results into a byte representation suitable for network transmission.

### Q212. Unmarshalling

**Question:** What is unmarshalling?

**Answer:** Unmarshalling reconstructs arguments or results from the received byte representation.

### Q213. IDL

**Question:** What is the purpose of an interface definition language in RPC systems?

**Answer:** It specifies remote procedure names, argument types, and return types so stubs can be generated consistently across languages.

### Q214. RPC not local

**Question:** Give three reasons an RPC is not exactly like a local procedure call.

**Answer:** RPC has network latency, partial failures, retries and duplicates, marshalling overhead, security issues, and different machine/language representations.

### Q215. At-least-once

**Question:** What is at-least-once RPC semantics?

**Answer:** The system retries until the operation executes one or more times or until failure is reported; duplicates are possible.

### Q216. At-most-once

**Question:** What is at-most-once RPC semantics?

**Answer:** The system ensures the operation is executed no more than once, usually using unique request IDs and duplicate suppression; it may execute zero times if failure occurs.

### Q217. Exactly-once

**Question:** Why is exactly-once RPC difficult or impossible to guarantee in the strongest sense?

**Answer:** Crashes, lost replies, retries, and external side effects make it hard to know whether an operation happened exactly once without durable coordination, and some side effects cannot be undone.

### Q218. Idempotence

**Question:** What is an idempotent operation?

**Answer:** An operation is idempotent if executing it multiple times has the same effect as executing it once.

### Q219. Read semantics

**Question:** Would you use at-least-once or at-most-once for reading a key from a data store? Explain.

**Answer:** At-least-once is often acceptable because repeated reads normally do not change state.

### Q220. Flight booking

**Question:** Would you use at-least-once or at-most-once for booking a flight? Explain.

**Answer:** At-most-once or stronger application-level transaction logic is needed because duplicate execution could book or charge twice.

### Q221. Duplicate suppression

**Question:** How do request IDs help implement at-most-once RPC?

**Answer:** The server can remember completed request IDs and return a cached result rather than executing a duplicate request again.

### Q222. Result cache

**Question:** Why might an at-most-once RPC server cache replies?

**Answer:** If the client retries after a lost reply, the server can resend the same result without re-executing the operation.

### Q223. Lost request

**Question:** Under at-most-once semantics, what can happen if the request is lost and no retry succeeds?

**Answer:** The operation may execute zero times and the client may receive an error or timeout.

### Q224. Lost reply

**Question:** What is the ambiguity caused by a lost RPC reply?

**Answer:** The client may not know whether the server executed the operation and the reply was lost, or whether the operation never executed.

### Q225. Timeouts

**Question:** Why do RPC clients use timeouts?

**Answer:** Because networks and servers can fail or delay indefinitely; timeouts let clients retry or report failure.

### Q226. Language heterogeneity

**Question:** How does RPC support a Python client calling a C++ server?

**Answer:** The IDL and marshalling format define a common wire representation independent of language-specific memory layouts.

### Q227. Side effects

**Question:** Why are external side effects hard for retry-based RPC?

**Answer:** The system may not be able to observe, undo, or deduplicate actions performed outside the server's own durable state, such as charging a credit card.

### Q228. Batching

**Question:** Why might an RPC system batch small calls?

**Answer:** Batching reduces per-call overhead and network round trips, though it can increase latency for individual calls.

### Q229. RPC transparency limit

**Question:** Should programmers completely ignore the network when using RPC?

**Answer:** No. RPC simplifies programming, but programmers must still reason about latency, failures, retries, security, and operation semantics.


## Distributed Storage: Dynamo

### Q230. Dynamo motivation

**Question:** What type of workload motivated Dynamo-style storage at Amazon?

**Answer:** Highly available, low-latency key-value workloads such as shopping carts and other stateful services that do not need full SQL transactions.

### Q231. Dynamo goals

**Question:** Name four design goals or requirements of Dynamo.

**Answer:** Highly available writes, low request-response latency, incremental scalability, replication under failures, and comprehensible conflict resolution.

### Q232. Availability versus consistency

**Question:** Why can high availability during failures imply conflicts?

**Answer:** If the system accepts writes on different replicas during partitions or failures, concurrent versions may be created and later need reconciliation.

### Q233. Hash partitioning problem

**Question:** Why is `hash(key) % N` problematic when the number of machines changes?

**Answer:** Changing N can remap many or most keys, causing large-scale data movement.

### Q234. Consistent hashing

**Question:** What is the main advantage of consistent hashing when adding or removing a node?

**Answer:** Only keys in local portions of the hash ring need to move, rather than remapping nearly all keys.

### Q235. Ring placement

**Question:** In consistent hashing, how is the node responsible for a key usually chosen?

**Answer:** Hash the key onto the ring and choose the first node clockwise at or after the key's position.

### Q236. Virtual nodes

**Question:** Why does Dynamo use virtual nodes?

**Answer:** Virtual nodes improve load balancing, support heterogeneous node capacity, and spread recovery or migration across many physical nodes.

### Q237. Replication factor

**Question:** What does replication factor N mean in Dynamo quorum notation?

**Answer:** N is the number of replicas that should store each key.

### Q238. Read quorum

**Question:** What does R mean in Dynamo quorum notation?

**Answer:** R is the number of replicas that must reply to a read before it is considered successful.

### Q239. Write quorum

**Question:** What does W mean in Dynamo quorum notation?

**Answer:** W is the number of replicas that must acknowledge a write before it is considered successful.

### Q240. Quorum overlap

**Question:** If N = 3, R = 2, and W = 2, do read and write quorums necessarily overlap?

**Answer:** Yes. Since R + W = 4 > N = 3, any read quorum and write quorum share at least one replica.

### Q241. No quorum overlap

**Question:** If N = 3, R = 1, and W = 1, do read and write quorums necessarily overlap?

**Answer:** No. R + W = 2 <= 3, so a read can miss the replica that accepted the latest write.

### Q242. Latency tradeoff

**Question:** How does increasing R affect reads?

**Answer:** It may improve the chance of seeing a recent value, but it increases read latency and reduces read availability because more replicas must respond.

### Q243. Write availability tradeoff

**Question:** How does increasing W affect writes?

**Answer:** It improves durability/consistency chances but increases write latency and reduces write availability during failures.

### Q244. Sloppy quorum

**Question:** What is the idea of sloppy quorum?

**Answer:** If some preferred replicas are unavailable, the system can write to other reachable nodes temporarily to maintain availability.

### Q245. Hinted handoff

**Question:** What is hinted handoff used for?

**Answer:** A temporary node stores a hint and later hands the data back to the intended replica when it recovers.

### Q246. Conflict detection

**Question:** Why does Dynamo need version metadata such as vector-clock-like context?

**Answer:** It helps detect whether one version supersedes another or whether versions are concurrent and need application-level reconciliation.

### Q247. Shopping cart reconciliation

**Question:** Why is application-level conflict resolution reasonable for a shopping cart?

**Answer:** The application can merge item sets or otherwise apply domain-specific rules, often preserving user intent better than blind overwrites.

### Q248. Last-write-wins risk

**Question:** What is a risk of last-write-wins conflict resolution?

**Answer:** It may discard a concurrent update that should have been preserved.

### Q249. Coordinator

**Question:** In a Dynamo-style operation, what can a coordinator node do?

**Answer:** It receives the client request, determines the replica set, sends requests to replicas, waits for R or W responses, and returns the result.

### Q250. Preference list

**Question:** What is a preference list in Dynamo?

**Answer:** It is the ordered set of nodes responsible for storing replicas of a key.

### Q251. Incremental scalability

**Question:** What does incremental scalability mean?

**Answer:** The system can add or remove nodes with limited disruption and without global reconfiguration.

### Q252. 99.9 percentile latency

**Question:** Why might Dynamo focus on 99.9th percentile latency instead of only average latency?

**Answer:** User-facing services care about tail latency because a small fraction of slow requests can still affect many users and composed services.

### Q253. Eventual consistency

**Question:** What does eventual consistency mean?

**Answer:** If no new updates occur and replicas can communicate, they should eventually converge to the same value.

### Q254. Dynamo versus SQL

**Question:** Why might Dynamo avoid full SQL-style transactions?

**Answer:** The target workloads value high availability, low latency, and scalability more than complex relational queries and strong transaction guarantees.

### Q255. Read repair

**Question:** What is read repair?

**Answer:** During reads, the coordinator can detect stale replicas and update them with newer versions.

### Q256. Anti-entropy

**Question:** What is anti-entropy in replicated storage?

**Answer:** Background synchronization among replicas to detect and repair divergence.

### Q257. Consistent hashing movement

**Question:** A consistent-hash ring has 9 equal nodes. Adding one equal node ideally moves about what fraction of keys to the new node?

**Answer:** About 1 / 10 of the keys, assuming balanced placement.


## Distributed Storage: GFS and HDFS

### Q258. Scale out

**Question:** Why do GFS and HDFS scale out instead of scaling up?

**Answer:** Many commodity machines provide high aggregate storage and I/O bandwidth at lower cost, while also enabling parallel processing.

### Q259. I/O bottleneck

**Question:** A single disk scans 100 Tb at 3 Gbps. Approximately how long does it take?

**Answer:** 100 Tb / 3 Gbps = 33,333 s, or about 9.26 hours.

### Q260. Aggregate I/O

**Question:** If 1000 disks each scan at 3 Gbps, what is the aggregate scan bandwidth?

**Answer:** 1000 x 3 Gbps = 3 Tbps.

### Q261. Parallel scan

**Question:** At 3 Tbps aggregate bandwidth, how long to scan 100 Tb?

**Answer:** 100 Tb / 3 Tbps = about 33.3 seconds.

### Q262. Failure motivation

**Question:** Why must large-scale storage systems expect failures?

**Answer:** With thousands of commodity machines, disks, networks, racks, and power systems, component failures are common events rather than rare exceptions.

### Q263. GFS workload

**Question:** What workload assumptions influenced GFS design?

**Answer:** Large files, streaming reads, sequential appends, write-once/read-many patterns, and high throughput rather than low-latency random access.

### Q264. Not for small random queries

**Question:** Why is GFS/HDFS not ideal for many low-latency random small-object queries?

**Answer:** Large blocks, metadata access, and batch-oriented throughput design make it inefficient for small random operations requiring sub-second latency.

### Q265. Chunk or block

**Question:** What is a chunk in GFS or a block in HDFS?

**Answer:** It is a large fixed-size unit into which files are split and stored across chunkservers or datanodes.

### Q266. Large chunks

**Question:** Give two advantages of large chunk/block sizes.

**Answer:** They reduce metadata overhead and amortize seek and setup costs over large sequential transfers.

### Q267. Large chunk drawback

**Question:** Give one drawback of large chunks or blocks.

**Answer:** Small files can waste space and metadata assumptions; a popular small set of chunks can become hot.

### Q268. Master role

**Question:** What does the GFS master or HDFS namenode manage?

**Answer:** It manages metadata such as namespace, file-to-chunk/block mappings, replica locations, and placement decisions.

### Q269. Data path

**Question:** Why is the master not a data-path bottleneck?

**Answer:** Clients ask the master for metadata but transfer data directly to and from chunkservers or datanodes.

### Q270. Replication

**Question:** Why do GFS/HDFS replicate blocks?

**Answer:** Replication provides fault tolerance, availability, and sometimes read throughput through multiple copies.

### Q271. Default replication

**Question:** What is a common HDFS replication factor?

**Answer:** Three replicas is a common default.

### Q272. Rack awareness

**Question:** Why place replicas across racks?

**Answer:** It protects against rack-level failures and can improve availability, while balancing cross-rack bandwidth cost.

### Q273. Primary lease

**Question:** What is the purpose of a primary lease in GFS writes?

**Answer:** The master grants a lease to one replica to order mutations consistently among replicas for a chunk.

### Q274. Record append

**Question:** Why is record append useful in GFS?

**Answer:** It lets multiple clients append concurrently while GFS chooses the offset and preserves append atomicity properties for records.

### Q275. HDFS write pipeline

**Question:** At a high level, how are replicated HDFS writes often pipelined?

**Answer:** The client sends data to one datanode, which forwards it to the next replica, and so on, with acknowledgments returning back along the pipeline.

### Q276. Metadata bottleneck

**Question:** Why can a single namenode be a scalability concern?

**Answer:** All metadata operations depend on it, so memory capacity, request rate, and availability of the master become important constraints.

### Q277. File survival 1

**Question:** A file has 1000 blocks, each with 3 independent replicas. Each machine fails during the month with probability 0.01. Assuming no repair and independent placement, what is the approximate probability the file survives?

**Answer:** A block is lost with probability 0.01^3 = 0.000001. File survival is (1 - 0.000001)^1000, about 0.999, very close to 1.

### Q278. File survival 2

**Question:** If each block has 2 replicas and machine failure probability is 0.02, what is the probability a single block is lost?

**Answer:** 0.02^2 = 0.0004.

### Q279. File survival 3

**Question:** With 500 blocks, 2 replicas per block, and per-machine failure probability 0.02, approximate file survival probability.

**Answer:** Single-block survival is 1 - 0.0004 = 0.9996. File survival is 0.9996^500, about 0.819.

### Q280. Throughput focus

**Question:** Why are GFS/HDFS good for batch analytics?

**Answer:** They provide high aggregate sequential I/O bandwidth and colocate large data blocks with compute across many machines.

### Q281. Data locality

**Question:** What is data locality in HDFS-style processing?

**Answer:** Scheduling computation near the machines that store the needed data to reduce network traffic.

### Q282. Master metadata memory

**Question:** Why does large block size reduce master memory pressure?

**Answer:** Fewer blocks per file means fewer metadata entries for the master to store and manage.

### Q283. Client cache metadata

**Question:** Why may clients cache chunk locations?

**Answer:** Caching avoids repeated master lookups for subsequent accesses to the same chunks.

### Q284. Heartbeat

**Question:** What are heartbeats from datanodes or chunkservers used for?

**Answer:** They report liveness and sometimes storage status to the master.

### Q285. Re-replication

**Question:** What should the system do when a block replica is lost?

**Answer:** It should create a new replica on another healthy node to restore the desired replication factor.

### Q286. GFS versus Dynamo

**Question:** Which is more suitable for large sequential log processing, GFS/HDFS or Dynamo?

**Answer:** GFS/HDFS, because the workload is large, sequential, and batch-oriented.

### Q287. Dynamo versus HDFS

**Question:** Which is more suitable for interactive sub-second key-value access, Dynamo or HDFS?

**Answer:** Dynamo, because it is designed for low-latency highly available key-value access.


## Time and Logical Clocks in Distributed Systems

### Q288. Clock drift

**Question:** Why do physical clocks on different machines drift?

**Answer:** Quartz oscillators vary with temperature, age, vibration, radiation, and manufacturing differences.

### Q289. Clock synchronization difficulty

**Question:** Give two reasons Internet clock synchronization is hard.

**Answer:** Message delays are variable and asynchronous, and messages can be lost or delayed unpredictably.

### Q290. UTC source

**Question:** How can machines obtain accurate wall-clock time in principle?

**Answer:** They can use timing signals such as GPS or other UTC sources, though this is not always practical for every machine.

### Q291. Simple time RPC problem

**Question:** Why is simply asking a time server for the time insufficient?

**Answer:** The server's reply is delayed by unknown network latency, so the received time is already stale.

### Q292. Cristian variables

**Question:** In Cristian's algorithm, what are T1, T2, T3, and T4?

**Answer:** T1 is client send time, T2 is server receive time, T3 is server send time, and T4 is client receive time.

### Q293. Cristian RTT

**Question:** Given T1=100, T2=150, T3=170, and T4=240, compute the network delay sample delta.

**Answer:** delta = (T4 - T1) - (T3 - T2) = (240 - 100) - (170 - 150) = 140 - 20 = 120.

### Q294. Cristian setting

**Question:** Using the previous values and symmetric delay assumption, to what time should the client set its clock?

**Answer:** Set to T3 + delta/2 = 170 + 60 = 230.

### Q295. NTP accuracy

**Question:** Why might NTP-level synchronization still be inadequate for some distributed systems?

**Answer:** Clocks are never exactly synchronized, and many systems need to reason about event order rather than wall-clock time.

### Q296. Logical clock motivation

**Question:** What is the main idea of logical clocks?

**Answer:** Ignore precise physical time and capture ordering relationships among events.

### Q297. Happens-before rules

**Question:** State the basic Lamport happens-before rules.

**Answer:** Events in the same process are ordered by program order. A send event happens before its corresponding receive. The relation is transitive.

### Q298. Concurrency

**Question:** When are two events concurrent in the happens-before sense?

**Answer:** Neither event happens before the other.

### Q299. Lamport update

**Question:** How is a Lamport clock updated on local events and message receives?

**Answer:** Increment on local or send events. On receive, set the clock to max(local clock, message timestamp) + 1.

### Q300. Lamport example

**Question:** Process P has Lamport clock 5 and receives a message with timestamp 9. What is P's new clock?

**Answer:** max(5, 9) + 1 = 10.

### Q301. Lamport send

**Question:** If a process clock is 7 just before sending a message and it increments on send, what timestamp is attached?

**Answer:** 8.

### Q302. Lamport limitation

**Question:** If event a has Lamport timestamp 3 and event b has timestamp 7, can we conclude a happened before b?

**Answer:** No. Lamport timestamps respect happens-before, but timestamp order alone does not prove causality.

### Q303. Vector clock idea

**Question:** What extra information does a vector clock keep compared with a Lamport clock?

**Answer:** It keeps one counter per process, allowing detection of causality and concurrency.

### Q304. Vector comparison

**Question:** How do you decide if vector timestamp A happens before B?

**Answer:** A happens before B if A[i] <= B[i] for all i and A[j] < B[j] for at least one component j.

### Q305. Vector concurrent 1

**Question:** Are vector timestamps [2,1,0] and [1,2,0] causally ordered?

**Answer:** No. Neither is componentwise <= the other, so they are concurrent.

### Q306. Vector ordered

**Question:** Do vector timestamps [1,2,0] and [1,3,2] show a happens-before relation?

**Answer:** Yes. [1,2,0] <= [1,3,2] and at least one component is smaller, so the first happens before the second.

### Q307. Vector receive

**Question:** Process 2 has vector [3,4,1] and receives a message with vector [5,2,2]. After taking componentwise max and incrementing its own component, what is the new vector if process indices are 1-based and this is process 2?

**Answer:** Componentwise max is [5,4,2]. Increment process 2's component: [5,5,2].

### Q308. Replica ordering

**Question:** Why can concurrent updates cause inconsistent replicas?

**Answer:** If replicas apply concurrent operations in different orders and the operations do not commute, they can reach different states.

### Q309. Total order

**Question:** What is the purpose of totally ordered multicast in replicated systems?

**Answer:** To ensure all replicas deliver and apply updates in the same global order.

### Q310. Physical versus logical

**Question:** Give one situation where physical time is useful and one where logical time is better.

**Answer:** Physical time is useful for deadlines or real-time timestamps. Logical time is better for reasoning about causality and event order.

### Q311. Make example

**Question:** Why can unsynchronized clocks break a distributed edit-compile workflow using `make`?

**Answer:** If file timestamps from different machines are inconsistent, `make` may believe an object file is newer than the source and skip needed compilation.

### Q312. Probability never zero

**Question:** Why can the probability of strange clock behavior never be zero in an asynchronous distributed system?

**Answer:** Because communication delay and failure cannot be perfectly bounded or eliminated, so clocks cannot be kept perfectly synchronized.

### Q313. Vector cost

**Question:** What is a cost of vector clocks compared with Lamport clocks?

**Answer:** Vector clocks require O(number of processes) metadata per timestamp instead of a single integer.

### Q314. Lamport total order

**Question:** How can Lamport timestamps be extended to produce a deterministic total order?

**Answer:** Break ties using process IDs or another fixed unique identifier after comparing Lamport timestamps.

### Q315. Clock adjustment

**Question:** Why should a synchronized physical clock often be slewed rather than set backwards abruptly?

**Answer:** Moving a clock backwards can break software assumptions about monotonic time; gradual adjustment avoids non-monotonic jumps.

### Q316. Causal delivery

**Question:** What does causal delivery ensure?

**Answer:** If message or event a causally precedes b, then processes deliver or apply a before b.


## Parallelism and Collective Communication

### Q317. Scale-out compute

**Question:** What is the basic idea of scale-out parallel data processing?

**Answer:** Split work across many commodity machines or workers, process pieces in parallel, and combine results.

### Q318. Dataflow graph

**Question:** What is a dataflow graph?

**Answer:** A directed acyclic graph where vertices are operations and edges represent data flow and dependencies.

### Q319. Relational dataflow

**Question:** Give an example of a relational dataflow operation.

**Answer:** Selection, projection, join, union, or aggregation.

### Q320. ML dataflow

**Question:** Give an example of an ML dataflow operation.

**Answer:** Matrix multiplication, convolution, ReLU, addition, or softmax.

### Q321. Task parallelism

**Question:** What is task parallelism?

**Answer:** Different tasks in a workflow are scheduled across workers, respecting dependency constraints.

### Q322. Data parallelism

**Question:** What is data parallelism in general data processing?

**Answer:** Partition the input data across workers and run similar computation on different partitions.

### Q323. Critical path

**Question:** Why can a parallel program's runtime not be less than the critical path length?

**Answer:** Tasks on the critical path depend on each other and must execute sequentially in that order.

### Q324. Speedup

**Question:** Sequential time is 60 s and parallel time is 15 s. What is speedup?

**Answer:** Speedup = 60 / 15 = 4.

### Q325. Workflow speedup

**Question:** A workflow has total task work 46 and critical path length 22. With enough workers and no scheduling overhead, what is the maximum possible speedup?

**Answer:** 46 / 22 = 2.09 approximately.

### Q326. Worker lower bound

**Question:** Total work is 100 s and there are 4 identical workers. What lower bound does work impose on parallel runtime?

**Answer:** 100 / 4 = 25 s.

### Q327. Runtime lower bound

**Question:** Total work is 100 s, critical path is 40 s, and there are 4 workers. What is a lower bound on runtime?

**Answer:** max(100/4, 40) = max(25, 40) = 40 s.

### Q328. Collective primitive list

**Question:** Name seven collective communication primitives covered in CSC4303.

**Answer:** Broadcast, reduce, scatter, gather, allgather, reduce-scatter, and allreduce.

### Q329. Broadcast

**Question:** What is broadcast?

**Answer:** One node starts with a message and all nodes end with that same message.

### Q330. Reduce

**Question:** What is reduce?

**Answer:** All nodes start with values; one node ends with the aggregation, such as sum, of all values.

### Q331. Scatter

**Question:** What is scatter?

**Answer:** One node starts with multiple chunks and distributes one chunk to each node.

### Q332. Gather

**Question:** What is gather?

**Answer:** Each node starts with a chunk and one root collects all chunks.

### Q333. Allgather

**Question:** What is allgather?

**Answer:** Each node starts with a chunk and all nodes end with all chunks.

### Q334. Reduce-scatter

**Question:** What is reduce-scatter?

**Answer:** Values are reduced across nodes and the reduced result is partitioned so each node receives one part.

### Q335. Allreduce

**Question:** What is allreduce?

**Answer:** All nodes contribute values and all nodes receive the final reduced value or vector.

### Q336. Communication cost model

**Question:** If sending a message of length n costs alpha + n beta, what do alpha and beta represent?

**Answer:** alpha is startup latency; beta is per-byte or per-unit transmission cost.

### Q337. MST broadcast cost

**Question:** For p nodes and message length n, what is the common tree broadcast cost when p is a power of two?

**Answer:** log2(p) x (alpha + n beta).

### Q338. MST broadcast numeric

**Question:** Let p=8, alpha=2 ms, beta*n=5 ms. What is tree broadcast cost?

**Answer:** log2(8) = 3 steps. Cost = 3 x (2 + 5) = 21 ms.

### Q339. Tree reduce cost

**Question:** What is a simple tree reduce cost expression, ignoring computation overhead?

**Answer:** log2(p) x (alpha + n beta), similar to tree broadcast, plus any reduction computation cost.

### Q340. Small-message algorithm

**Question:** Why are tree or MST algorithms often preferred for small messages?

**Answer:** They reduce the number of sequential startup-latency steps to O(log p), which matters when alpha dominates.

### Q341. Large-message algorithm

**Question:** Why are ring algorithms often preferred for large messages?

**Answer:** They split data into chunks and keep all links/nodes busy, improving bandwidth utilization when n beta dominates.

### Q342. Ring allreduce cost

**Question:** Give a common high-level cost for ring allreduce with p nodes and message length n.

**Answer:** A common model is about 2(p-1) alpha + 2(p-1)n beta / p, for reduce-scatter plus allgather phases.

### Q343. Ring allreduce numeric

**Question:** For ring allreduce with p=4, alpha=1 ms, and n beta=12 ms, estimate cost using 2(p-1)alpha + 2(p-1)n beta/p.

**Answer:** 2(3)(1) + 2(3)(12)/4 = 6 + 18 = 24 ms.

### Q344. Allgather by gather plus broadcast

**Question:** How can allgather be implemented using gather and broadcast?

**Answer:** First gather all chunks at a root; then broadcast the concatenated full data to all nodes.

### Q345. Allgather cost from sample

**Question:** Using the CSC4303 sample-style formula, if gather costs log(p)alpha + (p-1)n beta/p and broadcast costs log(p)(alpha + n beta), what is allgather cost?

**Answer:** 2log(p)alpha + log(p)n beta + (p-1)n beta/p.

### Q346. Allgather numeric

**Question:** Using the previous formula with p=8, alpha=1, and n beta=4, what is the allgather cost?

**Answer:** log2(8)=3. Cost = 2*3*1 + 3*4 + (7*4)/8 = 6 + 12 + 3.5 = 21.5 time units.

### Q347. Reduce plus broadcast

**Question:** Which collective can be implemented as reduce followed by broadcast?

**Answer:** Allreduce.

### Q348. Scatter plus allgather

**Question:** Which ring allreduce phases are often used for large vectors?

**Answer:** Reduce-scatter followed by allgather.

### Q349. Root bottleneck

**Question:** Why can naive gather or parameter-server-like aggregation bottleneck at the root?

**Answer:** All workers send to one node, so the root's network and processing capacity limit throughput.

### Q350. Balanced tree

**Question:** Why does a balanced tree reduce latency compared with a chain broadcast?

**Answer:** A balanced tree doubles the number of informed nodes each step, needing O(log p) steps instead of O(p).

### Q351. Chain broadcast

**Question:** If p=16 nodes use a chain broadcast, how many sequential sends are needed?

**Answer:** 15 sequential sends.

### Q352. Tree steps

**Question:** If p=16 nodes use a balanced binary-tree broadcast, how many rounds are needed?

**Answer:** log2(16) = 4 rounds.

### Q353. Scatter identification

**Question:** A root has chunks A, B, C, D and after the primitive each of four nodes has exactly one distinct chunk. Which primitive is this?

**Answer:** Scatter.

### Q354. Gather identification

**Question:** Each of four nodes has one chunk and after the primitive the root has all four chunks. Which primitive is this?

**Answer:** Gather.

### Q355. Allreduce identification

**Question:** Each node starts with a vector, and every node ends with the elementwise sum of all vectors. Which primitive is this?

**Answer:** Allreduce.

### Q356. Data dependency

**Question:** In a dataflow graph, what does an edge from task A to task B mean?

**Answer:** B depends on data produced by A, so B cannot run until the required output from A is available.

### Q357. Load balance

**Question:** Why is load balance important in parallel processing?

**Answer:** If work is unevenly distributed, slow workers become stragglers and determine job completion time.


## Distributed ML, LLM Systems, and Data Center Networking

### Q358. ML training stages

**Question:** Name the three main stages of iterative neural-network training.

**Answer:** Forward propagation, backward propagation, and weight update.

### Q359. Forward propagation

**Question:** What happens during forward propagation?

**Answer:** The model applies operators to a batch of inputs to produce predictions and loss values.

### Q360. Backward propagation

**Question:** What happens during backward propagation?

**Answer:** The model is traversed in reverse to compute gradients for trainable weights.

### Q361. Weight update

**Question:** What happens during the weight-update stage?

**Answer:** The optimizer uses gradients and the loss objective to update model parameters.

### Q362. Why distributed ML

**Question:** Why distribute ML training across multiple workers or GPUs?

**Answer:** To reduce end-to-end training time and to train models or batches too large for one device.

### Q363. Data-parallel training

**Question:** Describe data-parallel training.

**Answer:** Each worker holds a copy of the model, processes a different mini-batch, computes gradients, aggregates gradients across workers, and updates the model.

### Q364. Model parallelism

**Question:** Describe model parallelism.

**Answer:** The model is partitioned across devices, for example by layers, pipeline stages, or tensor shards.

### Q365. Data versus model parallelism

**Question:** When is model parallelism needed instead of only data parallelism?

**Answer:** When the model or intermediate activations are too large to fit or compute efficiently on one device.

### Q366. Tensor parallelism

**Question:** What is tensor parallelism?

**Answer:** Splitting large tensor operations or parameters across multiple devices so they cooperate on the same layer/operator.

### Q367. Pipeline parallelism

**Question:** What is pipeline parallelism?

**Answer:** Splitting model layers into stages on different devices and processing microbatches through the stages like a pipeline.

### Q368. Parameter server

**Question:** What are the roles in a parameter-server framework?

**Answer:** Workers compute gradients on data partitions; parameter servers receive gradients, aggregate/update parameters, and send updated results back.

### Q369. Parameter server bottleneck

**Question:** Why can a parameter server become a bottleneck?

**Answer:** Many workers communicate with it, concentrating network traffic, memory bandwidth, and computation at the server.

### Q370. Naive allreduce

**Question:** Why is naive allreduce through one root similar to a parameter-server bottleneck?

**Answer:** All data flows through one node, making that node's bandwidth and processing the limiting resource.

### Q371. Ring allreduce for ML

**Question:** Why is ring allreduce useful in data-parallel training?

**Answer:** It aggregates gradients without a central server and balances communication across workers, especially for large gradient vectors.

### Q372. Gradient aggregation

**Question:** Why must data-parallel workers aggregate gradients?

**Answer:** To compute an update equivalent to training on the combined batch and keep model replicas synchronized.

### Q373. Synchronous training

**Question:** What is a straggler problem in synchronous distributed training?

**Answer:** All workers may wait for the slowest worker before completing a step, reducing overall throughput.

### Q374. ML model size

**Question:** Why do larger models make distributed systems more important?

**Answer:** They require more memory, more compute, longer training time, and more communication for parameters and activations.

### Q375. ML serving

**Question:** How is ML serving different from ML training?

**Answer:** Serving runs inference for user requests under latency and throughput constraints; training repeatedly computes gradients and updates parameters.

### Q376. LLM prefill

**Question:** What is the prefill phase in LLM inference?

**Answer:** The model processes the input prompt and builds initial key-value cache state, often using substantial compute.

### Q377. LLM decoding

**Question:** What is the decoding phase in LLM inference?

**Answer:** The model generates output tokens one at a time, repeatedly reading and updating KV cache.

### Q378. TTFT

**Question:** What does TTFT mean?

**Answer:** Time to first token: the latency until the first generated token is produced.

### Q379. TPOT

**Question:** What does TPOT mean?

**Answer:** Time per output token: the per-token latency during decoding after the first token.

### Q380. Prefill versus decoding

**Question:** Why can prefill and decoding interfere when batched together?

**Answer:** Prefill can be compute-heavy while decoding can be memory/KV-cache heavy; mixing them may hurt TTFT or TPOT due to resource contention.

### Q381. Continuous batching

**Question:** What is continuous batching in LLM serving?

**Answer:** The scheduler adds new requests and removes completed requests at iteration or token boundaries to keep GPUs utilized.

### Q382. Continuous batching tradeoff

**Question:** Give one benefit and one cost of continuous batching.

**Answer:** Benefit: higher GPU utilization and throughput. Cost: more complex scheduling and possible interference among requests.

### Q383. DistServe idea

**Question:** What is the basic idea of disaggregating prefill and decoding?

**Answer:** Run prefill and decoding on separate resources so each phase can be optimized for its own bottleneck and service-level objective.

### Q384. Disaggregation cost

**Question:** What cost does prefill/decoding disaggregation introduce?

**Answer:** KV-cache or intermediate state must be transferred, and scheduling/resource allocation becomes more complex.

### Q385. Goodput

**Question:** In serving systems, what is goodput?

**Answer:** Useful request throughput that meets specified latency or service-level objectives, not merely raw completed requests per second.

### Q386. Data-center scale

**Question:** Name three characteristics of modern cloud data centers.

**Answer:** They may contain hundreds of thousands of servers, cost billions of dollars, and be geographically distributed.

### Q387. Data-center cost

**Question:** Why is network cost significant even if servers dominate total cost?

**Answer:** Large data centers need many switches, links, transceivers, and transit connections; network performance also affects utilization of expensive servers and GPUs.

### Q388. Resource stranding

**Question:** What is resource stranding in servers?

**Answer:** An application may exhaust one resource such as CPU, memory, disk, or network while other resources on the same machine remain underused.

### Q389. Agility

**Question:** What does 'any service, any server' mean in data centers?

**Answer:** Servers form a large fungible pool, and services can be dynamically placed, expanded, or contracted across machines.

### Q390. VM

**Question:** What is a virtual machine in the cloud context?

**Answer:** A VM runs a guest OS on virtual hardware provided by a hypervisor, giving isolation between tenants or workloads.

### Q391. Container

**Question:** What is a container?

**Answer:** A lightweight virtualization unit that packages an application and libraries while sharing the host OS kernel.

### Q392. VM versus container

**Question:** Compare VMs and containers in isolation and startup cost.

**Answer:** VMs provide stronger isolation with a guest OS but are heavier and slower to start. Containers are lighter and faster but share the host kernel.

### Q393. Overlay network

**Question:** What is an overlay network in a cloud data center?

**Answer:** A virtual network built on top of the physical underlay, often mapping tenant addresses to physical host locations.

### Q394. Underlay

**Question:** What is the underlay network?

**Answer:** The physical network of switches, links, and host addresses that carries encapsulated overlay traffic.

### Q395. Overlay mapping

**Question:** Why does forwarding between VMs often need an overlay-to-underlay lookup?

**Answer:** The virtual destination address must be mapped to the physical host or tunnel endpoint where the destination VM currently resides.

### Q396. Fat tree

**Question:** Why do data centers use fat-tree or Clos-like topologies?

**Answer:** They provide many parallel paths and high bisection bandwidth using commodity switches.

### Q397. Non-blocking

**Question:** What does a non-blocking data-center network try to provide?

**Answer:** Enough capacity so many hosts can communicate simultaneously without a central bottleneck under expected traffic assumptions.

### Q398. Incast

**Question:** What is incast in a data-center network?

**Answer:** Many senders simultaneously send to one receiver or through one top-of-rack switch, causing a burst that overflows buffers.

### Q399. Incast mitigation

**Question:** Give two possible ways to mitigate incast.

**Answer:** Use request staggering, better flow control, larger or smarter buffers, lower retransmission timeout, pacing, or application-level batching.

### Q400. GPU cluster communication

**Question:** Why are GPU clusters sensitive to network performance?

**Answer:** Distributed training and inference move large tensors and activations; slow communication can leave expensive GPUs idle.

### Q401. GPU interconnect

**Question:** Why might specialized GPU interconnects be used in addition to Ethernet?

**Answer:** They can provide lower latency and higher bandwidth for GPU-GPU communication within or across servers.

### Q402. Tail latency

**Question:** Why is tail latency important for data-center services?

**Answer:** A request may depend on many subrequests; a slow tail subrequest can delay the whole user-facing response.

### Q403. Service composition

**Question:** If a service request fans out to 100 subrequests, why does the 99th percentile of subrequest latency matter?

**Answer:** The overall request often waits for many subrequests, so even rare slow subrequests become common at the aggregate level.

### Q404. Network and utilization

**Question:** Why can poor networking reduce server or GPU utilization?

**Answer:** Workers may wait for data, gradients, RPC replies, or storage I/O, leaving compute resources idle.


## Mixed Sample-Style Questions

### Q405. TCP or UDP mixed

**Question:** Choose TCP or UDP for each: (1) file backup, (2) live voice call, (3) DNS query, (4) online bank transfer. Briefly justify.

**Answer:** (1) TCP for reliable ordered transfer. (2) UDP is common because low latency matters and some loss is acceptable. (3) UDP is common for small low-latency queries with retries. (4) TCP plus application-level transaction/security logic because correctness matters.

### Q406. LPM mixed

**Question:** A router table has 0.0.0.0/0 -> A, 10.0.0.0/8 -> B, 10.2.0.0/16 -> C, 10.2.3.0/24 -> D. Find next hops for 10.2.3.4, 10.2.9.1, 10.8.1.1, and 11.1.1.1.

**Answer:** 10.2.3.4 -> D; 10.2.9.1 -> C; 10.8.1.1 -> B; 11.1.1.1 -> A.

### Q407. RPC semantics mixed

**Question:** Choose at-least-once or at-most-once: (1) increment a bank balance, (2) read the current temperature sensor value, (3) delete a file, (4) fetch a cached web object.

**Answer:** (1) At-most-once or stronger, because duplicates change money. (2) At-least-once is acceptable if repeated reads are harmless. (3) At-most-once is safer unless delete is explicitly idempotent. (4) At-least-once is usually acceptable.

### Q408. Dynamo quorum mixed

**Question:** For N=5, evaluate whether quorum overlap is guaranteed for (1) R=2,W=3, (2) R=3,W=3, (3) R=1,W=5.

**Answer:** Overlap requires R+W>N. (1) 5 is not greater than 5, so not guaranteed. (2) 6>5, guaranteed. (3) 6>5, guaranteed.

### Q409. HDFS survival mixed

**Question:** A file has 2000 blocks, replication factor 3, and independent machine failure probability 0.005. Approximate the probability a single block is lost and the file survives.

**Answer:** Single block loss = 0.005^3 = 1.25e-7. File survival = (1 - 1.25e-7)^2000, about 0.99975.

### Q410. Cristian mixed

**Question:** Given T1=10, T2=40, T3=50, T4=100, compute delta and the client clock setting under symmetric delay.

**Answer:** delta=(100-10)-(50-40)=90-10=80. Set client clock to T3+delta/2=50+40=90.

### Q411. Lamport mixed

**Question:** A process with Lamport clock 12 receives a message timestamped 20. It then sends a message. What timestamp is on the sent message if it increments once on receive and once on send?

**Answer:** After receive: max(12,20)+1=21. After send increment: 22, so the sent timestamp is 22.

### Q412. Vector mixed

**Question:** Compare V=[3,1,4] and W=[3,2,4]. What is the relationship?

**Answer:** V <= W componentwise and W is larger in one component, so V happens before W.

### Q413. Collective mixed

**Question:** With p=16, alpha=1 ms, and n beta=7 ms, compute tree broadcast cost.

**Answer:** log2(16)=4. Cost=4*(1+7)=32 ms.

### Q414. Allreduce mixed

**Question:** With p=8, alpha=0.5 ms, and n beta=40 ms, estimate ring allreduce cost using 2(p-1)alpha + 2(p-1)n beta/p.

**Answer:** 2*7*0.5 + 2*7*40/8 = 7 + 70 = 77 ms.

### Q415. Workflow mixed

**Question:** A DAG has total work 90, critical path 30, and 5 workers. What lower bound on runtime and upper bound on speedup follow?

**Answer:** Runtime lower bound=max(90/5,30)=30. Speedup upper bound=90/30=3.

### Q416. Storage-system choice

**Question:** Choose HDFS/GFS or Dynamo: (1) nightly batch scan over 10 TB logs, (2) shopping cart update, (3) sub-second key-value lookup, (4) append-only large file analytics.

**Answer:** (1) HDFS/GFS. (2) Dynamo. (3) Dynamo. (4) HDFS/GFS.

### Q417. P2P choice

**Question:** For a file-sharing system, compare centralized index and flooding in one sentence each.

**Answer:** Centralized index gives simple fast lookup but creates a bottleneck and single point of failure. Flooding avoids a central index but creates high message overhead and incomplete search under TTL limits.

### Q418. Socket sequence

**Question:** A TCP server calls `socket`, `bind`, `listen`, then blocks. Which call returns a per-client descriptor after a client connects?

**Answer:** `accept` returns the per-client connected descriptor.

### Q419. HTTP PLT

**Question:** A page needs 1 HTML file and 8 small images from the same server. Why can persistent connections improve PLT compared with one connection per object?

**Answer:** They avoid repeated TCP handshakes and repeated slow start, allowing multiple requests over the same connection.
