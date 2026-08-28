import 'package:flutter/material.dart';
import '../../../../core/di/service_locator.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../shared/widgets/app_loading.dart';
import '../../../../shared/widgets/app_error_state.dart';
import '../../../../shared/widgets/app_empty_state.dart';
import '../../../../shared/widgets/app_alert_banner.dart';
import '../../../../shared/widgets/app_status_indicator.dart' show RiskState;
import '../../../areas/presentation/controllers/area_controller.dart';
import '../controllers/dashboard_controller.dart';
import '../widgets/dashboard_risk_card.dart';
import '../widgets/dashboard_conditions_card.dart';
import '../widgets/dashboard_explanation_card.dart';
import '../../../notifications/presentation/screens/notification_history_screen.dart';
import '../../../alerts/presentation/screens/alert_detail_screen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  final _areaController = ServiceLocator.instance.areaController;
  final _dashboardController = ServiceLocator.instance.dashboardController;

  @override
  void initState() {
    super.initState();
    _areaController.addListener(_onAreaChanged);
    _dashboardController.addListener(_onDashboardStateChanged);
    _loadInitialData();
  }

  @override
  void dispose() {
    _areaController.removeListener(_onAreaChanged);
    _dashboardController.removeListener(_onDashboardStateChanged);
    super.dispose();
  }

  void _onAreaChanged() {
    if (_areaController.status == AreaStateStatus.loaded && _areaController.activeArea != null) {
      if (_dashboardController.activeArea?.areaId != _areaController.activeArea!.areaId) {
        _dashboardController.loadDashboard(_areaController.activeArea!);
      }
    } else if (_areaController.activeArea == null) {
      _dashboardController.clearDashboard();
    }
  }

  void _onDashboardStateChanged() {
    setState(() {});
  }

  void _loadInitialData() {
    if (_areaController.activeArea != null) {
      _dashboardController.loadDashboard(_areaController.activeArea!);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Flood Guardian',
              style: AppTypography.label.copyWith(color: AppColors.gray500),
            ),
            Text(
              _dashboardController.activeArea?.areaName ?? 'Select an Area',
              style: AppTypography.headline,
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications_outlined),
            tooltip: 'Notifications',
            onPressed: () {
              if (_dashboardController.activeArea != null) {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => NotificationHistoryScreen(
                      areaId: _dashboardController.activeArea!.areaId,
                    ),
                  ),
                );
              }
            },
          ),
          if (_dashboardController.status != DashboardStateStatus.initial &&
              _dashboardController.status != DashboardStateStatus.loading)
            IconButton(
              icon: _dashboardController.isRefreshing
                  ? const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Icon(Icons.refresh),
              onPressed: _dashboardController.isRefreshing
                  ? null
                  : _dashboardController.refreshDashboard,
              tooltip: 'Refresh Dashboard',
            ),
        ],
      ),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_areaController.activeArea == null) {
      return Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Expanded(
              child: AppEmptyState(
                title: 'No Area Selected',
                message: 'Please select an area to view the flood dashboard.',
                icon: Icons.location_off,
              ),
            ),
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.blue500,
                foregroundColor: AppColors.white,
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
              onPressed: () {
                Navigator.pushNamed(context, '/areas'); // Let's use string literal to avoid needing to import AppRouter here if it's not imported. Wait, AppRouter is not imported. 
              },
              child: const Text('Select Area', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            ),
          ],
        ),
      );
    }

    switch (_dashboardController.status) {
      case DashboardStateStatus.initial:
      case DashboardStateStatus.loading:
        return const AppLoading();
      case DashboardStateStatus.error:
        return AppErrorState(
          title: 'Failed to Load Dashboard',
          message: _dashboardController.error?.message ?? 'An unknown error occurred.',
          onRetry: () => _dashboardController.loadDashboard(_areaController.activeArea!),
        );
      case DashboardStateStatus.loaded:
        return _buildDashboardContent();
    }
  }

  Widget _buildDashboardContent() {
    final prediction = _dashboardController.currentPrediction;
    final alert = _dashboardController.activeAlert;

    if (prediction == null) {
      return const Padding(
        padding: EdgeInsets.all(24.0),
        child: AppEmptyState(
          title: 'No Active Prediction',
          message: 'There is currently no active flood prediction data for this area. Please check back later.',
          icon: Icons.analytics_outlined,
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: _dashboardController.refreshDashboard,
      child: ListView(
        padding: const EdgeInsets.all(16.0),
        children: [
          if (alert != null) ...[
            GestureDetector(
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => AlertDetailScreen(alertId: alert.alertId),
                  ),
                );
              },
              child: AppAlertBanner(
                title: alert.title,
                description: alert.message,
                state: _mapAlertState(alert.alertLevel.name),
                actionLabel: 'Details',
                onAction: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => AlertDetailScreen(alertId: alert.alertId),
                    ),
                  );
                },
              ),
            ),
            const SizedBox(height: 16),
          ],
          DashboardRiskCard(prediction: prediction),
          const SizedBox(height: 16),
          DashboardConditionsCard(prediction: prediction),
          if (prediction.explanation != null) ...[
            const SizedBox(height: 16),
            DashboardExplanationCard(explanation: prediction.explanation!),
          ],
          const SizedBox(height: 32),
          Center(
            child: Text(
              'Data provided by Flood Guardian Backend',
              style: AppTypography.caption.copyWith(color: AppColors.gray500),
            ),
          ),
        ],
      ),
    );
  }

  RiskState _mapAlertState(String level) {
    switch (level.toLowerCase()) {
      case 'emergency':
        return RiskState.emergency;
      case 'danger':
        return RiskState.danger;
      case 'warning':
        return RiskState.warning;
      case 'watch':
        return RiskState.watch;
      default:
        return RiskState.safe;
    }
  }
}
