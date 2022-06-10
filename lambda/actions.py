import boto3
import datetime
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('budgets')
AccountId = boto3.client('sts').get_caller_identity().get('Account')


def focm():
    today = datetime.datetime.now()
    first = today.replace(day=1, hour=0, minute=0, second=0)
    firstDayOfCurrMonth = first
    return firstDayOfCurrMonth


def create_budget(name, email, amount, unit='PERCENTAGE', method='EMAIL'):
    response = client.create_budget(
        AccountId=AccountId,
        Budget={
            'BudgetName': name,
            'TimeUnit': 'MONTHLY',
            'TimePeriod': {
                'Start': focm(),
                'End': datetime.datetime(2030, 1, 1)
            },
            'BudgetType': 'COST',
            'LastUpdatedTime': focm(),
            'AutoAdjustData': {
                'AutoAdjustType': 'HISTORICAL',  # | 'FORECAST',
                'HistoricalOptions': {
                    'BudgetAdjustmentPeriod': 1,
                },
            }
        },
        NotificationsWithSubscribers=[
            {
                'Notification': {
                    'NotificationType': 'FORECASTED',
                    'ComparisonOperator': 'GREATER_THAN',
                    'Threshold': amount,
                    'ThresholdType': unit,
                    'NotificationState': 'ALARM',
                },
                'Subscribers': [
                    {
                        'SubscriptionType': method,
                        'Address': email
                    },
                ]
            },
        ]
    )
    return response


def delete_budget(name):
    if get_budget(name) == None:
        return

    response = client.delete_budget(
        AccountId=AccountId,
        BudgetName=name
    )
    return response


def upsert_budget(name, email, amount, unit='PERCENTAGE', method='EMAIL'):
    if get_budget(name) == None:
        print('Create budget')
        create_budget(name, email, amount, unit, method)
    else:
        print('Replace budget')
        delete_budget(name)
        create_budget(name, email, amount, unit, method)


def get_budget(name):
    try:
        response = client.describe_budget(
            AccountId=AccountId,
            BudgetName=name
        )
        return response.get('Budget')

    except ClientError as e:
        if e.response['Error']['Code'] == 'NotFoundException':
            return None
