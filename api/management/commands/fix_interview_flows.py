from django.core.management.base import BaseCommand
from api.models import InterviewFlow, Category, Field

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        field = Field.objects.get(id=1)
        categories = Category.objects.all()
        
        for cat in categories:
            existing = InterviewFlow.objects.filter(
                field=field, category=cat
            ).count()
            
            if existing < 4:
                for step in range(existing + 1, 5):
                    InterviewFlow.objects.get_or_create(
                        field=field,
                        category=cat,
                        step_order=step
                    )
                self.stdout.write(f"Fixed: {cat.name} → 4 steps")
        
        self.stdout.write("Done!")