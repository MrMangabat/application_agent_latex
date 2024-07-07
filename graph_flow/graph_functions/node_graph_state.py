from typing import TypedDict, List, Annotated
from langgraph.graph.message import add_messages, AnyMessage

max_iterations = 5
max_context_iterations = 2

class GraphState(TypedDict):
    """
    TypedDict for the graph state.

    Args:
        TypedDict: Base class for TypedDict.
    """
    error: str
    messages: Annotated[List[AnyMessage], add_messages]
    generation: str
    iterations: int
    context_iteration: int
    final: dict
    cover_letter_template: str
    words_to_avoid: List[str]
    sentences_to_avoid: List[str]
    unique_skills: List[str]
    cv: str
