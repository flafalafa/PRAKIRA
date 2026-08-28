# Enterprise Notification Preferences & Quiet Hours

This module acts as the "Personal Assistant" for every user of the Flood Guardian system. It ensures that users only receive the notifications they care about, at the times they want them, while guaranteeing that critical emergency alerts always get through.

## Architecture
- **Profile (`profile.py`)**: `UserPreferenceProfile` defines the schema for a user's settings, including master switches, area subscriptions, minimum severity, and quiet hours.
- **Filters (`filters.py`)**: 
  - `MasterSwitchFilter`: Checks if the user has globally muted notifications.
  - `AreaSubscriptionFilter`: Ensures the notification belongs to an area the user is watching.
  - `SeverityFilter`: Checks if the event is serious enough for the user (e.g. they only want `DANGER` or above).
  - `QuietHoursFilter`: Suppresses notifications during the user's sleep window.
- **Registry (`registry.py`)**: Manages the list of active filters.
- **Manager (`manager.py`)**: The orchestrator that evaluates a `NotificationRequest` against a `UserPreferenceProfile`. It runs all filters and builds a `NotificationPreferenceResult`.

## Emergency Override
The most critical feature of this module is the Emergency Override. If a notification has an `EMERGENCY` priority or severity, the manager bypasses *all* user filters. Even if the user has muted all notifications, unsubscribed from the area, and set quiet hours, the system will force the notification through. Human safety supersedes user preferences.
