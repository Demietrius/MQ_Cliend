import os
import json
import Message
import cglogging as cgl
import process_message
from RequestRouter import RequestRouter

logger_Class = cgl.cglogging()
logger = logger_Class.setup_logging()


def lambda_handler(event, context):
    logger.debug("Received event: {}".format(event))
    message = Message.Message()
    try:
        # Trigger Event
        if "Records" in event:
            for record in event["Records"]:
                if "body" not in record:
                    message.get_fatal_standard_message(2)

                if "Message" not in record["body"]:
                    message.get_fatal_standard_message(3)
                body = json.loads(record["body"])
                if "eventRequest" not in body["Message"] \
                        or "eventResponse" not in body["Message"]:
                    message.get_fatal_standard_message(4)
                trigger_message = json.loads(body["Message"])
                if trigger_message["eventResponse"]["standardResponse"]["returnCode"] == 0:
                    action = trigger_message["eventRequest"]["commonParms"]["action"]
                    response = RequestRouter.router(action,
                                                    trigger_message)

        # This will handle testing locally, or a direct call from a lambda.
        elif "body" not in event:
            if "commonParms" not in event \
                    and "domainName" not in event["context"] \
                    and "action" not in event["commonParms"]:
                return message.get_fatal_standard_message(5)
            request_action = event["commonParms"]["action"]
            response = RequestRouter.router(request_action, event)
        # Main api request
        else:
            # API Gateway request with body, such as POST
            logger.debug("Request is from API Gateway")
            request = json.loads(json.dumps(event))
            body = json.loads(request["body"])
            if body is None:
                # Assemble body from parameters in the event.
                body = {
                    "context": {
                        "client": "CAG POS",
                        "transactionId": "transaction_id",
                        "language": "EN",
                        "domainName": os.environ.get("CAG_DOMAIN")
                    },
                    "commonParms": {
                        "view": "DEFAULT",
                        "version": "1.0.0",
                        "action": request["resource"][1:]  # Get the action from the resource
                    },
                    # get parameter from query parameters
                    "request": request["queryStringParameters"]
                }
            # Get Token and other details from headers, if specified there
            if "x-token" in request["headers"]:
                body["context"]["securityToken"] = request["headers"]["x-token"]

            # grabbing the view from the get request
            if "queryStringParameters" in request and request["queryStringParameters"] is not None \
                    and "view" in request["queryStringParameters"]:
                body["commonParms"]["view"] = request["queryStringParameters"]["view"].upper()

            if "requestContext" in request and "identity" in request["requestContext"] \
                    and "sourceIp" in request["requestContext"]["identity"]:
                body["request"]["requestIp"] = request["requestContext"]["identity"]["sourceIp"]

            if 'context' not in body \
                    and 'commonParms' not in body \
                    and 'domainName' not in body['context'] \
                    and 'action' not in body['commonParms']:
                return message.get_fatal_standard_message(5)

            # Token data from the authorizer
            tokenData = None
            if "requestContext" in event and "authorizer" in event["requestContext"]:
                tokenData = json.loads(event["requestContext"]["authorizer"]["authenticated"])

            request_action = body["commonParms"]["action"]
            logger.debug(request_action)
            response = RequestRouter.router(request_action, body)

        if response["standardResponse"]["returnCode"] == 0:
            transactionResponse = {'statusCode': '200', 'headers': {}}
            transactionResponse['headers']['Content - Type'] = 'applicationjson'
            transactionResponse['headers']['Access-Control-Allow-Methods'] = 'OPTIONS,POST,PUT,PATCH'
            transactionResponse['headers']['Access-Control-Allow-Headers'] = 'Content-Type'
            transactionResponse['headers']['Access-Control-Allow-Origin'] = '*'
            transactionResponse['headers']['Access-Control-Allow-Credentials'] = True
            transactionResponse['body'] = json.dumps(response)
        else:
            transactionResponse = {'statusCode': '400', 'headers': {}}
            transactionResponse['headers']['Content - Type'] = 'applicationjson'
            transactionResponse['headers']['Access-Control-Allow-Methods'] = 'OPTIONS,POST,PUT,PATCH'
            transactionResponse['headers']['Access-Control-Allow-Headers'] = 'Content-Type'
            transactionResponse['headers']['Access-Control-Allow-Origin'] = '*'
            transactionResponse['headers']['Access-Control-Allow-Credentials'] = True
            if "Records" in event:
                transactionResponse['body'] = json.dumps(message.get_good_standard_message())
            else:
                transactionResponse['body'] = json.dumps(response)

            logger.debug("Transaction Response: {}".format(transactionResponse))
        return transactionResponse

    except Exception as details:
        logger.error('Exception, Unexpected error: {} , {}'.format(1, details))
        transactionResponse = {'statusCode': '400', 'headers': {}}
        transactionResponse['headers']['Content - Type'] = 'applicationjson'
        transactionResponse['headers']['Access-Control-Allow-Methods'] = 'OPTIONS,POST,PUT,PATCH'
        transactionResponse['headers']['Access-Control-Allow-Headers'] = 'Content-Type'
        transactionResponse['headers']['Access-Control-Allow-Origin'] = '*'
        transactionResponse['headers']['Access-Control-Allow-Credentials'] = True
        # if this is an event trigger we do not want to return bad request
        if "Records" in event:
            transactionResponse['body'] = json.dumps(message.get_good_standard_message())
        else:
            transactionResponse['body'] = json.dumps(message.get_fatal_standard_message(1))
        return transactionResponse
