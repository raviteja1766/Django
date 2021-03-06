# Generated by Django 3.0 on 2020-04-07 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fb_post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='commented_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='posted_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='posted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='fb_post.User'),
        ),
        migrations.AlterField(
            model_name='reaction',
            name='reacted_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='reaction',
            name='reacted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fb_post.User'),
        ),
    ]
