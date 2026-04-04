import json
import logging

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from core.services.ai import analyze_page

logger = logging.getLogger('core.views.ai')


@method_decorator(csrf_exempt, name='dispatch')
class AnalyzePageView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        url = data.get('url', '').strip()
        if not url:
            return JsonResponse({'error': 'URL required'}, status=400)

        result = analyze_page(
            title=data.get('title', ''),
            url=url,
            description=data.get('description', ''),
            keywords=data.get('keywords', ''),
            content=data.get('content', ''),
        )

        if result is None:
            return JsonResponse({'error': 'Analysis failed'}, status=500)

        return JsonResponse(result)
