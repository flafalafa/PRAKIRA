import 'package:flutter/material.dart';
import '../../../../core/di/service_locator.dart';
import '../../../../app/router.dart';
import '../controllers/auth_controller.dart';
import '../../../../app/theme/app_colors.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    _checkSession();
  }

  Future<void> _checkSession() async {
    // Add a slight delay for better UX on fast devices
    await Future.delayed(const Duration(seconds: 1));
    
    final authController = ServiceLocator.instance.authController;
    await authController.restoreSession();

    if (!mounted) return;

    if (authController.status == AuthStatus.authenticated) {
      Navigator.pushReplacementNamed(context, AppRouter.dashboardRoute);
    } else {
      Navigator.pushReplacementNamed(context, AppRouter.loginRoute);
    }
  }

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      backgroundColor: AppColors.blue500,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.water_drop,
              size: 80,
              color: AppColors.white,
            ),
            SizedBox(height: 24),
            Text(
              'Flood Guardian',
              style: TextStyle(
                color: AppColors.white,
                fontSize: 28,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 48),
            CircularProgressIndicator(
              valueColor: AlwaysStoppedAnimation<Color>(AppColors.white),
            ),
          ],
        ),
      ),
    );
  }
}
