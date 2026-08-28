import 'package:dio/dio.dart';
import '../../app/config/app_config.dart';
import 'interceptors/auth_interceptor.dart';
import 'interceptors/logging_interceptor.dart';
import 'interceptors/rate_limit_interceptor.dart';
import 'interceptors/retry_interceptor.dart';
import 'interceptors/tracing_interceptor.dart';
import 'token_provider.dart';

abstract class ApiClient {
  Future<Response> get(
    String path, {
    Map<String, dynamic>? queryParameters,
    bool allowRetry = false,
  });

  Future<Response> post(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    bool allowRetry = false,
  });

  Future<Response> put(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    bool allowRetry = false,
  });

  Future<Response> patch(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    bool allowRetry = false,
  });

  Future<Response> delete(
    String path, {
    Map<String, dynamic>? queryParameters,
    bool allowRetry = false,
  });
}

class DioApiClient implements ApiClient {
  late final Dio _dio;
  final TokenProvider tokenProvider;

  DioApiClient({required this.tokenProvider}) {
    _dio = Dio(BaseOptions(
      baseUrl: '${AppConfig.apiBaseUrl}${AppConfig.apiVersion}',
      connectTimeout: const Duration(milliseconds: AppConfig.connectTimeout),
      receiveTimeout: const Duration(milliseconds: AppConfig.receiveTimeout),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    ));

    // Pipeline order matters
    _dio.interceptors.addAll([
      TracingInterceptor(),
      AuthInterceptor(tokenProvider),
      RateLimitInterceptor(),
      RetryInterceptor(dio: _dio),
      LoggingInterceptor(),
    ]);
  }

  @override
  Future<Response> get(
    String path, {
    Map<String, dynamic>? queryParameters,
    bool allowRetry = false,
  }) async {
    return await _dio.get(
      path,
      queryParameters: queryParameters,
      options: Options(extra: {'allowRetry': allowRetry}),
    );
  }

  @override
  Future<Response> post(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    bool allowRetry = false,
  }) async {
    return await _dio.post(
      path,
      data: data,
      queryParameters: queryParameters,
      options: Options(extra: {'allowRetry': allowRetry}),
    );
  }

  @override
  Future<Response> put(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    bool allowRetry = false,
  }) async {
    return await _dio.put(
      path,
      data: data,
      queryParameters: queryParameters,
      options: Options(extra: {'allowRetry': allowRetry}),
    );
  }

  @override
  Future<Response> patch(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    bool allowRetry = false,
  }) async {
    return await _dio.patch(
      path,
      data: data,
      queryParameters: queryParameters,
      options: Options(extra: {'allowRetry': allowRetry}),
    );
  }

  @override
  Future<Response> delete(
    String path, {
    Map<String, dynamic>? queryParameters,
    bool allowRetry = false,
  }) async {
    return await _dio.delete(
      path,
      queryParameters: queryParameters,
      options: Options(extra: {'allowRetry': allowRetry}),
    );
  }
}
