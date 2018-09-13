import os

username = os.environ['USER_NAME']
sources_directory = os.environ['SOURCE_DIRECTORY']
overwrite_flag = True if os.environ['OVERWRITE_FLAG'] == 'true' else False

# print(type(username), username)
# print(type(sources_directory), sources_directory)
# print(type(overwrite_flag), overwrite_flag)

# You shouldn't edit the following
username_url = '/' + username
infoarena_base_url = 'https://infoarena.ro'
infoarena_user_url = 'https://infoarena.ro/utilizator'
infoarena_monitor_url = 'https://infoarena.ro/monitor'

no_login_data = {
    'force_view_source': 'Vezi+sursa'
}


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def ok_green(message):
        return Colors.OKGREEN + str(message) + Colors.ENDC

    @staticmethod
    def ok_blue(message):
        return Colors.OKBLUE + str(message) + Colors.ENDC

    @staticmethod
    def bold(message):
        return Colors.BOLD + str(message) + Colors.ENDC

    @staticmethod
    def warning(message):
        return Colors.WARNING + str(message) + Colors.ENDC
