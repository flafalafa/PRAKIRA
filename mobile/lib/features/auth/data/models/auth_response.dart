class AuthResponse {
  final String accessToken;

  const AuthResponse({
    required this.accessToken,
  });

  factory AuthResponse.fromJson(Map<String, dynamic> json) {
    return AuthResponse(
      accessToken: json['access_token'] as String,
    );
  }
}
