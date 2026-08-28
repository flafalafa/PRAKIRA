import 'package:flutter/material.dart';

import 'app/app.dart';
import 'app/config/app_config.dart';
import 'core/logging/app_logger.dart';
import 'core/storage/storage_provider.dart';
import 'core/di/service_locator.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  debugPrint('🚀 STEP 1: Flutter Binding initialized');

  // Initialize centralized logging
  AppLogger.init();

  debugPrint('🚀 STEP 2: Logger initialized');

  // Load environment configuration
  const String env = String.fromEnvironment(
    'ENV',
    defaultValue: 'development',
  );

  AppConfig.init(env);

  debugPrint(
    '🚀 STEP 3: AppConfig initialized: ${AppConfig.environment}',
  );

  // Initialize storage
  debugPrint('⏳ STEP 4: Starting StorageProvider...');

  await StorageProvider.init();

  debugPrint('✅ STEP 4: StorageProvider completed');

  // Initialize dependencies
  debugPrint('⏳ STEP 5: Starting ServiceLocator...');

  await ServiceLocator.instance.init();

  debugPrint('✅ STEP 5: ServiceLocator completed');

  // Bootstrap Flutter application
  debugPrint('🎉 STEP 6: Calling runApp...');

  runApp(const FloodGuardianApp());

  debugPrint('🎉 STEP 7: runApp completed');
}
