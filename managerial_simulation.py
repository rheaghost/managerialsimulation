import os
from crewai import Agent, Crew, Process, Task,LLM
# from crewai.llms import LLM

local_llm = LLM(
    model="ollama/llama3:latest",
    base_url="http://localhost:11434"
)

# =====================================================================
# 🎛️ SCENARIO CONFIGURATION (Change these to run different simulations!)
# =====================================================================
SCENARIO_TITLE = "Remote Work vs. Return to Office"

SCENARIO_DESCRIPTION = """
We are deciding whether to maintain our current 100% remote work policy 
or mandate a return to the physical office for at least 3 days a week.
"""

CTO_FOCUS = """How a physical presence or remote infrastructure impacts 
our digital security, tech stack, and software development velocity."""

CFO_FOCUS = """The financial impact of office leases, utility costs, 
potential employee turnover costs, and physical infrastructure asset management."""

OUTPUT_FILE = "CEO_Remote_vs_RTO_Decision.md"

# =====================================================================

# 1. DEFINE GENERALIZED AGENTS
cfo_agent = Agent(
    role="Chief Financial Officer (CFO)",
    goal=f"Analyze the strictly financial impact of: {SCENARIO_DESCRIPTION}",
    backstory=f"You are a data-driven financial officer. Your focus is: {CFO_FOCUS}",
    llm=local_llm,
    verbose=True,
    allow_delegation=False
)

cto_agent = Agent(
    role="Chief Technology Officer (CTO)",
    goal=f"Analyze the tech and strategic infrastructure impact of: {SCENARIO_DESCRIPTION}",
    backstory=f"You are a forward-looking technology strategist. Your focus is: {CTO_FOCUS}",
    llm=local_llm,
    verbose=True,
    allow_delegation=False
)

ceo_agent = Agent(
    role="Chief Executive Officer (CEO)",
    goal=f"Review the findings of both the CFO and CTO regarding {SCENARIO_TITLE}. Make a final executive recommendation.",
    backstory="""You are a pragmatic leader. You weigh aggressive growth and execution 
    against financial safety and employee retention to make the competitive call.""",
    llm=local_llm,
    verbose=True,
    allow_delegation=False
)

# 2. DEFINE DYNAMIC TASKS
task1 = Task(
    description=f"Analyze the financial risks and benefits regarding: {SCENARIO_DESCRIPTION}",
    expected_output="A list of financial pros and cons with estimated cost impact.",
    agent=cfo_agent
)

task2 = Task(
    description=f"Analyze the long-term technical and strategic advantages/disadvantages regarding: {SCENARIO_DESCRIPTION}",
    expected_output="A report focusing on operations, security, and execution velocity.",
    agent=cto_agent
)

task3 = Task(
    description=f"Review the CFO and CTO findings regarding {SCENARIO_TITLE}. Provide a final directive signed by the CEO.",
    expected_output="A final executive summary and directive signed by the CEO.",
    agent=ceo_agent,
    context=[task1, task2] 
)

# 3. ASSEMBLE AND RUN
board_meeting = Crew(
    agents=[cfo_agent, cto_agent, ceo_agent],
    tasks=[task1, task2, task3],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    print(f"Starting Board Meeting simulation for: {SCENARIO_TITLE}...")
    result = board_meeting.kickoff()
    
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(str(result))
        print(f"\n[SUCCESS] Transcript saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"\n[WARNING] Could not save file, but here is output:\n{result}")
