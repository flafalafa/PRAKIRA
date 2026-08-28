import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:shared_preferences/shared_preferences.dart';

abstract class LocalStorage {
  Future<void> saveString(String key, String value);
  Future<String?> getString(String key);
  Future<void> delete(String key);
  Future<void> clear();
}

abstract class SecureStorage {
  Future<void> saveSecret(String key, String value);
  Future<String?> getSecret(String key);
  Future<void> deleteSecret(String key);
  Future<void> clearSecrets();
}

class StorageProvider implements LocalStorage, SecureStorage {
  static late SharedPreferences _sharedPrefs;
  static const FlutterSecureStorage _secureStorage = FlutterSecureStorage();
  
  static final StorageProvider _instance = StorageProvider._internal();
  factory StorageProvider() => _instance;
  StorageProvider._internal();

  static Future<void> init() async {
    _sharedPrefs = await SharedPreferences.getInstance();
  }

  // --- Local Storage Implementation ---
  @override
  Future<void> saveString(String key, String value) async {
    await _sharedPrefs.setString(key, value);
  }

  @override
  Future<String?> getString(String key) async {
    return _sharedPrefs.getString(key);
  }

  @override
  Future<void> delete(String key) async {
    await _sharedPrefs.remove(key);
  }

  @override
  Future<void> clear() async {
    await _sharedPrefs.clear();
  }

  // --- Secure Storage Implementation ---
  @override
  Future<void> saveSecret(String key, String value) async {
    await _secureStorage.write(key: key, value: value);
  }

  @override
  Future<String?> getSecret(String key) async {
    return await _secureStorage.read(key: key);
  }

  @override
  Future<void> deleteSecret(String key) async {
    await _secureStorage.delete(key: key);
  }

  @override
  Future<void> clearSecrets() async {
    await _secureStorage.deleteAll();
  }
}
