import 'package:equatable/equatable.dart';

enum RiskLevel {
  safe,
  watch,
  warning,
  danger,
  emergency,
  unknown;

  static RiskLevel fromString(String? value) {
    if (value == null) return RiskLevel.unknown;
    switch (value.toLowerCase()) {
      case 'safe':
        return RiskLevel.safe;
      case 'watch':
        return RiskLevel.watch;
      case 'warning':
        return RiskLevel.warning;
      case 'danger':
        return RiskLevel.danger;
      case 'emergency':
        return RiskLevel.emergency;
      default:
        return RiskLevel.unknown;
    }
  }
}

class PredictionExplanationModel extends Equatable {
  final List<String> primaryRiskFactors;
  final List<String> supportingObservations;
  final List<String> triggeredRules;
  final String confidenceExplanation;
  final List<String> missingData;
  final String reasonSummary;

  const PredictionExplanationModel({
    this.primaryRiskFactors = const [],
    this.supportingObservations = const [],
    this.triggeredRules = const [],
    this.confidenceExplanation = '',
    this.missingData = const [],
    this.reasonSummary = '',
  });

  factory PredictionExplanationModel.fromJson(Map<String, dynamic> json) {
    return PredictionExplanationModel(
      primaryRiskFactors: List<String>.from(json['primary_risk_factors'] ?? []),
      supportingObservations: List<String>.from(json['supporting_observations'] ?? []),
      triggeredRules: List<String>.from(json['triggered_rules'] ?? []),
      confidenceExplanation: json['confidence_explanation'] as String? ?? '',
      missingData: List<String>.from(json['missing_data'] ?? []),
      reasonSummary: json['reason_summary'] as String? ?? '',
    );
  }

  @override
  List<Object?> get props => [
        primaryRiskFactors,
        supportingObservations,
        triggeredRules,
        confidenceExplanation,
        missingData,
        reasonSummary,
      ];
}

class PredictionModel extends Equatable {
  final String predictionId;
  final String areaId;
  final DateTime predictionTime;
  final double riskScore;
  final RiskLevel riskLevel;
  final double? confidence;
  final String predictionStatus;
  final DateTime? estimatedArrivalTime;
  final double? estimatedFloodDepth;
  final int? estimatedDuration;
  final String? recommendation;
  final PredictionExplanationModel? explanation;
  final Map<String, dynamic> supportingFactors;
  final String predictionVersion;
  final DateTime createdAt;

  const PredictionModel({
    required this.predictionId,
    required this.areaId,
    required this.predictionTime,
    required this.riskScore,
    required this.riskLevel,
    this.confidence,
    required this.predictionStatus,
    this.estimatedArrivalTime,
    this.estimatedFloodDepth,
    this.estimatedDuration,
    this.recommendation,
    this.explanation,
    this.supportingFactors = const {},
    required this.predictionVersion,
    required this.createdAt,
  });

  factory PredictionModel.fromJson(Map<String, dynamic> json) {
    return PredictionModel(
      predictionId: json['prediction_id'] as String,
      areaId: json['area_id'] as String,
      predictionTime: DateTime.parse(json['prediction_time'] as String),
      riskScore: (json['risk_score'] as num).toDouble(),
      riskLevel: RiskLevel.fromString(json['risk_level'] as String?),
      confidence: json['confidence'] != null ? (json['confidence'] as num).toDouble() : null,
      predictionStatus: json['prediction_status'] as String? ?? 'unknown',
      estimatedArrivalTime: json['estimated_arrival_time'] != null
          ? DateTime.tryParse(json['estimated_arrival_time'] as String)
          : null,
      estimatedFloodDepth: json['estimated_flood_depth'] != null
          ? (json['estimated_flood_depth'] as num).toDouble()
          : null,
      estimatedDuration: json['estimated_duration'] as int?,
      recommendation: json['recommendation'] as String?,
      explanation: json['explanation'] != null
          ? PredictionExplanationModel.fromJson(json['explanation'] as Map<String, dynamic>)
          : null,
      supportingFactors: json['supporting_factors'] as Map<String, dynamic>? ?? {},
      predictionVersion: json['prediction_version'] as String? ?? '1.0',
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  @override
  List<Object?> get props => [
        predictionId,
        areaId,
        predictionTime,
        riskScore,
        riskLevel,
        confidence,
        predictionStatus,
        estimatedArrivalTime,
        estimatedFloodDepth,
        estimatedDuration,
        recommendation,
        explanation,
        supportingFactors,
        predictionVersion,
        createdAt,
      ];
}
