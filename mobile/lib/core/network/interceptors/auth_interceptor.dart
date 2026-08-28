import 'package:dio/dio.dart';
import '../token_provider.dart';

class AuthInterceptor extends Interceptor {
  final TokenProvider tokenProvider;

  AuthInterceptor(this.tokenProvider);

  @override
  Future<void> onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    final token = await tokenProvider.getToken();
    if (token != null && token.isNotEmpty) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    super.onRequest(options, handler);
  }
}
