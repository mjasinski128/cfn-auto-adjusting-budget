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
    logger.info('Props {}'.format(event['ResourceProperties']))
    responseData = {}

    print(boto3.__version__)
    print('Name ' + event['ResourceProperties'].get('Name'))
    print('Amount/Prc ' + str(event['ResourceProperties'].get('Amount')))
    print('Email ' + event['ResourceProperties'].get('Email'))

    if event['RequestType'] == 'Create' or event['RequestType'] == 'Update':
        actions.upsert_budget(event['ResourceProperties'].get('Name'), amount=int(
            event['ResourceProperties'].get('Amount')), email=event['ResourceProperties'].get('Email'))

    if event['RequestType'] == 'Delete':
        actions.delete_budget(event['ResourceProperties'].get('Name'))

    logger.info('responseData {}'.format(responseData))
    cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData)
