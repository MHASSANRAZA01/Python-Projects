import streamlit as st

 
st.set_page_config(
    page_title="Advanced Unit Converter",
    page_icon="🔄",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 20px;
    }
    .stTitle {
        color: #2E86C1;
        font-size: 40px;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* Style for both selectbox and number input containers */
    .stSelectbox, div[data-testid="stNumberInput"] {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Style for the white container around number input */
    div[data-testid="stNumberInput"] {
        background-color: white;
        border-radius: 10px;
        padding: 8px;
        margin: 4px;
    }
    
    /* Style for the actual input field */
    [data-testid="stNumberInput"] input {
        background-color: #262730;
        color: white;
        border-radius: 4px;
    }
    
    /* Style for select boxes */
    div[data-baseweb="select"] {
        background-color: #262730;
        border-radius: 4px;
    }
    
    .result-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to convert length
def convert_length(value, from_unit, to_unit):
    conversion_factors = {
        'meters': 1.0,
        'kilometers': 0.001,
        'miles': 0.000621371,
        'feet': 3.28084
    }
    return value * conversion_factors[to_unit] / conversion_factors[from_unit]

# Function to convert temperature
def convert_temperature(value, from_unit, to_unit):
    if from_unit == 'Celsius' and to_unit == 'Fahrenheit':
        return value * 9/5 + 32
    elif from_unit == 'Fahrenheit' and to_unit == 'Celsius':
        return (value - 32) * 5/9
    return value

# Function to convert weight
def convert_weight(value, from_unit, to_unit):
    conversion_factors = {
        'kilograms': 1.0,
        'grams': 1000.0,
        'pounds': 2.20462,
        'ounces': 35.274
    }
    return value * conversion_factors[to_unit] / conversion_factors[from_unit]

# Main app with enhanced UI
st.title('🔄 Smart Unit Converter')

# Create columns for better layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Select Category")
    category = st.selectbox('', ['Length', 'Temperature', 'Weight'], 
                          help="Choose the type of conversion you want to perform",
                          key='category_select')

with col2:
    st.markdown("### Enter Value")
    value = st.number_input('', value=0.0, 
                           help="Enter the numeric value you want to convert",
                           key='value_input')

# Create two columns for input and output units
unit_col1, unit_col2 = st.columns([1, 1])

# Conversion logic with enhanced UI
if category == 'Length':
    with unit_col1:
        st.markdown("### From")
        from_unit = st.selectbox('', ['meters', 'kilometers', 'miles', 'feet'],
                                key='length_from')
    with unit_col2:
        st.markdown("### To")
        to_unit = st.selectbox('', ['meters', 'kilometers', 'miles', 'feet'],
                              key='length_to')
    result = convert_length(value, from_unit, to_unit)

elif category == 'Temperature':
    with unit_col1:
        st.markdown("### From")
        from_unit = st.selectbox('', ['Celsius', 'Fahrenheit'],
                                key='temp_from')
    with unit_col2:
        st.markdown("### To")
        to_unit = st.selectbox('', ['Celsius', 'Fahrenheit'],
                              key='temp_to')
    result = convert_temperature(value, from_unit, to_unit)

elif category == 'Weight':
    with unit_col1:
        st.markdown("### From")
        from_unit = st.selectbox('', ['kilograms', 'grams', 'pounds', 'ounces'],
                                key='weight_from')
    with unit_col2:
        st.markdown("### To")
        to_unit = st.selectbox('', ['kilograms', 'grams', 'pounds', 'ounces'],
                              key='weight_to')
    result = convert_weight(value, from_unit, to_unit)

# Display result with enhanced styling
st.markdown("---")
st.markdown(
    f"""
    <div class="result-container">
        <h3 style='text-align: center; color: black;'>Result</h3>
        <h2 style='text-align: center;  color: #2E86C1;'>{value} {from_unit} = {result:.4f} {to_unit}</h2>
    </div>
    """, 
    unsafe_allow_html=True
)

# Add information cards
st.markdown("---")
st.markdown("### Quick Reference")
info_col1, info_col2, info_col3 = st.columns([1, 1, 1])

with info_col1:
    st.info("📏 Length\n\n1 km = 1000 m\n1 mile = 1.60934 km")

with info_col2:
    st.info("🌡️ Temperature\n\n°F = (°C × 9/5) + 32\n°C = (°F - 32) × 5/9")

with info_col3:
    st.info("⚖️ Weight\n\n1 kg = 1000 g\n1 kg = 2.20462 lbs")
