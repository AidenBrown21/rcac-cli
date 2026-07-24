# -*- coding: utf-8 -*-
"""Tests for RCAC CLI REPL functionality"""
import builtins
import unittest
from unittest import mock

from rcac_cli.main import run_repl

class TestReplExit(unittest.TestCase):
    @mock.patch("rcac_cli.main.ensure_api_key")
    @mock.patch.object(builtins, 'input', side_effect=['exit'])
    def test_repl_exits_on_exit_command(self, mock_input, mock_ensure_api_key):
        run_repl()
        self.assertTrue(mock_input.called)

if __name__ == '__main__':
    unittest.main()
