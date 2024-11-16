import os
from typing import List, Dict, Any
from chromadb import Client, Settings
from model_clients.clients import create_model_client
from handlers.logger import logger

class MerchantFeedbackSystem:
    def __init__(self, model_name: str = "Azure-gpt-model"):
        self.chroma_client = Client(Settings(
            persist_directory=os.path.join("processed_documents", "chroma_db")
        ))
        
        # Create or get the collection
        try:
            self.collection = self.chroma_client.get_collection("conversation_embeddings")
        except:
            self.collection = self.chroma_client.create_collection(
                name="conversation_embeddings",
                metadata={"description": "Processed conversation embeddings"}
            )
            
        self.model_client = create_model_client(model_name)
        
    def get_merchant_personas(self) -> List[Dict[str, Any]]:
        """Retrieve all merchant personas from the database."""
        results = self.collection.get()
        personas = []
        
        for metadata in results['metadatas']:
            if 'merchant_persona' in metadata:
                personas.append(metadata['merchant_persona'])
        
        return personas
    
    def get_design_feedback(self, design_description: str, merchant_type: str = None) -> Dict[str, Any]:
        """
        Get feedback on a design from merchant personas.
        
        Args:
            design_description: Description of the design/feature to get feedback on
            merchant_type: Optional filter for specific merchant types
        """
        # Get relevant merchant personas
        personas = self.get_merchant_personas()
        if merchant_type:
            personas = [p for p in personas if p.get('business_type') == merchant_type]
        
        if not personas:
            return {"error": "No matching merchant personas found"}
        
        # Prepare prompt for the model
        prompt = f"""
        You are an AI assistant analyzing a design from the perspective of different merchant personas.
        
        Design Description:
        {design_description}
        
        Merchant Personas:
        {personas}
        
        Please provide:
        1. General feedback on the design
        2. Specific feedback from each merchant persona's perspective
        3. Potential improvements based on merchant pain points and preferences
        4. Any usability concerns or suggestions
        
        Format the response in a clear, structured way.
        """
        
        try:
            response = self.model_client.Azure_client(prompt)
            return {
                "feedback": response,
                "merchant_count": len(personas),
                "merchant_types": list(set(p.get('business_type') for p in personas))
            }
        except Exception as e:
            logger.error(f"Error getting design feedback: {str(e)}")
            return {"error": str(e)}
    
    def query_merchant_knowledge(self, question: str, merchant_type: str = None) -> Dict[str, Any]:
        """
        Query the merchant knowledge base for specific information.
        
        Args:
            question: The question to ask about merchant behavior/preferences
            merchant_type: Optional filter for specific merchant types
        """
        # Query ChromaDB for relevant context
        results = self.collection.query(
            query_texts=[question],
            n_results=5
        )
        
        # Filter results by merchant type if specified
        relevant_docs = []
        for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
            if not merchant_type or metadata.get('merchant_persona', {}).get('business_type') == merchant_type:
                relevant_docs.append(doc)
        
        if not relevant_docs:
            return {"error": "No relevant information found"}
        
        # Prepare prompt for the model
        context = "\n".join(relevant_docs)
        prompt = f"""
        Based on the following merchant conversation data, please answer the question.
        
        Context:
        {context}
        
        Question:
        {question}
        
        Please provide a detailed answer based on the merchant behavior and preferences shown in the context.
        """
        
        try:
            response = self.model_client.Azure_client(prompt)
            return {
                "answer": response,
                "sources_used": len(relevant_docs)
            }
        except Exception as e:
            logger.error(f"Error querying merchant knowledge: {str(e)}")
            return {"error": str(e)}

def main():
    # Example usage
    feedback_system = MerchantFeedbackSystem()
    
    # Example design feedback
    design = """
    New checkout flow for merchants:
    - One-page checkout
    - Auto-save progress
    - Mobile-optimized interface
    - Integration with popular payment gateways
    """
    
    feedback = feedback_system.get_design_feedback(design, merchant_type="ecommerce")
    print("Design Feedback:", feedback)
    
    # Example knowledge query
    question = "What are common pain points for ecommerce merchants regarding payment processing?"
    answer = feedback_system.query_merchant_knowledge(question, merchant_type="ecommerce")
    print("\nKnowledge Query:", answer)

if __name__ == "__main__":
    main() 