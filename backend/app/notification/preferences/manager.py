"""Main Preference Manager."""
from app.notification.request import NotificationRequest
from app.notification.preferences.profile import UserPreferenceProfile
from app.notification.preferences.result import NotificationPreferenceResult, PreferenceDecision
from app.notification.preferences.registry import PreferenceFilterRegistry
from app.notification.preferences.filters import MasterSwitchFilter, AreaSubscriptionFilter, SeverityFilter, QuietHoursFilter
from app.notification.preferences.validator import ProfileValidator
from app.notification.preferences.policy import PreferencePolicyConfig
from app.core.logger import get_logger

logger = get_logger(__name__)

# Register core filters
PreferenceFilterRegistry.register(MasterSwitchFilter())
PreferenceFilterRegistry.register(AreaSubscriptionFilter())
PreferenceFilterRegistry.register(SeverityFilter())
PreferenceFilterRegistry.register(QuietHoursFilter())

class PreferenceManager:
    def __init__(self, config: PreferencePolicyConfig = None):
        self.config = config or PreferencePolicyConfig()
        
    def evaluate(self, request: NotificationRequest, profile: UserPreferenceProfile) -> NotificationPreferenceResult:
        logger.info(f"Evaluating preferences for user: {profile.user_id}")
        
        ProfileValidator.validate(profile)
        
        result = NotificationPreferenceResult(
            selected_channels=profile.preferred_channels
        )
        
        # 1. Emergency Override
        is_emergency = request.severity == "EMERGENCY" or request.priority == "EMERGENCY"
        if is_emergency and self.config.emergency_override_enabled:
            logger.info(f"EMERGENCY OVERRIDE active for user {profile.user_id}")
            result.emergency_override_status = True
            result.applied_preferences.append("EMERGENCY_OVERRIDE")
            return result
            
        # 2. Evaluate normal filters
        for filter_obj in PreferenceFilterRegistry.get_all():
            is_allowed, reason = filter_obj.evaluate(request, profile)
            
            if filter_obj.name == "QUIET_HOURS_FILTER":
                result.quiet_hours_status = not is_allowed
                
            if not is_allowed:
                logger.info(f"Notification suppressed by {filter_obj.name}: {reason}")
                result.decision = PreferenceDecision.SUPPRESS
                result.delivery_allowed = False
                result.suppression_reason = reason
                result.applied_preferences.append(filter_obj.name)
                return result
                
            result.applied_preferences.append(filter_obj.name)
            
        logger.info(f"Notification allowed for user {profile.user_id}")
        return result
