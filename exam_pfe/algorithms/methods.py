from app.models import Question


def is_correct(questions, answers: list) -> list: 
    is_answer_true: list = []  
    for index, question in enumerate(questions):
        is_answer_true.append(None)
        for answer in answers[index]:
            if not answer in question[1]["qst_correct_answer"]:
                is_answer_true[index]=False
                break
        if is_answer_true[index] == None:
            is_answer_true[index]=True
    return is_answer_true
