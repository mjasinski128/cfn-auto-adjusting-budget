#!/usr/bin/env python3

import actions
import logging
import boto3
from time import tzname
import cfnresponse

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info('Event {}'.format(event))
    responseData = {}

    props = event['ResourceProperties']
    logger.info('Props {}'.format(props))

    budgetName = event['LogicalResourceId']+'-'+event['StackId'].split('/')[-1]

    print('Name ' + budgetName)
    print('Amount/Prc ' + str(event['ResourceProperties'].get('Amount')))
    print('Email ' + event['ResourceProperties'].get('Email'))

    if event['RequestType'] == 'Create' or event['RequestType'] == 'Update':
        actions.upsert_budget(budgetName, amount=int(
            event['ResourceProperties'].get('Amount')), email=event['ResourceProperties'].get('Email'))

    if event['RequestType'] == 'Delete':
        actions.delete_budget(budgetName)

    logger.info('responseData {}'.format(responseData))
    cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData)
