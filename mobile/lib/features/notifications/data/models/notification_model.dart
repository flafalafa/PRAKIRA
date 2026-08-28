import 'package:equatable/equatable.dart';

class NotificationDeliveryStatus extends Equatable {
  final String notificationStatus;
  final String providerStatus;
  final DateTime? deliveryTimestamp;
  final String? failureState;
  final String? retryState;

  const NotificationDeliveryStatus({
    required this.notificationStatus,
    required this.providerStatus,
    this.deliveryTimestamp,
    this.failureState,
    this.retryState,
  });

  factory NotificationDeliveryStatus.fromJson(Map<String, dynamic> json) {
    return NotificationDeliveryStatus(
      notificationStatus: json['notification_status'] as String,
      providerStatus: json['provider_status'] as String,
      deliveryTimestamp: json['delivery_timestamp'] != null
          ? DateTime.tryParse(json['delivery_timestamp'] as String)
          : null,
      failureState: json['failure_state'] as String?,
      retryState: json['retry_state'] as String?,
    );
  }

  @override
  List<Object?> get props => [
        notificationStatus,
        providerStatus,
        deliveryTimestamp,
        failureState,
        retryState,
      ];
}

class NotificationModel extends Equatable {
  final String notificationId;
  final String alertId;
  final String? predictionId;
  final String areaId;
  final String severity;
  final String title;
  final String message;
  final String priority;
  final String currentStatus;
  final DateTime createdAt;
  final DateTime updatedAt;
  final NotificationDeliveryStatus? deliverySummary;

  const NotificationModel({
    required this.notificationId,
    required this.alertId,
    this.predictionId,
    required this.areaId,
    required this.severity,
    required this.title,
    required this.message,
    required this.priority,
    required this.currentStatus,
    required this.createdAt,
    required this.updatedAt,
    this.deliverySummary,
  });

  factory NotificationModel.fromJson(Map<String, dynamic> json) {
    return NotificationModel(
      notificationId: json['notification_id'] as String,
      alertId: json['alert_id'] as String,
      predictionId: json['prediction_id'] as String?,
      areaId: json['area_id'] as String,
      severity: json['severity'] as String,
      title: json['title'] as String,
      message: json['message'] as String,
      priority: json['priority'] as String,
      currentStatus: json['current_status'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
      deliverySummary: json['delivery_summary'] != null
          ? NotificationDeliveryStatus.fromJson(json['delivery_summary'] as Map<String, dynamic>)
          : null,
    );
  }

  @override
  List<Object?> get props => [
        notificationId,
        alertId,
        predictionId,
        areaId,
        severity,
        title,
        message,
        priority,
        currentStatus,
        createdAt,
        updatedAt,
        deliverySummary,
      ];
}
