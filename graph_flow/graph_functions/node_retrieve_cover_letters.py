from .node_graph_state import GraphState
from retrieve_documents.retrieve_templates import template_retriever
from retrieve_documents.retrieve_cv import cv_retrieve
import os

def retrieve_cover_letter(state: GraphState) -> GraphState:
    print("------ Retrieving cover letter ------")
    query_for_search = state['messages'][1]  # Extract the query from the state

    # Construct the absolute path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    jobtemplates_dir = os.path.join(base_dir, "../../jobtemplates")

    retriever_cover_letter = template_retriever(directory_path=jobtemplates_dir)  # Your retriever initialization here
    retrieve_cover_letter_template = retriever_cover_letter.invoke(query_for_search)

    print("------ Retrieving cv ------")
    cv_dir = os.path.join(base_dir, "../../curriculum_vitae")
    
    # Assuming a specific CV file name, modify as needed
    cv_file_path = os.path.join(cv_dir, "JMangabat_CV.pdf")
    retrieve_cv = cv_retrieve(cv_file_path=cv_file_path)  # Your retriever initialization here

    print("------ RETRIEVAL END ------")
    state['cover_letter_template'] = retrieve_cover_letter_template
    state['cv'] = retrieve_cv

    return state