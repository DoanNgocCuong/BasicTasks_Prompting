import dspy
import json
import pandas as pd
from typing import List, Dict
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class AnswerImprover(dspy.Module):
    def __init__(self, initial_prompt: str):
        super().__init__()
        self.initial_prompt = initial_prompt
        self.predict = dspy.Predict("user_input -> improved_output")
    
    def forward(self, user_input: str) -> str:
        """
        Nhận user_input và trả về improved_output dựa trên initial_prompt
        """
        context = {
            "system_prompt": self.initial_prompt,
            "user_input": user_input
        }
        
        # Thực hiện dự đoán với context
        result = self.predict(
            user_input=f"""
            System Prompt: {context['system_prompt']}
            
            User Input: {context['user_input']}
            
            Please provide the improved output following the system prompt's format.
            """
        )
        
        return result.improved_output

class PromptOptimizer:
    def __init__(self, model: str = 'openai/gpt-4'):
        """Khởi tạo optimizer với API key từ environment variable"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.lm = dspy.LM(model, api_key=api_key)
        dspy.configure(lm=self.lm)

    def load_training_data(self, file_path: str, sheet_name: str = 'TestingPromptOnDataset') -> List[Dict]:
        """Load dữ liệu training từ Excel file"""
        try:
            # Đọc file Excel với sheet_name được chỉ định
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            return [
                {
                    "user_input": row["user_input"],
                    "expected_output": row["assistant_response"]  # Đổi tên cột theo file của bạn
                }
                for _, row in df.iterrows()
            ]
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return []

    def evaluate_output(self, predicted: str, expected: str) -> float:
        """Đánh giá kết quả dự đoán"""
        try:
            pred_json = json.loads(predicted)
            exp_json = json.loads(expected)
            
            score = 0.0
            # Kiểm tra cấu trúc JSON
            if pred_json.get("message_type") == exp_json.get("message_type"):
                score += 0.3
            # Kiểm tra band score
            if pred_json.get("message", {}).get("band") == exp_json.get("message", {}).get("band"):
                score += 0.3
            # Kiểm tra số lượng improvements
            if len(pred_json.get("message", {}).get("improvement", [])) >= 2:
                score += 0.4
            return score
        except json.JSONDecodeError:
            return 0.0
        except Exception as e:
            print(f"Error in evaluation: {str(e)}")
            return 0.0

    def optimize_prompt(
        self,
        initial_prompt: str,
        train_data: List[Dict],
        num_rounds: int = 3,
        temperature: float = 0.7,
        num_threads: int = 4
    ) -> tuple[str, float]:
        """Tối ưu hóa prompt và trả về prompt tối ưu cùng với điểm số"""
        
        # Khởi tạo module
        improver = AnswerImprover(initial_prompt)
        
        # Cấu hình optimizer - bỏ max_rounds
        optimizer = dspy.MIPROv2(
            metric=self.evaluate_output,
            temperature=temperature,
            num_threads=num_threads
        )
        
        # Thực hiện tối ưu hóa
        optimized_module = optimizer.compile(
            improver,
            trainset=train_data
        )
        
        # Lấy prompt tối ưu và đánh giá
        optimized_prompt = optimizer.get_compiled_prompt()
        avg_score = self._evaluate_prompt(optimized_prompt, train_data)
        
        return optimized_prompt, avg_score

    def _evaluate_prompt(self, prompt: str, test_data: List[Dict]) -> float:
        """Đánh giá hiệu quả của prompt trên tập test"""
        improver = AnswerImprover(prompt)
        scores = []
        
        for example in test_data:
            try:
                result = improver(example["user_input"])
                score = self.evaluate_output(result, example["expected_output"])
                scores.append(score)
            except Exception as e:
                print(f"Error evaluating example: {str(e)}")
                scores.append(0.0)
        
        return sum(scores) / len(scores) if scores else 0.0

    def save_prompt(self, prompt: str, score: float, output_dir: str = "prompts"):
        """Lưu prompt và điểm số"""
        Path(output_dir).mkdir(exist_ok=True)
        
        output = {
            "prompt": prompt,
            "score": score,
            "timestamp": pd.Timestamp.now().isoformat()
        }
        
        file_path = Path(output_dir) / f"optimized_prompt_{score:.2f}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        return file_path

def main():
    # Đường dẫn file Excel
    excel_path = Path("D:/OneDrive - Hanoi University of Science and Technology/GIT/BasicTasks_Prompting/tuningPrompt.xlsx")
    
    if not excel_path.exists():
        print(f"Error: File not found at {excel_path}")
        return
        
    # Khởi tạo optimizer
    optimizer = PromptOptimizer()
    
    # Load dữ liệu training
    train_data = optimizer.load_training_data(
        file_path=str(excel_path),
        sheet_name='TestingPromptOnDataset'  # Tên sheet mặc định
    )
    
    if not train_data:
        print("No training data loaded")
        return
        
    # Đọc Excel và lấy system_prompt
    df = pd.read_excel(excel_path, sheet_name='TestingPromptOnDataset')
    
    # Debug: In ra tên các cột
    print("Available columns:", df.columns.tolist())
    
    # Lấy system_prompt đầu tiên
    initial_prompt = df['system_prompt'].iloc[0]  # Đổi từ 'prompt' thành 'system_prompt'
    
    # In ra để kiểm tra
    print("\nInitial prompt:", initial_prompt)
    
    # Tối ưu hóa prompt
    optimized_prompt, score = optimizer.optimize_prompt(
        initial_prompt=initial_prompt,
        train_data=train_data,
        num_rounds=3
    )
    
    # Lưu kết quả
    saved_path = optimizer.save_prompt(optimized_prompt, score)
    
    print(f"=== Kết quả tối ưu hóa ===")
    print(f"Điểm số: {score:.2f}")
    print(f"Đã lưu tại: {saved_path}")
    
    # Test prompt mới
    test_improver = AnswerImprover(optimized_prompt)
    test_input = df['user_input'].iloc[0]  # Lấy input đầu tiên để test
    test_result = test_improver(test_input)
    
    print("\n=== Kết quả test ===")
    print(json.dumps(json.loads(test_result), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()