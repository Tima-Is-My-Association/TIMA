from piwikapi.tracking import PiwikTracker
from TIMA.settings import PIWIK_SITE_ID, PIWIK_URL, PIWIK_AUTH_TOKEN
from urllib.error import HTTPError

def track(request, title):
    if PIWIK_SITE_ID and PIWIK_URL and PIWIK_AUTH_TOKEN:
        try:
            piwik = PiwikTracker(PIWIK_SITE_ID, request)
            piwik.set_api_url('%s/piwik.php' % PIWIK_URL)
            piwik.set_ip(get_client_ip(request))
            piwik.set_token_auth(PIWIK_AUTH_TOKEN)
            piwik.do_track_page_view(title)
        except HTTPError:
            pass

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    else:
        return request.META.get('REMOTE_ADDR')