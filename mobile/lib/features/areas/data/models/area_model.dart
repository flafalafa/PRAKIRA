import 'package:equatable/equatable.dart';
import 'location_model.dart';

enum AreaStatus {
  active,
  inactive,
  maintenance,
  unknown,
}

class AreaModel extends Equatable {
  final String areaId;
  final String areaName;
  final String areaCode;
  final AreaStatus status;
  final String areaType;
  final LocationModel? location;
  final DateTime createdAt;
  final DateTime updatedAt;

  const AreaModel({
    required this.areaId,
    required this.areaName,
    required this.areaCode,
    required this.status,
    required this.areaType,
    this.location,
    required this.createdAt,
    required this.updatedAt,
  });

  factory AreaModel.fromJson(Map<String, dynamic> json) {
    return AreaModel(
      areaId: json['area_id'] as String,
      areaName: json['area_name'] as String,
      areaCode: json['area_code'] as String,
      status: _parseStatus(json['status'] as String?),
      areaType: json['area_type'] as String? ?? 'unknown',
      location: json['location'] != null
          ? LocationModel.fromJson(json['location'] as Map<String, dynamic>)
          : null,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'area_id': areaId,
      'area_name': areaName,
      'area_code': areaCode,
      'status': status.name,
      'area_type': areaType,
      if (location != null) 'location': location!.toJson(),
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }

  static AreaStatus _parseStatus(String? statusStr) {
    if (statusStr == null) return AreaStatus.unknown;
    switch (statusStr.toLowerCase()) {
      case 'active':
        return AreaStatus.active;
      case 'inactive':
        return AreaStatus.inactive;
      case 'maintenance':
        return AreaStatus.maintenance;
      default:
        return AreaStatus.unknown;
    }
  }

  @override
  List<Object?> get props => [
        areaId,
        areaName,
        areaCode,
        status,
        areaType,
        location,
        createdAt,
        updatedAt,
      ];
}
