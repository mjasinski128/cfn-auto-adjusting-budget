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


def update_budget(name, email, amount, unit='PERCENTAGE', method='EMAIL'):
    response = client.update_budget(
        AccountId=AccountId,
        NewBudget={
            'BudgetName': name,
            'TimeUnit': 'MONTHLY',
            'TimePeriod': {
                'Start': focm(),
                'End': datetime.datetime(2030, 1, 1)
            },
            'BudgetType': 'COST',
            'AutoAdjustData': {
                'AutoAdjustType': 'HISTORICAL',
                'HistoricalOptions': {
                    'BudgetAdjustmentPeriod': 1,
                },
            }
        },
    )

    responseAct = client.describe_notifications_for_budget(
        AccountId=AccountId,
        BudgetName=name,
        MaxResults=100
    )

    logger.info('describe_notifications_for_budget {}'.format(responseAct))

    # print('responseAct '+name+' '+AccountId)
    # print(json.dumps(responseAct, indent=4, sort_keys=True, default=str))

    responseSub = client.describe_subscribers_for_notification(
        AccountId=AccountId,
        BudgetName=name,
        Notification=responseAct.get('Notifications')[0],
        MaxResults=100
    )

    logger.info('describe_subscribers_for_notification {}'.format(responseSub))

    # print('responseSub '+name+' '+AccountId+' ' +
    #       responseSub.get('Subscribers')[0].get('Address')+' '+str(email))
    # print(json.dumps(responseSub, indent=4, sort_keys=True, default=str))

    if email != responseSub.get('Subscribers')[0].get('Address'):
        client.update_subscriber(
            AccountId=AccountId,
            BudgetName=name,
            Notification=responseAct.get('Notifications')[0],
            OldSubscriber=responseSub.get('Subscribers')[0],
            NewSubscriber={
                'SubscriptionType': method,
                'Address': email
            }
        )

    if amount != responseAct.get('Notifications')[0].get('Threshold'):
        client.update_notification(
            AccountId=AccountId,
            BudgetName=name,
            OldNotification=responseAct.get('Notifications')[0],
            NewNotification={
                'NotificationType': responseAct.get('Notifications')[0].get('NotificationType'),
                'ComparisonOperator': responseAct.get('Notifications')[0].get('ComparisonOperator'),
                'Threshold': amount,
                'ThresholdType': unit,
                'NotificationState': responseAct.get('Notifications')[0].get('NotificationState'),
            }
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
        print('Create')
        create_budget(name, email, amount, unit, method)
    else:
        print('Update')
        update_budget(name, email, amount, unit, method)


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


#bname = 'Budg4'
#upsert_budget(bname, amount=125, email='mateusz.jasinski@gmail.com')
#create_budget(bname, amount=126, email='mateusz.jasinski@gmail.com')
# update_budget(bname)
# delete_budget(bname)
#print(json.dumps(get_budget(bname), indent=4, sort_keys=True, default=str))
