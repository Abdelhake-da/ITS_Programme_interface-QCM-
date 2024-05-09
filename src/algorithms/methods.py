from app.models import Question


def is_correct(questions, answers: list) -> list: 
    is_answer_true: list = []  
    tup_list = []
    for index, question in enumerate(questions):
        tup = []
        is_answer_true.append(None)
        for answer in answers[index]:
            for ans in  answer:
                if not ans in question[1]["qst_correct_answer"]:
                    is_answer_true[index]=False
                    tup.append((ans,False))
                else:
                    tup.append((ans,True))
        if is_answer_true[index] == None:
            is_answer_true[index]=True
        tup_list.append(tup)
    return is_answer_true,tup_list
def calc_note(response: list):
    num_total = len(response)
    true = response.count(True)
    return format((true * 20) / num_total, ".2f")
