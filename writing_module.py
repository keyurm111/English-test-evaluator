import streamlit as st
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer
from spellchecker import SpellChecker
import language_tool_python
from PIL import Image
from textstat import flesch_kincaid_grade

# Download required NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# Initialize tools
lemmatizer = WordNetLemmatizer()
spell = SpellChecker()
tool = language_tool_python.LanguageTool('en-US')
stop_words = set(stopwords.words('english'))

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def evaluate_writing_response(response, task_type):
    feedback = {}
    words = word_tokenize(response)
    sentences = sent_tokenize(response)
    
    # Adjusting Task Achievement score based on word count and content
    word_count = len(words)
    required_word_count = 150 if task_type == 'Task 1' else 250
    task_achievement_score = min(word_count / required_word_count, 1) * 0.7  # Adjusted weight to 0.7 to avoid overestimation
    
    # Add more detailed trend analysis for Task 1 or argument clarity for Task 2
    if task_type == 'Task 1':
        key_trend_words = ['increase', 'decrease', 'fluctuate', 'stable', 'peak', 'trend']
        if any(word in response.lower() for word in key_trend_words):
            task_achievement_score += 0.15  # Added weight to Task Achievement for key trend usage
    else:
        if 'conclusion' in response.lower():
            task_achievement_score += 0.15  # Added weight for conclusion presence
    
    # Max out Task Achievement score to avoid exceeding 1
    task_achievement_score = min(task_achievement_score, 1)
    feedback['Task Achievement'] = f"Word Count: {word_count}. Task Achievement Score: {task_achievement_score * 9:.1f}/9"

    # Coherence and Cohesion scoring (adjusted linking and structure analysis)
    linking_words = ['however', 'therefore', 'moreover', 'furthermore', 'nevertheless', 'in addition', 'consequently']
    linking_used = sum(1 for word in words if word.lower() in linking_words)
    paragraph_count = response.count("\n") + 1
    cohesion_score = min((linking_used / 6) + (paragraph_count / 4), 1) * 0.7  # Adjusted weight to better reflect real cohesion issues
    
    feedback['Coherence and Cohesion'] = f"Linking Words: {linking_used}. Paragraphs: {paragraph_count}. Score: {cohesion_score * 9:.1f}/9"

    # Lexical Resource (adjusted vocabulary analysis)
    tagged_words = nltk.pos_tag(words)
    lemmas = [lemmatizer.lemmatize(word.lower(), get_wordnet_pos(pos)) for word, pos in tagged_words]
    unique_lemmas = set(lemmas) - stop_words
    lexical_variety = len(unique_lemmas) / len(words)
    advanced_words = len([word for word in unique_lemmas if len(word) > 8])
    
    # Adjusted lexical resource scoring to reduce score for limited variety
    lexical_score = min((lexical_variety * 1.5 + (advanced_words / 20)), 1) * 0.7
    
    feedback['Lexical Resource'] = f"Unique words: {len(unique_lemmas)}. Advanced words: {advanced_words}. Score: {lexical_score * 9:.1f}/9"

    # Grammatical Range and Accuracy (penalizing grammar errors more)
    errors = tool.check(response)
    grammar_errors = len([error for error in errors if error.category != 'TYPOS'])
    spelling_errors = len(spell.unknown(words))
    
    # Penalize the score more heavily for grammar/spelling issues
    complex_sentences = sum(1 for sentence in sentences if len(word_tokenize(sentence)) > 12)
    grammar_score = max(0, min(((complex_sentences / len(sentences)) - (grammar_errors / 100) - (spelling_errors / 100)), 1)) * 0.7  # Reduced weight to limit inflation of grammar score
    
    feedback['Grammatical Range and Accuracy'] = f"Complex sentences: {complex_sentences}. Grammar errors: {grammar_errors}. Spelling errors: {spelling_errors}. Score: {grammar_score * 9:.1f}/9"

    # Readability metric (Flesch-Kincaid)
    readability = flesch_kincaid_grade(response)
    feedback['Readability'] = f"Flesch-Kincaid Grade Level: {readability:.1f}"

    # Final score calculation with adjusted weights
    overall_score = (task_achievement_score + cohesion_score + lexical_score + grammar_score) / 4
    band = get_ielts_band(overall_score)
    
    feedback['Overall Band'] = f"Estimated IELTS Band Score: {band}.0"
    
    return feedback, band

# Adjusted band score mapping to reflect more accurate ranges
def get_ielts_band(overall_score):
    band_scores = {
        9: (0.9, 1.0),
        8: (0.8, 0.9),
        7: (0.7, 0.8),
        6: (0.6, 0.7),
        5: (0.5, 0.6),
        4: (0.4, 0.5),
        3: (0.3, 0.4),
        2: (0.2, 0.3),
        1: (0, 0.2),
    }
    
    for band, (lower, upper) in band_scores.items():
        if lower <= overall_score < upper:
            return band
    return 1

def calculate_overall_band(task_1_band, task_2_band):
    weighted_average = (task_1_band * 1/3) + (task_2_band * 2/3)
    return round(weighted_average * 2) / 2

# Streamlit interface
def ielts_writing_test():
    st.header("IELTS Writing Test")

    # Task 1 prompt
    st.subheader("Task 1")
    task_1_options = [
        "1. The graph shows the average monthly rainfall in three cities over a year.",
        "2. The diagram illustrates the process of recycling plastic bottles.",
        "3. The pie charts below show the comparison of different kinds of energy production of France in two years.",
    ]
    
    task_1_selected = st.selectbox("Choose a Task 1 prompt:", task_1_options)
    st.write(f"**Task:** {task_1_selected}")
    
    image_paths = {
        task_1_options[0]: 'rainfall_graph.jpg',
        task_1_options[1]: 'recycling_process.jpg',
        task_1_options[2]: 'energy_sources_pie_chart.jpg'
    }
    
    st.image(Image.open(image_paths[task_1_selected]), caption=f"Graph for {task_1_selected}")

    if 'task_1_response' not in st.session_state:
        st.session_state['task_1_response'] = ''
    if 'task_1_feedback' not in st.session_state:
        st.session_state['task_1_feedback'] = None
    
    st.session_state['task_1_response'] = st.text_area("Your Task 1 response (Minimum 150 words):", st.session_state['task_1_response'])
    
    # Task 2 prompt
    st.subheader("Task 2")
    task_2_options = [
        "1. Some people think that children should begin their formal education at a very early age. Others think they should begin at least 7 years old. Discuss both views and give your opinion.",
        "2. Many people believe that social media has had a negative impact on society. To what extent do you agree or disagree with this opinion?",
        "3. Some believe that unpaid community service should be a compulsory part of high school programs. Do you agree or disagree?",
    ]
    
    task_2_selected = st.selectbox("Choose a Task 2 prompt:", task_2_options)
    st.write(f"**Task:** {task_2_selected}")
    
    if 'task_2_response' not in st.session_state:
        st.session_state['task_2_response'] = ''
    if 'task_2_feedback' not in st.session_state:
        st.session_state['task_2_feedback'] = None
    
    st.session_state['task_2_response'] = st.text_area("Your Task 2 response (Minimum 250 words):", st.session_state['task_2_response'])
    
    # Submission and evaluation
    if st.button("Submit both tasks"):
        # Evaluate Task 1
        if len(st.session_state['task_1_response'].split()) >= 150:
            task_1_feedback, task_1_band = evaluate_writing_response(st.session_state['task_1_response'], 'Task 1')
            st.session_state['task_1_feedback'] = task_1_feedback
            st.session_state['task_1_band'] = task_1_band
        else:
            st.write("Please write at least 150 words for Task 1.")

        # Evaluate Task 2
        if len(st.session_state['task_2_response'].split()) >= 250:
            task_2_feedback, task_2_band = evaluate_writing_response(st.session_state['task_2_response'], 'Task 2')
            st.session_state['task_2_feedback'] = task_2_feedback
            st.session_state['task_2_band'] = task_2_band
        else:
            st.write("Please write at least 250 words for Task 2.")
        
        # Show feedback and calculate overall band
        if st.session_state['task_1_feedback'] and st.session_state['task_2_feedback']:
            st.write(f"Your estimated IELTS Band Score for Task 1: Band {st.session_state['task_1_band']}.0")
            st.write("Task 1 Feedback:")
            for criteria, comment in st.session_state['task_1_feedback'].items():
                st.write(f"{criteria}: {comment}")

            st.write(f"Your estimated IELTS Band Score for Task 2: Band {st.session_state['task_2_band']}.0")
            st.write("Task 2 Feedback:")
            for criteria, comment in st.session_state['task_2_feedback'].items():
                st.write(f"{criteria}: {comment}")
            
            # Calculate overall band with IELTS weighting
            overall_band = calculate_overall_band(st.session_state['task_1_band'], st.session_state['task_2_band'])
            st.write(f"**Overall Estimated IELTS Band Score: Band {overall_band:.1f}**")

def main():
    st.title("IELTS Writing Test Application")
    ielts_writing_test()

if __name__ == '__main__':
    main()
