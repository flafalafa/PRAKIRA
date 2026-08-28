import 'package:equatable/equatable.dart';
import 'network_exceptions.dart' as net;

abstract class AppFailure extends Equatable {
  final String message;
  final String errorCode;

  const AppFailure(this.message, this.errorCode);

  @override
  List<Object> get props => [message, errorCode];
}

class NetworkFailure extends AppFailure {
  const NetworkFailure(super.message, super.errorCode);
}

class ServerFailure extends AppFailure {
  const ServerFailure(super.message, super.errorCode);
}

class ValidationFailure extends AppFailure {
  final Map<String, dynamic>? details;
  const ValidationFailure(super.message, super.errorCode, {this.details});
  
  @override
  List<Object> get props => [message, errorCode, details ?? {}];
}

class UnauthorizedFailure extends AppFailure {
  const UnauthorizedFailure(super.message, super.errorCode);
}

class RateLimitFailure extends AppFailure {
  const RateLimitFailure(super.message, super.errorCode);
}

class UnknownFailure extends AppFailure {
  const UnknownFailure(super.message, super.errorCode);
}

class CacheFailure extends AppFailure {
  const CacheFailure(super.message, super.errorCode);
}

// Exceptions (used internally before mapping to Failures)
class CacheException implements Exception {}

AppFailure mapExceptionToFailure(Exception exception) {
  if (exception is net.NoInternetException) {
    return NetworkFailure(exception.message, exception.errorCode ?? 'NO_INTERNET');
  } else if (exception is net.TimeoutException) {
    return NetworkFailure(exception.message, exception.errorCode ?? 'TIMEOUT');
  } else if (exception is net.ValidationException) {
    return ValidationFailure(
      exception.message,
      exception.errorCode ?? 'VALIDATION_ERROR',
      details: exception.apiError?.details,
    );
  } else if (exception is net.UnauthorizedException) {
    return UnauthorizedFailure(exception.message, exception.errorCode ?? 'UNAUTHORIZED');
  } else if (exception is net.RateLimitException) {
    return RateLimitFailure(exception.message, exception.errorCode ?? 'RATE_LIMIT_EXCEEDED');
  } else if (exception is net.NotFoundException) {
    return ServerFailure(exception.message, exception.errorCode ?? 'NOT_FOUND');
  } else if (exception is net.ConflictException) {
    return ServerFailure(exception.message, exception.errorCode ?? 'CONFLICT');
  } else if (exception is net.ServerException) {
    return ServerFailure(exception.message, exception.errorCode ?? 'INTERNAL_SERVER_ERROR');
  } else if (exception is net.NetworkException) {
    return NetworkFailure(exception.message, exception.errorCode ?? 'NETWORK_ERROR');
  } else if (exception is CacheException) {
    return const ServerFailure('Cache error', 'CACHE_ERROR');
  }
  return const UnknownFailure('An unexpected error occurred', 'UNKNOWN_ERROR');
}
