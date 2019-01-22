"""
Entrypoint for the BrewBlox menu
"""

import platform
from abc import ABC, abstractmethod
from subprocess import STDOUT, CalledProcessError, check_call


def is_pi():
    return platform.machine().startswith('arm')


class Command(ABC):
    def __init__(self, description, keywords):
        self.description = description
        self.keywords = keywords

    def __str__(self):
        return '{} ({}) :: {}'.format(self.keywords[0], ', '.join(self.keywords[1:]), self.description)

    def announce(self, shell_cmds):
        print('The following shell commands will be used: \n')
        for cmd in shell_cmds:
            print('\t', cmd)
        print('')
        input('Press ENTER to continue, Ctrl+C to cancel')

    def run(self, shell_cmd):
        print('\n' + 'Running command: \n\t', shell_cmd, '\n')
        return check_call(shell_cmd, shell=True, stderr=STDOUT)

    def run_all(self, shell_cmds, announce=True):
        if announce:
            self.announce(shell_cmds)
        return [self.run(cmd) for cmd in shell_cmds]

    @abstractmethod
    def action(self):
        pass


class ExitCommand(Command):
    def __init__(self):
        super().__init__('Exit this menu', ['exit', 'x'],)

    def action(self):
        raise SystemExit


class ComposeDownCommand(Command):
    def __init__(self):
        super().__init__('Stop running services', ['down', 'd'])

    def action(self):
        cmd = 'docker-compose stop'
        self.run_all([cmd])


class ComposeUpCommand(Command):
    def __init__(self):
        super().__init__('Start all services if not running', ['up', 'u'])

    def action(self):
        cmd = 'docker-compose up -d'
        self.run_all([cmd])


class ComposeUpdateCommand(Command):
    def __init__(self):
        super().__init__('Update all services', ['update', 'p'])

    def action(self):
        shell_commands = [
            'docker-compose down',
            'docker-compose pull',
            'docker-compose up -d',
        ]
        self.run_all(shell_commands)


class SetupCommand(Command):
    def __init__(self):
        super().__init__('Run first-time setup', ['setup', 'e'])

    def action(self):
        host = 'https://localhost/datastore'
        database = 'brewblox-ui-store'
        modules = ['services', 'dashboards', 'dashboard-items']

        shell_commands = [
            'docker-compose down',
            'docker-compose pull',
            'sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 ' +
            '-keyout traefik/brewblox.key ' +
            '-out traefik/brewblox.crt',
            'sudo chmod 644 traefik/brewblox.crt',
            'sudo chmod 600 traefik/brewblox.key',
            'docker-compose up -d datastore traefik',
            'sleep 5',
            'curl -Sk -X GET --retry 10 --retry-delay 5 {} > /dev/null'.format(host),
            'curl -Sk -X PUT {}/_users'.format(host),
            'curl -Sk -X PUT {}/{}'.format(host, database),
            *[
                'cat presets/{}.json '.format(mod) +
                '| curl -Sk -X POST ' +
                '--header \'Content-Type: application/json\' ' +
                '--header \'Accept: application/json\' ' +
                '--data "@-" {}/{}/_bulk_docs'.format(host, database)
                for mod in modules
            ],
            'docker-compose down',
        ]
        self.run_all(shell_commands)


class FirmwareFlashCommand(Command):
    def __init__(self):
        super().__init__('Flash firmware on Spark', ['flash', 'f'])

    def action(self):
        tag = 'rpi-develop' if is_pi() else 'develop'
        shell_commands = [
            'docker-compose down',
            'docker pull brewblox/firmware-flasher:{}'.format(tag),
            'docker run -it --rm --privileged brewblox/firmware-flasher:{} trigger-dfu'.format(tag),
            'sleep 2',
            'docker run -it --rm --privileged brewblox/firmware-flasher:{} flash'.format(tag),
            'sleep 5',
            'docker run -it --rm --privileged brewblox/firmware-flasher:{} flash-bootloader'.format(tag),
        ]

        input('Please press ENTER when your Spark is connected over USB')
        self.run_all(shell_commands)


class CheckStatusCommand(Command):
    def __init__(self):
        super().__init__('Check system status', ['status', 'a'])

    def action(self):
        cmd = 'docker-compose ps'
        self.run_all([cmd])


MENU = """
-----------------------------
{}
-----------------------------

Press Ctrl+C to exit.
"""


def main():
    all_commands = [
        ComposeUpCommand(),
        ComposeDownCommand(),
        ComposeUpdateCommand(),
        SetupCommand(),
        FirmwareFlashCommand(),
        CheckStatusCommand(),
        ExitCommand(),
    ]
    command_descriptions = [
        '{} - {}'.format(idx+1, cmd)
        for idx, cmd in enumerate(all_commands)
    ]

    print('Welcome to the BrewBlox menu!')

    try:
        while True:
            print(MENU.format('\n'.join(command_descriptions)))
            arg = input('Please type a command name or index, and press ENTER. ')

            command = next(
                (cmd for idx, cmd in enumerate(all_commands) if arg in cmd.keywords + [str(idx+1)]),
                None,
            )

            if command:
                command.action()
                break

    except CalledProcessError as ex:
        print('\n' + 'Error:', str(ex))

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
