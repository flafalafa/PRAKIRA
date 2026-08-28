import '../../../../core/errors/failure.dart';
import '../../../../core/errors/network_exceptions.dart';
import '../../../../core/storage/session_manager.dart';
import '../models/login_request.dart';
import '../datasources/auth_remote_datasource.dart';

abstract class AuthRepository {
  Future<void> login(LoginRequest request);
  Future<void> logout();
}

class AuthRepositoryImpl implements AuthRepository {
  final AuthRemoteDataSource remoteDataSource;
  final SessionManager sessionManager;

  AuthRepositoryImpl({
    required this.remoteDataSource,
    required this.sessionManager,
  });

  @override
  Future<void> login(LoginRequest request) async {
    try {
      final response = await remoteDataSource.login(request);
      
      // Save session securely
      await sessionManager.saveSession(response.data.accessToken);
    } on NetworkException catch (e) {
      throw mapExceptionToFailure(e);
    } catch (e) {
      throw UnknownFailure(e.toString(), 'UNKNOWN_ERROR');
    }
  }

  @override
  Future<void> logout() async {
    try {
      // First, attempt to clear the backend session
      await remoteDataSource.logout();
      
      // Always clear the local session regardless of backend success
      await sessionManager.clearSession();
    } on NetworkException catch (e) {
      // Even if network fails, we clear the local session for safety
      await sessionManager.clearSession();
      throw mapExceptionToFailure(e);
    } catch (e) {
      await sessionManager.clearSession();
      throw UnknownFailure(e.toString(), 'UNKNOWN_ERROR');
    }
  }
}
