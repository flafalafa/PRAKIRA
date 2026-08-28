import 'dart:developer' as developer;
import '../../app/config/app_config.dart';

enum LogLevel { debug, info, warning, error }

class AppLogger {
  static void init() {
    // Basic setup if any required
  }

  static void debug(String message) {
    if (AppConfig.isDebugMode) {
      _log(LogLevel.debug, message);
    }
  }

  static void info(String message) {
    _log(LogLevel.info, message);
  }

  static void warning(String message, [dynamic error, StackTrace? stackTrace]) {
    _log(LogLevel.warning, message, error, stackTrace);
  }

  static void error(String message, [dynamic error, StackTrace? stackTrace]) {
    _log(LogLevel.error, message, error, stackTrace);
  }

  static void _log(LogLevel level, String message, [dynamic error, StackTrace? stackTrace]) {
    // In production, this can be directed to Crashlytics / Sentry / Datadog.
    // For now, write to Dart developer console.
    developer.log(
      message,
      name: level.toString().toUpperCase().split('.').last,
      error: error,
      stackTrace: stackTrace,
    );
  }
}
