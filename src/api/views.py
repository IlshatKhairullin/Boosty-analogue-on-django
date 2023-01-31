from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view()
def status_view(request):
    return Response({"status": "ok"})
