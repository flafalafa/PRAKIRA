# Enterprise Notification Delivery Tracking & History

This module acts as the "Black Box" or Flight Data Recorder for the notification system. It tracks the complete lifecycle of a notification from the moment it is created until it is successfully delivered or permanently failed.

## Architecture
- **Models (`models.py`, `status.py`)**: `NotificationHistoryRecord` tracks the current state, while a list of `TimelineEvent` records the chronological history of how it got there. The `NotificationStatus` enum defines the state machine (e.g. `CREATED` -> `SCHEDULED` -> `DELIVERED`).
- **Tracker (`tracker.py`)**: The main facade used by other modules to record events. It exposes methods like `track_creation()`, `track_scheduling()`, and `track_delivery_result()`.
- **Timeline & Audit (`timeline.py`, `audit.py`)**: `TimelineManager` adds discrete events to a notification's history. `AuditManager` specifically tracks state transitions for auditing and troubleshooting purposes.
- **Query & Metrics (`query.py`, `metrics.py`)**: Provides read access to the history data. `HistoryQuery` allows searching by ID, status, or prediction. `HistoryMetrics` calculates success rates, failure rates, and delivery times.
- **Repository (`repository.py`)**: An in-memory data store for the history records (to be replaced by a database in a future phase).

## Observability
This module does not participate in the decision-making process or the delivery of notifications. It strictly observes and records. It is the foundation for future analytics dashboards, user notification histories, and system health monitoring.
