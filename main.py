import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph
from pprint import pprint
import uuid

## Internal imports
from utils import set_project_root


from common import get_llm_model

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

# Call the function to set the project root and update the PYTHONPATH
ROOT = set_project_root()

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
    "foster",
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
    "mathematical modelin",
    "makes me a suitable candidate for this role",
    "make me a great fit for this role",
    "positions me well for this role",
    "invaluable in driving innovative AI solutions",
    "makes me a strong candidate for this role",
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


About the job
Solita’s Data & AI team vokser, og i den forbindelse søger vi en Data Platform Consultant til kundeprojekter på tværs af industrier.

Stillingen besættes i Aalborg.

Du skal helst mestre dansk flydende og engelsk på forretningsniveau.

Om stillingen og arbejdsopgaverne

Som Data Platform Consultant hos Solita vil du arbejde sammen med Solitas datateam på forskellige kundeprojekter, hvor dataplatforme og forskellige løsninger til dataudnyttelse opbygges, dataopbevaring moderniseres, og data indhentet fra IoT-kilder behandles. Du har muligheden for at påvirke, hvilken slags projekt du ønsker at arbejde på. Vi ønsker at finde dig et projekt, der inkluderer at lære noget nyt, muligheden for at bruge dine eksisterende færdigheder og skabe indhold, der er meningsfuldt for dig.

Vi forventer, at du vil komme til at arbejde med følgende områder og teknologier:

Deltagelse i presales møder hos kunder og binde forretningskrav sammen med datakilder
Analyse, design og implementering af datadrevne løsninger for kunder
Implementering af teknologi inden for dataplatforme, herunder Databricks eller Snowflake
Brug af forskellige data modelleringsmetoder som eks. dimensionel modellering og Data Vault
Fordel med viden om Databricks og/eller Snowflake
Fordel med viden om Azure, AWS og/eller GCP
Fordel med viden om AWS
ETL/Data warehouse/lakehouse udvikling
Erfaring med Microsoft stack er et stort plus
Viden om SQL
Fordel med viden om Microsofts analyse- og dataværktøjer som fx Power BI, Azure og Fabric.

Hvorfor skal du vælge Solita?
Solita har ry for at levere produkter og services af høj kvalitet indenfor aftalt tid og pris. Vi sætter høje krav til vores udvikleres faglighed, men vi værdsætter samtidigt også forskellighed og originalitet. Derfor er et job hos os lig med masser af udfordrende projekter, dygtige kollegaer og plads til at være den du er.
Som Data Platform Consultant hos os får du mulighed for at tage de certificeringer, der er relevante for netop din faglige udvikling, det kan være indenfor områder såsom Azure og AWS. Vi har et stærkt tech community med månedlige tech talks om de seneste nye teknologier, og vi har udpeget tech evangelists, som er kapaciteter indenfor hver deres nicheområde, eksempelvis cloud.
Og så forventer vi selvfølgelig, at du går op i dit job og leverer dit bedste, men du får ikke en medalje for at være den der altid lukker og slukker om aftenen – der skal være balance mellem arbejdsliv og privatliv.



"""

def generate_cover_letter_wrapper(state: GraphState) -> GraphState:
    return generate_cover_letter(state, llm_model)


 # Update this node definition to pass the required arguments

def wrapped_validation_context_chain(state: GraphState) -> GraphState:
    return llm_validation(state, llm_model)

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
    graph_flow_extra_validation(some_job, do_not_use_words, forbidden_sentences)
