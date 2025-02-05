from rest_framework.throttling import BaseThrottle
from rest_framework.exceptions import Throttled
from django.core.cache import cache
from django.conf import settings
from django.utils.timezone import now, timedelta


class GroupBasedThrottle(BaseThrottle):
    def __init__(self):
        self.cache = cache
        self.history = None
        self.rate = None
        self.num_requests = None
        self.duration = None

    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            return None
        user = request.user
        group_name = self.get_user_group(user)
        return f'throttle_{group_name}_{user.id}'

    def get_user_group(self, user):
        if user.is_superuser:
            return 'super_user'
        elif user.groups.filter(name='Manager').exists():
            return 'manager'
        elif user.groups.filter(name='DeliveryCrew').exists():
            return 'delivery_crew'
        return 'default'

    def parse_rate(self, rate):
        if not rate:
            return None, None
        try:
            num_requests, period = rate.split('/')
            duration = {'min': 60, 'hour': 3600, 'day': 86400}.get(period, 60)
            return int(num_requests), duration
        except ValueError:
            return None, None

    def get_rate(self, request):
        group_name = self.get_user_group(request.user)
        rates = getattr(settings, 'REST_FRAMEWORK', {}).get('DEFAULT_THROTTLE_RATES', {})
        rate = rates.get(group_name, rates.get('default', '3/min'))
        return self.parse_rate(rate)

    def allow_request(self, request, view):
        key = self.get_cache_key(request, view)
        if not key:
            return True  # Allow requests for unauthenticated users or no key

        # Fetch rate limit
        self.num_requests, self.duration = self.get_rate(request)
        if not self.num_requests or not self.duration:
            return True  # No throttling if rate or duration is undefined

        self.history = self.cache.get(key, [])

        # Clean up history to only include requests within the current window
        window_start = now() - timedelta(seconds=self.duration)
        self.history = [timestamp for timestamp in self.history if timestamp > window_start]

        if len(self.history) >= self.num_requests:
            # User has hit the rate limit
            retry_after = (self.history[0] + timedelta(seconds=self.duration) - now()).total_seconds()
            self.throttle_failure(retry_after)

        # Add the current request to the history and save it back
        self.history.append(now())
        self.cache.set(key, self.history, timeout=self.duration)
        return True

    def throttle_failure(self, retry_after):
        raise Throttled(detail=f'Request limit exceeded. Try again in {int(retry_after)} seconds.')
