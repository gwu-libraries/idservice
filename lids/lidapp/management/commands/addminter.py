from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now
from django.db.utils import IntegrityError
from lidapp.models import Minter
from optparse import make_option
from lids import settings
import logging


class Command(BaseCommand):
    args = '<name> <type>'
    help = 'Create a new minter'

    option_list = BaseCommand.option_list + (
        make_option('-a', '--authority-number',
                    action='store',
                    dest='authority_number',
                    default='',
                    help='The assigned institutional number (such as an ARK NAAN)'),
        make_option('-p', '--prefix',
                    action='store',
                    dest='prefix',
                    default='',
                    help='Characters to prepend to every identifier minted'),
        make_option('-t', '--template',
                    action='store',
                    dest='template',
                    default='',
                    help='The format of the identifier string'),
        make_option('-i', '--inactive',
                    action='store_false',
                    dest='active',
                    default=True,
                    help='Make the new minter inactive (for legacy minters)'),
        make_option('-d', '--description',
                    action='store',
                    dest='description',
                    default='',
                    help='Optional description of the minter'),
        )

    def handle(self, *args, **options):
        try:
            name = args[0]
            minter_type = args[1][0]
            if minter_type not in [pair[0] for pair in settings.ID_TYPES]:
                raise CommandError('That ID type is not available.')
            logger = logging.getLogger('lidapp.actions')
            minter = Minter.objects.create(name = name,
                                   minter_type = minter_type,
                                   authority_number = options['authority_number'],
                                   prefix = options['prefix'],
                                   template = options['template'],
                                   date_created = now(),
                                   active = options['active'],
                                   description = options['description'])
            logger.info('Action: addminter  IP: 127.0.0.1  Minter: %s  Type: %s  Result:SUCCESS. Data: %s' % (name, minter_type, options))
            self.stdout.write('Minter successfully created!\n' + minter.dump_string())
        except IndexError:
            raise CommandError('Please supply the required arguments: <name> <type>')
        except IntegrityError:
            raise CommandError('A minter by that name already exists')
