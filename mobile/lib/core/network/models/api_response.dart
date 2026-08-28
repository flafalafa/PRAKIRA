import 'package:equatable/equatable.dart';
import 'api_meta.dart';

class SuccessResponse<T> extends Equatable {
  final T data;
  final ApiMeta meta;
  final String requestId;
  final DateTime timestamp;
  final String version;

  const SuccessResponse({
    required this.data,
    required this.meta,
    required this.requestId,
    required this.timestamp,
    required this.version,
  });

  factory SuccessResponse.fromJson(
    Map<String, dynamic> json,
    T Function(Object? json) fromJsonT,
  ) {
    return SuccessResponse<T>(
      data: fromJsonT(json['data']),
      meta: json['meta'] != null
          ? ApiMeta.fromJson(json['meta'])
          : const ApiMeta(),
      requestId: json['request_id'] as String? ?? '',
      timestamp: json['timestamp'] != null
          ? DateTime.tryParse(json['timestamp'] as String) ?? DateTime.now()
          : DateTime.now(),
      version: json['version'] as String? ?? 'v1',
    );
  }

  @override
  List<Object?> get props => [data, meta, requestId, timestamp, version];
}

class PaginatedResponse<T> extends Equatable {
  final List<T> data;
  final ApiMeta meta;
  final String requestId;
  final DateTime timestamp;
  final String version;

  const PaginatedResponse({
    required this.data,
    required this.meta,
    required this.requestId,
    required this.timestamp,
    required this.version,
  });

  factory PaginatedResponse.fromJson(
    Map<String, dynamic> json,
    T Function(Object? json) fromJsonT,
  ) {
    return PaginatedResponse<T>(
      data: (json['data'] as List<dynamic>?)
              ?.map((item) => fromJsonT(item))
              .toList() ??
          [],
      meta: json['meta'] != null
          ? ApiMeta.fromJson(json['meta'])
          : const ApiMeta(),
      requestId: json['request_id'] as String? ?? '',
      timestamp: json['timestamp'] != null
          ? DateTime.tryParse(json['timestamp'] as String) ?? DateTime.now()
          : DateTime.now(),
      version: json['version'] as String? ?? 'v1',
    );
  }

  @override
  List<Object?> get props => [data, meta, requestId, timestamp, version];
}
