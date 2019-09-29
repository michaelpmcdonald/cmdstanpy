import os
import unittest
import json

from cmdstanpy.cmdstan_args import Method, VariationalArgs, CmdStanArgs
from cmdstanpy.utils import EXTENSION
from cmdstanpy.model import Model
from cmdstanpy.stanfit import RunSet, StanVariational
from contextlib import contextmanager
import logging
from multiprocessing import cpu_count
import numpy as np
import sys
from testfixtures import LogCapture

here = os.path.dirname(os.path.abspath(__file__))
datafiles_path = os.path.join(here, 'data')


class StanVariationalTest(unittest.TestCase):
    def test_set_variational_attrs(self):
        stan = os.path.join(datafiles_path, 'variational', 'eta_should_be_big.stan')
        model = Model(stan_file=stan)
        model.compile()
        no_data = {}
        args = VariationalArgs(algorithm='meanfield')
        cmdstan_args = CmdStanArgs(
            model_name=model.name,
            model_exe=model.exe_file,
            chain_ids=None,
            data=no_data,
            method_args=args,
        )
        runset = RunSet(args=cmdstan_args, chains=1)
        vi = StanVariational(runset)

        # check StanVariational.__init__ state
        self.assertEqual(vi._column_names,None)
        self.assertEqual(vi._variational_mean,None)
        self.assertEqual(vi._output_samples,None)

        # process csv file, check attrs
        output = os.path.join(datafiles_path, 'variational', 'eta_big_output.csv')
        vi._set_variational_attrs(output)
        self.assertEqual(vi.column_names,('lp__', 'log_p__', 'log_g__', 'mu.1', 'mu.2'))
        self.assertAlmostEqual(vi.variational_params_dict['mu.1'], 31.0299, places=3)
        self.assertAlmostEqual(vi.variational_params_dict['mu.2'], 28.8141, places=3)
        self.assertEqual(vi.output_samples().shape, (1000, 5))


class VariationalTest(unittest.TestCase):
    def test_variational_good(self):
        stan = os.path.join(datafiles_path, 'variational', 'eta_should_be_big.stan')
        model = Model(stan_file=stan)
        model.compile()
        no_data = {}
        vi = model.variational()
        self.assertTrue(True)
        # test numpy output
        # test pandas output
        # test dict output
        # test sample



if __name__ == '__main__':
    unittest.main()
