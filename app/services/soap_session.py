import threading
import time
from zeep import Client

# Stores the current valid SOAP SessionId. If None, there is no active session.
_session_id = None
# A threading lock to ensure that only one thread at a time can update the session.
# This prevents race conditions if multiple requests try to refresh the session simultaneously.
_session_lock = threading.Lock()
# Stores the expiration time (as a Unix timestamp) for the current session.
# If the current time is greater than this value, the session is considered expired and a new login is needed.
_session_expiry = 0  # timestamp

# Logs in to the SOAP service using the configured credentials and returns a new SessionId.
def login_soap():
    client = Client(SOAP_URL)
    result = client.service.OpenSession(logon=SOAP_USER, password=SOAP_PASS)
    return result.SessionId

# Checks if the given SessionId is still valid by calling the SOAP service's CheckSession method.
# Returns True if the session is valid, False otherwise.
def check_session(session_id):
    client = Client(SOAP_URL)
    sc = {"SessionId": session_id, "IsAuthenticated": True}
    try:
        client.service.CheckSession(sc)
        return True
    except Exception:
        return False

# Returns a valid SessionId for SOAP requests.
# If there is no session, or the session is expired, or the session is invalid, it logs in again to obtain a new SessionId.
# Uses a lock to ensure thread safety.
def get_soap_session_id():
    global _session_id, _session_expiry
    with _session_lock:
        now = time.time()
        # If there is no session, or it is expired, or the check fails, log in again
        if not _session_id or now > _session_expiry or not check_session(_session_id):
            _session_id = login_soap()
            _session_expiry = now + 25 * 60  # 25 minutes validity
        return _session_id

# Returns the security context dictionary required by SOAP methods:
# { "SessionId": <valid session id>, "IsAuthenticated": True }
# Always ensures the SessionId is valid by calling get_soap_session_id().
def get_security_context():
    return {"SessionId": get_soap_session_id(), "IsAuthenticated": True}

# Closes the current SOAP session by calling the CloseSession method on the SOAP service, and clears the stored SessionId.
def logout_soap():
    global _session_id
    if _session_id:
        client = Client(SOAP_URL)
        sc = {"SessionId": _session_id, "IsAuthenticated": True}
        try:
            client.service.CloseSession(sc)
        except Exception:
            pass
        _session_id = None 