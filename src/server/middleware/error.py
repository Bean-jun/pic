def error_400(request):
    return "Forbidden", 403


def error_500(request):
    return "Internal Error", 500
