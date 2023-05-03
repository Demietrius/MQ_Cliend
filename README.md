# Python Lambda Template

## Quick Start

To get started, click "Use this Template" and follow the instructions to create a new repository from this repo. For more information, see [GitHub's documentation](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)

After starting your new project you will need to run
`pip install pre-commit`

To start using this template, make sure to use a replace function that
your ide supports (in pycharm it's Ctrl + shift+ r) to search and replace
```.name``` variable with your lambda function name

## Connecting to API Gateway

This template makes use of several resources that we have access to in API Gateway.

* Token: The security token will be in the header of the request, as `x-token`.
* Authorizer: API Gateway will call the authorizer to validate the token. The authorizer will return the deconstructed token, along with some user data, and it will be populated in the event.
* Query String Parameters: These can be in the URL of the request, and will be populated by API Gateway. They can specify basic details, especially on GET requests.

## To Test

### If you are using pycharm

* Right-click on the src folder and set the Directory as "Source Root"
* Right-click on the tests folder and set the Directory as "Test Source Root"

### For all IDE's

* Add a json file named "CNG_CREDENTIALS" to your folder that contains all your projects (if using PyCharm, it will be called "PyCharmProjects").
The file should consist of at least the variables
  ```json {"ca_user": " ", "ca_password": " "}```. The tests will reference this file to authenticate before each test run. Do not ever put your credentials in the code!
* Navigate to the integration testing and start building and testing

## Test Coverage

You can generate a coverage report that shows the code that your tests run by running

```bash
coverage run -m unittest discover
coverage html
```

You will need the coverage library, so run `pip install coverage` to get it.

## Boilerplate code included in this repo

This repo includes several files that include boilerplate code for your lambda, in the `src` folder. Some of them help with organization of your code, while others wrap various libraries to access different parts of AWS.

- app - The first file the lambda will touch.
- RequestRouter - Handles the different actions your lambda supports.
- Message - Handles the standard response structure and the different error messages you might return.
- ValidateToken - Checks the user's token to get its token data and make sure it is valid.
- cglogging - Manages logging to the Cloudwatch console.
- database_accessor - Manages access to the database. You will edit this to add your own database functions.
- lambda_accessor - Lets you send requests to other lambdas.
- secret_manager - Lets you get AWS secrets, such as ZA tokens and database credentials.
- topic_accessor - Lets you write to a topic.

## Overview

This project contains source code and supporting files for a serverless application that you can deploy with the SAM
CLI. It includes the following files and folders. For your lambda, make sure to rename everything that here says "hello_world"

- hello_world - Code for the application's Lambda function.
- events - Invocation events that you can use to invoke the function.
- tests - Unit tests for the application code.
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are
defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same
deployment process that updates your application code.

If you prefer to use an integrated development environment (IDE) to build and test your application, you can use the AWS
Toolkit.
The AWS Toolkit is an open source plug-in for popular IDEs that uses the SAM CLI to build and deploy serverless
applications on AWS. The AWS Toolkit also adds a simplified step-through debugging experience for Lambda function code.
See the following links to get started.

* [CLion](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [GoLand](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [IntelliJ](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [WebStorm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [Rider](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [PhpStorm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [PyCharm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [RubyMine](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [DataGrip](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [VS Code](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/welcome.html)
* [Visual Studio](https://docs.aws.amazon.com/toolkit-for-visual-studio/latest/user-guide/welcome.html)

## Deploy the sample application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality
for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that
matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI
    - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application
to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region,
  and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual
  review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for
  the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required
  permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value
  for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must
  explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the
  project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your
  application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

## Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
The_Template$ sam build --use-container
```

The SAM CLI installs dependencies defined in `hello_world/requirements.txt`, creates a deployment package, and saves it
in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input
that the function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
The_Template$ sam local invoke HelloWorldFunction --event events/event.json
```

The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
The_Template$ sam local start-api
The_Template$ curl http://localhost:3000/
```

The SAM CLI reads the application template to determine the API's routes and the functions that they invoke.
The `Events` property on each function's definition includes the route and method for each path.

```yaml
      Events:
        HelloWorld:
          Type: Api
          Properties:
            Path: /hello
            Method: get
```

## Add a resource to your application

The application template uses AWS Serverless Application Model (AWS SAM) to define application resources. AWS SAM is an
extension of AWS CloudFormation with a simpler syntax for configuring common serverless application resources such as
functions, triggers, and APIs. For resources not included
in [the SAM specification](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md),
you can use
standard [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html)
resource types.

## Fetch, tail, and filter Lambda function logs

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets you fetch logs generated by your
deployed Lambda function from the command line. In addition to printing the logs on the terminal, this command has
several nifty features to help you quickly find the bug.

`NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using SAM.

```bash
The_Template$ sam logs -n HelloWorldFunction --stack-name The_Template --tail
```

You can find more information and examples about filtering Lambda function logs in
the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html)
.

## Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
The_Template$ pip install -r tests/requirements.txt --user
# unit test
The_Template$ python -m pytest tests/unit -v
# integration test, requiring deploying the stack first.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack we are testing
The_Template$ AWS_SAM_STACK_NAME=<stack-name> python -m pytest tests/integration -v
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack
name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name The_Template
```

## Resources

See
the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)
for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

Next, you can use AWS Serverless Application Repository to deploy ready to use Apps that go beyond hello world samples
and learn how authors developed their
applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)

## Utility

In the top level of project run `python ./utility/error_message_extractor.py` csv file will output into `utility/output/error_messages_sheet.csv`

In the top level of project run `python ./utility/env_variable.py` csv file will output into the console how many times an environment variable is used and where they are located
