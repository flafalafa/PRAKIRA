import 'package:flutter/material.dart';
import '../../../../core/di/service_locator.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../shared/widgets/app_loading.dart';
import '../../../../shared/widgets/app_error_state.dart';
import '../../../../shared/widgets/app_empty_state.dart';
import '../../data/models/notification_model.dart';
import '../../data/services/local_push_notification_service.dart';

class NotificationHistoryScreen extends StatefulWidget {
  final String areaId;

  const NotificationHistoryScreen({super.key, required this.areaId});

  @override
  State<NotificationHistoryScreen> createState() => _NotificationHistoryScreenState();
}

class _NotificationHistoryScreenState extends State<NotificationHistoryScreen> {
  final _repository = ServiceLocator.instance.notificationRepository;
  final _pushService = ServiceLocator.instance.pushNotificationService;
  
  List<NotificationModel> _notifications = [];
  bool _isLoading = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _fetchNotifications();
  }

  Future<void> _fetchNotifications() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final response = await _repository.getNotifications(widget.areaId);
      setState(() {
        _notifications = response.data;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = e.toString();
        _isLoading = false;
      });
    }
  }

  void _simulateNotification() {
    if (_pushService is LocalPushNotificationService) {
      final mockPayload = {
        'type': 'new_alert',
        'area_id': widget.areaId,
        'alert_id': 'mock-alert-123',
      };
      
      // Simulate tap
      (_pushService as LocalPushNotificationService).simulateNotificationTap(mockPayload);
      
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Simulated tap on notification')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Notifications', style: AppTypography.title),
        actions: [
          IconButton(
            icon: const Icon(Icons.bug_report),
            tooltip: 'Simulate Notification Tap',
            onPressed: _simulateNotification,
          ),
        ],
      ),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_isLoading) return const AppLoading();
    if (_errorMessage != null) {
      return AppErrorState(
        title: 'Failed to load notifications',
        message: _errorMessage!,
        onRetry: _fetchNotifications,
      );
    }

    if (_notifications.isEmpty) {
      return const AppEmptyState(
        title: 'No Notifications',
        message: 'You have no recent notifications for this area.',
        icon: Icons.notifications_none,
      );
    }

    return ListView.separated(
      itemCount: _notifications.length,
      separatorBuilder: (_, __) => const Divider(height: 1),
      itemBuilder: (context, index) {
        final notif = _notifications[index];
        return ListTile(
          contentPadding: const EdgeInsets.all(AppSpacing.s16),
          leading: Icon(
            _getIconForSeverity(notif.severity),
            color: _getColorForSeverity(notif.severity),
          ),
          title: Text(notif.title, style: AppTypography.label.copyWith(fontWeight: FontWeight.bold)),
          subtitle: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: AppSpacing.s4),
              Text(notif.message, style: AppTypography.body),
              const SizedBox(height: AppSpacing.s8),
              Text(
                notif.createdAt.toLocal().toString().split('.')[0],
                style: AppTypography.caption.copyWith(color: AppColors.gray500),
              ),
            ],
          ),
          onTap: () {
            // Reusing router logic inline
            if (notif.alertId.isNotEmpty) {
              Navigator.pushNamed(
                context, 
                '/alert_detail', 
                arguments: notif.alertId,
              );
            }
          },
        );
      },
    );
  }

  IconData _getIconForSeverity(String severity) {
    switch (severity.toLowerCase()) {
      case 'emergency': return Icons.warning_amber_rounded;
      case 'danger': return Icons.error_outline;
      case 'warning': return Icons.warning_amber;
      case 'watch': return Icons.info_outline;
      default: return Icons.notifications_none;
    }
  }

  Color _getColorForSeverity(String severity) {
    switch (severity.toLowerCase()) {
      case 'emergency': return AppColors.emergency;
      case 'danger': return AppColors.danger;
      case 'warning': return AppColors.warning;
      case 'watch': return AppColors.watch;
      default: return AppColors.primaryLight;
    }
  }
}
