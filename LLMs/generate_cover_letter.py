### External imports ###
import sys
import os
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
### Internal imports ###
from prompt_templates.generate_cover_letter_prompt import create_cover_letter_prompt, cover_letter_parser
from utils import set_project_root


def cover_letter_chain(
        skills: list[str],
        llm_model: ChatOpenAI, 
        document_template: list[str],
        cv: str,
        job_offer_analysis: str,
        matching_skills: str,
        parser: PydanticOutputParser,
        messages: list[str]):  # Added messages parameter
    
    cover_letter_template, formatted_messages = create_cover_letter_prompt(
        semilarity_document_template=document_template, 
        cv=cv, 
        some_skills=skills, 
        job_analysis=job_offer_analysis, 
        matching_skills=matching_skills,
        messages=messages  # Pass messages
    )

    generate_cover_letter = cover_letter_template | llm_model | parser

    cover_letter = generate_cover_letter.invoke(
        {
            "semilarity_jobtemplate": document_template,
            "curriculum_vitae": cv,
            "my_skills": skills,
            "analysis_output": job_offer_analysis,
            "skill_match": matching_skills,
            "messages_placeholder": formatted_messages  # Use the formatted messages
        }
    )

    return cover_letter
