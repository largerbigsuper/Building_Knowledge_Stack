from django.contrib.auth import login, logout

from server.server_settings import UID, CID
from server.settings import DATETIME_FORMAT


def customer_login(request, user):
    login(request, user)
    request.session[UID] = user.id
    request.session[CID] = user.customer.id


def admin_login(request, user):
    login(request, user)
    request.session[UID] = user.id


def common_logout(request):
    logout(request)

def strtime(datime):
    return datime.strftime(DATETIME_FORMAT)

def get_filename(filename):
    return filename.upper()
