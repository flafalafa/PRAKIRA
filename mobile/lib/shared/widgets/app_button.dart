import 'package:flutter/material.dart';
import '../../app/theme/app_colors.dart';

enum AppButtonType { primary, secondary, danger, emergency }

class AppButton extends StatelessWidget {
  final String label;
  final VoidCallback? onPressed;
  final AppButtonType type;
  final bool isLoading;
  final IconData? icon;

  const AppButton({
    super.key,
    required this.label,
    required this.onPressed,
    this.type = AppButtonType.primary,
    this.isLoading = false,
    this.icon,
  });

  @override
  Widget build(BuildContext context) {
    if (type == AppButtonType.secondary) {
      return OutlinedButton(
        onPressed: isLoading ? null : onPressed,
        style: OutlinedButton.styleFrom(
          side: BorderSide(
            color: onPressed == null ? AppColors.disabledLight : AppColors.primaryLight,
          ),
        ),
        child: _buildChild(),
      );
    }

    Color bgColor;
    Color fgColor = AppColors.white;

    switch (type) {
      case AppButtonType.danger:
        bgColor = AppColors.danger;
        break;
      case AppButtonType.emergency:
        bgColor = AppColors.emergency;
        break;
      case AppButtonType.primary:
      default:
        bgColor = AppColors.primaryLight;
        break;
    }

    return ElevatedButton(
      onPressed: isLoading ? null : onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: bgColor,
        foregroundColor: fgColor,
      ),
      child: _buildChild(fgColor),
    );
  }

  Widget _buildChild([Color? color]) {
    if (isLoading) {
      return SizedBox(
        height: 24,
        width: 24,
        child: CircularProgressIndicator(
          strokeWidth: 2.5,
          valueColor: AlwaysStoppedAnimation<Color>(color ?? AppColors.primaryLight),
        ),
      );
    }

    if (icon != null) {
      return Row(
        mainAxisSize: MainAxisSize.min,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, size: 20),
          const SizedBox(width: 8),
          Text(label),
        ],
      );
    }

    return Text(label);
  }
}
