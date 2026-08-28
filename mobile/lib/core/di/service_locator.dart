import 'package:flutter/foundation.dart';

import '../storage/secure_token_storage.dart';
import '../storage/session_manager.dart';
import '../network/api_client.dart';

import '../../features/auth/data/datasources/auth_remote_datasource.dart';
import '../../features/auth/data/repositories/auth_repository.dart';
import '../../features/auth/presentation/controllers/auth_controller.dart';

import '../../features/areas/data/storage/area_selection_storage.dart';
import '../../features/areas/data/datasources/area_remote_datasource.dart';
import '../../features/areas/data/repositories/area_repository.dart';
import '../../features/areas/presentation/controllers/area_controller.dart';

import '../../features/predictions/data/datasources/prediction_remote_datasource.dart';
import '../../features/predictions/data/repositories/prediction_repository.dart';

import '../../features/alerts/data/datasources/alert_remote_datasource.dart';
import '../../features/alerts/data/repositories/alert_repository.dart';

import '../../features/dashboard/presentation/controllers/dashboard_controller.dart';

import '../../features/notifications/domain/services/push_notification_service.dart';
import '../../features/notifications/data/services/local_push_notification_service.dart';
import '../../features/notifications/data/datasources/notification_remote_datasource.dart';
import '../../features/notifications/data/repositories/notification_repository.dart';

class ServiceLocator {
  static final ServiceLocator _instance = ServiceLocator._internal();

  static ServiceLocator get instance => _instance;

  ServiceLocator._internal();

  late final SecureTokenStorage secureTokenStorage;
  late final SessionManager sessionManager;
  late final ApiClient apiClient;

  late final AuthRemoteDataSource authRemoteDataSource;
  late final AuthRepository authRepository;
  late final AuthController authController;

  late final AreaSelectionStorage areaSelectionStorage;
  late final AreaRemoteDataSource areaRemoteDataSource;
  late final AreaRepository areaRepository;
  late final AreaController areaController;

  late final PredictionRemoteDataSource predictionRemoteDataSource;
  late final PredictionRepository predictionRepository;

  late final AlertRemoteDataSource alertRemoteDataSource;
  late final AlertRepository alertRepository;

  late final DashboardController dashboardController;

  late final PushNotificationService pushNotificationService;
  late final NotificationRemoteDataSource notificationRemoteDataSource;
  late final NotificationRepository notificationRepository;

  Future<void> init() async {
    debugPrint('🔵 DI 1: Starting ServiceLocator');

    // ==========================================
    // 1. STORAGE
    // ==========================================

    secureTokenStorage = FlutterSecureTokenStorageImpl();

    debugPrint('🔵 DI 2: SecureTokenStorage created');

    sessionManager = SessionManager(
      storage: secureTokenStorage,
    );

    debugPrint('🔵 DI 3: SessionManager created');

    await sessionManager.initialize();

    debugPrint('✅ DI 4: SessionManager initialized');

    // ==========================================
    // 2. NETWORK
    // ==========================================

    apiClient = DioApiClient(
      tokenProvider: sessionManager,
    );

    debugPrint('✅ DI 5: ApiClient created');

    // ==========================================
    // 3. DATA SOURCES
    // ==========================================

    authRemoteDataSource = MockAuthRemoteDataSourceImpl();

    areaRemoteDataSource = AreaRemoteDataSourceImpl(
      apiClient: apiClient,
    );

    predictionRemoteDataSource = PredictionRemoteDataSourceImpl(
      apiClient: apiClient,
    );

    alertRemoteDataSource = AlertRemoteDataSourceImpl(
      apiClient: apiClient,
    );

    notificationRemoteDataSource = NotificationRemoteDataSourceImpl(
      apiClient: apiClient,
    );

    debugPrint('✅ DI 6: DataSources created');

    // ==========================================
    // 4. REPOSITORIES
    // ==========================================

    authRepository = AuthRepositoryImpl(
      remoteDataSource: authRemoteDataSource,
      sessionManager: sessionManager,
    );

    debugPrint('🔵 DI 7: AuthRepository created');

    areaSelectionStorage =
        SharedPrefsAreaSelectionStorageImpl();

    debugPrint('🔵 DI 8: AreaSelectionStorage created');

    areaRepository = AreaRepositoryImpl(
      remoteDataSource: areaRemoteDataSource,
      selectionStorage: areaSelectionStorage,
    );

    predictionRepository = PredictionRepositoryImpl(
      remoteDataSource: predictionRemoteDataSource,
    );

    alertRepository = AlertRepositoryImpl(
      remoteDataSource: alertRemoteDataSource,
    );

    notificationRepository = NotificationRepository(
      remoteDataSource: notificationRemoteDataSource,
    );

    debugPrint('✅ DI 9: Repositories created');

    // ==========================================
    // 5. PUSH NOTIFICATION
    // ==========================================

    pushNotificationService =
        LocalPushNotificationService();

    debugPrint(
      '🔵 DI 10: Starting PushNotificationService',
    );

    await pushNotificationService.initialize();

    debugPrint(
      '✅ DI 11: PushNotificationService initialized',
    );

    // ==========================================
    // 6. CONTROLLERS
    // ==========================================

    authController = AuthController(
      repository: authRepository,
      sessionManager: sessionManager,
    );

    debugPrint('✅ DI 12: AuthController created');

    areaController = AreaController(
      repository: areaRepository,
    );

    debugPrint('✅ DI 13: AreaController created');

    dashboardController = DashboardController(
      predictionRepository: predictionRepository,
      alertRepository: alertRepository,
    );

    debugPrint('🎉 DI 14: DashboardController created');

    debugPrint(
      '🎉 DI COMPLETED SUCCESSFULLY',
    );
  }
}
