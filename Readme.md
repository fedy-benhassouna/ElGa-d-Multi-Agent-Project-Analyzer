

#  **ElGaïd: Multi-Agent Project Analyzer**

### *An Autonomous Multi-Agent System for Project Evaluation & Technical Specification Generation*

---

## 📌 **Overview**

**ElGaïd** (القائد — *“The Leader”* in Tunisian/Arabic) is a **multi-agent analysis system** powered by **Groq LLMs** via the AutoGen framework.
The application takes a project's details and orchestrates **five specialized AI agents**—each representing a real enterprise role—to collaboratively produce:

* Strategic feasibility assessment
* Technical architecture
* Product roadmap
* Development plan + cost estimation
* Client success strategy

This project demonstrates **how to design, coordinate, and execute a multi-agent pipeline**, where each agent builds on the previous agent’s output in a controlled chain.

---

# 🧠 **System Architecture**

## 🔥 Multi-Agent Roles

ElGaïd uses **AutoGen’s GroupChat + GroupChatManager** and runs **isolated two-agent conversations** to control the flow and avoid cross-agent confusion.

Five specialized agents are defined:

| Agent                      | Role                                             |
| -------------------------- | ------------------------------------------------ |
| **CEO**                    | Evaluates business feasibility & strategy        |
| **CTO**                    | Produces technical architecture & stack          |
| **Product Manager**        | Defines roadmap, milestones & product vision     |
| **Lead Developer**         | Estimates costs, dev plan & technical risks      |
| **Client Success Manager** | Creates support, onboarding & communication plan |

Each agent has its own **system message**, optimized for consistent high-quality output.

---

## 🏗️ **Architecture Diagram**

![System Architecture](architecture_diagram.png)

*Figure 1: ElGaïd Multi-Agent System Architecture - Sequential workflow with isolated agent conversations*

---

# ⚙️ **Technical Flow**

### 1️⃣ **User Input Collection**

A Streamlit form collects:

* Project name
* Description
* Technical requirements
* Timeline, budget, priority
* Special considerations

These inputs are formatted into a **PROJECT DETAILS block** that is given to every agent.

---

### 2️⃣ **Multi-Agent Orchestration**

Unlike typical “all agents in one room” setups, ElGaïd uses a **deterministic sequential multi-agent workflow**:

```
Client Agent → CEO → CTO → Product Manager → Lead Developer → Client Success Manager
```

Each step uses:

```python
ceo_chat = GroupChat(
    agents=[user_proxy, ceo],
    messages=[],
    max_round=3,
    speaker_selection_method='round_robin'
)
```

This architecture ensures:

* No agent interruptions
* No context contamination
* Predictable outputs
* Clean logs

This pattern is ideal for **production-grade multi-agent systems**.


---

## 🔧 **Key Technologies**

| Component          | Description                               |
| ------------------ | ----------------------------------------- |
| **Groq LLM**       | Extremely fast inference for large models |
| **AutoGen**        | Multi-agent orchestration framework       |
| **Streamlit**      | Web UI layer                              |
| **UserProxyAgent** | Simulated user in agent conversations     |
| **AssistantAgent** | Autonomous specialized AI agents          |

---

# 🚀 **Installation**

### 1. Clone the project:

```bash
git clone https://github.com/your-username/elkaid-multiagent.git
cd elkaid-multiagent
```

### 2. Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Run:

```bash
streamlit run app.py
```

---

# 🎬 **Demo**

## Input Data Example

The following image shows an example of the input form with project details:

![Input Data Example](demo_input.png)

*Figure 2: Example input form showing project details (name, description, type, timeline, budget, etc.)*

## Results Video

Watch the video below to see ElGaïd in action, demonstrating the complete multi-agent analysis workflow and results:

https://github.com/user-attachments/assets/demo_results.mp4

*Video: Complete demonstration of ElGaïd multi-agent system analyzing a project and generating comprehensive outputs*

---

# 🤖 **Agent Definitions**

### CEO Agent

Strategic evaluation: feasibility, market potential, risks, KPIs.

### CTO Agent

Provides:

* Architecture (microservices, serverless, etc.)
* Stack recommendations
* Scalability strategy
* Security model
* Integration requirements

### Product Manager

Produces:

* Product vision
* MVP features
* Release roadmap
* User stories
* GTM strategy

### Lead Developer

Outputs:

* Technical implementation plan
* Task breakdown
* Cost estimation
* Cloud infrastructure setup
* Risk mitigation

### Client Success Manager

Generates:

* Communication plan
* Support strategy
* Onboarding flow
* Feedback loops
* Escalation procedures

---

# 🧩 **Multi-Agent Sequential Pipeline (Core Pattern)**

Example for CEO stage:

```python
ceo_chat = GroupChat(
    agents=[user_proxy, ceo],
    messages=[],
    max_round=3,
    speaker_selection_method='round_robin'
)

ceo_manager = GroupChatManager(groupchat=ceo_chat, llm_config=llm_config)

user_proxy.initiate_chat(
    ceo_manager,
    message=f"{project_info}\n\nAs the CEO, analyze this project."
)
```

This pattern is repeated for every agent.

---

# 🎨 **User Interface**

Streamlit tabs organize results:

* CEO's Analysis
* CTO's Technical Architecture
* Product Roadmap
* Dev Plan
* Client Success Strategy

Each tab displays the stored response for readability.

