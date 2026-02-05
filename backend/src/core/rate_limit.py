from typing import Dict, Optional
from datetime import datetime, timedelta
import time
import asyncio

# In-memory rate limiter (for development/testing)
# In production, you'd want to use Redis or another distributed store
class RateLimiter:
    def __init__(self):
        self.requests: Dict[str, list] = {}

    def is_allowed(self, identifier: str, max_requests: int, window_seconds: int) -> bool:
        """
        Check if a request is allowed based on rate limits

        Args:
            identifier: Unique identifier for the client (IP, user ID, etc.)
            max_requests: Maximum number of requests allowed
            window_seconds: Time window in seconds

        Returns:
            True if request is allowed, False otherwise
        """
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=window_seconds)

        # Clean up old requests outside the window
        if identifier in self.requests:
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if req_time > window_start
            ]
        else:
            self.requests[identifier] = []

        # Check if we're under the limit
        if len(self.requests[identifier]) < max_requests:
            # Add current request
            self.requests[identifier].append(now)
            return True

        return False

    def get_reset_time(self, identifier: str, window_seconds: int) -> datetime:
        """
        Get the time when the rate limit will reset
        """
        if identifier in self.requests:
            oldest_request = min(self.requests[identifier])
            return oldest_request + timedelta(seconds=window_seconds)
        return datetime.utcnow()

# Global rate limiter instance
rate_limiter = RateLimiter()


class RateLimitService:
    """
    Service class for managing rate limiting across the application
    """

    @staticmethod
    def check_rate_limit(identifier: str, max_requests: int, window_seconds: int) -> tuple[bool, dict]:
        """
        Check if a request is allowed and return rate limit info

        Returns:
            Tuple of (is_allowed: bool, rate_limit_headers: dict)
        """
        is_allowed = rate_limiter.is_allowed(identifier, max_requests, window_seconds)

        # Calculate rate limit headers
        reset_time = rate_limiter.get_reset_time(identifier, window_seconds)
        reset_timestamp = int(reset_time.timestamp())
        current_requests = len(rate_limiter.requests.get(identifier, []))

        headers = {
            "X-RateLimit-Limit": str(max_requests),
            "X-RateLimit-Remaining": str(max(max_requests - current_requests, 0)),
            "X-RateLimit-Reset": str(reset_timestamp),
        }

        return is_allowed, headers


# Convenience function for auth endpoints
def check_auth_rate_limit(identifier: str) -> tuple[bool, dict]:
    """
    Specific rate limiting for authentication endpoints
    Typically more restrictive than general endpoints
    """
    # Allow 5 attempts per 15 minutes for auth endpoints
    return RateLimitService.check_rate_limit(identifier, max_requests=5, window_seconds=900)  # 15 minutes