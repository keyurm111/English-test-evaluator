# English-test-evaluator
The English Test Evaluator is an automated system for evaluating IELTS modules: Speaking, Writing, Reading, and Listening. It leverages Natural Language Processing (NLP), speech recognition, and machine learning to provide accurate, real-time assessments aligned with IELTS standards.
Key Features:

Speaking Module: Real-time evaluation of pronunciation, fluency, lexical resource, and coherence using speech-to-text conversion and NLP tools.
Writing Module: Automated scoring for grammar, coherence, task achievement, and vocabulary with constructive feedback.
Reading Module : Comprehension analysis through multiple question types, including True/False/Not Given and matching headings.
Listening Module : Audio-based testing with synchronized questions and accurate scoring.
User-Friendly Interface: Built with Streamlit, offering intuitive navigation, real-time feedback, and detailed performance insights.
The system is designed to reduce human biases, save evaluation time, and provide a scalable solution for global learners and institutions.

Technologies Used:
Python as the core development language.
NLP Libraries like NLTK and LanguageTool for evaluating text-based tasks.
Google Speech API for speech recognition.
Streamlit for an interactive web-based user interface.

----------------------------------------------------------------------------------------
make a first folder with name of "speaking and writing module".in which add below files.
main_app.py
energy_source_pie_chart.jpg
rainfall_graph.jpg
recycling_process.jpg
speaking_module.py
writing_module.py
---------------------------------------------------------------------------------
For listening and reading module:
make folder with name of "listening and reading module". in which add below files.
index.html
reading.html
listening.html
make a subfolder in this this folder with name of source in which add below files.
1.png
2.png
3.png
4.png
listening1.mp3
---------------------------------------------------------------------------------------------------
After this open your terminal and write "streamlit run main_app.py" for speaking and writing module.
so you can see the http link. copy this link and paste the link in your browser so you can see both modules.
for reading and listening module, just run index.html. 
--------------------------------------------
Important python libraries for this project:
pip install streamlit 
pip install nltk 
pip install pyspellchecker 
pip install language-tool-python 
pip install pillow 
pip install textstat
pip install SpeechRecognition


