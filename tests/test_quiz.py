"""Regression tests for the engineering understanding check."""

import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from campusflow.quiz import normalize_answer, score_answers
from campusflow.quiz_cli import run_understanding_check
from main import run_cli


CORRECT = ["B", "C", "B", "D", "A", "C"]


class TestEngineeringQuiz(unittest.TestCase):

    def test_normalization(self):
        self.assertEqual(normalize_answer(" b "), "B")

    def test_invalid_answer_rejected(self):
        for value in ("E", "", "AB", None):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    normalize_answer(value)

    def test_perfect_score(self):
        self.assertEqual(score_answers(CORRECT), 6)

    def test_partial_and_zero_scores(self):
        self.assertEqual(
            score_answers(["B", "A", "B", "A", "A", "A"]), 3
        )
        self.assertEqual(
            score_answers(["A", "A", "A", "A", "B", "A"]), 0
        )

    def test_invalid_answer_count(self):
        with self.assertRaises(ValueError):
            score_answers(["A"])

    def test_invalid_cli_answer_reprompts(self):
        output = StringIO()
        answers = ["Z"] + CORRECT

        with patch("builtins.input", side_effect=answers):
            with redirect_stdout(output):
                score = run_understanding_check()

        self.assertEqual(score, 6)
        self.assertIn("Invalid answer", output.getvalue())
        self.assertIn("Final score: 6/6", output.getvalue())
        self.assertIn("Two concept explanations", output.getvalue())

    def test_quiz_accessible_from_main_menu(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            output = StringIO()

            with patch(
                "builtins.input",
                side_effect=["11"] + CORRECT + ["9"],
            ):
                with redirect_stdout(output):
                    result = run_cli(path)

            self.assertEqual(result, 0)
            self.assertIn("Final score: 6/6", output.getvalue())


if __name__ == "__main__":
    unittest.main()
