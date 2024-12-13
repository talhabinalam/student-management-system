from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exclude certain URLs from login check
        excluded_urls = [
            reverse('login'),  # Login page
            '/admin/'          # Admin site
        ]

        # Skip authentication check for excluded URLs
        if not request.user.is_authenticated and not any(
            request.path.startswith(url) for url in excluded_urls
        ):
            return redirect('login')

        return self.get_response(request)
