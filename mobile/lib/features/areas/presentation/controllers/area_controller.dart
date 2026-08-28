import 'package:flutter/foundation.dart';
import '../../../../core/errors/failure.dart';
import '../../../../core/logging/app_logger.dart';
import '../../data/models/area_model.dart';
import '../../data/repositories/area_repository.dart';

enum AreaStateStatus {
  initial,
  loading,
  loaded,
  empty,
  error,
}

class AreaController extends ChangeNotifier {
  final AreaRepository _repository;

  AreaStateStatus _status = AreaStateStatus.initial;
  AppFailure? _error;
  List<AreaModel> _areas = [];
  AreaModel? _activeArea;

  AreaController({required AreaRepository repository}) : _repository = repository {
    AppLogger.debug('AREA: Initializing AreaController');
  }

  AreaStateStatus get status => _status;
  AppFailure? get error => _error;
  List<AreaModel> get areas => _areas;
  AreaModel? get activeArea => _activeArea;

  Future<void> loadAreas({int page = 1, int pageSize = 20}) async {
    AppLogger.debug('AREA: Loading available areas (page: $page, size: $pageSize)');
    _status = AreaStateStatus.loading;
    _error = null;
    notifyListeners();

    try {
      final response = await _repository.getAreas(page: page, pageSize: pageSize);
      _areas = response.data;
      
      AppLogger.debug('AREA: ${_areas.length} areas loaded');
      
      if (_areas.isEmpty) {
        _status = AreaStateStatus.empty;
      } else {
        _status = AreaStateStatus.loaded;
      }
      notifyListeners();
    } on AppFailure catch (failure) {
      AppLogger.debug('AREA: API Error - ${failure.message}');
      _status = AreaStateStatus.error;
      _error = failure;
      notifyListeners();
    } catch (e) {
      AppLogger.debug('AREA: Unknown Error - $e');
      _status = AreaStateStatus.error;
      _error = UnknownFailure(e.toString(), 'UNKNOWN_ERROR');
      notifyListeners();
    }
  }

  Future<void> restoreActiveArea() async {
    AppLogger.debug('AREA: Restoring previously selected area...');
    try {
      final areaId = await _repository.getSelectedAreaId();
      if (areaId != null) {
        AppLogger.debug('AREA: Found saved area ID: $areaId, fetching details...');
        final response = await _repository.getAreaById(areaId);
        _activeArea = response.data;
        AppLogger.debug('AREA: Area selection restored successfully: ${_activeArea?.areaName}');
        notifyListeners();
      } else {
        AppLogger.debug('AREA: No previously selected area found.');
      }
    } catch (e) {
      AppLogger.debug('AREA: Failed to restore area: $e');
      // If restoration fails (e.g., area deleted from backend), clear it safely
      await _repository.clearSelectedAreaId();
      _activeArea = null;
      notifyListeners();
    }
  }

  Future<void> selectArea(String areaId) async {
    AppLogger.debug('AREA: Selecting area: $areaId');
    // Validate that the area exists in our loaded list or fetch it
    try {
      final targetArea = _areas.firstWhere(
        (a) => a.areaId == areaId,
        orElse: () => throw Exception('Area not found in loaded list'),
      );
      
      await _repository.saveSelectedAreaId(areaId);
      _activeArea = targetArea;
      AppLogger.debug('AREA: Saving selected area = ${_activeArea?.areaName}');
      notifyListeners();
    } catch (e) {
      AppLogger.debug('AREA: Area not in list, fetching from backend...');
      // Fallback: Try fetching from backend if not in loaded list
      try {
        final response = await _repository.getAreaById(areaId);
        await _repository.saveSelectedAreaId(areaId);
        _activeArea = response.data;
        AppLogger.debug('AREA: Saving selected area = ${_activeArea?.areaName}');
        notifyListeners();
      } catch (innerE) {
        AppLogger.debug('AREA: Selection Error - $innerE');
        _status = AreaStateStatus.error;
        _error = UnknownFailure('Failed to select area: $innerE', 'SELECTION_ERROR');
        notifyListeners();
      }
    }
  }

  Future<void> clearSelection() async {
    AppLogger.debug('AREA: Clearing area selection');
    await _repository.clearSelectedAreaId();
    _activeArea = null;
    notifyListeners();
  }
}
