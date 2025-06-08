from typing import Dict, List
from dataclasses import dataclass
from enum import Enum

class FlowType(Enum):
    CHECKOUT = "checkout"
    PAYMENT = "payment"
    ONBOARDING = "onboarding"
    DASHBOARD = "dashboard"
    ANALYTICS = "analytics"
    GENERAL = "general"  # Added for universal UX principles
    ETHICAL = "ethical"  # New category for ethical design principles
    VISUAL = "visual"  # New category for visual design principles
    PRICING = "pricing"  # New category for pricing transparency
    CONTENT = "content"  # New category for UX writing principles
    GAMIFICATION = "gamification"  # New category for gamification principles
    CART = "cart"  # New category for cart and checkout optimization

@dataclass
class UXPrinciple:
    name: str
    description: str
    source: str
    category: str
    priority: int = 1  # 1-5, 5 being highest priority

class UXPrinciplesManager:
    def __init__(self):
        self.principles: Dict[FlowType, List[UXPrinciple]] = {
            FlowType.GENERAL: [
                # Aesthetic and Usability
                UXPrinciple(
                    name="Aesthetic-Usability Effect",
                    description="Users often perceive aesthetically pleasing design as design that's more usable",
                    source="Laws of UX",
                    category="Perception",
                    priority=5
                ),
                UXPrinciple(
                    name="Choice Overload",
                    description="The tendency for people to get overwhelmed when presented with too many options",
                    source="Laws of UX",
                    category="Decision Making",
                    priority=5
                ),
                UXPrinciple(
                    name="Chunking",
                    description="Breaking down information into meaningful groups to improve comprehension",
                    source="Laws of UX",
                    category="Information Architecture",
                    priority=5
                ),
                UXPrinciple(
                    name="Cognitive Load",
                    description="Minimize the mental resources needed to understand and interact with an interface",
                    source="Laws of UX",
                    category="Performance",
                    priority=5
                ),
                UXPrinciple(
                    name="Doherty Threshold",
                    description="Maintain system response times under 400ms for optimal productivity",
                    source="Laws of UX",
                    category="Performance",
                    priority=5
                ),
                UXPrinciple(
                    name="Fitts's Law",
                    description="Make interactive elements large enough and close enough to be easily acquired",
                    source="Laws of UX",
                    category="Interaction Design",
                    priority=5
                ),
                UXPrinciple(
                    name="Hick's Law",
                    description="Reduce the number and complexity of choices to speed up decision making",
                    source="Laws of UX",
                    category="Decision Making",
                    priority=5
                ),
                UXPrinciple(
                    name="Jakob's Law",
                    description="Follow established design patterns that users are familiar with",
                    source="Laws of UX",
                    category="Consistency",
                    priority=5
                ),
                UXPrinciple(
                    name="Law of Common Region",
                    description="Group related elements within clearly defined boundaries",
                    source="Laws of UX",
                    category="Visual Design",
                    priority=4
                ),
                UXPrinciple(
                    name="Law of Proximity",
                    description="Place related elements close to each other",
                    source="Laws of UX",
                    category="Visual Design",
                    priority=4
                ),
                UXPrinciple(
                    name="Law of Prägnanz",
                    description="Use simple, clear visual forms that require minimal cognitive effort",
                    source="Laws of UX",
                    category="Visual Design",
                    priority=4
                ),
                UXPrinciple(
                    name="Law of Similarity",
                    description="Use consistent visual styles for related elements",
                    source="Laws of UX",
                    category="Visual Design",
                    priority=4
                ),
                UXPrinciple(
                    name="Miller's Law",
                    description="Limit the number of items in working memory to 7±2",
                    source="Laws of UX",
                    category="Information Architecture",
                    priority=5
                ),
                UXPrinciple(
                    name="Occam's Razor",
                    description="Choose the simplest solution that works",
                    source="Laws of UX",
                    category="Design Philosophy",
                    priority=5
                ),
                UXPrinciple(
                    name="Paradox of the Active User",
                    description="Design for immediate use without requiring extensive learning",
                    source="Laws of UX",
                    category="Usability",
                    priority=5
                ),
                UXPrinciple(
                    name="Peak-End Rule",
                    description="Focus on creating positive peak and ending experiences",
                    source="Laws of UX",
                    category="User Experience",
                    priority=5
                ),
                UXPrinciple(
                    name="Postel's Law",
                    description="Be flexible with input but strict with output",
                    source="Laws of UX",
                    category="Error Handling",
                    priority=4
                ),
                UXPrinciple(
                    name="Serial Position Effect",
                    description="Place important information at the beginning and end of lists",
                    source="Laws of UX",
                    category="Information Architecture",
                    priority=4
                ),
                UXPrinciple(
                    name="Tesler's Law",
                    description="Some complexity is inherent and cannot be eliminated",
                    source="Laws of UX",
                    category="Design Philosophy",
                    priority=4
                ),
                UXPrinciple(
                    name="Von Restorff Effect",
                    description="Make important elements visually distinct",
                    source="Laws of UX",
                    category="Visual Design",
                    priority=4
                ),
                UXPrinciple(
                    name="Zeigarnik Effect",
                    description="Show progress for incomplete tasks to improve recall",
                    source="Laws of UX",
                    category="Task Management",
                    priority=4
                )
            ],
            FlowType.CHECKOUT: [
                # Core Checkout Principles
                UXPrinciple(
                    name="One-Click Checkout",
                    description="Enable quick purchase completion with pre-filled information",
                    source="Stripe",
                    category="Efficiency",
                    priority=5
                ),
                UXPrinciple(
                    name="Progress Indicators",
                    description="Show clear progress through checkout steps with visual indicators",
                    source="Stripe",
                    category="Navigation",
                    priority=5
                ),
                UXPrinciple(
                    name="Early Fee Disclosure",
                    description="Display all costs (taxes, fees, shipping) at the beginning of checkout",
                    source="Stripe",
                    category="Transparency",
                    priority=5
                ),
                UXPrinciple(
                    name="Smart Form Filling",
                    description="Support autofill and address validation to minimize input errors",
                    source="Stripe",
                    category="Efficiency",
                    priority=4
                ),
                UXPrinciple(
                    name="Guest Checkout",
                    description="Allow purchase completion without account creation",
                    source="Stripe",
                    category="Accessibility",
                    priority=5
                ),
                UXPrinciple(
                    name="Mobile Optimization",
                    description="Ensure fully responsive and touch-friendly checkout interface",
                    source="Stripe",
                    category="Responsiveness",
                    priority=5
                ),
                UXPrinciple(
                    name="Minimal Distractions",
                    description="Remove unnecessary elements during checkout to maintain focus",
                    source="Stripe",
                    category="Focus",
                    priority=4
                ),
                UXPrinciple(
                    name="Brand Consistency",
                    description="Maintain brand identity throughout checkout for trust",
                    source="Stripe",
                    category="Trust",
                    priority=4
                ),
                UXPrinciple(
                    name="Multiple Payment Options",
                    description="Support various payment methods including local options",
                    source="Stripe",
                    category="Flexibility",
                    priority=5
                ),
                UXPrinciple(
                    name="Security Indicators",
                    description="Display trust badges and security certifications prominently",
                    source="Stripe",
                    category="Trust",
                    priority=5
                ),
                UXPrinciple(
                    name="Error Prevention",
                    description="Implement real-time validation and clear error messages",
                    source="Stripe",
                    category="Error Handling",
                    priority=4
                ),
                UXPrinciple(
                    name="Address Validation",
                    description="Verify and correct addresses in real-time",
                    source="Stripe",
                    category="Data Quality",
                    priority=4
                ),
                UXPrinciple(
                    name="Order Summary",
                    description="Show clear itemized breakdown of costs and items",
                    source="Stripe",
                    category="Transparency",
                    priority=4
                ),
                UXPrinciple(
                    name="Return Policy Visibility",
                    description="Make return policies easily accessible during checkout",
                    source="Stripe",
                    category="Trust",
                    priority=3
                ),
                UXPrinciple(
                    name="Save for Later",
                    description="Allow customers to save cart for future purchase",
                    source="Stripe",
                    category="Flexibility",
                    priority=3
                )
            ],
            FlowType.PAYMENT: [
                UXPrinciple(
                    name="Multiple Payment Options",
                    description="Offer various payment methods including UPI, cards, net banking",
                    source="Stripe",
                    category="Flexibility",
                    priority=5
                ),
                UXPrinciple(
                    name="Secure Payment Indicators",
                    description="Clearly display security badges and trust indicators",
                    source="Stripe",
                    category="Trust",
                    priority=5
                ),
                UXPrinciple(
                    name="Save Payment Information",
                    description="Allow users to save payment methods for future use",
                    source="Stripe",
                    category="Convenience",
                    priority=4
                ),
                UXPrinciple(
                    name="Error Prevention",
                    description="Implement validation and clear error messages",
                    source="Don't Make Me Think",
                    category="Error Handling",
                    priority=4
                )
            ],
            FlowType.ONBOARDING: [
                UXPrinciple(
                    name="Progressive Disclosure",
                    description="Show information gradually as needed",
                    source="Don't Make Me Think",
                    category="Information Architecture",
                    priority=4
                ),
                UXPrinciple(
                    name="Clear Value Proposition",
                    description="Communicate benefits clearly to small businesses",
                    source="Meesho Tech",
                    category="Communication",
                    priority=5
                ),
                UXPrinciple(
                    name="Visual Guidance",
                    description="Use visual cues for tier 3/4 market users",
                    source="Meesho Tech",
                    category="Accessibility",
                    priority=4
                ),
                UXPrinciple(
                    name="Localized Content",
                    description="Use language and examples relevant to local context",
                    source="Meesho Tech",
                    category="Localization",
                    priority=5
                )
            ],
            FlowType.DASHBOARD: [
                UXPrinciple(
                    name="Information Hierarchy",
                    description="Organize information by importance and frequency of use",
                    source="Don't Make Me Think",
                    category="Layout",
                    priority=5
                ),
                UXPrinciple(
                    name="Action-Oriented Design",
                    description="Make common actions easily accessible",
                    source="GO-JEK",
                    category="Navigation",
                    priority=4
                ),
                UXPrinciple(
                    name="Real-time Updates",
                    description="Show live data and updates",
                    source="GO-JEK",
                    category="Performance",
                    priority=4
                ),
                UXPrinciple(
                    name="Customizable Views",
                    description="Allow users to customize their dashboard",
                    source="GO-JEK",
                    category="Personalization",
                    priority=3
                )
            ],
            FlowType.ANALYTICS: [
                UXPrinciple(
                    name="Data Visualization",
                    description="Use appropriate charts and graphs for data presentation",
                    source="GO-JEK",
                    category="Visualization",
                    priority=5
                ),
                UXPrinciple(
                    name="Actionable Insights",
                    description="Provide clear, actionable insights from data",
                    source="GO-JEK",
                    category="Value",
                    priority=5
                ),
                UXPrinciple(
                    name="Export Options",
                    description="Allow easy export of data in multiple formats",
                    source="GO-JEK",
                    category="Functionality",
                    priority=4
                ),
                UXPrinciple(
                    name="Performance Metrics",
                    description="Show key performance indicators prominently",
                    source="GO-JEK",
                    category="Metrics",
                    priority=4
                )
            ],
            FlowType.ETHICAL: [
                # Anti-Deceptive Patterns
                UXPrinciple(
                    name="Transparent Pricing",
                    description="Clearly display all costs, fees, and charges without hidden terms",
                    source="D91 Labs",
                    category="Transparency",
                    priority=5
                ),
                UXPrinciple(
                    name="No Forced Actions",
                    description="Avoid requiring unnecessary actions or permissions to proceed",
                    source="D91 Labs",
                    category="User Control",
                    priority=5
                ),
                UXPrinciple(
                    name="Clear Interface",
                    description="Maintain interface clarity without misleading elements or hidden options",
                    source="D91 Labs",
                    category="Interface Design",
                    priority=5
                ),
                UXPrinciple(
                    name="Minimal Nagging",
                    description="Limit notifications and prompts to essential communications",
                    source="D91 Labs",
                    category="Communication",
                    priority=4
                ),
                UXPrinciple(
                    name="Unobstructed Flow",
                    description="Ensure users can complete tasks without artificial barriers",
                    source="D91 Labs",
                    category="User Flow",
                    priority=5
                ),
                UXPrinciple(
                    name="No Sneaky Practices",
                    description="Avoid hidden costs, auto-renewals, or bundled products without clear disclosure",
                    source="D91 Labs",
                    category="Transparency",
                    priority=5
                ),
                UXPrinciple(
                    name="Genuine Social Proof",
                    description="Use authentic user reviews and testimonials without manipulation",
                    source="D91 Labs",
                    category="Trust",
                    priority=4
                ),
                UXPrinciple(
                    name="No False Urgency",
                    description="Avoid creating artificial time pressure or scarcity",
                    source="D91 Labs",
                    category="User Control",
                    priority=5
                ),
                UXPrinciple(
                    name="Clear Terms",
                    description="Present terms and conditions in clear, understandable language",
                    source="D91 Labs",
                    category="Transparency",
                    priority=4
                ),
                UXPrinciple(
                    name="Opt-In Defaults",
                    description="Set default options to the safest choice for users",
                    source="D91 Labs",
                    category="User Control",
                    priority=5
                ),
                UXPrinciple(
                    name="Easy Cancellation",
                    description="Make it as easy to cancel as it is to subscribe",
                    source="D91 Labs",
                    category="User Control",
                    priority=5
                ),
                UXPrinciple(
                    name="No Dark Patterns",
                    description="Avoid any design elements that manipulate user behavior",
                    source="D91 Labs",
                    category="Ethics",
                    priority=5
                ),
                UXPrinciple(
                    name="Accessible Information",
                    description="Ensure all important information is easily accessible and readable",
                    source="D91 Labs",
                    category="Transparency",
                    priority=4
                ),
                UXPrinciple(
                    name="Consistent Messaging",
                    description="Maintain consistent communication without misleading claims",
                    source="D91 Labs",
                    category="Communication",
                    priority=4
                ),
                UXPrinciple(
                    name="User-Centric Defaults",
                    description="Set default options that benefit the user, not the business",
                    source="D91 Labs",
                    category="Ethics",
                    priority=5
                )
            ],
            FlowType.VISUAL: [
                # Visual Cue Principles
                UXPrinciple(
                    name="High Visibility Filters",
                    description="Use visual elements instead of text for filtering options",
                    source="Meesho Tech",
                    category="Navigation",
                    priority=5
                ),
                UXPrinciple(
                    name="Visual Hierarchy",
                    description="Place most important filters in first two positions",
                    source="Meesho Tech",
                    category="Layout",
                    priority=5
                ),
                UXPrinciple(
                    name="Scroll Indicator",
                    description="Use partial button to indicate more options available",
                    source="Meesho Tech",
                    category="Navigation",
                    priority=4
                ),
                UXPrinciple(
                    name="Icon-Based Navigation",
                    description="Use clear, intuitive icons that work without text",
                    source="Meesho Tech",
                    category="Visual Design",
                    priority=5
                ),
                UXPrinciple(
                    name="Category Visualization",
                    description="Use appropriate images for each category filter",
                    source="Meesho Tech",
                    category="Visual Design",
                    priority=4
                ),
                UXPrinciple(
                    name="Dynamic Filtering",
                    description="Show relevant filters based on user behavior",
                    source="Meesho Tech",
                    category="Personalization",
                    priority=5
                ),
                UXPrinciple(
                    name="Filter Performance",
                    description="Rank and fix filters based on their performance",
                    source="Meesho Tech",
                    category="Optimization",
                    priority=4
                ),
                UXPrinciple(
                    name="Visual Consistency",
                    description="Maintain consistent visual style across filters",
                    source="Meesho Tech",
                    category="Visual Design",
                    priority=4
                ),
                UXPrinciple(
                    name="Screen Real Estate",
                    description="Optimize use of screen space for maximum impact",
                    source="Meesho Tech",
                    category="Layout",
                    priority=5
                ),
                UXPrinciple(
                    name="Progressive Disclosure",
                    description="Show additional options through scrolling",
                    source="Meesho Tech",
                    category="Navigation",
                    priority=4
                ),
                UXPrinciple(
                    name="Visual Feedback",
                    description="Provide clear visual feedback for user actions",
                    source="Meesho Tech",
                    category="Interaction",
                    priority=5
                ),
                UXPrinciple(
                    name="Cultural Relevance",
                    description="Use visuals that resonate with local market",
                    source="Meesho Tech",
                    category="Localization",
                    priority=5
                ),
                UXPrinciple(
                    name="Minimal Text",
                    description="Reduce reliance on text-based instructions",
                    source="Meesho Tech",
                    category="Accessibility",
                    priority=5
                ),
                UXPrinciple(
                    name="Visual Affordances",
                    description="Make interactive elements visually obvious",
                    source="Meesho Tech",
                    category="Interaction",
                    priority=4
                ),
                UXPrinciple(
                    name="Color and Contrast",
                    description="Use high contrast and culturally appropriate colors",
                    source="Meesho Tech",
                    category="Visual Design",
                    priority=4
                )
            ],
            FlowType.PRICING: [
                # Pricing Transparency Principles
                UXPrinciple(
                    name="Early Fee Disclosure",
                    description="Display nonstandard fees and special charges on product pages",
                    source="Nielsen Norman Group",
                    category="Transparency",
                    priority=5
                ),
                UXPrinciple(
                    name="Total Cost Visibility",
                    description="Show complete cost including all fees before checkout",
                    source="Nielsen Norman Group",
                    category="Transparency",
                    priority=5
                ),
                UXPrinciple(
                    name="Shipping Cost Calculator",
                    description="Allow users to calculate shipping costs on product pages",
                    source="Nielsen Norman Group",
                    category="Functionality",
                    priority=5
                ),
                UXPrinciple(
                    name="Fee Explanation",
                    description="Clearly explain the purpose of each fee",
                    source="Nielsen Norman Group",
                    category="Transparency",
                    priority=4
                ),
                UXPrinciple(
                    name="Prominent Fee Display",
                    description="Place fee information near the product price",
                    source="Nielsen Norman Group",
                    category="Layout",
                    priority=5
                ),
                UXPrinciple(
                    name="Progressive Disclosure",
                    description="Show basic fees upfront, detailed breakdowns on demand",
                    source="Nielsen Norman Group",
                    category="Information Architecture",
                    priority=4
                ),
                UXPrinciple(
                    name="International Shipping Clarity",
                    description="Clearly indicate international shipping costs and restrictions",
                    source="Nielsen Norman Group",
                    category="Transparency",
                    priority=5
                ),
                UXPrinciple(
                    name="Special Delivery Notice",
                    description="Highlight special delivery requirements and costs",
                    source="Nielsen Norman Group",
                    category="Transparency",
                    priority=4
                ),
                UXPrinciple(
                    name="Fee Consistency",
                    description="Maintain consistent fee terminology across the site",
                    source="Nielsen Norman Group",
                    category="Consistency",
                    priority=4
                ),
                UXPrinciple(
                    name="Tax Estimation",
                    description="Provide tax estimates based on location",
                    source="Nielsen Norman Group",
                    category="Functionality",
                    priority=4
                ),
                UXPrinciple(
                    name="Bulk Pricing Clarity",
                    description="Clearly show pricing for bulk or oversized items",
                    source="Nielsen Norman Group",
                    category="Transparency",
                    priority=4
                ),
                UXPrinciple(
                    name="Service Fee Transparency",
                    description="Explain service fees and their purpose",
                    source="Nielsen Norman Group",
                    category="Transparency",
                    priority=5
                ),
                UXPrinciple(
                    name="Installation Cost Clarity",
                    description="Show installation costs for applicable items",
                    source="Nielsen Norman Group",
                    category="Transparency",
                    priority=4
                ),
                UXPrinciple(
                    name="Fee Breakdown",
                    description="Provide detailed breakdown of all costs",
                    source="Nielsen Norman Group",
                    category="Transparency",
                    priority=4
                ),
                UXPrinciple(
                    name="No Hidden Costs",
                    description="Avoid revealing significant costs only at checkout",
                    source="Nielsen Norman Group",
                    category="Ethics",
                    priority=5
                )
            ],
            FlowType.CONTENT: [
                # UX Writing Principles
                UXPrinciple(
                    name="Clear Language",
                    description="Use simple, straightforward language that users can easily understand",
                    source="FinTech UX Writing",
                    category="Clarity",
                    priority=5
                ),
                UXPrinciple(
                    name="Concise Communication",
                    description="Be direct and to the point, avoiding unnecessary complexity",
                    source="FinTech UX Writing",
                    category="Clarity",
                    priority=5
                ),
                UXPrinciple(
                    name="Consistent Terminology",
                    description="Maintain consistent terms and phrases throughout the interface",
                    source="FinTech UX Writing",
                    category="Consistency",
                    priority=5
                ),
                UXPrinciple(
                    name="Jargon-Free Content",
                    description="Avoid financial jargon and technical terms unless necessary",
                    source="FinTech UX Writing",
                    category="Accessibility",
                    priority=5
                ),
                UXPrinciple(
                    name="Progressive Disclosure",
                    description="Reveal complex information gradually as needed",
                    source="FinTech UX Writing",
                    category="Information Architecture",
                    priority=4
                ),
                UXPrinciple(
                    name="Error Prevention",
                    description="Provide clear instructions and warnings to prevent user errors",
                    source="FinTech UX Writing",
                    category="Error Handling",
                    priority=5
                ),
                UXPrinciple(
                    name="Action-Oriented Text",
                    description="Use verbs and active voice to guide user actions",
                    source="FinTech UX Writing",
                    category="Interaction",
                    priority=4
                ),
                UXPrinciple(
                    name="Contextual Help",
                    description="Provide relevant help text exactly when users need it",
                    source="FinTech UX Writing",
                    category="Support",
                    priority=4
                ),
                UXPrinciple(
                    name="Brand Voice",
                    description="Maintain consistent brand voice and tone across all content",
                    source="FinTech UX Writing",
                    category="Branding",
                    priority=4
                ),
                UXPrinciple(
                    name="Accessible Content",
                    description="Ensure content is readable by screen readers and assistive technologies",
                    source="FinTech UX Writing",
                    category="Accessibility",
                    priority=5
                ),
                UXPrinciple(
                    name="Legal Compliance",
                    description="Ensure all content meets regulatory and legal requirements",
                    source="FinTech UX Writing",
                    category="Compliance",
                    priority=5
                ),
                UXPrinciple(
                    name="User-Centric Language",
                    description="Focus on user benefits and outcomes rather than features",
                    source="FinTech UX Writing",
                    category="User Focus",
                    priority=4
                ),
                UXPrinciple(
                    name="Clear Error Messages",
                    description="Provide specific, actionable error messages with solutions",
                    source="FinTech UX Writing",
                    category="Error Handling",
                    priority=5
                ),
                UXPrinciple(
                    name="Progressive Complexity",
                    description="Start with simple concepts and gradually introduce complexity",
                    source="FinTech UX Writing",
                    category="Learning",
                    priority=4
                ),
                UXPrinciple(
                    name="Trust-Building Content",
                    description="Use language that builds trust and confidence",
                    source="FinTech UX Writing",
                    category="Trust",
                    priority=5
                )
            ],
            FlowType.GAMIFICATION: [
                # Core Gamification Principles
                UXPrinciple(
                    name="Reward System",
                    description="Implement points, badges, and rewards for financial achievements",
                    source="FinTech Gamification",
                    category="Engagement",
                    priority=5
                ),
                UXPrinciple(
                    name="Progress Visualization",
                    description="Use progress bars and visual indicators to show financial goal progress",
                    source="FinTech Gamification",
                    category="Feedback",
                    priority=5
                ),
                UXPrinciple(
                    name="Financial Challenges",
                    description="Create engaging challenges and goals for saving and investing",
                    source="FinTech Gamification",
                    category="Motivation",
                    priority=5
                ),
                UXPrinciple(
                    name="Educational Gamification",
                    description="Use interactive quizzes and exercises to teach financial concepts",
                    source="FinTech Gamification",
                    category="Learning",
                    priority=5
                ),
                UXPrinciple(
                    name="Social Competition",
                    description="Implement leaderboards and social sharing for financial achievements",
                    source="FinTech Gamification",
                    category="Community",
                    priority=4
                ),
                UXPrinciple(
                    name="Personalized Goals",
                    description="Allow users to set and track personalized financial goals",
                    source="FinTech Gamification",
                    category="Personalization",
                    priority=5
                ),
                UXPrinciple(
                    name="Instant Feedback",
                    description="Provide immediate feedback for financial actions and achievements",
                    source="FinTech Gamification",
                    category="Feedback",
                    priority=5
                ),
                UXPrinciple(
                    name="Tiered Rewards",
                    description="Implement progressive reward levels based on user engagement",
                    source="FinTech Gamification",
                    category="Engagement",
                    priority=4
                ),
                UXPrinciple(
                    name="Visual Progress",
                    description="Use visual representations (like city building) for financial progress",
                    source="FinTech Gamification",
                    category="Visualization",
                    priority=4
                ),
                UXPrinciple(
                    name="Daily Challenges",
                    description="Offer daily financial tasks and challenges to maintain engagement",
                    source="FinTech Gamification",
                    category="Engagement",
                    priority=4
                ),
                UXPrinciple(
                    name="Achievement Unlocking",
                    description="Design progressive achievement system for financial milestones",
                    source="FinTech Gamification",
                    category="Motivation",
                    priority=4
                ),
                UXPrinciple(
                    name="Community Features",
                    description="Enable social interaction and community challenges",
                    source="FinTech Gamification",
                    category="Community",
                    priority=4
                ),
                UXPrinciple(
                    name="Reward Store",
                    description="Create a marketplace for redeeming earned points and rewards",
                    source="FinTech Gamification",
                    category="Engagement",
                    priority=4
                ),
                UXPrinciple(
                    name="Financial Literacy Games",
                    description="Develop interactive games for learning financial concepts",
                    source="FinTech Gamification",
                    category="Learning",
                    priority=4
                ),
                UXPrinciple(
                    name="Savings Challenges",
                    description="Implement competitive savings challenges with rewards",
                    source="FinTech Gamification",
                    category="Motivation",
                    priority=5
                )
            ],
            FlowType.CART: [
                # Core Cart Abandonment Prevention Principles
                UXPrinciple(
                    name="Progressive Profiling",
                    description="Collect customer information gradually over multiple visits",
                    source="E-commerce Best Practices",
                    category="Data Collection",
                    priority=5
                ),
                UXPrinciple(
                    name="One-Page Checkout",
                    description="Consolidate checkout process into a single page",
                    source="E-commerce Best Practices",
                    category="Efficiency",
                    priority=5
                ),
                UXPrinciple(
                    name="One-Click Checkout",
                    description="Enable instant checkout for returning customers",
                    source="E-commerce Best Practices",
                    category="Efficiency",
                    priority=5
                ),
                UXPrinciple(
                    name="Cost Transparency",
                    description="Display all costs and fees upfront",
                    source="E-commerce Best Practices",
                    category="Trust",
                    priority=5
                ),
                UXPrinciple(
                    name="Mobile Optimization",
                    description="Optimize checkout for mobile devices with clear CTAs",
                    source="E-commerce Best Practices",
                    category="Accessibility",
                    priority=5
                ),
                UXPrinciple(
                    name="Guest Checkout",
                    description="Allow purchases without account creation",
                    source="E-commerce Best Practices",
                    category="Accessibility",
                    priority=5
                ),
                UXPrinciple(
                    name="Trust Signals",
                    description="Display security badges and payment method icons",
                    source="E-commerce Best Practices",
                    category="Trust",
                    priority=5
                ),
                UXPrinciple(
                    name="Payment Options",
                    description="Offer multiple payment methods including digital wallets",
                    source="E-commerce Best Practices",
                    category="Flexibility",
                    priority=5
                ),
                UXPrinciple(
                    name="Cross-Channel Consistency",
                    description="Maintain consistent checkout experience across all channels",
                    source="E-commerce Best Practices",
                    category="Consistency",
                    priority=4
                ),
                UXPrinciple(
                    name="Checkout Analytics",
                    description="Track and analyze checkout metrics for optimization",
                    source="E-commerce Best Practices",
                    category="Analytics",
                    priority=4
                ),
                UXPrinciple(
                    name="Fraud Prevention",
                    description="Implement robust fraud detection without hindering legitimate purchases",
                    source="E-commerce Best Practices",
                    category="Security",
                    priority=5
                ),
                UXPrinciple(
                    name="Omnichannel Checkout",
                    description="Enable checkout on all customer touchpoints",
                    source="E-commerce Best Practices",
                    category="Accessibility",
                    priority=4
                ),
                UXPrinciple(
                    name="Cart Recovery",
                    description="Implement automated cart recovery emails with incentives",
                    source="E-commerce Best Practices",
                    category="Retention",
                    priority=4
                ),
                UXPrinciple(
                    name="Personalized Recommendations",
                    description="Show relevant product recommendations during checkout",
                    source="E-commerce Best Practices",
                    category="Personalization",
                    priority=4
                ),
                UXPrinciple(
                    name="Post-Purchase Engagement",
                    description="Maintain engagement after purchase with updates and reviews",
                    source="E-commerce Best Practices",
                    category="Retention",
                    priority=4
                ),
                UXPrinciple(
                    name="Loyalty Integration",
                    description="Integrate loyalty programs into checkout process",
                    source="E-commerce Best Practices",
                    category="Retention",
                    priority=4
                )
            ]
        }

    def get_principles_for_flow(self, flow_type: FlowType) -> List[UXPrinciple]:
        """Get all principles for a specific flow type."""
        return (self.principles.get(flow_type, []) + 
                self.principles.get(FlowType.GENERAL, []) + 
                self.principles.get(FlowType.ETHICAL, []) +
                self.principles.get(FlowType.VISUAL, []) +
                self.principles.get(FlowType.PRICING, []) +
                self.principles.get(FlowType.CONTENT, []) +
                self.principles.get(FlowType.GAMIFICATION, []) +
                self.principles.get(FlowType.CART, []))

    def get_high_priority_principles(self, flow_type: FlowType) -> List[UXPrinciple]:
        """Get high priority principles (priority >= 4) for a specific flow type."""
        flow_principles = self.principles.get(flow_type, [])
        general_principles = self.principles.get(FlowType.GENERAL, [])
        ethical_principles = self.principles.get(FlowType.ETHICAL, [])
        visual_principles = self.principles.get(FlowType.VISUAL, [])
        pricing_principles = self.principles.get(FlowType.PRICING, [])
        content_principles = self.principles.get(FlowType.CONTENT, [])
        gamification_principles = self.principles.get(FlowType.GAMIFICATION, [])
        cart_principles = self.principles.get(FlowType.CART, [])
        return [p for p in flow_principles + general_principles + ethical_principles + visual_principles + pricing_principles + content_principles + gamification_principles + cart_principles if p.priority >= 4]

    def get_principles_by_category(self, flow_type: FlowType, category: str) -> List[UXPrinciple]:
        """Get principles for a specific flow type and category."""
        flow_principles = self.principles.get(flow_type, [])
        general_principles = self.principles.get(FlowType.GENERAL, [])
        ethical_principles = self.principles.get(FlowType.ETHICAL, [])
        visual_principles = self.principles.get(FlowType.VISUAL, [])
        pricing_principles = self.principles.get(FlowType.PRICING, [])
        content_principles = self.principles.get(FlowType.CONTENT, [])
        gamification_principles = self.principles.get(FlowType.GAMIFICATION, [])
        cart_principles = self.principles.get(FlowType.CART, [])
        return [p for p in flow_principles + general_principles + ethical_principles + visual_principles + pricing_principles + content_principles + gamification_principles + cart_principles if p.category == category]

    def generate_prompt_context(self, flow_type: FlowType) -> str:
        """Generate a prompt context string with relevant principles."""
        principles = self.get_high_priority_principles(flow_type)
        context = f"UX Principles for {flow_type.value} flow:\n\n"
        
        # Group principles by category
        categories = {}
        for principle in principles:
            if principle.category not in categories:
                categories[principle.category] = []
            categories[principle.category].append(principle)
        
        # Format by category
        for category, principles in categories.items():
            context += f"\n{category}:\n"
            for principle in principles:
                context += f"- {principle.name}: {principle.description} (Priority: {principle.priority})\n"
        
        return context 