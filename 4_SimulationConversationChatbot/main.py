from api_responder import generate_conversation_id, init_conversation, send_message
from ai_generator import generate_input
from agent_evaluation import evaluate_response
import json

# Configuration
INIT_URL = "http://103.253.20.13:9400/personalized-ai-coach/api/v1/bot/initConversation"
WEBHOOK_URL = "http://103.253.20.13:9400/personalized-ai-coach/api/v1/bot/webhook"
OPENAI_API_KEY = "your_openai_api_key"  # Replace with your OpenAI API key
BOT_ID = 3

def simulate_conversation(openai_api_key, num_turns=3):
    # Initialize conversation
    conversation_id = generate_conversation_id()
    init_response = init_conversation(BOT_ID, conversation_id, INIT_URL)
    
    results = []
    for _ in range(num_turns):
        # Generate user input
        user_input = generate_input(api_key=openai_api_key)
        print(f"\nUser: {user_input}")
        
        # Get API response
        api_response = send_message(conversation_id, user_input, WEBHOOK_URL)
        print(f"Assistant: {api_response['message']}")
        
        # Evaluate response
        evaluation = evaluate_response(
            api_key=openai_api_key,
            user_input=user_input,
            api_response=api_response["message"]
        )
        
        # Store results
        results.append({
            "turn": _ + 1,
            "user_input": user_input,
            "api_response": api_response["message"],
            "evaluation_score": evaluation.score,
            "evaluation_reasoning": evaluation.reasoning
        })
        
        print(f"Evaluation Score: {evaluation.score}/10")
        print(f"Reasoning: {evaluation.reasoning}")
    
    # Save results
    with open(f"simulation_results_{conversation_id}.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return results

if __name__ == "__main__":
    OPENAI_API_KEY = "your_openai_api_key"
    results = simulate_conversation(OPENAI_API_KEY)
