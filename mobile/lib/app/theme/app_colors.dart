import 'package:flutter/material.dart';

class AppColors {
  AppColors._();

  // ---------------------------------------------------------------------------
  // PRIMITIVE COLORS
  // ---------------------------------------------------------------------------

  // Blues (Water / Primary Brand)
  static const Color blue50 = Color(0xFFE3F2FD);
  static const Color blue100 = Color(0xFFBBDEFB);
  static const Color blue300 = Color(0xFF64B5F6);
  static const Color blue500 = Color(0xFF2196F3);
  static const Color blue700 = Color(0xFF1976D2);
  static const Color blue900 = Color(0xFF0D47A1);

  // Grays (Neutrals)
  static const Color gray50 = Color(0xFFFAFAFA);
  static const Color gray100 = Color(0xFFF5F5F5);
  static const Color gray200 = Color(0xFFEEEEEE);
  static const Color gray300 = Color(0xFFE0E0E0);
  static const Color gray400 = Color(0xFFBDBDBD);
  static const Color gray500 = Color(0xFF9E9E9E);
  static const Color gray600 = Color(0xFF757575);
  static const Color gray700 = Color(0xFF616161);
  static const Color gray800 = Color(0xFF424242);
  static const Color gray900 = Color(0xFF212121);

  // Greens (Safe / Success)
  static const Color green50 = Color(0xFFE8F5E9);
  static const Color green500 = Color(0xFF4CAF50);
  static const Color green700 = Color(0xFF388E3C);
  static const Color green900 = Color(0xFF1B5E20);

  // Yellows (Watch / Info)
  static const Color yellow50 = Color(0xFFFFFDE7);
  static const Color yellow500 = Color(0xFFFFEB3B);
  static const Color yellow700 = Color(0xFFFBC02D);
  static const Color yellow900 = Color(0xFFF57F17);

  // Oranges (Warning)
  static const Color orange50 = Color(0xFFFFF3E0);
  static const Color orange500 = Color(0xFFFF9800);
  static const Color orange700 = Color(0xFFF57C00);
  static const Color orange900 = Color(0xFFE65100);

  // Reds (Danger / Emergency / Error)
  static const Color red50 = Color(0xFFFFEBEE);
  static const Color red300 = Color(0xFFE57373);
  static const Color red500 = Color(0xFFF44336);
  static const Color red700 = Color(0xFFD32F2F);
  static const Color red900 = Color(0xFFB71C1C);

  // Purples (Emergency escalation)
  static const Color purple50 = Color(0xFFF3E5F5);
  static const Color purple500 = Color(0xFF9C27B0);
  static const Color purple700 = Color(0xFF7B1FA2);
  static const Color purple900 = Color(0xFF4A148C);

  // Base
  static const Color white = Color(0xFFFFFFFF);
  static const Color black = Color(0xFF000000);

  // ---------------------------------------------------------------------------
  // SEMANTIC COLORS (LIGHT MODE)
  // ---------------------------------------------------------------------------
  static const Color primaryLight = blue700;
  static const Color onPrimaryLight = white;
  static const Color secondaryLight = gray800;
  static const Color onSecondaryLight = white;
  static const Color backgroundLight = gray50;
  static const Color onBackgroundLight = gray900;
  static const Color surfaceLight = white;
  static const Color onSurfaceLight = gray900;
  static const Color errorLight = red700;
  static const Color onErrorLight = white;
  static const Color borderLight = gray300;
  static const Color disabledLight = gray400;

  // ---------------------------------------------------------------------------
  // SEMANTIC COLORS (DARK MODE)
  // ---------------------------------------------------------------------------
  static const Color primaryDark = blue300;
  static const Color onPrimaryDark = gray900;
  static const Color secondaryDark = gray300;
  static const Color onSecondaryDark = gray900;
  static const Color backgroundDark = Color(0xFF121212);
  static const Color onBackgroundDark = gray100;
  static const Color surfaceDark = Color(0xFF1E1E1E);
  static const Color onSurfaceDark = gray100;
  static const Color errorDark = red300;
  static const Color onErrorDark = gray900;
  static const Color borderDark = gray800;
  static const Color disabledDark = gray700;

  // ---------------------------------------------------------------------------
  // RISK & STATUS COLORS (Applies to both modes generally, with slight tweaks)
  // ---------------------------------------------------------------------------
  
  // SAFE (Normal conditions)
  static const Color safe = green500;
  static const Color onSafe = white;
  static const Color safeBgLight = green50;
  static const Color safeBgDark = Color(0xFF112912);

  // WATCH (Be aware)
  static const Color watch = yellow700;
  static const Color onWatch = black;
  static const Color watchBgLight = yellow50;
  static const Color watchBgDark = Color(0xFF332D06);

  // WARNING (Action may be required)
  static const Color warning = orange700;
  static const Color onWarning = white;
  static const Color warningBgLight = orange50;
  static const Color warningBgDark = Color(0xFF381F04);

  // DANGER (Immediate threat)
  static const Color danger = red700;
  static const Color onDanger = white;
  static const Color dangerBgLight = red50;
  static const Color dangerBgDark = Color(0xFF360C0C);

  // EMERGENCY (Critical, highest severity)
  static const Color emergency = purple700;
  static const Color onEmergency = white;
  static const Color emergencyBgLight = purple50;
  static const Color emergencyBgDark = Color(0xFF230730);

  // General Status
  static const Color success = safe;
  static const Color info = blue500;
}
