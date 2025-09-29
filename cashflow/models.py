from django.core.exceptions import ValidationError
from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.name}'

class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        unique_together = ('name', 'type')

    def __str__(self):
        return f'{self.name} {self.type}'

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    class Meta:
        unique_together = ('name', 'category')

    def __str__(self):
        return f'{self.name} {self.category}'

class CashFlow(models.Model):
    date = models.DateField()
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, null=True, blank=True)

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        errors = {}
        if self.amount is not None and self.amount <= 0:
            errors["amount"] = "Сумма должна быть больше 0."

        if self.category and self.type and self.category.type_id != self.type_id:
            errors["category"] = "Категория должна относиться к выбранному типу."

        if self.subcategory and self.category and self.subcategory.category_id != self.category_id:
            errors["subcategory"] = "Подкатегория должна относиться к выбранной категории."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} {self.type} {self.category}/{self.subcategory or '-'} {self.amount}"