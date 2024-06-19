from langchain_community.document_loaders import PyPDFLoader

def cv_retrieve(cv_file_path: str) -> str:
    CV_LOADER = PyPDFLoader(file_path=cv_file_path)
    pages = CV_LOADER.load()
    
    # Initialize an empty list to hold the processed lines
    all_lines = []
    
    for page in pages:
        # Get the page content
        content = page.page_content  # Assuming the page object has a text attribute for the content
        
        # Remove the first 32 characters ---> !!unique to my personal CV + not perfectly cleaned!!
        if len(content) > 332:
            content = content[332:]
        else:
            content = ""
        
        # Split the content by newline characters and add each line to the list
        lines = content.split('\n')
        all_lines.extend(lines)
    
    # Join all lines into a single string with newline characters
    processed_content = '\n'.join(all_lines)
    
    return processed_content