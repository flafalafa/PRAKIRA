import 'package:equatable/equatable.dart';

class ApiError extends Equatable {
  final String errorCode;
  final String message;
  final Map<String, dynamic>? details;
  final String requestId;
  final DateTime timestamp;
  final String path;
  final String version;

  const ApiError({
    required this.errorCode,
    required this.message,
    this.details,
    required this.requestId,
    required this.timestamp,
    required this.path,
    required this.version,
  });

  factory ApiError.fromJson(Map<String, dynamic> json) {
    return ApiError(
      errorCode: json['error_code'] as String? ?? 'UNKNOWN_ERROR',
      message: json['message'] as String? ?? 'An unknown error occurred.',
      details: json['details'] as Map<String, dynamic>?,
      requestId: json['request_id'] as String? ?? '',
      timestamp: json['timestamp'] != null
          ? DateTime.tryParse(json['timestamp'] as String) ?? DateTime.now()
          : DateTime.now(),
      path: json['path'] as String? ?? '',
      version: json['version'] as String? ?? 'v1',
    );
  }

  @override
  List<Object?> get props => [
        errorCode,
        message,
        details,
        requestId,
        timestamp,
        path,
        version,
      ];
}
