import 'package:flutter/material.dart';
import '../../../../shared/widgets/app_card.dart';
import '../../../../shared/widgets/app_status_indicator.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../predictions/data/models/prediction_model.dart';

class DashboardRiskCard extends StatelessWidget {
  final PredictionModel prediction;

  const DashboardRiskCard({super.key, required this.prediction});

  RiskState _mapRiskLevelToState(RiskLevel level) {
    switch (level) {
      case RiskLevel.safe:
        return RiskState.safe;
      case RiskLevel.watch:
        return RiskState.watch;
      case RiskLevel.warning:
        return RiskState.warning;
      case RiskLevel.danger:
        return RiskState.danger;
      case RiskLevel.emergency:
        return RiskState.emergency;
      default:
        return RiskState.safe;
    }
  }
  
  String _formatTime(DateTime dt) {
    return '${dt.hour.toString().padLeft(2, '0')}:${dt.minute.toString().padLeft(2, '0')}';
  }

  @override
  Widget build(BuildContext context) {
    final riskState = _mapRiskLevelToState(prediction.riskLevel);
    final isEmergency = riskState == RiskState.emergency;

    return AppCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Current Risk',
                style: AppTypography.title.copyWith(
                  color: isEmergency ? AppColors.red700 : null,
                  fontWeight: isEmergency ? FontWeight.bold : null,
                ),
              ),
              Text(
                'Updated ${_formatTime(prediction.predictionTime)}',
                style: AppTypography.caption.copyWith(color: AppColors.gray500),
              ),
            ],
          ),
          const SizedBox(height: 16),
          AppStatusIndicator(
            state: riskState,
            label: '${prediction.riskLevel.name.toUpperCase()} (Score: ${prediction.riskScore.toStringAsFixed(1)})',
          ),
          if (prediction.recommendation != null && prediction.recommendation!.isNotEmpty) ...[
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: isEmergency ? AppColors.red700.withValues(alpha: 0.1) : AppColors.gray100,
                borderRadius: BorderRadius.circular(8),
                border: isEmergency ? Border.all(color: AppColors.red700) : null,
              ),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(
                    Icons.info_outline,
                    color: isEmergency ? AppColors.red700 : AppColors.primaryLight,
                    size: 20,
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Recommendation',
                          style: AppTypography.label.copyWith(
                            color: isEmergency ? AppColors.red700 : null,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          prediction.recommendation!,
                          style: AppTypography.body.copyWith(
                            color: isEmergency ? AppColors.red700 : null,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }
}
