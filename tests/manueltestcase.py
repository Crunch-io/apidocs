import doctest
import manuel
import manuel.testing
import os
import re
import types

def doctestfile(m, path, optionflags=0, checker=None):
    with open(path) as f:
        test = f.read()
    name = os.path.basename(path)

    def test_file(self):
        if isinstance(self, types.FunctionType):
            setup = self
            def test_file_w_setup(self):
                setup(self)
                _run_test(self, m, test, {}, name, path, optionflags, checker,
                          'test')
            test_file_w_setup.__name__ = _testify(setup.__name__)
            test_file_w_setup.filepath = path
            test_file_w_setup.filename = os.path.basename(path)
            return test_file_w_setup

        _run_test(self, m, test, {}, name, path, optionflags, checker, 'test')

    test_file.__name__ = name_from_path(path)
    test_file.filepath = path
    test_file.filename = os.path.basename(path)

    return test_file




_not_word = re.compile(r'\W')

def name_from_path(path):
    return _testify(
        _not_word.sub('_', os.path.splitext(os.path.basename(path))[0])
        )


def _testify(name):
    if not name.startswith('test'):
        name = 'test_' + name
    return name


def _run_test(self, m, test, globs, name, path,
              optionflags, checker, testname='self', lineno=0):
    globs.update(getattr(self, 'globs', ()))
    globs[testname] = self
    optionflags |= doctest.IGNORE_EXCEPTION_DETAIL
    document = manuel.Document(test, location=path)
    document.parse_with(m)
    [regions] = manuel.testing.group_regions_by_test_case(document)
    manuel.testing.TestCase(m, regions, globs).runTest()
