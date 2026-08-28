import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flood_guardian/shared/widgets/app_button.dart';
import 'package:flood_guardian/shared/widgets/app_status_indicator.dart';

void main() {
  group('Shared Widgets', () {
    testWidgets('AppButton renders label and handles tap', (WidgetTester tester) async {
      bool tapped = false;
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AppButton(
              label: 'Test Button',
              onPressed: () => tapped = true,
            ),
          ),
        ),
      );

      expect(find.text('Test Button'), findsOneWidget);
      
      await tester.tap(find.byType(AppButton));
      expect(tapped, isTrue);
    });

    testWidgets('AppButton shows loading indicator when isLoading is true', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AppButton(
              label: 'Test Button',
              onPressed: () {},
              isLoading: true,
            ),
          ),
        ),
      );

      expect(find.byType(CircularProgressIndicator), findsOneWidget);
      expect(find.text('Test Button'), findsNothing);
    });

    testWidgets('AppStatusIndicator renders correctly based on RiskState', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: AppStatusIndicator(
              state: RiskState.danger,
              label: 'DANGER ZONE',
            ),
          ),
        ),
      );

      expect(find.text('DANGER ZONE'), findsOneWidget);
      expect(find.byType(Icon), findsOneWidget);
    });
  });
}
