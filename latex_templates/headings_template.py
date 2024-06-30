
def create_latex_pdf(state: GraphState) -> GraphState:
    # State
    generation = state['generation']
    final = state['final']

    print("------ Creating LaTeX PDF ------")
    print(final, "-------------- check if latex safe variables are here")
    # Access solution components
    company_name = generation.company_name
    job_title = generation.job_title
    motivation = generation.motivation
    skills = generation.skills
    continued_learning = generation.continued_learning
    thank_you = generation.thank_you

    # Process the tuple to remove newlines and format for LaTeX
    for item in state['generation']:
        key, value = item
        if key == 'motivation':
            # Remove newlines
            value = value.replace('\n', ' ')
            motivation = value
        elif key == 'skills':
            # Remove newlines
            value = value.replace('\n', ' ')
            skills = value
        elif key == 'continued_learning':
            # Remove newlines
            value = value.replace('\n', ' ')
            continued_learning = value
        elif key == 'thank_you':
            # Remove newlines
            value = value.replace('\n', ' ')
            thank_you = value

        
        

    # Directory where the variables.tex file will be saved
    directory = 'companies_applied_for'

    # Create the directory if it does not exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    company_directory = os.path.join(directory, company_name)
    if not os.path.exists(company_directory):
        os.makedirs(company_directory)

    # Write the query_for_search variable to a separate .tex file in the specified directory
    query_file_path = os.path.join(company_directory, 'query_for_search.tex')

    with open(query_file_path, 'w') as query_file:
        query_file.write(f"\\newcommand{{\\job_vacancy}}{{{query_for_search}}}\n")

    # Write these variables to a .tex file in the specified directory
    resume_file_path = os.path.join(company_directory, company_name + '.tex')

    with open(resume_file_path, 'w') as job:
        job.write(f"\\newcommand{{\\job_vacancy}}{{{query_for_search}}}\n")
        

    with open(resume_file_path, 'w') as text_for_latex:
        text_for_latex.write(f"\\newcommand{{\\finalCompanyName}}{{{company_name}}}\n")
        text_for_latex.write(f"\\newcommand{{\\finalJobtitle}}{{{job_title}}}\n")
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


    tex_content = tex_content = f"""
     %----------------------------------------------------------------------------------------
    % PACKAGES AND OTHER DOCUMENT CONFIGURATIONS
    %----------------------------------------------------------------------------------------

    \\documentclass{{article}}
    % \\usepackage{{charter}} % Use the Charter font
    \\usepackage{{graphicx}} % Required for including images
    \\usepackage{{fancyhdr}} % Required for customizing headers and footers
    \\usepackage{{setspace}} % Remove paragraph indentation
    \\usepackage{{titlesec}} % Used to customize the \\section command
    \\usepackage[
        a4paper, % Paper size
        top=15mm, % Top margin
        bottom=15mm, % Bottom margin
        left=15mm, % Left margin
        right=15mm, % Right margin
        % showframe % Uncomment to show frames around the margins for debugging purposes
    ]{{geometry}}

    % \\setlength{{\\parindent}}{{0pt}} % Paragraph indentation
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
    %----------------------------------------------------------------------------------------
    %----------------------------------------------------------------------------------------
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
            {{\\finalMotivation}}
        \\end{{spacing}}
        \\vspace*{{0mm}}

        \\begin{{spacing}}{{1.2}}
            {{\\finalSkills}}
        \\end{{spacing}}
        \\vspace*{{0mm}}

    \\subsection*{{Continued Learning}}
        \\begin{{spacing}}{{1.2}}
            {{\\finalContinuedLearning}}
        \\end{{spacing}}
        \\vspace*{{0mm}}

    \\subsection*{{Thanks for your time}}
        \\begin{{spacing}}{{1.2}}
            {{\\finalThankYou}}\\\\        
        \\end{{spacing}}

    \\noindent Kind regards,\\\\
        Jannik Mangabat
    %----------------------------------------------------------------------------------------
    % LETTER CONTENT
    %----------------------------------------------------------------------------------------

    \\end{{document}}
    """

    with open(latex_file_path, 'w') as file:
        file.write(tex_content)
