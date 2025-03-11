import streamlit as st
import re

def check_password_strength(password):
    score = 0
    suggestions = []
    
    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Make the password at least 8 characters long.")
    
    # Uppercase and Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Include both uppercase and lowercase letters.")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        suggestions.append("Include at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        suggestions.append("Include at least one special character (!@#$%^&*).")
    
    return score, suggestions

def main():
    st.set_page_config(page_title="Password Strength Meter", page_icon="🔒", layout="centered")
    
    st.markdown("""<h2 style='text-align: center; color: #4CAF50;'>🔑 Password Strength Meter</h2>""", unsafe_allow_html=True)
    
    password = st.text_input("Enter your password:", type="password")
    
    if st.button("Check Strength"):
        if password:
            score, suggestions = check_password_strength(password)
            
            if score <= 2:
                st.error("🚨 Weak Password! Try making it stronger.")
            elif score == 3 or score == 4:
                st.warning("⚠️ Moderate Password! Consider adding more security features.")
            else:
                st.success("✅ Strong Password! Good job!")
            
            if suggestions:
                st.markdown("**🔹 Suggestions to Improve:**")
                for suggestion in suggestions:
                    st.markdown(f"- {suggestion}")
        else:
            st.warning("⚠️ Please enter a password to check.")
    
    st.markdown("---")
    st.markdown("👨‍💻 Create By Hassan Raza ")
    
if __name__ == "__main__":
    main()
