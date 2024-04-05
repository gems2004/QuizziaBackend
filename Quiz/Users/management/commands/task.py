from django.core.management.base import BaseCommand
from django.utils import timezone
from Users.models import Teacher


class Command(BaseCommand):

    def handle(self, *args, **options):
        current_date = timezone.now().date()

        teachers_to_check = Teacher.objects.filter(bundle_expiry__isnull=False)

        for teacher in teachers_to_check:
            if teacher.bundle_expiry < current_date:
                teacher.is_subscribed = False
                teacher.fk_bundle_id = 1
                teacher.bundle_expiry = None
                teacher.save()
                self.stdout.write(self.style.SUCCESS(f'Teacher {teacher.fullname} subscription expired.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Teacher {teacher.fullname} subscription is still active.'))
