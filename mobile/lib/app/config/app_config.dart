class AppConfig {
  static late String environment;
  static late String apiBaseUrl;
  static const String apiVersion = '/api/v1';
  static const int connectTimeout = 15000;
  static const int receiveTimeout = 15000;
  
  static bool get isDebugMode => environment == 'development';

  static void init(String env) {
    environment = env;
    switch (env) {
      case 'production':
        apiBaseUrl = 'https://api.floodguardian.id'; // Replace with real prod URL
        break;
      case 'staging':
        apiBaseUrl = 'https://staging-api.floodguardian.id';
        break;
      case 'development':
      default:
        apiBaseUrl = 'http://10.0.2.2:8000'; // Default Android emulator local host
        break;
    }
  }
}
