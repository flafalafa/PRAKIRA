import 'package:flutter/material.dart';

class AppTypography {
  AppTypography._();

  // Font weights
  static const FontWeight _regular = FontWeight.w400;
  static const FontWeight _medium = FontWeight.w500;
  static const FontWeight _semiBold = FontWeight.w600;
  static const FontWeight _bold = FontWeight.w700;

  // ---------------------------------------------------------------------------
  // TEXT STYLES (Baseline)
  // ---------------------------------------------------------------------------
  
  static const TextStyle display = TextStyle(
    fontSize: 48,
    fontWeight: _bold,
    letterSpacing: -1.0,
    height: 1.2,
  );

  static const TextStyle headline = TextStyle(
    fontSize: 32,
    fontWeight: _semiBold,
    letterSpacing: -0.5,
    height: 1.25,
  );

  static const TextStyle title = TextStyle(
    fontSize: 20,
    fontWeight: _semiBold,
    letterSpacing: 0.15,
    height: 1.4,
  );

  static const TextStyle body = TextStyle(
    fontSize: 16,
    fontWeight: _regular,
    letterSpacing: 0.5,
    height: 1.5,
  );

  static const TextStyle bodyMedium = TextStyle(
    fontSize: 16,
    fontWeight: _medium,
    letterSpacing: 0.25,
    height: 1.5,
  );

  static const TextStyle label = TextStyle(
    fontSize: 14,
    fontWeight: _medium,
    letterSpacing: 0.1,
    height: 1.4,
  );

  static const TextStyle caption = TextStyle(
    fontSize: 12,
    fontWeight: _regular,
    letterSpacing: 0.4,
    height: 1.33,
  );

  static const TextStyle button = TextStyle(
    fontSize: 14,
    fontWeight: _semiBold,
    letterSpacing: 0.1,
    height: 1.4,
  );

  static const TextStyle navigation = TextStyle(
    fontSize: 10,
    fontWeight: _medium,
    letterSpacing: 0.5,
    height: 1.2,
  );

  // ---------------------------------------------------------------------------
  // SPECIALIZED TEXT STYLES
  // ---------------------------------------------------------------------------

  static const TextStyle error = TextStyle(
    fontSize: 14,
    fontWeight: _medium,
    letterSpacing: 0.1,
    height: 1.4,
  );

  static const TextStyle emergency = TextStyle(
    fontSize: 24,
    fontWeight: _bold,
    letterSpacing: 0,
    height: 1.3,
  );

  // ---------------------------------------------------------------------------
  // TEXT THEME GENERATORS
  // ---------------------------------------------------------------------------
  
  static TextTheme getTextTheme({required Color textColor, required Color bodyColor}) {
    return TextTheme(
      displayLarge: display.copyWith(color: textColor),
      displayMedium: headline.copyWith(color: textColor),
      displaySmall: headline.copyWith(fontSize: 28, color: textColor),
      
      headlineLarge: headline.copyWith(color: textColor),
      headlineMedium: title.copyWith(fontSize: 24, color: textColor),
      headlineSmall: title.copyWith(color: textColor),
      
      titleLarge: title.copyWith(color: textColor),
      titleMedium: bodyMedium.copyWith(color: textColor),
      titleSmall: label.copyWith(color: textColor),
      
      bodyLarge: body.copyWith(color: bodyColor),
      bodyMedium: body.copyWith(fontSize: 14, color: bodyColor),
      bodySmall: caption.copyWith(color: bodyColor),
      
      labelLarge: button.copyWith(color: textColor),
      labelMedium: label.copyWith(fontSize: 12, color: textColor),
      labelSmall: navigation.copyWith(color: textColor),
    );
  }
}
