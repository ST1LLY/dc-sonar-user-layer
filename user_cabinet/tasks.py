import json
import logging
import os
import sys

import pika
from celery import shared_task
from django.conf import settings
from django.core import serializers
from django.db.models import Q
from filelock import Timeout, FileLock

import user_cabinet.modules.support_functions as sup_f
from .models import Domain


@shared_task()
def NTLMDumpJobSetter() -> None:
    task_name = 'ntlm-dump-job-setter'
    logging.info(f'run {task_name}')
    rmq_conn = None
    try:

        lock = FileLock(os.path.join(settings.LOCKS_DIRS['user_cabinet'], f'{task_name}.lock'), timeout=1)
        with lock.acquire(timeout=10):

            domains_qs = Domain.objects.filter(
                (
                    Q(dump_status=Domain.ProcessStatus.INIT)
                    | Q(dump_status=Domain.ProcessStatus.ERROR)
                    | Q(dump_status=Domain.ProcessStatus.FINISHED)
                )
                & (
                    Q(brute_status=Domain.ProcessStatus.INIT)
                    | Q(brute_status=Domain.ProcessStatus.ERROR)
                    | Q(brute_status=Domain.ProcessStatus.FINISHED)
                )
            )

            if not domains_qs:
                logging.info("Domains for dumping haven't been gotten")
                return
            logging.info(f'domains_qs = {domains_qs}')

            domains = json.loads(
                serializers.serialize(
                    'json', domains_qs, fields=('pk', 'name', 'hostname', 'workstation_name', 'workstation_password')
                )
            )
            logging.info(f'domains = {domains}')
            for idx, domain in enumerate(domains):

                rmq_conn = pika.BlockingConnection(pika.ConnectionParameters(**settings.RMQ_SETTINGS))
                channel = rmq_conn.channel()
                channel.queue_declare(queue='wait_dumping_ntlm', durable=True)

                logging.info(f'domain: {domain}')

                channel.basic_publish(
                    exchange='',
                    routing_key='wait_dumping_ntlm',
                    body=sup_f.dict_to_json_bytes(domain),
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # make message persistent
                    ),
                )
                domains_qs[idx].dump_status = Domain.ProcessStatus.WAIT_PERFORMING
                domains_qs[idx].save()
    except Timeout:
        logging.info(f'Previous process of {task_name} is working')
    except Exception:
        logging.error('Error', exc_info=sys.exc_info())
    finally:
        if rmq_conn is not None:
            rmq_conn.close()


@shared_task()
def NoExpPassJobSetter() -> None:
    task_name = 'noexp-pass-job-setter'
    logging.info(f'run {task_name}')
    rmq_conn = None
    try:

        lock = FileLock(os.path.join(settings.LOCKS_DIRS['user_cabinet'], f'{task_name}.lock'), timeout=1)
        with lock.acquire(timeout=10):
            domains_qs = Domain.objects.filter(
                Q(no_exp_pass_status=Domain.ProcessStatus.INIT)
                | Q(no_exp_pass_status=Domain.ProcessStatus.ERROR)
                | Q(no_exp_pass_status=Domain.ProcessStatus.FINISHED)
            )
            if not domains_qs:
                logging.info("Domains for checking no exp passwords haven't been found")
                return
            logging.info(f'domains_qs = {domains_qs}')
            domains = json.loads(
                serializers.serialize(
                    'json', domains_qs, fields=('pk', 'name', 'hostname', 'base_dn', 'user_dn', 'user_password')
                )
            )
            logging.info(f'domains = {domains}')

            for idx, domain in enumerate(domains):

                rmq_conn = pika.BlockingConnection(pika.ConnectionParameters(**settings.RMQ_SETTINGS))
                channel = rmq_conn.channel()
                channel.queue_declare(queue='wait_no_exp_pass_checking', durable=True)

                logging.info(f'domain: {domain}')

                channel.basic_publish(
                    exchange='',
                    routing_key='wait_no_exp_pass_checking',
                    body=sup_f.dict_to_json_bytes(domain),
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # make message persistent
                    ),
                )
                domains_qs[idx].no_exp_pass_status = Domain.ProcessStatus.WAIT_PERFORMING
                domains_qs[idx].save()

    except Timeout:
        logging.info(f'Previous process of {task_name} is working')
    except Exception:
        logging.error('Error', exc_info=sys.exc_info())
    finally:
        if rmq_conn is not None:
            rmq_conn.close()


@shared_task()
def ReusedPassJobSetter() -> None:
    task_name = 'reused-pass-job-setter'
    logging.info(f'run {task_name}')
    rmq_conn = None
    try:
        lock = FileLock(os.path.join(settings.LOCKS_DIRS['user_cabinet'], f'{task_name}.lock'), timeout=1)
        with lock.acquire(timeout=10):
            pass
    except Timeout:
        logging.info(f'Previous process of {task_name} is working')
    except Exception:
        logging.error('Error', exc_info=sys.exc_info())
    finally:
        if rmq_conn is not None:
            rmq_conn.close()
