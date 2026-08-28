import 'package:flutter_test/flutter_test.dart';
import 'package:flood_guardian/core/errors/failure.dart';
import 'package:flood_guardian/core/errors/network_exceptions.dart';
import 'package:flood_guardian/core/storage/secure_token_storage.dart';
import 'package:flood_guardian/core/storage/session_manager.dart';
import 'package:flood_guardian/features/auth/data/models/login_request.dart';
import 'package:flood_guardian/features/auth/data/models/auth_response.dart';
import 'package:flood_guardian/features/auth/data/datasources/auth_remote_datasource.dart';
import 'package:flood_guardian/features/auth/data/repositories/auth_repository.dart';
import 'package:flood_guardian/features/auth/presentation/controllers/auth_controller.dart';
import 'package:flood_guardian/core/network/models/api_response.dart';
import 'package:flood_guardian/core/network/models/api_meta.dart';

class MockSecureTokenStorage implements SecureTokenStorage {
  String? _token;

  @override
  Future<void> saveAccessToken(String token) async {
    _token = token;
  }

  @override
  Future<String?> getAccessToken() async {
    return _token;
  }

  @override
  Future<void> deleteAccessToken() async {
    _token = null;
  }

  @override
  Future<void> clearAll() async {
    _token = null;
  }
}

class MockAuthRemoteDataSource implements AuthRemoteDataSource {
  bool shouldThrow = false;
  bool networkFailure = false;
  bool shouldFailLogout = false;

  @override
  Future<SuccessResponse<AuthResponse>> login(LoginRequest request) async {
    if (networkFailure) {
      throw ServerException(message: 'Server error');
    }
    if (shouldThrow || request.password == 'wrong_password') {
      throw UnauthorizedException(message: 'Invalid credentials');
    }
      return SuccessResponse(
        data: const AuthResponse(accessToken: 'mock_token_123'),
        meta: const ApiMeta(),
        requestId: 'req-1',
        timestamp: DateTime.now(),
        version: '1',
      );
  }

  @override
  Future<void> logout() async {
    if (shouldFailLogout) {
      throw ServerException(message: 'Network error during logout');
    }
  }
}

void main() {
  group('Auth Layer Tests', () {
    late MockSecureTokenStorage mockStorage;
    late SessionManager sessionManager;
    late MockAuthRemoteDataSource mockRemoteDataSource;
    late AuthRepositoryImpl authRepository;
    late AuthController authController;

    setUp(() {
      mockStorage = MockSecureTokenStorage();
      sessionManager = SessionManager(storage: mockStorage);
      mockRemoteDataSource = MockAuthRemoteDataSource();
      authRepository = AuthRepositoryImpl(
        remoteDataSource: mockRemoteDataSource,
        sessionManager: sessionManager,
      );
      authController = AuthController(
        repository: authRepository,
        sessionManager: sessionManager,
      );
    });

    test('SessionManager initializes and restores session', () async {
      await mockStorage.saveAccessToken('existing_token');
      await sessionManager.initialize();
      expect(await sessionManager.getToken(), 'existing_token');
      expect(await sessionManager.hasValidSession(), isTrue);
    });

    test('AuthRepository login success saves token', () async {
      const request = LoginRequest(username: 'user', password: 'password');
      await authRepository.login(request);
      
      expect(await mockStorage.getAccessToken(), 'mock_token_123');
    });

    test('AuthRepository login failure does not save token', () async {
      const request = LoginRequest(username: 'user', password: 'wrong_password');
      
      try {
        await authRepository.login(request);
        fail('Should throw AppFailure');
      } catch (e) {
        expect(e, isA<AppFailure>());
      }
      expect(await mockStorage.getAccessToken(), isNull);
    });

    test('AuthRepository logout clears local session even if backend fails', () async {
      await sessionManager.saveSession('token_123');
      mockRemoteDataSource.shouldFailLogout = true;
      
      try {
        await authRepository.logout();
        fail('Should throw AppFailure');
      } catch (e) {
        expect(e, isA<AppFailure>());
      }
      expect(await mockStorage.getAccessToken(), isNull); // Local session still cleared
    });

    test('AuthController state transitions during successful login', () async {
      expect(authController.status, AuthStatus.unauthenticated);
      
      // We don't await immediately to check intermediate state
      final loginFuture = authController.login('user', 'password');
      expect(authController.status, AuthStatus.authenticating);
      
      await loginFuture;
      expect(authController.status, AuthStatus.authenticated);
      expect(authController.error, isNull);
    });

    test('AuthController state transitions during failed login', () async {
      expect(authController.status, AuthStatus.unauthenticated);
      
      await authController.login('user', 'wrong_password');
      
      expect(authController.status, AuthStatus.authenticationFailure);
      expect(authController.error, isA<UnauthorizedFailure>());
    });

    test('AuthController restoreSession handles existing session', () async {
      await mockStorage.saveAccessToken('token');
      await authController.restoreSession();
      expect(authController.status, AuthStatus.authenticated);
    });

    test('AuthController logout clears state', () async {
      await authController.login('user', 'password');
      expect(authController.status, AuthStatus.authenticated);
      
      await authController.logout();
      expect(authController.status, AuthStatus.unauthenticated);
      expect(await sessionManager.hasValidSession(), isFalse);
    });
  });
}
