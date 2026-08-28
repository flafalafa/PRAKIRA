import 'package:flutter/material.dart';
import '../../app/theme/app_icons.dart';
import '../../app/theme/app_typography.dart';
import '../../app/theme/app_spacing.dart';
import '../../app/theme/app_colors.dart';
import 'app_button.dart';

class AppEmptyState extends StatelessWidget {
  final String title;
  final String message;
  final IconData? icon;
  final VoidCallback? onAction;
  final String? actionLabel;

  const AppEmptyState({
    super.key,
    required this.title,
    required this.message,
    this.icon,
    this.onAction,
    this.actionLabel,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.s32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              icon ?? AppIcons.info,
              size: 64,
              color: AppColors.gray400,
            ),
            const SizedBox(height: AppSpacing.s16),
            Text(
              title,
              style: AppTypography.title,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: AppSpacing.s8),
            Text(
              message,
              style: AppTypography.body,
              textAlign: TextAlign.center,
            ),
            if (onAction != null && actionLabel != null) ...[
              const SizedBox(height: AppSpacing.s24),
              AppButton(
                label: actionLabel!,
                onPressed: onAction,
                type: AppButtonType.secondary,
              ),
            ]
          ],
        ),
      ),
    );
  }
}
