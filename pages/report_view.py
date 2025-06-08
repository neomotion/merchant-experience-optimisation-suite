import streamlit as st
import plotly.graph_objects as go
import math

def create_meter_chart(score: float, rating: str):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score * 20,  # Convert 5-point scale to percentage
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1},
            'bar': {'color': "#1E88E5"},
            'steps': [
                {'range': [0, 40], 'color': "#EF5350"},
                {'range': [40, 60], 'color': "#FFA726"},
                {'range': [60, 80], 'color': "#66BB6A"},
                {'range': [80, 100], 'color': "#26A69A"}
            ],
        },
        title = {'text': rating}
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "#2196F3", 'family': "Arial"}
    )
    return fig

def show_report():
    if not st.session_state.test_results:
        st.error("No test results available. Please run a test first.")
        if st.button("Create New Test"):
            st.session_state.page = 'create_test'
            st.experimental_rerun()
        return
    
    results = st.session_state.test_results
    
    # Header with test details
    st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
    st.subheader("📊 Test Results")
    st.markdown(f"**Feature Tested:** {results['feature_text']}")
    st.markdown(f"**Flow Type:** {results['flow_type']}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Display results for each persona
    for persona, score in results['scores'].items():
        with st.container():
            st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
            st.markdown(f"### 👤 {persona.replace('_', ' ').title()}")
            
            # Calculate rating based on score
            rating = "Excellent" if score >= 4.5 else "Good" if score >= 4.0 else "Fair" if score >= 3.0 else "Poor"
            
            # Display score meter
            fig = create_meter_chart(score, rating)
            st.plotly_chart(fig, use_container_width=True)
            
            # Feedback sections
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 💡 Value & Usefulness")
                st.markdown("- Clear value proposition")
                st.markdown("- Meets merchant needs")
                st.markdown("- Solves key pain points")
            
            with col2:
                st.markdown("#### 🎯 Usability & Design")
                st.markdown("- Intuitive interface")
                st.markdown("- Efficient workflow")
                st.markdown("- Professional appearance")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Run New Test"):
            st.session_state.page = 'create_test'
            st.experimental_rerun()
    
    with col2:
        if st.download_button(
            "Download Report",
            data=str(results),
            file_name="test_results.json",
            mime="application/json"
        ):
            st.success("Report downloaded successfully!") 