"""
The listener of info_reused_pass_checking queue.
Having received a message from the info_reused_pass_checking queue, it updates the information of
reused password accounts for the specific domain.
"""
import datetime
import json
import os
import sys
from typing import Any

import django
import pika

sys.path.append('..')

import modules.support_functions as sup_f

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dc_sonar_web.settings')
django.setup()
from django.conf import settings
from user_cabinet.models import Domain, ReusedPassAcc

filename = os.path.basename(__file__).split('.')[0]
logger = sup_f.init_custome_logger(
    os.path.join(settings.LOGS_DIR, f'{filename}.log'),
    os.path.join(settings.LOGS_DIR, f'{filename}_error.log'),
    logging_level=settings.LOGS_LEVEL,
)


def rmq_callback(channel: Any, method: Any, _: Any, body: Any) -> None:
    """
    The performer of the received message from the queue
    """
    domain = None
    try:
        logger.info('Working on a msg')
        msg = json.loads(body.decode('utf-8'))
        logger.info(f'msg: {msg}')
        domain = Domain.objects.get(pk=msg['domain_pk'])
        if msg['status'] == 'PERFORMING':
            domain.reused_pass_status = Domain.ProcessStatus.PERFORMING
            domain.reused_pass_err_desc = ''
        elif msg['status'] == 'ERROR':
            domain.reused_pass_status = Domain.ProcessStatus.ERROR
            domain.reused_pass_err_desc = msg['error_desc']
        elif msg['status'] == 'FINISHED':
            domain.reused_pass_status = Domain.ProcessStatus.FINISHED
            domain.reused_pass_err_desc = ''
            ReusedPassAcc.objects.filter(domain=domain).delete()
            for user in msg['users']:
                ReusedPassAcc(
                    domain=Domain.objects.get(pk=user['domain_pk']),
                    sam_acc_name=user['user_login'],
                    reused_domain=Domain.objects.get(pk=user['reused_domain_pk']),
                    reused_sam_acc_name=user['reused_user_login'],
                ).save()
        else:
            domain.reused_pass_status = Domain.ProcessStatus.ERROR
            domain.reused_pass_err_desc = f"Unknown msg['status']: {msg['status']}"
        domain.reused_pass_status_update = datetime.datetime.now().astimezone()
        domain.save()

    except Exception as exc:
        logger.error('Error', exc_info=sys.exc_info())
        if domain:
            domain.reused_pass_status = Domain.ProcessStatus.ERROR
            domain.reused_pass_err_desc = sup_f.get_error_text(exc)
            domain.reused_pass_status_update = datetime.datetime.now().astimezone()
            domain.save()
    finally:
        channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':

    rmq_conn = None   # pylint: disable=invalid-name
    try:
        rmq_conn = pika.BlockingConnection(pika.ConnectionParameters(**settings.RMQ_SETTINGS))
        created_channel = rmq_conn.channel()

        created_channel.queue_declare(queue='info_reused_pass_checking', durable=True)
        created_channel.basic_consume(queue='info_reused_pass_checking', on_message_callback=rmq_callback)
        created_channel.start_consuming()
    except Exception:
        logger.error('Error', exc_info=sys.exc_info())
    finally:
        if rmq_conn is not None:
            rmq_conn.close()
