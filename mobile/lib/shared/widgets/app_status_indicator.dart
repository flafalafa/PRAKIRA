import 'package:flutter/material.dart';
import '../../app/theme/app_colors.dart';
import '../../app/theme/app_icons.dart';
import '../../app/theme/app_typography.dart';
import '../../app/theme/app_radius.dart';
import '../../app/theme/app_spacing.dart';

enum RiskState { safe, watch, warning, danger, emergency }

class AppStatusIndicator extends StatelessWidget {
  final RiskState state;
  final String label;

  const AppStatusIndicator({
    super.key,
    required this.state,
    required this.label,
  });

  @override
  Widget build(BuildContext context) {
    Color bgColor;
    Color fgColor;
    IconData icon;

    final isDark = Theme.of(context).brightness == Brightness.dark;

    switch (state) {
      case RiskState.safe:
        bgColor = isDark ? AppColors.safeBgDark : AppColors.safeBgLight;
        fgColor = AppColors.safe;
        icon = AppIcons.safe;
        break;
      case RiskState.watch:
        bgColor = isDark ? AppColors.watchBgDark : AppColors.watchBgLight;
        fgColor = AppColors.watch;
        icon = AppIcons.info;
        break;
      case RiskState.warning:
        bgColor = isDark ? AppColors.warningBgDark : AppColors.warningBgLight;
        fgColor = AppColors.warning;
        icon = AppIcons.warning;
        break;
      case RiskState.danger:
        bgColor = isDark ? AppColors.dangerBgDark : AppColors.dangerBgLight;
        fgColor = AppColors.danger;
        icon = AppIcons.danger;
        break;
      case RiskState.emergency:
        bgColor = isDark ? AppColors.emergencyBgDark : AppColors.emergencyBgLight;
        fgColor = AppColors.emergency;
        icon = AppIcons.emergency;
        break;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.s12, vertical: AppSpacing.s8),
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: AppRadius.medium,
        border: Border.all(color: fgColor.withValues(alpha: 0.3)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, color: fgColor, size: 20),
          const SizedBox(width: AppSpacing.s8),
          Text(
            label,
            style: AppTypography.label.copyWith(color: fgColor, fontWeight: FontWeight.bold),
          ),
        ],
      ),
    );
  }
}
