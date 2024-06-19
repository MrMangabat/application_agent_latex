from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatMessagePromptTemplate, PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser


class OutputStuctureV2(BaseModel):
    company_name: str = Field(description="Company name")
    job_title: str = Field(description="Job title")
    introduction: str = Field(description="Introduction")
    motivation: str = Field(description="Motivation")
    skills: str = Field(description="Skills")
    continued_learning: str = Field(description="Continued learning")
    thank_you: str = Field(description="Thank you for your time")

cover_letter_parser = PydanticOutputParser(pydantic_object=OutputStuctureV2)


def create_cover_letter_prompt(
        semilarity_document_template: list[str],
        cv:list[str],
        some_skills: list[str], 
        job_analysis: str, 
        matching_skills: dict,  
        ) -> ChatPromptTemplate:
    
    system_generate_cover_letter_template_str = """
        You are to assist in wrting a professional cover latter for a job//
        This template is the jobtemplate: {semilarity_jobtemplate}. Keep the personal tonality found in jobtemplate//
        The jobtemplate is a professional document and the generated cover letter should be heavily inspired from it//
        This is the first job after a master's degree in data science//
        Grammatical correctness is essential//
        Use casual business language//
        Ensure, the English language is equal to EITLS c1 score//
        The template job application must be in English//
        There unique skills can be in this list {my_skills}//
        {format_cover_letter_messages}
        """

    SYSTEM_GENERATE_COVER_LETTER_PROMT = SystemMessagePromptTemplate(
        prompt = PromptTemplate(
            template=system_generate_cover_letter_template_str,
            input_variables=["semilarity_jobtemplate, cv"],
            partical_variables={"format_cover_letter_messages": cover_letter_parser.get_format_instructions()}
        )
    )

    human_generate_cover_letter_template_str = """       
        Introduction section: write four lines to generate an with interest in IT and AI with inspiration from the {analysis_output}//
        Motivation section: write it using matching pairs {skill_match} and how these can be utilized for the company's benefit//
        What I can Offer section: write a section about what I can offer given my experiences found in {curriculum_vitae} and how they can be utilized for the company's benefit//
        Continued learning section: and provide short context that I am willing to learn what is necessary for the company and specific role//
        Thank you section: write a short and consice thank you note to setup a coffee//
        I DO NOT have prior experience in a professional environment in programming, ONLY academia//
        I DO have prior experience in project management//
        {format_cover_letter_messages}
        """

    HUMAN_GENERATE_COVER_LETTER_PROMPT = HumanMessagePromptTemplate(
        prompt = PromptTemplate(
            template=human_generate_cover_letter_template_str,
            input_variables=["my_skills", "analysis_output", "skill_match", "curriculum_vitae"],
            partical_variables={"format_cover_letter_messages": cover_letter_parser.get_format_instructions()}
        )
    )

    cover_letter_messages = [SYSTEM_GENERATE_COVER_LETTER_PROMT, HUMAN_GENERATE_COVER_LETTER_PROMPT]

    cover_letter_review_template = ChatPromptTemplate(
        messages=cover_letter_messages
    )


    pydantic_cover_letter_formatter = cover_letter_parser.get_format_instructions()

    cover_letter_review_template.format_messages(
        semilarity_jobtemplate = semilarity_document_template,
        my_skills = some_skills, 
        analysis_output = job_analysis,
        skill_match = matching_skills,
        curriculum_vitae = cv,
        format_cover_letter_messages = pydantic_cover_letter_formatter,
    )

    return cover_letter_review_template

