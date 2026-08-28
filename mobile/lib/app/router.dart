import 'package:flutter/material.dart';
import '../features/showcase/design_system_showcase.dart';
import '../features/auth/presentation/screens/splash_screen.dart';
import '../features/auth/presentation/screens/login_screen.dart';
import '../features/dashboard/presentation/screens/dashboard_screen.dart';
import '../features/areas/presentation/screens/area_selection_screen.dart';

class AppRouter {
  static const String splashRoute = '/';
  static const String loginRoute = '/login';
  static const String dashboardRoute = '/dashboard';
  static const String showcaseRoute = '/showcase';
  
  static const String homeRoute = '/home'; // Retained for compatibility if needed
  static const String areasRoute = '/areas';
  static const String predictionsRoute = '/predictions';
  static const String alertsRoute = '/alerts';
  static const String notificationsRoute = '/notifications';
  static const String settingsRoute = '/settings';

  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case splashRoute:
        return MaterialPageRoute(builder: (_) => const SplashScreen());
      case loginRoute:
        return MaterialPageRoute(builder: (_) => const LoginScreen());
      case dashboardRoute:
        return MaterialPageRoute(builder: (_) => const DashboardScreen());
      case showcaseRoute:
        return MaterialPageRoute(builder: (_) => const DesignSystemShowcase());
      case homeRoute:
        return MaterialPageRoute(builder: (_) => const PlaceholderScreen(title: 'Home'));
      case areasRoute:
        return MaterialPageRoute(builder: (_) => const AreaSelectionScreen());
      case predictionsRoute:
        return MaterialPageRoute(builder: (_) => const PlaceholderScreen(title: 'Predictions'));
      case alertsRoute:
        return MaterialPageRoute(builder: (_) => const PlaceholderScreen(title: 'Alerts'));
      case notificationsRoute:
        return MaterialPageRoute(builder: (_) => const PlaceholderScreen(title: 'Notifications'));
      case settingsRoute:
        return MaterialPageRoute(builder: (_) => const PlaceholderScreen(title: 'Settings'));
      default:
        return MaterialPageRoute(
          builder: (_) => Scaffold(
            body: Center(child: Text('No route defined for ${settings.name}')),
          ),
        );
    }
  }
}

// Temporary placeholder for architecture foundation
class PlaceholderScreen extends StatelessWidget {
  final String title;
  const PlaceholderScreen({super.key, required this.title});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: Center(child: Text('Screen: $title\nArchitecture Foundation')),
    );
  }
}
