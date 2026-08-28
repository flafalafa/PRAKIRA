import 'package:dio/dio.dart';
import '../network/models/api_error.dart';

class NetworkException implements Exception {
  final String message;
  final String? errorCode;
  final ApiError? apiError;

  NetworkException({
    required this.message,
    this.errorCode,
    this.apiError,
  });

  @override
  String toString() =>
      'NetworkException(message: $message, errorCode: $errorCode)';
}

class TimeoutException extends NetworkException {
  TimeoutException({String? message})
      : super(
          message: message ?? 'Connection timed out',
          errorCode: 'TIMEOUT',
        );
}

class NoInternetException extends NetworkException {
  NoInternetException({String? message})
      : super(
          message: message ?? 'No internet connection',
          errorCode: 'NO_INTERNET',
        );
}

class RateLimitException extends NetworkException {
  final Duration? retryAfter;

  RateLimitException({
    super.message = 'Rate limit exceeded',
    this.retryAfter,
    super.apiError,
  }) : super(
          errorCode: 'RATE_LIMIT_EXCEEDED',
        );
}

class ServerException extends NetworkException {
  final int? statusCode;

  ServerException({
    super.message = 'Internal server error',
    this.statusCode,
    super.apiError,
  }) : super(
          errorCode: 'INTERNAL_SERVER_ERROR',
        );
}

class ValidationException extends NetworkException {
  ValidationException({
    super.message = 'Validation failed',
    super.apiError,
  }) : super(
          errorCode: 'VALIDATION_ERROR',
        );
}

class UnauthorizedException extends NetworkException {
  UnauthorizedException({
    super.message = 'Unauthorized',
    super.apiError,
  }) : super(
          errorCode: 'UNAUTHORIZED',
        );
}

class ConflictException extends NetworkException {
  ConflictException({
    super.message = 'Conflict',
    super.apiError,
  }) : super(
          errorCode: 'CONFLICT',
        );
}

class NotFoundException extends NetworkException {
  NotFoundException({
    super.message = 'Resource not found',
    super.apiError,
  }) : super(
          errorCode: 'NOT_FOUND',
        );
}

/// Helper to map DioException to application NetworkExceptions.
NetworkException mapDioExceptionToNetworkException(DioException error) {
  if (error.type == DioExceptionType.connectionTimeout ||
      error.type == DioExceptionType.receiveTimeout ||
      error.type == DioExceptionType.sendTimeout) {
    return TimeoutException();
  }

  if (error.type == DioExceptionType.connectionError) {
    return NoInternetException();
  }

  if (error.response != null) {
    final statusCode = error.response!.statusCode;
    ApiError? apiError;

    if (error.response!.data != null &&
        error.response!.data is Map<String, dynamic>) {
      try {
        apiError = ApiError.fromJson(error.response!.data);
      } catch (_) {
        // Fallback if parsing fails
      }
    }

    final message = apiError?.message ?? error.message ?? 'Unknown error';

    switch (statusCode) {
      case 400:
        return ValidationException(message: message, apiError: apiError);
      case 401:
      case 403:
        return UnauthorizedException(message: message, apiError: apiError);
      case 404:
        return NotFoundException(message: message, apiError: apiError);
      case 409:
        return ConflictException(message: message, apiError: apiError);
      case 422:
        return ValidationException(message: message, apiError: apiError);
      case 429:
        Duration? retryAfter;
        final retryAfterHeader = error.response!.headers.value('retry-after');
        if (retryAfterHeader != null) {
          final seconds = int.tryParse(retryAfterHeader);
          if (seconds != null) {
            retryAfter = Duration(seconds: seconds);
          }
        }
        return RateLimitException(
            message: message, retryAfter: retryAfter, apiError: apiError);
      case 500:
      case 502:
      case 503:
      case 504:
      default:
        return ServerException(
            message: message, statusCode: statusCode, apiError: apiError);
    }
  }

  return NetworkException(message: error.message ?? 'Unknown error');
}
