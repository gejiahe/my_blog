# Generated by Django 2.1 on 2020-11-08 04:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_auto_20201108_0859'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleColumn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='articlepost',
            name='column',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='article', to='article.ArticleColumn'),
        ),
    ]
