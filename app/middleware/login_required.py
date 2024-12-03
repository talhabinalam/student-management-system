from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exclude certain URLs from login check
        excluded_urls = [reverse('login')]  # Add more public routes here
        if not request.user.is_authenticated and request.path not in excluded_urls:
            return redirect('login')
        return self.get_response(request)
