import json
import os

import cglogging as cgl
import boto3
import jwt
from botocore.exceptions import ClientError

logger_Class = cgl.cglogging()
logger = logger_Class.setup_logging()


class ValidateToken:
    token = ""
    authSupplierId = 0
    swappedSupplierId = 0
    authBusinessId = 0
    authUserId = 0
    authLogonType = ""
    branchAccess = []
    public_key = os.environ.get('CAG_public_key')
    region = os.environ.get('CAG_REGION')

    @classmethod
    def validate_jwt(cls, token):
        cls.token = token
        logger.debug("inside validate Token")
        try:
            errNum, return_type, errMsg, publicKey = cls.get_public_key(cls.public_key, cls.region)

            decoded = jwt.decode(cls.token, publicKey, algorithms='RS256')

            if 'exp' not in decoded or 'logonType' not in decoded or \
                    'supplierId' not in decoded or 'userId' not in decoded or \
                    'businessId' not in decoded:
                return 23, 'FATAL', 'Exception, validate token structure'

            else:
                cls.authLogonType = decoded['logonType']
                cls.authBusinessId = decoded['businessId']
                cls.authUserId = decoded['userId']

                # Supplier Id
                cls.authSupplierId = decoded['supplierId']
                if "swapSupplierId" in decoded:
                    cls.swappedSupplierId = decoded["swapSupplierId"]

                # Branch Access, if included
                if "branchAccess" in decoded:
                    cls.branchAccess = decoded["branchAccess"]

                return 0, 'GOOD', errMsg

        except Exception as details:
            logger.error('Unexpected error: {0}'.format(details))
            return 24, 'FATAL', 'Exception, invalid token'

    @classmethod
    def getFromTokenData(cls, token, tokenData):
        # use destructured token so there's no need for a call to secrets
        cls.token = token
        cls.authSupplierId = tokenData["authSupplierId"]
        cls.swappedSupplierId = tokenData["swapSupplierId"]
        cls.authBusinessId = tokenData["authBusinessId"]
        cls.authUserId = tokenData["authUserId"]
        cls.authLogonType = tokenData["authLogonType"]
        cls.branchAccess = tokenData["authBranchAccess"]
        return 0, "GOOD", ""

    @classmethod
    def get_public_key(cls, publicSecretName, regionName):
        errNum, errMsg, secret = 0, '', ''
        try:
            logger.debug("inside get public key")
            public_secret_name = publicSecretName
            region_name = regionName

            # Create a Secrets Manager client
            session = boto3.session.Session()
            client = session.client(
                service_name='secretsmanager',
                region_name=region_name
            )

            try:
                get_secret_value_response = client.get_secret_value(
                    SecretId=public_secret_name
                )
            except ClientError as e:
                logger.debug('Unexpected error: {0}'.format(e))
                if e.response['Error']['Code'] == 'DecryptionFailureException':
                    return 25, 'FATAL', 'DecryptionFailureException', secret
                elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                    return 26, 'FATAL', 'InternalServiceErrorException', secret
                elif e.response['Error']['Code'] == 'InvalidParameterException':
                    return 27, 'FATAL', 'InvalidParameterException', secret
                elif e.response['Error']['Code'] == 'InvalidRequestException':
                    return 38, 'FATAL', 'InvalidRequestException', secret
                elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                    return 35, 'FATAL', 'ResourceNotFoundException', secret
            else:
                # Decrypts secret using the associated KMS CMK.
                # Depending on whether the secret is a string or binary, one of these fields will be populated.
                if 'SecretString' in get_secret_value_response:
                    secretDict = json.loads(get_secret_value_response['SecretString'])
                    secret = secretDict['PublicKey']

            return errNum, 'GOOD', errMsg, secret
        except Exception as details:
            logger.error('Unexpected error: {0}'.format(details))
        return 24, 'FATAL', 'Exception, get public key', secret

    @classmethod
    def get_authLogonType(cls):
        return cls.authLogonType

    @classmethod
    def get_authSupplierId(cls):
        return cls.authSupplierId

    @classmethod
    def get_activeSupplier(cls):
        if cls.swappedSupplierId == 0:
            return cls.authSupplierId
        return cls.swappedSupplierId

    @classmethod
    def get_authBusinessId(cls):
        return cls.authBusinessId

    @classmethod
    def get_authUserId(cls):
        return cls.authUserId

    @classmethod
    def get_branchAccess(cls):
        return cls.branchAccess
