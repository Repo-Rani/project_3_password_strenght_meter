import streamlit as st
import random
import string
import time

# Function to generate a strong password
def generate_password(length=12, use_uppercase=True, use_lowercase=True, use_digits=True, use_special=True):
    characters = ''
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Password strength check function
def check_password_strength(password):
    strength = 0
    remarks = []
    tips = []

    # Check length
    if len(password) >= 8:
        strength += 1
    else:
        remarks.append('❌ Password should be at least 8 characters long.')
        tips.append('👉 Try adding more characters to make it longer.')

    # Check for digits
    if any(char.isdigit() for char in password):
        strength += 1
    else:
        remarks.append('❌ Password should contain at least one digit.')
        tips.append('👉 Add numbers like 1, 2, 3, etc.')

    # Check for uppercase letters
    if any(char.isupper() for char in password):
        strength += 1
    else:
        remarks.append('❌ Password should contain at least one uppercase letter.')
        tips.append('👉 Use capital letters like A, B, C, etc.')

    # Check for lowercase letters
    if any(char.islower() for char in password):
        strength += 1
    else:
        remarks.append('❌ Password should contain at least one lowercase letter.')
        tips.append('👉 Use small letters like a, b, c, etc.')

    # Check for special characters
    if any(not char.isalnum() for char in password):
        strength += 1
    else:
        remarks.append('❌ Password should contain at least one special character.')
        tips.append('👉 Add symbols like @, #, $, etc.')

    # Determine strength level
    if strength == 5:
        remarks = ['✅ Your password is very strong!']
    elif strength >= 3:
        remarks = ['⚠️ Your password is strong, but can be improved.']
    else:
        remarks = ['❌ Your password is weak. Please consider a stronger password.']

    return strength, remarks, tips

# Streamlit app
st.set_page_config(page_title="🔐 Ultimate Password Tool", page_icon="🔒", layout="centered")

# Title and description
st.title("🔐 Ultimate Password Tool")
st.write("Create strong passwords and check their strength in real-time!")

# Sidebar for password generation
with st.sidebar:
    st.header("🔧 Password Generator")
    password_length = st.slider("Select password length", 8, 20, 12)
    use_uppercase = st.checkbox("Include Uppercase Letters", value=True)
    use_lowercase = st.checkbox("Include Lowercase Letters", value=True)
    use_digits = st.checkbox("Include Digits", value=True)
    use_special = st.checkbox("Include Special Characters", value=True)
    
    if st.button("Generate Strong Password"):
        generated_password = generate_password(password_length, use_uppercase, use_lowercase, use_digits, use_special)
        st.session_state.generated_password = generated_password
        st.success("Password generated successfully!")
        st.code(generated_password)
        st.balloons()  # Confetti animation

    # Copy to clipboard button
    if "generated_password" in st.session_state:
        if st.button("📋 Copy to Clipboard"):
            st.write("Password copied to clipboard!")
            st.code(st.session_state.generated_password)

# Main app for password strength checking
st.header("🔍 Check Your Password Strength")
password = st.text_input("Enter your password:", type="password", help="Type your password here.", key="password_input")

# Toggle password visibility
if st.checkbox("Show Password"):
    st.text_input("Enter your password:", value=password, type="default", key="password_input_visible")
else:
    st.text_input("Enter your password:", value=password, type="password", key="password_input_hidden")

# Real-time feedback
if password:
    strength, remarks, tips = check_password_strength(password)

    # Display strength with a progress bar and color
    st.subheader("Password Strength")
    if strength <= 2:
        st.error("Weak Password")
        st.progress(strength / 5)
    elif strength == 3 or strength == 4:
        st.warning("Medium Password")
        st.progress(strength / 5)
    else:
        st.success("Strong Password")
        st.progress(strength / 5)

    # Display remarks
    st.subheader("Feedback")
    for remark in remarks:
        st.write(remark)

    # Display tips to improve password
    if strength < 5:
        st.subheader("💡 Tips to Improve Your Password")
        for tip in tips:
            st.write(tip)

# Password history (last 3 generated passwords)
if "password_history" not in st.session_state:
    st.session_state.password_history = []

if "generated_password" in st.session_state:
    if st.session_state.generated_password not in st.session_state.password_history:
        st.session_state.password_history.append(st.session_state.generated_password)
    if len(st.session_state.password_history) > 3:
        st.session_state.password_history.pop(0)

if st.session_state.password_history:
    st.subheader("📜 Last Generated Passwords")
    for pwd in st.session_state.password_history:
        st.code(pwd)
        if st.button(f"Delete {pwd}"):
            st.session_state.password_history.remove(pwd)
            st.experimental_rerun()

# Footer
st.markdown("---")
st.write("Made with ❤️ using Streamlit")

# Add some animations or fun elements
st.balloons()  
