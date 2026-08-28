import 'package:flutter/material.dart';
import 'app_typography.dart';
import 'app_radius.dart';
import 'app_spacing.dart';
import 'app_elevation.dart';

class AppComponentTheme {
  AppComponentTheme._();

  static ElevatedButtonThemeData getElevatedButtonTheme(Color primary, Color onPrimary) {
    return ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        foregroundColor: onPrimary,
        backgroundColor: primary,
        elevation: AppElevation.low,
        minimumSize: const Size.fromHeight(48), // Use standard height
        padding: const EdgeInsets.symmetric(horizontal: AppSpacing.s24),
        shape: const RoundedRectangleBorder(borderRadius: AppRadius.medium),
        textStyle: AppTypography.button,
      ),
    );
  }

  static OutlinedButtonThemeData getOutlinedButtonTheme(Color primary) {
    return OutlinedButtonThemeData(
      style: OutlinedButton.styleFrom(
        foregroundColor: primary,
        minimumSize: const Size.fromHeight(48),
        padding: const EdgeInsets.symmetric(horizontal: AppSpacing.s24),
        shape: const RoundedRectangleBorder(borderRadius: AppRadius.medium),
        side: BorderSide(color: primary, width: 1.5),
        textStyle: AppTypography.button,
      ),
    );
  }

  static TextButtonThemeData getTextButtonTheme(Color primary) {
    return TextButtonThemeData(
      style: TextButton.styleFrom(
        foregroundColor: primary,
        minimumSize: const Size(64, 48),
        padding: const EdgeInsets.symmetric(horizontal: AppSpacing.s16),
        shape: const RoundedRectangleBorder(borderRadius: AppRadius.medium),
        textStyle: AppTypography.button,
      ),
    );
  }

  static InputDecorationTheme getInputDecorationTheme(Color primary, Color error, Color border) {
    return InputDecorationTheme(
      filled: true,
      fillColor: Colors.transparent,
      contentPadding: const EdgeInsets.symmetric(horizontal: AppSpacing.s16, vertical: AppSpacing.s12),
      border: OutlineInputBorder(
        borderRadius: AppRadius.medium,
        borderSide: BorderSide(color: border),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: AppRadius.medium,
        borderSide: BorderSide(color: border),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: AppRadius.medium,
        borderSide: BorderSide(color: primary, width: 2),
      ),
      errorBorder: OutlineInputBorder(
        borderRadius: AppRadius.medium,
        borderSide: BorderSide(color: error, width: 2),
      ),
      focusedErrorBorder: OutlineInputBorder(
        borderRadius: AppRadius.medium,
        borderSide: BorderSide(color: error, width: 2),
      ),
      labelStyle: AppTypography.label.copyWith(color: border), // Or an appropriate color
      errorStyle: AppTypography.error.copyWith(color: error),
    );
  }

  static CardThemeData getCardTheme(Color surface) {
    return CardThemeData(
      color: surface,
      elevation: AppElevation.low,
      shadowColor: Colors.black.withValues(alpha: 0.1),
      shape: const RoundedRectangleBorder(borderRadius: AppRadius.large),
      margin: EdgeInsets.zero,
    );
  }
}
