from rest_framework.exceptions import APIException


class AlreadyStarted(APIException):
    status_code = 409
    default_detail = 'Match has already started'
    default_code = 'already_started'


class AlreadyFinished(APIException):
    status_code = 409
    default_detail = 'Match is already finished'
    default_code = 'already_finished'


class AlreadyClosed(APIException):
    status_code = 409
    default_detail = 'Match is already closed'
    default_code = 'already_closed'
