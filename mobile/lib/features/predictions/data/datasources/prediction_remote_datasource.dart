import '../../../../core/network/api_client.dart';
import '../../../../core/network/models/api_response.dart';
import 'package:dio/dio.dart';
import '../../../../core/errors/network_exceptions.dart';
import '../models/prediction_model.dart';

abstract class PredictionRemoteDataSource {
  Future<PaginatedResponse<PredictionModel>> getPredictions({
    int page = 1,
    int pageSize = 10,
    required String areaId,
  });

  Future<SuccessResponse<PredictionModel>> getCurrentPrediction(String areaId);
}

class PredictionRemoteDataSourceImpl implements PredictionRemoteDataSource {
  final ApiClient apiClient;

  PredictionRemoteDataSourceImpl({required this.apiClient});

  @override
  Future<PaginatedResponse<PredictionModel>> getPredictions({
    int page = 1,
    int pageSize = 10,
    required String areaId,
  }) async {
    try {
      final queryParams = <String, dynamic>{
        'page': page,
        'page_size': pageSize,
      };

      final response = await apiClient.get(
        '/areas/$areaId/predictions',
        queryParameters: queryParams,
      );
      
      return PaginatedResponse.fromJson(
        response.data,
        (json) => PredictionModel.fromJson(json as Map<String, dynamic>),
      );
    } on DioException catch (e) {
      throw mapDioExceptionToNetworkException(e);
    }
  }

  @override
  Future<SuccessResponse<PredictionModel>> getCurrentPrediction(String areaId) async {
    try {
      final response = await apiClient.get('/areas/$areaId/prediction');
      
      return SuccessResponse.fromJson(
        response.data,
        (json) => PredictionModel.fromJson(json as Map<String, dynamic>),
      );
    } on DioException catch (e) {
      throw mapDioExceptionToNetworkException(e);
    }
  }
}
