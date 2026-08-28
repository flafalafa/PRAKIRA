import 'package:flutter/foundation.dart';
import '../../../../core/errors/failure.dart';
import '../../../areas/data/models/area_model.dart';
import '../../../predictions/data/models/prediction_model.dart';
import '../../../predictions/data/repositories/prediction_repository.dart';
import '../../../alerts/data/models/alert_model.dart';
import '../../../alerts/data/repositories/alert_repository.dart';

enum DashboardStateStatus {
  initial,
  loading,
  loaded,
  error,
}

class DashboardController extends ChangeNotifier {
  final PredictionRepository predictionRepository;
  final AlertRepository alertRepository;

  DashboardStateStatus _status = DashboardStateStatus.initial;
  DashboardStateStatus get status => _status;

  AreaModel? _activeArea;
  AreaModel? get activeArea => _activeArea;

  PredictionModel? _currentPrediction;
  PredictionModel? get currentPrediction => _currentPrediction;

  AlertModel? _activeAlert;
  AlertModel? get activeAlert => _activeAlert;

  AppFailure? _error;
  AppFailure? get error => _error;

  bool _isRefreshing = false;
  bool get isRefreshing => _isRefreshing;

  DashboardController({
    required this.predictionRepository,
    required this.alertRepository,
  });

  bool get isEmergency =>
      _currentPrediction?.riskLevel == RiskLevel.emergency ||
      _activeAlert?.alertLevel == AlertLevel.emergency;

  Future<void> loadDashboard(AreaModel area) async {
    if (_status == DashboardStateStatus.loading) return;

    _activeArea = area;
    _status = DashboardStateStatus.loading;
    _error = null;
    notifyListeners();

    await _fetchData(area.areaId);
  }

  Future<void> refreshDashboard() async {
    if (_activeArea == null || _isRefreshing) return;

    _isRefreshing = true;
    notifyListeners();

    await _fetchData(_activeArea!.areaId);

    _isRefreshing = false;
    notifyListeners();
  }

  Future<void> _fetchData(String areaId) async {
    try {
      // Fetch Prediction and Alert concurrently for efficiency.
      // If Prediction fails, we throw to show error state since it's the main data.
      // If Alert fails, we catch it locally and leave it null (partial data).
      
      final predictionFuture = predictionRepository.getCurrentPrediction(areaId);
      final alertFuture = alertRepository.getActiveAlert(areaId).catchError((e) {
        // Log error if needed, but don't fail the whole dashboard
        return null;
      });

      _currentPrediction = await predictionFuture;
      _activeAlert = await alertFuture;

      _status = DashboardStateStatus.loaded;
    } on AppFailure catch (e) {
      _error = e;
      _status = DashboardStateStatus.error;
    } catch (e) {
      _error = const UnknownFailure('An unexpected error occurred while loading the dashboard', 'UNKNOWN_ERROR');
      _status = DashboardStateStatus.error;
    } finally {
      if (!_isRefreshing) {
        notifyListeners();
      }
    }
  }

  void clearDashboard() {
    _activeArea = null;
    _currentPrediction = null;
    _activeAlert = null;
    _status = DashboardStateStatus.initial;
    _error = null;
    notifyListeners();
  }
}
