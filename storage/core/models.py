from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import MinValueValidator

# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Product(models.Model):
    title = models.CharField(max_length=255)
    item_num = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class ProductLot(models.Model):
    product = models.ForeignKey(    Product,
                                    on_delete=models.CASCADE,
                                    related_name='lots')
    lot = models.CharField(max_length=100, unique=True)
    quantity = models.IntegerField()


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    item_num = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class IngredientLot(models.Model):
    ingredient = models.ForeignKey( Ingredient,
                                    on_delete=models.CASCADE,
                                    related_name='lots')
    lot = models.CharField(max_length=100, unique=True)
    quantity = models.IntegerField()
    supplier = models.CharField(max_length=255)


class ProductIngredients(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient , on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=6, decimal_places=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.product.title} - {self.ingredient.name}: {self.quantity}"


