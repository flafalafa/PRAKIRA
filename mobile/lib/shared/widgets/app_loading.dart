import 'package:flutter/material.dart';
import '../../app/theme/app_colors.dart';

class AppLoading extends StatelessWidget {
  final bool isCentered;

  const AppLoading({
    super.key,
    this.isCentered = true,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    final loader = CircularProgressIndicator(
      color: isDark ? AppColors.primaryDark : AppColors.primaryLight,
    );

    if (isCentered) {
      return Center(child: loader);
    }
    
    return loader;
  }
}
