import 'package:flutter_test/flutter_test.dart';
import 'package:flood_guardian/features/areas/data/models/area_model.dart';

void main() {
  group('AreaModel', () {
    test('should parse correctly from valid JSON', () {
      final json = {
        "area_id": "area-123",
        "area_name": "Test Area",
        "area_code": "TA-01",
        "status": "active",
        "area_type": "river",
        "location": {
          "latitude": -6.2,
          "longitude": 106.8,
          "timezone": "Asia/Jakarta",
          "country": "Indonesia"
        },
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
      };

      final result = AreaModel.fromJson(json);

      expect(result.areaId, "area-123");
      expect(result.status, AreaStatus.active);
      expect(result.location?.latitude, -6.2);
    });

    test('should fallback to unknown status on unrecognized status string', () {
      final json = {
        "area_id": "area-123",
        "area_name": "Test Area",
        "area_code": "TA-01",
        "status": "some_new_status_from_backend",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
      };

      final result = AreaModel.fromJson(json);

      expect(result.status, AreaStatus.unknown);
    });
  });
}
