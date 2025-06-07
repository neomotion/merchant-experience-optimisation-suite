import os
import re
import json
import uuid
import argparse
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from handlers.logger import logger

import nltk
import pandas as pd
from tqdm import tqdm
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from chroma_setup import ChromaDBManager
from docx import Document
import glob

# Download necessary NLTK data
nltk.download('punkt', quiet=True)

# Initialize sentence transformer model for embeddings
MODEL_NAME = 'all-MiniLM-L6-v2'


class ConversationProcessor:
    def __init__(self, input_dir: str, output_dir: str, chunk_size: int = 512, chunk_overlap: int = 100):
        """
        Initialize the conversation processor.

        Args:
            input_dir: Directory containing input files
            output_dir: Directory to save processed files
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Initialize text splitter for chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

        # Initialize sentence transformer model
        logger.info(f"Loading sentence transformer model: {MODEL_NAME}")
        self.model = SentenceTransformer(MODEL_NAME)

        # Initialize ChromaDB manager
        self.chroma_manager = ChromaDBManager(persist_directory=os.path.join(output_dir, "chroma_db"))
        self.collection = self.chroma_manager.collection

    def process_directory(self) -> None:
        """Process all files in the input directory."""
        # Get all .docx files in the input directory
        logger.info(f"Looking for .docx files in directory: {self.input_dir}")
        logger.info(f"Full path being searched: {os.path.join(self.input_dir, '*.docx')}")
        files = glob.glob(os.path.join(self.input_dir, "*.docx"))
        logger.info(f"Found {len(files)} files to process")
        if len(files) == 0:
            logger.info("No files found. Directory contents:")
            try:
                dir_contents = os.listdir(self.input_dir)
                logger.info(f"Directory contents: {dir_contents}")
            except Exception as e:
                logger.error(f"Error listing directory: {str(e)}")
            return

        all_processed_data = []
        successful_files = []
        failed_files = []

        for file_path in files:
            try:
                processed_data = self.process_file(file_path)
                if processed_data is None:
                    logger.error(f"Skipping file {file_path} due to processing error")
                    failed_files.append(os.path.basename(file_path))
                    continue
                
                # Save individual file results only if processing was successful
                output_file = os.path.join(
                    self.output_dir,
                    os.path.splitext(os.path.basename(file_path))[0] + "_processed.jsonl"
                )
                with open(output_file, "w") as f:
                    json.dump(processed_data, f)
                logger.info(f"Processed {os.path.basename(file_path)} and saved to {output_file}")
                
                all_processed_data.extend(processed_data["chunks"])
                successful_files.append(os.path.basename(file_path))
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {str(e)}")
                failed_files.append(os.path.basename(file_path))
                continue

        # Log processing summary
        logger.info("\nProcessing Summary:")
        logger.info(f"Total files: {len(files)}")
        logger.info(f"Successfully processed: {len(successful_files)}")
        logger.info(f"Failed to process: {len(failed_files)}")
        if successful_files:
            logger.info("Successfully processed files:")
            for file in successful_files:
                logger.info(f"- {file}")
        if failed_files:
            logger.info("Failed to process files:")
            for file in failed_files:
                logger.info(f"- {file}")

        # Save combined results only if there is data to save
        if all_processed_data:
            combined_output = os.path.join(self.output_dir, "all_conversations_processed.jsonl")
            with open(combined_output, "w") as f:
                json.dump(all_processed_data, f)
            logger.info(f"All processing complete. Combined output saved to {combined_output}")

            # Store in ChromaDB
            self.store_in_chromadb(all_processed_data)
        else:
            logger.warning("No data was successfully processed. No combined output file created.")

    def process_file(self, file_path: str) -> Dict[str, Any]:
        """Process a single conversation file."""
        try:
            logger.info(f"Processing file: {file_path}")
            
            # Extract raw text from docx
            doc = Document(file_path)
            paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
            
            if not paragraphs:
                logger.error(f"No content found in file {file_path}")
                return None
            
            # Skip any shell prompts or command outputs
            conversation_start = 0
            for i, para in enumerate(paragraphs):
                if para.startswith('Speaker') or (para.isupper() and len(para.split()) <= 3):
                    conversation_start = i
                    break
            
            if conversation_start == 0 and not any(para.startswith('Speaker') or (para.isupper() and len(para.split()) <= 3) for para in paragraphs):
                logger.error(f"No conversation found in file {file_path}")
                return None
            
            raw_text = "\n".join(paragraphs[conversation_start:])
            logger.info(f"Extracted {len(raw_text)} characters of raw text")

            # Clean text
            cleaned_text = self.clean_text(raw_text)
            logger.info("Text cleaned successfully")

            # Parse conversation
            conversation = self.parse_conversation(cleaned_text)
            if not conversation:
                logger.error(f"No valid conversation data found in file {file_path}")
                return None
                
            logger.info(f"Parsed {len(conversation)} conversation utterances")

            # Extract merchant persona
            merchant_persona = self.extract_merchant_persona(conversation)
            logger.info("Extracted merchant persona")

            # Anonymize PII
            anonymized_conversation = self.anonymize_pii(conversation)
            logger.info("Anonymized conversation data")

            # Chunk conversation
            chunked_data = self.chunk_conversation(anonymized_conversation, merchant_persona)
            if not chunked_data:
                logger.error(f"No valid chunks created from file {file_path}")
                return None
                
            logger.info(f"Created {len(chunked_data)} chunks")

            # Generate embeddings for each chunk and convert to list
            for chunk in chunked_data:
                embedding = self.model.encode(chunk["text"])
                chunk["embedding"] = embedding.tolist()  # Convert numpy array to list

            logger.info("Generated embeddings for chunks")

            # Prepare metadata as primitive types with safe defaults
            metrics = merchant_persona.get("metrics", {})
            metadata = {
                "file_path": str(file_path),
                "total_speakers": int(len(set(u["speaker_id"] for u in conversation))),
                "total_utterances": int(len(conversation)),
                "processed_at": datetime.now().isoformat(),
                "merchant_id": str(merchant_persona.get("merchant_id", "")),
                "business_type": str(merchant_persona.get("business_type", "")),
                "cart_conversion": float(metrics.get("cart_conversion", 0.0) or 0.0),
                "mobile_percentage": float(metrics.get("mobile_percentage", 0.0) or 0.0)
            }

            # Save processed data
            output = {
                "file_path": file_path,
                "chunks": chunked_data,
                "metadata": metadata,
                "conversation_history": [
                    {
                        "speaker": str(u["speaker"]),
                        "content": str(u["content"]),
                        "timestamp": str(u.get("timestamp", ""))
                    }
                    for u in conversation
                ]
            }
            
            return output

        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            return None

    def extract_metadata(self, file_path: str, text: str) -> Dict[str, Any]:
        """Extract metadata from the file."""
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        # Try to extract source from text if it follows your example format
        source_match = re.search(r'<source>(.*?)</source>', text)
        source = source_match.group(1) if source_match else filename

        return {
            "filename": filename,
            "file_path": file_path,
            "file_size": file_size,
            "source": source,
            "processed_date": datetime.now().isoformat(),
            "processor_version": "1.0"
        }

    def clean_text(self, text: str) -> str:
        """Clean and standardize the text."""
        # Remove any shell prompts or command outputs
        text = re.sub(r'\(venv\).*?\n', '', text)
        text = re.sub(r'\(dev-serve/default\).*?\n', '', text)
        text = re.sub(r'Command output:.*?\n', '', text)
        
        # Remove redundant whitespace while preserving line breaks
        lines = []
        for line in text.split('\n'):
            line = line.strip()
            if line:
                # Remove XML/HTML-like tags
                line = re.sub(r'<document.*?>|</document>|<document_content>|</document_content>|<source>.*?</source>', '', line)
                # Remove system messages
                if not line.startswith('System:'):
                    lines.append(line)
        
        return '\n'.join(lines)

    def parse_conversation(self, text: str) -> List[Dict[str, Any]]:
        """Parse conversation text into structured format."""
        conversation = []
        current_speaker = None
        current_timestamp = None
        current_content = []

        # Split into lines and remove empty lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Check for timestamp line
            if re.match(r'\d{2}:\d{2}\s*-\s*\d{2}:\d{2}', line):
                current_timestamp = line
                i += 1
                continue
                
            # Check for speaker line - now handles both "Speaker X" and actual names
            if line.startswith('Speaker') or (line.isupper() and len(line.split()) <= 3):
                # Save previous speaker's content if exists
                if current_speaker and current_content:
                    conversation.append({
                        "speaker": current_speaker,
                        "timestamp": current_timestamp,
                        "content": " ".join(current_content),
                        "speaker_id": current_speaker.split()[1] if current_speaker.startswith('Speaker') else current_speaker
                    })
                    current_content = []

                current_speaker = line
                i += 1
            else:
                current_content.append(line)
                i += 1

        # Add the last utterance if exists
        if current_speaker and current_content:
            conversation.append({
                "speaker": current_speaker,
                "timestamp": current_timestamp,
                "content": " ".join(current_content),
                "speaker_id": current_speaker.split()[1] if current_speaker.startswith('Speaker') else current_speaker
            })

        return conversation

    def standardize_timestamp(self, timestamp: str) -> Tuple[str, str]:
        """Standardize timestamp to ISO format."""
        match = re.match(r'(\d+):(\d+) - (\d+):(\d+)', timestamp)
        if match:
            start_min, start_sec, end_min, end_sec = match.groups()

            # Convert to seconds
            start_time_sec = int(start_min) * 60 + int(start_sec)
            end_time_sec = int(end_min) * 60 + int(end_sec)

            # Format as MM:SS
            start_time = f"{int(start_time_sec / 60):02d}:{start_time_sec % 60:02d}"
            end_time = f"{int(end_time_sec / 60):02d}:{end_time_sec % 60:02d}"

            return start_time, end_time

        raise ValueError(f"Invalid timestamp format: {timestamp}")

    def extract_merchant_persona(self, conversation: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract merchant persona from conversation data."""
        persona = {
            "merchant_id": None,
            "business_type": "ecommerce",  # Default based on conversation context
            "pain_points": [],
            "preferences": [],
            "behavior_patterns": [],
            "feedback": {
                "ui_feedback": [],
                "feature_feedback": [],
                "usability_feedback": []
            },
            "metrics": {
                "cart_conversion": None,
                "mobile_percentage": None
            },
            "conversation_history": []
        }
        
        # Extract merchant information from conversation
        for utterance in conversation:
            content = utterance["content"].lower()
            
            # Look for pain points
            pain_point_indicators = ["problem", "issue", "difficult", "challenge", "struggle", "concern"]
            if any(indicator in content for indicator in pain_point_indicators):
                persona["pain_points"].append(content)
            
            # Look for UI/UX preferences
            ui_indicators = ["design", "visual", "interface", "layout", "look", "feel"]
            if any(indicator in content for indicator in ui_indicators):
                persona["feedback"]["ui_feedback"].append(content)
            
            # Look for feature feedback
            feature_indicators = ["feature", "functionality", "option", "capability"]
            if any(indicator in content for indicator in feature_indicators):
                persona["feedback"]["feature_feedback"].append(content)
            
            # Look for usability feedback
            usability_indicators = ["easy", "difficult", "intuitive", "confusing", "clear", "simple"]
            if any(indicator in content for indicator in usability_indicators):
                persona["feedback"]["usability_feedback"].append(content)
            
            # Look for metrics
            if "cart to conversion" in content:
                match = re.search(r'(\d+)%', content)
                if match:
                    persona["metrics"]["cart_conversion"] = float(match.group(1))
            
            if "mobile" in content and "%" in content:
                match = re.search(r'(\d+)%', content)
                if match:
                    persona["metrics"]["mobile_percentage"] = float(match.group(1))
            
            # Store conversation history
            persona["conversation_history"].append({
                "speaker": utterance["speaker"],
                "content": utterance["content"],
                "timestamp": utterance.get("timestamp", "")
            })
        
        return persona

    def anonymize_pii(self, conversation: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Anonymize PII in the conversation."""
        pii_mapping = {}  # To maintain consistent replacements

        anonymized_conversation = []
        for utterance in conversation:
            content = utterance["content"]

            # Apply replacements
            anonymized_content = content
            for original, replacement in pii_mapping.items():
                anonymized_content = re.sub(rf'\b{re.escape(original)}\b', replacement, anonymized_content)

            # Additional regex patterns for common PII
            # Credit card numbers
            anonymized_content = re.sub(r'\b(?:\d{4}[-\s]?){3}\d{4}\b', '[CREDIT_CARD]', anonymized_content)

            # Email addresses not caught by NER
            anonymized_content = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]',
                                        anonymized_content)

            # Phone numbers not caught by NER
            anonymized_content = re.sub(r'\b(?:\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b', '[PHONE]',
                                        anonymized_content)

            # URLs
            anonymized_content = re.sub(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', '[URL]', anonymized_content)

            # Create a copy of the utterance and update content
            anonymized_utterance = utterance.copy()
            anonymized_utterance["content"] = anonymized_content
            anonymized_utterance["anonymized"] = True

            anonymized_conversation.append(anonymized_utterance)

        return anonymized_conversation

    def chunk_conversation(self, conversation: List[Dict[str, Any]], merchant_persona: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Chunk the conversation using Recursive Character Splitting."""
        # Combine all content for initial chunking
        full_text = "\n\n".join([f"{u['speaker']} ({u['timestamp']}): {u['content']}"
                                 for u in conversation if 'content' in u])

        # Split into chunks
        chunks = self.text_splitter.split_text(full_text)
        
        # Prepare chunks with metadata
        processed_chunks = []
        for i, chunk in enumerate(chunks):
            # Generate a unique ID for each chunk
            chunk_id = str(uuid.uuid4())
            
            # Get metrics with safe defaults
            metrics = merchant_persona.get("metrics", {})
            cart_conversion = metrics.get("cart_conversion")
            mobile_percentage = metrics.get("mobile_percentage")
            
            # Prepare flattened metadata as primitive types with safe defaults
            metadata = {
                "chunk_id": chunk_id,
                "merchant_id": str(merchant_persona.get("merchant_id", "")),
                "business_type": str(merchant_persona.get("business_type", "")),
                "cart_conversion": float(cart_conversion if cart_conversion is not None else 0.0),
                "mobile_percentage": float(mobile_percentage if mobile_percentage is not None else 0.0),
                "created_at": datetime.now().isoformat()
            }
            
            processed_chunks.append({
                "id": chunk_id,
                "text": chunk,
                "metadata": metadata
            })
        
        return processed_chunks

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using the sentence transformer model."""
        return self.model.encode(text)

    def store_in_chromadb(self, processed_data: List[Dict[str, Any]]) -> None:
        """Store processed data in ChromaDB."""
        logger.info(f"Storing {len(processed_data)} items in ChromaDB")
        try:
            # Extract required data
            ids = [item["id"] for item in processed_data]
            texts = [item["text"] for item in processed_data]
            metadatas = [item["metadata"] for item in processed_data]
            embeddings = [item["embedding"] for item in processed_data]
            
            # Store in ChromaDB
            self.chroma_manager.add_documents(
                documents=texts,
                metadatas=metadatas,
                ids=ids,
                embeddings=embeddings
            )
            
            # Verify storage
            collection_count = self.chroma_manager.collection.count()
            logger.info(f"Verified ChromaDB collection count: {collection_count}")
            
            logger.info("Successfully stored data in ChromaDB")
        except Exception as e:
            logger.error(f"Error storing data in ChromaDB: {str(e)}")
            raise


def main():
    parser = argparse.ArgumentParser(description='Process conversation data files')
    parser.add_argument('--input_dir', type=str, default='input', help='Directory containing input files')
    parser.add_argument('--output_dir', type=str, default='processed_documents', help='Directory to save processed files')
    parser.add_argument('--chunk_size', type=int, default=512, help='Size of text chunks')
    parser.add_argument('--chunk_overlap', type=int, default=100, help='Overlap between chunks')

    args = parser.parse_args()

    # Create processor and run
    processor = ConversationProcessor(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap
    )

    processor.process_directory()


if __name__ == "__main__":
    main()