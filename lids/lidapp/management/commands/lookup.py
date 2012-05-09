from django.core.management.base import BaseCommand, CommandError
from lidapp.models import ID
import logging


class Command(BaseCommand):
    args = '<identifier>'
    help = 'Get metadata for an identifier'

    def handle(self, *args, **options):
        logger = logging.getLogger('lidapp.actions')
        identifier = args[0]
        try:
            id_obj = ID.objects.get(identifier=identifier)
        except ID.DoesNotExist:
            raise CommandError('Identifier "%s" does not exist' % identifier)

        logger.info('Action: lookup  IP: 127.0.0.1  ID: %s  Result:SUCCESS.' % identifier)
        self.stdout.write(id_obj.dump_string() + '\n')
