AI generated
# Microservice Job Processing System (Python + Flask + Docker)

## Overview

This project implements a simple **2-service microservice architecture** using Python and Flask.

* **API Service**: Acts as a gateway for clients.
* **Worker Service**: Handles background job processing asynchronously.

The system demonstrates:

* HTTP communication between services
* Asynchronous job execution using threads
* Basic job state management
* Docker Compose orchestration

---

## Architecture

```
Client → API Service → Worker Service → (background processing)
                         ↓
                    Job State Storage (in-memory)
```

### Components

#### 1. API Service (`api/`)

* Receives client requests
* Forwards jobs to worker service
* Retrieves job status and results

#### 2. Worker Service (`worker/`)

* Creates and manages jobs
* Processes jobs asynchronously using threads
* Stores job state in memory

---

## Features

* Asynchronous job processing (non-blocking API)
* Job lifecycle states:

  * `pending`
  * `running`
  * `done`
  * `failed`
* Simulated workload:

  * Fibonacci computation
  * Artificial delay (`sleep`)
  * Random failure injection
* RESTful endpoints
* Dockerized services

---

## How It Works

1. Client sends a request to API:

   ```
   POST /job/{number}
   ```

2. API forwards request to Worker:

   ```
   POST /process
   ```

3. Worker:

   * Creates a `Job`
   * Starts a background thread
   * Returns `job_id` immediately

4. Client polls:

   ```
   GET /job/{job_id}
   ```

---

## API Endpoints

### API Service (Port 5000)

#### Create Job

```
POST /job/{number}
```

Response:

```json
{
  "status": "taken",
  "job_id": 1
}
```

---

#### Get Job Status

```
GET /job/{job_id}
```

Response:

```json
{
  "job_id": 1,
  "status": "running",
  "input": 100,
  "output": null
}
```

---

#### List All Jobs

```
GET /list-all
```

---

### Worker Service (Port 5001)

#### Process Job

```
POST /process
Body:
{
  "n": 100
}
```

---

#### Get Job Info

```
GET /info
Body:
{
  "id": 1
}
```

---

#### List All Jobs

```
GET /all
```

---

## Job Model

Each job contains:

* `job_id`
* `status`
* `input`
* `output`
* `init_time`
* `finished_time`
* `mod` (for Fibonacci calculation)

---

## Running the Project

### 1. Build and Run

```bash
docker-compose up --build
```

---

### 2. Test the System

#### Create a job

```bash
curl -X POST http://localhost:5000/job/100
```

#### Get job status

```bash
curl http://localhost:5000/job/1
```

#### List all jobs

```bash
curl http://localhost:5000/list-all
```

---

## Important Notes

* Services communicate using Docker internal DNS:

  ```
  http://worker:5001
  ```
* Do NOT use `localhost` between containers
* Worker uses in-memory storage (data is lost on restart)
* Threading is used for async execution (not production-grade)

---

## Limitations

* No persistence (no database)
* Not thread-safe under heavy load
* No retry or queue system
* No authentication or validation
* Uses Flask development server

---

## Possible Improvements

* Add Redis or database for persistence
* Replace threading with a real job queue (Celery, RabbitMQ)
* Add retry and timeout handling
* Implement pagination and filtering
* Add structured logging
* Add health check endpoints

---

## Summary

This project demonstrates a minimal but functional **microservice system** with:

* Service-to-service communication
* Asynchronous processing
* API gateway pattern
* Docker-based deployment

It serves as a foundation for building more advanced distributed systems.
