from django.contrib.sessions.middleware import SessionMiddleware
from django.shortcuts import redirect
from django.urls import resolve


class BackButtonMiddleware(SessionMiddleware):
    def process_request(self, request):
        # Store the current URL in the session if it's not already stored
        print('123=================================================')
        print(request.path)
        print("123=================================================")
        if "last_url" not in request.session:
            request.session["last_url"] = request.path

    def process_response(self, request, response):
        # Check if the request is a result of a "Back" button click
        if (
            request.META.get("HTTP_REFERER")
            and resolve(request.META["HTTP_REFERER"]).url_name
            != resolve(request.path).url_name
        ):
            # Redirect to the last visited URL if it's different from the current URL
            return redirect(request.session["last_url"])

        return response
