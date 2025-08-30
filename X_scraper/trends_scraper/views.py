from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import TrendRun
from scraper import main  # tumhara existing scraper function
import uuid
from datetime import datetime
import socket


# -----------------------------
# GET latest trend
# -----------------------------
@require_http_methods(["GET"])
def latest_trends(request):
    try:
        trend = TrendRun.objects.latest("scraped_at")
        data = {
            "id": str(trend.id),
            "trend1": trend.trend1,
            "trend2": trend.trend2,
            "trend3": trend.trend3,
            "trend4": trend.trend4,
            "trend5": trend.trend5,
            "scraped_at": trend.scraped_at,
            "ip_address": trend.ip_address,
        }
        return JsonResponse(data, status=200)
    except TrendRun.DoesNotExist:
        return JsonResponse({"error": "No trends found"}, status=404)


# -----------------------------
# POST: scrape & save new trend
# -----------------------------
@csrf_exempt
@require_http_methods(["POST"])
def scrape_save_trend(request):
    try:
        trends_list = main()  # returns list of 5 strings
        if len(trends_list) < 5:
            trends_list += [""] * (5 - len(trends_list))

        trend_obj = TrendRun.objects.create(
            id=uuid.uuid4(),
            trend1=trends_list[0],
            trend2=trends_list[1],
            trend3=trends_list[2],
            trend4=trends_list[3],
            trend5=trends_list[4],
            scraped_at=datetime.utcnow(),
            ip_address=socket.gethostbyname(socket.gethostname())
        )

        data = {
            "id": str(trend_obj.id),
            "trend1": trend_obj.trend1,
            "trend2": trend_obj.trend2,
            "trend3": trend_obj.trend3,
            "trend4": trend_obj.trend4,
            "trend5": trend_obj.trend5,
            "scraped_at": trend_obj.scraped_at,
            "ip_address": trend_obj.ip_address,
            "message": "Trend scraped and saved successfully!"
        }
        return JsonResponse(data, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
