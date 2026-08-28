import 'package:flutter/material.dart';
import 'theme/app_theme.dart';
import 'router.dart';
import '../core/constants/app_constants.dart';

class FloodGuardianApp extends StatelessWidget {
  const FloodGuardianApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: AppConstants.appName,
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system, // Support dark mode readiness
      initialRoute: AppRouter.splashRoute,
      onGenerateRoute: AppRouter.generateRoute,
      debugShowCheckedModeBanner: false,
    );
  }
}
