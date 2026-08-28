import 'package:dio/dio.dart';
import 'dart:math' as math;

class RetryInterceptor extends Interceptor {
  final Dio dio;
  final int maxRetries;
  final Duration initialDelay;

  RetryInterceptor({
    required this.dio,
    this.maxRetries = 3,
    this.initialDelay = const Duration(seconds: 1),
  });

  @override
  Future<void> onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    final options = err.requestOptions;
    
    if (_shouldRetry(err, options)) {
      int retryCount = options.extra['retryCount'] ?? 0;
      
      if (retryCount < maxRetries) {
        retryCount++;
        options.extra['retryCount'] = retryCount;

        // Exponential backoff
        final delay = Duration(
          milliseconds: initialDelay.inMilliseconds * math.pow(2, retryCount - 1).toInt(),
        );

        await Future.delayed(delay);

        try {
          final response = await dio.request(
            options.path,
            data: options.data,
            queryParameters: options.queryParameters,
            cancelToken: options.cancelToken,
            options: Options(
              method: options.method,
              headers: options.headers,
              responseType: options.responseType,
              contentType: options.contentType,
              extra: options.extra,
            ),
            onReceiveProgress: options.onReceiveProgress,
            onSendProgress: options.onSendProgress,
          );
          return handler.resolve(response);
        } on DioException catch (e) {
          // If the retry also fails, it will loop back here because 
          // the retry request also goes through the interceptor.
          // The retryCount prevents infinite loops.
          return super.onError(e, handler);
        } catch (e) {
          return super.onError(err, handler);
        }
      }
    }

    return super.onError(err, handler);
  }

  bool _shouldRetry(DioException err, RequestOptions options) {
    // Only retry idempotent methods automatically
    final isIdempotent = ['GET', 'PUT', 'DELETE'].contains(options.method.toUpperCase());
    
    // Some callers may explicitly ask for a retry despite being POST 
    // by passing 'allowRetry' in the extra options.
    final allowRetry = options.extra['allowRetry'] == true;

    if (!isIdempotent && !allowRetry) return false;

    // Retry on timeouts or network connection errors
    if (err.type == DioExceptionType.connectionTimeout ||
        err.type == DioExceptionType.receiveTimeout ||
        err.type == DioExceptionType.sendTimeout ||
        err.type == DioExceptionType.connectionError) {
      return true;
    }

    // Retry on specific server errors (502, 503, 504)
    if (err.response != null) {
      final statusCode = err.response!.statusCode;
      if (statusCode == 502 || statusCode == 503 || statusCode == 504) {
        return true;
      }
    }

    return false;
  }
}
