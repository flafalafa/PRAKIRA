import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flood_guardian/app/theme/app_theme.dart';
import 'package:flood_guardian/app/theme/app_colors.dart';

void main() {
  group('AppTheme', () {
    test('lightTheme initializes correctly', () {
      final theme = AppTheme.lightTheme;
      
      expect(theme.brightness, Brightness.light);
      expect(theme.colorScheme.primary, AppColors.primaryLight);
      expect(theme.scaffoldBackgroundColor, AppColors.backgroundLight);
    });

    test('darkTheme initializes correctly', () {
      final theme = AppTheme.darkTheme;
      
      expect(theme.brightness, Brightness.dark);
      expect(theme.colorScheme.primary, AppColors.primaryDark);
      expect(theme.scaffoldBackgroundColor, AppColors.backgroundDark);
    });
  });
}
