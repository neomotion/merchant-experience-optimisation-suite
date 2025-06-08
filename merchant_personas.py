"""
REDUNDANT MODULE (can be referred to in the future for detailed merchant persona generation)

This file contains the MerchantPersona class and the MerchantPersonaManager class.
The MerchantPersona class is a dataclass that contains the attributes of a merchant persona.
The MerchantPersonaManager class is a class that contains the methods for managing merchant personas.
"""

from typing import Dict, List
from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path

class MerchantType(Enum):
    SMALL_BUSINESS = "small_business"
    ECOMMERCE = "ecommerce"
    RETAIL = "retail"
    SAAS = "saas"
    MARKETPLACE = "marketplace"
    FREELANCER = "freelancer"
    ENTERPRISE = "enterprise"

class BusinessStage(Enum):
    STARTUP = "startup"
    GROWING = "growing"
    ESTABLISHED = "established"
    SCALING = "scaling"

@dataclass
class MerchantPersona:
    name: str
    type: MerchantType
    stage: BusinessStage
    characteristics: Dict[str, str]
    pain_points: List[str]
    goals: List[str]
    preferences: Dict[str, str]
    metrics: Dict[str, float]
    behavior_patterns: List[str]
    tech_savviness: int  # 1-5 scale
    priority: int  # 1-5 scale

class MerchantPersonaManager:
    def __init__(self, processed_docs_path: str = "processed_documents"):
        self.processed_docs_path = Path(processed_docs_path)
        self.personas: Dict[str, MerchantPersona] = {}
        self.load_personas()

    def load_personas(self):
        """Load personas from processed documents."""
        # Example personas based on common merchant types
        self.personas = {
            "small_retail_merchant": MerchantPersona(
                name="Small Retail Merchant",
                type=MerchantType.RETAIL,
                stage=BusinessStage.GROWING,
                characteristics={
                    "business_size": "1-10 employees",
                    "location": "urban",
                    "customer_base": "local",
                    "inventory_size": "medium"
                },
                pain_points=[
                    "Inventory management",
                    "Cash flow management",
                    "Customer retention",
                    "Payment reconciliation"
                ],
                goals=[
                    "Increase sales",
                    "Improve customer experience",
                    "Streamline operations",
                    "Expand to online sales"
                ],
                preferences={
                    "payment_methods": "card, UPI, cash",
                    "reporting": "daily sales reports",
                    "support": "24/7 availability"
                },
                metrics={
                    "average_transaction": 1500.0,
                    "monthly_volume": 500000.0,
                    "mobile_percentage": 65.0
                },
                behavior_patterns=[
                    "Uses mobile app for daily operations",
                    "Prefers simple interfaces",
                    "Values quick support"
                ],
                tech_savviness=3,
                priority=4
            ),
            "ecommerce_startup": MerchantPersona(
                name="E-commerce Startup",
                type=MerchantType.ECOMMERCE,
                stage=BusinessStage.STARTUP,
                characteristics={
                    "business_size": "1-5 employees",
                    "platform": "own website",
                    "customer_base": "national",
                    "product_range": "niche"
                },
                pain_points=[
                    "Payment gateway integration",
                    "Cart abandonment",
                    "Shipping costs",
                    "Customer trust"
                ],
                goals=[
                    "Increase conversion rate",
                    "Reduce cart abandonment",
                    "Build brand trust",
                    "Scale operations"
                ],
                preferences={
                    "payment_methods": "card, UPI, netbanking",
                    "analytics": "real-time dashboard",
                    "automation": "high"
                },
                metrics={
                    "average_transaction": 2500.0,
                    "monthly_volume": 1000000.0,
                    "mobile_percentage": 75.0
                },
                behavior_patterns=[
                    "Data-driven decision making",
                    "Early adopter of new features",
                    "Values automation"
                ],
                tech_savviness=4,
                priority=5
            ),
            "saas_enterprise": MerchantPersona(
                name="SaaS Enterprise",
                type=MerchantType.SAAS,
                stage=BusinessStage.ESTABLISHED,
                characteristics={
                    "business_size": "100+ employees",
                    "customer_base": "global",
                    "revenue_model": "subscription",
                    "integration_needs": "complex"
                },
                pain_points=[
                    "Multi-currency support",
                    "Compliance requirements",
                    "Integration complexity",
                    "Scalability"
                ],
                goals=[
                    "Global expansion",
                    "Compliance automation",
                    "Integration efficiency",
                    "Customer success"
                ],
                preferences={
                    "payment_methods": "card, bank transfer, multiple currencies",
                    "reporting": "custom analytics",
                    "api": "comprehensive"
                },
                metrics={
                    "average_transaction": 50000.0,
                    "monthly_volume": 5000000.0,
                    "mobile_percentage": 40.0
                },
                behavior_patterns=[
                    "Enterprise-grade requirements",
                    "Long-term planning",
                    "Security focused"
                ],
                tech_savviness=5,
                priority=5
            ),
            "marketplace_seller": MerchantPersona(
                name="Marketplace Seller",
                type=MerchantType.MARKETPLACE,
                stage=BusinessStage.SCALING,
                characteristics={
                    "business_size": "5-20 employees",
                    "platforms": "multiple marketplaces",
                    "customer_base": "national",
                    "inventory": "diverse"
                },
                pain_points=[
                    "Multi-platform management",
                    "Order fulfillment",
                    "Payment reconciliation",
                    "Customer service"
                ],
                goals=[
                    "Cross-platform efficiency",
                    "Automated operations",
                    "Scalable processes",
                    "Customer satisfaction"
                ],
                preferences={
                    "payment_methods": "card, UPI, marketplace wallet",
                    "automation": "high",
                    "integration": "multi-platform"
                },
                metrics={
                    "average_transaction": 2000.0,
                    "monthly_volume": 2000000.0,
                    "mobile_percentage": 70.0
                },
                behavior_patterns=[
                    "Multi-tasking across platforms",
                    "Efficiency focused",
                    "Quick decision making"
                ],
                tech_savviness=4,
                priority=4
            ),
            "freelance_professional": MerchantPersona(
                name="Freelance Professional",
                type=MerchantType.FREELANCER,
                stage=BusinessStage.GROWING,
                characteristics={
                    "business_size": "solo",
                    "industry": "professional services",
                    "customer_base": "local/national",
                    "work_mode": "remote"
                },
                pain_points=[
                    "Invoice management",
                    "Payment tracking",
                    "Client communication",
                    "Time management"
                ],
                goals=[
                    "Streamline invoicing",
                    "Improve cash flow",
                    "Professional image",
                    "Client retention"
                ],
                preferences={
                    "payment_methods": "UPI, card, bank transfer",
                    "automation": "medium",
                    "reporting": "simple"
                },
                metrics={
                    "average_transaction": 10000.0,
                    "monthly_volume": 300000.0,
                    "mobile_percentage": 80.0
                },
                behavior_patterns=[
                    "Mobile-first approach",
                    "Time-sensitive",
                    "Self-service preference"
                ],
                tech_savviness=3,
                priority=3
            )
        }

    def get_persona(self, persona_id: str) -> MerchantPersona:
        """Get a specific persona by ID."""
        return self.personas.get(persona_id)

    def get_all_personas(self) -> Dict[str, MerchantPersona]:
        """Get all available personas."""
        return self.personas

    def get_personas_by_type(self, merchant_type: MerchantType) -> List[MerchantPersona]:
        """Get personas of a specific merchant type."""
        return [p for p in self.personas.values() if p.type == merchant_type]

    def get_personas_by_stage(self, stage: BusinessStage) -> List[MerchantPersona]:
        """Get personas at a specific business stage."""
        return [p for p in self.personas.values() if p.stage == stage]

    def get_high_priority_personas(self) -> List[MerchantPersona]:
        """Get personas with high priority (>=4)."""
        return [p for p in self.personas.values() if p.priority >= 4]

    def generate_persona_context(self, persona_id: str) -> str:
        """Generate a detailed context string for a persona."""
        persona = self.get_persona(persona_id)
        if not persona:
            return ""

        context = f"Merchant Persona: {persona.name}\n\n"
        context += f"Type: {persona.type.value}\n"
        context += f"Business Stage: {persona.stage.value}\n\n"
        
        context += "Characteristics:\n"
        for key, value in persona.characteristics.items():
            context += f"- {key}: {value}\n"
        
        context += "\nPain Points:\n"
        for point in persona.pain_points:
            context += f"- {point}\n"
        
        context += "\nGoals:\n"
        for goal in persona.goals:
            context += f"- {goal}\n"
        
        context += "\nPreferences:\n"
        for key, value in persona.preferences.items():
            context += f"- {key}: {value}\n"
        
        context += "\nMetrics:\n"
        for key, value in persona.metrics.items():
            context += f"- {key}: {value}\n"
        
        context += "\nBehavior Patterns:\n"
        for pattern in persona.behavior_patterns:
            context += f"- {pattern}\n"
        
        context += f"\nTech Savviness: {persona.tech_savviness}/5\n"
        context += f"Priority: {persona.priority}/5"
        
        return context

    def get_persona_suggestions(self, feature_type: str) -> List[str]:
        """Get suggested personas for a specific feature type."""
        suggestions = {
            "payment_processing": ["ecommerce_startup", "marketplace_seller", "saas_enterprise"],
            "analytics": ["saas_enterprise", "ecommerce_startup", "marketplace_seller"],
            "invoicing": ["freelance_professional", "small_retail_merchant"],
            "inventory": ["small_retail_merchant", "marketplace_seller"],
            "reporting": ["saas_enterprise", "ecommerce_startup"],
            "mobile_app": ["freelance_professional", "small_retail_merchant"],
            "api_integration": ["saas_enterprise", "marketplace_seller"],
            "compliance": ["saas_enterprise", "ecommerce_startup"],
            "customer_support": ["small_retail_merchant", "marketplace_seller"],
            "automation": ["marketplace_seller", "ecommerce_startup"]
        }
        return suggestions.get(feature_type, []) 