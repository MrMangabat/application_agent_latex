import os
import sys
import re
from operator import itemgetter
from datetime import datetime
from utils import split_text_at_punctuation

from langchain.document_loaders.text import TextLoader

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain.chat_models.openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import PydanticOutputParser

from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain.pydantic_v1 import BaseModel, Field

from langchain.vectorstores import qdrant

from config import GPT_API

import re
from typing import Annotated, List, Dict, TypedDict
from langgraph.graph.message import add_messages, AnyMessage
from utils import check_latex_safety, validate_words



os.environ["OPENAI_API_KEY"] = GPT_API

current_date = datetime.now().strftime('%B%Y')

SET_TEMPERATURE = 0.2
MODEL = "gpt-4o-2024-05-13"#"gpt-3.5-turbo"

LLM_MODEL = ChatOpenAI(
    model=MODEL,
    name="Agent for job applications",
    temperature=SET_TEMPERATURE,
    n=1)

# loader = TextLoader("ai_engineer_software_engineer.txt")

loader = DirectoryLoader(path="jobtemplates/")

load_applications = loader.load()

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    encode_kwargs = {'normalize_embeddings':False}
)

vectorstore = qdrant.Qdrant.from_documents(
    documents=load_applications,
    embedding=embedding_model,
    location=":memory:"
)

skills = [
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
    "Dilligent"
]

IT_Management = [
    "ITIL",
    "SAFe",
    "PRINCE2",
    "CMMI",
    "SCRUM",
    "Agile development",
    "UML(frequency, class or C4)",
    "Stakeholder classification"
]

Programming_languages = [
    "Python intermediate level",
    "SQL working understanding",
    "R working understanding",
    "JavaScript working understanding"
]

technical_skills = [
    "git"
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
    "Hyggingface",
    "Pytorch",
    "SonarCube",
    "Seaborn(/matplotlib/Plotly)",
    "PyTest",
    "SKlearn"
    "Unsupervised learning: dimensionality reduction, explorative factor analysis, K-mean..",
    "Supervised learning: Random Forests, multiple logistic regression, SVP, NNs, Classification"
]

skills_dict = {
    'soft skills': skills,
    'IT Management': IT_Management,
    'Programming languages': Programming_languages,
    'Technical skills': technical_skills
}

do_not_use_words = [
    "abreast",
    "ardent",
    "cruisal",
    "deeply",
    "eagerly",
    "endeavors",
    "enhance",
    "enhanced",
    "enhancing",
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
    "thrilled",
    "versed"
]
query_for_search = """


Engineering

In the platform area in Digital Architecture, Data and AI we lay the groundwork for other product teams to delivering accurate, available, and comprehensive data products to enable actionable insights. In addition to this we create trusted and curated enterprise data products that span the entire business of Vestas. This newly established department is an integral component of Vestas' innovative Digital Powerhouse. Our mission is to empower customers, partners, and colleagues to seamlessly discover, access, and connect essential information for informed decisions and impactful actions.

 
Digital Solutions & Development > Digital Solutions > Chapter - Data Engineering & Architecture

  
As a Data Engineer in the platform area, you will collaborate closely with colleagues both inside and outside of the platform area.
 
Your role involves leveraging a range of cloud technologies and tools tailored to the specific product you are working on. This encompasses working with technologies and tools such as Snowflake, databricks, dbt (data build tool) and Azure Services (storage accounts, key vaults).

 

Responsibilities

Your key responsibilities will be:
 

Designing, constructing, and maintaining scalable, reliable, and efficient data products
Managing and monitoring data products
Engaging in close collaboration with stakeholders who consume the data product
Establishing necessary integrations with various sources to enable data extraction
 
 
Qualifications 

Degree in Business Intelligence, Data Engineering or Software Development and/or 3 to 5 years of Professional work experience in a similar field
Comfortable in a dynamic and changeable working day
Comprehensive analytical and problem-solving skills
Advanced communication and collaboration skills, with the ability to work effectively in a cross-functional team environment
Proficient communication skills in English (our corporate language), Danish is not required
 
Competencies

 We envision that you possess experience in designing, building, and maintaining data transformation logic. Furthermore, you may see yourself reflected in any of the following categories:

Proficiency in programming languages like SQL and Python - experience with dbt, spark, Airflow or Terraform is considered an asset
Experience in the development code in a team using devops techniques and agile development methodologies
Expertise in working with various Data Warehouse solutions and constructing data products using technologies such as Snowflake, Databricks, Azure Data Engineering Stack (like storage accounts, key vaults, Synapse, MSSQL, etc.)
Understanding of data warehouse modelling methodologies (Kimball, data vault et al.) as well as concepts like data mesh or similar
 
On a personal level, we anticipate that you:

Possess a collaborative and open-minded nature, eager to contribute to a globally diverse cross-functional team within the organization
Display curiosity and motivation for developing innovative data products that generate value exhibing positive communication skills, coupled with a positive, problem-solving approach to accomplishing tasks
Thrive in diverse environments and exhibit flexibility in adapting to evolving conditions embracing a commitment to continuous learning and a desire to contribute to the collective growth of the team
 
What we offer 

You will join a newly established, innovative, and committed team committed to support the business through the development of enterprise data products. You will also have the possibility to be part of forming how to best build data products. You will experience an environment that promotes continuous learning, enabling you to actualize your ambitions and get the chance to work in an agile office environment. While we hold our team members to high individual standards of collaboration, accountability, and meeting deadlines, we provide unwavering support to one another, collectively celebrating successes and addressing challenges.


"""

semilarity_document_template = vectorstore.similarity_search_with_score(
    query = query_for_search,
    k = 1,
    score_threshold=0.1)

print("semilarity_document_template", semilarity_document_template)

VACANCY_ANALYSIS_PROMT = ChatPromptTemplate.from_messages(
    [
        ('system',"""
                You are an assisatant to a human resource manager//
                You are to assist in the analysis of a job vacancy//
                Identify vocal points of interest that the company is looking for//
                Identify the company name//
                Identify the job title//
                Identify the skills and technical experience required for the job vacancy provided here//
                identify the skills and requirements for the job vacancy//
        """),

        ('human',"""
                Given the job vacancy, you are to analyse the following in detail: {SomeVacantPosition}//
                Use these skills {my_skills} to conduct an analysis between job requirements and find matching skills//
                Output should contain a list of matching skills required for the job vacancy//
                {format_instructions_1}
        """),
    ]
)

## Output data structure
class OutputStuctureV1(BaseModel):
    company_name: str = Field(description="identified company name")
    job_title: str = Field(description="identified job title")
    analysis_output: str = Field(description="analysis of the job vacancy")
    employees_skills_requirement: dict = Field(description="identified skills and technical experience required for the job vacancy")
    matching_skills: dict = Field(description="matching skills in the job vacancy")

parser_1 = PydanticOutputParser(pydantic_object=OutputStuctureV1)

format_messages = VACANCY_ANALYSIS_PROMT.format(
    SomeVacantPosition = query_for_search,
    my_skills = skills_dict,
    format_instructions_1 = parser_1.get_format_instructions())

chain = LLM_MODEL | parser_1 

analysis_chain = chain.invoke(format_messages)


# Extracting identified information from analysis_chain
identified_company_name = analysis_chain.company_name
identified_job_title = analysis_chain.job_title
identified_skill_requirements = analysis_chain.employees_skills_requirement
identified_matching_skills = analysis_chain.matching_skills
identified_analysis_output = analysis_chain.analysis_output

# Create the output dictionary according to the schema
output = {
    "company_name": identified_company_name,
    "job_title": identified_job_title,
    "analysis_output": identified_analysis_output,
    "employees_skills_requirement": identified_skill_requirements
}

# Getting keys from the dictionary
get_employee_requirements_keys = identified_skill_requirements.keys()

# Create an itemgetter object with these keys
get_employee_requirements_lists = itemgetter(*get_employee_requirements_keys)

# Applying itemgetter to the dictionary to get the lists
employee_requirements = get_employee_requirements_lists(identified_skill_requirements)

# Zipping keys with their corresponding lists
lists_with_employee_requirements = zip(get_employee_requirements_keys, employee_requirements)

# If you need to process lists_with_employee_requirements further, you can do so here
get_matching_skills_keys = identified_matching_skills.keys()
get_matching_skills_lists = itemgetter(*get_matching_skills_keys)
matching_skills = get_matching_skills_lists(identified_matching_skills)
lists_with_matching_skills = zip(get_matching_skills_keys, matching_skills)
# Example usage:
# print the output dictionary
print(list(lists_with_employee_requirements))
print(list(lists_with_matching_skills))

TEXT_GENERATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        ('system',"""
         You are to assist in setting up a job application template//
         The total amount of characters that can be used is 4000, include white spaces//
         
         Grammatical correctness is essential//
         Use casual business language//
         Ensure, the English language is equal to EITLS c1 score//
         The template job application must be in English//
         200-300 characters for the introduction section//
         800-1000 characters for the motivation section//
         500-800 characters for the skills section//
         560 characters for the masters section//
         390 characters for the bachelors section//
         300 characters for the continued learning section//
         200 characters for the thank you note//
         This template is the jobtemplate: {semilarity_jobtemplate}// 
         
        """),

        ('human',"""
         
         I have the following knowledge and skills which can be found in the following dictionary {skills}//
         
         write two lines to generate a short introduction with interest in IT and AI with inspiration from the {analysis_output}//
         
         write motivation with matching pairs {skill_match} and {employee_requirements} and how these can be utilized for the company's benefi//
         
         write a section about skills somme of the skills and how they can be utilized for the company's benefit//

         keep educational background for later access and save the section about masters degree into latex_edu_master and the section about bachelors into latex_edu_bachelor//
         keep continued learning section and provide short context that I am willing to learn what is necessary for the company and specific role//
        
         write a short and consice thank you note to setup a cofee//

         I DO NOT have prior experience in a professional environment in programming, ONLY academia//
         I DO have prior experience in project management//
         {format_instructions_2}
        """),
    ]
)

## Output data structure
class OutputStuctureV2(BaseModel):
    
    latex_company_name: str = Field(description="Company name")
    latex_job_title: str = Field(description="Job title")
    latex_introduction: str = Field(description="Introduction")
    latex_motivation: str = Field(description="Motivation")
    latex_skills: str = Field(description="Skills")
    latex_edu_masters: str = Field(description="Masters")
    latex_edu_bachelor: str = Field(description="Bachelor")
    latex_continued_learning: str = Field(description="Continued learning")
    latex_thank_you: str = Field(description="Thank you for your time")


parser_2 = PydanticOutputParser(pydantic_object=OutputStuctureV2)

format_messages_2 = TEXT_GENERATION_PROMPT.format(
    analysis_output = identified_analysis_output,
    employee_requirements = lists_with_employee_requirements,
    skill_match = lists_with_matching_skills,
    skills = skills_dict,
    semilarity_jobtemplate = semilarity_document_template,
    format_instructions_2 = parser_2.get_format_instructions())

print(format_messages_2)
chain_2 = LLM_MODEL | parser_2

analysis_chain_2 = chain_2.invoke(format_messages_2)

REMOVE_WORDS_PROMPT = ChatPromptTemplate.from_messages(
    [
        ('system',"""
         
         keep the original text here {analysis_chain_2} and substitube words if they appear on this list {forbidden_words} with something similar //
         
        {format_instructions_3}
         

        """),
    ]
)

class OutputStuctureV3(BaseModel):
    
    latex_company_name: str = Field(description="Company name")
    latex_job_title: str = Field(description="Job title")
    latex_introduction: str = Field(description="Introduction")
    latex_motivation: str = Field(description="Motivation")
    latex_skills: str = Field(description="Skills")
    latex_edu_masters: str = Field(description="Masters")
    latex_edu_bachelor: str = Field(description="Bachelor")
    latex_continued_learning: str = Field(description="Continued learning")
    latex_thank_you: str = Field(description="Thank you for your time")

parser_3 = PydanticOutputParser(pydantic_object=OutputStuctureV3)

format_messages_3 = REMOVE_WORDS_PROMPT.format(
    analysis_chain_2 = analysis_chain_2,
    forbidden_words = do_not_use_words,
    format_instructions_3 = parser_3.get_format_instructions())

print(format_messages_3)
chain_3 = LLM_MODEL | parser_3

analysis_chain_3 = chain_3.invoke(format_messages_3)


company_name = analysis_chain_3.latex_company_name
jobtitle = analysis_chain_3.latex_job_title
introduction = analysis_chain_3.latex_introduction
motivation = analysis_chain_3.latex_motivation
skills = analysis_chain_3.latex_skills
masters = analysis_chain_3.latex_edu_masters
bachelors = analysis_chain_3.latex_edu_bachelor
continued_learning = analysis_chain_3.latex_continued_learning
thank_you = analysis_chain_3.latex_thank_you

max_iterations = 5

class GraphState(TypedDict):
    """
    TypedDict for the graph state.

    Args:
        TypedDict: Base class for TypedDict.
    """
    error: str
    messages: Annotated[List[AnyMessage], add_messages]
    generation: str
    iterations: int

def generate_application(state: GraphState) -> GraphState:
    """
    Generate a job application based on the job template provided.

    Args:
        state (GraphState): The current graph state.

    Returns:
        state (dict): New key added to state, generation.
    """
    print("------ Generating application ------")

    # State
    messages = state['messages']
    iterations = state['iterations']
    error = state['error']


   
    # ensure that messages is not empty
    if not messages:
        messages = [('system', company_name, jobtitle, introduction, motivation, skills, masters, bachelors, continued_learning, thank_you)]

    # Generate solution
        APPLICATION_OUTPUT_PROMPT = ChatPromptTemplate.from_messages(
            [
                ('system',"""
                    Validate, that the generated application is not using any of these words found here {forbidden_words}in any of the following{company_name}, 
                    {job_title},{introduction}, {motivation}, {skills}, {masters}, {bachelors}, {continued_learning} and {thank_you}//
                    if any of these words are found, replace them with something similar//   
                 {format_instructions_3}
                """
                )
            ]
        )

        parser_3 = PydanticOutputParser(pydantic_object=OutputStuctureV2)

        messages += APPLICATION_OUTPUT_PROMPT.format(
        company_name = company_name,
        job_title = jobtitle,
        introduction = introduction,
        motivation = motivation,
        skills = skills,
        masters = masters,
        bachelors = bachelors,
        continued_learning = continued_learning,
        thank_you = thank_you,
        forbidden_words = do_not_use_words,
        format_instructions_3 = parser_3.get_format_instructions())

        application_solution = chain_3.invoke(format_messages_3)
        
        # Increment iterations
        iterations + 1

        return {
            "generation": application_solution,
            "messages": messages,
            "iterations": iterations,
            "error": error
        }
    
def check_generation(state: GraphState) -> GraphState:
    """
    Check the generated application for errors.

    Args:
        state (GraphState): The current graph state.

    Returns:
        state (GraphState): Updated graph state with error status.
    """
    # State
    messages = state['messages']
    iterations = state['iterations']
    error = state['error']
    application_solution = state['generation']

    # Access solution components
    try:
        company_name = application_solution.latex_company_name
        job_title = application_solution.latex_job_title
        introduction = application_solution.latex_introduction
        motivation = application_solution.latex_motivation
        skills = application_solution.latex_skills
        masters = application_solution.latex_edu_masters
        bachelors = application_solution.latex_edu_bachelor
        continued_learning = application_solution.latex_continued_learning
        thank_you = application_solution.latex_thank_you

        # Validate words
        forbidden_words_used = validate_words(do_not_use_words, company_name, job_title, introduction, motivation, skills, masters, bachelors, continued_learning, thank_you)
        if forbidden_words_used:
            raise ValueError(f"Forbidden words used: {', '.join(forbidden_words_used)}")

        # Check LaTeX safety
        safe_texts = check_latex_safety(company_name, job_title, introduction, motivation, skills, masters, bachelors, continued_learning, thank_you)
        if any(text != original for text, original in zip(safe_texts, [company_name, job_title, introduction, motivation, skills, masters, bachelors, continued_learning, thank_you])):
            raise ValueError("LaTeX safety issues found in the generated application")

    except Exception as e:
        print("---APPLICATION CHECK: FAILED---")
        error_message = [("user", f"Your generated application has errors: {e}. Please review your inputs and try again.")]
        messages += error_message
        error = "yes"
    else:
        print("---NO APPLICATION ERRORS---")
        error = "no"

    return {
        "generation": application_solution,
        "messages": messages,
        "iterations": iterations,
        "error": error
    }


def decide_to_finish(state: GraphState) -> str:
    """
    Determines whether to finish or retry based on the error status and iteration count.

    Args:
        state (GraphState): The current graph state.

    Returns:
        str: Next node to call.
    """
    error = state["error"]
    iterations = state["iterations"]

    if error == "no" or iterations >= max_iterations:
        print("---DECISION: FINISH---")
        return "end"
    else:
        print("---DECISION: RE-TRY SOLUTION---")
        return "generate"

# # Example usage
# state = {
#     "messages": [],
#     "iterations": 0,
#     "error": ""
# }

# # Loop until the decision is to finish or max_iterations is reached
# while state['iterations'] < max_iterations:
#     # Generate application

#     state = generate_application(state)
#     # print(f"State {counter} iter: {state}")
#     # Check the generation
#     state = check_generation(state)
    
#     # Decide next step
#     next_step = decide_to_finish(state)
#     # counter += 1
#     if next_step == "end":
#         break

# print(f"Next step: {next_step}")

#### Utilities
import uuid 

def _print_event(event: dict, _printed: set, max_length=1500):
    current_state = event.get("dialog_state")
    if current_state:
        print(f"Currently in: ", current_state[-1])
    message = event.get("messages")
    if message:
        if isinstance(message, list):
            message = message[-1]
        if message.id not in _printed:
            msg_repr = message.pretty_repr(html=True)
            if len(msg_repr) > max_length:
                msg_repr = msg_repr[:max_length] + " ... (truncated)"
            print(msg_repr)
            _printed.add(message.id)

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph

builder = StateGraph(GraphState)

# Define the nodes
builder.add_node("generate", generate_application)  # generation solution
builder.add_node("check_generation", check_generation)  # check code

# Build graph
builder.set_entry_point("generate")
builder.add_edge("generate", "check_generation")
builder.add_conditional_edges(
    "check_generation",
    decide_to_finish,
    {
        "end": END,
        "generate": "generate",
    },
)

memory = SqliteSaver.from_conn_string(":memory:")
graph = builder.compile(checkpointer=memory)

_printed = set()
thread_id = str(uuid.uuid4())
config = {
    "configurable": {
        # Checkpoints are accessed by thread_id
        "thread_id": thread_id,
    }
}

question = query_for_search
events = graph.stream(
    {"messages": [("user", question)], "iterations": 0}, config, stream_mode="values"
)
for event in events:
    _print_event(event, _printed)

event['generation']