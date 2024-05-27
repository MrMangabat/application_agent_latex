# import os
# import re
# from operator import itemgetter
# from utils import split_text_at_punctuation
# from langchain.document_loaders.text import TextLoader
# from langchain_community.document_loaders import DirectoryLoader
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain.chat_models.openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import PydanticOutputParser
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.pydantic_v1 import BaseModel, Field
# from langchain.vectorstores import qdrant
# from config import GPT_API

# # Configuration
# os.environ["OPENAI_API_KEY"] = GPT_API
# SET_TEMPERATURE = 0.3
# MODEL = "gpt-4o-2024-05-13"
# LLM_MODEL = ChatOpenAI(model=MODEL, name="Agent for job applications", temperature=SET_TEMPERATURE, n=1)
# embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2", encode_kwargs={'normalize_embeddings': False})

# # Sample data (these can be moved to separate config or data files)
# skills = ["Business analytics", "Business maturity", "Strategy", "Non-technical and technical communication", "Algorithms & datastrucures", "Software Engineering", "detail oriented", "Creative thinker", "Problem solving", "Critical thinking", "Team player", "Time management", "Adaptability", "Conflict resolution", "Collaborative", "Dilligent"]
# IT_Management = ["ITIL", "SAFe", "PRINCE2", "CMMI", "SCRUM", "Agile development", "UML(frequency, class or C4)", "Stakeholder classification"]
# Programming_languages = ["Python intermediate level", "SQL working understanding", "R working understanding", "JavaScript working understanding"]
# technical_skills = ["git", "Statistical modelling", "Fundamental Azure knowledge", "PostGres", "Neo4J", "Qdrant", "ANNOY", "Docker", "scraping", "crawling", "MT5", "Bert", "FinBert", "T5", "Scrapy", "Numpy", "Polars", "Pandas", "FastAPI", "VUE3", "TensorFlow2", "Hyggingface", "Pytorch", "SonarCube", "Seaborn(/matplotlib/Plotly)", "PyTest", "SKlearn", "Unsupervised learning: dimensionality reduction, explorative factor analysis, K-mean..", "Supervised learning: Random Forests, multiple logistic regression, SVP, NNs, Classification"]
# skills_dict = {'soft skills': skills, 'IT Management': IT_Management, 'Programming languages': Programming_languages, 'Technical skills': technical_skills}
# do_not_use_words = ["abreast", "ardent", "cruisal", "deeply", "eagerly", "endeavors", "enhance", "enhanced", "enhancing", "extensive", "extensively", "expert", "expertise", "forefront", "fostering", "fueled", "fulfilling", "honed", "intricacies", "intricate", "meticulous", "perfect", "perfectly", "prowess", "profoundly", "realm", "seamlessly", "specialist", "stems", "thrilled", "versed"]

# class JobAnalyzer:
#     def __init__(self, query, loader_path):
#         self.query = query
#         self.loader_path = loader_path
#         self.vectorstore = None

#     def load_documents(self):
#         loader = DirectoryLoader(path=self.loader_path)
#         documents = loader.load()
#         self.vectorstore = qdrant.Qdrant.from_documents(documents=documents, embedding=embedding_model, location=":memory:")

#     def analyze_job_vacancy(self):
#         semilarity_document_template = self.vectorstore.similarity_search_with_score(query=self.query, k=1, score_threshold=0.1)
#         VACANCY_ANALYSIS_PROMT = ChatPromptTemplate.from_messages([
#             ('system', "You are an assistant to a human resource manager// Identify vocal points of interest that the company is looking for// Identify the company name// Identify the job title// Identify the skills and technical experience required for the job vacancy provided here// identify the skills and requirements for the job vacancy//"),
#             ('human', "Given the job vacancy, you are to analyse the following in detail: {SomeVacantPosition}// Use these skills {my_skills} to conduct an analysis between job requirements and find matching skills// Output should contain a list of matching skills required for the job vacancy// {format_instructions_1}"),
#         ])
        
#         class OutputStuctureV1(BaseModel):
#             company_name: str = Field(description="identified company name")
#             job_title: str = Field(description="identified job title")
#             analysis_output: str = Field(description="analysis of the job vacancy")
#             employees_skills_requirement: dict = Field(description="identified skills and technical experience required for the job vacancy")
#             matching_skills: dict = Field(description="matching skills in the job vacancy")

#         parser_1 = PydanticOutputParser(pydantic_object=OutputStuctureV1)
#         format_messages = VACANCY_ANALYSIS_PROMT.format(SomeVacantPosition=self.query, my_skills=skills_dict, format_instructions_1=parser_1.get_format_instructions())
#         chain = LLM_MODEL | parser_1
#         return chain.invoke(format_messages)

# class TextGenerator:
#     def __init__(self, analysis_chain):
#         self.analysis_chain = analysis_chain

#     def generate_text(self):
#         TEXT_GENERATION_PROMPT = ChatPromptTemplate.from_messages([
#             ('system', "You are to assist in setting up a job application template// The total amount of characters that can be used is 4000, include white spaces// 200-300 characters for the introduction section// 800-1000 characters for the motivation section// 500-800 characters for the skills section// 560 characters for the masters section// 390 characters for the bachelors section// 300 characters for the continued learning section// 200 characters for the thank you note// Grammatical correctness is essential// Use casual business language// Ensure, the English language is equal to EITLS c1 score// The template job application must be in English// This template is the jobtemplate: {semilarity_jobtemplate}//"),
#             ('human', "I have the following knowledge and skills which can be found in the following dictionary {skills}// write two lines to generate a short introduction with interest in IT and AI with inspiration from the {analysis_output}// write motivation with matching pairs {skill_match} and {employee_requirements} and how these can be utilized for the company's benefit// write a section about skills some of the skills and how they can be utilized for the company's benefit// keep educational background for later access and save the section about masters degree into latex_edu_master and the section about bachelors into latex_edu_bachelor// keep continued learning section and provide short context that I am willing to learn what is necessary for the company and specific role// write a short and concise thank you note to setup a coffee// I DO NOT have prior experience in a professional environment in programming, ONLY academia// I DO have prior experience in project management// {format_instructions_2}"),
#         ])
        
#         class OutputStuctureV2(BaseModel):
#             latex_company_name: str = Field(description="Company name")
#             latex_job_title: str = Field(description="Job title")
#             latex_introduction: str = Field(description="Introduction")
#             latex_motivation: str = Field(description="Motivation")
#             latex_skills: str = Field(description="Skills")
#             latex_edu_masters: str = Field(description="Masters")
#             latex_edu_bachelor: str = Field(description="Bachelor")
#             latex_continued_learning: str = Field(description="Continued learning")
#             latex_thank_you: str = Field(description="Thank you for your time")

#         parser_2 = PydanticOutputParser(pydantic_object=OutputStuctureV2)
#         format_messages_2 = TEXT_GENERATION_PROMPT.format(analysis_output=self.analysis_chain.analysis_output, employee_requirements=self.analysis_chain.employees_skills_requirement, skill_match=self.analysis_chain.matching_skills, skills=skills_dict, semilarity_jobtemplate=self.analysis_chain, format_instructions_2=parser_2.get_format_instructions())
#         chain_2 = LLM_MODEL | parser_2
#         return chain_2.invoke(format_messages_2)

# class WordValidator:
#     def __init__(self, forbidden_words, *texts):
#         self.forbidden_words = forbidden_words
#         self.texts = texts

#     def validate_words(self):
#         false_count = 0
#         true_count = 0
#         forbidden_words_used = []

#         for text in self.texts:
#             words = text.split()
#             for word in words:
#                 if word in self.forbidden_words:
#                     false_count += 1
#                     forbidden_words_used.append(word)
#                 else:
#                     true_count += 1
#         return true_count, false_count, forbidden_words_used

#     def check_latex_safety(self):
#         replacements = {
#             '\\': ' ', '{': ' ', '}': ' ', '#': ' ', '%': ' ', '&': 'and', '_': ' ', '^': ' ', '~': ' ', '$': 'dollars', '/': ' ', '*': ' ', '-': ' '
#         }
#         pattern = r'[\\{}#%&_^\~$\/\*\-]'
        
#         true_count = 0
#         false_count = 0
#         results = []

#         def replace_match(match):
#             return replacements[match.group(0)]
        
#         for text in self.texts:
#             if re.search(pattern, text):
#                 false_count += 1
#                 safe_text = re.sub(pattern, replace_match, text)
#             else:
#                 true_count += 1
#                 safe_text = text
#             results.append(safe_text)

#         print(f"Number of safe texts: {true_count}")
#         print(f"Number of modified texts: {false_count}")
#         return results

# class LatexFileWriter:
#     def __init__(self, directory, **kwargs):
#         self.directory = directory
#         self.variables = kwargs

#     def write_to_file(self):
#         if not os.path.exists(self.directory):
#             os.makedirs(self.directory)

#         variables_file_path = os.path.join(self.directory, 'variables.tex')
#         with open(variables_file_path, 'w') as text_for_latex:
#             for key, value in self.variables.items():
#                 text_for_latex.write(f"\\newcommand{{\\{key}}}{{{value}}}\n")

# class MainApp:
#     def __init__(self, query, loader_path, forbidden_words):
#         self.query = query
#         self.loader_path = loader_path
#         self.forbidden_words = forbidden_words

#     def run(self):
#         analyzer = JobAnalyzer(query=self.query, loader_path=self.loader_path)
#         analyzer.load_documents()
#         analysis_chain = analyzer.analyze_job_vacancy()
        
#         generator = TextGenerator(analysis_chain=analysis_chain)
#         generated_texts = generator.generate_text()

#         validator = WordValidator(self.forbidden_words, *generated_texts)
#         true_count, false_count, forbidden_words_used = validator.validate_words()
#         safe_texts = validator.check_latex_safety()

#         output_text = {
#             'finalCompanyName': safe_texts[0],
#             'finalJobtitle': safe_texts[1],
#             'finalIntroduction': safe_texts[2],
#             'finalMotivation': safe_texts[3],
#             'finalSkills': safe_texts[4],
#             'finalEducationMaster': safe_texts[5],
#             'finalEducationBachelor': safe_texts[6],
#             'finalContinuedLearning': safe_texts[7],
#             'finalThankYou': safe_texts[8]
#         }

#         writer = LatexFileWriter(directory='latex', **output_text)
#         writer.write_to_file()

# if __name__ == "__main__":
#     query_for_search = """
#     VI SØGER EN DATA SCIENTIST, DER VIL GÅ FORAN SAMMEN MED OS ... [rest of the query]
#     """
#     app = MainApp(query=query_for_search, loader_path="jobtemplates/", forbidden_words=do_not_use_words)
#     app.run()
