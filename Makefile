
AUTO_BUDGET_NAME ?= autoMonthlyBudgetResource
LAMBDA_DEPLOY_BUCKET ?= cfn-public-bucket-mjasinski128
LAMBDA_DEPLOY_PACKAGE ?= lambda-deployment-package.zip

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
		--timeout-in-minutes 10

remove-budget:
	aws cloudformation delete-stack \
		--stack-name $(AUTO_BUDGET_NAME)