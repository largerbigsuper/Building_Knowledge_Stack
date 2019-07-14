import json
import os
import glob
from datamodels.subjects.models import mm_Subject
from datamodels.questions.models import mm_Question, mm_QuestionRecord, mm_Exam


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
resource_base = os.path.join(base_dir, 'resource')

Question_Type_DICT = {
    '单选题': mm_Question.Question_Type_Danxuanti,
    '多选题': mm_Question.Question_Type_Duouanti,
    '判断题': mm_Question.Question_Type_Panduanti,
}


def import_questions_from_files(files=None):
    mm_Exam.all().delete()
    mm_QuestionRecord.all().delete()
    mm_Question.all().delete()
    for path in files:
        fname = os.path.basename(path).split('.')[0]
        subject_name, type_name = fname.split('_')
        subject_id = mm_Subject.get(name=subject_name).id
        qtype = Question_Type_DICT[type_name]
        print(subject_name, subject_id, type_name, qtype)
        with open(path) as f:
            questions = json.loads(f.read())
            for q in questions:
                q['subject_id'] = subject_id
                q['qtype'] = qtype
                mm_Question.create(**q)


def run():
    questions_dir = os.path.join(resource_base, 'questions')
    files = glob.glob(questions_dir + '/**')
    import_questions_from_files(files)


