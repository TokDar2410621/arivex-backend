class CloudflareIPMiddleware:
    """Reads CF-Connecting-IP and rewrites REMOTE_ADDR so DRF throttles use the real client IP."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cf_ip = request.META.get("HTTP_CF_CONNECTING_IP")
        if cf_ip:
            request.META["REMOTE_ADDR"] = cf_ip
        else:
            forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
            if forwarded:
                request.META["REMOTE_ADDR"] = forwarded.split(",")[0].strip()
        return self.get_response(request)
