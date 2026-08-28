import 'package:equatable/equatable.dart';

class LocationModel extends Equatable {
  final double latitude;
  final double longitude;
  final String? precision;
  final String timezone;
  final String country;
  final String? province;
  final String? city;
  final String? district;
  final String? subdistrict;

  const LocationModel({
    required this.latitude,
    required this.longitude,
    this.precision,
    this.timezone = 'Asia/Jakarta',
    this.country = 'Indonesia',
    this.province,
    this.city,
    this.district,
    this.subdistrict,
  });

  factory LocationModel.fromJson(Map<String, dynamic> json) {
    return LocationModel(
      latitude: (json['latitude'] as num).toDouble(),
      longitude: (json['longitude'] as num).toDouble(),
      precision: json['precision'] as String?,
      timezone: json['timezone'] as String? ?? 'Asia/Jakarta',
      country: json['country'] as String? ?? 'Indonesia',
      province: json['province'] as String?,
      city: json['city'] as String?,
      district: json['district'] as String?,
      subdistrict: json['subdistrict'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'latitude': latitude,
      'longitude': longitude,
      if (precision != null) 'precision': precision,
      'timezone': timezone,
      'country': country,
      if (province != null) 'province': province,
      if (city != null) 'city': city,
      if (district != null) 'district': district,
      if (subdistrict != null) 'subdistrict': subdistrict,
    };
  }

  @override
  List<Object?> get props => [
        latitude,
        longitude,
        precision,
        timezone,
        country,
        province,
        city,
        district,
        subdistrict,
      ];
}
