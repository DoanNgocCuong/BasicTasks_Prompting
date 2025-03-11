import pandas as pd
from itertools import product

# Load the uploaded Excel file
file_path = "workflow_mece_table.xlsx"
df = pd.read_excel(file_path)

# Extract category names and their possible values
categories = {}
for _, row in df.iterrows():
    category = row["Category"]
    intent = row["User Intent"]
    step = row["Step"]
    action = row["User Action"]
    
    key = f"{category} {intent} {step}"
    if category not in categories:
        categories[category] = {}
    categories[category][key] = action

# Generate all possible combinations
category_keys = list(categories.keys())
category_values = [list(cat.keys()) for cat in categories.values()]
all_combinations = list(product(*category_values))

# Format output with correct structure
formatted_combinations = []
for combo in all_combinations:
    combo_label = " - ".join(key.replace(" ", " ") for key in combo)
    prompt = "\n".join(categories[category][key] for category, key in zip(category_keys, combo))
    formatted_combinations.append((combo_label, prompt))

# Convert to DataFrame
output_df = pd.DataFrame(formatted_combinations, columns=["Tổ hợp", "Prompt"])

# Save to Excel and display
output_file = "output_gen_prompt.xlsx"
output_df.to_excel(output_file, index=False)

# Display result
import ace_tools as tools
tools.display_dataframe_to_user(name="Generated Combinations", dataframe=output_df)

# Provide file path for download
output_file
