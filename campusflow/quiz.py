"""Pure validation and scoring for the engineering quiz."""

from campusflow.quiz_questions import QUESTIONS


def normalize_answer(answer):
    if not isinstance(answer, str):
        raise ValueError("Choose A, B, C or D")

    answer = answer.strip().upper()

    if answer not in ("A", "B", "C", "D"):
        raise ValueError("Choose A, B, C or D")

    return answer


def score_answers(answers, questions=QUESTIONS):
    """Score valid answers without reading user input."""
    if not isinstance(answers, (list, tuple)):
        raise ValueError("Answers must be a sequence")

    if len(answers) != len(questions):
        raise ValueError("Answer count does not match questions")

    score = 0

    for answer, question in zip(answers, questions):
        if normalize_answer(answer) == question["answer"]:
            score += 1

    return score
