# Generated by Django 4.0.5 on 2022-07-12 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_cabinet', '0006_alter_brutedntlmacc_sam_acc_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brutedntlmacc',
            name='domain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bruted_ntlm_acc', to='user_cabinet.domain'),
        ),
        migrations.AlterField(
            model_name='noexppassacc',
            name='domain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='no_exp_pass_acc', to='user_cabinet.domain'),
        ),
        migrations.AlterField(
            model_name='reusedpassacc',
            name='domain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reused_pass_acc', to='user_cabinet.domain'),
        ),
    ]
