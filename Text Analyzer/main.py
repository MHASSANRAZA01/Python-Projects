import streamlit as st
import re

def count_vowels(text):
    return sum(1 for char in text.lower() if char in 'aeiou')

def text_analysis():
    st.markdown("""
        <style>
            .stTextInput>div>div>input {
                background-color: #1e1e1e;
                color: white;
            }
            .stTextArea>div>textarea {
                background-color: #1e1e1e;
                color: white;
            }
            .stButton>button {
                background-color: #444;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center;'>Text Analyzer</h1>", unsafe_allow_html=True)
    
    with st.container():
        st.subheader("Enter the Paragraph:")
        text = st.text_area("", "", key="paragraph")
        
        st.markdown("🔍 **Enter a word to search for:**")
        search_word = st.text_input("Search Word", "", key="search_word")
        
        st.markdown("✍️ **Enter a word to replace it with:**")
        replace_word = st.text_input("Replace Word", "", key="replace_word")
        
        if st.button("Analyze Paragraph"):
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
                if search_word and replace_word:
                    modified_text = re.sub(rf"\b{re.escape(search_word)}\b", replace_word, text, flags=re.IGNORECASE)
                    
                    st.subheader("🔍 Search and Replace Results")
                    occurrences = len(re.findall(rf"\b{re.escape(search_word)}\b", text, flags=re.IGNORECASE))
                    st.write(f"Found {occurrences} occurrence(s) of '{search_word}'")
                    
                    st.markdown("**Modified Text:**")
                    st.success(modified_text)
                    
                    st.markdown(f"<div style='background-color: #1e1e1e; color: white; padding: 10px; border-radius: 5px;'>{modified_text}</div>", unsafe_allow_html=True)
                
                # Uppercase & Lowercase Conversion
                st.subheader("🔠 Text Transformations")
                st.write("**Uppercase:")
                st.code(text.upper())
                st.write("**Lowercase:")
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
