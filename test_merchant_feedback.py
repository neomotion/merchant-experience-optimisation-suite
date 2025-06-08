import os
from dotenv import load_dotenv
import json
from typing import List, Dict, Optional, Union
from merchant_feedback import MerchantFeedbackSystem
from handlers.logger import logger
from chroma_setup import ChromaDBManager
from model_clients.clients import create_model_client
from sentence_transformers import SentenceTransformer
import argparse
from datetime import datetime
from ux_principles import UXPrinciplesManager, FlowType
from PIL import Image
import base64
from io import BytesIO
import traceback
import uuid

from handlers.config_reader import ConfigReader

# Load environment variables
load_dotenv()
config = ConfigReader()
conf = config.read_config()

# Constants
MODEL_NAME = conf.get("model.model_name")
EMBEDDING_MODEL = conf.get("model.embedding_model")
DEFAULT_CHROMA_DIR = conf.get("sys_config.base_chromadb_dir")
DEFAULT_N_RESULTS = conf.get("sys_config.default_n_results")

# Initialize components
chroma_manager = ChromaDBManager(persist_directory=DEFAULT_CHROMA_DIR)
main_client = create_model_client(MODEL_NAME)
ux_manager = UXPrinciplesManager()

# Persona Definitions
personas = {
    "internet_first_entrepreneur": { # Combined Eagle + Fox
        "name": "Internet First Entrepreneur",
        "description": "A data-driven, innovative entrepreneur with a strong focus on user experience and strategic growth, blending agility with methodical decision-making.",
        "characteristics": """
        - Values long-term partnerships and embraces the latest technological advancements
        - Prioritizes user experience, continuous innovation, and data intelligence for decision-making
        - Methodical yet agile, open to experimentation and creative problem-solving
        - Focused on quality, data accuracy, and sustained market leadership
        - Manages complex sales funnels and payment flows with strategic precision
        - Balances resource constraints with a strong emphasis on brand identity and market reach
        - Tracks performance metrics closely and seeks self-serve capabilities
        - Analytical, design-savvy, adaptable, and user-centric
        - Represents the upper SME to MM premium segment
        """
    }, 
    "hybrid_emerging_business": {  # Combined Ox + Ant
        "name": "Hybrid Emerging Business",
        "description": "A resourceful, founder-driven business transitioning from traditional to digital with a cautious yet enterprising mindset.",
        "characteristics": """
        - Balances traditional business values with a willingness to adopt digital tools
        - Operates with limited resources and a trial-and-error approach to growth
        - Prefers familiar business metrics like GMV and RTO but open to learning new ones
        - Seeks easy-to-use, affordable digital solutions and DIY-friendly onboarding
        - Values proactive customer support and guidance, including social media advice
        - Price-sensitive and focused on customer acquisition and scaling challenges
        - Limited tech savviness but motivated to automate and streamline operations
        - Enterprising, cautious, and resourceful
        - Represents the emerging business segment
        """
    }
}


# Feature Testing Query Template
test_query_template = """
You are simulating a usability test as {persona_name}, representing {persona_description}

Merchant Characteristics:
{persona_characteristics}

Feature to Test: "{feature_description}"
{image_context}
Context: "{context}"

UX Principles to Consider:
{ux_principles}

Your goal is to assess the feature's usability and suggest improvements from your persona's perspective.
Consider these key aspects:

1. Value Offering
- How well does it address your business needs?
- Does it align with your segment's requirements ({persona_name})?
- What business value do you expect from this feature?

2. Feature Usefulness
- How practical is this feature for your business operations?
- Does it solve your specific pain points?
- What additional capabilities would make it more valuable?

3. Ease of Use
- How intuitive is the feature for your technical expertise level?
- Are the workflows aligned with your business processes?
- What aspects might be challenging for your segment?

4. Discoverability
- How easily can you find and understand the feature?
- Is the navigation logical for your business context?
- Are important functions clearly visible?

5. Design Appeal
- Does the design match your brand expectations?
- Is it visually appropriate for your business segment?
- Does it inspire confidence in using the feature?

Provide specific, actionable feedback that reflects:
- Your business segment's expectations
- Your technical comfort level
- Your typical workflow needs
- Your specific challenges
- Your success metrics

Format your response as if you were speaking directly about your experience with the feature.
"""

def analyze_image(image_path: str, model_name: str = MODEL_NAME) -> str:
    """
    Analyze image using LLM and return structured description

    Args:
        image_path: Path to image file for visual analysis
        model_name: Name of the model to use

    Returns:
        String containing the analysis
    """
    try:
        # Get basic image information
        img = img.resize((512, 512))  # Resize to reduce size
        width, height = img.size
        mode = img.mode
        format = img.format
        
        # Convert image to base64 for LLM analysis
        buffered = BytesIO()
        img.save(buffered, format="PNG", quality=85)  # Compress image
        buffered.seek(0)  # Important: seek back to the beginning
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Use LLM to analyze the image
        client = create_model_client(model_name)
        analysis_prompt = f"""
            Analyze this design interface image and provide a detailed description focusing on:
            1. UI Components and Layout
            2. Visual Design Elements
            3. User Interaction Points
            4. Accessibility Features
            5. Potential Usability Concerns
            
            Image Details:
            - Dimensions: {width}x{height} pixels
            - Format: {format}
            - Color Mode: {mode}
        """
        
        # Get analysis from LLM with image in the proper format
        analysis = client.send_request(analysis_prompt, base64_image)
        return analysis
    except Exception as e:
        logger.error(f"Error analyzing image: {str(e)}")
        return ""
        

def generate_context_keywords(text: str, image_path: Optional[str] = None, model_name: str = MODEL_NAME) -> str:
    """
    Generate keywords and summary from text and image context

    Args:
        text: Text description of the feature to test
        image_path: Path to image file for visual feedback
        model_name: Name of the model to use

    Returns:
        String containing the keywords and summary
    """
    try:
        client = create_model_client(model_name)
        
        # Prepare image context if provided
        image_context = ""
        if image_path and os.path.exists(image_path):
            image_analysis = analyze_image(image_path, model_name)
            image_context = f"\nVisual Design Analysis:\n{image_analysis}"
        
        context_prompt = f"""
        Analyze and extract key points from the following input:
        
        Text Description:
        {text}
        
        {image_context}
        
        Return a concise list of keywords and a brief summary that would be efficient to retrieve data from RAG.
        Focus on:
        1. Main features and functionality
        2. User experience aspects (including visual design if image provided)
        3. Technical requirements
        4. Business impact
        """

        result = client.send_request(context_prompt)
        return result
    except Exception as e:
        logger.error(f"Error generating context keywords: {str(e)}")
        return text  # Return original text on error

def calculate_usability_score(response: str, model_name: str = MODEL_NAME) -> float:
    """
    Calculate a usability score using the specified model to evaluate the response against design principles.
    Returns a score between 1.0 and 5.0.

    Args:
        response: Feedback from the merchant
        model_name: Name of the model to use

    Returns:
        Float score between 1.0 and 5.0
    """
    try:
        client = create_model_client(model_name)

        scoring_prompt = f"""
        Evaluate the following user test response against these core design principles:

        CORE DESIGN PRINCIPLES:
        1. User Experience & Interface
           - Clarity and ease of understanding
           - Consistent and predictable behavior
           - Mobile and device responsiveness
           - Error prevention and recovery

        2. Business Value & Efficiency
           - Task completion efficiency
           - Integration with existing workflows
           - Impact on business operations
           - ROI and performance metrics

        3. Merchant-Centric Features
           - Alignment with merchant needs
           - Learning curve and onboarding
           - Security and trust
           - Localization and customization

        USER TEST RESPONSE:
        {response}

        Rate the response on a scale of 1.0 to 5.0 where:
        1.0 = Very poor usability, major issues identified
        2.0 = Poor usability, significant issues present
        3.0 = Average usability, some issues noted
        4.0 = Good usability, minor issues only
        5.0 = Excellent usability, few or no issues

        Analyze the response thoroughly against each principle category, then provide a single decimal number between 1.0 and 5.0 as your final score. Only return the numerical score.
        """
        
        score_text = client.send_request(scoring_prompt)
        try:
            score = float(score_text.strip())
            return max(1.0, min(5.0, score))  # Clamp between 1.0 and 5.0
        except ValueError:
            logger.error(f"Invalid score format: {score_text}")
            return 3.0  # Default score on error
    except Exception as e:
        logger.error(f"Error calculating usability score: {str(e)}")
        return 3.0  # Default score on error

def format_feedback_summary(feedback: str, model_name: str = MODEL_NAME) -> Dict:
    """
    Format the feedback into a structured summary using the specified model.

    Args:
        feedback: Feedback from the merchant
        model_name: Name of the model to use

    Returns:
        Dictionary containing the structured summary
    """
    try:
        client = create_model_client(model_name)
        summary_prompt = f"""
        Analyze the following merchant feedback and extract key points for each category:
        {feedback}
        
        IMPORTANT: Return ONLY a valid JSON object with NO additional text or formatting (no markdown, no ```json tags).
        Follow this EXACT structure:
        {{
            "Value Offering": {{
                "summary": "Provide a detailed 2-3 line summary of how well the feature addresses business needs, including specific benefits and potential impact on operations.",
                "quote": "Direct quote from merchant about value"
            }},
            "Feature Usefulness": {{
                "summary": "Provide a detailed 2-3 line summary of the feature's practicality and benefits, including specific use cases and advantages.",
                "quote": "Direct quote from merchant about usefulness"
            }},
            "Ease of Use": {{
                "summary": "Provide a detailed 2-3 line summary of the feature's intuitiveness and simplicity, including specific aspects of the user experience.",
                "quote": "Direct quote from merchant about ease of use"
            }},
            "Discoverability": {{
                "summary": "Provide a detailed 2-3 line summary of how easy features are to find and understand, including specific navigation and guidance aspects.",
                "quote": "Direct quote from merchant about discoverability"
            }},
            "Design Appeal": {{
                "summary": "Provide a detailed 2-3 line summary of the visual and professional aspects, including specific design elements and aesthetics.",
                "quote": "Direct quote from merchant about design"
            }}
        }}
        """
        
        result = client.send_request(summary_prompt)

        # Log the raw response for debugging
        logger.info(f"Raw model response:\n{result}")
        
        # Clean the response to ensure we only have JSON
        result = result.strip()
        if result.startswith('```json'):
            result = result[7:]
        if result.endswith('```'):
            result = result[:-3]
        result = result.strip()

        logger.info(f"Cleaned response:\n{result}")
        
        try:
            return json.loads(result)
        except json.JSONDecodeError as je:
            logger.error(f"Initial JSON parsing failed: {str(je)}")
            # If parsing fails, try to extract just the JSON part
            start = result.find('{')
            end = result.rfind('}') + 1
            if start >= 0 and end > start:
                try:
                    cleaned_json = result[start:end]
                    # Replace any potential invalid characters
                    cleaned_json = cleaned_json.replace('\n', ' ').replace('\r', '')
                    logger.info(f"Attempting to parse extracted JSON:\n{cleaned_json}")
                    return json.loads(cleaned_json)
                except json.JSONDecodeError:
                    logger.error(f"Error parsing extracted JSON: {str(je)}")
                    return create_default_summary()
            else:
                logger.error("Could not find valid JSON structure in response")
                return create_default_summary()
    except Exception as e:
        logger.error(f"Error formatting feedback summary: {str(e)}")
        return create_default_summary()

def create_default_summary() -> Dict:
    """Create a default summary structure when parsing fails"""
    return {
        "Value_Offering": {
            "summary": "Error processing feedback",
            "quote": "N/A"
        },
        "Feature_Usefulness": {
            "summary": "Error processing feedback",
            "quote": "N/A"
        },
        "Ease_of_Use": {
            "summary": "Error processing feedback",
            "quote": "N/A"
        },
        "Discoverability": {
            "summary": "Error processing feedback",
            "quote": "N/A"
        },
        "Design_Appeal": {
            "summary": "Error processing feedback",
            "quote": "N/A"
        }
    }

def get_usability_rating(score: float) -> str:
    """Convert numerical score to descriptive rating"""
    if score >= 4.5:
        return "Excellent"
    elif score >= 4.0:
        return "Very Good"
    elif score >= 3.5:
        return "Good"
    elif score >= 3.0:
        return "Fair"
    elif score >= 2.5:
        return "Poor"
    else:
        return "Very Poor"

def run_feature_test(
    feature_text: str,
    flow_type: Optional[FlowType] = None,
    image_path: Optional[str] = None,
    persona_names: List[str] = None,
    model_name: str = MODEL_NAME
) -> Dict:
    """
    Run feature test with optional image analysis

    Args:
        feature_text: Text description of the feature to test
        flow_type: Type of user flow to test (e.g., CHECKOUT, PAYMENT, etc.)
        image_path: Path to image file for visual feedback
        persona_names: List of personas to test with
        model_name: Name of the model to use

    Returns:
        Dictionary containing results
    """
    try:
        client = create_model_client(model_name)
        
        # Step 1: Generate context from text and image
        context_query = generate_context_keywords(feature_text, image_path, model_name)
        logger.info(f"Context query: {context_query}")
        
        # Step 2: Retrieve context from ChromaDB
        chroma_results = chroma_manager.query(context_query)
        logger.info(f"ChromaDB RAG results: {json.dumps(chroma_results, indent=2)}")
        retrieved_docs_texts = []
        if chroma_results and chroma_results.get('documents') and \
           isinstance(chroma_results['documents'], list) and \
           len(chroma_results['documents']) > 0 and \
           isinstance(chroma_results['documents'][0], list):
            retrieved_docs_texts = chroma_results['documents'][0]
        else:
            logger.warning("ChromaDB RAG: No documents found or unexpected result structure.")
        
        context = "\n\n".join(retrieved_docs_texts)
        logger.info(f"ChromaDBContext: {context}")
        if not context:
            logger.info("ChromaDB RAG: Context is empty after retrieval and processing.")

        # Step 3: Get UX principles if flow type is provided
        ux_principles = ""
        if flow_type:
            principles = ux_manager.get_principles_for_flow(flow_type)
            ux_principles = "\n".join([f"- {p.name}: {p.description}" for p in principles])
        
        results = []
        for persona_name in (persona_names or ["internet_first_entrepreneur"]):
            if persona_name not in personas:
                logger.warning(f"Persona {persona_name} not found, skipping")
                continue
                
            persona = personas[persona_name]
                
            # Prepare test query
            query = test_query_template.format(
                persona_name=persona["name"],
                persona_description=persona["description"],
                persona_characteristics=persona["characteristics"],
                feature_description=feature_text,
                image_context=f"\nVisual Analysis:\n{analyze_image(image_path) if image_path else ''}",
                context=context,
                ux_principles=ux_principles
            )

            logger.info(f"Final Query Prompt: {query}")
            
            # Get feedback
            feedback = client.send_request(query)
            logger.info(f"Feedback: {feedback}")
            
            # Calculate usability score
            score = calculate_usability_score(feedback, model_name)
            logger.info(f"Usability Score: {score}")
            
            # Format feedback summary
            summary = format_feedback_summary(feedback, model_name)
            logger.info(f"Formated Feedback Summary: {summary}")
            
            results.append({
                "persona": persona_name,
                "usability_score": {
                    "score": score,
                    "rating": get_usability_rating(score)
                },
                "feedback_summary": summary,
                "raw_feedback": feedback
            })

            logger.info(f"Final Results: {results}")

            # Store the results in ChromaDB
            feedback_id = str(uuid.uuid4())
            chroma_manager.add_documents(
                documents=[feedback],
                ids=[feedback_id],
                metadatas=[{
                    "persona": persona_name,
                    "feature": feature_text,
                    "score": score,
                    "type": "feedback",
                    "original_id": feedback_id
                }]
            )
            
        return {
            "feature_name": feature_text.split(":")[0] if ":" in feature_text else feature_text,
            "flow_type": flow_type.value if flow_type else "general",
            "test_results": results
        }
        
    except Exception as e:
        logger.error(f"Error running feature test: {str(e)}\\n{traceback.format_exc()}")
        return {
            "feature_name": feature_text.split(":")[0] if ":" in feature_text else feature_text,
            "flow_type": flow_type.value if flow_type else "general",
            "test_results": []
        }

def test_merchant_feedback(feature_text: str, image_path: Optional[str] = None, 
                         selected_personas: Optional[List[str]] = None,
                         flow_type: Optional[FlowType] = None,
                         n_results: int = DEFAULT_N_RESULTS):
    """
    Run comprehensive merchant feedback tests
    
    Args:
        feature_text: Text description of the feature to test
        image_path: Path to image file for visual feedback
        selected_personas: List of personas to test with
        flow_type: Type of user flow to test (e.g., CHECKOUT, PAYMENT, etc.)
        n_results: Number of results to retrieve from ChromaDB
    """
    try:
        # Initialize the feedback system
        feedback_system = MerchantFeedbackSystem()
        
        # Run feature tests
        logger.info("Starting feature tests...")
        feedback_results = run_feature_test(
            feature_text,
            image_path,
            selected_personas,
            flow_type,
            n_results=n_results
        )
        
        print(f"\nFeature Feedback Results:")
        for persona, result in feedback_results.items():
            print(f"\n{persona} Feedback:")
            print(f"Usability Score: {result['usability_score']['score']:.1f} ({result['usability_score']['rating']})")
            print(f"Feedback: {result['raw_feedback']}")
            print(f"Context Used: {result['context_used'][:200]}...")
                
    except Exception as e:
        logger.error(f"Error in test_merchant_feedback: {str(e)}")
        raise

def extract_flow_type_from_text(text: str) -> Optional[FlowType]:
    """Extract flow type from feature text if not explicitly provided"""
    text_lower = text.lower()
    flow_type_mapping = {
        "checkout": FlowType.CHECKOUT,
        "payment": FlowType.PAYMENT,
        "onboarding": FlowType.ONBOARDING,
        "dashboard": FlowType.DASHBOARD,
        "analytics": FlowType.ANALYTICS,
        "general": FlowType.GENERAL,
        "ethical": FlowType.ETHICAL,
        "visual": FlowType.VISUAL,
        "pricing": FlowType.PRICING,
        "content": FlowType.CONTENT,
        "gamification": FlowType.GAMIFICATION,
        "cart": FlowType.CART
    }
    
    for flow_name, flow_type in flow_type_mapping.items():
        if flow_name in text_lower:
            return flow_type
    return None

def main():
    parser = argparse.ArgumentParser(description="Run merchant feedback tests")
    parser.add_argument("--feature_text", required=True, help="Feature description in format 'Feature name: Description'")
    parser.add_argument("--flow_type", choices=[f.value for f in FlowType], help="Type of user flow")
    parser.add_argument("--image", help="Path to image file for visual analysis")
    parser.add_argument("--personas", nargs="+", 
                       choices=["internet_first_entrepreneur",  # Combined Eagle + Fox
                               "hybrid_emerging_business"],     # Combined Ox + Ant
                       help="List of personas to test with")
    
    args = parser.parse_args()
    
    # Extract feature name and description
    feature_parts = args.feature_text.split(":", 1)
    feature_name = feature_parts[0].strip()
    feature_description = feature_parts[1].strip() if len(feature_parts) > 1 else feature_parts[0].strip()
    
    # Get flow type - first try explicit argument, then extract from text
    flow_type = None
    if args.flow_type:
        flow_type = FlowType(args.flow_type)
    else:
        flow_type = extract_flow_type_from_text(feature_description)
        if flow_type:
            logger.info(f"Extracted flow type '{flow_type.value}' from feature text")
    
    # Run test with default personas if none specified
    if not args.personas:
        args.personas = ["internet_first_entrepreneur"]  # Default to internet_first_entrepreneur
    
    # Run test
    results = run_feature_test(
        feature_text=feature_description,
        flow_type=flow_type,
        image_path=args.image,
        persona_names=args.personas
    )
    
    # Print results
    print("\n=== Test Results ===")
    print(f"Feature: {results['feature_name']}")
    print(f"Flow Type: {results['flow_type']}")
    print("\n--- Feedback Summary ---")
    
    for result in results["test_results"]:
        print(f"\nPersona: {result['persona']}")
        print(f"Usability Score: {result['usability_score']['score']:.1f} ({result['usability_score']['rating']})")
        
        summary = result["feedback_summary"]
        for category in ["Value_Offering", "Feature_Usefulness", "Ease_of_Use", "Discoverability", "Design_Appeal"]:
            if category in summary:
                print(f"\n{category}:")
                print(f"Summary: {summary[category].get('summary', 'N/A')}")
                print(f"Merchant Quote: \"{summary[category].get('quote', 'N/A')}\"")
    
    print("\n=== End of Results ===\n")

if __name__ == "__main__":
    main() 