import os
import Message
import topic_accessor
from ValidateToken import ValidateToken as validate_token
import process_message

import cglogging as cgl

logger_Class = cgl.cglogging()
logger = logger_Class.setup_logging()


class RequestRouter:

    @classmethod
    def router(cls, action, request, tokenData):
        message = Message.Message()
        response = None
        requestAction = action.upper()

        # return bad token if error
        if tokenData is not None:
            errNum, return_type, errMsg = validate_token.getFromTokenData(request["context"]["securityToken"],
                                                                          tokenData)
        else:
            errNum, return_type, errMsg = validate_token.validate_jwt(request["context"]["securityToken"])
        if errNum != 0:
            return message.get_response(errNum, "")

        message = Message.Message()
        logger.debug("inside router")

        # Check Security
        security_return = check_security(validate_token, requestAction, request)
        if security_return != 0:
            return message.get_fatal_standard_message(security_return)

        if requestAction == "READ":
            response = process_message.create(request)

        if requestAction == "CREATE":
            response = process_message.update(request)

        elif requestAction == "UPDATE":
            response = process_message.update(request)

        elif requestAction == "DELETE":
            response = process_message.delete(request)

        # writing to the topic
        if response["standardResponse"]["returnCode"] == 0:
            topic_accessor.build_sns_message(request, response)

        return response


# --------------------security check-------------------------------

def check_security(validate_token, action, request):
    # ZA has access no matter what
    if validate_token.authLogonType == "ZA":
        if "supplierId" not in request["request"]:
            request["request"]["supplierId"] = validate_token.get_activeSupplier()
        return 0

    # Non-ZA must be using their active supplier, including CA
    if "supplierId" in request["request"]:
        if request["request"]["supplierId"] != validate_token.get_activeSupplier():
            return 17
    else:
        request["request"]["supplierId"] = validate_token.get_activeSupplier()

    # CA has access to everything
    if validate_token.authLogonType == "CA":
        return 0

    # Supplier Logon Types

    # Who has access to what
    accessDefinitions = {
        "READ": {"SA", "SF", "SC", "SX"},
        "UPDATE": {"SA", "SF", "SX"},
        "CREATE": {},
    }

    # Check branch access for specific rules
    good_access = True
    for branch in validate_token.get_branchAccess:
        # if the token does not match the parent then we throw error
        if branch["account"] == "MASTER" and branch["supplierId"] != validate_token.get_activeSupplier():
            return 30

        # This logic will determine if the domain is at the correct parent or child level
        # logic is defaulted to parent
        if branch["supplierId"] == request["request"]["supplierId"]:
            if branch["account"] == "MASTER":
                # return 30
                break
            if branch["account"] == "BRANCH":
                good_access = False
                # break
    if not good_access:
        return 30

    # Verify the logon type has access to the action
    if validate_token.auth_logonType not in accessDefinitions[action]:
        return 30

    # Allowed
    return 0
