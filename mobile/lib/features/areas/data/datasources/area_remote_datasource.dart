import '../../../../core/network/api_client.dart';
import '../../../../core/network/models/api_response.dart';
import 'package:dio/dio.dart';
import '../../../../core/errors/network_exceptions.dart';
import '../models/area_model.dart';

abstract class AreaRemoteDataSource {
  Future<PaginatedResponse<AreaModel>> getAreas({
    int page = 1,
    int pageSize = 10,
  });

  Future<SuccessResponse<AreaModel>> getAreaById(String id);
}

class AreaRemoteDataSourceImpl implements AreaRemoteDataSource {
  final ApiClient apiClient;

  AreaRemoteDataSourceImpl({required this.apiClient});

  @override
  Future<PaginatedResponse<AreaModel>> getAreas({
    int page = 1,
    int pageSize = 10,
  }) async {
    try {
      final response = await apiClient.get(
        '/areas',
        queryParameters: {
          'page': page,
          'page_size': pageSize,
        },
      );
      
      return PaginatedResponse.fromJson(
        response.data,
        (json) => AreaModel.fromJson(json as Map<String, dynamic>),
      );
    } on DioException catch (e) {
      throw mapDioExceptionToNetworkException(e);
    }
  }

  @override
  Future<SuccessResponse<AreaModel>> getAreaById(String id) async {
    try {
      final response = await apiClient.get('/areas/$id');
      
      return SuccessResponse.fromJson(
        response.data,
        (json) => AreaModel.fromJson(json as Map<String, dynamic>),
      );
    } on DioException catch (e) {
      throw mapDioExceptionToNetworkException(e);
    }
  }
}
