import yaml

def parse_yaml(file_path) -> dict:
    with open(file_path, 'r') as stream:
        try:
            yaml_data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    
    responses_dict = yaml_data['responses']
    
    # Create a simplified dictionary where the response key maps to the first 'text' field in the list of responses.
    simplified_responses_dict = {k: v[0]['text'] for k, v in responses_dict.items()}
    
    return simplified_responses_dict

file_path = 'your_file_path.yml'  # replace with your file path
responses = parse_yaml(file_path)
print(responses)