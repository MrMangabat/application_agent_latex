### External imports ###
import sys
import os
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

### Internal imports ###
from prompt_templates.generate_cover_letter_prompt import create_cover_letter_prompt, cover_letter_parser
from utils import set_project_root

### setting environment variables ###

# Add the project root directory to the PYTHONPATH
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.abspath(os.path.join(current_dir, '..'))
# if project_root not in sys.path:
#     sys.path.append(project_root)

# Call the function to set the project root and update the PYTHONPATH
ROOT = set_project_root()

def cover_letter_chain(
        # some_input: str, 
        skills: list[str],
        llm_model: ChatOpenAI, 
        document_template: list[str],
        cv: str,
        job_offer_analysis: str,
        matching_skills: str,
        parser: PydanticOutputParser):
    
    # pydantic_cover_letter_formatter = cover_letter_parser.get_format_instructions()

    generate_cover_letter = create_cover_letter_prompt(
        semilarity_document_template=document_template, 
        cv=cv, 
        some_skills=skills, 
        job_analysis=job_offer_analysis, 
        matching_skills=matching_skills
    ) | llm_model | parser

    cover_letter = generate_cover_letter.invoke(
        {
            # "job_position":some_input, 
            "semilarity_jobtemplate": document_template,
            "curriculum_vitae": cv,
            "my_skills":skills, 
            "analysis_output":job_offer_analysis, 
            "skill_match":matching_skills
            # "format_cover_letter_messages":pydantic_cover_letter_formatter
        }
    )

    return cover_letter