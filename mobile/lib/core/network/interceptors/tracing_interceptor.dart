import 'package:dio/dio.dart';
import 'package:uuid/uuid.dart';

class TracingInterceptor extends Interceptor {
  final Uuid _uuid = const Uuid();

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    if (!options.headers.containsKey('X-Request-ID')) {
      options.headers['X-Request-ID'] = _uuid.v4();
    }
    
    // We can also add a correlation ID if passed in the options, 
    // or generate a new one if not present, but for now we'll 
    // generate a unique Correlation ID if it's not set.
    if (!options.headers.containsKey('X-Correlation-ID')) {
      options.headers['X-Correlation-ID'] = _uuid.v4();
    }
    
    super.onRequest(options, handler);
  }
}
