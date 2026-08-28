import 'package:flutter/material.dart';
import '../../app/theme/app_spacing.dart';

enum AppCardType { defaultCard, interactive, status, emergency }

class AppCard extends StatelessWidget {
  final Widget child;
  final EdgeInsetsGeometry padding;
  final AppCardType type;
  final VoidCallback? onTap;
  final Color? color;

  const AppCard({
    super.key,
    required this.child,
    this.padding = const EdgeInsets.all(AppSpacing.s16),
    this.type = AppCardType.defaultCard,
    this.onTap,
    this.color,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    Color? cardColor = color;
    double elevation = theme.cardTheme.elevation ?? 2.0;

    if (type == AppCardType.emergency) {
      cardColor = theme.colorScheme.errorContainer;
      elevation = 8.0;
    } else if (type == AppCardType.status && cardColor == null) {
      cardColor = theme.colorScheme.primaryContainer;
    }

    Widget cardContent = Padding(
      padding: padding,
      child: child,
    );

    if (onTap != null || type == AppCardType.interactive) {
      cardContent = InkWell(
        onTap: onTap,
        borderRadius: theme.cardTheme.shape is RoundedRectangleBorder 
            ? (theme.cardTheme.shape as RoundedRectangleBorder).borderRadius as BorderRadius?
            : null,
        child: cardContent,
      );
    }

    return Card(
      color: cardColor,
      elevation: elevation,
      child: cardContent,
    );
  }
}
