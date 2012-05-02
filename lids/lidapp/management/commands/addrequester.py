from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now
from django.db.utils import IntegrityError
from lidapp.models import Requester
from optparse import make_option
import logging


class Command(BaseCommand):
    args = '<name> <IP address>'
    help = 'Create a new requester'

    option_list = BaseCommand.option_list + (
        make_option('-o', '--organization',
                    action='store',
                    dest='organization',
                    default='',
                    help='The organization the requester belongs to'),
        make_option('-a', '--admin',
                    action='store_true',
                    dest='admin',
                    default=False,
                    help='The requester has rights to edit any identifier'),
        make_option('-d', '--description',
                    action='store',
                    dest='description',
                    default='',
                    help='Optional description of the requester'),
        )

    def handle(self, *args, **options):
        try:
            name = args[0]
            ip = args[1]
            requester = Requester.objects.create(name = name, ip = ip,
                                                 organization = options['organization'],
                                                 admin = options['admin'],
                                                 description = options['description'],
                                                 date_created = now())
            logger = logging.getLogger('lidapp.actions')
            logger.info('Action: addrequester  IP: 127.0.0.1  Requester: %s  IP: %s  Result:SUCCESS  Data: %s' % (name, ip, options))
            self.stdout.write('Requester successfully created\n' + requester.dump_string())
        except IndexError:
            raise CommandError('Please supply the required arguments: <name> <IP address>')
        except IntegrityError:
            raise CommandError('A requester with that name or IP already exists')
