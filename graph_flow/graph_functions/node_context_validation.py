from .node_graph_state import GraphState

from LLMs.validation_chain import validation_context_chain
from prompt_templates.sentence_word_validation_prompt import validator_parser


def llm_validation(state: GraphState, llm_model) -> GraphState:
    messages = state['messages']
    iterations = state['iterations']

    cv_validation = state['cv']
    no_go_words = state['words_to_avoid']
    skill = state['unique_skills']
    generation = state['generation']
    introduction = generation.introduction
    motivation = generation.motivation
    continued_learning = generation.continued_learning
    thank_you = generation.thank_you

    print("------ VALIDATE GENERATION ------")
    print("\n")
    print("------ STATES VALUES inside VALIDATE GENERATION ------")
    print("\n")
    print("------ CV VALIDATION ------")
    print(len(cv_validation))
    print("\n")
    print("------ NO GO WORDS ------")
    print(len(no_go_words))
    print("\n")
    print("------ SKILLS ------")
    print(len(skill))
    print("\n")
    print("------ INTRODUCTION ------")
    print(introduction)
    print("\n")
    print("------ MOTIVATION ------")
    print(motivation)
    print("\n")
    print("------ CONTINUED LEARNING ------")
    print(continued_learning)
    print("\n")
    print("------ THANK YOU ------")
    print(thank_you)
    print("\n")
    print("------ END OF STATES VALUES ------")
    print("\n")
    
    context_validation_chain = validation_context_chain(
        llm_model=llm_model,
        cv=cv_validation,
        skill_set=skill,
        introduction=introduction,
        motivation=motivation,
        continued_learning=continued_learning,
        thank_you=thank_you,
        no_go_words=no_go_words,
        parser=validator_parser
    )

    # Add messages
    messages += [
        ('assistant', f"""Here is the attempt to generate a professional cover letter: {context_validation_chain.motivation}, {context_validation_chain.skills}, {context_validation_chain.continued_learning}, {context_validation_chain.thank_you}""")
    ]
    
    
    print("------ VALIDATE GENERATION completed------")
    print("\n")
    print(" ------- ITERATION: ", iterations, " -------")
    print(" ------ COVER LETTER ------")
    print("\n")
    print(context_validation_chain.introduction)
    print("\n")
    print(context_validation_chain.motivation)
    print("\n")
    print(context_validation_chain.skills)
    print("\n")
    print(context_validation_chain.continued_learning)
    print("\n")
    print(context_validation_chain.thank_you)
    print("\n")
    print(" ------ END OF VALIDATION-- ------")
    print("\n")

    return {
        "generation": context_validation_chain,
        "messages": messages,
        "iterations": iterations,
    }