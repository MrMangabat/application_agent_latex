from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate
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
    error: str = Field(description="Error message")

validator_parser = PydanticOutputParser(pydantic_object=OutputStuctureV2)


def validation_prompt(
        some_cv: str,
        some_skills: list[str], 
        some_introduction: str, 
        some_motivation: str,
        some_continued_learning: str,
        some_thank_you: str,
        some_no_go_words: list[str]
        ) -> ChatPromptTemplate:
    
    system_context_validator_template_str = """
        You are to assist, that the generated cover letter is not applying incorrect context.
        For example, if a job requires a skill like Tableau and Tableau is not in the list of {prompt_skills}, the cover letter should not mention Tableau.
        
        Do not apply sentences that are close to this: 
        "crucial for this role" or 
        "which are essential for", or 
        "I am a perfect fit for this role", or
        "perfectly align", or
        "perfectly aligned", or 
        "perfectly suited", or
        
        Reduce extended use of interposed phrases.

        Check that the cover letter is not using any of these words found here {prompt_forbidden_words}.

        {format_validator_messages}
        """

    SYSTEM_CONTEXT_VALIDATOR_PROMPT = SystemMessagePromptTemplate(
        prompt = PromptTemplate(
            template=system_context_validator_template_str,
            input_variables=["prompt_skills", "prompt_forbidden_words", "prompt_cv"],
            partial_variables={"format_validator_messages": validator_parser.get_format_instructions()}
        )
    )

    human_validator_template_str = """       
        Validate context which can be found in the following sections:
        introduction: {prompt_introduction}
        motivation: {prompt_motivation}
        skills: {prompt_skills}
        continued learning: {prompt_continued_learning}
        thank you: {prompt_thank_you}

        highlight any errors found in the cover letter
        {format_validator_messages}
        """

    HUMAN_CONTEXT_VALIDATOR_PROMPT = HumanMessagePromptTemplate(
        prompt = PromptTemplate(
            template=human_validator_template_str,
            input_variables=["prompt_skills", "prompt_introduction", "prompt_motivation", "prompt_continued_learning", "prompt_thank_you"],
            partial_variables={"format_validator_messages": validator_parser.get_format_instructions()}
        )
    )
    context_validate_messages = [SYSTEM_CONTEXT_VALIDATOR_PROMPT, HUMAN_CONTEXT_VALIDATOR_PROMPT]

    context_validator_review_template = ChatPromptTemplate(
        messages=context_validate_messages
    )


    pydantic_context_validator_formatter = validator_parser.get_format_instructions()

    context_validator_review_template.format_messages(
        prompt_skills = some_skills, 
        prompt_introduction = some_introduction,
        prompt_motivation = some_motivation,
        prompt_continued_learning = some_continued_learning,
        prompt_thank_you = some_thank_you,
        prompt_cv = some_cv,
        prompt_forbidden_words = some_no_go_words,
        format_cover_letter_messages = pydantic_context_validator_formatter
    )

    return context_validator_review_template

