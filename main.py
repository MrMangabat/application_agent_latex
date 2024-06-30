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
from graph_flow.graph_functions.node_context_validation import validation_context_chain
from graph_flow.graph_functions.node_check_generation import check_generation
from graph_flow.graph_functions.node_check_latex_syntax import check_latex_syntax
from graph_flow.graph_functions.node_create_latex_pdf import create_latex_pdf
from graph_flow.graph_functions.node_decide_to_finish import decide_to_finish

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
    "eagerly",
    "endeavors",
    "extensive",
    "extensively", 
    "expert",
    "expertise",
    "facets"
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
Er du passioneret for at skabe værdi gennem data? Kan du omsætte komplekse data til klar indsigt? Er du dygtig til at facilitere krav og forstå behovene fra forskellige interessenter? Hvis ja, så har vi den perfekte stilling til dig som Data Scientist i vores analytics-team hos Danica Pension.
Vi søger kompetencer indenfor SQL, Alteryx, Python og Tableau 
Vi søger dig der har solide kompetencer inden for SQL, Alteryx, Python, Tableau og PowerBI. Du har erfaring med dataanalyse og data visualisering, og du trives med at samarbejde på tværs af forskellige faggrupper og stakeholdere. 
Dine primære ansvarsområder vil være at: 
At levere værdifuld indsigt til vores ledelse og bestyrelse. 
Identificere nye datakilder og muligheder for at optimere vores dataanalyse og -visualisering. 
Samarbejde med kollegaer i analytics-teamet og på tværs af organisationen for at sikre, at vores data er pålidelige, relevante og anvendelige. 
Samarbejde på tværs af organisationen og drive datavisualiserings-projekter.
Udvikling af bl.a. predictive modelleing, ML, mv..
Vi leder efter en person med følgende kvalifikationer: 
En stærk baggrund i SQL, Python, Tableau.
Erfaring med dataanalyse, datavisualisering, erfaring med ML og predictive modelling.
En proaktiv tilgang til at identificere nye muligheder og udfordringer i vores data 
Evnen til at kommunikere komplekse analyseresultater til ikke-tekniske kollegaer og stakeholdere 
En positiv og samarbejdsorienteret tilgang til arbejdet 
Vi tilbyder udfordringer, udvikling og fremtid 
Hos Danica Pension tilbyder vi en spændende og udfordrende stilling i et innovativt og dynamisk arbejdsmiljø, hvor du vil have mulighed for at udvikle dine kompetencer inden for dataanalyse og -visualisering.  
Du får fast arbejdssted i vores nye hovedsæde på Bernstorffsgade 40, 1577 Kbh V, hvor du bliver en del af et fællesskab med gode kolleger og et rigtig godt arbejdsmiljø. Vi er en arbejdsplads med en uformel omgangstone og en god samarbejdsånd. Vores arbejde er præget af kvalitet, selvstændig opgaveløsning og åbenhed over for nye ideer. Vi er en fleksibel arbejdsplads med mulighed for at arbejde hjemmefra.  
"""

def generate_cover_letter_wrapper(state: GraphState) -> GraphState:
    return generate_cover_letter(state, llm_model)

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
    work_flow.add_conditional_edges("check_generation", decide_to_finish,
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
    from IPython.display import Image, display

    try:
        display(Image(graph.get_graph(xray=True).draw_mermaid_png()))
    except Exception as e:
        print(f"Error displaying the graph: {e}")
    
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
    print("------------- INSIDE GRAPH FLOW -------------")
    print(initial_state["words_to_avoid"])
    print("\n")
    print(initial_state["sentences_to_avoid"])
    print("\n")
    # Run the graph in streaming mode
    for output in graph.invoke(initial_state, config=config, stream_mode='values'):
        print("------------- OUTPUT -------------")
        pprint(output)

if __name__ == "__main__":
    llm_model = get_llm_model()
    graph_flow(some_job, do_not_use_words, forbidden_sentences)
