import pandas as pd
import time
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def load_data(file_path):
    """Load conversation data from an Excel file."""
    return pd.read_excel(file_path)

def generate_response(context, history, model="gpt-3.5-turbo", temperature=0, max_tokens=1024):
    """Generate a response using OpenAI's ChatCompletion API."""
    chat_messages = [{"role": "system", "content": context}]
    
    # Add message history
    for msg in history:
        chat_messages.append({"role": "user", "content": msg})
    
    try_count = 0
    while try_count < 3:
        try:
            start_time = time.time()
            completion = client.chat.completions.create(
                model=model,
                messages=chat_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1,
                frequency_penalty=1,
                presence_penalty=2
            )
            end_time = time.time()
            return completion.choices[0].message.content, end_time - start_time
            
        except Exception as e:
            try_count += 1
            print(f"Error on attempt {try_count}: {str(e)}")
            if try_count >= 3:
                return "Request failed after 3 retries.", 0
            time.sleep(3)

def simulate_conversation(row):
    """Simulate a conversation based on the row of data."""
    message_history = []
    response_times = []
    response_count = 0

    # Extract settings from Excel row
    createUserQuestion_prompt = row['createUserQuestion_prompt']  
    AIAssistantResponse_prompt = row['AIAssistantResponse_prompt']
    initialUserQuestion = row['initialUserQuestion']
    maxConversationTurns = row['maxConversationTurns']

    # Person A starts the conversation
    message_history.append({"role": "Person A", "content": initialUserQuestion})
    response_times.append(0)  # No response time for the first question
    print(f"---\nPerson A: {initialUserQuestion}")

    conversationTurnCount = 0  # Đếm số lượt hội thoại

    while conversationTurnCount < maxConversationTurns:
        # Person B responds
        person_B_response, response_time = generate_response(
            AIAssistantResponse_prompt, 
            [msg["content"] for msg in message_history]  # Extract only content for API
        )
        message_history.append({"role": "Person B", "content": person_B_response})
        response_times.append(response_time)
        print(f"---\nPerson B: {person_B_response} (Response time: {response_time:.2f}s)")
        conversationTurnCount += 1
        time.sleep(1)

        if conversationTurnCount >= maxConversationTurns:
            break

        # Person A responds
        current_question, response_time = generate_response(
            createUserQuestion_prompt, 
            [msg["content"] for msg in message_history],  # Extract only content for API
            temperature=0.3
        )
        message_history.append({"role": "Person A", "content": current_question})
        response_times.append(response_time)
        print(f"---\nPerson A: {current_question} (Response time: {response_time:.2f}s)")
        time.sleep(1)

    return message_history, response_times

def export_conversations_to_excel(all_messages, output_path):
    """Export all conversations and response times to an Excel file."""
    try:
        df_export = pd.DataFrame(all_messages, columns=['Role', 'Conversation', 'Response_Time'])
        df_export.to_excel(output_path, index=False)
        print(f"Conversations exported to {output_path}")
    except PermissionError:
        print("Error: Please close the Excel file before saving.")

def main():
    try:
        # Load data
        input_file = '6_TuningWith2Prompting/2PromptingTuning.xlsx'
        output_file = 'result.xlsx'
        df = load_data(input_file)

        all_messages = []

        for index, row in df.iterrows():
            print(f"\n=== Processing Conversation {index + 1} ===")
            message_history, response_times = simulate_conversation(row)

            # Add conversation and response times to all messages
            for i in range(len(message_history)):
                all_messages.append([
                    message_history[i]["role"],           # Role
                    message_history[i]["content"],        # Conversation
                    response_times[i]                     # Response_Time
                ])
            all_messages.append(['Separator', '---------------------------', 0])

        # Export results
        export_conversations_to_excel(all_messages, output_file)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
