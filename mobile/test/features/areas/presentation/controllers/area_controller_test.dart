import 'package:flutter_test/flutter_test.dart';
import 'package:flood_guardian/features/areas/presentation/controllers/area_controller.dart';
import 'package:flood_guardian/features/areas/data/repositories/area_repository.dart';
import 'package:flood_guardian/features/areas/data/models/area_model.dart';
import 'package:flood_guardian/core/network/models/api_response.dart';
import 'package:flood_guardian/core/errors/failure.dart';
import 'package:flood_guardian/core/network/models/api_meta.dart';
import 'package:flood_guardian/core/network/models/pagination_meta.dart';

class MockAreaRepository implements AreaRepository {
  bool shouldThrow = false;
  PaginatedResponse<AreaModel>? paginatedResponse;
  String? storedAreaId;

  @override
  Future<PaginatedResponse<AreaModel>> getAreas({int page = 1, int pageSize = 10}) async {
    if (shouldThrow) throw const ServerFailure('Server error', '500');
    return paginatedResponse!;
  }

  @override
  Future<SuccessResponse<AreaModel>> getAreaById(String id) async => throw UnimplementedError();

  @override
  Future<void> saveSelectedAreaId(String areaId) async {}

  @override
  Future<String?> getSelectedAreaId() async => storedAreaId;

  @override
  Future<void> clearSelectedAreaId() async {}
}

void main() {
  late AreaController controller;
  late MockAreaRepository mockRepository;

  setUp(() {
    mockRepository = MockAreaRepository();
    controller = AreaController(repository: mockRepository);
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

  group('loadAreas', () {
    test('should emit loaded status on success', () async {
      mockRepository.paginatedResponse = PaginatedResponse(
        data: [tAreaModel],
        meta: const ApiMeta(pagination: PaginationMeta(page: 1, pageSize: 20, total: 1, totalPages: 1, hasNext: false, hasPrevious: false)),
        requestId: '123',
        timestamp: DateTime.now(),
        version: 'v1',
      );

      await controller.loadAreas();

      expect(controller.status, AreaStateStatus.loaded);
      expect(controller.areas, [tAreaModel]);
    });

    test('should emit error status on failure', () async {
      mockRepository.shouldThrow = true;

      await controller.loadAreas();

      expect(controller.status, AreaStateStatus.error);
      expect(controller.error, isA<ServerFailure>());
    });
  });
}
