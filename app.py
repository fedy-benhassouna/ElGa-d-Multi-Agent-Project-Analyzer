from typing import List, Literal, Dict, Optional
import streamlit as st
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
import os



# Set environment variable for Groq
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Explicitly disable OpenAI to prevent AutoGen from using it
os.environ.pop("OPENAI_API_KEY", None)  # Remove OpenAI API key if present

# Configure Groq LLM for AutoGen
# CRITICAL: AutoGen uses OpenAI API by default if base_url is not specified!
# Must specify base_url to force AutoGen to use Groq API endpoint instead
llm_config = {
    "config_list": [
        {
            "model": "openai/gpt-oss-20b",  # GPT-OSS-20B model hosted on Groq
            "api_key": GROQ_API_KEY,  # Use Groq API key
            "base_url": "https://api.groq.com/openai/v1",  # CRITICAL: Groq API endpoint (not OpenAI!)
        }
    ],
    "temperature": 0.7,
}

def init_session_state() -> None:
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False

def main() -> None:
    st.set_page_config(page_title="AI Services Agency", layout="wide")
    init_session_state()
    
    st.title("ElGaïd: Multi-Agent Project Analyzer")
    
    # Project Input Form
    with st.form("project_form"):
        st.subheader("Project Details")
        
        project_name = st.text_input("Project Name")
        project_description = st.text_area(
            "Project Description",
            help="Describe the project, its goals, and any specific requirements"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            project_type = st.selectbox(
                "Project Type",
                ["Web Application", "Mobile App", "API Development", 
                 "Data Analytics", "AI/ML Solution", "Other"]
            )
            timeline = st.selectbox(
                "Expected Timeline",
                ["1-2 months", "3-4 months", "5-6 months", "6+ months"]
            )
        
        with col2:
            budget_range = st.selectbox(
                "Budget Range",
                ["10k TND - 25k TND", "25k TND - 50k TND", "50k TND - 100k TND", "100k TND +"]
            )
            priority = st.selectbox(
                "Project Priority",
                ["High", "Medium", "Low"]
            )
        
        tech_requirements = st.text_area(
            "Technical Requirements (optional)",
            help="Any specific technical requirements or preferences"
        )
        
        special_considerations = st.text_area(
            "Special Considerations (optional)",
            help="Any additional information or special requirements"
        )
        
        submitted = st.form_submit_button("Analyze Project")
    
    if submitted and project_name and project_description:
        try:
            # Prepare project info
            project_info = f"""
PROJECT DETAILS:
==================
Name: {project_name}
Description: {project_description}
Type: {project_type}
Timeline: {timeline}
Budget: {budget_range}
Priority: {priority}
Technical Requirements: {tech_requirements if tech_requirements else 'Standard requirements'}
Special Considerations: {special_considerations if special_considerations else 'None'}
"""
            
            st.session_state.messages.append({"role": "user", "content": project_info})
            
            with st.spinner("AI Services Agency is analyzing your project..."):
                
                # Create User Proxy (simulates the user/client)
                user_proxy = UserProxyAgent(
                    name="Client",
                    system_message="You are the client representative. You provide project requirements and ask for analysis.",
                    code_execution_config=False,
                    human_input_mode="NEVER",
                    llm_config=llm_config
                )
                
                # Create CEO Agent
                ceo = AssistantAgent(
                    name="CEO",
                    system_message="""You are an experienced CEO who has led multiple successful companies. 
                    Your role is to evaluate project feasibility and provide strategic recommendations.
                    
                    Analyze the project and provide:
                    1. Project feasibility assessment
                    2. Market opportunity analysis
                    3. Risk assessment
                    4. Strategic recommendations
                    5. Success metrics and KPIs
                    
                    Be concise but comprehensive. Focus on business viability and strategic value.""",
                    llm_config=llm_config
                )
                
                # Create CTO Agent
                cto = AssistantAgent(
                    name="CTO",
                    system_message="""You are a senior technical architect with 15+ years of experience. 
                    Your role is to design technical architecture and select optimal technologies.
                    
                    Provide:
                    1. Recommended architecture (microservices/monolithic/serverless/hybrid)
                    2. Technology stack with justification
                    3. Scalability and performance considerations
                    4. Security implementation approach
                    5. Infrastructure requirements
                    6. Integration points and APIs
                    
                    Be specific about technologies and provide technical rationale.""",
                    llm_config=llm_config
                )
                
                # Create Product Manager Agent
                product_manager = AssistantAgent(
                    name="ProductManager",
                    system_message="""You are an experienced product manager who has launched multiple successful products.
                    Your role is to define product roadmap and ensure market success.
                    
                    Provide:
                    1. Product vision and objectives
                    2. Feature prioritization (MVP vs future releases)
                    3. Development phases with clear milestones
                    4. User stories and requirements
                    5. Success metrics and KPIs
                    6. Go-to-market strategy
                    
                    Focus on delivering value to users and achieving product-market fit.""",
                    llm_config=llm_config
                )
                
                # Create Lead Developer Agent
                developer = AssistantAgent(
                    name="LeadDeveloper",
                    system_message="""You are a senior full-stack developer with expertise in multiple technologies.
                    Your role is to plan technical implementation and provide realistic estimates.
                    
                    Provide:
                    1. Development approach and methodology (Agile/Scrum)
                    2. Detailed technology stack implementation
                    3. Effort estimates for each development phase
                    4. Team composition and roles needed
                    5. Development timeline with milestones
                    6. Cloud infrastructure costs (AWS/Azure/GCP)
                    7. Technical risks and mitigation strategies
                    
                    Be realistic about estimates and identify potential technical challenges.""",
                    llm_config=llm_config
                )
                
                # Create Client Success Manager Agent
                client_manager = AssistantAgent(
                    name="ClientSuccessManager",
                    system_message="""You are an experienced client success manager focused on delivery excellence.
                    Your role is to ensure client satisfaction and project success.
                    
                    Provide:
                    1. Communication plan and reporting structure
                    2. Customer acquisition and retention strategy
                    3. User onboarding process
                    4. Support and maintenance plan
                    5. Feedback collection mechanisms
                    6. Success metrics and monitoring approach
                    7. Risk management and escalation procedures
                    
                    Focus on building long-term client relationships and ensuring satisfaction.""",
                    llm_config=llm_config
                )
                
                # Create GroupChat for sequential analysis
                agents_list = [user_proxy, ceo, cto, product_manager, developer, client_manager]
                
                # Storage for individual responses
                responses = {
                    "ceo": "",
                    "cto": "",
                    "pm": "",
                    "dev": "",
                    "client": ""
                }
                
                # CEO Analysis
                st.info("🔄 CEO analyzing project feasibility...")
                ceo_chat = GroupChat(
                    agents=[user_proxy, ceo],
                    messages=[],
                    max_round=3,
                    speaker_selection_method='round_robin'  # Fix underpopulated GroupChat warning
                )
                ceo_manager = GroupChatManager(groupchat=ceo_chat, llm_config=llm_config)
                
                user_proxy.initiate_chat(
                    ceo_manager,
                    message=f"{project_info}\n\nAs the CEO, please analyze this project and provide your strategic assessment."
                )
                
                # Get CEO's response
                for msg in ceo_chat.messages:
                    if msg.get("name") == "CEO":
                        responses["ceo"] += msg.get("content", "") + "\n\n"
                
                # CTO Analysis
                st.info("🔄 CTO creating technical specifications...")
                cto_chat = GroupChat(
                    agents=[user_proxy, cto],
                    messages=[],
                    max_round=3,
                    speaker_selection_method='round_robin'  # Fix underpopulated GroupChat warning
                )
                cto_manager = GroupChatManager(groupchat=cto_chat, llm_config=llm_config)
                
                user_proxy.initiate_chat(
                    cto_manager,
                    message=f"{project_info}\n\nCEO's Analysis:\n{responses['ceo']}\n\nAs the CTO, please create detailed technical specifications."
                )
                
                for msg in cto_chat.messages:
                    if msg.get("name") == "CTO":
                        responses["cto"] += msg.get("content", "") + "\n\n"
                
                # Product Manager Analysis
                st.info("🔄 Product Manager creating roadmap...")
                pm_chat = GroupChat(
                    agents=[user_proxy, product_manager],
                    messages=[],
                    max_round=3,
                    speaker_selection_method='round_robin'  # Fix underpopulated GroupChat warning
                )
                pm_manager = GroupChatManager(groupchat=pm_chat, llm_config=llm_config)
                
                user_proxy.initiate_chat(
                    pm_manager,
                    message=f"{project_info}\n\nAs the Product Manager, please create a comprehensive product roadmap."
                )
                
                for msg in pm_chat.messages:
                    if msg.get("name") == "ProductManager":
                        responses["pm"] += msg.get("content", "") + "\n\n"
                
                # Developer Analysis
                st.info("🔄 Lead Developer planning implementation...")
                dev_chat = GroupChat(
                    agents=[user_proxy, developer],
                    messages=[],
                    max_round=3,
                    speaker_selection_method='round_robin'  # Fix underpopulated GroupChat warning
                )
                dev_manager = GroupChatManager(groupchat=dev_chat, llm_config=llm_config)
                
                user_proxy.initiate_chat(
                    dev_manager,
                    message=f"{project_info}\n\nTechnical Specs:\n{responses['cto']}\n\nAs the Lead Developer, provide implementation plan with cost estimates."
                )
                
                for msg in dev_chat.messages:
                    if msg.get("name") == "LeadDeveloper":
                        responses["dev"] += msg.get("content", "") + "\n\n"
                
                # Client Manager Analysis
                st.info("🔄 Client Success Manager creating strategy...")
                client_chat = GroupChat(
                    agents=[user_proxy, client_manager],
                    messages=[],
                    max_round=3,
                    speaker_selection_method='round_robin'  # Fix underpopulated GroupChat warning
                )
                client_mgr = GroupChatManager(groupchat=client_chat, llm_config=llm_config)
                
                user_proxy.initiate_chat(
                    client_mgr,
                    message=f"{project_info}\n\nAs the Client Success Manager, create a comprehensive client success strategy."
                )
                
                for msg in client_chat.messages:
                    if msg.get("name") == "ClientSuccessManager":
                        responses["client"] += msg.get("content", "") + "\n\n"
                
                # Display Results in Tabs
                tabs = st.tabs([
                    "CEO's Strategic Analysis",
                    "CTO's Technical Specification",
                    "Product Manager's Roadmap",
                    "Developer's Implementation Plan",
                    "Client Success Strategy"
                ])
                
                with tabs[0]:
                    st.markdown("## CEO's Strategic Analysis")
                    st.markdown(responses["ceo"] if responses["ceo"] else "No response generated.")
                    st.session_state.messages.append({"role": "assistant", "content": responses["ceo"]})
                
                with tabs[1]:
                    st.markdown("## CTO's Technical Specification")
                    st.markdown(responses["cto"] if responses["cto"] else "No response generated.")
                    st.session_state.messages.append({"role": "assistant", "content": responses["cto"]})
                
                with tabs[2]:
                    st.markdown("## Product Manager's Roadmap")
                    st.markdown(responses["pm"] if responses["pm"] else "No response generated.")
                    st.session_state.messages.append({"role": "assistant", "content": responses["pm"]})
                
                with tabs[3]:
                    st.markdown("## Lead Developer's Implementation Plan")
                    st.markdown(responses["dev"] if responses["dev"] else "No response generated.")
                    st.session_state.messages.append({"role": "assistant", "content": responses["dev"]})
                
                with tabs[4]:
                    st.markdown("## Client Success Strategy")
                    st.markdown(responses["client"] if responses["client"] else "No response generated.")
                    st.session_state.messages.append({"role": "assistant", "content": responses["client"]})
                
                st.success("✅ Analysis Complete!")
                st.session_state.analysis_complete = True
                
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")
            st.error("Please check your inputs and try again.")
            import traceback
            st.code(traceback.format_exc())
    
    # Sidebar Options
    with st.sidebar:
        st.header("🔧 Configuration")
        st.success("✅ Using Groq LLM")
        st.info("Model: openai/gpt-oss-20b")
        
        st.subheader("Options")
        if st.checkbox("Show Analysis History"):
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"][:500] + "..." if len(message["content"]) > 500 else message["content"])
        
        if st.button("Clear History"):
            st.session_state.messages = []
            st.session_state.analysis_complete = False
            st.rerun()

if __name__ == "__main__":
    main()