### External imports ###
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

### Internal imports ###
from prompt_templates.sentence_word_validation_prompt import validation_prompt, validator_parser

def validation_context_chain(
        llm_model: ChatOpenAI,
        skill_set: list[str], 
        cover_letter_generation: str,
        some_no_go_words: list[str],
        some_invalid_sentences: list[str],
        messages: list[str],
        parser: PydanticOutputParser):
    
    generate_validation = validation_prompt(
        some_skills=skill_set, 
        some_no_go_words=some_no_go_words,
        some_no_go_sentences=some_invalid_sentences,
        cover_letter_generation=cover_letter_generation,
        some_messages=messages
    ) | llm_model | parser

    context_validation = generate_validation.invoke(
        {
            "prompt_skills": skill_set,
            "prompt_content": cover_letter_generation,
            "prompt_invalid_sentences": some_invalid_sentences,
            "prompt_forbidden_words": some_no_go_words,
            "message_placeholder": messages,
        }
    )

    return context_validation
