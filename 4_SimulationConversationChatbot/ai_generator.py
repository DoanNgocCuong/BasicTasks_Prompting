from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def generate_input(api_key, prompt=None):
    if prompt is None:
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Generate a realistic user question to test an AI assistant.
            Focus on common customer service scenarios.
            The question should be clear and specific."""),
            ("user", "Generate a test question")
        ])
    
    llm = ChatOpenAI(api_key=api_key, model="gpt-4")
    response = llm.invoke(prompt)
    return response.content.strip()
