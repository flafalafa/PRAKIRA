import 'package:shared_preferences/shared_preferences.dart';

abstract class AreaSelectionStorage {
  Future<void> saveSelectedAreaId(String areaId);
  Future<String?> getSelectedAreaId();
  Future<void> clearSelectedAreaId();
}

class SharedPrefsAreaSelectionStorageImpl implements AreaSelectionStorage {
  static const String _activeAreaKey = 'ACTIVE_AREA_ID';

  @override
  Future<void> saveSelectedAreaId(String areaId) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_activeAreaKey, areaId);
  }

  @override
  Future<String?> getSelectedAreaId() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_activeAreaKey);
  }

  @override
  Future<void> clearSelectedAreaId() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_activeAreaKey);
  }
}
