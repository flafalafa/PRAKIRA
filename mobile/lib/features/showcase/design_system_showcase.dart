import 'package:flutter/material.dart';
import '../../app/theme/app_colors.dart';
import '../../app/theme/app_spacing.dart';
import '../../app/theme/app_typography.dart';
import '../../shared/widgets/app_button.dart';
import '../../shared/widgets/app_card.dart';
import '../../shared/widgets/app_chip.dart';
import '../../shared/widgets/app_badge.dart';
import '../../shared/widgets/app_text_field.dart';
import '../../shared/widgets/app_status_indicator.dart';
import '../../shared/widgets/app_alert_banner.dart';
import '../../shared/widgets/app_loading.dart';

class DesignSystemShowcase extends StatelessWidget {
  const DesignSystemShowcase({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Design System Showcase'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(AppSpacing.s16),
        children: [
          _buildSectionTitle('Typography'),
          const Text('Display Text', style: AppTypography.display),
          const Text('Headline Text', style: AppTypography.headline),
          const Text('Title Text', style: AppTypography.title),
          const Text('Body Text', style: AppTypography.body),
          const Text('Caption Text', style: AppTypography.caption),
          const Text('EMERGENCY TEXT', style: AppTypography.emergency),
          
          const Divider(height: AppSpacing.s32),
          
          _buildSectionTitle('Buttons'),
          AppButton(label: 'Primary Button', onPressed: () {}),
          const SizedBox(height: AppSpacing.s8),
          AppButton(label: 'Secondary Button', onPressed: () {}, type: AppButtonType.secondary),
          const SizedBox(height: AppSpacing.s8),
          AppButton(label: 'Danger Button', onPressed: () {}, type: AppButtonType.danger),
          const SizedBox(height: AppSpacing.s8),
          AppButton(label: 'Emergency Button', onPressed: () {}, type: AppButtonType.emergency),
          const SizedBox(height: AppSpacing.s8),
          AppButton(label: 'Loading Button', onPressed: () {}, isLoading: true),
          
          const Divider(height: AppSpacing.s32),

          _buildSectionTitle('Cards'),
          const AppCard(
            child: Text('Default Card Content', style: AppTypography.body),
          ),
          const SizedBox(height: AppSpacing.s8),
          const AppCard(
            type: AppCardType.status,
            child: Text('Status Card Content', style: AppTypography.body),
          ),
          const SizedBox(height: AppSpacing.s8),
          const AppCard(
            type: AppCardType.emergency,
            child: Text('Emergency Card Content', style: AppTypography.body),
          ),

          const Divider(height: AppSpacing.s32),

          _buildSectionTitle('Inputs'),
          const AppTextField(label: 'Email', hint: 'Enter email'),
          const SizedBox(height: AppSpacing.s8),
          const AppTextField(label: 'Password', obscureText: true, errorText: 'Invalid password'),

          const Divider(height: AppSpacing.s32),

          _buildSectionTitle('Chips & Badges'),
          Wrap(
            spacing: AppSpacing.s8,
            children: [
              AppChip(label: 'Filter', onTap: () {}),
              AppChip(label: 'Active', isSelected: true, onTap: () {}),
              const AppBadge(text: 'NEW'),
              const AppBadge(text: '3', color: AppColors.blue500),
            ],
          ),

          const Divider(height: AppSpacing.s32),

          _buildSectionTitle('Status Indicators'),
          const AppStatusIndicator(state: RiskState.safe, label: 'Safe'),
          const SizedBox(height: AppSpacing.s8),
          const AppStatusIndicator(state: RiskState.watch, label: 'Watch'),
          const SizedBox(height: AppSpacing.s8),
          const AppStatusIndicator(state: RiskState.warning, label: 'Warning'),
          const SizedBox(height: AppSpacing.s8),
          const AppStatusIndicator(state: RiskState.danger, label: 'Danger'),
          const SizedBox(height: AppSpacing.s8),
          const AppStatusIndicator(state: RiskState.emergency, label: 'Emergency'),

          const Divider(height: AppSpacing.s32),

          _buildSectionTitle('Alert Banners'),
          const AppAlertBanner(
            state: RiskState.warning,
            title: 'Heavy Rain Expected',
            description: 'Please be cautious on the road.',
            actionLabel: 'Details',
          ),
          const SizedBox(height: AppSpacing.s8),
          const AppAlertBanner(
            state: RiskState.emergency,
            title: 'EVACUATE IMMEDIATELY',
            description: 'Flood levels have exceeded critical limits.',
            actionLabel: 'Instructions',
          ),

          const Divider(height: AppSpacing.s32),

          _buildSectionTitle('Loaders'),
          const AppLoading(isCentered: false),
        ],
      ),
    );
  }

  Widget _buildSectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.only(bottom: AppSpacing.s16),
      child: Text(title, style: AppTypography.title.copyWith(color: AppColors.gray500)),
    );
  }
}
