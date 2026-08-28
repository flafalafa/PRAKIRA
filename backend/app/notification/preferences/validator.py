"""Profile Validator."""
from app.notification.preferences.profile import UserPreferenceProfile
from app.notification.preferences.exceptions import PreferenceValidationFailure

class ProfileValidator:
    @staticmethod
    def validate(profile: UserPreferenceProfile) -> bool:
        if not profile.user_id:
            raise PreferenceValidationFailure("User ID is required")
        if not profile.preferred_channels:
            raise PreferenceValidationFailure("At least one preferred channel is required")
        valid_severities = ["SAFE", "WATCH", "WARNING", "DANGER", "EMERGENCY"]
        if profile.minimum_severity not in valid_severities:
            raise PreferenceValidationFailure(f"Invalid minimum severity: {profile.minimum_severity}")
        return True
