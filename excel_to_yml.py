import os
import pandas as pd
import yaml
import math
# Define the input Excel file path
input_file = "stateless_bot.xlsx"

# Read the Excel file into a DataFrame
df = pd.read_excel(input_file)

# Extract the intents column and apply substring operation
intents = df["Intent"].astype(str).str[8:]  # Modify the substring operation as per your requirement
actions = df["Action"].astype(str).str[8:]
# Convert the intents to a list
intents_list = intents.str.strip('"').tolist()
actions_list = actions.str.strip('"').tolist()

# Insert "nlu_fallback" at the beginning of the intents list
intents_list.insert(0, "nlu_fallback")
actions_list.insert(0, "utter_nlu_fallback")

# Create the "bot" folder if it doesn't exist
os.makedirs("bot", exist_ok=True)
os.makedirs("bot/data", exist_ok=True)

# Write the intents list to the output YAML file with indentation
with open("bot/domain.yml", "w") as file:
    file.write("version: \"3.1\"\n\n")
    file.write("intents:\n")
    for intent in intents_list:
        file.write(f"{' ' * 2}- {intent}\n")

    file.write("\nsession_config:\n  session_expiration_time: 60\n  carry_over_slots_to_new_session: true\n\n")
    file.write("responses:\n")
    for index in range(len(intents_list)):
        file.write(f"  {actions_list[index]}:\n")
        file.write(f"  - text: \"{intents_list[index]}\"\n\n")

print("Data written to domain.yml successfully.")

with open("bot/config.yml", "w") as file:
    file.write("recipe: default.v1\nassistant_id: chembot01\nlanguage: en\n")
    file.write("pipeline: \n   - name: WhitespaceTokenizer\n   - name: RegexFeaturizer\n   - name: LexicalSyntacticFeaturizer\n   - name: CountVectorsFeaturizer\n   - name: CountVectorsFeaturizer\n     analyzer: char_wb\n     min_ngram: 1\n     max_ngram: 4\n   - name: DIETClassifier\n     epochs: 100\n     constrain_similarities: true\n   - name: EntitySynonymMapper\n   - name: ResponseSelector\n     epochs: 100\n     constrain_similarities: true\n   - name: FallbackClassifier\n     threshold: 0.70\n     ambiguity_threshold: 0.10")
    file.write("\npolicies:\n   - name: MemoizationPolicy\n   - name: RulePolicy\n   - name: UnexpecTEDIntentPolicy\n     max_history: 5\n     epochs: 100\n   - name: TEDPolicy\n     max_history: 5\n     epochs: 100\n     constrain_similarities: true")
print("Data written to config.yml successfully.")

# Generate the "rules_from_csv.yml" file
with open("bot/data/rules.yml", "w") as file:
    file.write("version: \"3.1\"\n\nrules:\n")
    for index in range(len(intents_list)):
        rule_intent = intents_list[index]
        file.write(f"{' ' * 2}- rule: {rule_intent}\n")
        file.write(f"{' ' * 4}steps:\n")
        file.write(f"{' ' * 4}- intent: {rule_intent}\n")
        file.write(f"{' ' * 4}- action: {actions_list[index]}\n\n")

print("Data written to rules.yml successfully.")

df = pd.read_excel(input_file, sheet_name="Intents")

with open("bot/data/nlu.yml", "w") as file:
    file.write("version: \"3.1\"\n\n")
    file.write("nlu:\n")
    for column in df.columns:
        if intent != "nlu_fallback":
            file.write(f"- {column}\n")
            file.write("  examples: |\n")
            for index in range(len(df[column])):
                if(str(df[column][index]) != "nan"):
                    file.write(f"{' ' * 4}- {str(df[column][index])}\n")
            # Add more example lines as needed
            file.write("\n")

print("Data written to nlu.yml successfully.")
