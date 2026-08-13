ICFES Virtual Tutor 🎓

A free console-based quiz application that helps Colombian high school students practice for the ICFES Saber 11 exam. This project focuses on Mathematics as a beta version, with plans to expand to other subjects and migrate to a web interface.

📖 About

Many students from public schools in Colombia don't have access to paid ICFES prep courses. This tool provides free, unlimited practice with real exam-style questions, instant feedback, and explanations — helping close the gap in exam preparation resources.

✨ Features
20 Mathematics questions covering Algebra, Geometry, Statistics, and Arithmetic (ICFES-style, multiple choice)
Instant feedback after each answer, including the correct answer and a full explanation when you get it wrong
Automatic results history saved to a JSON file, with name, date, and score for every attempt
Simple, beginner-friendly codebase — built while learning Python from scratch
🛠️ Tech Stack
Python 3 — core logic
JSON — question bank and results storage
datetime — timestamps for each attempt
Streamlit (coming soon) — web interface
🚀 How to Run
Make sure you have Python installed (python.org)
Clone this repository:
   git clone https://github.com/your-username/your-repo-name.git
Navigate to the project folder:
   cd your-repo-name
Run the app:
   python main.py
Enter your name, select "Matematicas" as the subject, and answer the 20 questions with the letter of your chosen option (A, B, C, or D)
📁 Project Structure
ICFES-PROYECTO/
├── main.py                      # Main program logic
├── preguntas_matematicas.json   # Question bank (20 Math questions)
├── resultados.json              # Auto-generated: stores each attempt's results
├── .gitignore
└── README.md
📊 How It Works
The program loads all questions from preguntas_matematicas.json
It asks the user's name and prints a welcome message
For each question, it shows the topic, the question text, and the four options
The user answers, and the program checks it against the correct answer, showing an explanation if incorrect
At the end, it shows the final score and saves the result (name, date, score) to resultados.json, keeping a full history of every attempt
🗺️ Roadmap
Ready Console-based quiz with Mathematics questions
Ready  Results history saved as JSON
 Web interface built with Streamlit
 Add more subjects: Critical Reading, Social Studies, Natural Sciences
 AI-powered question generation for unlimited practice
 Deploy online so any student can access it for free
👨‍💻 Author

Built by Daniel, a high school student from Jamundí, Valle del Cauca, Colombia, preparing for the ICFES exam and learning Python along the way.

📄 License

This project is open for educational purposes. Feel free to fork it and adapt it for your own school project.
