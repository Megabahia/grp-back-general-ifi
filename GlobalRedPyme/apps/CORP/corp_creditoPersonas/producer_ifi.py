import boto3
import json
# Importar configuraciones
from apps.config import config


def publish(data):
    topicArn = config.AWS_TOPIC_ARN
    snsClient = boto3.client(
        'sns',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        region_name=config.AWS_REGION_NAME,
    )

    data.pop('reporteBuro')
    data.pop('identificacion')
    data.pop('ruc')
    data.pop('rolesPago')
    data.pop('panillaIESS')
    data.pop('documentoAprobacion')
    data.pop('imagen')
    data.pop('imagenComercial')

    response = snsClient.publish(
        TopicArn=topicArn,
        Message=json.dumps(data),
        Subject='PURCHASE',
        MessageAttributes={"TransactionType":{"DataType":"String","StringValue":"PURCHASE"}}
    )
    print(response['ResponseMetadata']['HTTPStatusCode'])