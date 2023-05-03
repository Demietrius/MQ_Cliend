from database_accessor import DatabaseConnector
from Message import Message


def create(request):
    message = Message
    database = DatabaseConnector()

    # validating request
    return_code = check_create(request)
    if return_code != 0:
        return message.get_fatal_standard_message(return_code)


def read(request):
    message = Message
    database = DatabaseConnector()

    # validating request
    return_code = check_read(request)
    if return_code != 0:
        return message.get_fatal_standard_message(return_code)


def update(request):
    message = Message
    database = DatabaseConnector()

    # validating request
    return_code = check_update(request)
    if return_code != 0:
        return message.get_fatal_standard_message(return_code)


def delete(request):
    message = Message
    database = DatabaseConnector()

    # validating request
    return_code = check_delete(request)
    if return_code != 0:
        return message.get_fatal_standard_message(return_code)


# ---------------------------request validation------------------------------


def check_commonparams(request):
    if "commonParms" not in request:
        return 7
    if "action" not in request["commonParms"]:
        return 8
    if "view" not in request["commonParms"]:
        return 9
    if "version" not in request["commonParms"]:
        return 10
    else:
        return 0


def check_context(request):
    if "context" not in request:
        return 11
    if "securityToken" not in request["context"]:
        return 12
    if "domainName" not in request["context"]:
        return 13
    if "language" not in request["context"]:
        return 14
    else:
        return 0


def check_read(request):
    return_code = check_commonparams(request)
    if return_code != 0:
        return return_code
    return_code = check_context(request)
    if return_code != 0:
        return return_code
    if "request" not in request:
        return 16
    if "supplierId" not in request["request"]:
        return 17
    if "businessProfileId" not in request["request"]:
        return 18
    else:
        return 0


def check_create(request):
    return_code = check_commonparams(request)
    if return_code != 0:
        return return_code
    return_code = check_context(request)
    if return_code != 0:
        return return_code
    if "request" not in request:
        return 16
    if "supplierId" not in request["request"]:
        return 17
    if "businessProfileId" not in request["request"]:
        return 18
    else:
        return 0


def check_update(request):
    return_code = check_commonparams(request)
    if return_code != 0:
        return return_code
    return_code = check_context(request)
    if return_code != 0:
        return return_code
    if "request" not in request:
        return 16
    if "supplierId" not in request["request"]:
        return 17
    if "businessProfileId" not in request["request"]:
        return 18
    else:
        return 0


def check_delete(request):
    return_code = check_commonparams(request)
    if return_code != 0:
        return return_code
    return_code = check_context(request)
    if return_code != 0:
        return return_code
    if "request" not in request:
        return 16
    if "supplierId" not in request["request"]:
        return 17
    if "businessProfileId" not in request["request"]:
        return 18
    else:
        return 0
