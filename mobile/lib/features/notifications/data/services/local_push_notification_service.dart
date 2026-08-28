import 'dart:async';
import 'package:flutter/foundation.dart';
import '../../domain/services/push_notification_service.dart';

/// A local/mock implementation of PushNotificationService.
/// 
/// This is used because Firebase/FCM is not currently configured in the project.
/// It provides the required abstraction boundary and allows the application to 
/// handle permission states and simulate notification events without a real push provider.
class LocalPushNotificationService implements PushNotificationService {
  NotificationPermissionState _permissionState = NotificationPermissionState.unknown;
  
  final _permissionController = StreamController<NotificationPermissionState>.broadcast();
  final _foregroundController = StreamController<Map<String, dynamic>>.broadcast();
  final _tapController = StreamController<Map<String, dynamic>>.broadcast();

  @override
  NotificationPermissionState get permissionState => _permissionState;

  @override
  Stream<NotificationPermissionState> get onPermissionChanged => _permissionController.stream;

  @override
  Stream<Map<String, dynamic>> get onForegroundMessage => _foregroundController.stream;

  @override
  Stream<Map<String, dynamic>> get onNotificationTap => _tapController.stream;

  @override
  Future<void> initialize() async {
    // In a real implementation, we would check the current OS permission state here.
    debugPrint('LocalPushNotificationService: initialized (mock)');
  }

  @override
  Future<NotificationPermissionState> requestPermission() async {
    // Mocking permission request
    if (_permissionState == NotificationPermissionState.unknown) {
      _permissionState = NotificationPermissionState.granted;
      _permissionController.add(_permissionState);
      debugPrint('LocalPushNotificationService: permission granted');
    }
    return _permissionState;
  }

  @override
  Future<String?> getToken() async {
    // Return a dummy token for testing since FCM is not available
    return 'mock_device_token_xyz_123';
  }

  // --- Utility methods for local debugging/simulation ---

  void simulateForegroundMessage(Map<String, dynamic> payload) {
    _foregroundController.add(payload);
  }

  void simulateNotificationTap(Map<String, dynamic> payload) {
    _tapController.add(payload);
  }
}
