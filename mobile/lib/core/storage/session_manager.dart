import '../network/token_provider.dart';
import 'secure_token_storage.dart';

class SessionManager implements TokenProvider {
  final SecureTokenStorage _storage;
  
  String? _cachedToken;
  bool _isInitialized = false;

  SessionManager({required SecureTokenStorage storage}) : _storage = storage;

  /// Initializes the session manager by loading the token from secure storage.
  /// This should be called during app startup.
  Future<void> initialize() async {
    if (_isInitialized) return;
    _cachedToken = await _storage.getAccessToken();
    _isInitialized = true;
  }

  @override
  Future<String?> getToken() async {
    if (!_isInitialized) {
      await initialize();
    }
    return _cachedToken;
  }

  /// Checks if a valid session exists.
  Future<bool> hasValidSession() async {
    final token = await getToken();
    return token != null && token.isNotEmpty;
  }

  /// Saves the session securely.
  Future<void> saveSession(String accessToken) async {
    await _storage.saveAccessToken(accessToken);
    _cachedToken = accessToken;
  }

  /// Clears the session securely.
  Future<void> clearSession() async {
    await _storage.clearAll();
    _cachedToken = null;
  }
}
