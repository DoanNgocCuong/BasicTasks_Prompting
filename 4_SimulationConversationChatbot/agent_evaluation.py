from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field

class EvaluationResult(BaseModel):
    score: int = Field(description="Score from 1-10")
    reasoning: str = Field(description="Detailed explanation of the evaluation")

def evaluate_response(api_key, user_input, api_response):
    # Create evaluation prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are evaluating an AI assistant's response quality."),
        MessagesPlaceholder(variable_name="conversation"),
        ("system", "Rate the response quality from 1-10 and explain why.")
    ])
    
    # Initialize evaluator
    evaluator = ChatOpenAI(api_key=api_key, model="gpt-4").with_structured_output(EvaluationResult)
    
    # Format conversation for evaluation
    conversation = [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": api_response}
    ]
    
    # Get evaluation
    result = evaluator.invoke({"conversation": conversation})
    return result
