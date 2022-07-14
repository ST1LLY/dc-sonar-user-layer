from socket import gethostbyname, gaierror
from typing import Any

from rest_framework import serializers

from .models import Domain, BrutedNTLMAcc, NoExpPassAcc, ReusedPassAcc
from .modules.aes_cipher import AESCipher


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

    def create(self, validated_data: Any) -> Any:
        aes_cipher = AESCipher()
        validated_data['workstation_password'] = aes_cipher.encrypt(validated_data['workstation_password'])
        validated_data['user_password'] = aes_cipher.encrypt(validated_data['user_password'])
        return Domain.objects.create(**validated_data)


class BrutedNTLMAccSerializer(serializers.ModelSerializer[BrutedNTLMAcc]):
    class Meta:
        model = BrutedNTLMAcc
        fields = ['pk', 'sam_acc_name', 'acc_password', 'update_time']


class DomainBrutedNTLMAccSerializer(serializers.ModelSerializer[Domain]):
    bruted_ntlm_acc: Any = BrutedNTLMAccSerializer(many=True, read_only=True)

    class Meta:
        model = Domain
        fields = ['pk', 'name', 'hostname', 'base_dn', 'bruted_ntlm_acc']


class NoExpPassAccSerializer(serializers.ModelSerializer[NoExpPassAcc]):
    class Meta:
        model = NoExpPassAcc
        fields = ['pk', 'sam_acc_name', 'create_time']


class DomainNoExpPassAccSerializer(serializers.ModelSerializer[Domain]):
    no_exp_pass_acc: Any = NoExpPassAccSerializer(many=True, read_only=True)

    class Meta:
        model = Domain
        fields = ['pk', 'name', 'hostname', 'base_dn', 'no_exp_pass_acc']


class DomainReusedPassAccSerializer(serializers.ModelSerializer[Domain]):

    class Meta:
        model = Domain
        fields = ['pk', 'name', 'hostname']


class ReusedPassAccSerializer(serializers.ModelSerializer[ReusedPassAcc]):
    domain: Any = DomainReusedPassAccSerializer(read_only=True)
    reused_domain: Any = DomainReusedPassAccSerializer(read_only=True)

    class Meta:
        model = ReusedPassAcc
        fields = ['pk', 'domain', 'sam_acc_name', 'reused_domain', 'reused_sam_acc_name', 'create_time']
