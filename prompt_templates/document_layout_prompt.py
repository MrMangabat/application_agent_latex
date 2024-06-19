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


def create_layout_structure_prompt(skillsets: list[str], job_to_apply: str) -> ChatPromptTemplate:
    
    system_layout_template_str = """
    #
    #
    #
    #
    #
    {format_messages}
    """

    SYSTEM_LAYOUT_PROMT = SystemMessagePromptTemplate(
        prompt=PromptTemplate(
            template=system_layout_template_str,
            input_variables=["##########"],
            partial_variables={"format_messages": analysis_parser.get_format_instructions()}
        )
    )

    human_layout_template_str = """
    #
    #
    # 
    # 
    {format_messages}
    """

    HUMAN_LAYOUT_PROMPT = HumanMessagePromptTemplate(
        prompt=PromptTemplate(
            template=human_layout_template_str,
            input_variables=["##########"],
            partial_variables={"format_messages": analysis_parser.get_format_instructions()}
        )
    )

    layout_messages = [SYSTEM_LAYOUT_PROMT, HUMAN_LAYOUT_PROMPT]

    layout_review_template = ChatPromptTemplate(
        messages=layout_messages
    )

    pydantic_analysis_formatter = analysis_parser.get_format_instructions()

    layout_review_template.format_messages(
        ##########
        ##########
        ##########
        ########## 
    format_messages=pydantic_analysis_formatter)

    return layout_review_template