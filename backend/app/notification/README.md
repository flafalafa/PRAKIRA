# Enterprise Notification Foundation

This module acts as the robust, provider-agnostic core of the Notification Delivery layer. It receives the standardized `FloodPredictionResult` from the Decision Engine and structures it into a generic `NotificationRequest` payload, ready to be dispatched to any notification channel (Push, WhatsApp, SMS, Email).

## Architecture
- **Request/Response (`request.py`, `response.py`)**: Defines the internal contracts (`NotificationRequest`, `NotificationResponse`, `DeliveryStatus`). These models ensure that downstream channels don't need to know anything about Flood Prediction objects.
- **Priority (`priority.py`)**: Maps flood severities to IT-standard notification priorities (`LOW`, `NORMAL`, `HIGH`, `CRITICAL`, `EMERGENCY`).
- **Context (`context.py`)**: A wrapper object that pairs the prediction with its relevant geographical/execution metadata.
- **Builder & Factory (`builder.py`, `factory.py`)**: Responsible for extracting the explanation, recommendation, and status from the prediction and shaping it into the standardized request format.
- **Channel Interface (`channel.py`)**: Abstract base class (`BaseNotificationChannel`) that enforces a strict `send(NotificationRequest) -> DeliveryStatus` contract for any future concrete implementations (e.g. FirebasePushChannel, WhatsAppChannel).
- **Registry (`registry.py`)**: Maintains a list of active notification channels and allows turning them on/off dynamically.
- **Foundation & Manager (`foundation.py`, `manager.py`)**: The entry points for the Notification Delivery layer.

## Design Philosophy
This module intentionally **does not send** any notifications. It acts strictly as a preparation layer (formatting, prioritizing, and structuring) to prevent the core business logic from being tightly coupled to specific third-party APIs (like Twilio or Firebase).
