from typing import TypedDict

from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.tools import tool


# =====================================================
# LLM
# =====================================================

llm = ChatOllama(
    model="llama3.2",
    temperature=0

)


# =====================================================
# TOOLS
# =====================================================

@tool
def user_lookup(username: str) -> str:
    """Lookup employee details"""

    users = {
        "himanshu": "QA Engineer",
        "john": "DevOps Engineer",
        "alice": "HR Manager"
    }

    return users.get(username.lower(), "User not found")


@tool
def password_reset(username: str) -> str:
    """Reset user password"""

    return f"Password reset email sent to {username}"


@tool
def create_ticket(issue: str) -> str:
    """Create support ticket"""

    return f"Ticket INC1001 created for issue: {issue}"


@tool
def system_status(system_name: str) -> str:
    """Check system status"""

    systems = {
        "jira": "JIRA is UP",
        "vpn": "VPN is DOWN",
        "confluence": "Confluence is UP"
    }

    return systems.get(system_name.lower(), "System not found")


@tool
def knowledge_base(query: str) -> str:
    """Search KB"""

    articles = {
        "vpn": "Restart VPN client and reconnect.",
        "wifi": "Restart router and network adapter.",
        "email": "Check Outlook configuration."
    }

    for key in articles:
        if key in query.lower():
            return articles[key]

    return "No article found"


@tool
def calculator(expression: str) -> str:
    """Perform calculations"""

    try:
        return str(eval(expression))
    except:
        return "Invalid expression"


# =====================================================
# STATE
# =====================================================

class AgentState(TypedDict):
    user_input: str
    actions: list
    results: list
    final_answer: str


# =====================================================
# ROUTER
# =====================================================

def router(state: AgentState):

    query = state["user_input"].lower()

    actions = []

    if "lookup" in query:
        actions.append("lookup")

    if "reset password" in query:
        actions.append("reset")

    if "ticket" in query:
        actions.append("ticket")

    if "status" in query:
        actions.append("status")

    if any(op in query for op in ["+", "-", "*", "/"]):
        actions.append("calculator")

    if any(word in query for word in ["vpn", "wifi", "email"]):
        actions.append("kb")

    if not actions:
        actions.append("kb")

    return {"actions": actions}


# =====================================================
# EXECUTE TOOLS
# =====================================================

def execute_tools(state: AgentState):

    query = state["user_input"].lower()

    results = []

    for action in state["actions"]:

        if action == "lookup":

            username = query.split()[-1]

            output = user_lookup.invoke(
                {"username": username}
            )

            results.append({
                "tool": "lookup",
                "result": output
            })

        elif action == "reset":

            username = query.split()[-1]

            output = password_reset.invoke(
                {"username": username}
            )

            results.append({
                "tool": "reset",
                "result": output
            })

        elif action == "ticket":

            output = create_ticket.invoke(
                {"issue": query}
            )

            results.append({
                "tool": "ticket",
                "result": output
            })

        elif action == "status":

            system = "vpn"

            if "jira" in query:
                system = "jira"

            elif "confluence" in query:
                system = "confluence"

            output = system_status.invoke(
                {"system_name": system}
            )

            results.append({
                "tool": "status",
                "result": output
            })

        elif action == "calculator":

            output = calculator.invoke(
                {"expression": query}
            )

            results.append({
                "tool": "calculator",
                "result": output
            })

        elif action == "kb":

            output = knowledge_base.invoke(
                {"query": query}
            )

            results.append({
                "tool": "kb",
                "result": output
            })

    return {"results": results}


# =====================================================
# RESPONSE NODE
# =====================================================

def response_node(state: AgentState):

    tool_results = "\n".join(
        [
            f"{r['tool']} -> {r['result']}"
            for r in state["results"]
        ]
    )

    prompt = f"""
    You are an IT Support Assistant.

    User Request:
    {state['user_input']}

    Tool Results:
    {tool_results}

    Create a concise professional response.
    """

    response = llm.invoke(prompt)

    return {
        "final_answer": response.content
    }


# =====================================================
# BUILD GRAPH
# =====================================================

builder = StateGraph(AgentState)

builder.add_node("router", router)
builder.add_node("execute_tools", execute_tools)
builder.add_node("response", response_node)

builder.set_entry_point("router")

builder.add_edge("router", "execute_tools")
builder.add_edge("execute_tools", "response")
builder.add_edge("response", END)

graph = builder.compile()


# =====================================================
# MAIN
# =====================================================

# =====================================================
# MAIN
# =====================================================

def run_cli():
    """
    Interactive CLI for manual testing
    """

    while True:

        user_input = input(
            "\nAsk something (or type exit): "
        )

        if user_input.lower() == "exit":
            break

        result = graph.invoke({
            "user_input": user_input
        })

        print("\n====================")
        print("TOOLS EXECUTED")
        print("====================")

        for item in result["results"]:
            print(item)

        print("\n====================")
        print("FINAL RESPONSE")
        print("====================")

        print(result["final_answer"])


if __name__ == "__main__":
    run_cli()