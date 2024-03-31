from django.core.management.base import BaseCommand
from django.utils import timezone
from your_app.models import Teacher


class Command(BaseCommand):

    def handle(self, *args, **options):
        current_date = timezone.now().date()

        # Get all teachers with non-null bundle_expiry
        teachers_to_check = Teacher.objects.filter(bundle_expiry__isnull=False)

        for teacher in teachers_to_check:
            if teacher.bundle_expiry < current_date:
                teacher.is_subscribed = False
                teacher.fk_bundle = 1
                teacher.save()
                self.stdout.write(self.style.SUCCESS(f'Teacher {teacher.fullname} subscription expired.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Teacher {teacher.fullname} subscription is still active.'))