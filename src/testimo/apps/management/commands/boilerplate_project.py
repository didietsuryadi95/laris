import json
import os

from django.core.management import BaseCommand
from django.conf import settings
from humanize import naturaltime
from shutil import copyfile
from datetime import timedelta, datetime
from django.utils.timezone import now
from django.utils import timezone


class Command(BaseCommand):
    help = "Running Boilerplate"
    app_name = getattr(settings, 'APP_NAME')

    def add_arguments(self, parser):
        parser.add_argument(
            '--config',
            help='config file with json format',
        )

    def get_current_settings_var(self, variable):
        return getattr(settings, variable, None)

    def get_old_value(self, field):
        data = {
            'app_name': self.app_name,
            'domain_name': self.get_current_settings_var('META_SITE_DOMAIN'),
            'shop_name': self.get_current_settings_var('OSCAR_SHOP_NAME'),
            'shop_tag_line': self.get_current_settings_var('OSCAR_SHOP_TAGLINE'),
            'prefix': self.get_current_settings_var('env_prefix'),
            'description': self.get_current_settings_var('SITE_DESCRIPTION'),
            'order_number_prefix': self.get_current_settings_var('ORDER_NUMBER_PREFIX'),
            'name': self.get_current_settings_var('SHIPPING_SENDER')['name'],
            'mobile': self.get_current_settings_var('PARTNER_PHONE_NUMBER'),
            'email': self.get_current_settings_var('PARTNER_EMAIL'),
            'address': self.get_current_settings_var('SHIPPING_ORIGIN')['address'],
            'city': self.get_current_settings_var('SHIPPING_ORIGIN')['city'],
            'state': self.get_current_settings_var('SHIPPING_ORIGIN')['state'],
            'country': self.get_current_settings_var('SHIPPING_ORIGIN')['country'],
            'postcode': self.get_current_settings_var('SHIPPING_ORIGIN')['postcode'],
            'instagram': self.get_current_settings_var('SOCIAL_INSTAGRAM'),
            'facebook': self.get_current_settings_var('SOCIAL_FACEBOOK'),
            'twitter': self.get_current_settings_var('SOCIAL_TWITTER'),
            'youtube': self.get_current_settings_var('SOCIAL_YOUTUBE'),
            #style
            'primary': '#1E1E1E',
            'accent': '#1E1E1E',
            'notice': '#FA3C50',
            'success': '#32AA6E',
            'alert': '#F4D143',
            'error': '#FA3C50',
            'black': '#1E1E1E',
            'grey': '#828282',
            'white': '#FFFFFF',
            'light-grey': '#DCDCDC',
            'primary-dark': '#1E1E1E',
            #font
            'primary_font_name': 'Thasadith',
            'primary_font_var': 'thasadith',
            'secondary_font_name': 'Sarabun',
            'secondary_font_var': 'sarabun',
            'font_light_size': 300,
            'font_reguler_size': 400,
            'font_medium_size': 500,
            'font_bold_size': 'bold'

        }
        return data.get(field, None)

    def get_target(self, kind):
        import os
        from functools import reduce
        templates_dir = []
        for root, dirs, files in os.walk("templates/"):
            for filename in files:
                templates_dir.append(os.path.join(root, filename))

        files = {
            'settings': [self.app_name + i for i in ['/settings.py', '/wsgi.py']]
            + ['manage.py', 'run_celery'] + ['../../' + i for i in ['docker-compose.yml', 'setup.py', 'setup.cfg',
                                                                    'Vagrantfile']],
            'folder': ['./', '../', '../../solr-core/', '../../../'],
            'style': ['staticfiles/less/components/' + i for i in ['colors.less', 'font-face.less', 'typography.less',
                                                                   'variables.less']],
            'html': templates_dir,
            'image': 'staticfiles/img/',
            'config': ['./apps/management/commands/boilerplate_project.py']
        }
        return reduce(lambda x, y: x+y, [files[k] for k in kind])

    @staticmethod
    def replace_in_files(old_value, new_value, files):
        if old_value is None:
            return False
        if old_value == new_value:
            return True
        for f in files:
            with open(f, 'r') as file:
                filedata = file.read()
            filedata = filedata.replace(old_value, new_value)
            with open(f, 'w') as file:
                file.write(filedata)
        return True

    @staticmethod
    def change_folder_name(old_name, new_name, folders):
        if old_name == new_name:
            return True
        for f in folders:
            os.rename(f + old_name, f + new_name)
        return True

    @staticmethod
    def copy_file_from(local_dir, current_dir):
        for root, dirs, files in os.walk(local_dir):
            for file in files:
                for root_target, dirs_target, files_target in os.walk(current_dir):
                    for target in files_target:
                        if file.endswith(target):
                            copyfile(os.path.join(root, file), os.path.join(root_target, target))
        return True

    def processing(self, action, new_value, variable, kind_file):
        filtered_file = [k for k in kind_file if k != 'folder']
        if 'replace_files' in action:
            self.replace_in_files(self.get_old_value(variable), new_value, self.get_target(filtered_file))
        if 'change_folder_name' in action:
            self.change_folder_name(self.get_old_value(variable), new_value, self.get_target(['folder']))
        if 'copy_files' in action:
            self.copy_file_from(new_value, self.get_target(['image']))

    def handle(self, *args, **options):
        start = timezone.now()
        with open('../../fixtures/config.json', encoding='utf-8') as config:
            variables = json.loads(config.read())

        total_variable = len(variables)
        self.stdout.write(f'Initiate {total_variable} variables to be executed')

        starting_time = now()

        for idx, variable in enumerate(variables):
            self.processing(variable.get('action'), variable.get('value'),
                            variable.get('variable'), variable.get('target'))
            self.report_progress(idx, total_variable, starting_time)

        end = timezone.now()
        self.stdout.write(
            f"DONE, Address data already dumped into database. It took {(end - start).seconds} SECONDS")

    def report_progress(self, iteration: int, total: int, starting_time: datetime):
        bar_size = 20
        percent = "{0:.1f}".format(100 * (iteration / float(total)))
        filled_length = int(bar_size * iteration // total)
        bar = '█' * filled_length + '-' * (bar_size - filled_length)

        runtime = ''
        if starting_time:
            runtime = naturaltime(now() - starting_time)

        ending_time = ''
        if starting_time:
            seconds_from_start = (now() - starting_time).total_seconds()
            per_second = int(iteration / seconds_from_start)
            try:
                ending_time = naturaltime(timedelta(seconds=(-1 * ((total - iteration) / per_second))))
            except (TypeError, ZeroDivisionError):
                ending_time = '???'

        self.stdout.write(
            self.style.SUCCESS(
                f'\r |{bar}| {percent}% (Executed Rate: {per_second}/s) [Started: {runtime} - Done: {ending_time}]'),
            ending="\r"
        )

        # Print New Line on Complete
        if iteration == total:
            self.stdout.write('\n')



