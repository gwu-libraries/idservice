from django.core.management.base import BaseCommand, CommandError
from lidapp.models import ID


class Command(BaseCommand):
    args = '<identifier>'
    help = 'Get metadata for an identifier'

    def handle(self, *args, **options):
        identifier = args[0]
        try:
            id = ID.objects.get(identifier=identifier)
        except ID.DoesNotExist:
            raise CommandError('Identifier "%s" does not exist' % identifier)

        self.stdout.write(id.dump_string() + '\n')
