"""Interactive engineering understanding check."""

from campusflow.quiz import normalize_answer, score_answers
from campusflow.quiz_questions import QUESTIONS


def ask_answer():
    while True:
        try:
            return normalize_answer(input("Your answer (A/B/C/D): "))
        except ValueError:
            print("Invalid answer. Choose A, B, C or D.")


def run_understanding_check():
    print("\n--- Engineering Understanding Check ---")
    print("Answer all six questions.")

    answers = []

    for number, question in enumerate(QUESTIONS, start=1):
        print(f"\nQuestion {number}: {question['question']}")

        for letter, option in question["options"].items():
            print(f"  {letter}. {option}")

        answers.append(ask_answer())

    score = score_answers(answers)
    print(f"\nFinal score: {score}/6")

    print("\nTwo concept explanations:")
    for index in (0, 5):
        question = QUESTIONS[index]
        print(
            f"Question {index + 1} — "
            f"Correct answer: {question['answer']}"
        )
        print(question["explanation"])

    return score
