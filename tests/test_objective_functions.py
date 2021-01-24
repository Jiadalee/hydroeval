import unittest
import numpy

import hydroeval


# two randomly generated series
_sim = numpy.array(
    [4.88322951, 13.00581834, 7.02440554, 3.97091122, 9.97534342,
     10.33979266, 10.66188354, 5.02212142, 10.11439072, 8.74766372,
     2.00477724, 15.77613262, 13.60435174, 11.03978688, 12.48102837,
     15.73067134, 1.5596135, 16.38242713, 12.43641555, 18.51378375,
     15.79254569, 18.23969688, 10.9313429, 19.71969387, 10.93025247,
     14.84931417, 5.46188619, 9.94941719, 1.9727649, 15.94516433,
     10.3383131, 3.59512995, 7.0910027, 13.13433473, 3.67594266,
     17.67672078, 1.86348799, 11.59849535, 10.21208572, 16.95266279,
     14.43738518, 6.30404177, 8.64896434, 9.11393758, 4.1732255,
     9.72432999, 7.34643289, 9.14102392, 14.99222829, 11.27481394]
)

_obs = numpy.array(
    [4.12163019, 18.36232758, 8.01263988, 10.77006985, 19.63840808,
     13.38709782, 19.64878261, 1.46967891, 2.94507986, 18.66989149,
     10.94374588, 12.84710497, 2.16565322, 10.52564014, 14.51876746,
     10.47721219, 19.94729036, 2.61103336, 3.26042311, 16.74206836,
     9.13145529, 1.64976642, 14.06612306, 18.83125766, 18.10650122,
     18.73195666, 11.94963858, 10.67992664, 9.41582541, 7.9814575,
     8.95723473, 4.85209156, 2.17512672, 8.16731153, 3.62260147,
     14.70382033, 7.79189021, 8.30683168, 4.06517918, 16.01770834,
     15.10669104, 5.94213565, 14.7101872, 5.4553562, 11.66817334,
     2.93192041, 18.17779718, 2.75021921, 10.7884185, 5.45776009]
)


class TestObjectiveFunctions(unittest.TestCase):

    sim = numpy.array([_sim, _obs]).T
    obs = numpy.array([_obs]).T

    expected = {
        'nse': [-0.4147181744134911, 1.],
        'kge': [[0.15369876412650862, 1.], [0.16987016624040058, 1.],
                [0.8356487288365464, 1.], [1.009944878592298, 1.]],
        'kgeprime': [[0.15206235432502702, 1.], [0.16987016624040058, 1.],
                     [0.8274201360388176, 1.], [1.009944878592298, 1.]],
        'kgenp': [[0.14584322654661874, 1.], [0.14756302521008402, 1.],
                  [0.9467449811089002, 1.], [1.009944878592298, 1.]],
        'rmse': [6.86371794420358, 0.],
        'mare': [0.5368739065131718, 0.],
        'pbias': [-0.9944878592297871, 0.],
        'nse_c2m': [-0.17174599454622552, 1.],
        'kge_c2m': [0.0832468511314153, 1.],
        'kgeprime_c2m': [0.0822876002774894, 1.],
        'kgenp_c2m': [0.07865744074865072, 1.]
    }

    def test_each_function(self):
        for obj_fn in self.expected.keys():
            with self.subTest(objective_function=obj_fn):
                numpy.testing.assert_almost_equal(
                    getattr(hydroeval, obj_fn)(self.sim, self.obs),
                    self.expected[obj_fn]
                )


if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()

    test_suite.addTests(
        test_loader.loadTestsFromTestCase(TestObjectiveFunctions))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)
