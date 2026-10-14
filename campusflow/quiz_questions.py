"""Engineering understanding question bank."""

QUESTIONS = [
    {
        "question": "Why validate a ticket before changing it?",
        "options": {
            "A": "To make the program faster",
            "B": "To prevent invalid changes",
            "C": "To delete old tickets",
            "D": "To skip testing",
        },
        "answer": "B",
        "explanation": "Validation prevents bad inputs from changing valid data.",
    },
    {
        "question": "How should combined search filters work?",
        "options": {
            "A": "Match any one filter",
            "B": "Ignore all filters",
            "C": "Match every supplied filter",
            "D": "Modify matching tickets",
        },
        "answer": "C",
        "explanation": "AND filtering requires every supplied condition to match.",
    },
    {
        "question": "What should read-only search preserve?",
        "options": {
            "A": "Only ticket IDs",
            "B": "Original ticket data",
            "C": "Only resolved tickets",
            "D": "Only priority values",
        },
        "answer": "B",
        "explanation": "Searching must not mutate stored tickets.",
    },
    {
        "question": "Why run regression tests?",
        "options": {
            "A": "To remove documentation",
            "B": "To replace Git",
            "C": "To avoid code reviews",
            "D": "To detect broken existing behavior",
        },
        "answer": "D",
        "explanation": "Regression tests help catch unintended changes.",
    },
    {
        "question": "Why use feature branches and pull requests?",
        "options": {
            "A": "To isolate and review changes",
            "B": "To avoid all tests",
            "C": "To delete main",
            "D": "To hide errors",
        },
        "answer": "A",
        "explanation": "Branches isolate work while PRs support peer review.",
    },
    {
        "question": "Why write a temporary file before replacing JSON?",
        "options": {
            "A": "To remove validation",
            "B": "To skip persistence",
            "C": "To protect existing data if writing fails",
            "D": "To prevent reopening tickets",
        },
        "answer": "C",
        "explanation": "Write first, then replace to reduce the risk of data loss.",
    },
]
