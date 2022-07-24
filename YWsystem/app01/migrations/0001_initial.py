# Generated by Django 2.1 on 2019-05-06 01:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_ip', models.CharField(max_length=32)),
                ('server_type', models.CharField(max_length=128)),
                ('server_os_type', models.CharField(max_length=128)),
                ('server_to_app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='app_to_server', to='app01.Application')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='YWUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('phone', models.CharField(max_length=32)),
                ('email', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='host',
            name='server_to_yw_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='yw_user_to_server', to='app01.YWUser'),
        ),
    ]