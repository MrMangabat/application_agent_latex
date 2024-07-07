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
        some_skills: list[str], 
        some_no_go_words: list[str],
        some_no_go_sentences: list[str],
        cover_letter_generation: str,
        some_messages: list[str]) -> ChatPromptTemplate:
    
    system_context_validator_template_str = """
        You are to assist, that the generated cover letter is not applying incorrect context.
        For example, if a job requires a skill like Tableau and Tableau is not in the list of {prompt_skills}, the cover letter should not mention Tableau.
        
        When writing the cover letter, do not apply more that maximum of 4 words when using grammatical parallelism, e.g. within "" ""\n
        "" incorrect example: "My proficiency includes Python, Statistical Modelling, knowing PostGres, Docker, using Numpy, Pandas, TensorFlow2, familiar with Huggingface, Pytorch, Seaborn, PyTest, and SKlearn.""
        "" incorrect example: "My proficiency includes Python, Statistical Modelling, PostGres, Docker, Numpy, Pandas, TensorFlow2, Huggingface, Pytorch, Seaborn, PyTest, and SKlearn.""
        "" correct example: "My proficiency in Python, Statistical Modelling, PostGres, and Docker, along with my knowledge of unsupervised and supervised learning techniques""
        "" correct example: "My experience includes project management, leading teams, developing software solutions, and improving business processes.""
        
        Reduce use of interposed phrases, e.g. within "" ""
        "" incorrect example: "Effective communication, which includes clear and concise information exchange, teamwork, involving collaboration with diverse groups, problem-solving skills, requiring critical thinking, and adaptability, essential for adjusting to new challenges, are essential for success in this role.""
        "" incorrect example: "Time management, essential for meeting deadlines, emotional intelligence, key to understanding team dynamics, strategic planning, important for long-term goals, customer service, crucial for client satisfaction, and innovation, necessary for staying competitive, are critical for success in this role.""
        "" correct example: "Effective communication, including clear information exchange, involving collaboration, problem-solving, critical thinking, and adaptability""
        "" correct example: "Time management, emotional intelligence, strategic planning, customer service, and innovation""
        {format_validator_messages}
        """

    SYSTEM_CONTEXT_VALIDATOR_PROMPT = SystemMessagePromptTemplate(
        prompt = PromptTemplate(
            template=system_context_validator_template_str,
            input_variables=["prompt_skills"],
            partial_variables={"format_validator_messages": validator_parser.get_format_instructions()}
        )
    )

    human_validator_template_str = """       
        Check {prompt_content} for words found here {prompt_forbidden_words} and sentences here {prompt_invalid_sentences}.
        {format_validator_messages}
        {message_placeholder}
        """

    HUMAN_CONTEXT_VALIDATOR_PROMPT = HumanMessagePromptTemplate(
        prompt = PromptTemplate(
            template=human_validator_template_str,
            input_variables=["prompt_forbidden_words", "prompt_invalid_sentences", "prompt_content", "message_placeholder"],
            partial_variables={"format_validator_messages": validator_parser.get_format_instructions()}
        )
    )
    context_validate_messages = [SYSTEM_CONTEXT_VALIDATOR_PROMPT, HUMAN_CONTEXT_VALIDATOR_PROMPT]

    context_validator_review_template = ChatPromptTemplate(
        messages=context_validate_messages
    )

    pydantic_context_validator_formatter = validator_parser.get_format_instructions()

    context_validator_review_template.format_messages(
        prompt_skills=some_skills, 
        prompt_invalid_sentences=some_no_go_sentences,
        prompt_forbidden_words=some_no_go_words,
        prompt_content=cover_letter_generation,
        message_placeholder=some_messages,
        format_cover_letter_messages=pydantic_context_validator_formatter
    )

    return context_validator_review_template
