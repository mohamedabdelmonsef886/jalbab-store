"""
زرع التصنيفات الثلاثة الأساسية في قاعدة البيانات.
الاستخدام: python manage.py seed_categories
"""
from django.core.management.base import BaseCommand
from store.models import Category


class Command(BaseCommand):
    help = "إنشاء التصنيفات الأساسية (نقاب، عبايات، طرح)"

    def handle(self, *args, **options):
        categories = [
            {
                'name': 'نقاب',
                'slug': 'nqab',
                'description': 'نقابات بأقمشة فاخرة وتصاميم أنيقة.'
            },
            {
                'name': 'عبايات',
                'slug': 'abayat',
                'description': 'عبايات عصرية ورسمية بلمسة إسلامية.'
            },
            {
                'name': 'طرح',
                'slug': 'tarh',
                'description': 'طرح بألوان وأقمشة متنوعة تناسب كل الأذواق.'
            },
        ]

        created_count = 0
        updated_count = 0

        for cat in categories:
            obj, created = Category.objects.get_or_create(
                name=cat['name'],
                defaults={
                    'slug': cat['slug'],
                    'description': cat['description'],
                }
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f"✓ تم إنشاء التصنيف: {obj.name} (slug: {obj.slug})"
                ))
            else:
                # لو موجود، نحدّث الـ slug لو كان عربي
                has_arabic = any('\u0600' <= c <= '\u06FF' for c in obj.slug)
                if has_arabic or obj.slug != cat['slug']:
                    old_slug = obj.slug
                    obj.slug = cat['slug']
                    obj.save()
                    updated_count += 1
                    self.stdout.write(self.style.WARNING(
                        f"• تم تحديث slug: {obj.name} ({old_slug} → {obj.slug})"
                    ))
                else:
                    self.stdout.write(self.style.WARNING(
                        f"• التصنيف موجود بالفعل: {obj.name} ({obj.slug})"
                    ))

        self.stdout.write(self.style.SUCCESS(
            f"\nاكتمل! تم إنشاء {created_count} تصنيف جديد، وتحديث {updated_count}."
        ))