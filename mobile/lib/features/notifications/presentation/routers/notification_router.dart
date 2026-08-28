import 'package:flutter/material.dart';
import '../../../areas/presentation/controllers/area_controller.dart';
import '../../../../core/di/service_locator.dart';
import '../../../alerts/presentation/screens/alert_detail_screen.dart';

class NotificationRouter {
  final GlobalKey<NavigatorState> navigatorKey;
  final AreaController _areaController;

  NotificationRouter({
    required this.navigatorKey,
    AreaController? areaController,
  }) : _areaController = areaController ?? ServiceLocator.instance.areaController;

  /// Handles an incoming notification tap payload.
  void handleNotificationTap(Map<String, dynamic> payload) {
    if (payload.isEmpty) return;

    final type = payload['type'] as String?;
    final areaId = payload['area_id'] as String?;
    final alertId = payload['alert_id'] as String?;

    if (areaId != null && areaId.isNotEmpty) {
      // Navigate or set area
      _areaController.selectArea(areaId);
    }

    if (type == 'alert_update' || type == 'new_alert') {
      if (alertId != null && alertId.isNotEmpty) {
        // Navigate to Alert Detail
        navigatorKey.currentState?.push(
          MaterialPageRoute(
            builder: (context) => AlertDetailScreen(alertId: alertId),
          ),
        );
      } else {
        // Just go to dashboard
        _navigateToDashboard();
      }
    } else {
      // Unknown or generic notification type
      _navigateToDashboard();
    }
  }

  void _navigateToDashboard() {
    // Basic approach: pop until first route if already in the app,
    // or just push replacement. Here we just pop to root for simplicity.
    navigatorKey.currentState?.popUntil((route) => route.isFirst);
  }
}
