
import os
from datetime import date

from dotenv import load_dotenv
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver

from typing import TypedDict, Annotated
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage
)
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel


# ----------------------------------
# 1. Environment Configuration
# ----------------------------------

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY missing from .env")

if not os.getenv("SERPER_API_KEY"):
    raise ValueError("SERPER_API_KEY missing from .env")


checkpointer = MemorySaver()

# ----------------------------------
# 2. Initialize Components
# ----------------------------------

console = Console()

llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0
)

search = GoogleSerperAPIWrapper()


# ----------------------------------
# 3. Search Decision Function
# ----------------------------------

def should_search(query: str) -> bool:

    router_prompt = f"""
    You are a search decision engine.

    Today's date: {date.today()}

    Decide whether the user's question requires Google Search.

    Return ONLY:
    SEARCH
    or
    NO_SEARCH

    SEARCH when:
    - Asking about current office holders or people.
    - Asking about latest news or events.
    - Asking about sports results or tournament winners.
    - Asking about current statistics, rankings or counts.
    - Asking about current prices, versions or releases.
    - Asking about facts that may have changed.
    - User explicitly requests Google Search.

    NO_SEARCH when:
    - Asking established historical facts.
    - Asking general programming concepts.
    - Asking mathematical questions.
    - Asking stable technical explanations.
    - Asking facts unlikely to change.

    When uncertain, choose SEARCH.

    User question: {query}
    """

    decision = llm.invoke(router_prompt).content.strip().upper()

    return decision.startswith("SEARCH")


# ----------------------------------
# 4. Generate Answer Using Search
# ----------------------------------

def answer_with_search(query: str) -> str:

    console.print("[dim cyan]🔎 Searching Google...[/dim cyan]")

    # Fetch Google results
    search_results = search.run(query)

    # Display raw search results for debugging
    console.print(
        Panel(
            search_results,
            title="🔎 Google Search Results",
            border_style="yellow",
            padding=(1, 2)
        )
    )

    # Ask Groq to answer using search results
    response = llm.invoke([
        (
            "system",
            """
            You are a research assistant.

            STRICT INSTRUCTIONS:

            1. Google Search results are your primary source of truth.
            2. Never override search results with outdated pretrained knowledge.
            3. Never claim an event is in the future if search results
               show that it has already happened.
            4. Never substitute older information for newer results.
            5. Answer directly using relevant search results.
            6. If results are insufficient or contradictory, say so.
            7. Never invent dates, scores, statistics or facts.
            8. Mention source names when available.
            9. Format answers using Markdown.
            """
        ),
        (
            "human",
            f"""
            USER QUESTION:
            {query}

            GOOGLE SEARCH RESULTS:
            <search_results>
            {search_results}
            </search_results>

            Answer the user's question using these results.
            """
        )
    ])

    return response.content


# ----------------------------------
# 5. Generate Answer Without Search
# ----------------------------------

def answer_without_search(query: str) -> str:

    console.print(
        "[dim yellow]⚡ Using model knowledge...[/dim yellow]"
    )

    response = llm.invoke(query)

    return response.content


# ----------------------------------
# 6. Interactive Chat Loop
# ----------------------------------

console.print(
    Panel(
        "[bold green]AI Research Assistant Started[/bold green]\n"
        "[dim]Ask anything. Type 'quit' to exit.[/dim]",
        border_style="green",
        padding=(1, 2)
    )
)


# ----------------------------------
# 6. LangGraph State
# ----------------------------------

class ResearchState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    route: str


# ----------------------------------
# 7. Router Node
# ----------------------------------

def router_node(state: ResearchState):

    query = next(
        msg.content for msg in reversed(state["messages"])
        if isinstance(msg, HumanMessage)
    )

    decision = should_search(query)

    return {
        "route": "search" if decision else "no_search"
    }


# ----------------------------------
# 8. Search Node
# ----------------------------------

def search_node(state: ResearchState):

    query = next(
        msg.content for msg in reversed(state["messages"])
        if isinstance(msg, HumanMessage)
    )

    console.print("[dim cyan]🔎 Searching Google...[/dim cyan]")

    search_results = search.run(query)

    console.print(
        Panel(
            search_results,
            title="🔎 Google Search Results",
            border_style="yellow"
        )
    )

    messages = [
        SystemMessage(content="""
            You are a research assistant.
            Google Search results are your primary source of truth.
            Never invent facts, dates or statistics.
            If results are insufficient or contradictory, say so.
            Format answers using Markdown.
        """),
        *state["messages"],
        HumanMessage(content=f"""
            Google Search results:
            {search_results}

            Answer the original user question using these results.
        """)
    ]

    response = llm.invoke(messages)

    return {
        "messages": [AIMessage(content=response.content)]
    }


# ----------------------------------
# 9. No Search Node
# ----------------------------------

def no_search_node(state: ResearchState):

    console.print(
        "[dim yellow]⚡ Using model knowledge...[/dim yellow]"
    )

    messages = [
        SystemMessage(content="""
            You are a helpful AI research assistant.
            Answer accurately and format responses using Markdown.
        """),
        *state["messages"]
    ]

    response = llm.invoke(messages)

    return {
        "messages": [AIMessage(content=response.content)]
    }


# ----------------------------------
# 10. Build LangGraph
# ----------------------------------

workflow = StateGraph(ResearchState)

workflow.add_node("router", router_node)
workflow.add_node("search", search_node)
workflow.add_node("no_search", no_search_node)

workflow.add_edge(START, "router")

workflow.add_conditional_edges(
    "router",
    lambda state: state["route"],
    {
        "search": "search",
        "no_search": "no_search"
    }
)

workflow.add_edge("search", END)
workflow.add_edge("no_search", END)

agent = workflow.compile(checkpointer=checkpointer)


while True:

    try:

        # User input
        console.print("\n")

        console.print(
            Panel(
                "[bold white]Enter your question[/bold white]",
                title="[bold cyan]👤 User[/bold cyan]",
                border_style="cyan",
                padding=(1, 2)
            )
        )

        query = console.input("[bold cyan]➜ [/bold cyan]").strip()

        # Exit condition
        if query.lower() in ("quit", "exit"):
            console.print("[bold yellow]Goodbye 👋🏼[/bold yellow]")
            break

        if not query:
            continue

        # # Decide whether to search
        # if should_search(query):

        #     final_text = answer_with_search(query)

        # else:

        #     final_text = answer_without_search(query)

        response = agent.invoke(
        {
        "messages": [
            HumanMessage(content=query)
        ]
        },
        config={
        "configurable": {
            "thread_id": "devesh"
            }
        }
        )

        final_text = response["messages"][-1].content

        # Display AI response
        console.print(
            Panel(
                Markdown(final_text),
                title="[bold green]🤖 AI Assistant[/bold green]",
                border_style="green",
                padding=(1, 2)
            )
        )

    except KeyboardInterrupt:

        console.print("\n[bold yellow]Goodbye 👋🏼[/bold yellow]")
        break

    except Exception as e:

        console.print(
            Panel(
                f"[red]{type(e).__name__}: {e}[/red]",
                title="[bold red]Error[/bold red]",
                border_style="red"
            )
        )
