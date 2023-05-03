import os
import sys

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH, ".aws-sam/build/HelloWorldFunction"
)

sys.path.append(SOURCE_PATH)

os.environ["CAG_BUSINESS_PROFILE_FUNCTION"] = "BusinessProfileMS-Dev"
os.environ["CAG_private_key"] = "CAG_Private_Key-Dev"
os.environ["CAG_public_key"] = "CAG_Public_Key-Dev"
os.environ["CAG_REGION"] = "us-east-1"
os.environ["ENVIRONMENT_TYPE"] = "local"
os.environ["CAG_DATABASE_CREDENTIALS"] = "CAG_ForeFlight_Connection-Dev"
os.environ["CAG_DOMAIN"] = "Template"
os.environ["CAG_ERROR_NUMBER"] = "1000"
