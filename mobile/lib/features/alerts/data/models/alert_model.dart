import 'package:equatable/equatable.dart';

enum AlertLevel {
  watch,
  warning,
  danger,
  emergency,
  unknown;

  static AlertLevel fromString(String? value) {
    if (value == null) return AlertLevel.unknown;
    switch (value.toLowerCase()) {
      case 'watch':
        return AlertLevel.watch;
      case 'warning':
        return AlertLevel.warning;
      case 'danger':
        return AlertLevel.danger;
      case 'emergency':
        return AlertLevel.emergency;
      default:
        return AlertLevel.unknown;
    }
  }
}

class AlertExplanationModel extends Equatable {
  final List<String> primaryRiskFactors;
  final List<String> supportingObservations;
  final List<String> triggeredRules;
  final String confidenceExplanation;
  final List<String> missingData;

  const AlertExplanationModel({
    this.primaryRiskFactors = const [],
    this.supportingObservations = const [],
    this.triggeredRules = const [],
    this.confidenceExplanation = '',
    this.missingData = const [],
  });

  factory AlertExplanationModel.fromJson(Map<String, dynamic> json) {
    return AlertExplanationModel(
      primaryRiskFactors: List<String>.from(json['primary_risk_factors'] ?? []),
      supportingObservations: List<String>.from(json['supporting_observations'] ?? []),
      triggeredRules: List<String>.from(json['triggered_rules'] ?? []),
      confidenceExplanation: json['confidence_explanation'] as String? ?? '',
      missingData: List<String>.from(json['missing_data'] ?? []),
    );
  }

  @override
  List<Object?> get props => [
        primaryRiskFactors,
        supportingObservations,
        triggeredRules,
        confidenceExplanation,
        missingData,
      ];
}

class AlertModel extends Equatable {
  final String alertId;
  final String areaId;
  final AlertLevel alertLevel;
  final double riskScore;
  final double? confidence;
  final String predictionId;
  final String title;
  final String message;
  final String? recommendation;
  final DateTime issuedAt;
  final DateTime updatedAt;
  final DateTime? expiresAt;
  final DateTime? estimatedArrivalTime;
  final String alertStatus;
  final AlertExplanationModel? explanation;

  const AlertModel({
    required this.alertId,
    required this.areaId,
    required this.alertLevel,
    required this.riskScore,
    this.confidence,
    required this.predictionId,
    required this.title,
    required this.message,
    this.recommendation,
    required this.issuedAt,
    required this.updatedAt,
    this.expiresAt,
    this.estimatedArrivalTime,
    required this.alertStatus,
    this.explanation,
  });

  factory AlertModel.fromJson(Map<String, dynamic> json) {
    return AlertModel(
      alertId: json['alert_id'] as String,
      areaId: json['area_id'] as String,
      alertLevel: AlertLevel.fromString(json['alert_level'] as String?),
      riskScore: (json['risk_score'] as num).toDouble(),
      confidence: json['confidence'] != null ? (json['confidence'] as num).toDouble() : null,
      predictionId: json['prediction_id'] as String,
      title: json['title'] as String,
      message: json['message'] as String,
      recommendation: json['recommendation'] as String?,
      issuedAt: DateTime.parse(json['issued_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
      expiresAt: json['expires_at'] != null ? DateTime.tryParse(json['expires_at'] as String) : null,
      estimatedArrivalTime: json['estimated_arrival_time'] != null
          ? DateTime.tryParse(json['estimated_arrival_time'] as String)
          : null,
      alertStatus: json['alert_status'] as String? ?? 'unknown',
      explanation: json['explanation'] != null
          ? AlertExplanationModel.fromJson(json['explanation'] as Map<String, dynamic>)
          : null,
    );
  }

  @override
  List<Object?> get props => [
        alertId,
        areaId,
        alertLevel,
        riskScore,
        confidence,
        predictionId,
        title,
        message,
        recommendation,
        issuedAt,
        updatedAt,
        expiresAt,
        estimatedArrivalTime,
        alertStatus,
        explanation,
      ];
}
