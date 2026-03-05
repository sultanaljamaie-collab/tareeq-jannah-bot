import random
import json

categories = [
"العقيدة",
"القرآن",
"السيرة",
"الفقه",
"الصحابة",
"التاريخ الإسلامي"
]

levels = ["easy","medium","hard"]

base_questions = [

("كم عدد أركان الإسلام؟",["4","5","6","7"],"5","العقيدة"),
("كم عدد أركان الإيمان؟",["5","6","7","8"],"6","العقيدة"),
("كم عدد سور القرآن؟",["110","114","120","124"],"114","القرآن"),
("ما أول سورة في القرآن؟",["الفاتحة","البقرة","الإخلاص","الناس"],"الفاتحة","القرآن"),
("من هو خاتم الأنبياء؟",["موسى","عيسى","محمد ﷺ","إبراهيم"],"محمد ﷺ","السيرة"),
("من هو أول خليفة للمسلمين؟",["عمر","أبو بكر","عثمان","علي"],"أبو بكر","الصحابة"),
("في أي عام حدثت الهجرة؟",["620","622","624","630"],"622","التاريخ الإسلامي")
]

questions = []

for i in range(10000):

    q = random.choice(base_questions)

    question = {
    "question":q[0],
    "options":q[1],
    "answer":q[2],
    "category":q[3],
    "level":random.choice(levels)
    }

    questions.append(question)

with open("questions.py","w",encoding="utf8") as f:

    f.write("questions = ")
    json.dump(questions,f,ensure_ascii=False,indent=2)

print("تم إنشاء 10000 سؤال بنجاح")
