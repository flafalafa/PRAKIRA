# Enterprise Push Notification Provider

This module represents the edge of the Notification Delivery layer. It is responsible for taking scheduled jobs and translating them into provider-specific API calls (e.g. Firebase Cloud Messaging, APNs) to deliver the actual payload to user devices.

## Architecture
- **Base Interface (`base/provider.py`)**: `BasePushProvider` enforces a strict contract. Every provider must implement methods like `send()`, `send_batch()`, `validate()`, and `health()`.
- **Registry & Factory (`base/registry.py`, `base/factory.py`)**: Manages the instantiation and retrieval of active push providers. Allows dynamic swapping (e.g. falling back to an alternate provider if FCM goes down).
- **FCM Implementation (`fcm/`)**:
  - `mapper.py`: Translates our generic `NotificationRequest` into the specific JSON schema required by Firebase Cloud Messaging (including Android high-priority flags).
  - `validator.py`: Ensures the token is valid and the payload size does not exceed FCM limits (4KB).
  - `client.py`: The actual HTTP client that connects to the Google API (currently mocked).
  - `provider.py`: The wrapper class that implements `BasePushProvider` using the FCM specific components.

## Resilience
If the `send()` method encounters a network timeout, it catches the exception and returns a `NotificationDeliveryResult` with `retryable=True` and `delivery_status=FAILED`. The upstream Scheduler (T-603) will read this result and automatically requeue the job using exponential backoff.
