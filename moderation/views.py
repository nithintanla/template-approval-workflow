from django.http import JsonResponse
from .utils import moderate_campaign

def moderate_template(request):
    if request.method == "POST":
        content = request.POST.get("content", "")
        result = moderate_campaign(content)
        return JsonResponse({"status": result})
    return JsonResponse({"error": "Invalid request"}, status=400)
