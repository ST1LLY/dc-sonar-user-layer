"""
Django admin panel settings

Author:
    Konstantin S. (https://github.com/ST1LLY)
"""
# pylint:disable=missing-class-docstring,unsubscriptable-object
# https://github.com/PyCQA/pylint-django/issues/361 (unsubscriptable-object)
from django.contrib import admin

from .models import Domain, BrutedNTLMAcc, NoExpPassAcc, ReusedPassAcc


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin[Domain]):
    list_display = (
        'name',
        'hostname',
        'base_dn',
        'dump_status',
        'brute_status',
        'no_exp_pass_status',
        'reused_pass_status',
    )
    list_filter = ('dump_status', 'brute_status', 'no_exp_pass_status', 'reused_pass_status')

    class Meta:
        ordering = (
            'name',
            'hostname',
            'base_dn',
            'dump_status',
            'brute_status',
            'no_exp_pass_status',
            'reused_pass_status',
        )


@admin.register(BrutedNTLMAcc)
class BrutedNTLMAccsAdmin(admin.ModelAdmin[BrutedNTLMAcc]):
    list_display = ('domain', 'sam_acc_name')

    class Meta:
        ordering = ('domain', 'sam_acc_name')


@admin.register(NoExpPassAcc)
class NoExpPassAccsAdmin(admin.ModelAdmin[NoExpPassAcc]):
    list_display = ('domain', 'sam_acc_name')

    class Meta:
        ordering = ('domain', 'sam_acc_name')


@admin.register(ReusedPassAcc)
class ReusedPassAccsAdmin(admin.ModelAdmin[ReusedPassAcc]):
    list_display = ('domain', 'sam_acc_name', 'reused_domain', 'reused_sam_acc_name')

    class Meta:
        ordering = ('domain', 'sam_acc_name', 'reused_domain', 'reused_sam_acc_name')
