# Enterprise Escalation & Deduplication Engine

This module is the final intelligence layer before a notification is added to the delivery queue. While the `AlertPolicyEngine` determines if a brand new event *should* generate a notification, this engine evaluates the notification *in the context of what has already been queued or sent*.

## Architecture
- **History (`history.py`)**: Abstract interface to query the database/state for recently sent or currently queued notifications.
- **Rules (`rules.py`)**:
  - `DeduplicationRule`: Identifies if a newly generated notification is semantically identical to the one sent previously (e.g. `WARNING` -> `WARNING`). If so, it flags it for suppression.
  - `SeverityUpgradeRule`: Detects if the situation has worsened (e.g. `WATCH` -> `WARNING`). If the previous notification is still sitting in the queue (unsent), this rule forces a **Replacement**, swapping out the old benign message for the new urgent one.
- **Deduplicator & Escalator (`deduplicator.py`, `escalator.py`)**: The executors that run the rules and build the final `EscalationDecisionResult`.
- **Engine (`engine.py`)**: The facade that runs deduplication first (fast fail), and if it passes, runs escalation and replacement logic.

## Why have both Policy Engine and Escalation Engine?
- **Policy Engine (T-602)**: Evaluates static rules on a single event (e.g., "Is the confidence high enough to alert?").
- **Escalation Engine (T-605)**: Evaluates dynamic rules comparing the *current* event against the *past* events (e.g., "Is this event worse than the one I sent 5 minutes ago?").
