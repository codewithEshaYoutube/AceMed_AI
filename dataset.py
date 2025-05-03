from langchain_community.document_loaders import TextLoader

loader = TextLoader("raw.txt")
pages = loader.load_and_split()
