
## Auto Adjusting Budgets ##

New feature in AWS Budgets that enables customer to define limits based on your actual spend in the past (https://aws.amazon.com/about-aws/whats-new/2022/02/auto-adjusting-budgets/).
This removes guess work and allows to easily target increase in your spend.

Cloud Formation (CFN) resource for it is expected in future but is not yet supported, we have only web console and SDKs. CFN is extensible and in this particular case we will be using Custom Resources (https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources-lambda.html).
Custom Resource is essentially a user defined construct in CFN template that is fully programmable, in order to create, update or delete this new resource it invokes an AWS Lambda function that performs all the work. This implementastion uses Python SDK for AWS.


### Prerequisites ###


#### Baic #### 
* AWS CLI

#### Advanced ####
* python3
* pip
* make

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

`make deploy-budget` - deploy resources using CFN template

`make remove-budget` - remove budget with all created resources


Deploy as CFN StackSet to multiple OUs (https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html)

#### Advanced ####

`make package-lambda` - build deployment package and upload to shared location - required only after change to Lambda code.


### Current limitations ###
Provided sample relies on publicly readable S3 bucket - Lambda requires dedicated bundle/package that contains all dependancies. As such it has to be referenced by CFN template as zip bundle external to main template and must be accessible/redable during deployment.
It is strongly recommended to use location that is restricted to only IAM role used for CloudFormation deployment.

