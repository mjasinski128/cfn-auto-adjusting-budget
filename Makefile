
AUTO_BUDGET_NAME ?= autoMonthlyBudget110
LAMBDA_DEPLOY_BUCKET ?= cfn-public-bucket-mjasinski128
LAMBDA_DEPLOY_PACKAGE ?= autobudget-lambda-deployment-package.zip
EMAIL_ADDRESS ?= mateusz.jasinski@gmail.com

local-invoke:
	python3 -m venv lambda/venv
	. lambda/venv/bin/activate
	python3 lambda/test.py event.json

package-lambda:
	python3 -m venv lambda/venv
	. lambda/venv/bin/activate
	python3 -m pip install -r lambda/requirements.txt --target lambda/
	cd lambda && zip -r ../$(LAMBDA_DEPLOY_PACKAGE) .
	aws s3 cp $(LAMBDA_DEPLOY_PACKAGE) s3://$(LAMBDA_DEPLOY_BUCKET) 
	aws s3api put-object-acl --bucket $(LAMBDA_DEPLOY_BUCKET)  --key $(LAMBDA_DEPLOY_PACKAGE) --acl public-read 

deploy-budget:
	aws cloudformation create-stack \
		--stack-name $(AUTO_BUDGET_NAME) \
		--template-body file://template.yaml \
		--capabilities CAPABILITY_NAMED_IAM \
		--timeout-in-minutes 10 \
		--parameters "ParameterKey=Email,ParameterValue=$(EMAIL_ADDRESS)"

remove-budget:
	aws cloudformation delete-stack \
		--stack-name $(AUTO_BUDGET_NAME)