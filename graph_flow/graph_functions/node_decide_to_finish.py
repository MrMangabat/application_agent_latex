from .node_graph_state import GraphState, max_iterations

def decide_to_finish(state: GraphState) -> GraphState:
    """
    Determines whether to finish or retry based on the error status and iteration count.

    Args:
        state (GraphState): The current graph state.

    Returns:
        str: Next node to call.
    """

    error = state["error"]
    iterations = state["iterations"]

    if error == "no" or iterations >= max_iterations:

        return "check_latex_syntax"
    else:
        print("---DECISION: RE-TRY SOLUTION---")
        return "generate_application"