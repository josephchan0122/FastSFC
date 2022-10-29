import boto3
import os

from django.core.management.base import BaseCommand
from django.conf import settings
from app.core.helpers.s3 import S3


class Command(BaseCommand):
    help = ('Clean S3 filetype')

    def add_arguments(self, parser):
        parser.add_argument('-d', '--dry-run', help='Dry run for first 10 objects', required=False, action='store_true')

    def handle(self, *args, **options):
        self.dryrun = options['dry_run']
        self.input_bucket = 'fastsfc'
        self.output_bucket = 'fastsfc'
        self.run_for_all = True

        if self.dryrun:
            print('Replacing s3 filetypes in dry run mode (will only run for first 10 objects and saved to fastsfc-development bucket')
            self.output_bucket = 'fastsfc-development'
            self.run_for_all = False
        else:
            print('Replacing s3 filetypes in production mode')

        client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name='ap-southeast-1'
        )

        s3 = S3()

        def iterate_bucket_items(bucket):
            """
            Generator that iterates over all objects in a given s3 bucket

            See http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.list_objects_v2
            for return data format
            :param bucket: name of s3 bucket
            :return: dict of metadata for an object
            """
            paginator = client.get_paginator('list_objects_v2')
            page_iterator = paginator.paginate(Bucket=bucket)

            for page in page_iterator:
                if page['KeyCount'] > 0:
                    for item in page['Contents']:
                        yield item

        count = 0

        for item in iterate_bucket_items(self.input_bucket):
            try:
                content_type = s3.content_type_from_key(item['Key'])

                print('Copying', item['Key'], content_type)

                client.copy_object(
                    CopySource={
                        'Bucket': self.input_bucket,
                        'Key': item['Key']
                    },
                    ACL='public-read',
                    Bucket=self.output_bucket,
                    ContentType=content_type,
                    Key=item['Key'],
                    MetadataDirective='REPLACE',
                )

                if not self.run_for_all:
                    count += 1

                if count == 10:
                    break
            except:
                import traceback
                traceback.print_exc()

        print('Done')
