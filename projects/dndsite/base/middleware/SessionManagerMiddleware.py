from base.managers.SessionManager import SessionManager


class SessionManagerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.session_manager = SessionManager(session=request.session)
        response = self.get_response(request)
        return response