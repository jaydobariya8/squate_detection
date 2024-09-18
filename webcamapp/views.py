import os
import time
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'webcamapp/index.html')

@csrf_exempt
def save_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        file_path = os.path.join(settings.MEDIA_ROOT, f'image_{int(time.time())}.jpg')

        with open(file_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

        return JsonResponse({'status': 'Image saved successfully!'})
    return JsonResponse({'status': 'Failed to save image.'}, status=400)

def camera_view(request):
    return render(request, 'webcamapp/camera.html')
