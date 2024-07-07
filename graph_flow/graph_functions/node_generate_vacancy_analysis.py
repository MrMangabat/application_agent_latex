from .node_graph_state import GraphState
from common import get_llm_model
from LLMs.job_analysis import initial_analysis_chain
from prompt_templates.analyse_vacant_position_prompt import analysis_parser

def generate_vacancy_analysis(state: GraphState) -> GraphState:
    llm_model = get_llm_model()
    
    query_for_search = state['messages'][1]  # Extract the query from the state
    skills = state['unique_skills']

    print("------ Analysing vacancy ------")
    print("\n")
    vacancy_analysis = initial_analysis_chain(
        query_for_search,
        skills,
        llm_model,
        analysis_parser,
    )
    
    state['generation'] = vacancy_analysis
    print("------ Vacancy analysis completed ------")
    
    return state
