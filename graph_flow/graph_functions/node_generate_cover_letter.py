from .node_graph_state import GraphState

from LLMs.generate_cover_letter import cover_letter_chain
from prompt_templates.generate_cover_letter_prompt import cover_letter_parser

def generate_cover_letter(state: GraphState, llm_model) -> GraphState:
    print("------ Generating application ------")
    # State
    messages = state['messages']
    iterations = state['iterations']
    generation = state['generation']
    retrieve_cover_letter_template = state["cover_letter_template"]
    unique_skills = state["unique_skills"]
    
    curriculum_vitae = state["cv"]
    
    

    # Generate solution
    cover_letter = cover_letter_chain(
        skills=unique_skills,
        llm_model=llm_model,
        document_template=retrieve_cover_letter_template,
        cv=curriculum_vitae,
        job_offer_analysis=generation.analysis_output,
        matching_skills=generation.matching_skills,
        messages=messages,
        parser=cover_letter_parser
    )
    
    # Add messages
    messages = [
        ('system', f"""Here is the attempt to generate a professional cover letter: {cover_letter.motivation}, {cover_letter.skills}, {cover_letter.continued_learning}, {cover_letter.thank_you}""")
    ]

    # Increment iterations
    iterations = iterations + 1

    print("------ Application generation completed------")
    print("\n")
    print(" ------- ITERATION: ", iterations, " -------")

    print(" ------ END OF COVER LETTER ------")
    print("\n")


    return {
        "generation": cover_letter,
        "messages": messages,
        "iterations": iterations,
    }
