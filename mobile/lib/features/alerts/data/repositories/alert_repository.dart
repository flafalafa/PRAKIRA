import '../../../../core/errors/failure.dart';
import '../../../../core/network/models/api_response.dart';
import '../datasources/alert_remote_datasource.dart';
import '../models/alert_model.dart';
import '../../../../core/errors/network_exceptions.dart';

abstract class AlertRepository {
  Future<AlertModel?> getActiveAlert(String areaId);
  Future<PaginatedResponse<AlertModel>> getAlerts({
    int page = 1,
    int pageSize = 10,
    required String areaId,
    bool? isActive,
  });
  Future<AlertModel> getAlertById(String id);
}

class AlertRepositoryImpl implements AlertRepository {
  final AlertRemoteDataSource remoteDataSource;

  AlertRepositoryImpl({required this.remoteDataSource});

  @override
  Future<AlertModel?> getActiveAlert(String areaId) async {
    try {
      final response = await remoteDataSource.getActiveAlert(areaId);
      return response.data;
    } on NetworkException catch (e) {
      if (e.errorCode == 'NOT_FOUND') {
        // Active alert might return 404 if there are no active alerts
        return null;
      }
      throw mapExceptionToFailure(e);
    } catch (e) {
      throw mapExceptionToFailure(Exception(e.toString()));
    }
  }

  @override
  Future<PaginatedResponse<AlertModel>> getAlerts({
    int page = 1,
    int pageSize = 10,
    required String areaId,
    bool? isActive,
  }) async {
    try {
      return await remoteDataSource.getAlerts(
        page: page,
        pageSize: pageSize,
        areaId: areaId,
        isActive: isActive,
      );
    } on NetworkException catch (e) {
      throw mapExceptionToFailure(e);
    } catch (e) {
      throw mapExceptionToFailure(Exception(e.toString()));
    }
  }

  @override
  Future<AlertModel> getAlertById(String id) async {
    try {
      final response = await remoteDataSource.getAlertById(id);
      return response.data;
    } on NetworkException catch (e) {
      throw mapExceptionToFailure(e);
    } catch (e) {
      throw mapExceptionToFailure(Exception(e.toString()));
    }
  }
}
