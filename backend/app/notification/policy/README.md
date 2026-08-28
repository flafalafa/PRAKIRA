# Enterprise Alert Policy Engine

This module serves as the final gatekeeper before a notification is actually dispatched to the user. It evaluates the `NotificationRequest` against a set of business rules (Policies) to determine if it should be sent, suppressed, deferred, or escalated.

## Architecture
- **Context (`context.py`)**: `AlertPolicyContext` holds the current notification, the original prediction, and history (e.g. the last notification sent to this area).
- **Result (`result.py`)**: `AlertPolicyResult` contains the final verdict (`SEND`, `SUPPRESS`, `ESCALATE`, `DEFER`) and the reason for that verdict.
- **Rules (`rules.py`)**: Implementations of `BasePolicyRule`. Current rules include:
  - `DuplicateAlertRule`: Suppresses identical alerts sent back-to-back.
  - `CooldownPolicyRule`: Defers non-emergency alerts if they occur too soon after a previous alert (e.g. within 15 minutes). Bypassed by `EMERGENCY` priority.
  - `EscalationRule`: Detects if the severity has increased since the last alert and marks the decision as `ESCALATE`.
- **Registry (`registry.py`)**: Dynamically stores all active policy rules.
- **Evaluator (`evaluator.py`)**: Iterates through registered rules. If any rule dictates a suppression/deferral, it short-circuits (fast fail) and stops execution.
- **Engine (`engine.py`)**: The main facade that orchestrates the context setup and evaluation process.

## Use Cases
- **Spam Prevention**: If it rains steadily for 3 hours and the risk stays at `WARNING`, the engine suppresses redundant notifications so users aren't spammed every 5 minutes.
- **Escalation**: If the risk jumps from `WATCH` to `DANGER` within 10 minutes, the engine flags this as an escalation, allowing downstream systems to use louder alert tones.
- **Emergency Override**: If a dam breaks (`EMERGENCY`), the engine ignores all cooldown periods and forces the notification through immediately.
