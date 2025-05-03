from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import json

# Step 1: Load and Split Text
loader = TextLoader("raw.txt", encoding="utf-8")
documents = loader.load()

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=100
)

pages = text_splitter.split_documents(documents)

# Step 2: Create Prompt Template
prompt = PromptTemplate(
    input_variables=["text"],
    template="""
You are a data structuring expert. Convert the following textbook content into structured JSON format:

Content:
{text}

Return format:
{
  "chapter": "",
  "subheading": "",
  "definitions": [{"term": "", "definition": ""}],
  "key_concepts": ["", "", ""],
  "questions": [{"type": "MCQ/Short/Theory", "question": "", "answer": ""}]
}
"""
)

# Step 3: Initialize the LLM Chain
llm = OpenAI(temperature=0.2)  # Or use ChatOpenAI with gpt-4
chain = LLMChain(llm=llm, prompt=prompt)

# Step 4: Run through all chunks and collect results
structured_outputs = []

for i, doc in enumerate(pages):
    print(f"Processing chunk {i+1}/{len(pages)}")
    response = chain.run(text=doc.page_content)
    try:
        structured_outputs.append(json.loads(response))  # Make sure it's valid JSON
    except json.JSONDecodeError:
        print(f"⚠️ Skipping chunk {i+1}: JSON decode failed.")
        continue

# Step 5: Save to file
with open("structured_biology.json", "w", encoding="utf-8") as f:
    json.dump(structured_outputs, f, indent=4, ensure_ascii=False)

print("✅ Structured data saved to structured_biology.json")
