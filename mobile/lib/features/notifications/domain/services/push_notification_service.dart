import 'dart:async';

enum NotificationPermissionState {
  unknown,
  granted,
  denied,
  permanentlyDenied,
}

abstract class PushNotificationService {
  /// The current permission state.
  NotificationPermissionState get permissionState;

  /// Stream of permission state changes.
  Stream<NotificationPermissionState> get onPermissionChanged;

  /// Stream of notification payloads received while the app is in the foreground.
  Stream<Map<String, dynamic>> get onForegroundMessage;

  /// Stream of notification payloads tapped by the user.
  Stream<Map<String, dynamic>> get onNotificationTap;

  /// Initializes the push notification service.
  Future<void> initialize();

  /// Requests notification permission from the OS.
  Future<NotificationPermissionState> requestPermission();

  /// Retrieves the device push token, if available.
  Future<String?> getToken();
}
