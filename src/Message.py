import json
import datetime
import os


class Message:

    def __init__(self):
        self.dictionary = {
            # app message error codes
            1: "Unexpected error",
            2: "Missing body from Record.",
            3: "Missing Message from body.",
            4: "Missing eventResponse from Message.",
            5: "Request is not formatted correctly .",
            # process message error codes
            7: "Missing commonParms from request.",
            8: "Missing action from request.",
            9: "Missing view from request.",
            10: "Missing version from request.",
            11: "Missing context from request.",
            12: "Missing securityToken.",
            13: "Missing domainName.",
            14: "Missing language",
            15: "Missing request from request.",
            17: "Missing supplierId from request",
            18: "Missing businessProfileId from request.",
            # lambda accessor error codes
            19: "Missing payload from response in the lambda accessor.",
            20: "Missing StatusCode from response in the lambda accessor.",
            21: "Missing standardResponse from response body in the lambda accessor.",
            22: "Unexpected error in lambda accessor.",
            # validate token error codes
            23: "Exception, validate token structure.",
            24: "Unexpected error in validate token.",
            25: "Decryption failure exception.",
            26: "Internal service error exception.",
            27: "Invalid parameter exception.",
            28: "Invalid request exception.",
            29: "Resource not found exception.",
            30: "You are not allowed to perform this action.",
            # secret manager error codes
            31: "Decryption failure exception in secret manager.",
            33: "Invalid parameter exception in secret manager.",
            34: "Invalid request exception in secret manager.",
            35: "ResourceNotFoundException in secret manager.",
            36: "Error while crating secret in secret manager.",
            37: "Error while updating secret in secret manager.",
            38: "Duplicate secret in secret manager.",
            39: "Unexpected error in secret manager.",

            # database accessor error codes
            40: "Failed to connect to database.",
            41: "Failed to return data from database.",
            42: "Failed to read from database",
            43: "Failed to update from database",

            # lambda-specific error codes
            44: " "
        }
        self.message = {"standardResponse": {}, "responseMessage": {}}
        self.warnings = {"warnings": []}

    def add_warnings(self, warning):
        self.warnings["warnings"].append(warning)

    def add_all_warnings(self, warnings):
        self.warnings["warnings"].extend(warnings)

    def get_response(self, err_num, response):

        if err_num == 0:
            self.message["standardResponse"] = self.get_good_standard_message()["standardResponse"]
            self.message["responseMessage"] = response
            print(json.dumps(self.message))
            return self.message

        else:
            self.message["standardResponse"] = self.get_fatal_standard_message(err_num)["standardResponse"]
            self.message["responseMessage"] = response
            print(json.dumps(self.message))
            return self.message

    def get_good_standard_message(self):
        return {
            "standardResponse": {
                "count": 0,
                "domain": os.getenv("CAG_DOMAIN"),
                "errorMessage": "",
                "language": "EN",
                "responseType": "GOOD",
                "returnCode": 0,
                "timeStampOfMessage": format(datetime.datetime.utcnow()),
                "warnings": self.warnings["warnings"]
            }
        }

    def get_fatal_standard_message(self, err_num, custom_error=None):
        if custom_error is None:
            error_message = self.dictionary[err_num]
        else:
            error_message = custom_error
        return {
            "standardResponse": {
                "count": 0,
                "domain": os.getenv("CAG_DOMAIN"),
                "errorMessage": error_message,
                "language": "EN",
                "responseType": "FATAL",
                "returnCode": (int(os.getenv("CAG_ERROR_NUMBER")) + err_num),
                "timeStampOfMessage": format(datetime.datetime.utcnow()),
                "warnings": self.warnings["warnings"]
            }
        }
