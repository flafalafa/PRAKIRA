import 'package:flutter_secure_storage/flutter_secure_storage.dart';

abstract class SecureTokenStorage {
  Future<void> saveAccessToken(String token);
  Future<String?> getAccessToken();
  Future<void> deleteAccessToken();
  Future<void> clearAll();
}

class FlutterSecureTokenStorageImpl implements SecureTokenStorage {
  final FlutterSecureStorage _storage;
  static const String _accessTokenKey = 'secure_access_token';

  FlutterSecureTokenStorageImpl({FlutterSecureStorage? storage})
      : _storage = storage ?? const FlutterSecureStorage();

  @override
  Future<void> saveAccessToken(String token) async {
    await _storage.write(key: _accessTokenKey, value: token);
  }

  @override
  Future<String?> getAccessToken() async {
    return await _storage.read(key: _accessTokenKey);
  }

  @override
  Future<void> deleteAccessToken() async {
    await _storage.delete(key: _accessTokenKey);
  }

  @override
  Future<void> clearAll() async {
    await _storage.deleteAll();
  }
}
