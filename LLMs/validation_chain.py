### External imports ###

from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

### Internal imports ###
from prompt_templates.sentence_word_validation_prompt import validation_prompt, validator_parser
from utils import set_project_root

### setting environment variables ###

# Add the project root directory to the PYTHONPATH
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.abspath(os.path.join(current_dir, '..'))
# if project_root not in sys.path:
#     sys.path.append(project_root)

# Call the function to set the project root and update the PYTHONPATH

def validation_context_chain(
        llm_model: ChatOpenAI,
        cv: str,
        skill_set: list[str], 
        introduction: str, 
        motivation: str,
        continued_learning: str,
        thank_you: str,
        no_go_words: list[str],
        parser: PydanticOutputParser):
    
    # pydantic_context_validator_formatter = validator_parser.get_format_instructions()

    generate_validation = validation_prompt(
        some_cv=cv,
        some_skills=skill_set, 
        some_introduction=introduction,
        some_motivation=motivation,
        some_continued_learning=continued_learning,
        some_thank_you=thank_you,
        some_no_go_words=no_go_words) | llm_model | parser

    context_validation = generate_validation.invoke(
        {
            "prompt_cv": cv,
            "prompt_skills":skill_set,
            "prompt_introduction":introduction,
            "prompt_motivation":motivation,
            "prompt_continued_learning":continued_learning,
            "prompt_thank_you":thank_you,
            "prompt_forbidden_words":no_go_words,
            # "format_cover_letter_messages":pydantic_context_validator_formatter
        }
    )

    return context_validation