import os
import sys


class BaseTestMixin:
    def setUp(self):
        super().setUp()

        self.opened_files = []

    def open_asset(self, filename, mode='rb', encoding=None):
        module_path = os.path.abspath(sys.modules[self.__module__].__file__)
        f = open(os.path.join(os.path.dirname(module_path), 'assets', filename), mode, encoding=encoding)
        self.opened_files.append(f)
        return f

    def tearDown(self):
        super().tearDown()

        for f in self.opened_files:
            if not f.closed:
                f.close()
