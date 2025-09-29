from django.core.management.base import BaseCommand
from cashflow.models import Type, Status, Category, SubCategory

class Command(BaseCommand):
    help = "Стартовые данные в бд"

    def handle(self, *args, **options):
        in_type, _ = Type.objects.get_or_create(name="Поступление")
        out_type, _ = Type.objects.get_or_create(name="Списание")

        plan, _ = Status.objects.get_or_create(name="План")
        fact, _ = Status.objects.get_or_create(name="Факт")

        salary, _ = Category.objects.get_or_create(name="Зарплата", type=in_type)
        sales, _ = Category.objects.get_or_create(name="Продажи", type=in_type)
        rent, _ = Category.objects.get_or_create(name="Аренда", type=out_type)
        taxes, _ = Category.objects.get_or_create(name="Налоги", type=out_type)

        SubCategory.objects.get_or_create(name="Оклад", category=salary)
        SubCategory.objects.get_or_create(name="Бонус", category=salary)
        SubCategory.objects.get_or_create(name='Активы', category=sales)
        SubCategory.objects.get_or_create(name="Офис", category=rent)
        SubCategory.objects.get_or_create(name="НДС", category=taxes)

        self.stdout.write(self.style.SUCCESS("Стартовые данные добавлены"))
