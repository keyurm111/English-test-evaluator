import streamlit as st
from speaking_module import ielts_speaking_test
from writing_module import ielts_writing_test

def main():
    st.title("IELTS Practice Test Application")
    st.header("Choose a module to practice:")

    # Navigation menu
    module_choice = st.selectbox(
        "Select a module to practice:",
        ["Home", "Speaking Module", "Writing Module"]
    )

    if module_choice == "Speaking Module":
        ielts_speaking_test()
    elif module_choice == "Writing Module":
        ielts_writing_test()
    else:
        st.write("""
        Welcome to the IELTS Practice Test Application.  
        Select one of the modules above to start practicing:
        - **Speaking Module**: Practice the IELTS speaking test.
        - **Writing Module**: Practice IELTS writing tasks 1 and 2.
        """)

if __name__ == "__main__":
    main()
