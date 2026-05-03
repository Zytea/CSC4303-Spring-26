# CSC4303 Lecture Credit Summary

Scope: lecture PDFs `02-*.pdf` through `18-*.pdf`. Method: I checked the credit note on the final page of each lecture PDF and summarized it together with the lecture context. This document summarizes course, paper, and material sources only; it is not a page-by-page copyright attribution.

## Per-PDF credits and CSC4303 context

| PDF | CSC4303 lecture context | Final-page credit summary | Corresponding external source | Role in CSC4303 |
|---|---|---|---|---|
| `02-network.pdf` | Computer Network Overview: links, switching, packet switching, statistical multiplexing, buffering, channel metrics, packet delay, layering | Some slides are adapted from course slides of **15-440 in CMU** | CMU 15-440 Distributed Systems | Provides the high-level network and distributed-system motivation for scalable packet networks, buffering, congestion, and layering. |
| `03-transport.pdf` | Transport Layer: TCP/UDP, ports, sockets, TCP three-way handshake, connection release | Some slides are adapted from course slides of **CSE 461 in UW** | UW CSE 461 Computer Networks | Main source for transport-layer services, TCP/UDP comparison, ports, and connection management. |
| `04-flow_control.pdf` | TCP Flow Control: stop-and-wait, sliding windows, Go-Back-N, Selective Repeat, sequence-number wraparound | Some slides are adapted from course slides of **CSE 461 in UW** | UW CSE 461 Computer Networks | Main source for reliable transport, flow control, retransmission, and sliding-window exam problems. |
| `05-congestion.pdf` | TCP Congestion Control: queues, congestion collapse, throughput/goodput, max-min fairness, AIMD, slow start, fast retransmit, fast recovery | Some slides are adapted from course slides of **CSE 461 in UW** | UW CSE 461 Computer Networks | Main source for congestion-control, fairness, and TCP Tahoe/Reno-style reasoning. |
| `06-socket.pdf` | Socket Programming: Unix file descriptors, `socket`, `bind`, `listen`, `accept`, `connect`, network byte order, `select`, `poll`, concurrency | Some slides are adapted from course slides of **15-213 in CMU** | CMU 15-213/18-213 Introduction to Computer Systems | Main source for socket API, file-descriptor abstraction, client/server call order, blocking I/O, I/O multiplexing, and concurrency issues. |
| `07-IP.pdf` | Network Layer: datagram model, IPv4 header, prefixes/CIDR, fragmentation, DHCP, ARP, ICMP, NAT, IPv6 | Some slides are adapted from course slides of **CSE 461 in UW** | UW CSE 461 Computer Networks | Main source for IP addressing, forwarding, fragmentation, and network-layer support protocols. |
| `08-routing.pdf` | Routing: shortest paths, sink trees, distance vector, count-to-infinity, link state, Dijkstra, hierarchical routing | Some slides are adapted from course slides of **CSE 461 in UW** | UW CSE 461 Computer Networks | Main source for routing algorithms, convergence, forwarding-table reasoning, and shortest-path problems. |
| `09-p2p.pdf` | Peer-to-Peer: Napster, Gnutella, KaZaA, BitTorrent, DHT, Chord | Some slides are adapted from course slides of **COS 418/518 in Princeton** | Princeton COS 418/518 Distributed Systems | Main source for P2P lookup, DHT/Chord, file-sharing systems, and scalability tradeoffs. |
| `10-dynamo.pdf` | Distributed Storage System: Dynamo: shopping carts, consistent hashing, virtual nodes, replication, read/write quorums, conflict resolution | Some slides are adapted from course slides of **DS 5110 in UVA** | UVA DS 5110 Big Data Systems | Main source for Dynamo, consistent hashing, high availability, quorum reasoning, and eventually consistent storage. |
| `11-application.pdf` | Application Layer: HTTP, page load time, parallel and persistent connections, caching/proxies, DNS, CDNs | Some slides are adapted from course slides of **CSE 461 in UW** | UW CSE 461 Computer Networks | Main source for HTTP/DNS/CDN behavior and application-layer performance problems. |
| `12-rpc.pdf` | RPC: RPC layer, stubs, marshalling, IDL, failure semantics, at-least-once, at-most-once, exactly-once limitations | Some slides are adapted from course slides of **COS 418/518 in Princeton** | Princeton COS 418/518 Distributed Systems | Main source for RPC semantics, stubs, IDL, idempotence, duplicate suppression, and failure handling. |
| `13-gfs.pdf` | Distributed Storage System: GFS/HDFS: scale-out storage, chunks/blocks, single master, replication, leases, primary replicas, record append, HDFS placement | Some slides adapted from **COMP 4651 in HKUST** and **DS5110 in UVA** | HKUST COMP 4651 Cloud Computing and Big Data Systems; UVA DS 5110 Big Data Systems | Main source for large-scale file-system design, GFS/HDFS architecture, replication, chunk placement, and batch-storage reasoning. |
| `14-time.pdf` | Time in Distributed Systems: physical-clock synchronization, Cristian's algorithm, Lamport clocks, vector clocks, totally ordered multicast | Some slides adapted from course slides of **COS 418/518 in Princeton** | Princeton COS 418/518 Distributed Systems | Main source for logical time, causal ordering, distributed replication order, and timestamp calculations. |
| `15-collective.pdf` | Parallelism Basics and Collective Communication: dataflow graphs, task/data parallelism, collective primitives | References include **Collective communication: theory, practice, and experience**; slides from **DS5110 in UVA** and **DSC204A in UCSD** | Chan et al. collective-communication paper; UVA DS5110; UCSD DSC204A Scalable Data Systems | Source for parallel-computing abstractions and collective communication primitives. |
| `16-collective_algo.pdf` | Collective Communication Algorithm: MST/tree algorithms, ring algorithms, broadcast, reduce, scatter, gather, allgather, reduce-scatter, allreduce, cost analysis | References include **Collective communication: theory, practice, and experience**; slides from **DSC204A in UCSD** | Chan et al.; UCSD DSC204A | Main source for collective-communication algorithm complexity and MST/tree versus ring tradeoffs. |
| `17-mlsys.pdf` | Distributed ML and LLM Systems: ML training/serving, data/model parallelism, parameter servers, AllReduce, LLM prefill/decoding, continuous batching, DistServe | Slides from **15-779 in CMU**, **DSC204A in UCSD**; DistServe OSDI'24 paper | CMU 15-779 Advanced ML Systems; UCSD DSC204A; DistServe paper | Source for distributed ML training, LLM inference systems, continuous batching, disaggregated serving, TTFT/TPOT, and goodput. |
| `18-dcn.pdf` | Data Center Networking: cloud data-center costs, VMs, containers, overlay networks, container networking, fat tree, incast, GPU clusters | Slides adapted from **COS461 in Princeton** and **CSE599k in UW** | Princeton COS 461 Computer Networks; UW CSE599/CSE599K-style data-center networking materials | Source for data-center networking, virtualization, overlay/underlay forwarding, container networking, fat-tree design, incast, and GPU-cluster communication. |

## Aggregated source map

### CMU 15-440 Distributed Systems
Appears in `02-network.pdf`. In CSC4303, this source contributes the distributed-systems motivation for scalable networking: packet switching, buffering, congestion, and layering.

### UW CSE 461 Computer Networks
Appears in `03-transport.pdf`, `04-flow_control.pdf`, `05-congestion.pdf`, `07-IP.pdf`, `08-routing.pdf`, and `11-application.pdf`. This is the dominant source for the protocol portion of CSC4303: transport, flow control, congestion control, IP, routing, HTTP, DNS, and CDNs.

### CMU 15-213/18-213 Introduction to Computer Systems
Appears in `06-socket.pdf`. This source supports the systems-programming side of CSC4303: file descriptors, socket APIs, client/server call order, blocking I/O, `select`/`poll`, threads, processes, and race conditions.

### Princeton COS 418/518 Distributed Systems
Appears in `09-p2p.pdf`, `12-rpc.pdf`, and `14-time.pdf`. It supports the P2P, RPC, Lamport-clock, vector-clock, and distributed-systems semantics topics in CSC4303.

### UVA DS 5110 Big Data Systems
Appears in `10-dynamo.pdf`, `13-gfs.pdf`, and `15-collective.pdf`. It supports Dynamo, GFS/HDFS, big-data systems, parallel data processing, and part of the collective-communication background.

### HKUST COMP 4651 Cloud Computing and Big Data Systems
Appears in `13-gfs.pdf`. It supports the GFS/HDFS design material: scale-out storage, replication, chunk placement, master/chunkserver architecture, and batch-oriented file-system design.

### UCSD DSC 204A Scalable Data Systems
Appears in `15-collective.pdf`, `16-collective_algo.pdf`, and `17-mlsys.pdf`. It supports scalable data systems, collective communication, distributed ML, and LLM serving.

### CMU 15-779 Advanced Topics in Machine Learning Systems
Appears in `17-mlsys.pdf`. It supports distributed training, ML serving, LLM inference, and systems optimizations for modern ML workloads.

### Princeton COS 461 Computer Networks and UW CSE599/CSE599K-style data-center networking materials
Appear in `18-dcn.pdf`. They support data-center networking, virtualization, overlays, underlays, containers, fat trees, incast, and GPU-cluster networking.

### Chan et al., "Collective communication: theory, practice, and experience"
Appears in `15-collective.pdf` and `16-collective_algo.pdf`. It supports the collective primitives and algorithm families: tree/MST algorithms for latency-sensitive small messages and ring/bandwidth-oriented algorithms for large messages.

### DistServe OSDI'24 paper
Appears in `17-mlsys.pdf`. It supports disaggregated prefill/decoding, TTFT/TPOT, and LLM-serving goodput optimization.
