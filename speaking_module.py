import streamlit as st
import speech_recognition as sr
import time
import nltk
from nltk.corpus import cmudict
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
nltk.download('cmudict')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Function to recognize speech
def sptext():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        max_retries = 3
        retries = 0
        while retries < max_retries:
            try:
                audio = recognizer.listen(source, timeout=10)
                break
            except sr.WaitTimeoutError:
                retries += 1
                st.write("Timeout. Retrying...")
        if retries == max_retries:
            st.write("Failed to recognize speech after", max_retries, "retries")
            return None
        try:
            st.write("Recognizing...")
            data = recognizer.recognize_google(audio, language="en-US").lower()
            st.write("You said:", data)
        except sr.UnknownValueError:
            st.write("Didn't understand what you said")
            return None
        except sr.RequestError as e:
            st.write("Error:", e)
            return None
        return data

# Function to evaluate IELTS speaking test responses
def evaluate_ielts_response(responses, part):
    score = 0
    feedback = ""

    def evaluate_criteria(response):
        # Tokenize response into words and sentences
        words = word_tokenize(response)
        sentences = sent_tokenize(response)

        # Calculate fluency score
        fluency_score = len(words) / len(sentences)
        if fluency_score > 9:
            fluency_score = 9

        # Calculate vocabulary score
        vocabulary_score = len(set(words)) / (2 * len(words))

        # Calculate grammar score
        grammar_score = 0
        for sentence in sentences:
            tokens = word_tokenize(sentence)
            if len(tokens) > 7:
                grammar_score += 1
        grammar_score /= len(sentences)

        # Calculate pronunciation score
        pronunciation_score = 0
        for word in words:
            if word in cmudict.words():
                pronunciation_score += 1
        pronunciation_score /= (2 * len(words))

        # Calculate overall score
        overall_score = (fluency_score + vocabulary_score + grammar_score + pronunciation_score) / 4

        # Map overall score to band score
        band_scores = {
            9: (8, 9),
            8: (7, 8),
            7: (6, 7),
            6: (5, 6),
            5: (4, 5),
            4: (3, 4),
            3: (2, 3),
            2: (1, 2),
            1: (0, 1)
        }

        for band, score_range in band_scores.items():
            if score_range[0] <= overall_score <= score_range[1]:
                return band

        return 0

    fluency_band = evaluate_criteria(responses)
    lexical_band = evaluate_criteria(responses)
    grammar_band = evaluate_criteria(responses)
    pronunciation_band = evaluate_criteria(responses)

    overall_band = min(fluency_band, lexical_band, grammar_band, pronunciation_band)

    feedback = f"Your estimated IELTS Band Score for the {part} part: Band {overall_band}.0"
    return feedback

# Function to ask and process IELTS speaking test parts
def ielts_speaking_test():
    st.header("IELTS Speaking Test")

    # Part 1: Introduction Questions
    st.write("Part 1: Introduction Questions")
    st.write("I will ask you a few introductory questions. Please answer them.")

    introduction_questions = [
        "What is your full name?",
        "Where are you from?",
        "What do you do? Do you work or study?",
        "What are your hobbies?"
    ]

    introduction_responses = []

    for question in introduction_questions:
        st.write(question)
        response = sptext()
        if response:
            st.write("Your response:", response)
            introduction_responses.append(response)

    introduction_feedback = evaluate_ielts_response(' '.join(introduction_responses), 'introduction')
    st.write(introduction_feedback)

    # Part 2: Cue Card
    st.write("Part 2: Cue Card")
    cue_card_topic = "Describe a memorable event in your life. You should say: when it happened, where it happened, what happened, and explain why it was memorable."
    st.write(cue_card_topic)
    
    st.write("Please take a moment to think about your response. When you are ready, start speaking.")
    st.write("You have 1-2 minutes to speak.")
    time.sleep(60)  # Giving the user time to respond (you can adjust as needed)

    cue_card_response = sptext()
    if cue_card_response:
        st.write("Your response:", cue_card_response)
        cue_card_feedback = evaluate_ielts_response(cue_card_response, 'cue_card')
        st.write(cue_card_feedback)

    # Part 3: Follow-Up Questions
    st.write("Part 3: Follow-Up Questions")
    st.write("Now, I will ask you a few follow-up questions related to the cue card topic.")

    follow_up_questions = [
        "How did the event affect you?",
        "What did you learn from the experience?",
        "Would you like to experience something similar again? Why or why not?",
        "How do you think such events are important in people's lives?"
    ]

    follow_up_responses = []

    for question in follow_up_questions:
        st.write(question)
        response = sptext()
        if response:
            st.write("Your response:", response)
            follow_up_responses.append(response)

    follow_up_feedback = evaluate_ielts_response(' '.join(follow_up_responses), 'follow_up')
    st.write(follow_up_feedback)

# Main function for Streamlit app
def main():
    st.title("IELTS Speaking Test Application")

    # IELTS Speaking Test Feature
    if st.button("Start IELTS Speaking Test"):
        ielts_speaking_test()

if __name__ == '__main__':
    main()
    