import 'package:flutter/material.dart';
import '../../../../shared/widgets/app_card.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../predictions/data/models/prediction_model.dart';

class DashboardExplanationCard extends StatelessWidget {
  final PredictionExplanationModel explanation;

  const DashboardExplanationCard({super.key, required this.explanation});

  @override
  Widget build(BuildContext context) {
    return AppCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Decision Explanation',
            style: AppTypography.title,
          ),
          const SizedBox(height: 12),
          if (explanation.reasonSummary.isNotEmpty) ...[
            Text(
              explanation.reasonSummary,
              style: AppTypography.body,
            ),
            const SizedBox(height: 16),
          ],
          if (explanation.primaryRiskFactors.isNotEmpty) ...[
            Text(
              'Primary Risk Factors',
              style: AppTypography.label.copyWith(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            ...explanation.primaryRiskFactors.map((factor) => _buildBulletPoint(factor)),
            const SizedBox(height: 16),
          ],
          if (explanation.supportingObservations.isNotEmpty) ...[
            Text(
              'Supporting Observations',
              style: AppTypography.label.copyWith(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            ...explanation.supportingObservations.map((obs) => _buildBulletPoint(obs)),
          ],
        ],
      ),
    );
  }

  Widget _buildBulletPoint(String text) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 6.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Padding(
            padding: EdgeInsets.only(top: 6.0, right: 8.0),
            child: Icon(Icons.circle, size: 6, color: AppColors.gray500),
          ),
          Expanded(
            child: Text(text, style: AppTypography.body),
          ),
        ],
      ),
    );
  }
}
