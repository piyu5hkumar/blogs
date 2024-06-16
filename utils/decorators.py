from utils.custom_response import APIResponse
import functools
from rest_framework import status
from django.db import transaction
import traceback


def try_except_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            resp = func(*args, **kwargs)
            return resp
        except Exception as e:
            traceback.print_exc()
            return APIResponse(success=False, message=repr(e), status=status.HTTP_400_BAD_REQUEST)
    return wrapper


def try_except_rollback_handler(func):
    @functools.wraps(func)
    @transaction.atomic
    def wrapper(*args, **kwargs):
        try:
            resp = func(*args, **kwargs)
            return resp
        except Exception as e:
            transaction.set_rollback(True)
            traceback.print_exc()
            return APIResponse(success=False, message=str(e), status=status.HTTP_400_BAD_REQUEST)
    return wrapper