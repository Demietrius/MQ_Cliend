import datetime
import json
import os
import uuid
import datetime
import random

import boto3
import cglogging as cgl

logger_Class = cgl.cglogging()
logger = logger_Class.setup_logging()


def publish_sns_message(message, messageId, jobId, event, topicArn, domain, region):
    try:
        logger.debug("calling sns")
        # Create an SNS client
        sns = boto3.client('sns', region_name=region)

        # Publish a simple message to the specified SNS topic
        logger.debug("Event Publish : {}".format(message))

        messageString = json.dumps(message)

        if len(messageString) < 250000:

            response = sns.publish( \
                TopicArn=topicArn, \
                Subject=f'Job {jobId} created', \
                MessageDeduplicationId=messageId, \
                MessageGroupId=f'JOB-{jobId}', \
                Message=messageString, \
                MessageAttributes={ \
                    'event': { \
                        'DataType': 'String', \
                        'StringValue': event \
                        }, \
                    'domain': { \
                        'DataType': 'String', \
                        'StringValue': domain \
                        } \
                    } \
                )
            logger.debug("SNS Response: {}".format(response))
        else:
            logger.debug("SNS Message To Large : {}".format(len(messageString)))

        return 0
    except Exception as details:
        logger.error('Unexpected error: {0}'.format(details))
        return 2


def build_sns_message(request, response, user):
    logger.debug("building sns message")
    messageId = str(uuid.uuid4())
    jobId = str(random.randrange(0, 100000))

    message = {
        "eventRequest": request,
        "eventResponse": response,
        "domain": os.getenv("CAG_DOMAIN"),
        "domainKey": format(datetime.datetime.utcnow()),
        "event": request["commonParms"]["action"],
        "authUserId": user.authUserId,
        "authLogonType": user.authLogonType,
        "authBusinessId": user.authBusinessId,
        "authSupplierId": user.authSupplierId,
        "authBranchAccess": user.branchAccess,
        "swapSupplierId": user.swapSupplierId,
        "version": "1.0.0",
        "timeStampOfEvent": format(datetime.datetime.utcnow()),
    }
    publish_sns_message(message, messageId, jobId, request["commonParms"]["action"],
                        os.getenv("CAG_TOPIC"), os.getenv("CAG_DOMAIN"), os.getenv("CAG_REGION"))
