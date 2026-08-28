import 'package:flutter/material.dart';
import '../../app/theme/app_colors.dart';

class AppIconButton extends StatelessWidget {
  final IconData icon;
  final VoidCallback? onPressed;
  final String? tooltip;
  final Color? color;
  final double size;

  const AppIconButton({
    super.key,
    required this.icon,
    required this.onPressed,
    this.tooltip,
    this.color,
    this.size = 24.0,
  });

  @override
  Widget build(BuildContext context) {
    return IconButton(
      icon: Icon(icon),
      onPressed: onPressed,
      tooltip: tooltip,
      color: color ?? Theme.of(context).iconTheme.color ?? AppColors.gray900,
      iconSize: size,
      splashRadius: size, // Keeps touch target reasonable
    );
  }
}
