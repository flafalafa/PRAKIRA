import 'package:flutter/material.dart';
import '../../../../core/di/service_locator.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../shared/widgets/app_status_indicator.dart';
import '../../../../shared/widgets/app_loading.dart';
import '../../../../shared/widgets/app_error_state.dart';
import '../../data/models/alert_model.dart';

class AlertDetailScreen extends StatefulWidget {
  final String alertId;

  const AlertDetailScreen({super.key, required this.alertId});

  @override
  State<AlertDetailScreen> createState() => _AlertDetailScreenState();
}

class _AlertDetailScreenState extends State<AlertDetailScreen> {
  final _alertRepository = ServiceLocator.instance.alertRepository;
  AlertModel? _alert;
  bool _isLoading = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _fetchAlert();
  }

  Future<void> _fetchAlert() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final alert = await _alertRepository.getAlertById(widget.alertId);
      setState(() {
        _alert = alert;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = e.toString();
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Alert Details', style: AppTypography.title),
      ),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_isLoading) {
      return const AppLoading();
    }
    
    if (_errorMessage != null) {
      return AppErrorState(
        title: 'Failed to Load Alert',
        message: _errorMessage!,
        onRetry: _fetchAlert,
      );
    }

    if (_alert == null) {
      return const Center(child: Text('Alert not found'));
    }

    return SingleChildScrollView(
      padding: const EdgeInsets.all(AppSpacing.s16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Basic Alert Info
          _buildAlertHeader(_alert!),
          const SizedBox(height: AppSpacing.s24),
          _buildSection('Message', _alert!.message),
          if (_alert!.recommendation != null) ...[
            const SizedBox(height: AppSpacing.s16),
            _buildSection('Recommendation', _alert!.recommendation!),
          ],
          if (_alert!.explanation != null) ...[
            const SizedBox(height: AppSpacing.s24),
            _buildExplanation(_alert!.explanation!),
          ],
        ],
      ),
    );
  }

  Widget _buildAlertHeader(AlertModel alert) {
    return Row(
      children: [
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                alert.title,
                style: AppTypography.headline,
              ),
              const SizedBox(height: AppSpacing.s8),
              Text(
                'Issued: ${alert.issuedAt.toLocal().toString().split('.')[0]}',
                style: AppTypography.caption.copyWith(color: AppColors.gray500),
              ),
            ],
          ),
        ),
        AppStatusIndicator(
          state: _mapAlertState(alert.alertLevel.name),
          label: alert.alertLevel.name.toUpperCase(),
        ),
      ],
    );
  }

  Widget _buildSection(String title, String content) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(title, style: AppTypography.label.copyWith(fontWeight: FontWeight.bold)),
        const SizedBox(height: AppSpacing.s8),
        Text(content, style: AppTypography.body),
      ],
    );
  }

  Widget _buildExplanation(AlertExplanationModel explanation) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Explanation', style: AppTypography.title),
        const SizedBox(height: AppSpacing.s12),
        if (explanation.primaryRiskFactors.isNotEmpty) ...[
          Text('Primary Risk Factors:', style: AppTypography.label.copyWith(fontWeight: FontWeight.bold)),
          ...explanation.primaryRiskFactors.map((f) => Text('• $f', style: AppTypography.body)),
          const SizedBox(height: AppSpacing.s8),
        ],
        if (explanation.supportingObservations.isNotEmpty) ...[
          Text('Supporting Observations:', style: AppTypography.label.copyWith(fontWeight: FontWeight.bold)),
          ...explanation.supportingObservations.map((o) => Text('• $o', style: AppTypography.body)),
        ]
      ],
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
