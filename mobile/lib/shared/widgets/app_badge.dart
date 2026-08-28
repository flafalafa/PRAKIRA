import 'package:flutter/material.dart';
import '../../app/theme/app_typography.dart';
import '../../app/theme/app_radius.dart';
import '../../app/theme/app_colors.dart';

class AppBadge extends StatelessWidget {
  final String text;
  final Color? color;
  final Color? textColor;

  const AppBadge({
    super.key,
    required this.text,
    this.color,
    this.textColor,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 2.0),
      decoration: BoxDecoration(
        color: color ?? AppColors.danger,
        borderRadius: AppRadius.full,
      ),
      child: Text(
        text,
        style: AppTypography.navigation.copyWith(
          color: textColor ?? AppColors.white,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}
