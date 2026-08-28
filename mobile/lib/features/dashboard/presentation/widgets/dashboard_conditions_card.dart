import 'package:flutter/material.dart';
import '../../../../shared/widgets/app_card.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../predictions/data/models/prediction_model.dart';

class DashboardConditionsCard extends StatelessWidget {
  final PredictionModel prediction;

  const DashboardConditionsCard({super.key, required this.prediction});
  
  String _formatDateTime(DateTime dt) {
    final month = _monthName(dt.month);
    final time = '${dt.hour.toString().padLeft(2, '0')}:${dt.minute.toString().padLeft(2, '0')}';
    return '$month ${dt.day}, $time';
  }
  
  String _monthName(int month) {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    if (month >= 1 && month <= 12) return months[month - 1];
    return '';
  }

  @override
  Widget build(BuildContext context) {
    final factors = prediction.supportingFactors;
    final waterLevel = factors['water_level'];
    final rainfall = factors['rainfall'];
    
    // Determine if we have any valid conditions to show
    if (waterLevel == null && rainfall == null && prediction.estimatedArrivalTime == null) {
      return const SizedBox.shrink();
    }

    return AppCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Key Conditions',
            style: AppTypography.title,
          ),
          const SizedBox(height: 16),
          if (waterLevel != null) _buildConditionRow(
            icon: Icons.water,
            title: 'Water Level',
            value: waterLevel.toString(),
          ),
          if (rainfall != null) ...[
            const SizedBox(height: 12),
            _buildConditionRow(
              icon: Icons.cloud_queue,
              title: 'Rainfall',
              value: rainfall.toString(),
            ),
          ],
          if (prediction.estimatedArrivalTime != null) ...[
            const SizedBox(height: 12),
            _buildConditionRow(
              icon: Icons.radar,
              title: 'Estimated Arrival',
              value: _formatDateTime(prediction.estimatedArrivalTime!),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildConditionRow({
    required IconData icon,
    required String title,
    required String value,
  }) {
    return Row(
      children: [
        Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: AppColors.primaryLight.withValues(alpha: 0.1),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Icon(icon, color: AppColors.primaryLight, size: 24),
        ),
        const SizedBox(width: 16),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(title, style: AppTypography.caption),
              Text(
                value,
                style: AppTypography.label.copyWith(fontWeight: FontWeight.bold),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
