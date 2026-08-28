# Enterprise Notification Scheduler

This module acts as the delivery coordinator for the Notification system. Once the `AlertPolicyEngine` approves a notification, it is passed to this Scheduler. The scheduler determines *when* the notification should be dispatched, handles retries upon failure, and ensures high-priority messages are sent first.

## Architecture
- **Queue (`queue.py`)**: `MemoryPriorityQueue` is an async-safe priority queue. Jobs are sorted first by their `NotificationPriority` (EMERGENCY = highest), and second by their `execution_time`.
- **Policy (`policy.py`)**: Contains `RetryPolicy` (calculates exponential backoff times) and `SchedulingPolicy` (determines when a deferred or immediate job should run).
- **Dispatcher (`dispatcher.py`)**: The background worker that pulls ready jobs from the queue. If a job fails during execution, the dispatcher calculates the next retry time and puts it back in the queue.
- **Executor (`executor.py`)**: A wrapper that triggers the actual delivery (via `NotificationManager`) and updates the job's state.
- **Job & State (`job.py`, `state.py`)**: `ScheduledNotification` tracks the lifecycle of a request as it moves through states (`QUEUED`, `WAITING`, `RUNNING`, `COMPLETED`, `FAILED`).
- **Registry (`registry.py`)**: Provides a global lookup table for checking the status of any scheduled job.
- **Scheduler (`scheduler.py`)**: The main entry point to ingest new notifications and the `tick()` method to process the queue.

## Use Cases
- **Priority Routing**: An `EMERGENCY` notification queued 1 second ago will always jump ahead of 100 `LOW` priority notifications that were queued 10 minutes ago.
- **Exponential Backoff**: If the Firebase API is down, the first retry happens in 1 minute, the second in 2 minutes, the third in 4 minutes, preventing our servers from spamming a failing external API.
- **Deferred Delivery**: If the Policy Engine decides to `DEFER` a notification due to a cooldown rule, the scheduler holds it in the `WAITING` state until the execution time arrives.
