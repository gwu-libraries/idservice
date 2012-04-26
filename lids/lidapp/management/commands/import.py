from django.core.management.base import BaseCommand, CommandError
from lidapp.models import ID, Minter, Requester
from lids import settings
from optparse import make_option
from django.utils.timezone import now
from datetime import datetime
import csv


class Command(BaseCommand):
    args = '<file path>'
    help = '''Import identifiers from a csv file.
The first line of the csv file must contain the field names.
The fields must use the following names:
 - identifier
 - id_type ("ark", "handle", etc.) (currently only accepts "ark")
 - date_created
 - minter_name (defaults to "legacy")
 - requester_name (defaults to "legacy")
 - object_url
 - object_type ("item" or "collection", defaults to item)
 - description'''

    def _get_id_type_char(self, id_name):
        for pair in settings.ID_TYPES:
            if id_name == pair[1]:
                return pair[0]

    def _get_object_type_char(self, object_name):
        for pair in settings.OBJECT_TYPES:
            if object_name == pair[1]:
                return pair[0]

    def handle(self, *args, **options):
        try:
            f = open(args[0],'rb')
        except IndexError:
            raise CommandError('Please specify a csv file to read')
        reader = csv.DictReader(f)
        
        count, success, fail = 1,0,0
        for row in reader:
            # convert types to character codes
            id_type = self._get_id_type_char(row['id_type'])
            object_type = self._get_object_type_char(row['object_type'])
            # convert string timestamp, avoiding nulls
            timestamp = row['date_created']
            if timestamp == '0000-00-00 00:00:00':
                timestamp = '0000-01-01 00:00:01'
            try:
                fmt = '%Y-%m-%d %H:%M:%S'
                date_created = datetime.strptime(timestamp,fmt)
            except Exception:
                date_created = now()
            # get minter object - create legacy minter if necessary
            minter_name = row['minter_name'] if row['minter_name'] else 'legacy'
            try:
                minter = Minter.objects.get(name=minter_name)
            except Minter.DoesNotExist:
                minter = Minter.objects.create(name=minter_name,
                                               authority_number='unknown',
                                               prefix='unknown',
                                               template='unkown',
                                               minter_type=id_type,
                                               date_created=now(),
                                               description='A legacy place holder created on import. Not for current use')
            # get requester object - create legacy requester if necessary
            requester_name = row['requester_name'] if row['requester_name'] else 'legacy'
            try:
                requester = Requester.objects.get(name=requester_name)
            except Requester.DoesNotExist:
                requester = Requester.objects.create(name=requester_name,
                                                     organization='',
                                                     date_created = now(),
                                                     description = 'A legacy place holder created on import. Not for current use')
            # finally, create the new object
            try:
                id = ID.objects.create(identifier=row['identifier'],
                                       id_type=id_type,
                                       date_created=date_created,
                                       minter=minter,
                                       requester=requester,
                                       object_url=row['object_url'],
                                       object_type=object_type,
                                       description=row['description'],
                                       date_updated=now())
                success += 1
                self.stdout.write('%s Successfully import ID: %s\n' % (count, row['identifier']))
            except IntegrityError:
                fail += 1
                self.stdout.write('%s ID %s already exists in database. Skipping...\n' % (count, row['identifier']))

        self.stdout.write('Import process completed. %s Items successfully imported. %s Failed.\n' % (success, fail))
