import '../../../../core/network/models/api_response.dart';
import '../../../../core/network/models/api_meta.dart';
import '../../../../core/errors/network_exceptions.dart';
import '../models/login_request.dart';
import '../models/auth_response.dart';

abstract class AuthRemoteDataSource {
  Future<SuccessResponse<AuthResponse>> login(LoginRequest request);
  Future<void> logout();
}

class MockAuthRemoteDataSourceImpl implements AuthRemoteDataSource {
  
  @override
  Future<SuccessResponse<AuthResponse>> login(LoginRequest request) async {
    // Simulate network delay
    await Future.delayed(const Duration(seconds: 1));

    // Hardcoded valid token based on JWTAuthenticationProvider in backend
    // which accepts "valid_user_token"
    if (request.username.isNotEmpty && request.password.isNotEmpty) {
      if (request.password != 'wrong_password') {
        return SuccessResponse(
          data: const AuthResponse(accessToken: 'valid_user_token'),
          meta: const ApiMeta(),
          requestId: 'mock-request-id',
          timestamp: DateTime.now(),
          version: '1.0',
        );
      } else {
        throw UnauthorizedException(message: 'Invalid username or password');
      }
    } else {
      throw ValidationException(message: 'Username and password are required');
    }
  }

  @override
  Future<void> logout() async {
    // Simulate network delay
    await Future.delayed(const Duration(milliseconds: 500));
    // No-op for mock, simulates successful backend invalidation
  }
}
