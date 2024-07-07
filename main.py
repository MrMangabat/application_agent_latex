import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph
from pprint import pprint
import uuid

## Internal imports
from utils import set_project_root
from retrieve_documents.retrieve_cv import cv_retrieve
from retrieve_documents.retrieve_templates import template_retriever

from common import get_llm_model
from LLMs.job_analysis import initial_analysis_chain
from LLMs.generate_cover_letter import cover_letter_chain

from prompt_templates.analyse_vacant_position_prompt import analysis_parser
from prompt_templates.generate_cover_letter_prompt import cover_letter_parser
from prompt_templates.sentence_word_validation_prompt import validator_parser
from graph_flow.graph_functions.node_graph_state import GraphState
from graph_flow.graph_functions.node_retrieve_cover_letters import retrieve_cover_letter
from graph_flow.graph_functions.node_generate_vacancy_analysis import generate_vacancy_analysis
from graph_flow.graph_functions.node_generate_cover_letter import generate_cover_letter
from graph_flow.graph_functions.node_context_validation import llm_validation
from graph_flow.graph_functions.node_check_generation import check_generation
from graph_flow.graph_functions.node_check_latex_syntax import check_latex_syntax
from graph_flow.graph_functions.node_create_latex_pdf import create_latex_pdf
from graph_flow.graph_functions.node_decide_to_finish import decide_to_continue, decide_to_correct_context

### setting environment variables
### Setting root
# Call the function to set the project root and update the PYTHONPATH
# ROOT = set_project_root()
from config import GPT_API
os.environ["OPENAI_API_KEY"] = GPT_API

do_not_use_words = [
    "abreast",
    "ardent",
    "cruisal",
    "deeply",
    "eager",
    "eagerly",
    "endeavors",
    "excited",
    "excel",
    "extensive",
    "extensively", 
    "expert",
    "expertise",
    "facets",
    "forefront",
    "fostering",
    "fueled",
    "fulfilling",
    "honed",
    "intricacies",
    "intricate",
    "meticulous ",
    "perfect",
    "perfectly",
    "prowess",
    "profoundly",
    "realm",
    "seamlessly",
    "specialist",
    "stems",
    "strive",
    "striving",
    "superior",
    "superiority",
    "Tableau",
    "thrilled",
    "versed"
]

forbidden_sentences = [
    "I am a perfect fit for this role",
    "which is crucial",
    "crucial for this role",
    "perfectly aligned",
    "perfectly suited",
    "perfectly align",
    "which are essential for",
    "which are essential for this role",
    " mathematical modelin"
]

draft_skills = [
    "Business analytics",
    "Business maturity",
    "Strategy",
    "Non-technical and technical communication",
    "Algorithms & datastrucures",
    "Software Engineering",
    "detail oriented",
    "Creative thinker",
    "Problem solving",
    "Critical thinking",
    "Team player",
    "Time management",
    "Adaptability",
    "Conflict resolution",
    "Collaborative",
    "Dilligent",
    "Software development",
    "ITIL",
    "SAFe",
    "PRINCE2",
    "CMMI",
    "SCRUM",
    "Agile development",
    "UML(frequency, class or C4)",
    "Stakeholder classification",
    "Python intermediate level",
    "SQL working understanding",
    "R working understanding",
    "JavaScript working understanding",
    "Git",
    "Statistical modelling",
    "Fundamental Azure knowledge",
    "PostGres",
    "Neo4J",
    "Qdrant",
    "ANNOY",
    "Docker",
    "scraping",
    "crawling",
    "MT5",
    "Bert",
    "FinBert",
    "T5",
    "Scrapy",
    "Numpy",
    "Polars",
    "Pandas",
    "FastAPI",
    "VUE3",
    "TensorFlow2",
    "Huggingface",
    "Pytorch",
    "SonarCube",
    "Seaborn(/matplotlib/Plotly)",
    "PyTest",
    "SKlearn",
    "Unsupervised learning: dimensionality reduction, explorative factor analysis, K-mean..",
    "Supervised learning: Random Forests, multiple logistic regression, SVP, NNs, Classification",
]

some_job = """

Staff R&D ML/AI Engineer

Develop an ML framework to assist customers in semiconductor process integration and optimization. Joining a dynamic international team you will contribute to the development and deployment of ML solutions for silicon manufacturing.

Physics aware ML models are created using large volumes of measurement data augmented by Technology-CAD (TCAD) simulations.

Duties Include

Analyze and understand the ML solution that works better for a specific application
Integrate the ML solution in the ML framework
Contribute to extend the ML framework and integrate it with TCAD tools
Support AEs to solve the problems that customers report
Contribute to collaborative projects with customers and other partners based on business needs
Develop reusable and testable software components for use in a large existing code base, optimize existing components.

Qualifications

MS or PhD in Computer Science, Software Engineering or equivalent.
Strong understanding and expertise in ML/AI.
3+ years of hands-on experience in software development.
Solid programming skills in python. C++ is a plus.
Familiarity with Keras/TensorFlow is a plus.
Familiarity with training and operating streaming ML models is required.
Knowledge of semiconductor manufacturing process is a plus.
Strong desire to learn and explore new technologies.
English language working proficiency and communication skills allowing teamwork in an international environment.
Willingness to work in a distributed international team.

We offer a strong salary including a competitive benefits scheme.

Our Silicon Design & Verification business is all about building high-performance semiconductor chips— faster. We’re the world’s leading provider of solutions for designing and verifying advanced semiconductor chips. And we design the next-generation processes and models needed to manufacture those chips. We enable our customers to optimize chips for power, cost, and performance—eliminating months off their project schedules. At Synopsys, we’re at the heart of the innovations that change the way we work and play. Self-driving cars. Artificial Intelligence. The cloud. 5G. The Internet of Things. These breakthroughs are ushering in the Era of Smart Everything. And we’re powering it all with the world’s most advanced technologies for chip design and software security. If you share our passion for innovation, we want to meet you. Inclusion and Diversity are important to us. Synopsys considers all applicants for employment without regard to race, color, religion, national origin, gender, sexual orientation, gender identity, age, military veteran status, or disability.


"""

def generate_cover_letter_wrapper(state: GraphState) -> GraphState:
    return generate_cover_letter(state, llm_model)

 # Update this node definition to pass the required arguments
def wrapped_validation_context_chain(state: GraphState) -> GraphState:
    return llm_validation(state, llm_model)
        
def graph_flow(job_offer: str, invalid_words: list[str], invalid_sentences: list[str]):
    # Initialize the graph
    work_flow = StateGraph(GraphState)
    # Define the nodes
    work_flow.add_node("retrieve_cover_letter", retrieve_cover_letter)  # retrieve cover letter
    work_flow.add_node("analyse_vacancy", generate_vacancy_analysis)  # analyse vacancy
    work_flow.add_node("generate_application", generate_cover_letter_wrapper)  # generation solution
    work_flow.add_node("check_generation", check_generation)  # check generation
    work_flow.add_node("check_latex_syntax", check_latex_syntax)  # check LaTeX syntax
    work_flow.add_node("create_latex_pdf", create_latex_pdf)  # create LaTeX PDF
    # Build graph
    work_flow.set_entry_point("retrieve_cover_letter")
    work_flow.add_edge("retrieve_cover_letter", "analyse_vacancy")
    work_flow.add_edge("analyse_vacancy", "generate_application")
    work_flow.add_edge("generate_application", "check_generation")
    work_flow.add_conditional_edges("check_generation", decide_to_continue,
        {
            "check_latex_syntax": "check_latex_syntax",
            "generate_application": "generate_application",
        },
    )
    work_flow.add_edge("check_latex_syntax", "create_latex_pdf")  # Correct edge to finish point
    work_flow.set_finish_point("create_latex_pdf")

    # Set up the memory and compile the graph
    memory = SqliteSaver.from_conn_string(":memory:")

    # compile the graph
    graph = work_flow.compile(checkpointer=memory)

    # Display the graph
    # from IPython.display import Image, display

    # try:
    #     display(Image(graph.get_graph(xray=True).draw_mermaid_png()))
    # except Exception as e:
    #     print(f"Error displaying the graph: {e}")
    
    # Generate a unique thread ID
    unique_id = str(uuid.uuid4())

    # Configuration for the graph run
    config = {
        "configurable": {
            "thread_id": unique_id,
        }
    }

    initial_state = GraphState(
        error="",
        messages=['job_position', job_offer],
        generation="",
        iterations=0,
        final={},
        cover_letter_template="",
        words_to_avoid=invalid_words,
        sentences_to_avoid=invalid_sentences,
        unique_skills=draft_skills,
        cv=""
)
    
    print("\n")
    print("------------- INSIDE GRAPH FLOW EXTRA VALIDATION -------------")
    print("\n")

    # Run the graph in streaming mode
    for output in graph.invoke(initial_state, config=config):
        print("------------- OUTPUT -------------")
        pprint(output)

def graph_flow_extra_validation(job_offer: str, invalid_words: list[str], invalid_sentences: list[str]):

    
    # Initialize the graph
    work_flow = StateGraph(GraphState)
    # Define the nodes
    work_flow.add_node("retrieve_cover_letter", retrieve_cover_letter)
    work_flow.add_node("analyse_vacancy", generate_vacancy_analysis)
    work_flow.add_node("generate_application", generate_cover_letter_wrapper)
    work_flow.add_node("check_generation", check_generation)
    
   
    
    work_flow.add_node("validation_context_chain", wrapped_validation_context_chain)
    work_flow.add_node("check_latex_syntax", check_latex_syntax)
    work_flow.add_node("create_latex_pdf", create_latex_pdf)
    
    # Build graph
    work_flow.set_entry_point("retrieve_cover_letter")
    work_flow.add_edge("retrieve_cover_letter", "analyse_vacancy")
    work_flow.add_edge("analyse_vacancy", "generate_application")
    work_flow.add_edge("generate_application", "check_generation")
    
    # First conditional edge: From check_generation to either generate_application or validation_context_chain
    work_flow.add_conditional_edges("check_generation", decide_to_continue,
        {
            "generate_application": "generate_application",
            "validation_context_chain": "validation_context_chain",
        },
    )
    # Edge from validation_context_chain to check_generation
    work_flow.add_edge("validation_context_chain", "check_generation")
    # Second conditional edge: From validation_context_chain to either check_latex_syntax or validation_context_chain
    work_flow.add_conditional_edges("validation_context_chain", decide_to_correct_context,
        {
            "check_latex_syntax": "check_latex_syntax",
            "validation_context_chain": "validation_context_chain",
        },
    )
    
    work_flow.add_edge("check_latex_syntax", "create_latex_pdf")
    work_flow.set_finish_point("create_latex_pdf")

        # Generate a unique thread ID
    unique_id = str(uuid.uuid4())

    # Configuration for the graph run
    config = {
        "configurable": {
            "thread_id": unique_id,
        }
    }

    # Set up the memory and compile the graph
    memory = SqliteSaver.from_conn_string(":memory:")

    # compile the graph
    graph = work_flow.compile(checkpointer=memory)

    

    initial_state = GraphState(
        error="",
        messages=['job_position', job_offer],
        generation="",
        iterations=0,
        context_iteration=0,
        final={},
        cover_letter_template="",
        words_to_avoid=invalid_words,
        sentences_to_avoid=invalid_sentences,
        unique_skills=draft_skills,
        cv=""
    )

    print("\n------------- INSIDE GRAPH FLOW -------------\n")

    # Pass all required arguments to validation_context_chain
    for output in graph.invoke(initial_state, config=config):
        print("------------- OUTPUT -------------")
        pprint(output)


if __name__ == "__main__":
    llm_model = get_llm_model()
    graph_flow(some_job, do_not_use_words, forbidden_sentences)
    # graph_flow_extra_validation(some_job, do_not_use_words, forbidden_sentences)
