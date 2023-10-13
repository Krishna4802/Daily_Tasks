# Elasticsearch

* Install Homebrew : curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)

* To install Elasticsearch : brew tap elastic/tap -> intall the tap
                           : brew install elastic/tap/elasticsearch-full -> install the individual roducts


# As execute elasticsearch we need to install jdk also

* To install jdk : brew install openjdk
* To open jdk : sudo ln -sfn /opt/homebrew/opt/openjdk/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk
* Path for JDK : export ES_JAVA_HOME=/opt/homebrew/Cellar/openjdk/20.0.1/libexec/openjdk.jdk/Contents/Home


# Starting the ElasticSearch

* To start elastic search : ./bin/elasticsearch (or) brew services start elasticsearch
* to verify elastiseach status curl http://localhost:9200
* It will be started at the Default local host - 'http://localhost:9200'
* It will show you the system information

# indexing the data

# Indexing of data will be done through this python code

      import warnings
      from elasticsearch import Elasticsearch
      from urllib3.exceptions import InsecureRequestWarning

      #Disable the warning message
      warnings.filterwarnings("ignore", category=DeprecationWarning)
      warnings.filterwarnings("ignore", category=InsecureRequestWarning)

      # Connect to Elasticsearch
      es = Elasticsearch(['http://localhost:9200'], verify_certs=False)

      # Define the resume data
      resume = {
          'name': 'Krishna Prasath',
          'email': 'krishnaprasath.thirunavukaras@hashagile.com',
          'education': 'B.tech IT',
          'experience': 'Intern at HashAgile',
          'skills': ['C', 'Java', 'Data Analysis']
      }

      # Index the resume document
      index_name = 'resumes'  # Specify the index name
      document_id = '1'  # Specify a unique document ID

      # Index the document into Elasticsearch
      resp = es.index(index=index_name, id=document_id, document=resume)
      print(resp['result'])

      resp = es.get(index=index_name, id=document_id)
      print(resp['_source'])

# output :

{'name': 'Krishna Prasath', 'email': 'krishnaprasath.thirunavukaras@hashagile.com', 'education': 'B.tech IT', 'experience': 'Intern at HashAgile', 'skills': ['C', 'Java', 'Data Analysis']}


# Indexing of data from resume pdf will be done through this python code

we need to install a library for reading the content from pdf : pip3 install PyPDF2

      import warnings
      import PyPDF2
      from elasticsearch import Elasticsearch
      from urllib3.exceptions import InsecureRequestWarning

      # Disable the warning message
      warnings.filterwarnings("ignore", category=DeprecationWarning)
      warnings.filterwarnings("ignore", category=InsecureRequestWarning)

      # Connect to Elasticsearch
      es = Elasticsearch(['http://localhost:9200'], verify_certs=False)

      # Open the PDF file
      with open('krishna prasath resume (2).pdf', 'rb') as file:
          # Initialize a PDF reader object
          pdf_reader = PyPDF2.PdfReader(file)

          # Extract text from the PDF
          resume_text = ""
          for page in pdf_reader.pages:
              resume_text += page.extract_text()

      # Extract relevant information from the resume text
      resume_data = {}
      lines = [line.strip() for line in resume_text.split('\n') if line.strip()]

      # Extract name
      resume_data['name'] = lines[0]

      # Extract email and mobile
      for line in lines:
          if '@' in line:
              resume_data['email'] = line
          if line.isdigit():
              resume_data['mobile'] = line

      # Extract skills
      skills_start_index = lines.index('Technical Skills') + 1
      skills_end_index = lines.index('PROJECT')
      skills = [line.strip() for line in lines[skills_start_index:skills_end_index] if line.strip()]
      resume_data['skills'] = skills

      # Index the resume document
      index_name = 'resumes'  # Specify the index name
      document_id = '1'  # Specify a unique document ID

      # Index the document into Elasticsearch
      resp = es.index(index=index_name, id=document_id, body=resume_data)
      print(resp['result'])

      # Retrieve the document from Elasticsearch
      resp = es.get(index=index_name, id=document_id)
      print(resp['_source'])


# output
  
{'name': 'Krishna Prasath', 'email': 'krishnaprasath.thirunavukaras@hashagile.com', 'education': 'B.tech IT', 'experience': 'Intern at HashAgile', 'skills': ['C', 'Java', 'Data Analysis']}

* to stop elasticsearch : brew services stop elasticsearch
* to verify : curl http://localhost:9200 



# Python code to index 100 pdf datas

    import os
    import pdfplumber
    from elasticsearch import Elasticsearch
    import urllib3
    import re

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Connect to Elasticsearch
    es = Elasticsearch(['http://localhost:9200'], verify_certs=False)

    # Specify the folder path containing the resumes
    folder_path = '/Users/krishnaprasath/Documents/Resumes'

    # Index the resumes in the folder
    index_name = 'resumes'  # Specify the index name

    # Counter for indexing
    document_count = 0

    # Define different name patterns to capture
    name_patterns = [
        r"(?i)^\s*(?:Name:|)(.*)",  # Name: John Doe
        r"(?i)^\s*(?:Mr\.|Ms\.|Mrs\.)(?:\.\s*)?(.*?)",  # Mr./Ms./Mrs. John Doe
        r"(?i)^\s*(?:First|Given)\s*Name:\s*(.*?)",  # First/Given Name: John
        r"(?i)^\s*(?:Last|Family)\s*Name:\s*(.*?)",  # Last/Family Name: Doe
        r"(?i)^\s*(?:Full|)(?:\s*Name:|)\s*(.*?)$"  # Full Name: John Doe
    ]

    # Define pattern for mobile number extraction
    mobile_pattern = r"\b(\d{10})\b"

    # Define pattern for email extraction
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

    # Iterate over each file in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pdf'):
            # Construct the full file path
            file_path = os.path.join(folder_path, file_name)

            # Open the PDF file using pdfplumber
            with pdfplumber.open(file_path) as pdf:
            # Extract text from the PDF
            resume_text = ""
            for page in pdf.pages:
                resume_text += page.extract_text()

            # Extract name using the defined patterns
            name = ""
            for pattern in name_patterns:
            name_match = re.search(pattern, resume_text, re.MULTILINE)
            if name_match:
                name = name_match.group(1).strip()
                break

            # Extract mobile number using the mobile pattern
            mobile = ""
            mobile_match = re.findall(mobile_pattern, resume_text, re.MULTILINE)
            if mobile_match:
                mobile = ", ".join(set(mobile_match))  # Replace all duplicates with a single instance

            # Extract email using the email pattern
            email = ""
            email_match = re.findall(email_pattern, resume_text, re.MULTILINE)
            if email_match:
            email = ", ".join(set(email_match))  # Replace all duplicates with a single instance

            # Create a dictionary with the extracted data
            resume_data = {}
        if name:
            resume_data['name'] = name
        if mobile:
            resume_data['mobile'] = mobile
        if email:
            resume_data['email'] = email

        # Index the resume data into Elasticsearch
        if resume_data:
            document_count += 1
            document_id = f"resume-{document_count}"  # Generate a unique document ID

            # Index the document into Elasticsearch
            resp = es.index(index=index_name, id=document_id, body=resume_data)
            if resp['result'] == 'created':
                print(f"Indexed {file_name} successfully.")
            else:
                print(f"Failed to index {file_name}.")
        else:
            print(f"No relevant information found in {file_name}.")

        print()

    # Retrieve the indexed documents from Elasticsearch
    resp = es.search(index=index_name, q='*')
    hits = resp['hits']['hits']
    print(f"Total indexed documents: {len(hits)}")
    for hit in hits:
        print(f"Indexed data for {hit['_id']}:")
        print(hit['_source'])
        print()


