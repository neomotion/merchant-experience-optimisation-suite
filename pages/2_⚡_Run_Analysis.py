import streamlit as st
import time
from test_merchant_feedback import run_feature_test

st.set_page_config(page_title="Run Analysis", page_icon="⚡")

def run_analysis():
    if not st.session_state.get('feature_text'):
        st.error("No test configuration found. Please create a test first!")
        return
    
    # Check if we already have results for this exact configuration
    config_hash = f"{st.session_state.feature_text}_{st.session_state.flow_type}_{','.join(sorted(st.session_state.personas))}"
    
    if st.session_state.get('config_hash') == config_hash and st.session_state.get('test_results'):
        results = st.session_state.test_results
        st.success("✅ Using cached results!")
    else:
        with st.spinner("🔄 Running merchant feedback analysis..."):
            try:
                results = run_feature_test(
                    feature_text=st.session_state.feature_text,
                    flow_type=st.session_state.flow_type,
                    selected_personas=st.session_state.personas,
                    interface_image_path=st.session_state.get('image_path')
                )
                # Cache results with configuration hash
                st.session_state.test_results = results
                st.session_state.config_hash = config_hash
                st.success("✅ Analysis completed successfully!")
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                if st.button("Try Again"):
                    st.session_state.pop('test_results', None)
                    st.session_state.pop('config_hash', None)
                    st.rerun()
                return
    
    # Navigation options
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info("Click 'View Report' to see the detailed analysis")
    with col2:
        if st.button("View Report", type="primary"):
            st.session_state.page = 'report'
            st.rerun()

def main():
    st.title("⚡ Run Merchant Feedback Analysis")
    
    # Show test configuration
    st.subheader("📋 Test Configuration")
    st.markdown(f"""
    - **Feature Description:** {st.session_state.get('feature_text', 'Not set')}
    - **Flow Type:** {st.session_state.get('flow_type', 'Not set')}
    - **Selected Personas:** {', '.join(st.session_state.get('personas', []))}
    """)
    
    if st.session_state.get('image_path'):
        st.markdown("- **Interface Image:** Included ✓")
    
    # Run button
    if st.button("🚀 Run Analysis", type="primary", key="run_analysis"):
        run_analysis()
    elif st.session_state.get('test_results'):
        run_analysis()  # Show navigation if results exist

if __name__ == "__main__":
    main() 