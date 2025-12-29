def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

def parse_browser(user_agent: str) -> str:
    ua = user_agent.lower()
    if 'chrome' in ua:
        return 'Chrome'
    if 'safari' in ua:
        return 'Safari'
    if 'firefox' in ua:
        return 'Firefox'
    return 'Other'

def get_status_code(extra: dict):
    return extra.get('status_code')

BOT_KEYWORDS = [
    'bot',
    'crawler',
    'spider',
    'slurp',
    'bingpreview',
    'facebookexternalhit',
    'whatsapp',
    'telegrambot',
]


def is_bot(user_agent: str) -> bool:
    if not user_agent:
        return False
    ua = user_agent.lower()
    return any(keyword in ua for keyword in BOT_KEYWORDS)