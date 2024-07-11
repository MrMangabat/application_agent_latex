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
from graph_flow.graph_functions.node_initial_check import check_generation
from graph_flow.graph_functions.node_check_latex_syntax import check_latex_syntax
from graph_flow.graph_functions.node_create_latex_pdf import create_latex_pdf
from graph_flow.graph_functions.node_decide_to_continue import decide_to_continue
from graph_flow.graph_functions.node_decide_to_correct import decide_to_correct_context
from graph_flow.graph_functions.node_secondary_check import check_generation_secondary

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

Software Engineer – do you want the title of AI Engineer?

Would you like to join us from the beginning of our AI venture as we build a new team that will bring the right AI tools to create business value?

Join us as we identify the AI models, we should configure to create a more effective business and ultimately make a difference to both people with intimate healthcare needs and healthcare professionals worldwide.

” Bringing your curiosity about AI and innovation to the table, you’ll get to work with the latest technology and make it come to life in an international company with a higher purpose ,” says AI Lead, Simon Buemann.

A new team dedicated to AI

Within Digital, Data and IT, you will be part of a new AI team. The team will be responsible for gathering and evaluating requirements for AI solutions from the entire business, creating roadmaps as well as identifying, configuring and developing the solutions into our setup.

“ This area has a lot of interest from stakeholders across the business. I am looking forward to working with brand new technology and contributing to innovation globally – and hopefully growing our team along the way ,” explains Simon.

Deliver ethical and amazing AI solutions

With your team, your aim will be to deliver AI solutions that are aligned with Coloplast’s strategic goals and provide measurable business value. Throughout your work, it will be a priority to gather new knowledge on AI and contribute to the continuous improvement of our methodologies and practices.

Specifically, you will be delivering on our prioritised AI use cases in our roadmap to enhance operational efficiency and innovation. This covers all phases from refining business needs, developing solutions and configuring and grounding pre-built AI models, to testing and validation and finally creating documentation and supporting business roll-out. This also entails

 Collaborating with team members, vendors, and business stakeholders from inception to deployment, ensuring quality, timeliness, and alignment with the business requirements and expectations 
 Working with team members, other developers, and vendors to design, develop, test, and deploy AI solutions within Azure and other platforms that meet the technical and functional specifications 
 Ensuring that we implement sufficient test and documentation procedures 
 Collaborating with IT and software development teams to ensure seamless integration of AI capabilities 
 Monitoring and evaluating the performance and impact of the AI solutions, and providing recommendations for improvement and optimisation 
Knowledge and understanding of AI concepts, techniques, and applications 

In this role, you need good people skills to explain complex AI concepts and solutions to both technical and non-technical audiences. Also, you have a strong sense of structure and quality, allowing you to really test our AI models and make sure we create the best and most ethical ones.

Finally, you enjoy learning, as AI is a constantly changing area, and we furthermore imagine that you

 Hold a bachelor's degree or higher in Software Engineering, Engineering, Mathematics, Statistics, or similar 
 Have experience in software development and an understanding of AI model integration 
 Are proficient in Azure and other cloud services, maybe with a track record of setting up AI models in these environments 
 Have programming experience writing clean maintainable code for instance in Python, C++, Java or other relevant coding languages 
 Have knowledge and an understanding of AI concepts, techniques, and applications, such as machine learning, deep learning, natural language processing, computer vision, etc. 
 Are fluent in English 


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
    work_flow.add_node("retrieve_cover_letter", retrieve_cover_letter)
    work_flow.add_node("analyse_vacancy", generate_vacancy_analysis)
    work_flow.add_node("generate_application", generate_cover_letter_wrapper)
    work_flow.add_node("check_generation", check_generation)
    work_flow.add_node("check_generation_secondary", check_generation_secondary)
    work_flow.add_node("validation_context_chain", wrapped_validation_context_chain)
    work_flow.add_node("check_latex_syntax", check_latex_syntax)
    work_flow.add_node("create_latex_pdf", create_latex_pdf)


    #  Build graph
    work_flow.set_entry_point("retrieve_cover_letter")
    work_flow.add_edge("retrieve_cover_letter", "analyse_vacancy")
    work_flow.add_edge("analyse_vacancy", "generate_application")
    work_flow.add_edge("generate_application", "check_generation")

    # First conditional edge: From check_generation to either generate_application or validation_context_chain
    work_flow.add_conditional_edges("check_generation", decide_to_continue,
        path_map={
            "generate_application": "generate_application",
            "validation_context_chain": "validation_context_chain",
        }
    )

    work_flow.add_edge("validation_context_chain", "check_generation_secondary")
    # Conditional edge from validation_context_chain to either check_generation or check_latex_syntax
    work_flow.add_conditional_edges("check_generation_secondary", decide_to_correct_context,
        path_map={
            "validation_context_chain": "validation_context_chain",  # Loop back to check_generation for further validation
            "check_latex_syntax": "check_latex_syntax",  # Proceed to the next step when conditions are met
        }
    )

    # Edge from check_latex_syntax to create_latex_pdf
    work_flow.add_edge("check_latex_syntax", "create_latex_pdf")

    # Set the finish point
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
    for output in graph.stream(initial_state, config=config):
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
    work_flow.add_node("check_generation_secondary", check_generation_secondary)
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
        path_map={
            "generate_application": "generate_application",
            "validation_context_chain": "validation_context_chain",
        }
    )

    work_flow.add_edge("validation_context_chain", "check_generation_secondary")
    # Conditional edge from validation_context_chain to either check_generation or check_latex_syntax
    work_flow.add_conditional_edges("check_generation_secondary", decide_to_correct_context,
        path_map={
            "validation_context_chain": "validation_context_chain",  # Loop back to check_generation for further validation
            "check_latex_syntax": "check_latex_syntax",  # Proceed to the next step when conditions are met
        }
    )

    # Edge from check_latex_syntax to create_latex_pdf
    work_flow.add_edge("check_latex_syntax", "create_latex_pdf")

    # Set the finish point
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
    # graph_flow(some_job, do_not_use_words, forbidden_sentences)
    graph_flow_extra_validation(some_job, do_not_use_words, forbidden_sentences)
