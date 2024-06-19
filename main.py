### External imports
import sys
import os
from langchain_core.output_parsers import PydanticOutputParser



## Internal imports
from utils import set_project_root
from retrieve_documents.retrieve_cv import cv_retrieve
from retrieve_documents.retrieve_templates import template_retriever
from LLMs import LLM_model
from LLMs.job_analysis import initial_analysis_chain
from LLMs.generate_cover_letter import cover_letter_chain
from prompt_templates.analyse_vacant_position import analysis_parser
from prompt_templates.generate_cover_letter_prompt import cover_letter_parser
### setting environment variables
### Setting root
# Call the function to set the project root and update the PYTHONPATH
ROOT = set_project_root()
from config import GPT_API
os.environ["OPENAI_API_KEY"] = GPT_API


draft_skills = [
    ##
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
    ## management
    "ITIL",
    "SAFe",
    "PRINCE2",
    "CMMI",
    "SCRUM",
    "Agile development",
    "UML(frequency, class or C4)",
    "Stakeholder classification",
    ## technical
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
## Vacancy analysis LLM
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

if __name__ =="__main__":
    llm_instance = LLM_model.LLMModel(openai_api_key=GPT_API, temperature=0.1)
    llm_model = llm_instance.get_llm_model()

    #fetching cv/resume
    cv_doc = cv_retrieve("curriculum_vitae/JMangabat_CV.pdf")

    #fetching cover letter templates
    template_doc = template_retriever("jobtemplates")
    template_doc.invoke(some_job)

    print("-------------------------------- template_doc --------------------------------")
    print(template_doc, "\n")
    print("-------------------------------- cv --------------------------------")
    print(cv_doc)
    # initial chain
#     output = initial_analysis_chain(some_job, draft_skills,llm_model = llm_model, parser = analysis_parser)
    

#     # generate cover letter chain
#     some_cover_letter = cover_letter_chain(
#         skills = draft_skills,
#         llm_model = llm_model,
#         cv= cv_doc,
#         document_template=retrieve_templates(),
#         matching_skills=output.matching_skills,
#         parser = cover_letter_parser
#     )

#     print("\n")
#     print("----------- OUTPUT TYPE ------------")
#     print(type(output))
#     print("----------- OUTPUT test ------------")
#     print(output.company_name)
#     print("\n")
# for i in output:
#     print("--------INITIAL ANALYSIS CHAIN-----------")
#     print(i)
#     print("----------END---------")
#     print("\n")

#     print("--------COVER LETTER CHAIN-----------")
# for i in some_cover_letter:
#     print(i)
#     print("----------END---------")
#     print("\n")