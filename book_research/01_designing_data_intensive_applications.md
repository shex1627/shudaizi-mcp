# Designing Data-Intensive Applications — Martin Kleppmann (2017)

**Skill Category:** Architecture & System Design / Data Systems
**Relevance to AI-assisted / vibe-coding workflows:** Foundational for any architecture planning involving databases, distributed systems, or data pipelines — helps agents avoid naive storage and consistency decisions.

---

## What This Book Is About

DDIA is a practitioner's map of the landscape of data systems. It covers how databases, caches, message queues, batch processors, and stream processors actually work under the hood — and, more importantly, what tradeoffs each design choice implies. The book is organized in three parts:

1. **Foundations of Data Systems (Chapters 1-4):** Reliability, scalability, and maintainability as guiding principles. Data models (relational, document, graph). Storage engines (log-structured vs. page-oriented / B-trees vs. LSM-trees). Encoding and evolution (schema evolution, backward/forward compatibility).

2. **Distributed Data (Chapters 5-9):** Replication (single-leader, multi-leader, leaderless). Partitioning/sharding strategies. Transactions and their guarantees. The trouble with distributed systems (unreliable networks, clocks, and process pauses). Consistency and consensus algorithms (linearizability, causal consistency, total order broadcast, Paxos/Raft).

3. **Derived Data (Chapters 10-12):** Batch processing (MapReduce, dataflow engines like Spark). Stream processing (event logs, change data capture, event sourcing). The future of data systems — unbundling the database, end-to-end correctness arguments.

Kleppmann's through-line is that there is no single "best" system — every choice is a tradeoff, and understanding the tradeoff space is more valuable than memorizing any particular technology.

---

## Key Ideas & Mental Models

### 1. Reliability, Scalability, Maintainability (RSM)
The three pillars for evaluating any data system. Reliability means continuing to work correctly under faults. Scalability means having strategies for handling growth. Maintainability means making life easier for future engineers. These three properties should be the first-order evaluation criteria when selecting or designing any system.

### 2. Data Models Shape Your Thinking
The relational model, document model, and graph model each make certain queries natural and others awkward. Choosing a data model is choosing which relationships are easy to express and which require workarounds. This is not a purely technical decision — it shapes how developers think about the domain.

### 3. Storage Engine Internals Matter
Understanding the difference between B-tree and LSM-tree storage engines is not academic trivia. B-trees (used by PostgreSQL, MySQL/InnoDB) optimize for read-heavy workloads with in-place updates. LSM-trees (used by RocksDB, Cassandra, LevelDB) optimize for write-heavy workloads with append-only writes and background compaction. Choosing the wrong engine class for your access pattern leads to performance problems that no amount of indexing can fix.

### 4. Schema-on-Read vs. Schema-on-Write
Document databases and schema-less stores push schema enforcement to read time. Relational databases enforce it at write time. Neither is inherently better; they make different failure modes more or less likely. Schema-on-write catches data quality issues early; schema-on-read provides flexibility for heterogeneous or rapidly evolving data.

### 5. Replication Topologies and Their Failure Modes
- **Single-leader replication:** Simple, strong consistency possible, but the leader is a bottleneck and single point of failure for writes.
- **Multi-leader replication:** Better write availability across datacenters, but introduces write conflicts that must be resolved (last-write-wins, merge functions, CRDTs).
- **Leaderless replication (Dynamo-style):** High availability, tunable consistency via quorums (R + W > N), but vulnerable to stale reads, write conflicts, and sloppy quorums.

### 6. Partitioning Strategies
- **Key-range partitioning:** Enables efficient range scans, but prone to hot spots if access patterns cluster on certain key ranges.
- **Hash partitioning:** Distributes load more evenly, but destroys ordering — range queries require scatter-gather across all partitions.
- **Compound partitioning:** Use one column for partition key (hash-distributed) and another for sort key within the partition (range-scannable). This is the approach Cassandra uses.

### 7. Transaction Isolation Levels (The Hierarchy)
One of the most practically important sections of the book. Kleppmann clarifies the confusing zoo of isolation levels:
- **Read Committed:** No dirty reads, no dirty writes. The default in many databases. Still allows non-repeatable reads.
- **Snapshot Isolation (MVCC):** Each transaction sees a consistent snapshot. Prevents non-repeatable reads. Called "repeatable read" in PostgreSQL (but note: the SQL standard's definition of "repeatable read" is different and weaker).
- **Serializable:** Transactions behave as if executed one at a time. Three implementation approaches: actual serial execution (single-threaded, e.g., Redis, VoltDB), two-phase locking (2PL), serializable snapshot isolation (SSI, optimistic, used in PostgreSQL's serializable mode).

### 8. The Trouble with Distributed Systems
Chapter 8 is a masterclass in pessimism. Networks are unreliable (packets get lost, delayed, reordered, duplicated). Clocks are unreliable (clock skew, NTP issues, leap seconds). Processes pause (GC pauses, VM live migration, context switches). The practical upshot: you cannot rely on timeouts alone for failure detection, you cannot trust timestamps for ordering, and you cannot assume that a node that was the leader five seconds ago is still the leader now.

### 9. Consistency Models (The Spectrum)
- **Linearizability:** The strongest single-object consistency model. Behaves as if there is a single copy of the data. Required for leader election, distributed locks, uniqueness constraints. Expensive — requires coordination.
- **Causal consistency:** Preserves cause-and-effect ordering without the overhead of linearizability. Can be implemented without global coordination in some cases.
- **Eventual consistency:** The weakest useful guarantee. Only promises that if no more writes happen, all replicas will eventually converge. Provides no bound on how long "eventually" takes.

### 10. The CAP Theorem — And Why It Is Misleading
Kleppmann argues that the CAP theorem as popularly stated ("pick two of three: consistency, availability, partition tolerance") is misleading. In practice, network partitions are not optional — they happen. The real choice is between consistency and availability *during a partition*. More importantly, CAP only addresses one narrow form of consistency (linearizability) and one narrow form of availability. Real systems make much more nuanced tradeoffs that CAP does not capture. Kleppmann prefers talking about concrete tradeoffs rather than invoking CAP.

### 11. Consensus and Total Order Broadcast
Consensus (getting distributed nodes to agree on a value) is equivalent to several other problems: total order broadcast, atomic commit, leader election, and linearizable compare-and-set. Algorithms like Paxos, Raft, and Zab (ZooKeeper) solve consensus. They are the foundation of systems like etcd, ZooKeeper, and Consul.

### 12. Batch and Stream Processing as Data Integration
Part 3 reframes batch and stream processing not as niche big-data concerns but as fundamental tools for data integration. The key insight: derived data (materialized views, caches, search indexes, denormalized copies) should be treated as derivations from a system of record, recomputable at any time. This makes the system more maintainable and auditable.

### 13. Event Sourcing and Change Data Capture (CDC)
Rather than mutating a database in place and losing history, capture every change as an immutable event. CDC extracts the sequence of changes from a database's write-ahead log and feeds them to downstream consumers (search indexes, caches, analytics). Event sourcing stores the event log as the primary source of truth, deriving current state by replaying events.

### 14. The "Unbundled Database" Vision
Kleppmann's most forward-looking idea: instead of one monolithic database trying to be everything, compose a system from specialized components (a log for ordering, a store for state, an index for queries) connected by reliable data flows. This is essentially the architecture Kafka + stream processing enables.

---

## Patterns & Approaches Introduced

| Pattern | Description | When to Use |
|---|---|---|
| **Write-ahead log (WAL)** | Append changes to a durable log before applying to the main data structure. Enables crash recovery and replication. | Any system that needs durability and recoverability. |
| **SSTables + LSM-trees** | Sorted, immutable on-disk segments merged in the background. | Write-heavy workloads, time-series data, event logging. |
| **MVCC (Multi-Version Concurrency Control)** | Keep multiple versions of each row; readers see a consistent snapshot without blocking writers. | Any transactional system needing concurrent reads and writes (PostgreSQL, MySQL/InnoDB). |
| **Quorum reads/writes** | Require W + R > N to guarantee overlap between write and read replica sets. | Leaderless replication (Dynamo, Cassandra, Riak). |
| **Consistent hashing / hash ring** | Map keys to partitions using a hash ring to enable adding/removing nodes with minimal data movement. | Distributed key-value stores, caching layers. |
| **Change Data Capture (CDC)** | Extract a stream of changes from a database's internal log and feed it to downstream systems. | Keeping search indexes, caches, or analytics stores in sync with a primary database. |
| **Event sourcing** | Store every state change as an immutable event; derive current state by replaying events. | Audit-sensitive domains (finance, healthcare), systems requiring temporal queries. |
| **Lambda architecture** | Run batch and stream processing in parallel; merge results. | Superseded by the Kappa architecture in most cases, but historically important. |
| **Kappa architecture** | Use a single stream processing pipeline for both real-time and reprocessing (by replaying the log). | Preferred over Lambda when the stream processor can handle reprocessing. |
| **Saga pattern (implied)** | Coordinate multi-service operations via a sequence of local transactions with compensating actions. | Microservices that cannot use distributed transactions. |
| **Idempotent operations** | Design operations so that applying them multiple times has the same effect as applying them once. | Any system with at-least-once delivery (message queues, retries). |
| **Fencing tokens** | Include a monotonically increasing token with lock grants; reject operations with stale tokens. | Preventing split-brain in leader election and distributed locking. |

---

## Tradeoffs & Tensions

### Consistency vs. Availability vs. Latency
The real tradeoff triangle. Stronger consistency requires more coordination, which increases latency and reduces availability during partitions. Most production systems choose a point on the spectrum rather than an extreme.

### Normalization vs. Denormalization
Normalized data avoids update anomalies but requires joins. Denormalized data is faster to read but creates consistency risks on writes. The book treats this as a fundamental tension without a universal answer — the right choice depends on the read/write ratio and the cost of stale or inconsistent data.

### Single-leader vs. Multi-leader vs. Leaderless
Each replication strategy makes a different tradeoff between write throughput, read consistency, availability, and operational complexity. There is no objectively best choice.

### Synchronous vs. Asynchronous Replication
Synchronous: the leader waits for follower acknowledgment before confirming a write. Guarantees data is on multiple nodes but increases write latency and reduces availability if a follower is slow. Asynchronous: faster writes, but a failed leader can lose confirmed writes. Semi-synchronous (one sync follower, rest async) is a practical middle ground.

### Transactions vs. Performance
Serializable transactions provide the strongest guarantees but have the highest performance cost. Many systems default to weaker isolation levels for performance reasons, pushing complexity to the application layer. The book argues that developers should understand what guarantees they are actually getting, not just what the documentation claims.

### Schema Flexibility vs. Data Integrity
Document stores (MongoDB, CouchDB) offer flexibility but shift validation responsibility to the application. Relational databases enforce constraints but make schema migrations painful. The tradeoff is between developer velocity now and data quality assurance over time.

### Batch vs. Stream Processing
Batch processing (MapReduce, Spark) provides high throughput and simple fault tolerance (rerun failed tasks) but adds latency (process data in chunks). Stream processing provides lower latency but makes fault tolerance and exactly-once semantics harder to achieve.

### Derived Data: Push vs. Pull
Materialized views and caches can be updated eagerly (push, via CDC/triggers) or lazily (pull, compute on read). Push gives fresher data but requires infrastructure for change propagation. Pull is simpler but can serve stale data or hit performance problems under load.

---

## What to Watch Out For

### Common Misconceptions the Book Corrects
- **"NoSQL is better/worse than SQL"** — The book demolishes this false dichotomy. Different data models solve different problems. Many "NoSQL" databases have added SQL-like query languages; many SQL databases support document-like JSON columns.
- **"Eventual consistency is fine for everything"** — Eventual consistency is appropriate for many use cases but dangerous for others (e.g., account balances, inventory counts, unique constraint enforcement). The book emphasizes understanding *what* can go wrong, not just assuming convergence.
- **"Distributed transactions solve everything"** — Two-phase commit (2PC) is a blocking protocol. If the coordinator fails, participants hold locks indefinitely. This is why many modern systems avoid 2PC across service boundaries.
- **"CAP means you pick two"** — As discussed above, this framing is misleading. Partitions are not optional, and the real design space is much richer than three binary choices.

### Pitfalls for AI-Assisted Development
- **Defaulting to a single database for everything:** An AI coding agent might reach for PostgreSQL by reflex. The book provides a framework for knowing when a document store, graph database, or time-series database would be more appropriate.
- **Ignoring replication lag:** Code that reads immediately after writing may work in development (single-node) and fail in production (replicated). The book catalogs the specific anomalies that arise from replication lag (read-your-writes, monotonic reads, consistent prefix reads).
- **Confusing isolation levels:** The SQL standard's definitions of isolation levels are ambiguous. PostgreSQL's "repeatable read" is actually snapshot isolation. MySQL's "repeatable read" (InnoDB) uses next-key locking, which is different again. The book provides a clear taxonomy.
- **Underestimating clock skew:** Using timestamps for ordering events across nodes is unreliable. Logical clocks (Lamport timestamps, vector clocks) or hybrid logical clocks are needed for causal ordering.
- **Naive sharding decisions:** Partitioning by a monotonically increasing key (e.g., auto-increment ID, timestamp) creates hot spots on the partition that handles the latest data. The book explains why and offers alternatives.

---

## Applicability by Task Type

### Architecture Planning
**Extremely high relevance.** This is the book's primary use case. It provides the vocabulary and mental models needed to evaluate database choices, replication strategies, partitioning schemes, and consistency requirements. Any architecture decision involving data storage or data flow should be informed by the tradeoff frameworks in this book.

### Data Modeling & Schema Design
**High relevance.** Chapters 2-4 directly address data model selection (relational vs. document vs. graph), encoding formats (JSON, Avro, Protobuf, Thrift), and schema evolution strategies. The discussion of normalization vs. denormalization tradeoffs is particularly useful.

### API Design
**Moderate relevance.** The book does not focus on API design per se, but its treatment of encoding/serialization, backward/forward compatibility, and schema evolution (Chapter 4) directly informs API versioning strategies. The discussion of idempotency is critical for designing reliable API endpoints.

### Feature Design on Existing Systems
**High relevance.** When adding features to an existing system, understanding the underlying storage engine, replication topology, and transaction isolation level is essential for predicting how the new feature will behave under load and failure conditions. The book's catalog of "things that can go wrong" is a checklist for feature design reviews.

### Bug Diagnosis & Fixing (Especially Data Consistency Bugs)
**Very high relevance.** Many of the hardest bugs in production systems are data consistency bugs caused by replication lag, weak isolation levels, clock skew, or race conditions in distributed systems. The book provides a systematic framework for reasoning about these bugs: what anomaly is being observed, what guarantee is being violated, and what mechanism would prevent it.

### Writing Technical Documentation
**Moderate relevance.** The book's precise vocabulary (linearizability vs. serializability, consistency vs. consensus, partition vs. shard) is useful for writing clear technical documentation. Its diagrams and explanations of failure modes can serve as templates for documenting the consistency guarantees of your own systems.

---

## Relationship to Other Books in This Category

| Book | Relationship to DDIA |
|---|---|
| **"Database Internals" by Alex Petrov (2019)** | Goes deeper into storage engine internals (B-trees, LSM-trees, buffer management). Complements DDIA's broader survey with implementation-level detail. |
| **"Understanding Distributed Systems" by Roberto Vitillo (2022)** | A more concise, accessible introduction to distributed systems. Good as a primer before DDIA or as a quick reference after. |
| **"Distributed Systems" by Maarten van Steen & Andrew Tanenbaum** | The academic textbook on distributed systems. More theoretical and comprehensive than DDIA but less focused on practical engineering tradeoffs. |
| **"Site Reliability Engineering" (Google SRE book)** | Focuses on operating systems at scale. DDIA explains *why* systems behave the way they do; the SRE book explains *how* to keep them running. |
| **"Building Microservices" by Sam Newman** | Covers the architectural patterns around microservices. DDIA provides the data layer foundation that microservices architectures depend on (service-to-service data flow, event-driven architectures, saga patterns). |
| **"System Design Interview" by Alex Xu** | Uses many concepts from DDIA in a more applied, interview-prep format. DDIA provides the deeper understanding behind the patterns Xu describes. |
| **"A Philosophy of Software Design" by John Ousterhout** | Focuses on software complexity at the module/interface level. DDIA addresses complexity at the system/infrastructure level. Complementary perspectives on the same enemy: complexity. |

---

## Freshness Assessment

**Publication date:** March 2017 (O'Reilly).
**Core content durability:** Very high. The fundamental tradeoffs (consistency vs. availability, normalization vs. denormalization, B-trees vs. LSM-trees) have not changed and are unlikely to change.

### What Has Remained Fully Current
- Transaction isolation level taxonomy and anomalies
- Replication strategies and their failure modes
- The limitations of the CAP theorem
- Encoding and schema evolution principles
- The "trouble with distributed systems" (Chapter 8) — networks and clocks are still unreliable
- Batch and stream processing architectural patterns

### What Has Evolved Since 2017
- **Cloud-managed databases:** Services like AWS Aurora, Google Cloud Spanner, Azure Cosmos DB, CockroachDB, and PlanetScale have changed the operational landscape. Spanner notably offers externally consistent (linearizable) distributed transactions at global scale, which was considered impractical when the book was written. Aurora separates storage and compute in ways that blur traditional replication categories. Cosmos DB offers tunable consistency with five well-defined levels.
- **NewSQL maturity:** CockroachDB, TiDB, and YugabyteDB have matured significantly. They offer distributed SQL with serializable isolation, reducing the need to choose between relational features and horizontal scalability.
- **Kafka ecosystem:** Kafka Streams, ksqlDB, and Kafka Connect have made the "unbundled database" vision more practical. Kafka's move toward KRaft (replacing ZooKeeper) is relevant to the consensus discussion.
- **Serverless databases:** Neon (serverless Postgres), PlanetScale (serverless MySQL), DynamoDB on-demand, and similar offerings have changed the scalability/cost tradeoff for smaller workloads.
- **OLAP evolution:** ClickHouse, DuckDB, Apache Datafusion, and the broader columnar/analytics engine space have matured considerably since 2017. The book's treatment of column-oriented storage is still valid but the tooling landscape has expanded.
- **Multi-model databases:** The convergence trend has accelerated. PostgreSQL now has strong JSON support, MongoDB has added multi-document ACID transactions, and many databases support both document and relational paradigms.
- **CRDTs and local-first software:** Kleppmann himself has been leading research on CRDTs and local-first software since the book's publication. This work extends the book's discussion of conflict resolution in multi-leader replication.
- **Exactly-once stream processing:** Apache Flink and Kafka Streams have made exactly-once semantics more practical than the book's treatment suggests (though the underlying idempotency mechanisms are as the book describes).

### Recommendation
The book remains the single best resource for understanding data systems tradeoffs. Supplement it with awareness of cloud-managed database capabilities (especially Spanner's external consistency model and Aurora's storage-compute separation) and the maturation of NewSQL databases when making architecture decisions in 2024+.

---

## Key Framings Worth Preserving

> **"An application has to meet various requirements in order to be useful. There are functional requirements (what it should do) and nonfunctional requirements (general properties like security, reliability, compliance, scalability, compatibility, and maintainability)."**
> Used to frame the entire book. Architecture is about meeting nonfunctional requirements, not just making features work.

> **"Reliability means making systems work correctly, even when faults occur."**
> Distinguishes faults (component-level deviations) from failures (system-level inability to serve). The goal is fault tolerance, not fault prevention.

> **"The architecture of systems that operate at large scale is usually highly specific to the application — there is no such thing as a generic, one-size-fits-all scalable architecture."**
> A direct counter to the tendency (in interviews and AI-generated designs) to apply generic "scalable" patterns without understanding the specific workload.

> **"Impossibility results and pessimism about distributed systems are of huge practical value."**
> Understanding what is impossible (e.g., consensus in an asynchronous system with even one faulty node, per FLP) helps engineers stop searching for nonexistent silver bullets and focus on practical tradeoffs.

> **"If your application can tolerate temporarily reading stale data, eventual consistency may be acceptable. But if the cost of reading stale data is high, you need a stronger consistency guarantee."**
> The essential decision framework for choosing consistency levels. The question is not "which consistency model is best?" but "what is the cost of stale or inconsistent data in this specific use case?"

> **"Transactions are an abstraction layer that allows an application to pretend that certain concurrency problems and certain kinds of hardware and software faults don't exist."**
> Reframes transactions as a simplifying abstraction, not a performance tax. The question is not "should we use transactions?" but "what is the cost of not using them?"

> **"The main reason for wanting to partition data is scalability. Different partitions can be placed on different nodes in a shared-nothing cluster."**
> Grounding principle: do not partition prematurely. Partitioning adds complexity (cross-partition queries, rebalancing, hot spots). Only partition when a single node cannot handle the workload.

> **"CDC ensures that all changes made to the system of record are also reflected in the derived data systems, so that the derived systems have an accurate copy of the data."**
> The foundational principle behind modern data mesh and data platform architectures. Derived data should be recomputable, not manually synchronized.

> **"Don't think of batch and stream processing as separate; think of them as different points on a spectrum of data processing latency."**
> Dissolves the artificial boundary between "real-time" and "batch" systems. The same logical computation can be executed at different latency points depending on requirements.

---

*This reference document was compiled from the book's content, author talks, and widespread community discussion of its key concepts. It is intended as a practical aid for architecture decisions, not a substitute for reading the book.*
