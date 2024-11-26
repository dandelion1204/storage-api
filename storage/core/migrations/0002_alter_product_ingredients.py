# Generated by Django 3.2.11 on 2024-11-15 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='ingredients',
            field=models.ManyToManyField(related_query_name='product_ingredients', through='core.ProductIngredients', to='core.Ingredient'),
        ),
    ]