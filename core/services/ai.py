import json
import logging

from django.conf import settings
from google import genai

logger = logging.getLogger('core.ai')

GEMINI_MODEL = 'gemini-flash-lite-latest'

PROMPT_TEMPLATE = """Bu web sayfasi icin:
1. Tam olarak 3-5 adet kisa etiket oner (kucuk harf, Turkce veya Ingilizce, virgullu liste)
2. Sayfayi anlatan 2 paragraflik Turkce SEO aciklama yaz (sayfa ne hakkinda, kimin isine yarar, neden degerli)

Sayfa bilgileri:
Baslik: {title}
URL: {url}
Aciklama: {description}
Meta keywords: {keywords}

Sayfa icerigi:
{content}

Cevabini SADECE su JSON formatinda ver, baska bir sey yazma:
{{"tags": ["etiket1", "etiket2", "etiket3"], "description": "aciklama metni"}}"""


def analyze_page(title, url, description='', keywords='', content=''):
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key:
        logger.warning('GEMINI_API_KEY not configured')
        return None

    client = genai.Client(api_key=api_key)

    prompt = PROMPT_TEMPLATE.format(
        title=title or 'bilinmiyor',
        url=url,
        description=description or 'yok',
        keywords=keywords or 'yok',
        content=(content or '')[:2000],
    )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={
                'temperature': 0.3,
                'max_output_tokens': 500,
            },
        )
        text = response.text.strip()

        # Bazen markdown code block icinde donuyor
        if text.startswith('```'):
            text = text.split('\n', 1)[1].rsplit('```', 1)[0].strip()

        result = json.loads(text)
        return {
            'tags': [t.lower().strip() for t in result.get('tags', []) if t.strip()][:7],
            'description': result.get('description', ''),
        }
    except json.JSONDecodeError:
        logger.error('Gemini JSON parse hatasi: %s', text[:200])
        return None
    except Exception as e:
        logger.error('Gemini API hatasi: %s', e)
        return None
