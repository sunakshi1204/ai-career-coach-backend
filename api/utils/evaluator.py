def evaluate_answer(answer):
    score = min(len(answer.split()) / 5, 10)  # simple logic
    feedback = ""

    if len(answer.split()) < 10:
        feedback = "Answer is too short. Try to explain more."
    else:
        feedback = "Good answer, but can be more structured."

    improved = "Try to include examples and structured points."

    return score, feedback, improved