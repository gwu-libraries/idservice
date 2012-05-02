from django.core.management.base import BaseCommand, CommandError
from lidapp.models import ID
from optparse import make_option
import logging


class Command(BaseCommand):
    args = '<identifier>'
    help = 'Bind metadata to an identifier'

    option_list = BaseCommand.option_list + (
        make_option('-u', '--url',
                    action='store',
                    dest='object_url',
                    default=None,
                    help='The URL for the object'),
        make_option('-t', '--type',
                    action='store',
                    dest='object_type',
                    default=None,
                    help='The type of object ([i]tem or [c]ollection)'),
        make_option('-d', '--desc',
                    action='store',
                    dest='description',
                    default=None,
                    help='Optional descriptive text field'),
        )

    def handle(self, *args, **options):
        try:
            logger = logging.getLogger('lidapp.actions')
            identifier = args[0]
            id = ID.objects.get(identifier=identifier)
            kwargs = {}
            for opt in options:
                if opt in id.bindable_fields and options[opt] != None:
                    kwargs[opt] = options[opt]
            id.bind(**kwargs)
            logger.info('Action: bind  IP: 127.0.0.1  ID: %s  Result:SUCCESS. Data: %s' % (identifier, kwargs))
            self.stdout.write(id.dump_string() + '\n')
        except ID.DoesNotExist:
            raise CommandError('Identifier "%s" does not exist' % identifier)
        except ID.NoChanges:
            raise CommandError('You did not input any changes to the data')
        except ID.NoData:
            raise CommandError('You did not supply any data to bind.')

