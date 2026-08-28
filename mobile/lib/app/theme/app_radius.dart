import 'package:flutter/material.dart';

class AppRadius {
  AppRadius._();

  static const double r4 = 4.0;
  static const double r8 = 8.0;
  static const double r12 = 12.0;
  static const double r16 = 16.0;
  static const double r24 = 24.0;
  static const double r999 = 999.0; // Pill shape

  // Semantic radius
  static const BorderRadius small = BorderRadius.all(Radius.circular(r4));
  static const BorderRadius medium = BorderRadius.all(Radius.circular(r8));
  static const BorderRadius large = BorderRadius.all(Radius.circular(r16));
  static const BorderRadius extraLarge = BorderRadius.all(Radius.circular(r24));
  static const BorderRadius full = BorderRadius.all(Radius.circular(r999));
}
