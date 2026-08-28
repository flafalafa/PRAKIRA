import 'package:flutter/material.dart';
import '../../../../app/router.dart';
import '../../../../core/di/service_locator.dart';
import '../controllers/auth_controller.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../shared/widgets/app_button.dart';
import '../../../../app/theme/app_typography.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final AuthController _authController = ServiceLocator.instance.authController;
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _authController.addListener(_onAuthChanged);
  }

  @override
  void dispose() {
    _authController.removeListener(_onAuthChanged);
    _usernameController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _onAuthChanged() {
    if (!mounted) return;
    if (_authController.status == AuthStatus.authenticated) {
      Navigator.pushReplacementNamed(context, AppRouter.dashboardRoute);
    } else if (_authController.status == AuthStatus.authenticationFailure) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(_authController.error?.message ?? 'Login failed'),
          backgroundColor: AppColors.danger, // Wait, is there a danger color? If not, red500. Let's fix that too.
        ),
      );
    }
    // SetState to update loading status
    setState(() {});
  }

  Future<void> _handleLogin() async {
    final username = _usernameController.text.trim();
    final password = _passwordController.text.trim();
    if (username.isEmpty || password.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Please enter username and password'),
          backgroundColor: AppColors.yellow700,
        ),
      );
      return;
    }
    await _authController.login(username, password);
  }

  @override
  Widget build(BuildContext context) {
    final isLoading = _authController.status == AuthStatus.authenticating;

    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Icon(
                Icons.security,
                size: 64,
                color: AppColors.blue500,
              ),
              const SizedBox(height: 32),
              const Text(
                'Enterprise Login',
                style: AppTypography.headline,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 48),
              TextField(
                controller: _usernameController,
                decoration: const InputDecoration(
                  labelText: 'Username',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.person),
                ),
                enabled: !isLoading,
              ),
              const SizedBox(height: 16),
              TextField(
                controller: _passwordController,
                decoration: const InputDecoration(
                  labelText: 'Password',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.lock),
                ),
                obscureText: true,
                enabled: !isLoading,
              ),
              const SizedBox(height: 32),
              AppButton(
                label: isLoading ? 'Authenticating...' : 'Sign In',
                onPressed: isLoading ? () {} : _handleLogin,
                type: AppButtonType.primary,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
