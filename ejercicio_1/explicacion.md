# RAG Architecture for Technical Documentation Q&A

## 1. Objective

Design a **RAG (Retrieval-Augmented Generation)** architecture to answer questions over official technical documentation, optimized for **low latency**, **high availability**, and **production-grade operation**, starting from an initial volume of **~5,000 documents** and designed to **scale both in traffic and data volume**.

---

## 2. Overview

The architecture is organized around two clearly separated paths:

* **Serving path**: handles real-time user queries and is latency-critical.
* **Ingestion path**: processes new or updated documents and does not impact query latency.

This separation allows each path to scale independently and keeps system behavior predictable under load.

---

# 3. Architecture

This architecture shows how a chatbot can answer business questions based on business documents using a **Retrieval-Augmented Generation (RAG)** flow, and how documents are continuously ingested and monitored in a production environment.

The system is composed of four main areas:

1. User Input
2. Query Retrieval
3. Document Ingestion
4. Monitoring & Observability

---

## 3.1 User Input

The user is the starting point of the system.

A user can provide input in different formats, such as:

* Text (chat, search bar)
* Voice
* Documents
* Images or other media

Regardless of the format, the goal is always the same:
**capture the user’s intent and convert it into a query the system can process**.

At this stage, no retrieval or reasoning happens yet — the input is simply received and forwarded to the retrieval pipeline.

---

## 3.2 Query Retrieval Module

This module is responsible for **turning a user question into an answer**, using previously ingested knowledge.

It runs in real time and is optimized for fast responses.

The core API is implemented using **FastAPI**, an industry-standard framework for building high-performance APIs.

**Cloud execution options**

* **GCP:** Cloud Run or Google Kubernetes Engine (GKE)
* **AWS:** AWS Lambda or Amazon Elastic Kubernetes Service (EKS)

---

### 3.2.1 Preparing (Query Processing & Embedding)

This is the first step after receiving the user input.

Here, the system:

* Receives the input through an API
* Prepares the input:

  * If the input is a PDF, extracts the relevant information
  * If the input is audio, converts it to text
* Converts the processed input into a semantic representation (embedding)

In simple terms, this step adapts and translates **human language into something the system can search with**.

---

### 3.2.2 Retrieval (Find Relevant Information)

Once the query is prepared, the system searches the knowledge base by comparing the semantic similarity of the user question against stored document embeddings.

It is also possible to integrate **hybrid search**, combining:

* Semantic vector search
* Keyword-based search such as **BM25** or **TF-IDF**

This improves recall and robustness, especially for technical or structured content.

---

### 3.2.3 Ranking

In this step, the system:

* Compares the retrieved chunks
* Selects the most relevant ones
* Removes noise and low-quality matches

Typically, this is implemented as:

* An initial retrieval pool
* Followed by a re-ranking algorithm that selects the highest-relevance results

This ensures only the best context is passed to the language model.

---

### 3.2.4 Function Calling & Prompt Engine

This is where the final response is prepared.

The system:

* Builds a structured prompt
* Injects the selected document context
* Optionally triggers functions or tools if required
* Sends everything to the language model

The language model then generates an answer **grounded only in the retrieved documentation**, which is returned to the user as output.

---

## 3.3 Ingestion Module

The ingestion module is responsible for **feeding knowledge into the system**.

It operates independently from user queries and runs whenever documents are uploaded or updated.

Documents are uploaded by users or systems into cloud storage (such as Amazon S3 or Google Cloud Storage). This upload can trigger an event (for example, **Pub/Sub** or **EventBridge**) that starts a background job responsible for transforming documents into searchable knowledge.

PostgreSQL is used as the storage layer, since it supports:

* General relational database functionality
* Vector search through vector extensions and indexing

This approach allows efficient semantic search across thousands of embeddings and is available in both **Amazon RDS** and **Cloud SQL**.

---

### 3.3.1 Document Upload & Storage

Documents such as:

* PDFs
* Markdown files
* Word documents

are uploaded by users or systems and stored in cloud storage.

This storage acts as the **source of truth** for all documentation.

---

### 3.3.2 Parsing

Raw documents are not immediately usable.

In this step, the system:

* Extracts text from documents
* Identifies structure (titles, sections, tables)
* Enriches content with metadata (source, version, type)

---

### 3.3.3 Transformation (Chunking)

Large documents are split into smaller pieces.

Each chunk:

* Represents a coherent piece of information
* Can be independently searched and retrieved

This improves retrieval precision and leads to more accurate answers.

---

### 3.3.4 Indexing (Embedding & Storage)

Each chunk is converted into an embedding and stored in the vector database.

At this point, the document becomes **searchable knowledge** that the query retrieval module can use to answer user questions.

---

## 3.4 Monitoring & Alerts (LLMOps + Reliability)

Monitoring spans across the entire system.

It covers both:

* **LLMOps concerns** (prompt quality, latency, model behavior), which can be integrated with tools like **LangSmith**
* **Software reliability concerns** (errors, timeouts, system health)

Alerts can be triggered, for example:

* When error rates exceed a defined threshold
* When latency increases unexpectedly

Dashboards provide visibility into system metrics and overall health.

The monitoring layer tracks:

* End-to-end request latency
* Retrieval quality
* Prompt execution and model responses
* Failures and anomalies

---

## 4. System Properties

### Performance

* If consistent performance across different regions is important, Kubernetes (GKE/EKS) is typically a good fit. If not, serverless options like Cloud Run or AWS Lambda can simplify operations.
* If repeated questions are common, **Redis** can improve performance by caching frequent queries and responses.
* **pgvector** enables direct semantic search over large document collections.
* Vector indexes (such as **IVFFlat** or **HNSW**) help keep search latency stable as the embedding set grows.

### Reliability

* Distribute workloads across multiple zones for higher availability.
* Cloud SQL or RDS can be configured with replicas (and appropriate read/write patterns) to improve availability and reduce load on the primary database.
* Serving and ingestion paths remain decoupled, avoiding ingestion spikes impacting user latency.

### Scalability

* The serving layer scales horizontally by spawning multiple instances based on demand.
* Managed PostgreSQL services (RDS / Cloud SQL) can scale vertically (CPU, memory, storage) as needs grow.
* Vector indexes such as **IVFFlat** and **HNSW** enable efficient similarity search over tens or hundreds of thousands of embeddings.
* Chat history and user state are often a better fit for NoSQL databases (less structured, high throughput), such as **Firestore** or **DynamoDB**.

### Governance and Observability

* **Cloud Identity (GCP)** or **Cognito (AWS)** can manage authentication and authorization.
