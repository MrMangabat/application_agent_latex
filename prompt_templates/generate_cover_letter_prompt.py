from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class OutputStructureV2(BaseModel):
    company_name: str = Field(description="Company name")
    job_title: str = Field(description="Job title")
    introduction: str = Field(description="Introduction")
    motivation: str = Field(description="Motivation")
    skills: str = Field(description="Skills")
    continued_learning: str = Field(description="Continued learning")
    thank_you: str = Field(description="Thank you for your time")
    matching_skills: dict = Field(description="matching skills in the job vacancy")
    analysis_output: str = Field(description="analysis of the job vacancy")

cover_letter_parser = PydanticOutputParser(pydantic_object=OutputStructureV2)

def create_cover_letter_prompt(
        semilarity_document_template: list[str],
        cv: str,
        some_skills: list[str], 
        job_analysis: str, 
        matching_skills: dict,
        messages: list[str]) -> ChatPromptTemplate:  # Added messages as an argument
    
    system_generate_cover_letter_template_str = """
        You are to assist in writing a professional cover letter for a job.
        This template is the jobtemplate: {semilarity_jobtemplate}. Keep the personal tonality found in jobtemplate.
        The jobtemplate is a professional document and the generated cover letter should be heavily inspired by it.
        This is the first job after a master's degree in data science.
        Grammatical correctness is essential.
        Use casual business language.
        Ensure the English language is equal to IELTS C1 score.
        The template job application must be in English.
        The unique skills can be in this list: {my_skills}.
        {format_cover_letter_messages}
        {messages_placeholder}
    """

    SYSTEM_GENERATE_COVER_LETTER_PROMPT = SystemMessagePromptTemplate(
        prompt=PromptTemplate(
            template=system_generate_cover_letter_template_str,
            input_variables=["semilarity_jobtemplate", "my_skills", "format_cover_letter_messages", "messages_placeholder"],
            partial_variables={"format_cover_letter_messages": cover_letter_parser.get_format_instructions()}
        )
    )

    human_generate_cover_letter_template_str = """       
        Introduction section: Write four lines to generate an introduction with interest in IT and AI with inspiration from the {analysis_output}.
        Motivation section: Write it using matching pairs {skill_match} and how these can be utilized for the company's benefit.
        What I Can Offer section: Write a section about what I can offer given my experiences found in {curriculum_vitae} and how they can be utilized for the company's benefit.
        Continued learning section: Provide short context that I am willing to learn what is necessary for the company and specific role.
        Thank you section: Write a short and concise thank you note to set up a coffee.
        I DO NOT have prior experience in a professional environment in programming, ONLY academia.
        I DO have prior experience in project management.
        {format_cover_letter_messages}
        {messages_placeholder}  # Added messages placeholder
    """

    HUMAN_GENERATE_COVER_LETTER_PROMPT = HumanMessagePromptTemplate(
        prompt=PromptTemplate(
            template=human_generate_cover_letter_template_str,
            input_variables=["analysis_output", "skill_match", "curriculum_vitae", "format_cover_letter_messages", "messages_placeholder"],
            partial_variables={"format_cover_letter_messages": cover_letter_parser.get_format_instructions()}
        )
    )

    cover_letter_messages = [SYSTEM_GENERATE_COVER_LETTER_PROMPT, HUMAN_GENERATE_COVER_LETTER_PROMPT]

    cover_letter_review_template = ChatPromptTemplate(
        messages=cover_letter_messages,
        input_variables=["semilarity_jobtemplate", "my_skills", "analysis_output", "skill_match", "curriculum_vitae", "format_cover_letter_messages", "messages_placeholder"]
    )

    pydantic_cover_letter_formatter = cover_letter_parser.get_format_instructions()

    formatted_messages = cover_letter_review_template.format_messages(
        semilarity_jobtemplate=semilarity_document_template,
        my_skills=some_skills, 
        analysis_output=job_analysis,
        skill_match=matching_skills,
        curriculum_vitae=cv,
        format_cover_letter_messages=pydantic_cover_letter_formatter,
        messages_placeholder=messages  # Use a placeholder name
    )

    return cover_letter_review_template, formatted_messages
