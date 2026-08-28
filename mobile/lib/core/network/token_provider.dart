abstract class TokenProvider {
  /// Gets the current authentication token if one exists.
  /// Returns null if the user is not authenticated.
  Future<String?> getToken();
}
