import streamlit as st
import plotly.graph_objects as go
import math

# Custom CSS
st.markdown("""
<style>
    .report-header {
        background: linear-gradient(120deg, #2ecc71, #3498db);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .prompt-section {
        background: linear-gradient(120deg, #f6d365, #fda085);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .prompt-details {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .score-meter {
        text-align: center;
        margin: 1rem 0;
    }
    .feedback-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #3498db;
        height: 100%;
    }
    .merchant-quote {
        font-style: italic;
        color: #666;
        border-left: 3px solid #3498db;
        padding-left: 10px;
        margin: 10px 0;
        background-color: rgba(248, 249, 250, 0.5);
        padding: 0.8rem;
        border-radius: 0 8px 8px 0;
    }
    .category-header {
        color: #2c3e50;
        font-weight: 600;
        margin-top: 0.5rem;
        padding: 0.5rem;
        background-color: #e3f2fd;
        border-radius: 4px;
    }
    .persona-column {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        height: 100%;
    }
    .persona-name {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        padding: 0.5rem;
        background: #f8f9fa;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def create_meter_chart(score: float, rating: str):
    """Create a meter-style gauge chart using plotly"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score * 20,  # Convert 5-point scale to percentage
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1},
            'bar': {'color': "#2ecc71"},
            'steps': [
                {'range': [0, 40], 'color': "#ff6b6b"},
                {'range': [40, 60], 'color': "#ffd93d"},
                {'range': [60, 80], 'color': "#6c5ce7"},
                {'range': [80, 100], 'color': "#a8e6cf"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': score * 20
            }
        },
        title = {'text': rating, 'font': {'size': 20}}
    ))
    
    fig.update_layout(
        height=200,
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# Check if we have test results
if 'test_results' not in st.session_state or 'test_config' not in st.session_state:
    st.error("No test results found. Please run a test first.")
    st.stop()

# Header
st.markdown("""
<div class="report-header">
    <h1>📊 Test Results</h1>
    <p>Comprehensive analysis of your merchant experience test</p>
</div>
""", unsafe_allow_html=True)

# Display Prompt Summary
st.markdown("""
<div class="prompt-section">
    <h3>🎯 Test Configuration</h3>
    <div class="prompt-details">
""", unsafe_allow_html=True)

config = st.session_state.test_config
st.markdown(f"""
- **Feature Name:** {config['feature_name']}
- **Description:** {config['feature_description']}
- **Flow Type:** {config['flow_type']}
- **Selected Personas:** {', '.join([p.replace('_', ' ').title() for p in config['selected_personas']])}
""")

if config.get('image_path'):
    st.markdown("- **Interface Image:** Included")

st.markdown("</div></div>", unsafe_allow_html=True)

results = st.session_state.test_results

# Create columns for each persona
num_personas = len(results['test_results'])
cols = st.columns(num_personas)

# Display results for each persona
for idx, result in enumerate(results['test_results']):
    with cols[idx]:
        st.markdown('<div class="persona-column">', unsafe_allow_html=True)
        
        # Get persona name
        persona_id = result['persona']
        persona_name = personas.get(persona_id, {}).get('name', persona_id.replace('_', ' ').title())
        
        st.markdown(f"""
        <div class="persona-name">
            👤 {persona_name}
        </div>
        """, unsafe_allow_html=True)
        
        # Display usability score with meter chart
        score = result['usability_score']['score']
        rating = result['usability_score']['rating']
        meter_chart = create_meter_chart(score, rating)
        st.plotly_chart(meter_chart, use_container_width=True, key=f"meter_{idx}")
        
        # Display feedback summary
        summary = result['feedback_summary']
        for category, details in summary.items():
            with st.expander(f"📌 {category}", expanded=True):
                st.markdown(details['summary'])
                st.markdown(f"""
                <div class="merchant-quote">
                    "{details['quote']}"
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Export options in sidebar
st.sidebar.markdown("### 📤 Export Options")
if st.sidebar.button("Download Report", key="download"):
    # Here you would implement the report download functionality
    st.sidebar.success("Report downloaded successfully!")

# Show the tested image if available
if config.get('image_path'):
    st.sidebar.markdown("### 🖼️ Tested Interface")
    st.sidebar.image(config['image_path'], use_column_width=True)

# Navigation
st.sidebar.markdown("### 🔄 Actions")
if st.sidebar.button("Run New Test"):
    st.session_state.clear()
    st.switch_page("pages/1_��_Create_Test.py") 