import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone

from app.core.config import settings


def create_signed_token(subject: str) -> str:
    """Simple JWT-like token for local development; replace in production."""
    payload = {
        "sub": subject,
        "iat": int(datetime.now(timezone.utc).timestamp()),
        "exp": int((datetime.now(timezone.utc) + timedelta(hours=24)).timestamp()),
    }
    header = {"alg": "HS256", "typ": "JWT"}
    encoded_header = base64.urlsafe_b64encode(json.dumps(header, separators=(",", ":")).encode()).rstrip(b"=")
    encoded_payload = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).rstrip(b"=")
    signing_input = f"{encoded_header.decode()}.{encoded_payload.decode()}".encode()
    digest = hmac.new(settings.jwt_secret.encode(), signing_input, hashlib.sha256).digest()
    signature = base64.urlsafe_b64encode(digest).rstrip(b"=")
    return f"{encoded_header.decode()}.{encoded_payload.decode()}.{signature.decode()}"
