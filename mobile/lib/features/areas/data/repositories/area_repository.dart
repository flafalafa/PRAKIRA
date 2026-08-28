import '../../../../core/errors/failure.dart';
import '../../../../core/errors/network_exceptions.dart';
import '../../../../core/network/models/api_response.dart';
import '../datasources/area_remote_datasource.dart';
import '../models/area_model.dart';
import '../storage/area_selection_storage.dart';

abstract class AreaRepository {
  Future<PaginatedResponse<AreaModel>> getAreas({int page = 1, int pageSize = 10});
  Future<SuccessResponse<AreaModel>> getAreaById(String id);
  Future<void> saveSelectedAreaId(String areaId);
  Future<String?> getSelectedAreaId();
  Future<void> clearSelectedAreaId();
}

class AreaRepositoryImpl implements AreaRepository {
  final AreaRemoteDataSource remoteDataSource;
  final AreaSelectionStorage selectionStorage;

  AreaRepositoryImpl({
    required this.remoteDataSource,
    required this.selectionStorage,
  });

  @override
  Future<PaginatedResponse<AreaModel>> getAreas({int page = 1, int pageSize = 10}) async {
    try {
      return await remoteDataSource.getAreas(page: page, pageSize: pageSize);
    } on NetworkException catch (e) {
      throw mapExceptionToFailure(e);
    } catch (e) {
      throw UnknownFailure(e.toString(), 'UNKNOWN_ERROR');
    }
  }

  @override
  Future<SuccessResponse<AreaModel>> getAreaById(String id) async {
    try {
      return await remoteDataSource.getAreaById(id);
    } on NetworkException catch (e) {
      throw mapExceptionToFailure(e);
    } catch (e) {
      throw UnknownFailure(e.toString(), 'UNKNOWN_ERROR');
    }
  }

  @override
  Future<void> saveSelectedAreaId(String areaId) async {
    try {
      await selectionStorage.saveSelectedAreaId(areaId);
    } catch (e) {
      throw CacheFailure('Failed to save area selection: ${e.toString()}', 'CACHE_ERROR');
    }
  }

  @override
  Future<String?> getSelectedAreaId() async {
    try {
      return await selectionStorage.getSelectedAreaId();
    } catch (e) {
      throw CacheFailure('Failed to retrieve area selection: ${e.toString()}', 'CACHE_ERROR');
    }
  }

  @override
  Future<void> clearSelectedAreaId() async {
    try {
      await selectionStorage.clearSelectedAreaId();
    } catch (e) {
      throw CacheFailure('Failed to clear area selection: ${e.toString()}', 'CACHE_ERROR');
    }
  }
}
