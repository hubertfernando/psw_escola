# Generated by Django 5.2.4 on 2025-07-23 15:08

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nome', models.CharField(max_length=100)),
                ('telefone', models.CharField(max_length=100)),
                ('matricula', models.CharField(max_length=20, unique=True)),
                ('ingresso_sistema', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'alunos_alunos',
                'permissions': [('detail_aluno', 'Detalha o aluno')],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
