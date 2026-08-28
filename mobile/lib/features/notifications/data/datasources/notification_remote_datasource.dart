import '../../../../core/network/api_client.dart';
import '../../../../core/network/models/api_response.dart';
import 'package:dio/dio.dart';
import '../../../../core/errors/network_exceptions.dart';

abstract class NotificationRemoteDataSource {
  Future<PaginatedResponse<Map<String, dynamic>>> getNotifications(
    String areaId, {
    int page = 1,
    int pageSize = 20,
    String? severity,
    String? status,
  });

  Future<SuccessResponse<Map<String, dynamic>>> getNotificationById(String notificationId);
}

class NotificationRemoteDataSourceImpl implements NotificationRemoteDataSource {
  final ApiClient apiClient;

  NotificationRemoteDataSourceImpl({required this.apiClient});

  @override
  Future<PaginatedResponse<Map<String, dynamic>>> getNotifications(
    String areaId, {
    int page = 1,
    int pageSize = 20,
    String? severity,
    String? status,
  }) async {
    try {
      final queryParams = <String, dynamic>{
        'page': page,
        'page_size': pageSize,
      };
      if (severity != null) queryParams['severity'] = severity;
      if (status != null) queryParams['status'] = status;

      final response = await apiClient.get(
        '/$areaId/notifications',
        queryParameters: queryParams,
      );
      
      return PaginatedResponse.fromJson(
        response.data,
        (json) => json as Map<String, dynamic>,
      );
    } on DioException catch (e) {
      throw mapDioExceptionToNetworkException(e);
    }
  }

  @override
  Future<SuccessResponse<Map<String, dynamic>>> getNotificationById(String notificationId) async {
    try {
      final response = await apiClient.get('/notifications/$notificationId');
      
      return SuccessResponse.fromJson(
        response.data,
        (json) => json as Map<String, dynamic>,
      );
    } on DioException catch (e) {
      throw mapDioExceptionToNetworkException(e);
    }
  }
}
