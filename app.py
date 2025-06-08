import streamlit as st
import json
from datetime import datetime
import os
import time
from test_merchant_feedback import run_feature_test, FlowType, personas

# Set page config
st.set_page_config(
    page_title="AI Merchant Experience Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background: linear-gradient(90deg, #1E88E5 0%, #1565C0 100%);
        color: white;
        border: none;
        margin-top: 20px;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #1E88E5 0%, #1565C0 100%);
    }
    .welcome-container {
        background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .welcome-title {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .form-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 60vh;
        text-align: center;
    }
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .feedback-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .merchant-quote {
        font-style: italic;
        color: #666;
        border-left: 3px solid #1E88E5;
        padding-left: 1rem;
        margin: 1rem 0;
    }
    .prompt-section {
        margin-bottom: 2rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .prompt-details {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 8px;
        margin: 1rem;
    }
    .prompt-details h2 {
        color: #1E88E5;
        margin-bottom: 1.5rem;
    }
    .prompt-details h3 {
        color: #1565C0;
        margin: 1.5rem 0 1rem 0;
    }
    .prompt-details p {
        margin-bottom: 1rem;
        line-height: 1.6;
    }
    .feature-description {
        background: white;
        padding: 1rem;
        border-left: 4px solid #1E88E5;
        margin: 1rem 0;
    }
    .persona-column {
        padding: 1rem;
        border-radius: 8px;
        background: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .persona-name {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .score-section {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .score-value {
        font-size: 1.2rem;
        font-weight: bold;
    }
    .score-rating {
        font-size: 1.2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def save_test_results(results: dict):
    """Save test results to a JSON file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"processed_documents/test_results_{timestamp}.json"
    os.makedirs("processed_documents", exist_ok=True)
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    return filename

def main():
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 'create_test'
    if 'test_results' not in st.session_state:
        st.session_state.test_results = None
    
    # Header
    st.markdown("""
    <div class="welcome-container fade-in">
        <div class="welcome-title">Beta User: Synthetic Merchant</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("1️⃣ Create Test", use_container_width=True):
            st.session_state.page = 'create_test'
            st.rerun()
    with col2:
        if st.button("2️⃣ Run Test", use_container_width=True):
            if not st.session_state.get('feature_text'):
                st.error("Please create a test first!")
            else:
                st.session_state.page = 'running'
                st.rerun()
    with col3:
        if st.button("3️⃣ View Report", use_container_width=True):
            if not st.session_state.test_results:
                st.error("No test results available. Please run a test first!")
            else:
                st.session_state.page = 'report'
                st.rerun()
    
    # Main content based on current page
    if st.session_state.page == 'create_test':
        st.markdown('<div class="form-container fade-in">', unsafe_allow_html=True)
        st.subheader("📝 Create New Test")
        
        feature_text = st.text_area(
            "Describe the feature or interface you want to test", 
            placeholder="e.g., New checkout page design with international payment options",
            height=100
        )
        
        col1, col2 = st.columns(2)
        with col1:
            flow_type = st.selectbox(
                "Select Flow Type", 
                [flow.value for flow in FlowType]
            )
        
        with col2:
            # Persona selection
            st.markdown("""
            ### 👥 Select Test Personas
            Choose the merchant personas to test with:
            - Internet First Entrepreneur (Eagle + Fox)
            - Hybrid Emerging Business (Ox + Ant)
            """)
            personas_list = list(personas.keys())
            selected_personas = st.multiselect(
                "Select Test Personas",
                personas_list,
                default=["internet_first_entrepreneur"],
                help="Choose one or more personas to test the feature with"
            )
        
        # Optional image upload
        uploaded_file = st.file_uploader(
            "Upload interface image (optional)", 
            type=['png', 'jpg', 'jpeg']
        )
        
        if st.button("Save Test Configuration"):
            if not feature_text:
                st.error("Please describe the feature to test.")
            elif not selected_personas:
                st.warning("Please select at least one persona")
                st.stop()
            else:
                st.session_state.feature_text = feature_text
                st.session_state.flow_type = flow_type
                st.session_state.personas = selected_personas
                if uploaded_file:
                    # Save uploaded image
                    image_path = f"input/{uploaded_file.name}"
                    os.makedirs("input", exist_ok=True)
                    with open(image_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    st.session_state.image_path = image_path
                st.success("Test configuration saved! Click 'Run Test' to start analysis.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif st.session_state.page == 'running':
        with st.container():
            st.markdown('<div class="loading-container fade-in">', unsafe_allow_html=True)
            st.markdown("### 🔄 Analyzing Merchant Experience")
            progress = st.progress(0)
            
            steps = ["Initializing analysis...", 
                    "Processing feedback...",
                    "Preparing report..."]
            
            status = st.empty()
            for i, step in enumerate(steps):
                status.markdown(f"**{step}**")
                progress.progress((i + 1) * 33)
                time.sleep(1)
            
            # Run actual test using test_merchant_feedback
            try:
                results = run_feature_test(
                    feature_text=st.session_state.feature_text,
                    flow_type=FlowType(st.session_state.flow_type),
                    image_path=st.session_state.get('image_path'),
                    persona_names=st.session_state.personas
                )
                
                # Save results
                st.session_state.test_results = results
                save_test_results(results)
                
                st.session_state.page = 'report'
                st.rerun()
            except Exception as e:
                st.error(f"Error running test: {str(e)}")
                st.session_state.page = 'create_test'
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    elif st.session_state.page == 'report':
        st.markdown('<div class="form-container fade-in">', unsafe_allow_html=True)
        
        # Get results from session state
        results = st.session_state.test_results
        if not results:
            st.error("No test results available. Please run a test first!")
            if st.button("Create New Test"):
                st.session_state.page = 'create_test'
                st.rerun()
            st.stop()
        
        # Format timestamp
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        # Get friendly persona names - safely handle persona lookup
        selected_persona_names = []
        for test_result in results['test_results']:
            persona_id = test_result['persona']
            if isinstance(persona_id, str) and persona_id in personas:
                selected_persona_names.append(personas[persona_id]['name'])
            else:
                selected_persona_names.append(str(persona_id).replace('_', ' ').title())
        persona_list = ", ".join(selected_persona_names)
        
        # Display Test Configuration
        st.markdown("""
        <div class="prompt-section">
            <h2>🎯 Test Configuration</h2>
            <div class="prompt-details">
        """, unsafe_allow_html=True)
        
        # Feature Details Section
        st.subheader("Feature Details")
        st.markdown(f"""
        **Feature Name:**  
        {results['feature_name']}
        
        **Flow Type:**  
        {results['flow_type']}
        """)
        
        st.markdown("**Description:**")
        st.markdown(f"""
        <div class="feature-description">
        {st.session_state.feature_text}
        </div>
        """, unsafe_allow_html=True)
        
        # Test Parameters Section
        st.subheader("Test Parameters")
        st.markdown(f"""
        **Selected Personas:**  
        {persona_list}
        
        **Test Run:**  
        {timestamp}
        """)
        
        if 'image_path' in st.session_state and os.path.exists(st.session_state.image_path):
            st.markdown("**Interface Image:** Included _(viewable in sidebar)_")
            st.sidebar.markdown("### 🖼️ Tested Interface")
            st.sidebar.image(st.session_state.image_path)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Add some spacing
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Create columns for each persona
        num_personas = len(results['test_results'])
        if num_personas > 0:
            cols = st.columns(num_personas)
            
            # Display results for each persona in columns
            for idx, (col, test_result) in enumerate(zip(cols, results['test_results'])):
                with col:
                    st.markdown('<div class="persona-column">', unsafe_allow_html=True)
                    
                    # Get persona name
                    persona_id = test_result['persona']
                    persona_name = personas.get(persona_id, {}).get('name', persona_id.replace('_', ' ').title())
                    
                    # Persona name header
                    st.markdown(f"""
                    <div class="persona-name">
                        👤 {persona_name}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display usability score
                    score = test_result['usability_score']
                    st.markdown(f"""
                    <div class="score-section">
                        <div class="score-value">{score['score']}/5.0</div>
                        <div class="score-rating">{score['rating']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display feedback summary
                    for category, details in test_result['feedback_summary'].items():
                        with st.expander(f"📌 {category}", expanded=True):
                            st.markdown(details['summary'])
                            st.markdown(f"""
                            <div class="merchant-quote">
                                "{details['quote']}"
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No test results generated. Please check the logs for errors in the feedback generation process.")
        
        # Navigation buttons
        if st.button("Start New Test"):
            # Clear previous test data
            st.session_state.feature_text = None
            st.session_state.flow_type = None
            st.session_state.personas = None
            st.session_state.image_path = None
            st.session_state.test_results = None
            st.session_state.page = 'create_test'
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()