import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Field, Category

if Field.objects.count() == 0:
    f1 = Field.objects.create(name="Software Engineering")
    f2 = Field.objects.create(name="Data Science")
    f3 = Field.objects.create(name="Web Development")

    Category.objects.create(name="DSA", field=f1)
    Category.objects.create(name="System Design", field=f1)
    Category.objects.create(name="Machine Learning", field=f2)
    Category.objects.create(name="Python", field=f2)
    Category.objects.create(name="React", field=f3)
    Category.objects.create(name="Django", field=f3)

    print("✅ Data added!")
else:
    print("✅ Data already exists!")