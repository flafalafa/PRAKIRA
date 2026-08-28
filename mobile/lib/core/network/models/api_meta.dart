import 'package:equatable/equatable.dart';
import 'pagination_meta.dart';

class ApiMeta extends Equatable {
  final PaginationMeta? pagination;
  final String? source;
  final DateTime? lastUpdated;
  final List<String>? warnings;

  const ApiMeta({
    this.pagination,
    this.source,
    this.lastUpdated,
    this.warnings,
  });

  factory ApiMeta.fromJson(Map<String, dynamic> json) {
    return ApiMeta(
      pagination: json['pagination'] != null
          ? PaginationMeta.fromJson(json['pagination'])
          : null,
      source: json['source'] as String?,
      lastUpdated: json['last_updated'] != null
          ? DateTime.tryParse(json['last_updated'] as String)
          : null,
      warnings: json['warnings'] != null
          ? List<String>.from(json['warnings'])
          : null,
    );
  }

  @override
  List<Object?> get props => [pagination, source, lastUpdated, warnings];
}
