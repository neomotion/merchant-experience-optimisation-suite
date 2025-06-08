import streamlit as st
import os
from test_merchant_feedback import FlowType, personas
from PIL import Image
import json
from datetime import datetime

# Custom CSS
st.markdown("""
<style>
    .stTextInput, .stTextArea {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 10px;
    }
    .stButton > button {
        width: 100%;
        border-radius: 20px;
        padding: 10px 24px;
        background-color: #007bff;
        color: white;
    }
    .stButton > button:hover {
        background-color: #0056b3;
    }
    .form-header {
        background: linear-gradient(120deg, #007bff, #00bcd4);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .form-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #007bff;
    }
    .helper-text {
        color: #666;
        font-size: 0.9rem;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'test_config' not in st.session_state:
    st.session_state.test_config = {
        'feature_name': '',
        'feature_description': '',
        'flow_type': None,
        'selected_personas': [],
        'image_path': None
    }

# Header
st.markdown("""
<div class="form-header">
    <h1>🎯 Create Test</h1>
    <p>Configure your merchant experience test</p>
</div>
""", unsafe_allow_html=True)

# Main form
with st.form("test_creation_form"):
    # Feature Information Section
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.subheader("📝 Feature Information")
    
    feature_name = st.text_input(
        "Feature Name",
        placeholder="e.g., International Checkout",
        help="Enter a concise name for the feature being tested"
    )
    
    feature_description = st.text_area(
        "Feature Description",
        placeholder="Describe the key features, changes, and improvements...",
        help="Provide detailed information about the feature's functionality and purpose",
        height=150
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Test Configuration Section
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.subheader("⚙️ Test Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        flow_types = [ft.value for ft in FlowType]
        flow_type = st.selectbox(
            "Flow Type",
            flow_types,
            help="Select the type of user flow being tested"
        )
    
    with col2:
        available_personas = list(personas.keys())
        persona_help = """
        Choose the merchant personas to test with:
        - Internet First Key Account (Eagle): MM premium, data-driven decision makers
        - Internet First Startup (Fox): Upper SME/MM, UX-focused innovators
        - Offline First Business (Ox): Emerging, traditional businesses
        - Enterprise Strategic (Elephant): Enterprise/MM premium, established brands
        - Online First Emerging (Ant): Emerging, founder-driven startups
        """
        selected_personas = st.multiselect(
            "Select Personas",
            available_personas,
            default=["internet_first_startup", "enterprise_strategic"],  # Default to Fox and Elephant
            help=persona_help,
            format_func=lambda x: personas[x]["name"]  # Display friendly names
        )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Interface Upload Section
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.subheader("🖼️ Interface Upload")
    
    uploaded_file = st.file_uploader(
        "Upload Interface Image",
        type=["png", "jpg", "jpeg"],
        help="Upload a screenshot or mockup of the interface"
    )
    
    if uploaded_file:
        st.image(uploaded_file, caption="Preview", use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Submit button
    submitted = st.form_submit_button("Start Analysis", type="primary")
    
    if submitted and feature_name and feature_description:
        # Save image if provided
        image_path = None
        if uploaded_file:
            image = Image.open(uploaded_file)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = f"input/{timestamp}_{uploaded_file.name}"
            os.makedirs("input", exist_ok=True)
            image.save(image_path)
        
        # Save configuration to session state
        st.session_state.test_config = {
            'feature_name': feature_name,
            'feature_description': feature_description,
            'flow_type': flow_type,
            'selected_personas': selected_personas,
            'image_path': image_path
        }
        
        # Redirect to analysis page
        st.success("Test configuration saved! Redirecting to analysis...")
        st.switch_page("pages/2_⚡_Run_Analysis.py")
    elif submitted:
        st.error("Please provide both feature name and description.") 