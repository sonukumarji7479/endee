import os
import json
import random

categories = [
    "Java", "Python", "C Programming", "Data Structures", "Algorithms",
    "DBMS", "Operating System", "Computer Networks", "Artificial Intelligence",
    "Machine Learning", "Web Development", "HTML CSS", "JavaScript", "React",
    "Cyber Security", "Cloud Computing", "Software Engineering", "General Knowledge",
    "Aptitude", "Reasoning"
]

QA_DATA = {
    "Java": {
        "topics": ["JVM", "JRE", "Inheritance", "Polymorphism", "Encapsulation", "Abstraction", "Interface", "Exception Handling", "Garbage Collection", "Multithreading"],
        "real": [
            {"question": "Which of the following is NOT a Java feature?", "options": ["Dynamic", "Architecture Neutral", "Use of pointers", "Object Oriented"], "answer": "Use of pointers"},
            {"question": "What is the return type of the hashCode() method in the Object class?", "options": ["int", "long", "void", "Object"], "answer": "int"},
            {"question": "Which package contains the Random class?", "options": ["java.util", "java.lang", "java.io", "java.awt"], "answer": "java.util"}
        ]
    },
    "Python": {
        "topics": ["Lists", "Dictionaries", "Decorators", "Generators", "OOP", "PIP", "Pandas", "NumPy", "Functions", "Modules"],
        "real": [
            {"question": "Which keyword is used for function declaration in Python?", "options": ["def", "function", "fun", "define"], "answer": "def"},
            {"question": "Which data type is mutable in Python?", "options": ["Tuple", "String", "List", "Integer"], "answer": "List"}
        ]
    }
    # Placeholders for other topics filled programmatically
}

def generate_fake_mcqs(category, count=150):
    topic_data = QA_DATA.get(category, {
        "topics": ["Basic Concepts", "Architecture", "Best Practices", "Operators", "Variables", "Syntax", "Troubleshooting"],
        "real": []
    })
    
    questions = list(topic_data["real"])
    topics = topic_data["topics"]
    
    while len(questions) < count:
         topic = random.choice(topics)
         template_index = random.randint(0, 3)
         
         if template_index == 0:
              q = f"Which of the following best describes the concept of {topic} in {category}?"
              opts = [f"A method to achieve modularity via {topic}", f"A slow operations structure", f"A design pattern exclusively for memory", f"None of the above"]
              ans = opts[0]
         elif template_index == 1:
              q = f"What is the primary advantage of utilizing {topic} in {category} applications?"
              opts = [f"Improved code reusability", f"Slower execution time", f"Increased file size", f"Direct hardware access"]
              ans = opts[0]
         elif template_index == 2:
              q = f"In {category}, {topic} is considered which type of component?"
              opts = [f"Core Pillar", f"Optional Utility", f"Deprecated module", f"None"]
              ans = opts[0]
         else:
              q = f"Which error might you encounter if {topic} is misconfigured in {category}?"
              opts = [f"Runtime Exception", f"Compilation Warning", f"Nothing happens", f"Hardware failure"]
              ans = opts[0]

         # Shuffle options
         correct_ans = ans
         random.shuffle(opts)
         
         questions.append({
              "question": q,
              "options": opts,
              "answer": correct_ans
         })
         
    return questions

output_dir = os.path.join(os.path.dirname(__file__), "data", "quiz")
os.makedirs(output_dir, exist_ok=True)

for cat in categories:
    filename = "".join([c for c in cat if c.isalnum() or c in (' ', '_', '-')]).strip().lower().replace(' ', '_') + ".json"
    path = os.path.join(output_dir, filename)
    
    questions = generate_fake_mcqs(cat, 210) # Generate 210 each
    with open(path, 'w', encoding='utf-8') as f:
         json.dump(questions, f, indent=2)
    print(f"Generated {path}")

print("Total generated questions for 20 categories.")
