import 'package:flutter/material.dart';

class AppDivider extends StatelessWidget {
  final double indent;
  final double endIndent;

  const AppDivider({
    super.key,
    this.indent = 0.0,
    this.endIndent = 0.0,
  });

  @override
  Widget build(BuildContext context) {
    return Divider(
      indent: indent,
      endIndent: endIndent,
    );
  }
}
