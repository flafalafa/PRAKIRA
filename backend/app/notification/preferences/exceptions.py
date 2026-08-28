"""Preference Module Exceptions."""
from app.notification.exceptions import NotificationException

class PreferenceException(NotificationException):
    pass

class PreferenceLoadFailure(PreferenceException):
    pass

class PreferenceValidationFailure(PreferenceException):
    pass

class QuietHoursFailure(PreferenceException):
    pass

class AreaPreferenceFailure(PreferenceException):
    pass

class ChannelPreferenceFailure(PreferenceException):
    pass
