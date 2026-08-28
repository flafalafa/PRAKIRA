import 'package:flutter_test/flutter_test.dart';
import 'package:flood_guardian/core/network/models/api_error.dart';

void main() {
  group('ApiError', () {
    test('fromJson parses correctly', () {
      final json = {
        "error_code": "VALIDATION_FAILED",
        "message": "Invalid parameters",
        "details": {"field": "is required"},
        "request_id": "req-789",
        "timestamp": "2026-08-19T00:00:00Z",
        "path": "/api/v1/test",
        "version": "v1"
      };

      final error = ApiError.fromJson(json);

      expect(error.errorCode, 'VALIDATION_FAILED');
      expect(error.message, 'Invalid parameters');
      expect(error.details?['field'], 'is required');
      expect(error.requestId, 'req-789');
      expect(error.path, '/api/v1/test');
    });

    test('fromJson handles missing fields with defaults', () {
      final json = <String, dynamic>{};

      final error = ApiError.fromJson(json);

      expect(error.errorCode, 'UNKNOWN_ERROR');
      expect(error.message, 'An unknown error occurred.');
      expect(error.requestId, '');
      expect(error.path, '');
      expect(error.version, 'v1');
    });
  });
}
