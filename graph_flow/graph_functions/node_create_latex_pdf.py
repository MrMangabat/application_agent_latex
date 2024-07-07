# graph_functions/create_latex_pdf.py
import os
from datetime import datetime
from graph_flow.graph_functions.node_graph_state import GraphState

def create_latex_pdf(state: GraphState) -> GraphState:
    final = state['final']
    # query_for_search = state['messages'][1]  # Extract the query from the state

    print("------ Creating LaTeX PDF ------")
    print(final, "-------------- check if latex safe variables are here")
    
    # Access solution components
    company_name = final.get("company_name", "")
    job_title = final.get("job_title", "")
    introduction = final.get("introduction", "")
    motivation = final.get("motivation", "")
    skills = final.get("skills", "")
    continued_learning = final.get("continued_learning", "")
    thank_you = final.get("thank_you", "")

    # Directory where the variables.tex file will be saved
    directory = 'companies_applied_for'

    # Create the base directory if it does not exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    if company_name.lower() == "unknown":
        # Find the next available subdirectory number
        next_subdir_num = 0
        while os.path.exists(os.path.join(directory, f"unknown{next_subdir_num}")):
            next_subdir_num += 1

        company_directory = os.path.join(directory, f"unknown{next_subdir_num}")
    else:
        company_directory = os.path.join(directory, company_name)

    # Create the company directory if it does not exist
    if not os.path.exists(company_directory):
        os.makedirs(company_directory)

    # Write the query_for_search variable to a separate .tex file in the specified directory
    query_file_path = os.path.join(company_directory, 'query_for_search.tex')

    with open(query_file_path, 'w') as query_file:
        query_file.write(f"\\newcommand{{\\job_vacancy}}{{{state['messages'][1]}}}\n")

    # Write these variables to a .tex file in the specified directory
    resume_file_path = os.path.join(company_directory, company_name + '.tex')

    with open(resume_file_path, 'w') as text_for_latex:
        text_for_latex.write(f"\\newcommand{{\\finalCompanyName}}{{{company_name}}}\n")
        text_for_latex.write(f"\\newcommand{{\\finalJobtitle}}{{{job_title}}}\n")
        text_for_latex.write(f"\\newcommand{{\\finalIntroduction}}{{{introduction}}}\n")
        text_for_latex.write(f"\\newcommand{{\\finalMotivation}}{{{motivation}}}\n")
        text_for_latex.write(f"\\newcommand{{\\finalSkills}}{{{skills}}}\n")
        text_for_latex.write(f"\\newcommand{{\\finalContinuedLearning}}{{{continued_learning}}}\n")
        text_for_latex.write(f"\\newcommand{{\\finalThankYou}}{{{thank_you}}}\n")

    current_date = datetime.now().strftime('%Y-%m-%d')
    latex_filename = f'JMangabat_{company_name}_{job_title}_{current_date}.tex'

    latex_file_path = os.path.join(company_directory, latex_filename)

    # Check if the file already exists and create a unique file name if it does
    file_counter = 1
    while os.path.exists(latex_file_path):
        new_file_name = f'JMangabat_{company_name}_{job_title}_{current_date}_{file_counter}.tex'
        latex_file_path = os.path.join(company_directory, new_file_name)
        file_counter += 1

    tex_content = f"""
     %----------------------------------------------------------------------------------------
    % PACKAGES AND OTHER DOCUMENT CONFIGURATIONS
    %----------------------------------------------------------------------------------------

    \\documentclass{{article}}
    \\usepackage{{graphicx}} % Required for including images
    \\usepackage{{fancyhdr}} % Required for customizing headers and footers
    \\usepackage{{setspace}} % Remove paragraph indentation
    \\usepackage{{hyperref}} % For adding links

    \\usepackage{{titlesec}} % Used to customize the \\section command
    \\usepackage[
        a4paper, % Paper size
        top=15mm, % Top margin
        bottom=15mm, % Bottom margin
        left=15mm, % Left margin
        right=15mm, % Right margin
    ]{{geometry}}

    \\setlength{{\\parskip}}{{-0.7em}} % Vertical space between paragraphs

    \\fancypagestyle{{firstpage}}{{%
        \\fancyhf{{}} % Clear default headers/footers
        \\renewcommand{{\\headrulewidth}}{{0pt}} % No header rule
        \\renewcommand{{\\footrulewidth}}{{1pt}} % Footer rule thickness
    }}

    \\fancypagestyle{{subsequentpages}}{{%
        \\fancyhf{{}} % Clear default headers/footers
        \\renewcommand{{\\headrulewidth}}{{1pt}} % Header rule thickness
        \\renewcommand{{\\footrulewidth}}{{1pt}} % Footer rule thickness
    }}

    \\input{{{company_name}.tex}}

    \\AtBeginDocument{{\\thispagestyle{{firstpage}}}} % Use the first page headers/footers style on the first page
    \\pagestyle{{subsequentpages}} % Use the subsequent pages headers/footers style on subsequent pages

    \\begin{{document}}
    \\rule{{\\linewidth}}{{1pt}} % Horizontal rule

    % Use the commands in your document
    \\begin{{center}}
        Jannik M. B. Sørensen |
        Email: Mangabat93@gmail.com | 
        Odder, Denmark | {{{current_date}}}
    \\end{{center}}

    \\subsection*{{\\finalJobtitle, \\finalCompanyName}}
        \\begin{{spacing}}{{1.2}}
            \\noindent{{\\finalIntroduction}}\\\\
        \\end{{spacing}}
        \\vspace*{{0mm}}

        \\begin{{spacing}}{{1.2}}
            \\noindent{{\\finalMotivation}}\\\\
        \\end{{spacing}}
        \\vspace*{{0mm}}

        \\begin{{spacing}}{{1.2}}
            \\noindent{{\\finalSkills}}\\\\

            \\noindent Some additional highlights of the benefit I will bring to your organisation include:
                \\begin{{itemize}}
                    \\item Capable of applying cutting-edge algorithms and models for complex problem-solving.
                    \\item Strong consideration towards data integrity and regulations including AI-act.
                    \\item Able to set up agents focused on enhancing efficiency.
                    \\item Ability to collaborate with cross-functional teams to deliver high-impact projects.
                \\end{{itemize}}
        \\end{{spacing}}
        \\vspace*{{0mm}}


    \\subsection*{{Continued Learning}}
        \\begin{{spacing}}{{1.2}}
            \\noindent{{\\finalContinuedLearning}}\\\\
        \\end{{spacing}}
        \\vspace*{{0mm}}

    \\subsection*{{Thanks for your time}}
        \\begin{{spacing}}{{1.2}}
            \\noindent{{\\finalThankYou}}\\\\        
        \\end{{spacing}}

    \\noindent Kind regards,\\\\
        Jannik Mangabat

    \\footnote{{This cover letter is build with langgraph to employ self-correction, check \href{{https://github.com/MrMangabat/application_agent_latex}}{{GitHub}}}}.
    \\footnote{{LinkedIn : \href{{https://www.linkedin.com/in/jannik-mangabat-bach-616586b9/}}{{Jannik Mangabat}}}}.

    \\end{{document}}
    """

    with open(latex_file_path, 'w') as file:
        file.write(tex_content)

    # Optionally, you can update the state with any relevant information about the LaTeX file generation
    # state['messages'].append(f"LaTeX file created at {latex_file_path}")

    return state
