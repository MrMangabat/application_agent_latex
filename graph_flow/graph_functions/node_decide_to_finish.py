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

    if error == "no" or iterations < max_iterations:
        print("---DECISION: RE-TRY SOLUTION---")
        print("\n")

        return "generate_application"
    else:
        print("---DECISION: Move to Validation Context---")
        print("\n")

        return "check_latex_syntax"
    
def decide_to_correct_context(state: GraphState) -> GraphState:
    """
    Determines whether to finish or retry based on the error status and iteration count.

    Args:
        state (GraphState): The current graph state.

    Returns:
        str: Next node to call.
    """
    print("------------- INSIDE DECIDE TO CORRECT CONTEXT---")
    print("\n")

    error = state["error"]
    context_iterations = state["context_iteration"]

    if error == "no" or context_iterations < max_context_iterations:
        print("---DECISION: RE-TRY VALIDATION CONTEXT---")
        print("\n")

        return "validation_context_chain"
    else:
        print("---DECISION: Move to Check LaTeX Syntax---")
        print("\n")

        return "check_latex_syntax"
    