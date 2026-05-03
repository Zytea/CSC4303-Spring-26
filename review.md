# CSC4303 Network Programming

# Reference

- https://book.systemsapproach.org/foundation.html

# 0. network (02)

1. Multiplexing and demultiplexing
2. Buffering and Congestion Control (Packets dropped;  Sender adjusts rate until load = resources)
3. Model of a communication channel
   -  **Latency,  Capacity (Bandwidth), Jitter (variation in latency), Loss/Reliability**

## 0.1 Packet delay $d_{\text{total}} = d_{\text{prop}} + d_{\text{trans}} + d_{\text{proc}} + d_{\text{queue}}$

1. **Propagation delay** $d_{\text{prop}} = \frac{\text{distance}}{\text{propagation speed}}$ ( $2 \times 10^8$ m/s in fiber)
2. **Transmission delay** $d_{\text{trans }} = \frac{L}{B}$ 
   - $L$: packet size (bits)；$B$: bandwidth (bits/s)
3. **Processing delay** $d_{\text{proc}}$ (router processing time) 
   -   检查 packet header；
       
   -   看目标 IP 地址；
       
   -   查 routing table；
       
   -   检查 checksum；
       
   -   决定从哪个 output link 发出去。

4. **Queueing delay** $d_{\text{queue}}$ (time waiting in output queue) 
      - 取决于 traffic load 和 queue size。

> Store & Forward: $2\times(Prop + xmit)$
>
> Cut-through: $2\times Prop + xmit$ 

## 0.2 Network Model

|Layer|Description|Example|PDU|
|:--:|:--:|:--:|----|
|Application|Programs that use network service|HTTP, DNS, CDNs|Message|
|Transport|Provides end-to-end data delivery|TCP, UDP|Segment|
|Network|Send packets over multiple networks|IP, NAT, BGP|Packet|
|Link|Send frames over one or more links|Ethernet, 802.11|Frame|
|Physical|Send bits using signals|wires, fiber, wireless|Bit|

### 0.2.1 Layering characteristics

- Modularity.
-  Interface: horizontal & vertical
- Protocols define: 
  - Vertical Interface to higher layers (API) 
  - Horizontal Interface to peer (syntax & semantics) 
  - Actions taken on receipt of a messages 
  - Format and order of messages 
  - Error handling, termination, etc.
- Abstraction.

## 0.2.2 Multiplexing and demultiplexing

- **Multiplexing**: Multiple upper-layers can use the same lower-layer protocol (via headers).
- **Demultiplexing**: Lower-layer protocol can deliver data to the correct upper-layer protocol (via headers). 

# 1. Transport Layer (03-06)

## 1.0 Internet transports

### 1.0.1 Socket

#### 1.0.1.1 Basics

An endpoint for network communication that allows an application to attach to a specific port on the local network interface, enabling data exchange with other applications across the network.

<img src="assets/6.png" width="60%" height="60%">

- **Process**

  Cilent  `socket () ------------------------> connect () -> I/O -> close ()`

  Server `socket () -> bind () -> listen () -> accept () -> I/O -> close ()`

  1. The server blocks in `accept()` on `listenfd` for incoming connections. 

  2. The client calls `connect()` to initiate the TCP handshake, which also blocks. 

  3. Upon completion, the server's `accept()` returns a `connfd` and the client's `connect()` returns, establishing a bidirectional channel between `clientfd` and `connfd`.

     > - File descriptor 是进程看到的一个整数 handle
     > - 每个进程都有自己的 file descriptor table
     > - fd 会指向 kernel 里的真正对象
     >   - 这个对象可以是 file, pipe, socket, tty; 
     >   - 所以 socket 可以像文件一样 read/write/close
     >
     > Example:
     >
     > ```
     > Process P
     > ├── Thread 1
     > ├── Thread 2
     > └── Thread 3
     > 
     > 它们共享：
     > fd table:
     > 3 -> listenfd
     > 4 -> connfd for client A
     > 5 -> connfd for client B
     > ```
     >
     > ```
     > TCP socket 的 kernel object：
     > - local IP
     > - local port
     > - remote IP
     > - remote port
     > - TCP state，例如 LISTEN / ESTABLISHED / FIN_WAIT
     > - send buffer
     > - receive buffer
     > - accept queue
     > - sequence number
     > - congestion window
     > - retransmission timer
     > - reference count
     > ```

- **Create** `int socket (int af, int type, int protocol);` 

  - **domain** AF_INET IPv4 / AF_INET6 IPv6.

  - **type** SOCK_STREAM TCP / SOCK_DGRAM UDP.

  - **protocol** 0 (automatically select the default protocol).

  - `setsockopt(int sockfd, int level, int optname, const void *optval, socklen_t optlen);` to set socket options

    > Example:
    >
    > ```c
    > // Set master socket to allow multiple connections
    > int opt = 1;
    > if (setsockopt(master_socket, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) {
    >     perror("setsockopt");
    >     exit(EXIT_FAILURE);
    > }
    > ```

- **Bind** `int bind (int sockfd, struct sockaddr *addr, socklen_t addrlen);`

  When a **server** binds a socket to a specific address, it establishes that data arriving at that address is read from this socket, and data written to this socket is sent from that address.

  - **socket address** 

    ```c
    struct sockaddr
    {
        sa_family_t sa_family; // protocol family, e.g., AF_INET
        char ss_data[14]; // address data (14B for IPv4)
    }
    ```

  - **sockaddr_in** 

    ```c
    struct sockaddr_in
    {
        uint16_t sin_family; // always AF_INET
        uint16_t sin_port; // in network byte order
        struct in_addr sin_addr; // in network byte order
        unsigned char sin_zero[8]; // pad to sizeof (struct sockaddr), placeholder
    }
    
    struct in_addr {
        in_addr_t s_addr; // 32位无符号整数 (Network Byte Order)
    };
    ```
    
    Network data is transmitted in big-endian byte order. 
    
    - Use `htons()` and `htonl()` to **convert host-ordered values into network-ordered short** and long integers, respectively; Use `ntohs()` and `ntohl()` for the reverse.
    - Use ` int inet_pton(int af, const char *src, void *dst)` to **convert IP addresses from text to binary form**; `inet_ntop()` for the reverse.
    
      > Example:
      >
      > ```c
      > int listenfd = socket(AF_INET, SOCK_STREAM, 0);
      > 
      > struct sockaddr_in serveraddr;
      > memset(&serveraddr, 0, sizeof(serveraddr));
      > serveraddr.sin_family = AF_INET;
      > serveraddr.sin_port = htons(8080);
      > serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
      > 
      > if (inet_pton(AF_INET, SERVER_IP, &serveraddr.sin_addr) <= 0) {
      >     // handle error; demo only   
      > }
      > 
      > bind(listenfd, (struct sockaddr *)&serveraddr, sizeof(serveraddr));
      > listen(listenfd, 128);
      > ```

- **Listen** `int listen (int sockfd, int backlog);`

  `listen ()` transforms a socket descriptor into a listening socket capable of accepting client connections. The `backlog` parameter suggests how many pending connections the kernel may queue before refusing new requests (typically around 128).

- **Accept** `int accpet (int listenfd, sockaddr *addr, int *addrlen);`

  `accept()` blocks until a client connects via `listenfd`, stores the client's address in `addr`, and returns a `connfd` for communication using standard Unix I/O functions.

- **Connect** `int connect (int clientfd, sockaddr *addr, socklen_t addrlen);`

  Attempts to establish a connection with server at socket address `addr`.

  To convert a string-formatted IP address (e.g., `SERVER_IP`), use `inet_pton (int af, const char *src, void *dst)` to transform it into binary network format.

  |      Feature       |         `listenfd`          |              `connfd`               |
  | :----------------: | :-------------------------: | :---------------------------------: |
  |    **Purpose**     | Accepts connection requests | Handles data exchange with a client |
  |    **Creation**    |    Once at server start     |       Per accepted connection       |
  |    **Lifetime**    |    Entire server runtime    |     Duration of client service      |
  |    **Quantity**    |        One per port         |        One per active client        |
  | **Concurrent Use** |   Listens for all clients   |     Dedicated to single client      |

- **Send and Receive**

  `ssize_t read (int fd, void *buf, size_t len);` returns the number of bytes actually read (0 indicates the connection is closed, -1 indicates an error).

  `ssize_t write (int fd, const void *buf, size_t len);` returns the number of bytes actually written (-1 indicates an error).

- **Close** `int close (int sockfd)`

#### 1.0.1.2 **Concurrency**

- **Threading/Process** Race conditions increase complexity!
	
	- Create one thread/process per connection.

	  ```
	  main thread: accept()
	  worker thread: read() / write() / close()
	  ```
	
	  - Easy to write with blocking I/O.
	  - Each worker handles one `connfd`.
	  - But shared state may cause **race conditions**.
	
	  > Race condition: multiple threads access the same shared data concurrently, and the result depends on execution order.
	  >
	  > Example:
	  >
	  > In P2P flooding, if two threads check the same query at the same time:
	  >
	  > ```
	  > Thread A: query not seen
	  > Thread B: query not seen
	  > ```
	  >
	  > both may forward it, causing duplicate flooding or loop-avoidance failure.
	
	- Use **mutex** to protect critical sections.
	
	  ```c
	  lock = PTHREAD_MUTEX_INITIALIZER; // or pthread_mutex_init(&lock, NULL);
	  
	  pthread_mutex_lock(&lock);
	  // access shared state
	  pthread_mutex_unlock(&lock);
	  ```
	  
	  Mutex avoids races, but introduces extra complexity:
	  
	  - forgetting to lock → race condition
	  - forgetting to unlock → stuck forever
	  - wrong lock order → deadlock
	
- **I/O Multiplexing** 

  - `select()`

    - ```c
      int select(
        int nfds,
        fd_set *readfds, // Bitmap
        fd_set *writefds,
        fd_set *exceptfds,
        struct timeval *timeout
      );
      ```
  
      > Example:
      >
      > ```c
      > fd_set readset;
      > 
      > FD_ZERO(&readset);              // 清空集合
      > FD_SET(listenfd, &readset);     // 监控 listenfd
      > FD_SET(connfd, &readset);       // 监控 connfd
      > 
      > maxfd = max(listenfd, connfd);
      > select(maxfd + 1, &readset, NULL, NULL, NULL);
      > 
      > if (FD_ISSET(listenfd, &readset)) {
      >     accept(listenfd, NULL, NULL);
      > }
      > if (FD_ISSET(connfd, &readset)) {
      >     read(connfd, buf, sizeof(buf));
      > }
      > ```
  
  - `int poll(struct pollfd fds[], nfds_t nfds, int timeout);` 
  
    `poll()` is a system call used to monitor multiple file descriptors concurrently for I/O readiness. Unlike `select()`, it imposes **no fixed limit** on the number of file descriptors that can be monitored.
  
    ```c
    struct pollfd
    {
        int fd;        // file descriptor
        short events;  // requested events
        short revents; // returned events
    }   
    ```
    
    > Example:
    >
    > ```c
    > // ... Assuming listenfd is already created, bound, and listening ...
    > 
    > struct pollfd fds[1024];
    > int nfds = 1;
    > 
    > // 1. Initialization: Add the listening socket to the first slot
    > fds[0].fd = listenfd;
    > fds[0].events = POLLIN;
    > 
    > while (1) {
    >     // 2. Wait for events (-1 = blocking)
    >     int event_count = poll(fds, nfds, -1);
    >     if (event_count < 0) {
    >         perror("poll error");
    >         break;
    >     }
    > 
    >     // 3. Handle the listening socket (New Connections)
    >     if (fds[0].revents & POLLIN) {
    >         int connfd = accept(listenfd, NULL, NULL);
    >         if (connfd != -1 && nfds < 1024) {
    >             fds[nfds].fd = connfd;
    >             fds[nfds].events = POLLIN;
    >             nfds++;
    >             printf("New client connected, fd: %d\n", connfd);
    >         }
    >     }
    > 
    >     // 4. Handle existing client connections
    >     for (int i = 1; i < nfds; i++) {
    >         if (fds[i].revents & POLLIN) {
    >             char buf[1024];
    >             int n = read(fds[i].fd, buf, sizeof(buf));
    >             
    >             if (n <= 0) {
    >                 printf("Client on fd %d disconnected\n", fds[i].fd);
    >                 close(fds[i].fd);
    >                 
    >                 // Shrink the array
    >                 fds[i] = fds[nfds - 1]; 
    >                 nfds--;
    >                 i--; // Re-check the current index 
    >             } else {
    >                 // Successfully received data
    >                 printf("Received %d bytes from fd %d\n", n, fds[i].fd);
    >             }
    >         }
    >     }
    > }
    > ```

### 1.0.2 Port

Application process identifier: IP address + transport protocol + port (16-bit integers)

- port <1024, require administrative privileges

| Port       | Protocol | Use                                  |
| ---------- | -------- | ------------------------------------ |
| TCP/20, 21 | FTP      | File transfer                        |
| TCP/22     | SSH      | Remote login, replacement for Telnet |
| TCP/25     | SMTP     | Email                                |
| TCP/80     | HTTP     | World Wide Web                       |
| TCP/443    | HTTPS    | Secure Web (HTTP over SSL/TLS)       |
| TCP/3306   | MYSQL    | MYSQL database access                |
| UDP/53     | DNS      | Domain name service                  |

### 1.0.3 Overview of  UDP and TCP

1. UDP:
   - Performance is very important. Lost frames are mostly fine. 
   - e.g.,  Voice-over-IP, DNS, Games 

2. TCP:
   - Reliability is crucial in the application.
   - e.g., an email service. 

|      Feature       |                     TCP                      |                   UDP                   |
| :----------------: | :------------------------------------------: | :-------------------------------------: |
|        Mode        |                 Connections                  |                Datagrams                |
|    Reliability     |  No loss, no duplicates, in-order delivery   | May lose, reorder, or duplicate packets |
|     Data Size      |                  Unlimited                   |                 Limited                 |
|    Flow Control    |   Flow control matches sender to receiver    |    Send regardless of receiver state    |
| Congestion Control | Congestion control matches sender to network |    Send regardless of network state     |

## 1.1 UDP

- **Connectionless** 
  
    Each packet is independent.

    ```
    Sender    Time       Receiver
      |                     |
      |----- Packet1 -----> |
      |                     |
      |----- Packet2 -----> |
      |                     |
    ```

- **Buffering**

    UDP buffering is a "temporary storage area" maintained by the operating system for each UDP port, where arriving packets queue up when applications can't process them immediately.

    ```
    Application A  Application B   Application C
        ↓               ↓               ↓
    [Port X]        [Port Y]        [Port Z]      ← Port mapping
        ↓               ↓               ↓
    [Queue 1]       [Queue 2]       [Queue 3]     ← Independent UDP message queues
        │               │               │
        └───────┬───────┴───────┬───────┘
                ↓               ↓
        [Port Multiplexer/Demultiplexer]          ← Routes by port number
                ↓
        [Incoming UDP packets]
    ```

- **Header**

    Note that the Datagram length up to 64K.
    ```
         32-bit width (4 bytes per row)
    0                  16                31
    ┌──────────────────┬──────────────────┐
    │ Source Port      │ Destination Port │ ← Port addressing
    │   (16 bits)      │   (16 bits)      │
    ├──────────────────┴──────────────────┤
    │    Length        │    Checksum      │ ← Size & integrity
    │    (16 bits)     │    (16 bits)     │
    ├──────────────────────────────────┤
    │                                     │
    │           Application Data          │
    │                                     │
    └─────────────────────────────────────┘
    ```
    
    ⚠️最大 UDP application data = 65535  -20 - 8 = 65507 bytes (太网 MTU 常见是 1500 bytes)
## 1.2 TCP

- **Header**

    ```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    ┌──────────────────────────────┬──────────────────────────────┐
    │          Source Port         │       Destination Port       │ ← Identifies sockets
    ├──────────────────────────────┴──────────────────────────────┤
    │                      Sequence Number (32)                   │
    ├─────────────────────────────────────────────────────────────┤
    │                  Acknowledgment Number (32)                 │ ← Next expected byte
    ├───────────────┬───┬─────────┬───────────────────────────────┤
    │  Data Offset  │ 0 │  Flags  │       Window Size (16)        │ ← Control & flow 
    ├───────────────┴───┴─────────┼───────────────────────────────┤
    │         Checksum (16)       │       Urgent Pointer (16)     │ ← Integrity & urgent
    ├─────────────────────────────┴───────────────────────────────┤
    │                         Options (variable)                  │
    ├─────────────────────────────────────────────────────────────┤
    │                           Data                              │
    └─────────────────────────────────────────────────────────────┘
    ```

    > ⚠️max TCP payload = 1500 - 20 - 20 = 1460 bytes
    >
    > Data Offset = start of TCP data
    >
    > Flags: SYN, ACK, FIN, RST, PSH, URG
    >
    > - 比如三次握手用 SYN、ACK；四次挥手用 FIN、ACK。
    >
    > Window Size:
    >
    > - 接收方 advertised 给发送方的可用 buffer 空间。
    
    - **Connection Establishment (Setup)**
    
        - **Three-Way Handshake**

            Both parties send Initial Sequence Numbers (ISNs) via SYNchronize segments. Each party acknowledges the other's sequence number using ACKnowledge segments.
    
            <img src="assets/1.png" width="40%" height="40%">
    
            |Step|Initiator (Client)| Receiver (Server)|Description|
            |:--:|:--:|:--:|:--:|
            |First Handshake | Sends $\texttt{SYN}=1, \texttt{seq}=x$ | Waits for connection request | Client requests to establish a connection and sends its ISN $x$.|
            |Second Handshake | Waits for acknowledgment | Sends $\texttt{SYN}=1, \texttt{ACK}=1, \texttt{seq}=y, \texttt{ack}=x+1$ <br> It acknowledges receipt through sequence number $x$. | Server agrees to connect, sends its own ISN $y$, and acknowledges the receipt of $x$.|
            |Third Handshake | Sends $\texttt{ACK}=1, \texttt{seq}=x+1, \texttt{ack}=y+1$ | Connection established| Client acknowledges the receipt of $y$, and the connection is formally established.|
    
            $$
            ISN = M + F(\text{localip}, \text{localport}, \text{remoteip}, \text{remoteport}, \text{secret key})
            $$
            
            Three-way handshake prevents a server from wasting resources on stale or duplicate connection requests by requiring the client's final acknowledgment.
            
        - **State Machine**
        
            <img src="assets/2.png" width="100%" height="70%"  >
        
            - Client Path `CLOSED → connect() → SYN_SENT → Receive SYN+ACK → ESTABLISHED`
        
            - Server Path `CLOSED → listen() → LISTEN → Receive SYN → SYN_RCVD → Receive ACK → ESTABLISHED`
        
            - Both parties run instances of this state machine, and TCP allows for simultaneous open.
        
    - **Connection Release (Teardown)**
    
        - **Four-Way Handshake (symmetric)**
    
            <img src="assets/3.png" width="40%" height="40%">

            | Step | Initiator (Active Closer) | Receiver (Passive Closer) | Description |
            |:---:|:---:|:---:|:---:|
            | First Wave | Sends $\texttt{FIN}=1, \texttt{seq}=u$ | Waits for close request | Initiator has finished sending data and requests to close its sending channel. |
            | Second Wave | Waits for remaining data | Sends $\texttt{ACK}=1, \texttt{ack}=u+1$ | Receiver acknowledges the close request **but may still have data to send**. |
            | Third Wave | Waits for confirmation | Sends $\texttt{FIN}=1, \texttt{seq}=v$ | Receiver has finished sending data and requests to close its sending channel. |
            | Fourth Wave | Sends $\texttt{ACK}=1, \texttt{ack}=v+1$ | Connection closed | Initiator acknowledges the close request. |
        
        - **State Machine**
    
            <img src="assets/4.png" width="80%" height="70%" style="zoom:;" >
    
            - **Active Closer Path** `ESTABLISHED → close() → FIN_WAIT_1 → Receive ACK → FIN_WAIT_2 → Receive FIN → TIME_WAIT → Timeout → CLOSED`
    
            - **Passive Closer Path** `ESTABLISHED → Receive FIN → CLOSE_WAIT → close() → LAST_ACK → Receive ACK → CLOSED`
    
            - **TIME_WAIT State**
    
                - $2 \times \texttt{MSL}$ (Maximum Segment Lifetime).
                  - 旧 segment 在网络里最多活 1MSL
                    它触发的响应或重传又最多活 1MSL
    
                - Lost ACKs can be recovered.
                
                - Old segments won't confuse new connections.
        

## 1.3 TCP Flow Control

- **Goal:** Match transmission speed to reception capacity.

### 1.3.1 Stop-and-Wait **Automatic Repeat Query**

- ARQ with one message at a time. It allows only a single message to be outstanding from sender.

- Fine for LAN (low RTT; only one frame fits in network anyhow)

> Example: 
>
> B=1 Mbps, D = 50 ms
>
> → RTT = 2D = 100 ms $\iff$ 10 packets/s
>
> $$
> \begin{aligned}
> \text{efficiency}_\text{10kb}
> &= \frac{T_{\text{transmit}}}{T_{\text{transmit}}+RTT} \\ 
> &= \frac{L/B}{L/B+RTT} \\ &= \frac{L}{L+B\cdot RTT} \\
> & = \frac{L}{L + 2BD} = \frac{1e4}{1e4+1e6\times(1e-1)}=9.09\%
> \end{aligned}
> $$

### 1.3.2 **Sliding Window ARQ** 

It allows $W$ outstanding packets, enabling pipelining to send multiple packets per RTT for improved performance.

> $$
> \begin{aligned}
> &\text{throughput} \approx \frac{\text{W}}{RTT} \ge B \\
> \rightarrow &W_\min = \frac{2BD}{L}
> \end{aligned}
> $$

Sender buffers up to $W$ segments until they are acknowledged. $LFS – LAR ≤ W$

<img src="assets/5.png" width="60%" height="60%">

- **Go-Back-N**

     Only buffers next expected packet (LAS). Accepts only **sequential** packets, discards others, sends **cumulative** ACK.

     发送方：最多允许 N 个未确认的数据在路上
     接收方：只接受下一个按顺序来的数据
     如果乱序到达：直接丢弃
     丢包后：发送方从丢失的那个开始全部重传

- **Selective Repeat**

     Buffers entire window. Stores out-of-order packets, sends individual ACKs, retransmits only lost packets.

     发送方：最多允许 $W$ 个未确认的数据在路上
     接收方：接收窗口内的 packet，即使乱序也缓存
     如果乱序到达：不丢弃，先 buffer, 指针不动
     丢包后：发送方只重传真正丢失的那个 packet

- **Sequence Number**

     $n$ bit counter wraps around at $2^n - 1$. Let $\text{LAR}$ be Last Acknowledgement Received, $\text{LAS}$ be Last Acknowledgement Sent.
     |Method|Sender's Range|Receiver's Range|Min Number Needed to Avoid Overlap (M)|
     |:--:|:--:|:--:|:--:|
     |Go-Back-N|$[\text{LAR} + 1,\text{LAR} + W]$|$\text{LAS} + 1$|$W + 1$|
     |Selective Repeat|$[\text{LAR} + 1,\text{LAR} + W]$|$[\text{LAS} + 1,\text{LAS} + W]$|$2W$|

     > ⚠️ 为了判断 $x \text{ is after } y \iff 0 < (x-y) \bmod 2^{32} < 2^{31}$，**TCP** 要求窗口相关的序号比较必须落在 **半个 sequence space** 以内，也就是 $2W_\max < 2^{31}$, i.e., $W_\max = (2^{16}-1)2^S < 2^{30}$, 所以scale shift $S_\max=14$

- <img src="assets/image-20260502120018980.png" alt="image-20260502120018980" style="zoom: 67%;" />

- **Pacing**

    - **ACK Clocking** (sender)

        ACK clocking is a feedback mechanism where the network itself determines the sending pace, preventing queue buildup and ensuring efficient, low-latency data flow.

    - **Flow Control** (Receiver)

        Flow control uses the `WIN` field, calculated as `WIN = ReceiveBuffer - (LastByteRcvd - LastByteRead)`, to dynamically limit the sender's window, preventing receiver buffer overflow.

    $\text{SEQ} + \text{length} < \text{ACK} + \text{WIN}$

    - <img src="assets/image-20260502122214270.png" alt="image-20260502122214270" style="zoom:50%;" />

    - **Adaptive Timeout**

        |Name|Formula|
        |:--:|:--:|
        |$\text{SRTT}$ (average round‑trip time)|$\text{SRTT}_{n + 1} = (1 - \alpha)\cdot \text{SRTT}_n + \alpha \cdot \text{RTT}_{n + 1}$ |
        |$\text{Svar}$ (variability of RTT)|$\text{Svar}_{n + 1} = (1-\beta)\cdot \text{Svar}_n + \beta \cdot \mid \text{RTT}_{n + 1} - \text{SRTT}_{n + 1} \mid$|
        |$\text{Timeout}$|$\text{Timeout}_n = \text{SRTT}_n + 4 \cdot \text{Svar}_n$|

## 1.4 **TCP Congestion Control**

### 1.4.1 Effects of congestion

<img src="assets/image-20260502123056476.png" alt="image-20260502123056476" style="zoom: 50%;" />

TCP congestion control uses a sliding window (cwnd), interprets packet loss as a congestion signal, and adjusts the window via AIMD to achieve an **efficient and roughly** fair bandwidth allocation.

> Efficient: most capacity is used but there is no congestion 
>
> Fair: every sender gets a reasonable share of the network

### 1.4.2 Open-loop: **Max-Min fairness**

Increase the rate of one flow will decrease the rate of a smaller flow.

> Step 1 Initialize all flows at zero  
Step 2 Increase all flows equally  
Step 3 Freeze bottlenecked flows  
Step 4 Repeat for remaining flows

### 1.4.3 Close-loop: **Bandwidth allocation**

- Network layer provides direct feedback &vs.Transport layer reduces load 
[Network is distributed, no single party has an overall picture of its state. → AIMD]

    > Network layer: 我这里堵了，我能看到 queue / loss / ECN
    >
    > Transport layer: 我收到这个信号后，减少 cwnd / sending rate

- **Models**
  
    - Open loop [reserve] vs. Closed loop [use feedback to adjust rates]
    - Host support [sender] vs. Network support [router]
    - Window based [cwnd; rate ≈ cwnd / RTT] vs. Rate based 
    
    **==TCP is a closed loop,host-driven, and window-based==**
    
- **AIMD(Additive Increase Multiplicative Decrease)** 

    - Hosts additively increase rate while network not congested

    - Hosts multiplicatively decrease rate when congested

      <img src="assets/image-20260502131433059.png" alt="image-20260502131433059" style="zoom:50%;" />

    >  Other increase/decrease control laws do not! (Try MIAD, MIMD, MIAD)

- | Signal                | Example Protocol                           | Pros / Cons                                                  |
    | --------------------- | ------------------------------------------ | ------------------------------------------------------------ |
    | **Packet loss**       | TCP NewReno <br>Cubic TCP (Linux)          | * Hard to get wrong <br>* Hear about congestion late <br/>* Other events can cause loss |
    | **Packet delay**      | BBR (Google)                               | * Hear about congestion early <br/>* Need to infer congestion |
    | **Router indication** | TCPs with Explicit Congestion Notification | * Hear about congestion early <br/>* Require router support  |

- **TCP Tahoe**

    - **Slow Start**
      
       For each ACK received: $\text{cwnd} = \text{cwnd} + 1$, $\text{cwnd}$ doubles every RTT.

    - **Later Additive Increase (AI)**

        For each ACK received: $\text{cwnd} \leftarrow \text{cwnd} + \frac{1}{\text{cwnd}}$, roughly adds 1 packet per RTT.

    - **Switching Threshold (Initially Infinity)**

        Switch from **Slow-Start** to **AI** when When $\text{cwnd} > \text{ssthresh}$, and $\text{ssthresh} = \frac{\text{cwnd}}{2}$ after loss. **Begin with slow start after timeout ($\text{cwnd} = 1$).**

    - **Fast Retransmit**

        TCP's cumulative ACKs allow duplicate ACKs to signal lost packets for fast retransmission.

        (Treat three duplicate ACKs as a loss.)

    - **Fast Recovery (TCP Reno)**

        Fast recovery keeps data flowing during retransmission by maintaining the ACK clock. It avoids resetting to Slow Start after packet loss. Set $\text{ssthresh} = \frac{\text{cwnd}}{2}$ and then continue AI directly.

    > ```
    > 连接刚开始：
    >     cwnd = 1
    >     Slow Start 指数增长
    > 
    > 如果 cwnd > ssthresh：
    >     进入 AI
    >     每 RTT 大约 +1
    > 
    > 如果发生 timeout：
    >     ssthresh = cwnd / 2
    >     cwnd = 1
    >     回到 Slow Start
    > 
    > 收到第 3 个 duplicate ACK：
    >     retransmit 丢失的 packet
    >     ssthresh = cwnd / 2
    >     cwnd 大致减半
    > 
    > 后续又收到 duplicate ACK：
    >     说明又有一个后续 packet 到达 receiver
    >     sender 可以适当继续发送新 packet
    >     维持 ACK clock
    > 
    > 当重传的 packet 被 receiver 收到：
    >     receiver 补上缺口
    >     ACK number 突然跳到更后面, 退出 Fast Recovery：
    >         cwnd = ssthresh
    >         进入 Additive Increase
    > ```

# 2. Network Layer (07-08)

**Goal**: Get packets from source to destination, which may be separated by many hops

**Reasons:**

- **Internetworking:** Need to connect different link layer networks 
- **Addressing:** Need a globally unique way to “address” hosts 
- **Routing and forwarding:** Need to find and traverse paths between hosts

 Internet Protocol (IP) is the **“narrow waist”**

## 2.1 Internet Protocol (IP)

- **IPV4 Header**

```
0                   1                   2                   3
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
┌───────┬───────┬───────────────┬───────────────────────────────┐
│Version│  IHL  │Type of Service│       Total Length (16)       │ ← Basic identification 
├───────┴───────┴───────────────┼─────┬─────────────────────────┤
│      Identification (16)      │Flags│  Fragment Offset (13)   │ ← Fragmentation control
├───────────────┬───────────────┼─────┴─────────────────────────┤
│ Time to Live  │   Protocol    │     Header Checksum (16)      │ ← Routing & integrity 
├───────────────┴───────────────┴───────────────────────────────┤
│                      Source Address (32)                      │ ← Sender IP
├───────────────────────────────────────────────────────────────┤
│                   Destination Address (32)                    │ ← Receiver IP
├───────────────────────────────────────────────────────────────┤
│                  Options (if any, variable)                   │ ← Optional features
├───────────────────────────────────────────────────────────────┤
│                        Payload (Data)                         │
└───────────────────────────────────────────────────────────────┘
```

> ⚠️
>
> version= 4 (4b)
>
> IHL (4b; Internet Header Length) = header length in 32-bit words (5 for no options);
>
> Type of Service (8b) = priority and QoS; 
>
> Total Length (16b) = header + payload in bytes;
>
> Identification (16b) = unique ID for fragments in the same datagram;
>
> Flags (3b) = control bits for fragmentation (DF, MF); 
>
> Fragment Offset (13b) = position of fragment in original datagram (in 8-byte units);
>
> Time to Live (8b) = max hops before discard; 

- **IP Addresses** An IP address is assigned to each network interface. Consequently, routers possess multiple interfaces, while most hosts have just one or two (wired and wireless).

- **IP Prefixes** In a prefix of length L, the top L bits are identical across all addresses. In CIDR notation, such a prefix is denoted as `IP address/prefix length` (e.g. `128.13.0.0/16` is `128.13.0.0` to `128.13.255.255`.)

- **IP Forwarding** It uses **longest prefix matching** to select the most specific route via a forwarding table.

    > Example:
    >
    > Destination IP: 192.24.14.32 → B
    >
    > ```
    > Prefix              Next Hop
    > 0.0.0.0/0            A
    > 192.24.0.0/19        B
    > 192.24.12.0/22       C
    > ```

- Host/Router Distinction

    -  Routers do the routing, know way to all destinations; Hosts send remote traffic (out of prefix) to nearest router

    - Host Networking:  

        - IP Address 

        - Subnet Mask (prefix length)

            > Example:
            >
            > ```
            > IP Address:   192.168.1.23
            > Subnet Mask:  255.255.255.0
            > ```
            >
            > → 192.168.1.23/24 → 192.168.1.0/24

        - Gateway 

            > Example:
            >
            > ```
            > Host:        192.168.1.23/24
            > Gateway:     192.168.1.1
            > Destination: 8.8.8.8
            > ```

        - DNS Server

- **IP fragmentation**

    - **MTU** Max Transfer Size
    - **MSS** Maximum Segment Size

    <img src="assets/7.png" width="50%" height="50%">

    Each fragment is encapsulated with its own IP header.

    | Field | Size (bits) | Purpose |
    |:--:|:--:|:--:|
    | **Identification** | 16 | Unique identifier for the original datagram; **all fragments** of the same datagram share this value. |
    | **Flags** | 3 | Control bits for fragmentation<br>**DF (Don't Fragment)** If set 1, routers must not fragment the packet.<br>**MF (More Fragments)** If set 1, more fragments follow, otherwise indicates that it is the last fragment. |
    | **Fragment Offset** | 13 | Indicates the position of this fragment's data **in 8‑byte units** relative to the start of the original datagram. |

	> Example:
	>
	> ```
	> Datagram size = 4000 bytes
	> MTU = 1500 bytes
	> IP header = 20 bytes
	> 
	> Fragment 1:
	> Total Length = 1500
	> Data = 1480
	> Offset = 0
	> MF = 1
	> 
	> Fragment 2:
	> Total Length = 1500
	> Data = 1480
	> Offset = 1480 / 8 = 185
	> MF = 1
	> 
	> Fragment 3:
	> Total Length = 1060
	> Data = 1000
	> Offset = 370
	> MF = 0
	> ```
	

## 2.2 Related Protocols

### 2.2.1 Dynamic Host Configuration Protocol (DHCP) [Application Layer]

 **Problem: A node wakes up for the first time** … 

- 你的 IP 是多少
  你的 subnet/prefix 是什么
  你的 gateway 是谁
  你的 DNS server 是谁

- At least Ethernet address is on NIC → DHCP (mostly on routers)

- ```
  ┌────────┐
  │  DHCP  │
  ├────────┤
  │  UDP   │ ← ports 67 (server), 68 (client)
  ├────────┤
  │   IP   │
  ├────────┤
  │Ethernet│
  └────────┘
  ```

| Step | Message | IP Header (Src &rarr; Dst) | Ethernet (Src &rarr; Dst) | Purpose |
|:----:|:--------|:-------------------------------------------|:--------------------------------------------------------|:---------------------------------------|
| 1 | **DISCOVER** | `0.0.0.0` &rarr; `255.255.255.255` | `Client MAC` &rarr; `FF:FF:FF:FF:FF:FF` | Client broadcasts to find DHCP servers |
| 2 | **OFFER** | `Server's IP` &rarr; `255.255.255.255` | `Server MAC` &rarr; `FF:FF:FF:FF:FF:FF` | Server proposes IP configuration |
| 3 | **REQUEST** | `0.0.0.0` &rarr; `255.255.255.255` | `Client MAC` &rarr; `FF:FF:FF:FF:FF:FF` | Client accepts the offer |
| 4 | **ACK** | `Server's IP` &rarr; `255.255.255.255` | `Server MAC` &rarr; `FF:FF:FF:FF:FF:FF` | Server confirms and finalizes lease |

### 2.2.2 Address Resolution Protocol (ARP)

Problem: 

- How does it get the destination link address from a destination IP address? → ARP **(table stored in every device)**

**Every network device** possesses a unique **MAC (Media Access Control)** address (48b), which operates at the link layer.

```
┌────────┐
│  ARP   │
├────────┤
│Ethernet│
└────────┘
```

ARP resolves IP to MAC addresses locally. A node **broadcasts** an ARP request, receives a **private** reply, and **caches** the mapping in its ARP table.

| Step | Message         | Ethernet (Src → Dst)               | ARP Fields                                                   | Purpose                            |
| ---- | --------------- | ---------------------------------- | ------------------------------------------------------------ | ---------------------------------- |
| 1    | **ARP REQUEST** | `Sender MAC` → `FF:FF:FF:FF:FF:FF` | Sender IP = `A_IP`Sender MAC = `A_MAC`<br>Target IP = `B_IP`Target MAC = `unknown` | A broadcasts: “Who has `B_IP`?”    |
| 2    | **ARP REPLY**   | `B_MAC` → `A_MAC`                  | Sender IP = `B_IP`Sender MAC = `B_MAC`<br>Target IP = `A_IP`Target MAC = `A_MAC` | B replies: “`B_IP` is at `B_MAC`.” |

> - Link Layer Header:
>
> ```
> 0                   1                   2                   3
> 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
> ┌───────────────────────────────────────────────────────────────┐
> │                Destination MAC Address (first 32 bits)        │
> ├───────────────────────────────┬───────────────────────────────┤
> │ Destination MAC (last 16 bits)│    Source MAC (first 16 bits) │
> ├───────────────────────────────┴───────────────────────────────┤
> │                   Source MAC Address (last 32 bits)           │
> ├───────────────────────────────┬───────────────────────────────┤
> │       EtherType (16 bits)     │             Payload           │
> └───────────────────────────────┴───────────────────────────────┘
> ```

### 2.2.3 Internet Control Message Protocol (ICMP)

```
0                   1                   2                   3
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
┌───────────────┬───────────────┬───────────────────────────────┐
│     Type      │     Code      │           Checksum            │
├───────────────┴───────────────┼───────────────────────────────┤
│           Identifier          │        Sequence Number        │
├───────────────────────────────┴───────────────────────────────┤
│                             Payload                           │
└───────────────────────────────────────────────────────────────┘
```

When an error occurs, an ICMP error report is sent back to the source IP address and the problematic packet is discarded. The source host must then rectify the issue.

- **Message Format**
    - **IP Header** `Src = router, Dst = A, Protocol = 1`

    - **ICMP Header** `Type = 大类错误 / 消息类型, Code = 更具体的原因`

    - **ICMP Data** `Src = A, Dst = B, ...` (通常包含出问题 packet 的开头部分)

- **Type**

|Name|Code|Usage|
|:--:|:--:|:--:|
|Dest. Unreachable (Net or Host)|`3/0` or `3/1`|Lack of connectivity|
|Dest. Unreachable (Fragment)|`3/4`|Path MTU Discovery|
|Time Exceeded (Transit) |`11/0`|Traceroute ($\texttt{TTL} = 0$)|
|Echo Request or Reply|`8/0` or `0/0`|Ping|

- **Traceroute**

Traceroute sends probe packets with incrementing TTL. Each router that decrements TTL to zero replies with an ICMP Time Exceeded error, revealing its address.

## 2.3 Network Address Translation (NAT)

**NAT maps multiple private IP:port pairs to a single public IP with unique external ports** via a stateful translation table, enabling many internal devices to share one external address. **(NAT box (router))**

> Example:
>
> | What host thinks     | What ISP thinks        |
> | -------------------- | ---------------------- |
> | **Internal IP:port** | **External IP : port** |
> | 192.168.1.12 : 5523  | 44.25.80.3 : 1500      |
> | 192.168.1.13 : 1234  | 44.25.80.3 : 1501      |
> | 192.168.2.20 : 1234  | 44.25.80.3 : 1502      |

- Pros: 
  - Relieves much IP address pressure
  - Easy to deploy
  - Useful functionality
- Cons: 
  - Breaks end-to-end connectivity, complicates P2P applications, 
  -  Doesn’t work if return traffic bypasses the NAT
  - Breaks apps that expose their IP addresses (FTP)


## 2.4 IPV6

- IPV6 Header

 ```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
 ┌───────┬───────────────┬───────────────────────────────────────┐
 │Version│ Traffic Class │           Flow Label                  │
 ├───────┴───────────────┴───────┬───────────────────────────────┤
 │        Payload Length         │    Protocol   │Hop Limit(TTL) │
 ├───────────────────────────────┴───────────────────────────────┤
 |                         Source Address                        |
 │                           (128 bits)                          │
 ├───────────────────────────────────────────────────────────────┤
 |                      Destination Address                      |
 │                           (128 bits)                          │
 ├───────────────────────────────────────────────────────────────┤
 │                   Payload (TCP/UDP/ICMPv6 Data)               │
 └───────────────────────────────────────────────────────────────┘
 
 ```

> ⚠️
>
>  **Flow Label (20 bits)**：新增字段，用于标识特定数据流的质量服务。
>
>  **Payload Length (16 bits)**：仅指payload长度

-  Incompatible with IPv4
  - Dual stack (speak IPv4 and IPv6)
  - Translators (convert packets)
  - Tunnels (carry IPv6 over IPv4; 路过 IPv4 网络时加个 IPv4 header再上Ethernet)

## 2.5 Routing and Forwarding

-  Routing: deciding the direction to send traffic
-  Forwarding: sending a packet on its way **(longest prefix match)**

### 2.5.1 Routing

- Goal：

  | Property             | Meaning                           |
  | -------------------- | --------------------------------- |
  | **Correctness**      | Finds paths that work             |
  | **Efficient paths**  | Uses network bandwidth well       |
  | **Fair paths**       | Doesn't starve any nodes          |
  | **Fast convergence** | Recovers quickly after changes    |
  | **Scalability**      | Works well as network grows large |

- **Fully Distributed Routing**
  
    - **No central controller** All routers are equal and make independent decisions.  
    - **Local knowledge only** Routers learn about the network by exchanging messages with directly connected neighbors.
    - **Concurrent operation**
    - **Failure tolerance** There may be node/link/message failures. → poor scalability

- **Hierarchical Routing**

    Introduce a larger routing unit. Route first to the **region**, then to the IP prefix within the region.

    - Pros:  
      - Outside a region, nodes have one route to all hosts within the region
      - This gives savings in table size, messages and computation
    - Cons:
      - Each node may have a different route to an outside region
      - Routing decisions are still made by individual nodes

    - **Routing Table**

        - **Static Routing** (Manual Configuration)
        - **Dynamic Routing** RIP (Routing Information Protocol), OSPF (Open Shortest Path First, e.g., Dijkstra), BGP (Border Gateway Protocol).
    
    - **IP Prefix Aggregation and Subnets**
    
        **Goal:** 通过调整 IP prefix 的长度，让 routing table 变小。
    
        Routers can change prefix lengths without affecting hosts.
        
        - **Subnetting** Split large prefix into smaller ones internally, e.g., `/16 → /18`
        - **Aggregation** Join small prefixes into one large prefix externally, e.g., `/18 → /16`
    
### 2.5.2  Routing: Shortest Paths

- **Sink Tree** 

    Sink tree for a destination is the union of all shortest paths towards the destination. 

    **Each node only stores next hop (parent) towards root.**

- **Distance Vector Routing**

    Each node shares distance vectors with neighbors, updates paths using shortest heard distance, and forwards via best next hop.
    $$
    D_x(d)=\min_{v\in N(x)}\{c(x,v)+D_v(d)\}
    $$
    Slow convergence, count-to-infinity, and routing loops occur because nodes only know neighbor info, not full topology, causing outdated routes to propagate and persist.

    > - Adding routes:
    >   - News travels one hop per exchange
    > - Removing routes:
    >   - When a node fails, no more exchanges, other nodes forget
    >
    > Example: A
    >
    > 
    >
    > <img src="assets/image-20260502205537010.png" alt="image-20260502205537010" style="zoom: 33%;" />
    >
    > <img src="assets/image-20260502205811611.png" alt="image-20260502205811611" style="zoom:33%;" />
    >
    > …

    - **RIP (Routing Information Protocol)**

      - DV protocol with hop count as metric
        -  Infinity is 16 hops; limits network size
        -  Includes split horizon (不把 route 发回给你学到它的那个邻居), poison reverse (如果 A 是从 B 学到 D 的，A 就告诉 B：我到 D 是 infinity, i.e., B 不要通过 A 去 D。)
      - Routers send vectors every 30 seconds
        - Runs on top of UDP
        - Time-out in 180 secs to detect failures

      > ⚠️：依旧无法解决routing loops
      >
      > Example: 
      >
      > ```
      > A -> B -> C -> A
      > 
      > A thinks: to D via B
      > B thinks: to D via C
      > C thinks: to D via A
      > ```

- **Link-State Routing**

    1. **Flooding**
    
       - Send an incoming message on to all other neigbors.
    
       - Remember the message so that it is only flooded once.
    
       > Each node learns full topology
    
    2. **Dijkstra**
    
       > Each node computes its own forwarding table
       >
       > ![21_Dijkstra_2](assets/21_Dijkstra_2.png)
       >
       > - Using binary heaps the complexity is O((|E|+|V|)log(|V|)) 
       >
       > - O(|E|+|V|log(|V|)) with Fibonacci heaps
    
    - Adding routes:
    
      - 新的 LSP 被 flood
        所有节点加入新 topology 信息
        重新计算 shortest paths
    
    - Removing routes:
    
      - 相邻节点发现 link down
        生成新的 LSP
        flood 给全网
        所有节点删除这条 link
        重新跑 Dijkstra
        更新 forwarding table
    
    - Pros: 
    
      - Fast convergence (only one round of flooding and computation)
      - No count-to-infinity problem (full topology known)
    
    - Cons:
    
      - Seq. number reaches max, or is corrupted; Node crashes and loses seq. number; Network partitions then heals 
    
        → Include age on LSPs and forget old information that is not refreshed

# 3. Application Layer (09-18)

## 3.1 Peer to Peer

Leverage peer resources: **computation, storage, bandwidth**.  Also emerging: **mobility, coins (tokens), sensors**. 

Decentralized, scalable architecture.

- Tradeoff between possible location of files and searching difficulty

- Storage networks replicate files anywhere, making search difficult, especially with node churn.

- **Framework**  
    - **Join** How to start participating
    - **Publish** How to advertise files
    - **Search** How to find files
    - **Fetch** How to retrieve files

### 3.1.1 **Napster**

Server does all processing & Server maintains $O(N)$ state & Single point of failure

- **Join** Client contacts central server on startup
- **Publish** Reports list of files to central server
- **Search**  Query server → returns peer storing requested file $O(1)$ 
- **Fetch** Get file directly from peer

### 3.1.2 **Gnutella**

Complete decentralization & Query flooding

Search scope is $O(N)$ & Unpredictable search time & No guarantee of finding files (TTL-limited search only works well for haystacks)

- **Join** Client contacts a few existing nodes on startup → these become its "neighbors"
- **Publish** No need (no central index)
- **Search** Ask neighbors → neighbors ask their neighbors → when/if found, reply back along the path; TTL limits propagation $O(???)$ 
- **Fetch** Get file directly from peer

- **Gnutella/KaZaA [Two-level hierarchy]**

    - Kept a centralized registration

    - Supernodes have better connection to Internet and act as temporary indexing servers for other nodes to help improve the stability for the network.

    - Standard nodes connect to supernodes and report list of files.

    > Cons: Kept a centralized registration -> allowed for law suits

| Dimension | Napster | Gnutella | Gnutella/KaZaA (Two-Layer) |
|-----------|-------------|---------------------|--------------------------------|
| **Index** | Central server | No index | Supernodes maintain index (temporary central) |
| **Search** | Query central server | Flooding (ask neighbors) | Flooding between supernodes |
| **Transfer** | ~ | Direct peer-to-peer | ~ |
| **Join** | Contact central server | Find a few neighbors | Find and connect to a supernode |

### 3.1.3 **BitTorrent**

Central tracker server needed to bootstrap swarm.

#### Actions:

- **Join:** contact centralized “tracker” server, get a list of peers.

- **Publish:** Run a tracker server / provide `.torrent` with metadata (file name, size, chunk hashes, tracker URL).

- **Search:** Out-of-band. E.g., use Google to find a tracker.

  > Scalable, no single point of failure.

- **Fetch:** Download chunks of the file from your peers. Upload chunks you have to them.

#### **Roles**:

- **Seeder** Peer with the complete file, only **uploads** to others.

- **Leecher** Peer without the complete file, both **downloads and uploads** to others.

  > **Swarm** = seeders + leechers

- **Tracker** Central server coordinates **peers** (joins, maintains lists), but doesn't store files.

  > ```
  > Client -> Tracker: who has this file?
  > Tracker -> Client: here is a peer list
  > Client <-> Peers: exchange chunks
  > ```

#### **Policies:**

- **Tit-for-tat** Upload to the fastest $N$ peers you download from. 

  > Encourages fairness, discourages freeloading.

- **Optimistic unchoke** Randomly let new peers download to prevents starvation, discovers better partners.

- **Rarest first** Prioritize distributing scarce chunks to improve file availability and resilience.

### 3.1.4 **DHT (Distributed Hash Table; `Chord` if a ring)**

**Goals:** given a key, find the node responsible for that key

- Decentralized: no central authority 
- Scalable: low network traffic overhead 
- Efficient: find items quickly (latency) 
- Dynamic: nodes fail, new nodes join

Decentralized system using **consistent hashing**: keys and nodes hashed onto a ring ($0...2^m-1$). 

> Key identifier = SHA-1(key) → load balancing
>
> Node identifier = SHA-1(IP address) → independent failure

- Each key stored on its successor node. 

-  Each node maintains

  -  Finger table $\log N$

    - Entry i in the finger table of n is the first node that succeeds or equals n + 2i

      > Example:
      >
      > ```
      > For node n, the finger table entries are:
      > finger[0]: successor of n + 1     
      > finger[1]: successor of n + 2      
      > finger[2]: successor of n + 4      
      > ...
      > ```

  - Predecessor node

  -  $O(\log N)$ lookup 

    - Entry $i$ which starts from $1$ points to the first node on the ring that is $\ge x + 2^{i - 1}$

- Pros:

  -  Guaranteed Lookup
  -  $O(\log N)$ per node state and search scope
  - Influenced many future systems; esp. key-value stores

- Cons:

  - Supporting non-exact match search is hard

## 3.2 DSS1: Amazon Dynamo

- **Architecture**

    <img src="assets/8.png" width="60%" height="60%">

- **Partition**
  
    > **Hash partitioning** `partition = hash(key) % partition_count`
    >
    > - Add a node from $N-1→N$: move $\frac{N-1}{N}$ of the keys
    
    - **Consistent hashing** (ring; better) 
    
        - Add a node from $N-1→N$: move $\frac{\text{size of new range (left)}}{\text{size of all ranges (right)}}$ of the keys 

    - **Virtual nodes (vnodes)** Virtual nodes assign multiple ring positions to each physical node, distributing data migration and improving load balancing across all nodes.
    
        - **Heterogeneity** More powerful nodes can have more capacity, thus more vnodes.
    
        - **Token map storage**: All nodes.
    
            - Add a node: **Gossip**
    
                1.  Inform a few nodes about the new node
                2. $1/s$: Choose a random friend, Gossip about new nodes
    
    - **Replication** Dynamo skips nodes to ensure replicas reside on different nodes (set Replication Factor, i.e. $RF$).
    
        > Example: 
        >
        > ```
        > token(row) = hash(row's partition key)
        > 
        > 遇到第一个 node -> 第 1 个 replica
        > 继续走 (可能多步)
        > 遇到下一个不同 node -> 第 2 个 replica
        > 继续走
        > 直到拿够 RF 个 nodes
        > ```
    
    - **Dynamo Reads/Writes** $R/W$ is configurable. 
    
      When $R + W > RF$, the  read and written will overlap, with last write wins (LWW) resolving conflicts. → eventual consistency
    
      > 它只保证**有交集**，不保证读到的某一个 replica 包含所有最新写入。
    
    
      > Example:
      >
      > ```
      > Dynamo Config: RF = 3, W = 2, R = 2
      > 
      > client -> coordinator: put(k, v)
      > 
      > coordinator -> node1: write
      > coordinator -> node2: write
      > coordinator -> node3: write
      > 
      > node1 -> coordinator: ack
      > node2 -> coordinator: ack
      > node3: rebooting / slow / failed
      > 
      > coordinator 已经收到 2 个 ack
      > => coordinator -> client: ack
      > 
      > ack = your data is committed / safe enough by config
      > 
      > ------------------------------
      > 
      > client -> coordinator: get(k)
      > 
      > coordinator -> node1: read
      > coordinator -> node2: read
      > 
      > node1 -> coordinator: B
      > node2 -> coordinator: A
      > 
      > coordinator 发现版本不同
      > => 根据 timestamp / version context / conflict resolution 处理
      > => 返回 value 或 multiple conflicting values
      > ```
      >
      > ⚠️ R = 2 → Read one copy, and only request checksum from others.
    
      | **RF** | R     | W     | Behavior                                                     |
      | ------ | ----- | ----- | ------------------------------------------------------------ |
      | **3**  | **2** | **2** | **Parameters from the Dynamo paper:** Relatively balanced configuration; Good durability, good R/W latency |
      | 3      | 3     | 1     | **Slow reads, weak durability, fast writes** Writes are highly available, therefore fast; Reads will not return data even if one node is down; reads may fail; Risk: If the one node that took the write fails permanently, we'll lose committed data. |
      | 3      | 1     | 3     | **Slow writes, strong durability, fast reads** Reads are highly available, therefore fast; Writes are slow (from client's perspective) as they involve writing to three replicas. |
      | 3      | 3     | 3     | More likely that **reads see all prior writes**              |
      | 3      | 1     | 1     | Read quorum **doesn't overlap** write quorum Speed + availability more important than consistency |
    
    - **Dynamo API**
    
        -  `get (k)` returns **value(s) and context**. It returns multiple versions if conflicts exist. 
           -  The context contains Timestamps to track version history.
        -  `put (k,context,value)` uses the provided context to indicate which previous version(s) this new version supersedes or merges.

### 3.3 Proto1: HyperText Transfer Protocol (HTTP)

- **Web Fetch:**

  1. Resolve the server to IP address (DNS)
  2. Set up TCP connection to the server
  3. Send HTTP request for the page
  4. Await HTTP response for the page
  5. Execute and fetch embedded resources, render
  6. Clean up any idle TCP connections

- **Request**

|Method|Description|
|:--:|:--:|
|$\text{GET}$|Read a Web page|
|$\text{HEAD}$|Read a Web page's header|
|$\text{POST}$|Append to a Web page|
|$\text{PUT}$|Store a Web page|
|$\text{DELETE}$|Remove the Web page|
|$\text{TRACE}$|Echo the incoming request|
|$\text{CONNECT}$|Connect through a proxy|
|$\text{OPTIONS}$|Query options for a page|

- **Response**

|Meaning|Example|
|:--:|:--:|
| **Information** | $\texttt{100}$ Server agrees to handle client's request <br> $\texttt{101}$ Switching protocols |
| **Success**     | $\texttt{200}$ Request succeeded <br> $\texttt{201}$ New resource created <br> $\texttt{204}$ No content present |
| **Redirection** | $\texttt{301}$ Page moved permanently <br> $\texttt{302}$ Temporary redirect <br> $\texttt{304}$ Cached page still valid |
| **Client error**| $\texttt{400}$ Bad request <br> $\texttt{401}$ Authentication required <br> $\texttt{403}$ Forbidden page <br> $\texttt{404}$ Page not found <br> $\texttt{429}$ Too many requests |
| **Server error**| $\texttt{500}$ Internal server error <br> $\texttt{502}$ Bad gateway <br> $\texttt{503}$ Service unavailable, try again later <br> $\texttt{504}$ Gateway timeout |

### 3.3.1 Performance

**Page Load Time (PLT)** 

PLT measures web performance from click to page visible, influenced by **page structure, HTTP/TCP protocols, and network RTT/bandwidth**.

HTTP/1.0 used one TCP connection per web resource.

> Poor PLT:
>
> - Sequential request/responses, even when to different servers
> -  Multiple TCP connection setups (slow-start phases) to the same server
> -  Network is not used effectively, worse with many small resources
>
> To improve PLT:
>
> - Reduce content size for transfer →  Smaller images, gzip
> -  Make better use of the network → Parallel & persistent connections
> - Avoid fetching same content → Caching and proxies 
> - Move content closer to client → CDNs

- **Parallel Connections** Browser runs multiple parallel HTTP instances, pulls in completion time of last fetch.

- **Persistent Connections** Parallel connections compete with each other for network resources. Make one TCP connection to one server and use it multiple HTTP requests.


<img src="assets/image-20260502225209170.png" alt="image-20260502225209170" style="zoom: 33%;" />

- **Web Caching and Proxies**

    - **Cached Content**

        - **Locally** expiry information (expires header) & heuristics (cacheable, fresh, not modified recently) [Content is then available right away]
        - **Server** Last-Modified header / ETag” header [Content is available after 1 RTT (if connection open)]

<img src="assets/image-20260502225804976.png" alt="image-20260502225804976" style="zoom:33%;" />

- **Web Proxies** Place intermediary between clients and server.

### 3.3.2 Domain Name System (DNS)

DNS is a naming service to map between host names and their IP addresses 

- Goals:  Easy to manage & Efficient

- Approach:
  - Distributed directory based on a hierarchical namespace
  - Automated protocol to tie pieces together

<img src="assets/9.png" width="80%" height="60%">

> Example:
>
> ```
> .        root
> com      top-level domain / TLD
> google   second-level domain
> www      host name / subdomain
> ```

- **Top-Level Domains (TLDS)**

    - Run by ICANN (Internet Corp. for Assigned Names and Numbers)

    - 700+ generic TLD & 250+ country-code TLD

- **DNS Zones ** basis for distribution (with authoritative nameservers); Delegating the administration for a part of the DNS namespace

    > Example:
    >
    > ```
    > .edu.cn
    > └── cuhk.edu.cn
    > ```

- **DNS Resolution** Start with the root nameserver and work down zones.

<img src="assets/image-20260502230837254.png" alt="image-20260502230837254" style="zoom: 50%;" />

- **Local Nameservers (as DNS resolver) and Root Nameservers** (with **Replicas**)

    Local nameservers handle client queries and recursion, while root nameservers direct them to the appropriate top-level domain servers.

    Root (dot) is served by 13 **server names** (`a.root-servers.net` to `m.root-servers.net`)

- **Caching** Cached data periodically times out (set appropriate TTL).

    > Common practices:
    >
    > -  Top-level NS records: very high TTL → alleviate load on root 
    > - Intermediary NS records: high TTL 
    > - A records: small TTL (<7200s) → consistency concerns 
    > - Some A records: tiny TTL (<30s) → fault tolerance, load balancing

- **DNS Protocol** `dig www.google.com`

- **DNS Security Extensions (DNSSEC)**

    To DNS spoof, Trudy returns a fake DNS response that appears to be true.

    - RRSIG for digital signatures of records
    - DNSKEY for public keys for validation
    - DS for public keys for delegation

    > Example:
    >
    > ```
    > root .
    >   ↓ DS / DNSKEY
    > .com
    >   ↓ DS / DNSKEY
    > bank.com
    >   ↓ RRSIG
    > www.bank.com A record
    > ```

### 3.3.3 Content Delivery Networks (CDNs)

A CDN uses DNS to direct each client to the nearest replica server based on their IP address.

| browser cache | only useful for one user                        |
| ------------- | ----------------------------------------------- |
| proxy cache   | useful for one organization / ISP / local group |
| CDN           | CDN                                             |

## 3.4 Remote Prcedure Call (RPC)

- **Goal:** make communication appear like a local procedure call: way less painful than sockets

    > A procedure call:
    >
    > - Caller pushes arguments onto stack, jumps to address of callee function
    > - Callee reads arguments from stack, executes, puts return value in register, returns to next instruction in caller
    >
    > RPC：
    >
    > - Client stub marshals arguments (via RPC lib), sends request to server, waits for reply, unmarshals return value  (via RPC lib), returns to caller
    > - Server stub receives request, unmarshals arguments (via RPC lib), calls procedure, marshals return value  (via RPC lib), sends reply to client

- **Challenge:**

    -  Heterogeneity: language, data size, endians, float representation, data alignment 
    - Failure, Performance ($10^3 - 10^6$ slower than a 10-cycle ($3ns$) PC)

- **Interface description language** Mechanism to pass procedure parameters and return values in a machine-independent way (use IDL compiler, marshal and unmarshal).

- **At-Least-Once Scheme** Upon timeout, the client stub retransmits the request. After several failed attempts, it returns an error.

    > Used when read-only operations with no side effects / the application has its own functionality to cope with duplication and reordering

- **At-Most-Once Scheme** 

    Since identical calls may come from different clients, duplicate detection requires a unique `xid` per request.

    > ```c
    > if seen[xid]:            // 这个 xid 是否执行过
    >     retval = old[xid]    // 这个 xid 上次的返回值
    > else:
    >     retval = handler()
    >     old[xid] = retval
    >     seen[xid] = true
    > 
    > return retval
    > ```

    The client includes "seen all replies $\le x$" with every RPC (like **cumulative ACK**), allowing the server to discard outdated `xids` and prevent unbounded state growth.

    A **pending flag** per executing RPC avoids re-running duplicates.

    > ```c
    > if seen[xid]:
    >     return old[xid]
    > 
    > if pending[xid]:
    >     wait_or_ignore()
    > 
    > else:
    >     pending[xid] = true
    >         
    >     retval = handler()
    >     old[xid] = retval
    >     seen[xid] = true
    >         
    >     pending[xid] = false
    >     return retval
    > ```

    To survive crashes, both client and server persist pending/completed RPCs to disk.

- **Exactly-Once** retransmission (At-Least-Once) + deduplication (At-Most-Once) + persistence on both sides for crash recovery. Limitation: not possible with external physical actions.

    > ```c
    > # client side
    > while not received_reply:
    >     send(request with same xid)
    >     wait_or_timeout()
    > 
    > # server side
    > if xid in completed_log:
    >     return old_result[xid]
    > 
    > elif xid in pending:
    >     wait_or_ignore()
    > 
    > else:
    >     mark_pending(xid)
    >     result = handler()
    >     write_completed_log(xid, result)   # durable
    >     return result
    > ```

## 3.5 DSS2: The Google File System (GFS)

- **Target environment**

    - Files are huge, but not many.
    - Write once, read many.
    - I/O bandwidth is more important than latency.

    Typicsal workloads : Bulk Synchronous Processing (BSP).

- **Design Decisions**

    - **Chunk** Use 64MB chunks to amortize seek costs, pushing read throughput close to disk transfer limits for streaming workloads.

      > $$
      > \begin{aligned}
      > T_{\text{read}} 
      > &= T_{\text{seek}} + T_{\text{transfer}}\\
      > &= T_{\text{seek}}↓ + \frac{\text{chunk size↑}}{\text{disk bandwidth}} \\
      > \end{aligned}
      > $$

    - **Replication** Replicate each chunk three times across racks to balance write performance.

    - **Single master** Centralize metadata for coordination.

    - **Record append** Support concurrent appends.

- **General Architecture**

    <img src="assets/10.png" width="60%" height="60%">

    - **Single master**

        **Shadow masters** provide read-only access with slightly stale metadata by replicating the primary's operation log, ensuring availability during primary failure.

        GFS prevents master **overload** by minimizing its involvement: data never passes through it, large chunks reduce metadata ops, and chunk leases delegate write coordination authority to primary replicas.

        > Example:
        >
        > ```
        > 1. client 问 master：这个 chunk 的 replicas 在哪里？谁是 primary？
        > 2. master 返回：A 是 primary，B/C 是 secondaries
        > 3. client 把 data 推给 A/B/C 的 buffer
        > 4. client 发 write command 给 A
        > 5. A 决定写入顺序
        > 6. A 通知 B/C 按同样顺序写
        > 7. B/C ack A
        > 8. A ack client
        > ```

        <table>
        <thead>
            <tr>
            <th width="25%">Category</th>
            <th width="25%">Responsibility</th>
            <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
            <td rowspan="4" style="vertical-align: top;"><strong>Regular Management</strong></td>
            <td><strong>Metadata Storage</strong></td>
            <td>Stores namespaces, file-to-chunk mappings, chunk locations in memory (chunk -> replicas locations).</td>
            </tr>
            <tr>
            <td><strong>Namespace Locking</strong></td>
            <td>Locks directory operations to handle concurrent accesses.</td>
            </tr>
            <tr>
            <td><strong>Periodic Communication</strong></td>
            <td>Heartbeats with chunkservers to monitor health and exchange state.</td>
            </tr>
            <tr>
            <td><strong>Chunk Lifecycle</strong></td>
            <td>Creates chunks (rack-aware); re-replicates when replicas low; rebalances load/space.</td>
            </tr>
            <tr>
            <td rowspan="2" style="vertical-align: top;"><strong>Background Cleanup</strong></td>
            <td><strong>Garbage Collection</strong></td>
            <td>Logs deletion, renames files as hidden, lazily reclaims space.</td>
            </tr>
            <tr>
            <td><strong>Stale Replica Deletion</strong></td>
            <td>Uses version numbers to detect and remove outdated replicas.</td>
            </tr>
        </tbody>
        </table>

- **Chunkserver** Chunkservers store 64MB chunks locally with version numbers and checksums while clients read/write via chunk handle and byte range from master without data caching.

- **Client** GFS client sends control requests to master, caches metadata, but transfers data directly to/from chunkservers without caching file data.

- **File read and write**

  - **Read** Client asks master for chunk locations, then reads data directly from the nearest chunkserver and returns it to the application (**choose one to read**).

    > Nearest: `/d1/r1/n1`
    >
    > ```
    > same node:                          distance = 0
    > different nodes, same rack:         distance = 2
    > different racks, same datacenter:   distance = 4
    > different datacenters:              distance = 6
    > ```

  - **Write** Client gets locations, pushes data to all replicas' buffers, then primary serializes writes and coordinates secondaries before acknowledging (**write all primary and secondaries**).

    > HDFS default policy:
    >
    > - One replica on local node 
    > - 2nd and 3rd replica on two nodes of same remote rack
    > - Additional replicas are randomly placed

- **Fault Tolerance**

  GFS uses heartbeats to detect failures, reduces replica counts, and re-replicates chunks elsewhere to restore full replication.

  - High availability: Fast recovery, Chunk replication, Shadow master
  - Data integrity: Checksum every 64KB block in each chunk
#### GFS/HDFS vs. Dynamo

| Aspect          | GFS / HDFS                                                   | Dynamo                                                       |
| :-------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| Interface       | File system                                                  | Key-value store                                              |
| Assumptions     | Large files, write-once (sequential) read-many               | Small object storage, random write & read                    |
| Primary Targets | Batch processing, high throughput, fault tolerance at scale  | Transactional workloads, data availability & low latency response, conflict resolution |
| Design Choices  | Master-worker architecture, cross-rack replication, relaxed consistency | Peer-to-peer architecture, consistent hashing, eventual consistency |

## 3.6 Time in Distributed Systems

- **Cristian Algorithm**

<img src="assets/image-20260503101349797.png" alt="image-20260503101349797" style="zoom:50%;" />

- **The Lamport Clock Algorithm**

Lamport clocks ignore physical time and only capture the happens-before relationship between events.

**3 Assumptions:**

- 同一个 process 内，如果 a 先发生，b 后发生：`a -> b`
2. 如果 b 是发送消息，c 是接收这条消息：`b -> c`
   
- 如果 a -> b 且 b -> c：`a -> c`

**Algorithm:** Each process $P_i$ maintains a local clock $C_i$. 

- For a local event, $C_i \leftarrow C_i + 1$, then $C_{event} = C_i$. 

- When process $P_i$ sending an message $k$, set $C_k = C_i$. 
- When process $P_j$ receives an message $k$, $C_j \leftarrow \max (c_j,c_k) + 1$.
-  Break ties by appending the process number $P_i$ to each event

If $a \to b$, then $T_a < T_b$. However, **the converse does not hold** ($a → b \text{ or } a || b$) — Lamport timestamps alone cannot be used to infer causal relationships between events.

> And $a||b → \text{nothing}$

- **Totally-Ordered Multicast**

**Assumptions:** No node failures / message loss / message corruption

**Cons:** No scalability, Waits forever for message delays

Totally-ordered multicast ensures identical processing order. Replicas sort queues by Lamport timestamps (dynamically updating the head), broadcast ACKs strictly for this **head**, and execute it once globally acknowledged.

> Algorithm:
>
> ```
> 1. Client 把 update 发给某个 replica
> 
> 2. 该 replica 给 update 分配 Lamport timestamp，
>    然后 broadcast 给所有 replicas，包括自己
> 
> 3. 每个 replica 收到 update 后：
>    - 加入 local queue
>    - queue 按 Lamport timestamp 排序
> 
> 4. 每个 replica 只 ACK 自己 queue head 的 update!!!
> 
> 5. 一个 update 只有满足两个条件才能执行：
>    - 它在本地 queue head
>    - 它收到了所有 replica 的 ACK
> 
> 6. 执行并移除 head 后，
>    新的 head 才可能被 ACK
> ```

- **Vector clock**

Initially all vectors are $[\underbrace{0,0,\cdots,0}_{n \text{ processes}}]$.

For each local event on process $i$, increment local entry $c_i$.

If process $j$ receives message with vector $[d_1,d_2,\cdots, d_n]$, then $c_k = \max (c_k,d_k)$, and increment local entry $c_j$.

| Comparison |                 Lamport Clock                 |                Vector Clock                |
| :--------: | :-------------------------------------------: | :----------------------------------------: |
|   Given    |                 $C(a) < C(z)$                 |               $V(a) < V(z)$                |
| Conclusion |      Either $a \to z$ or $a \parallel z$      |                 $a \to z$                  |
| Precision  | Cannot distinguish causality from concurrency | Precisely captures happens-before relation |


## 3.7 Parallelism Basics and Collective Communication

- $Speed up = \frac{T_{\text{serial}}}{T_{\text{n parallel}}}$

<img src="assets/image-20260503103509290.png" alt="image-20260503103509290" style="zoom:33%;" />

- **Communication patterns**

  - Point-to-point communication
  - Collective communication

- **Model**

  - **Assumptions:**  `任意 worker i  ->  任意 worker j` & `一个 worker 可以一边收数据，一边发数据`

  - **Cost of Communication** $\alpha + n \beta$ (or $\alpha + Mn \beta$ if a message encounters a link that simutaneously accommodates $M$ messages) 

    where $\alpha$ Latency, $\beta = \frac1{B}$ Transfer time per byte, $n$ Message size in bytes, $\gamma$ Computation time per byte for reduction operations

- **Primitive**

| Primitive       | Pattern    | Description                                                  |
| --------------- | ---------- | ------------------------------------------------------------ |
| Broadcast       | One-to-all | One process sends the same data to all processes             |
| Reduce(-to-one) | All-to-one | All processes perform a reduction operation (sum, max, etc.) and send the result to one process |
| Scatter         | One-to-all | One process distributes distinct data chunks to all processes |
| Gather          | All-to-one | All processes send their data to a single process            |
| Allgather       | All-to-all | All processes collect data from all processes (each process gets the full data set) |
| Reduce-scatter  | All-to-all | Perform local reduction first, then scatter results (first half of Allreduce) |
| Allreduce       | All-to-all | All processes perform a reduction operation, and the result is distributed to all processes |

### 3.7.1 **Minimum Spanning Tree Algorithm** (emphasize low latency for small message)

Recursive halving broadcast splits nodes in half sends to opposite half recurses achieving $\log N$ rounds optimizing latency for small messages. 

<img src="assets/12.png" width="50%" height="50%">

Total cost:

- **Broadcast** $\log p (\alpha + n \beta)$
- **Reduce** $\log p  (\alpha + n \beta + n \gamma)$ Compute overhead is required for reduce.
- **Scatter/Gather** $\sum \limits_{k = 1}^{\log p}(\alpha + \frac{n}{2^k}\beta) = \alpha \log p + \frac{p - 1}{p}n \beta$
- **Allgather** Gather + Broadcast = $2  \log p \ \alpha + \log p\ n \beta + \frac{p - 1}{p}n \beta$
- **Reduce-scatter** Reduce + Scatter = $2log p \ \alpha + log p\ n (\beta +  \gamma) + \frac{p - 1}{p}n \beta$
- **Allreduce** Reduce + Broadcast = $2log p \ \alpha + log p\ n (2\beta +  \gamma)$

<img src="assets/13.png" width="50%" height="50%">

### 3.7.2 **Ring Algorithm** (emphasize bandwidth utilization for large message)

The bandwidth term $n \beta$ now dominates.

<img src="assets/14.png" width="50%" height="50%">

Total cost:

- **Broadcast** Scatter + Allgather

  $$
  (\log p + p - 1)\alpha + 2\frac{p - 1}{p}n\beta
  $$
  
- **Reduce** Reduce-scatter + Gather
  $$
  (\log p + p - 1)\alpha + 2\frac{p - 1}{p}n\beta + \frac{p - 1}{p}n\gamma
  $$
  
- **Scatter/Gather** MST-style
  $$
  \log p\ \alpha + \frac{p - 1}{p}n\beta
  $$
  
- **Allgather** 
  $$
  (p - 1)\left(\alpha + \frac{n}{p}\beta\right)
  =
  (p - 1)\alpha + \frac{p - 1}{p}n\beta
  $$
  
- **Reduce-scatter**
  $$
  (p - 1)\left(\alpha + \frac{n}{p}(\beta + \gamma)\right)
  =
  (p - 1)\alpha + \frac{p - 1}{p}n(\beta + \gamma)
  $$
  
- **Allreduce** Reduce-scatter + Allgather
  $$
  2(p - 1)\alpha + \frac{p - 1}{p}n(2\beta + \gamma)
  $$

<img src="assets/15.png" width="50%" height="50%">

**Ring algorithm can not be better for Scatter and Gather.**

> Proof:
>
> Scatter: root has total size $n$, and keeps its own $\frac{n}{p}$.
>
> So the data that must be sent out is:
>
> $$
> n - \frac{n}{p}
> =
> \frac{p-1}{p}n
> $$
>
> Therefore the bandwidth term must be:
>
> $$
> \frac{p-1}{p}n\beta
> $$
>
> So the bandwidth term is the same. The difference is only latency:
>
> $$
> \log p\alpha \quad \text{vs.} \quad (p-1)\alpha
> $$

## 3.8 Distributed ML and LLM Systems

### 3.8.1 Data Parallelism

> Typical ML training:
>
> **Forward propagation → Backward propagation → Weight update**
>
> Example:
> $$
> \theta^{(t)} = \theta^{(t-1)} - \epsilon \cdot \nabla_{\theta} L(\theta^{(t-1)}, D^{(t)})
> $$

Split the training dataset into batches across workers. Each worker keeps a full copy of the same model, computes gradients on its own data batch, and then gradients are aggregated across workers.

> Pattern:
>
> ```
> 1. Partition dataset into batches
> 2. Each GPU runs forward/backward on its own batch
> 3. Aggregate gradients across GPUs
> 4. Update model weights
> ```

**Pros**

- Massively parallelizable & No communication during forward/backward.

**Cons**

- Does not work when the model cannot fit on a single GPU.
- Does not scale when model parameters / gradients are very large.

- **AllReduce**

  |      Method      |  Comm  | Lat$\approx$         | Main issue / advantage                                |
  | :--------------: | :----: | -------------------- | :---------------------------------------------------- |
  | Parameter Server | $2NM$  | $\frac{2MN}{B}$      | Simple but centralized bottleneck                     |
  | Naïve AllReduce  | $N^2M$ | $\frac{MN}{B}$       | Too much all-to-all traffic                           |
  |  Ring AllReduce  | $2NM$  | $\frac{2M}{B}$       | Balanced workload; good bandwidth utilization         |
  |  Tree AllReduce  | $2NM$  | $\frac{2M\log N}{B}$ | Low depth, but parent/internal nodes may be hot spots |

### 3.8.2 Model Parallelism

Data parallelism alone cannot train models that do not fit into one GPU memory → **partition the model**

- **Tensor model parallelism**

<img src="assets/image-20260503121540645.png" alt="image-20260503121540645" style="zoom: 33%;" />

- **Pipeline model parallelism**

  A mini-batch is divided into multiple **micro-batches** so different pipeline stages can work at the same time.

  <img src="assets/image-20260503122541518.png" alt="image-20260503122541518" style="zoom:50%;" />

  Let:

  - $m$: micro-batches; $p$ pipeline stages
  - $t_f$: forward time per micro-batch; $t_b$: backward time per micro-batch

  $$
  \text{BubbleFraction}
  =
  \frac{(p-1)(t_f+t_b)}{m (t_f+t_b) + (p-1)(t_f+t_b)}
  \approx
  \frac{p-1}{m+p-1}
  $$

  > More micro-batches $m$ reduce bubbles, but too many in-flight micro-batches increase  intermediate activation memory usage.

  > Use schedules such as **1F1B** (one forward, one backward) to limit the number of in-flight micro-batches and reduce memory footprint.
  >
  > <img src="https://developer-blogs.nvidia.com/wp-content/uploads/2021/03/Pipeline_schedule_1F1B-1-625x185.png" alt="Scaling Language Model Training to a Trillion Parameters Using Megatron |  NVIDIA Technical Blog" style="zoom: 67%;" />

- **Hybrid parallelism**

  Large systems often combine:

  - Data parallelism across groups of GPUs
  - Tensor parallelism inside each layer
  - Pipeline parallelism across groups of layers

  |          Parallelism           | Pros                                                         | Cons                                                         |
  | :----------------------------: | :----------------------------------------------------------- | :----------------------------------------------------------- |
  |      **Data Parallelism**      | Massively parallelizable; <br>no communication during forward/backward | Model must fit on one GPU; <br/>large parameter communication for updates |
  |  **Tensor Model Parallelism**  | Supports large models; <br/>efficient for parameter-heavy layers | Intermediate communication; <br/>limited scaling             |
  | **Pipeline Model Parallelism** | Supports deep / large models; <br/>can train large batches   | Pipeline bubbles; <br/>activation memory pressure            |

### 3.8.3 ML Serving

- **ML serving**

  Deploy a trained model as an online inference service. →  **forward pass** + massive request volume

- **Goals for model inference**

  - **Auto-scale** to dynamic user requests.

  - **SLO-aware performance**: meet response-time Service-Level Objectives.

    >  Example: 98% of requests should finish within 500 ms.

  - **High throughput**: requests per second (RPS).

  - **Cost-effective**: improve GPU utilization and minimize service cost.

- **Batching**

  Process multiple inference requests together.

  | Batch size | Throughput | Latency |
  | :--------: | :--------: | :-----: |
  |   Small    |   Lower    |  Lower  |
  |   Large    |   Higher   | Higher  |

### 3.8.4 Generative LLM Inference

- **Autoregressive generation**

  LLM inference generates output tokens one by one.

  - **Prefill phase (compute-bound)**: process all input tokens at once.

  - **Decoding phase (memory-bound)**: generate one token per iteration; each token attends to previous tokens.

    > **KV cache**: store attention keys/values from previous tokens to avoid recomputation.

- **Static batching**

  Problems: Requests finish at different iterations → more empty slots

- **Continuous batching**

  Remove finished requests `<EOS>` → Add newly arrived requests immediately → Keep GPU serving batch full

  **Pros** Efficient as higher GPU utilization.

  **Cons** Prefill and decoding may interfere with each other. (TTFT↑ TPOT↑)

  > Because prefill is compute-bound and decoding is memory-bound

### 3.8.5 SOTA LLM Systems

- **LLM inference latency**

  <img src="assets/image-20260503135203568.png" alt="image-20260503135203568" style="zoom: 33%;" />
  $$
  \text{Latency} = \text{TTFT} + \text{TPOT} \times \#\text{OutputTokens}
  $$

  Different applications emphasize different metrics:

  |    Application     |   TTFT target    |         TPOT target         |
  | :----------------: | :--------------: | :-------------------------: |
  |        Chat        |     Low (1s)     | Match reading speed (100ms) |
  |       Search       | Very low (200ms) |     Match reading speed     |
  | Programming / code |     Very low     |       Very low (50ms)       |

- **Disaggregated prefill and decoding **

  Separate prefill and decoding into different instances / GPU pools. → no interference

  **Pros**

  - Turns one mixed SLO problem into two simpler optimization problems:
    - Prefill instance optimizes TTFT & Decoding instance optimizes TPOT.
  - Allows different parallelism strategies and resource allocation for each phase.

  **Cons**

  - Need to transfer KV cache from prefill side to decoding side.
  - End-to-end performance depends on **workload pattern, SLO requirements, parallelism strategy, and resource allocation**.

- **Fast LLM scaling**

  Need fast scaling because LLM serving demand is highly dynamic.

  Reasons:

  - Large models require hundreds of GBs to multiple TBs of memory.
  - There are many models to serve.
  - Request demand can spike quickly.

  Existing serverless inference approaches:

  | Approach                               | Problem                                                 |
  | :------------------------------------- | :------------------------------------------------------ |
  | Load remote models from object storage | **Slow**; bandwidth contention under concurrent loads   |
  | Overprovision GPUs                     | **Expensive**; resource waste when idle                 |
  | Cache models in host memory / SSD      | Cache misses fall back to **slow** SSD / remote loading |

  **Key insights for fast scaling**

  - Use high-speed GPU-cluster interconnects (e.g., RDMA) to **distribute** model weights quickly.

  - Use **model multicast** instead of keeping every model cached everywhere.

    > Example:
    >
    > ```
    > Remote storage -> Node A
    > Node A -> Node B, C, D
    > Node B -> Node E, F
    > ...
    > ```

  - Start inference while model weights are still being loaded (**execute-while-load**).

  - Use **collaborative inference** across nodes during model multicast.

  > FaaScale-style idea: binomial-pipeline model multicast + cooperative inference + GDR-based model transfer from GPU/host memory.

## 3.9 Data Center Networking (DCN)

**Goal:** provide scalable, reliable, low-latency services while keeping utilization high.

|      Component       | Approx. cost | Sub-components                   |
| :------------------: | :----------: | :------------------------------- |
|       Servers        |     ~45%     | CPU, memory, disk                |
| Power infrastructure |     ~25%     | UPS, cooling, power distribution |
|      Power draw      |     ~15%     | Electricity                      |
|       Network        |     ~15%     | Switches, links, transit         |

- **Sever cost**

  - **Uneven application fit** Applications exhaust one resource from CPU, memory, or disk
  - **Long provisioning timescales** demand for a new service can spike quickly.
  - **Session state and storage constraints** make migration harder.

  > 30% utilization are already “good”.

- **Agility: any service, any server**

  Turn servers into a single large **fungible pool**.

  Requirements:

  - **Workload management**: quickly install and run service code on servers.

    > Virtual machines, containers.

  - **Storage management**: let servers access persistent data.

    > Distributed file systems, e.g., HDFS.

  - **Network**: let any server communicate with any other server regardless of where it is physically located.

### 3.9.1 Data Center Servers 

- **Original server model**

  ```
  ┌───────┬───────┐
  │  App  │  App  │
  ├───────┴───────┤
  │     Libs      │
  ├───────────────┤
  │      OS       │
  ├───────────────┤
  │   Hardware    │──> To network
  └───────────────┘
  ```

- **Virtual machines (VMs)**

  **Hypervisor** virtualizes hardware and gives each VM its own virtual hardware.

  - The network thinks multiple hosts are connected.
  - Hypervisor acts as a hub/switch for inter-VM traffic.

  ```
  ┌───────┬───────┐   ┌───────┬───────┐
  │  App  │  App  │   │  App  │  App  │ ┐
  ├───────┴───────┤   ├───────┴───────┤ │
  │     Libs      │   │     Libs      │ ├──> VM
  ├───────────────┤   ├───────────────┤ │  
  │      OS       │   │      OS       │ ┘ 
  ├───────────────┤   ├───────────────┤
  │  Virtual HW   │   │  Virtual HW   │
  ├───────────────┴───┴───────────────┤
  │          Hypervisor + OS          │
  ├───────────────────────────────────┤
  │             Hardware              │──> To network
  └───────────────────────────────────┘
  ```

  - **Overlay address**: virtual IP used by VMs/customers.
  - **Underlay address**: physical host/network location.

  Forwarding between VMs requires a lookup:

  ```
  overlay address `10.10.10.1` ->  underlay physical location `192.1.1.1`
  ```

- **Containers**

  lighter-weight virtualization than VMs.

  - Better packaging than apps by bundling required libraries

  ```
  ┌───────────────┐   ┌───────────────┐
  │      App      │   │      App      │ ┐
  ├───────────────┤   ├───────────────┤ ├──> Container
  │     Libs      │   │     Libs      │ ┘
  ├───────────────┴───┴───────────────┤
  │    Container runtime (Docker)     │
  ├───────────────────────────────────┤
  │                OS                 │
  ├───────────────────────────────────┤
  │             Hardware              │── To network
  └───────────────────────────────────┘
  
  ```

  |      Dimension       | VM                       | Container             |
  | :------------------: | :----------------------- | :-------------------- |
  |          OS          | Each VM has a guest OS   | Share host OS         |
  |      Isolation       | Stronger                 | Lighter-weight        |
  |       Startup        | Slower                   | Faster                |
  | Migration/deployment | Heavier                  | Easier                |
  |       Main use       | Full machine abstraction | App/library packaging |

### 3.9.2 Container Networking

**Goals:**

- Communication with outside world and between containers.

- Avoiding port conflicts among containers on the same host.

- High performance for containers on the same host.

- Virtual private networks between related containers.

- **Host networking**

  Containers share the host's IP address and network stack.

- **Bridge networking**

  Create an internal network for containers on the same host.

  - Containers get private addresses on the bridge.
  - Use NAT to communicate with the outside world.

  > Example:
  >
  > ```
  > Container A              Container B
  > 172.17.0.2               172.17.0.3
  >    eth0                     eth0
  >     |                        |
  >   vethA                    vethB
  >     \                      /
  >      \                    /
  >       ---- docker0 bridge ---- Host NAT ---- outside world
  >               172.17.0.1        192.168.1.10
  > ```

- **Overlay networking**

  Create a private network across containers on different hosts.

  - **VXLAN** Encapsulates virtual network packets over the physical underlay.

  > Example:
  >
  > ```
  > Docker Host 1: 172.31.1.5
  >   Container A: 10.0.0.3
  > 
  > Docker Host 2: 192.168.1.25
  >   Container B: 10.0.0.4
  >   
  > Original packet:
  > 10.0.0.3 -> 10.0.0.4
  > 
  > Encapsulated packet:
  > 172.31.1.5 -> 192.168.1.25
  > [ inside: 10.0.0.3 -> 10.0.0.4 ]
  > ```

  |  Mode   | Main idea                          | Advantage                  | Limitation             |
  | :-----: | :--------------------------------- | :------------------------- | :--------------------- |
  |  Host   | Share host network stack           | Lowest overhead            | Port conflicts         |
  | Bridge  | Internal network on one host + NAT | Simple isolation           | NAT overhead           |
  | Overlay | Virtual network across hosts       | Multi-host private network | Encapsulation overhead |

### 3.9.3 Data Center Network

A rack contains commodity servers and a **top-of-rack (ToR) switch**.

**Modular design:** Preconfigured racks Power, network, and storage cabling.

- **Oversubscription**

  much more demand vs. supply for higher links

  <img src="assets/image-20260503143428436.png" alt="image-20260503143428436" style="zoom: 33%;" />

- **Bandwidth measurements**

  - **Bisection bandwidth**: split nodes into two halves with min cut bandwidth
  - **Full bisection bandwidth**: arbitrary half of nodes can communicate with the other half without blocking.

- **Fat-tree topology**

  <img src="assets/image-20260503143726477.png" alt="image-20260503143726477" style="zoom:33%;" />
  $$
  \text{blocking factor}
  =
  \frac{\#\text{downlinks}}{\#\text{uplinks}}
  $$

  | Topology property | Meaning For switch                                    |
  | :---------------: | :---------------------------------------------------- |
  |   Non-blocking    | Uplinks and downlinks balanced, no oversubscription   |
  |  Oversubscribed   | uplinks < downlinks, upper levels can bottleneck      |
  |     Fat tree      | Scales bandwidth by adding more switches/links upward |

- **Network incast**

  Incast arises from synchronized parallel requests.

- **Mitigations**

  - Reduce TCP minimum retransmission timeout  (often use 200ms >> DC RTT)
  - Increase switch buffer size.
  - Add small randomized delay before replies to desynchronize traffic.

### 3.9.4 Emerging GPU Clusters

- **GPU (Graphics Processing Unit) **

  More ALUs, Better energy efficiency per operation (simpler logic)

- **GPU system architecture**

  <img src="assets/image-20260503144802934.png" alt="image-20260503144802934" style="zoom: 33%;" />

  > GPU compute is extremely fast, so data movement between GPU, CPU memory, storage, and network becomes critical.

- **High-speed interconnect between GPUs**

  - **NVLink**: direct bidirectional GPU-to-GPU interconnect.
  - **NVSwitch**: connects multiple NVLinks to provide all-to-all GPU communication at full NVLink speed  (全连接).
  - **Fat-tree GPU clusters**: general-purpose high bisection bandwidth topology.
  - **Rail-only topology**: GPUs with the **same index** across high-bandwidth domains are connected by rail interconnects.
  - **TPU rack topology (3D torus)**
