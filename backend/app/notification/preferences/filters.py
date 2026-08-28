"""Preference Filters."""
from abc import ABC, abstractmethod
from typing import Tuple
from app.notification.request import NotificationRequest
from app.notification.preferences.profile import UserPreferenceProfile
from app.notification.preferences.quiet_hours import QuietHoursEvaluator

class BaseFilter(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @abstractmethod
    def evaluate(self, request: NotificationRequest, profile: UserPreferenceProfile) -> Tuple[bool, str]:
        """Returns (is_allowed, reason)"""
        pass

class MasterSwitchFilter(BaseFilter):
    name = "MASTER_SWITCH_FILTER"
    
    def evaluate(self, request: NotificationRequest, profile: UserPreferenceProfile) -> Tuple[bool, str]:
        if not profile.notifications_enabled:
            return False, "User has globally disabled notifications"
        return True, ""

class AreaSubscriptionFilter(BaseFilter):
    name = "AREA_SUBSCRIPTION_FILTER"
    
    def evaluate(self, request: NotificationRequest, profile: UserPreferenceProfile) -> Tuple[bool, str]:
        if not profile.subscribed_areas:
            return False, "User has no subscribed areas"
            
        if request.area_id not in profile.subscribed_areas:
            return False, f"User is not subscribed to area: {request.area_id}"
            
        return True, ""

class SeverityFilter(BaseFilter):
    name = "SEVERITY_FILTER"
    
    def evaluate(self, request: NotificationRequest, profile: UserPreferenceProfile) -> Tuple[bool, str]:
        severity_ranks = {"SAFE": 1, "WATCH": 2, "WARNING": 3, "DANGER": 4, "EMERGENCY": 5}
        req_rank = severity_ranks.get(request.severity, 0)
        prof_rank = severity_ranks.get(profile.minimum_severity, 0)
        
        if req_rank < prof_rank:
            return False, f"Notification severity ({request.severity}) is below user minimum ({profile.minimum_severity})"
            
        return True, ""

class QuietHoursFilter(BaseFilter):
    name = "QUIET_HOURS_FILTER"
    
    def evaluate(self, request: NotificationRequest, profile: UserPreferenceProfile) -> Tuple[bool, str]:
        if QuietHoursEvaluator.is_active(profile.quiet_hours):
            return False, "Quiet hours are currently active"
        return True, ""
