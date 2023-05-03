import json
import os

import boto3
import cglogging as cgl

logger_Class = cgl.cglogging()
logger = logger_Class.setup_logging()


class lambda_accessor:
    lambda_client = boto3.client("lambda", region_name=os.environ.get("CAG_REGION"))
    functionName = " "

    @classmethod
    def call_lambda(self, payload, function_name):
        try:
            test = json.dumps(payload)
            response = self.lambda_client.invoke(
                FunctionName=function_name,
                InvocationType="RequestResponse",
                LogType='None',
                Payload=json.dumps(payload),
            )

            #  does response contain payload element
            if 'Payload' not in response:
                return 19, None #missing Payload

            if 'StatusCode' not in response or response['StatusCode'] != 200:
                return 20, None #missing StatusCode

            jsonString = response['Payload'].read()
            responseObj = json.loads(jsonString)
            logger.debug("JSON String Response from profile: {}".format(responseObj))
            # add message validation on the response and take error
            if "body" in responseObj:
                body = json.loads(responseObj["body"])
                if 'standardResponse' not in body:
                    return 21, None  # "No standardResponse element in response from profiles"

                if body['standardResponse']['returnCode'] != 0:
                    return body['standardResponse']['returnCode'], responseObj
                return 0, body

            if 'standardResponse' not in responseObj:
                return 21, None  # "No standardResponse element in response from profiles"

            if responseObj['standardResponse']['returnCode'] != 0:
                return responseObj['standardResponse']['returnCode'], responseObj

            return 0, "GOOD", responseObj # good request

        except Exception as details:
            logger.error('Unexpected error: {0}'.format(details))
            return 22, None  # "Exception, on read"
