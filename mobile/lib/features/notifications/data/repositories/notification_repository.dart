import '../../../../core/errors/failure.dart';
import '../../../../core/errors/network_exceptions.dart';
import '../../../../core/network/models/api_response.dart';
import '../datasources/notification_remote_datasource.dart';
import '../models/notification_model.dart';

class NotificationRepository {
  final NotificationRemoteDataSource remoteDataSource;

  NotificationRepository({required this.remoteDataSource});

  Future<PaginatedResponse<NotificationModel>> getNotifications(
    String areaId, {
    int page = 1,
    int pageSize = 20,
    String? severity,
    String? status,
  }) async {
    try {
      final response = await remoteDataSource.getNotifications(
        areaId,
        page: page,
        pageSize: pageSize,
        severity: severity,
        status: status,
      );

      final data = response.data.map((json) => NotificationModel.fromJson(json)).toList();

      return PaginatedResponse<NotificationModel>(
        data: data,
        meta: response.meta,
        requestId: response.requestId,
        timestamp: response.timestamp,
        version: response.version,
      );
    } on NetworkException catch (e) {
      throw mapExceptionToFailure(e);
    } catch (e) {
      throw mapExceptionToFailure(Exception(e.toString()));
    }
  }

  Future<SuccessResponse<NotificationModel>> getNotificationById(String notificationId) async {
    try {
      final response = await remoteDataSource.getNotificationById(notificationId);
      final data = NotificationModel.fromJson(response.data);

      return SuccessResponse<NotificationModel>(
        data: data,
        meta: response.meta,
        requestId: response.requestId,
        timestamp: response.timestamp,
        version: response.version,
      );
    } on NetworkException catch (e) {
      throw mapExceptionToFailure(e);
    } catch (e) {
      throw mapExceptionToFailure(Exception(e.toString()));
    }
  }
}
