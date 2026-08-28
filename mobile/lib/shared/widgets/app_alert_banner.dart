import 'package:flutter/material.dart';
import '../../app/theme/app_colors.dart';
import '../../app/theme/app_icons.dart';
import '../../app/theme/app_typography.dart';
import '../../app/theme/app_radius.dart';
import '../../app/theme/app_spacing.dart';
import 'app_status_indicator.dart';

class AppAlertBanner extends StatelessWidget {
  final RiskState state;
  final String title;
  final String? description;
  final VoidCallback? onAction;
  final String? actionLabel;

  const AppAlertBanner({
    super.key,
    required this.state,
    required this.title,
    this.description,
    this.onAction,
    this.actionLabel,
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
        bgColor = AppColors.emergency;
        fgColor = AppColors.onEmergency;
        icon = AppIcons.emergency;
        break;
    }

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(AppSpacing.s16),
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: AppRadius.large,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          Row(
            children: [
              Icon(icon, color: fgColor),
              const SizedBox(width: AppSpacing.s12),
              Expanded(
                child: Text(
                  title,
                  style: AppTypography.title.copyWith(color: fgColor),
                ),
              ),
            ],
          ),
          if (description != null) ...[
            const SizedBox(height: AppSpacing.s8),
            Text(
              description!,
              style: AppTypography.body.copyWith(color: fgColor.withValues(alpha: 0.9)),
            ),
          ],
          if (onAction != null && actionLabel != null) ...[
            const SizedBox(height: AppSpacing.s12),
            Align(
              alignment: Alignment.centerRight,
              child: TextButton(
                onPressed: onAction,
                style: TextButton.styleFrom(foregroundColor: fgColor),
                child: Text(actionLabel!),
              ),
            ),
          ]
        ],
      ),
    );
  }
}
