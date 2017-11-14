import manuel.capture
import manuel.doctest
import manueltestcase
import os
import unittest

here = os.path.dirname(__file__)
m = manuel.doctest.Manuel() + manuel.capture.Manuel()

class MyTests(unittest.TestCase):

    test1 = manueltestcase.doctestfile(
        m,
        os.path.abspath(os.path.join(here, 'manueltestcase.rst')))

