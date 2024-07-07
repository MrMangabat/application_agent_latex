from .node_graph_state import GraphState
import re
def check_latex_syntax(state: GraphState) -> GraphState:
    print("------ Checking LaTeX syntax ------")
    
    # State
    generation = state['generation']
    
    generation_components = {
        "company_name": generation.company_name,
        "job_title": generation.job_title,
        "introduction": generation.introduction,
        "motivation": generation.motivation,
        "skills": generation.skills,
        "continued_learning": generation.continued_learning,
        "thank_you": generation.thank_you
    }

    # Dictionary to map LaTeX special characters to their safe equivalents
    replacements = {
        '\\': ' ',          # backslash to space
        '{': ' ',           # curly brace to space
        '}': ' ',           # curly brace to space
        '#': ' ',           # hash to space
        '%': ' ',           # percent to space
        '&': 'and',         # ampersand to 'and'
        '_': ' ',           # underscore to space
        '^': ' ',           # caret to space
        '~': ' ',           # tilde to space
        '$': 'dollars',     # dollar to space
        '/': ' ',           # slash to space
        '*': ' ',           # asterisk to space
        '-': ' '            # hyphen to space
    }
    
    # Regex pattern to match any LaTeX special character
    pattern = r'[\\{}#%&_^\~$\/\*\-]'
    
    # Function to replace matched characters
    def replace_match(match):
        return replacements[match.group(0)]
    
    # Process each input text and update the dictionary
    for component_name, component_value in generation_components.items():
        # print(type(component_value), "DTYPE")
        # print(component_value, "COMPONENT VALUE")
        
        if not isinstance(component_value, str):
            raise TypeError(f"Expected a string, but got {type(component_value)}")
        
        if re.search(pattern, component_value):
            print(f"Found LaTeX special characters in: {component_value}")
            safe_text = re.sub(pattern, replace_match, component_value)
            print(f"Replaced with safe characters: {safe_text}")
        else:
            safe_text = component_value
        
        # Update the dictionary with the sanitized value
        generation_components[component_name] = safe_text

    print("\n")
    print("------ LaTeX syntax check complete ------")
    print("\n")


    return {
        "generation": generation,
        "final": generation_components
    }