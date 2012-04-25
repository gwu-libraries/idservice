from django.core.management.base import BaseCommand, CommandError
from lidapp.models import ID, Minter, Requester
from optparse import make_option
from datetime import datetime

class Command(BaseCommand):
    args = '<minter_name>'
    help = 'Mints new identifiers'

    option_list = BaseCommand.option_list + (
        make_option('-q', '--quantity',
                    action='store',
                    type = 'int',
                    dest='quantity',
                    default=1,
                    help='The number of identifiers to create'),
        make_option('-d', '--display-metadata',
                    action='store_true',
                    dest='verbose',
                    default=False,
                    help='Display all metadata for each identifier'),
        )

    def handle(self, *args, **options):
        try:
            minter_name = args[0]
        except IndexError:
            raise CommandError('Please specify a minter')
        try:
            minter = Minter.objects.get(name=minter_name)
        except Minter.DoesNotExist:
            raise CommandError('Minter "%s" does not exist' % minter_name)
        try:
            requester = Requester.objects.get(name='CommandLine')
        except Requester.DoesNotExist:
            requester = Requester.objects.create(name='CommandLine', date_created=datetime.now())

        ids = minter.mint(requester=requester, quantity=options['quantity'])

        if not options['verbose']:
            output = '\n'.join([id.identifier for id in ids])
            self.stdout.write(output+'\n')
        else:
            for id in ids:
                self.stdout.write(id.dump_string()+'\n')
