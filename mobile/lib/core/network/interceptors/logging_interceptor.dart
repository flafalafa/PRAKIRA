import 'package:dio/dio.dart';
import '../../logging/app_logger.dart';

class LoggingInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    AppLogger.debug('=== API REQUEST ===');
    AppLogger.debug('Base URL: ${options.baseUrl}');
    AppLogger.debug('Full URL: ${options.uri}');
    AppLogger.debug('HTTP Method: ${options.method}');
    AppLogger.debug('Headers: ${options.headers}');
    if (options.data != null) {
      AppLogger.debug('Request Body: ${options.data}');
    }
    super.onRequest(options, handler);
  }

  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) {
    final reqOpts = response.requestOptions;
    AppLogger.debug('=== API RESPONSE ===');
    AppLogger.debug('Full URL: ${reqOpts.uri}');
    AppLogger.debug('HTTP Method: ${reqOpts.method}');
    AppLogger.debug('HTTP Status Code: ${response.statusCode}');
    AppLogger.debug('Response Body: ${response.data}');
    super.onResponse(response, handler);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    final reqOpts = err.requestOptions;
    AppLogger.error('=== API ERROR ===');
    AppLogger.error('Base URL: ${reqOpts.baseUrl}');
    AppLogger.error('Full URL: ${reqOpts.uri}');
    AppLogger.error('HTTP Method: ${reqOpts.method}');
    AppLogger.error('HTTP Status Code: ${err.response?.statusCode ?? 'N/A'}');
    AppLogger.error('DioException Type: ${err.type}');
    AppLogger.error('DioException Message: ${err.message}');
    if (err.response != null) {
      AppLogger.error('Response Body: ${err.response?.data}');
    }
    super.onError(err, handler);
  }
}
