import 'package:flutter/material.dart';
import '../../../../shared/widgets/app_card.dart';
import '../../../../shared/widgets/app_loading.dart';
import '../../../../shared/widgets/app_error_state.dart';
import '../../../../shared/widgets/app_empty_state.dart';
import '../controllers/area_controller.dart';
import '../../data/models/area_model.dart';

class AreaSelectorWidget extends StatefulWidget {
  final AreaController controller;

  const AreaSelectorWidget({super.key, required this.controller});

  @override
  State<AreaSelectorWidget> createState() => _AreaSelectorWidgetState();
}

class _AreaSelectorWidgetState extends State<AreaSelectorWidget> {
  @override
  void initState() {
    super.initState();
    widget.controller.addListener(_onControllerUpdate);
    // Trigger initial load if not already loaded
    if (widget.controller.status == AreaStateStatus.initial) {
      widget.controller.loadAreas();
    }
  }

  @override
  void dispose() {
    widget.controller.removeListener(_onControllerUpdate);
    super.dispose();
  }

  void _onControllerUpdate() {
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    switch (widget.controller.status) {
      case AreaStateStatus.initial:
      case AreaStateStatus.loading:
        return const AppLoading();
      case AreaStateStatus.error:
        return AppErrorState(
          title: 'Failed to Load Areas',
          message: widget.controller.error?.message ?? 'An unknown error occurred.',
          onRetry: () => widget.controller.loadAreas(),
        );
      case AreaStateStatus.empty:
        return AppEmptyState(
          title: 'No Areas Found',
          message: 'There are currently no areas available for monitoring.',
          icon: Icons.map_outlined,
          actionLabel: 'Refresh',
          onAction: () => widget.controller.loadAreas(),
        );
      case AreaStateStatus.loaded:
        return _buildAreaList(widget.controller.areas);
    }
  }

  Widget _buildAreaList(List<AreaModel> areas) {
    return ListView.builder(
      shrinkWrap: true,
      itemCount: areas.length,
      itemBuilder: (context, index) {
        final area = areas[index];
        final isSelected = widget.controller.activeArea?.areaId == area.areaId;

        return Padding(
          padding: const EdgeInsets.only(bottom: 8.0),
          child: AppCard(
            onTap: () => widget.controller.selectArea(area.areaId),
            child: ListTile(
              title: Text(area.areaName, style: const TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text(area.areaCode),
              trailing: isSelected
                  ? Icon(Icons.check_circle, color: Theme.of(context).primaryColor)
                  : const Icon(Icons.circle_outlined, color: Colors.grey),
            ),
          ),
        );
      },
    );
  }
}
