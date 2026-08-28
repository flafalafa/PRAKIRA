import 'package:flutter_test/flutter_test.dart';
import 'package:flood_guardian/core/network/models/api_response.dart';

void main() {
  group('SuccessResponse', () {
    test('fromJson parses correctly', () {
      final json = {
        "data": {"id": 1, "name": "Test"},
        "meta": {
          "source": "cache",
          "last_updated": "2026-08-19T00:00:00Z"
        },
        "request_id": "req-123",
        "timestamp": "2026-08-19T00:00:00Z",
        "version": "v1"
      };

      final response = SuccessResponse<Map<String, dynamic>>.fromJson(
        json,
        (data) => data as Map<String, dynamic>,
      );

      expect(response.data['id'], 1);
      expect(response.meta.source, 'cache');
      expect(response.requestId, 'req-123');
      expect(response.version, 'v1');
    });
  });

  group('PaginatedResponse', () {
    test('fromJson parses correctly', () {
      final json = {
        "data": [
          {"id": 1},
          {"id": 2}
        ],
        "meta": {
          "pagination": {
            "page": 1,
            "page_size": 10,
            "total": 20,
            "total_pages": 2,
            "has_next": true,
            "has_previous": false
          }
        },
        "request_id": "req-456",
        "timestamp": "2026-08-19T00:00:00Z",
        "version": "v1"
      };

      final response = PaginatedResponse<Map<String, dynamic>>.fromJson(
        json,
        (data) => data as Map<String, dynamic>,
      );

      expect(response.data.length, 2);
      expect(response.meta.pagination?.total, 20);
      expect(response.requestId, 'req-456');
    });
  });
}
