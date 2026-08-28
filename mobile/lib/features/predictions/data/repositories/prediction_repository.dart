import '../../../../core/errors/failure.dart';
import '../../../../core/network/models/api_response.dart';
import '../datasources/prediction_remote_datasource.dart';
import '../models/prediction_model.dart';
import '../../../../core/errors/network_exceptions.dart';

abstract class PredictionRepository {
  Future<PredictionModel?> getCurrentPrediction(String areaId);
  Future<PaginatedResponse<PredictionModel>> getPredictions({
    int page = 1,
    int pageSize = 10,
    required String areaId,
  });
}

class PredictionRepositoryImpl implements PredictionRepository {
  final PredictionRemoteDataSource remoteDataSource;

  PredictionRepositoryImpl({required this.remoteDataSource});

  @override
  Future<PredictionModel?> getCurrentPrediction(String areaId) async {
    try {
      final response = await remoteDataSource.getCurrentPrediction(areaId);
      return response.data;
    } on NetworkException catch (e) {
      if (e.errorCode == 'NOT_FOUND') {
        return null; // Legitimate no-data state
      }
      throw mapExceptionToFailure(e);
    } catch (e) {
      throw mapExceptionToFailure(Exception(e.toString()));
    }
  }

  @override
  Future<PaginatedResponse<PredictionModel>> getPredictions({
    int page = 1,
    int pageSize = 10,
    required String areaId,
  }) async {
    try {
      return await remoteDataSource.getPredictions(
        page: page,
        pageSize: pageSize,
        areaId: areaId,
      );
    } on NetworkException catch (e) {
      throw mapExceptionToFailure(e);
    } catch (e) {
      throw mapExceptionToFailure(Exception(e.toString()));
    }
  }
}
