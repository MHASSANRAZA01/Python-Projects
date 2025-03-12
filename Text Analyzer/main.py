import streamlit as st
import re

def count_vowels(text):
    return sum(1 for char in text.lower() if char in 'aeiou')

def text_analysis():
    st.title("📊 Text Analyzer")
    st.write("Enter a paragraph below and explore various text analysis features!")
    
    # User Input
    text = st.text_area("✍️ Enter your paragraph:", "")
    
    if text:
        words = text.split()
        num_words = len(words)
        num_chars = len(text)
        vowel_count = count_vowels(text)
        avg_word_length = round(num_chars / num_words, 2) if num_words > 0 else 0
        
        # Display Analysis Results
        st.subheader("📌 Analysis Results:")
        st.write(f"**Total Words:** {num_words}")
        st.write(f"**Total Characters (including spaces):** {num_chars}")
        st.write(f"**Number of Vowels:** {vowel_count}")
        st.write(f"**Average Word Length:** {avg_word_length}")
        
        # Search and Replace Feature
        st.subheader("🔍 Search & Replace")
        search_word = st.text_input("Enter word to search:")
        replace_word = st.text_input("Enter word to replace it with:")
        
        if search_word and replace_word:
    # Use re.escape() to handle special characters in search_word
             modified_text = re.sub(rf"\b{re.escape(search_word)}\b", replace_word, text, flags=re.IGNORECASE)
             st.write("**Modified Text:**")
             st.success(modified_text)

        
        # Uppercase & Lowercase Conversion
        st.subheader("🔠 Text Transformations")
        st.write("**Uppercase:**")
        st.code(text.upper())
        st.write("**Lowercase:**")
        st.code(text.lower())
        
        # Check for 'Python' in text
        if "python" in text.lower():
            st.success("✅ The paragraph contains the word 'Python'.")
        else:
            st.warning("❌ The paragraph does not contain the word 'Python'.")
    else:
        st.warning("⚠️ Please enter a paragraph to analyze.")

if __name__ == "__main__":
    text_analysis()
