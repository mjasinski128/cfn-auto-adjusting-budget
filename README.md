
## Auto Adjusting Budgets ##

New feature in AWS Budgets that enables customer to define limits based on your actual spend in the past (https://aws.amazon.com/about-aws/whats-new/2022/02/auto-adjusting-budgets/).
This removes guess work and allows to easily target increase in your spend.

Cloud Formation (CFN) resource for it is expected in future but is not yet supported, we have only web console and SDKs. CFN is extensible and in this particular case we will be using Custom Resources (https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources-lambda.html).
Custom Resource is essentially a user defined construct in CFN template that is fully programmable, in order to create, update or delete this new resource it invokes an AWS Lambda function that performs all the work. This implementastion uses Python SDK for AWS.


### Prerequisites ###

#### Basic #### 
* AWS CLI or web console

#### Advanced ####
* `python3`
* `pip`
* `make`

### Usage ###

#### Basic ####
 
Deploy to single AWS account with AWS CLI

```
	aws cloudformation create-stack \
		--stack-name SOME_STACK_NAME \
		--template-body file://template.yaml \
		--capabilities CAPABILITY_NAMED_IAM \
		--timeout-in-minutes 10 \
		--parameters "ParameterKey=Email,ParameterValue=SOME_EMAIL_ADDRESS"
```


using provided scripts:

* `make deploy-budget EMAIL_ADDRESS=SOME_EMAIL_ADDRESS` - deploy resources using CFN template
* `make remove-budget` - remove budget with all created resources


Deploy as CFN StackSet to multiple OUs (https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html)


Parameters:
* CFN `Amount` - Trigger value - i.e. 110 is 110% of reference value
* CFN `LambdaDeployBucket` / Make `LAMBDA_DEPLOY_BUCKET` - Name of S3 bucket for Lambda artefact. Default: `cfn-public-bucket-mjasinski128`
* CFN `LambdaDeployPackage` / Make `LAMBDA_DEPLOY_PACKAGE` - Name of Lambda aftefact. Default: `autobudget-lambda-deployment-package.zip`
* CFN `Email` / Make `EMAIL_ADDRESS` - E-mail address for buget notifications  - Default: `budget-alarms@example.com`



#### Advanced ####

* `make package-lambda` - Build deployment package and upload to shared location - (required once & after change to Lambda code).


### Current limitations ###

* Publicly readable S3 bucket - Project contains two parts, Lambda code in zip bundle and deployment template for CloudFormation.
Lambda needs to be built first, before Cloudformation makes request for it and stored on public S3 bycket or one readable during deploymnet (by CFN deployment IAM role) 

* Lambda bundle needs to be uploaded to S3 bucket before Clouddformation deployment.

* Budget name is auto-generated and can not be changed - each Budget has unique name to avoid conflicts and crashes (benefit in StackSet deployments).
