from rest_framework.exceptions import APIException


class MatchAlreadyPlayed(APIException):
    status_code = 409
    default_detail = 'Match is already played'
    default_code = 'match_already_played'


class MatchAlreadyClosed(APIException):
    status_code = 409
    default_detail = 'Match is already closed'
    default_code = 'match_already_closed'


class MatchNotPlayed(APIException):
    status_code = 409
    default_detail = 'Match still has to be played'
    default_code = 'match_not_played'
