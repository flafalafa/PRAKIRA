import 'package:flutter/foundation.dart';
import '../../../../core/errors/failure.dart';
import '../../data/models/login_request.dart';
import '../../data/repositories/auth_repository.dart';
import '../../../../core/storage/session_manager.dart';

enum AuthStatus {
  unauthenticated,
  authenticating,
  authenticated,
  loggingOut,
  authenticationFailure,
  sessionExpired,
}

class AuthController extends ChangeNotifier {
  final AuthRepository _repository;
  final SessionManager _sessionManager;

  AuthStatus _status = AuthStatus.unauthenticated;
  AppFailure? _error;

  AuthController({
    required AuthRepository repository,
    required SessionManager sessionManager,
  })  : _repository = repository,
        _sessionManager = sessionManager;

  AuthStatus get status => _status;
  AppFailure? get error => _error;

  /// Restores the session on app startup
  Future<void> restoreSession() async {
    await _sessionManager.initialize();
    final hasValidSession = await _sessionManager.hasValidSession();
    
    if (hasValidSession) {
      _status = AuthStatus.authenticated;
    } else {
      _status = AuthStatus.unauthenticated;
    }
    notifyListeners();
  }

  Future<void> login(String username, String password) async {
    if (_status == AuthStatus.authenticating) return;

    _status = AuthStatus.authenticating;
    _error = null;
    notifyListeners();

    final request = LoginRequest(username: username, password: password);
    try {
      await _repository.login(request);
      _status = AuthStatus.authenticated;
      _error = null;
      notifyListeners();
    } on AppFailure catch (failure) {
      _status = AuthStatus.authenticationFailure;
      _error = failure;
      notifyListeners();
    } catch (e) {
      _status = AuthStatus.authenticationFailure;
      _error = UnknownFailure(e.toString(), 'UNKNOWN_ERROR');
      notifyListeners();
    }
  }

  Future<void> logout() async {
    if (_status == AuthStatus.loggingOut || _status == AuthStatus.unauthenticated) {
      return;
    }

    _status = AuthStatus.loggingOut;
    notifyListeners();

    await _repository.logout();
    
    _status = AuthStatus.unauthenticated;
    notifyListeners();
  }

  /// Called when a 401 Unauthorized is caught globally
  void forceSessionExpired() {
    _status = AuthStatus.sessionExpired;
    _sessionManager.clearSession();
    notifyListeners();
  }
}
