import '../../features/areas/data/models/location_model.dart';

abstract class LocationProvider {
  Future<LocationModel?> getCurrentLocation();
}

class NoOpLocationProviderImpl implements LocationProvider {
  @override
  Future<LocationModel?> getCurrentLocation() async {
    // T-805: GPS/Device location is a future concern.
    // This implementation serves purely as an architectural boundary.
    return null;
  }
}
