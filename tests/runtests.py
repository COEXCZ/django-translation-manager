import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
test_dir = os.path.dirname(__file__)
sys.path.insert(0, test_dir)


def run_tests():
    import django
    from django.test.utils import get_runner
    from django.conf import settings

    django.setup()
    test_runner = get_runner(settings)()
    failures = test_runner.run_tests(["tests"])
    sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests()