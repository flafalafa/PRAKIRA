import 'package:flutter/material.dart';
import '../../app/theme/app_colors.dart';
import '../../app/theme/app_typography.dart';
import '../../app/theme/app_radius.dart';
import '../../app/theme/app_spacing.dart';

class AppChip extends StatelessWidget {
  final String label;
  final IconData? icon;
  final VoidCallback? onDeleted;
  final VoidCallback? onTap;
  final bool isSelected;
  final Color? color;

  const AppChip({
    super.key,
    required this.label,
    this.icon,
    this.onDeleted,
    this.onTap,
    this.isSelected = false,
    this.color,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    final bgColor = isSelected 
        ? (color ?? theme.colorScheme.primary) 
        : (isDark ? AppColors.gray800 : AppColors.gray200);
    
    final fgColor = isSelected
        ? AppColors.white
        : (isDark ? AppColors.gray300 : AppColors.gray700);

    return ActionChip(
      label: Text(label),
      avatar: icon != null ? Icon(icon, size: 16, color: fgColor) : null,
      onPressed: onTap,
      backgroundColor: bgColor,
      labelStyle: AppTypography.caption.copyWith(color: fgColor, fontWeight: isSelected ? FontWeight.w600 : FontWeight.w500),
      shape: const RoundedRectangleBorder(borderRadius: AppRadius.full),
      side: BorderSide.none,
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.s8, vertical: AppSpacing.s4),
    );
  }
}
