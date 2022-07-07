"""
Models for user cabinet logic
"""
import datetime
from typing import Any

from django.db import models


class Domain(models.Model):
    """
    Using domains in app
    """

    class ProcessStatus(models.TextChoices):
        """
        Statuses for process
        """

        # waiting of registration software in domain after adding domain in list
        WAIT_SOFT_ADDING = 'WAIT_SOFT_ADDING'
        # initial status after successful registration in domain
        INIT = 'INIT'
        # waiting of start a process
        WAIT_PERFORMING = 'WAIT_PERFORMING'
        # a process is being performed
        PERFORMING = 'PERFORMING'
        # a process has been done
        FINISHED = 'FINISHED'
        # if an error occurs during a process
        ERROR = 'ERROR'

    name: Any = models.CharField(max_length=255, unique=True, null=False)
    hostname: Any = models.CharField(max_length=255, unique=True, null=False)
    base_dn: Any = models.CharField(max_length=255, unique=True, null=False)
    workstation_name: Any = models.CharField(max_length=15, null=True)
    workstation_password: Any = models.CharField(max_length=128, null=True)
    user_dn: Any = models.CharField(max_length=255, unique=True, null=False)
    user_password: Any = models.CharField(max_length=128, null=True)

    dump_status: Any = models.CharField(
        max_length=20, default=ProcessStatus.WAIT_SOFT_ADDING, choices=ProcessStatus.choices
    )
    dump_status_update: Any = models.DateTimeField(default=datetime.datetime(1970, 1, 1))
    dump_err_desc: Any = models.TextField(null=True)

    brute_status: Any = models.CharField(
        max_length=20, default=ProcessStatus.WAIT_SOFT_ADDING, choices=ProcessStatus.choices
    )
    brute_progress: Any = models.PositiveSmallIntegerField(default=0)
    brute_status_update: Any = models.DateTimeField(default=datetime.datetime(1970, 1, 1))
    brute_error_desc: Any = models.TextField(null=True)
    no_exp_pass_status: Any = models.CharField(
        max_length=20, default=ProcessStatus.WAIT_SOFT_ADDING, choices=ProcessStatus.choices
    )
    no_exp_pass_status_update: Any = models.DateTimeField(default=datetime.datetime(1970, 1, 1))
    no_exp_pass_err_desc: Any = models.TextField(null=True)
    reused_pass_status: Any = models.CharField(
        max_length=20, default=ProcessStatus.WAIT_SOFT_ADDING, choices=ProcessStatus.choices
    )
    reused_pass_status_update: Any = models.DateTimeField(default=datetime.datetime(1970, 1, 1))
    reused_pass_err_desc: Any = models.TextField(null=True)



    def __str__(self) -> str:
        return f'{self.hostname}'


class BrutedNTLMAcc(models.Model):
    """
    Accounts bruted via NTLM-hashes
    """

    domain: Any = models.ForeignKey(Domain, on_delete=models.CASCADE)
    sam_acc_name: Any = models.CharField(max_length=15)
    acc_password: Any = models.CharField(max_length=128)
    update_time: Any = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.domain.name}, {self.sam_acc_name}'


class NoExpPassAcc(models.Model):
    """
    Accounts with never expire passwords
    """

    domain: Any = models.ForeignKey(Domain, on_delete=models.CASCADE)
    sam_acc_name: Any = models.CharField(max_length=15)
    create_time: Any = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.domain.name}, {self.sam_acc_name}'


class ReusedPassAcc(models.Model):
    """
    Accounts with reused passwords in different domains
    """

    domain: Any = models.ForeignKey(Domain, on_delete=models.CASCADE)
    sam_acc_name: Any = models.CharField(max_length=15)
    create_time: Any = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.domain.name}, {self.sam_acc_name}'
