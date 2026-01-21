# RAG Architecture for Technical Documentation Q&A

## 1. Objective

Design a **RAG (Retrieval-Augmented Generation)** architecture to answer questions over official technical documentation, optimized for  **low latency** ,  **high availability** , and  **production-grade operation** , starting from an initial volume of **~5,000 documents** and designed to  **scale both in traffic and data volume** .

---

## 2. Overview

The architecture is organized around two clearly separated paths:

* **Serving path** : handles real-time user queries and is latency-critical.
* **Ingestion path** : processes new or updated documents and does not impact query latency.

This separation allows each path to scale independently and keeps system behavior predictable under load.

---

## 3. Key Components

### Serving Path

* **GKE** runs the RAG service as stateless, horizontally scalable pods.
* **Redis (Memorystore)** caches frequent responses in memory.
* **Cloud SQL PostgreSQL + pgvector** stores documents, embeddings, and metadata.
* **LLM** generates the final answer using retrieved context.

---

### Ingestion Path

* **Cloud Storage** stores original documents and scales independently with data volume.
* **Pub/Sub + Dataflow** process new or modified documents in an event-driven manner.
* **Cloud SQL** receives document chunks and embeddings.
* **Firestore** stores pipeline configuration and processing versions.

---

### Governance and Observability

* **Cloud Identity** controls service-to-service access.
* **LangSmith** provides LLM observability and traceability.
* **Logging and metrics** support monitoring and diagnostics.

---

## 4. System Properties

### Performance

**What is achieved**

Fast and consistent responses under load.

**How it is achieved**

* Redis eliminates repeated work with sub-millisecond latency.
* pgvector enables direct semantic search over large documents.
* Embedding indexes (like IVFFlat, or HNSW) keep vector search latency stable as data grows.

### Reliability

**What is achieved**

Continuous availability and data consistency.

**How it is achieved**

* GKE distributes workloads across multiple zones.
* Cloud SQL runs with Primary + Standby and automatic failover.
* Serving and ingestion paths are decoupled.


### Scalability

**What is achieved**

Controlled growth in both query traffic and document volume.

**How it is achieved**

* The serving layer scales horizontally to handle increased read traffic, while ingestion is handled separately and focuses on writes.
* **Cloud SQL is optimized primarily for read workloads** (semantic search queries), while writes are handled by the ingestion pipeline. Database capacity (CPU, memory, and storage) can be vertically upgraded if higher performance or more storage is required, allowing a clear  **cost–performance trade-off** .
* Vector indexes such as **IVFFlat** and **HNSW** enable efficient similarity search over tens or hundreds of thousands of embeddings.
* **Cloud Storage and Firestore are fully managed services** that scale automatically with data volume; they only require multi-region configuration to provide durability and availability without additional operational effort.

---

### Governance and Observability

**What is achieved**

Controlled, auditable, and observable production operation.

**How it is achieved**

* Cloud Identity manages authentication and authorization.
* Firestore versions ingestion configurations.
* LangSmith enables auditing of prompts, latency, and response quality.
* Logs and metrics support continuous monitoring.

## 5. AWS Equivalent Architecture

The same RAG architecture can be implemented on AWS using equivalent managed services, while keeping the core design cloud-agnostic. Key components such as **Kubernetes (open source)** and **Redis** remain unchanged conceptually, enabling portability across cloud providers. **Amazon EKS** replaces GKE for running stateless RAG services, **Amazon RDS for PostgreSQL with pgvector** mirrors Cloud SQL, and **Amazon ElastiCache (Redis)** provides the same in-memory caching capabilities as Memorystore. **Amazon S3** serves as the source of truth for documents, equivalent to Cloud Storage.

The ingestion path preserves the same event-driven pattern: **S3 events and EventBridge** correspond to  **GCS triggers and Pub/Sub** , with **AWS Glue** replacing Dataflow for document processing. **Amazon Bedrock** provides LLMs and embeddings, **IAM and Cognito** cover governance and authentication (equivalent to Cloud Identity), **CloudWatch** replaces Cloud Monitoring and Logging, and **LangSmith** remains the LLM observability layer. This service-to-service mapping allows the architecture to remain flexible, portable, and consistent across clouds.
