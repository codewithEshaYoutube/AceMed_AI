from langchain.document_loaders import PyPDFLoader

loader = PyPDFLoader("biology-class-11th.pdf")
pages = loader.load_and_split()
