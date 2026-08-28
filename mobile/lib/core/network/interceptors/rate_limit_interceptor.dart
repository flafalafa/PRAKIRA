import 'package:dio/dio.dart';
import '../models/api_error.dart';
import '../../errors/network_exceptions.dart';

class RateLimitInterceptor extends Interceptor {
  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    if (err.response?.statusCode == 429) {
      Duration? retryAfter;
      final retryAfterHeader = err.response?.headers.value('retry-after');
      if (retryAfterHeader != null) {
        final seconds = int.tryParse(retryAfterHeader);
        if (seconds != null) {
          retryAfter = Duration(seconds: seconds);
        }
      }

      ApiError? apiError;
      if (err.response?.data != null && err.response!.data is Map<String, dynamic>) {
        try {
          apiError = ApiError.fromJson(err.response!.data);
        } catch (_) {}
      }

      final exception = RateLimitException(
        message: apiError?.message ?? 'Rate limit exceeded',
        retryAfter: retryAfter,
        apiError: apiError,
      );

      return handler.reject(
        DioException(
          requestOptions: err.requestOptions,
          response: err.response,
          type: err.type,
          error: exception,
        ),
      );
    }
    
    super.onError(err, handler);
  }
}
