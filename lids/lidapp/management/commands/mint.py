from django.core.management.base import BaseCommand, CommandError
from lidapp.models import ID, Minter, Requester
from optparse import make_option
from django.utils.timezone import now
import logging

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
        logger = logging.getLogger('lidapp.actions')
        try:
            minter_name = args[0]
            minter = Minter.objects.get(name=minter_name)
            requester = Requester.objects.get(ip='127.0.0.1')
        except IndexError:
            raise CommandError('Please specify a minter')
        except Minter.DoesNotExist:
            raise CommandError('Minter "%s" does not exist' % minter_name)
        except Requester.DoesNotExist:
            requester = Requester.objects.create(name='Command Line', date_created=now(),admin=True, ip='127.0.0.1')

        ids = minter.mint(requester=requester, quantity=options['quantity'])

        for x in range(options['quantity']):
            logger.info('Action: mint %s of %s  IP: 127.0.0.1  Result:SUCCESS.  Minted %s' % (x+1, options['quantity'], ids[x].identifier))

        if not options['verbose']:
            output = '\n'.join([id.identifier for id in ids])
            self.stdout.write(output+'\n')
        else:
            for id in ids:
                self.stdout.write(id.dump_string()+'\n')
