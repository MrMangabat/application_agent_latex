from .node_graph_state import GraphState, max_iterations, max_context_iterations

def decide_to_continue(state: GraphState) -> GraphState:
    """
    Determines whether to finish or retry based on the error status and iteration count.

    Args:
        state (GraphState): The current graph state.

    Returns:
        str: Next node to call.
    """

    error = state["error"]
    iterations = state["iterations"]

    if error == "no" or iterations == max_iterations:
        print("---DECISION: Move to Validation Context---")
        print("\n")

        return "validation_context_chain"
    else:
        print("---DECISION: RE-TRY SOLUTION---")
        print("\n")

        return "generate_application"
    