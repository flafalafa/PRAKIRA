import 'package:flutter/material.dart';
import 'app_colors.dart';
import 'app_typography.dart';
import 'app_component_theme.dart';

class AppTheme {
  AppTheme._();

  static final ThemeData lightTheme = ThemeData(
    useMaterial3: true,
    brightness: Brightness.light,
    colorScheme: const ColorScheme.light(
      primary: AppColors.primaryLight,
      onPrimary: AppColors.onPrimaryLight,
      secondary: AppColors.secondaryLight,
      onSecondary: AppColors.onSecondaryLight,
      surface: AppColors.surfaceLight,
      onSurface: AppColors.onSurfaceLight,
      error: AppColors.errorLight,
      onError: AppColors.onErrorLight,
    ),
    scaffoldBackgroundColor: AppColors.backgroundLight,
    textTheme: AppTypography.getTextTheme(
      textColor: AppColors.gray900,
      bodyColor: AppColors.gray800,
    ),
    appBarTheme: AppBarTheme(
      elevation: 0,
      centerTitle: true,
      backgroundColor: AppColors.surfaceLight,
      foregroundColor: AppColors.gray900,
      titleTextStyle: AppTypography.title.copyWith(color: AppColors.gray900),
      iconTheme: const IconThemeData(color: AppColors.gray900),
    ),
    elevatedButtonTheme: AppComponentTheme.getElevatedButtonTheme(AppColors.primaryLight, AppColors.onPrimaryLight),
    outlinedButtonTheme: AppComponentTheme.getOutlinedButtonTheme(AppColors.primaryLight),
    textButtonTheme: AppComponentTheme.getTextButtonTheme(AppColors.primaryLight),
    inputDecorationTheme: AppComponentTheme.getInputDecorationTheme(AppColors.primaryLight, AppColors.errorLight, AppColors.borderLight),
    cardTheme: AppComponentTheme.getCardTheme(AppColors.surfaceLight),
    dividerTheme: const DividerThemeData(color: AppColors.borderLight, thickness: 1, space: 1),
  );

  static final ThemeData darkTheme = ThemeData(
    useMaterial3: true,
    brightness: Brightness.dark,
    colorScheme: const ColorScheme.dark(
      primary: AppColors.primaryDark,
      onPrimary: AppColors.onPrimaryDark,
      secondary: AppColors.secondaryDark,
      onSecondary: AppColors.onSecondaryDark,
      surface: AppColors.surfaceDark,
      onSurface: AppColors.onSurfaceDark,
      error: AppColors.errorDark,
      onError: AppColors.onErrorDark,
    ),
    scaffoldBackgroundColor: AppColors.backgroundDark,
    textTheme: AppTypography.getTextTheme(
      textColor: AppColors.gray100,
      bodyColor: AppColors.gray300,
    ),
    appBarTheme: AppBarTheme(
      elevation: 0,
      centerTitle: true,
      backgroundColor: AppColors.surfaceDark,
      foregroundColor: AppColors.gray100,
      titleTextStyle: AppTypography.title.copyWith(color: AppColors.gray100),
      iconTheme: const IconThemeData(color: AppColors.gray100),
    ),
    elevatedButtonTheme: AppComponentTheme.getElevatedButtonTheme(AppColors.primaryDark, AppColors.onPrimaryDark),
    outlinedButtonTheme: AppComponentTheme.getOutlinedButtonTheme(AppColors.primaryDark),
    textButtonTheme: AppComponentTheme.getTextButtonTheme(AppColors.primaryDark),
    inputDecorationTheme: AppComponentTheme.getInputDecorationTheme(AppColors.primaryDark, AppColors.errorDark, AppColors.borderDark),
    cardTheme: AppComponentTheme.getCardTheme(AppColors.surfaceDark),
    dividerTheme: const DividerThemeData(color: AppColors.borderDark, thickness: 1, space: 1),
  );
}
