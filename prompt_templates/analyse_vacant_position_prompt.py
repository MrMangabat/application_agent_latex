from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatMessagePromptTemplate, PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

## Output data structure
class OutputStuctureV1(BaseModel):
    company_name: str = Field(description="identified company name")
    job_title: str = Field(description="identified job title")
    analysis_output: str = Field(description="analysis of the job vacancy")
    employees_skills_requirement: dict = Field(description="identified skills and technical experience required for the job vacancy")
    matching_skills: dict = Field(description="matching skills in the job vacancy")

analysis_parser = PydanticOutputParser(pydantic_object=OutputStuctureV1)


def create_analysis_prompt(skillsets: list[str], job_to_apply: str) -> ChatPromptTemplate:
    """_summary_

    Args:
        skillsets (list[str]): _description_
        job_to_apply (str): _description_

    Returns:
        ChatPromptTemplate: _description_
    """
    system_analysis_template_str = """
    You are an assistant to a human resource manager//
    You are to assist in the analysis of a job vacancy//
    Identify detailed overview over the each unique aspect in the job positionof interest that the company is looking for//
    Identify if it seems more personal or object oriented//
    Identify the company name//
    Identify the job title//
    Identify the skills and technical experience required for the job vacancy provided here to be stored as a dictionary employee skill requirement//
    {format_messages}
    """

    SYSTEM_ANALYSIS_PROMT = SystemMessagePromptTemplate(
        prompt=PromptTemplate(
            template=system_analysis_template_str,
            input_variables=["my_skills"],
            partial_variables={"format_messages": analysis_parser.get_format_instructions()}
        )
    )

    human_analysis_template_str = """
    Given the job vacancy, you are to analyse the following in detail: {job_position}//
    Use this list of skills {my_skills} to conduct an an mapping between job requirements and find matching skills//
    Output should contain a list of matching skills required for the job vacancy//

    {format_messages}
    """

    HUMAN_ANALYSIS_PROMPT = HumanMessagePromptTemplate(
        prompt=PromptTemplate(
            template=human_analysis_template_str,
            input_variables=["job_position"],
            partial_variables={"format_messages": analysis_parser.get_format_instructions()}
        )
    )

    analysis_messages = [SYSTEM_ANALYSIS_PROMT, HUMAN_ANALYSIS_PROMPT]

    analysis_review_template = ChatPromptTemplate(
        messages=analysis_messages
    )

    pydantic_analysis_formatter = analysis_parser.get_format_instructions()

    analysis_review_template.format_messages(
    my_skills=skillsets, 
    job_position=job_to_apply, 
    format_messages=pydantic_analysis_formatter)

    return analysis_review_template