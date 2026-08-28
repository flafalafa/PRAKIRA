import 'package:flutter_test/flutter_test.dart';
import 'package:flood_guardian/features/areas/data/repositories/area_repository.dart';
import 'package:flood_guardian/features/areas/data/datasources/area_remote_datasource.dart';
import 'package:flood_guardian/features/areas/data/storage/area_selection_storage.dart';
import 'package:flood_guardian/features/areas/data/models/area_model.dart';
import 'package:flood_guardian/core/network/models/api_response.dart';
import 'package:flood_guardian/core/network/models/api_meta.dart';
import 'package:flood_guardian/core/network/models/pagination_meta.dart';

class MockAreaRemoteDataSource implements AreaRemoteDataSource {
  PaginatedResponse<AreaModel>? paginatedResponse;

  @override
  Future<PaginatedResponse<AreaModel>> getAreas({int page = 1, int pageSize = 10}) async {
    return paginatedResponse!;
  }

  @override
  Future<SuccessResponse<AreaModel>> getAreaById(String id) async => throw UnimplementedError();
}

class MockAreaSelectionStorage implements AreaSelectionStorage {
  String? storedAreaId;

  @override
  Future<void> saveSelectedAreaId(String areaId) async {}

  @override
  Future<String?> getSelectedAreaId() async => storedAreaId;

  @override
  Future<void> clearSelectedAreaId() async {}
}

void main() {
  late AreaRepositoryImpl repository;
  late MockAreaRemoteDataSource mockRemoteDataSource;
  late MockAreaSelectionStorage mockSelectionStorage;

  setUp(() {
    mockRemoteDataSource = MockAreaRemoteDataSource();
    mockSelectionStorage = MockAreaSelectionStorage();
    repository = AreaRepositoryImpl(
      remoteDataSource: mockRemoteDataSource,
      selectionStorage: mockSelectionStorage,
    );
  });

  final tAreaModel = AreaModel(
    areaId: '1',
    areaName: 'Area 1',
    areaCode: 'A1',
    status: AreaStatus.active,
    areaType: 'type',
    createdAt: DateTime.now(),
    updatedAt: DateTime.now(),
  );

  group('getAreas', () {
    test('should return remote data when the call to remote data source is successful', () async {
      mockRemoteDataSource.paginatedResponse = PaginatedResponse(
        data: [tAreaModel],
        meta: const ApiMeta(pagination: PaginationMeta(page: 1, pageSize: 10, total: 1, totalPages: 1, hasNext: false, hasPrevious: false)),
        requestId: '123',
        timestamp: DateTime.now(),
        version: 'v1',
      );

      final result = await repository.getAreas(page: 1, pageSize: 10);

      expect(result.data, equals([tAreaModel]));
    });
  });

  group('getSelectedAreaId', () {
    test('should return area id from storage', () async {
      mockSelectionStorage.storedAreaId = '1';

      final result = await repository.getSelectedAreaId();

      expect(result, '1');
    });
  });
}
