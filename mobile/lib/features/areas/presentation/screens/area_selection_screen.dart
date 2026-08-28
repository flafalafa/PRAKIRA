import 'package:flutter/material.dart';
import '../../../../core/di/service_locator.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../shared/widgets/app_loading.dart';
import '../../../../shared/widgets/app_error_state.dart';
import '../../../../shared/widgets/app_empty_state.dart';
import '../controllers/area_controller.dart';

class AreaSelectionScreen extends StatefulWidget {
  const AreaSelectionScreen({super.key});

  @override
  State<AreaSelectionScreen> createState() => _AreaSelectionScreenState();
}

class _AreaSelectionScreenState extends State<AreaSelectionScreen> {
  final _areaController = ServiceLocator.instance.areaController;
  final TextEditingController _searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _areaController.addListener(_onAreaStateChanged);
    // Only load if empty to prevent unnecessary network calls
    if (_areaController.areas.isEmpty) {
      _areaController.loadAreas();
    }
  }

  @override
  void dispose() {
    _areaController.removeListener(_onAreaStateChanged);
    _searchController.dispose();
    super.dispose();
  }

  void _onAreaStateChanged() {
    setState(() {});
  }

  void _handleAreaSelected(String areaId) async {
    await _areaController.selectArea(areaId);
    if (!mounted) return;
    
    // Return to previous screen (Dashboard)
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Select Area'),
      ),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_areaController.status == AreaStateStatus.loading) {
      return const AppLoading();
    }

    if (_areaController.status == AreaStateStatus.error) {
      return AppErrorState(
        title: 'Failed to Load Areas',
        message: _areaController.error?.message ?? 'An unknown error occurred.',
        onRetry: () => _areaController.loadAreas(),
      );
    }

    if (_areaController.status == AreaStateStatus.empty || _areaController.areas.isEmpty) {
      return AppEmptyState(
        title: 'No Areas Found',
        message: 'There are currently no areas available.',
        icon: Icons.map_outlined,
        actionLabel: 'Refresh',
        onAction: () => _areaController.loadAreas(),
      );
    }

    // Filter areas based on search text
    final searchQuery = _searchController.text.toLowerCase();
    final filteredAreas = _areaController.areas.where((area) {
      return area.areaName.toLowerCase().contains(searchQuery);
    }).toList();

    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(16.0),
          child: TextField(
            controller: _searchController,
            decoration: InputDecoration(
              hintText: 'Search areas...',
              prefixIcon: const Icon(Icons.search),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(8),
              ),
              contentPadding: const EdgeInsets.symmetric(horizontal: 16),
            ),
            onChanged: (value) => setState(() {}), // Trigger rebuild to filter
          ),
        ),
        Expanded(
          child: RefreshIndicator(
            onRefresh: () => _areaController.loadAreas(),
            child: ListView.separated(
              itemCount: filteredAreas.length,
              separatorBuilder: (context, index) => const Divider(height: 1),
              itemBuilder: (context, index) {
                final area = filteredAreas[index];
                final isSelected = _areaController.activeArea?.areaId == area.areaId;

                return ListTile(
                  title: Text(
                    area.areaName,
                    style: AppTypography.title.copyWith(
                      fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                      color: isSelected ? AppColors.blue700 : AppColors.gray900,
                    ),
                  ),
                  subtitle: Text(
                    '${area.areaType.toUpperCase()} • ${area.areaCode}',
                    style: AppTypography.bodyMedium.copyWith(color: AppColors.gray600),
                  ),
                  trailing: isSelected 
                      ? const Icon(Icons.check_circle, color: AppColors.blue500) 
                      : null,
                  onTap: () => _handleAreaSelected(area.areaId),
                );
              },
            ),
          ),
        ),
      ],
    );
  }
}
