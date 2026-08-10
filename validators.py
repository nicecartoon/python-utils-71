from typing import Any, Dict


class Validator:
    """Class to validate input data types and structures."""

    @staticmethod
    def is_non_empty_string(value: Any) -> bool:
        """Check if the value is a non-empty string."""
        return isinstance(value, str) and len(value) > 0

    @staticmethod
    def is_positive_integer(value: Any) -> bool:
        """Check if the value is a positive integer."""
        return isinstance(value, int) and value > 0

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate the format of an email address."""
        import re
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(email_regex, email) is not None

    @staticmethod
    def validate_user_data(user_data: Dict[str, Any]) -> bool:
        """Validate user data against required fields."""
        return (Validator.is_non_empty_string(user_data.get('username')) and 
                Validator.is_valid_email(user_data.get('email')) and 
                Validator.is_positive_integer(user_data.get('age')))
