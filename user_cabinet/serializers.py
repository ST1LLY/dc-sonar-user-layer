from typing import Any

from rest_framework import serializers

from .models import Domain, BrutedNTLMAcc, NoExpPassAcc, ReusedPassAcc
from socket import gethostbyname, gaierror


class DomainSerializer(serializers.ModelSerializer[Domain]):
    class Meta:
        model = Domain
        fields = [
            'pk',
            'name',
            'hostname',
            'base_dn',
            'workstation_name',
            'workstation_password',
            'user_dn',
            'user_password',
            'dump_status',
            'dump_status_update',
            'dump_err_desc',
            'brute_status',
            'brute_progress',
            'brute_status_update',
            'brute_error_desc',
            'no_exp_pass_status',
            'no_exp_pass_status_update',
            'no_exp_pass_err_desc',
            'reused_pass_status',
            'reused_pass_status_update',
            'reused_pass_err_desc',
        ]

    @staticmethod
    def validate_hostname(value: str) -> str:
        """
        Try to resolve the fqdn before adding
        """
        try:
            gethostbyname(value)
        except gaierror as e:
            raise serializers.ValidationError(f'Error resolving DNS for {value}: {e}')
        return value


# class PublicDomainSerializer(serializers.ModelSerializer[Domain]):
#     pk = serializers.IntegerField(read_only=True)
#     fqdn = serializers.CharField(read_only=True)
#
#     class Meta:
#         model = Domain
#         fields = ['pk', 'fqdn']


class BrutedNTLMAccSerializer(serializers.ModelSerializer[BrutedNTLMAcc]):
    class Meta:
        model = BrutedNTLMAcc
        fields = ['pk', 'domain', 'sam_acc_name', 'acc_password', 'update_time']


class NoExpPassAccSerializer(serializers.ModelSerializer[NoExpPassAcc]):
    class Meta:
        model = NoExpPassAcc
        fields = ['pk', 'domain', 'sam_acc_name', 'create_time']


class ReusedPassAccSerializer(serializers.ModelSerializer[ReusedPassAcc]):
    class Meta:
        model = NoExpPassAcc
        fields = ['pk', 'domain', 'sam_acc_name', 'create_time']
