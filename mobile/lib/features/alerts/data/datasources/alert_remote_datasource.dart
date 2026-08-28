import '../../../../core/network/api_client.dart';
import '../../../../core/network/models/api_response.dart';
import 'package:dio/dio.dart';
import '../../../../core/errors/network_exceptions.dart';
import '../models/alert_model.dart';

abstract class AlertRemoteDataSource {
  Future<PaginatedResponse<AlertModel>> getAlerts({
    int page = 1,
    int pageSize = 10,
    required String areaId,
    bool? isActive,
  });

  Future<SuccessResponse<AlertModel>> getActiveAlert(String areaId);
  Future<SuccessResponse<AlertModel>> getAlertById(String id);
}

class AlertRemoteDataSourceImpl implements AlertRemoteDataSource {
  final ApiClient apiClient;

  AlertRemoteDataSourceImpl({required this.apiClient});

  @override
  Future<PaginatedResponse<AlertModel>> getAlerts({
    int page = 1,
    int pageSize = 10,
    required String areaId,
    bool? isActive,
  }) async {
    try {
      final queryParams = <String, dynamic>{
        'page': page,
        'page_size': pageSize,
      };
      if (isActive != null) queryParams['is_active'] = isActive;

      final response = await apiClient.get(
        '/areas/$areaId/alerts',
        queryParameters: queryParams,
      );
      
      return PaginatedResponse.fromJson(
        response.data,
        (json) => AlertModel.fromJson(json as Map<String, dynamic>),
      );
    } on DioException catch (e) {
      throw mapDioExceptionToNetworkException(e);
    }
  }

  @override
  Future<SuccessResponse<AlertModel>> getActiveAlert(String areaId) async {
    try {
      final response = await apiClient.get('/areas/$areaId/alerts/active');
      
      return SuccessResponse.fromJson(
        response.data,
        (json) => AlertModel.fromJson(json as Map<String, dynamic>),
      );
    } on DioException catch (e) {
      throw mapDioExceptionToNetworkException(e);
    }
  }

  @override
  Future<SuccessResponse<AlertModel>> getAlertById(String id) async {
    try {
      final response = await apiClient.get('/alerts/$id');
      
      return SuccessResponse.fromJson(
        response.data,
        (json) => AlertModel.fromJson(json as Map<String, dynamic>),
      );
    } on DioException catch (e) {
      throw mapDioExceptionToNetworkException(e);
    }
  }
}
