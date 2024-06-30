# import libraries

import os
import csv
import anthropic
from prompts import *

if not os.getenv('ANTHROPIC_API_KEY'):
    os.environ['ANTHROPIC_API_KEY'] = input(
        "Please enter your Anthropics API key: ")

# create the anthropic client
client = anthropic.Anthropic()
sonnet = "claude-3-5-sonnet-20240620"


# function to read the csv file from user
def read_csv(file_path):
    data = []
    with open(file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data.append(row)
    return data

# function to save the generated data to a new csv file


def save_to_csv(data, output_file, headers=None):
    mode = 'w' if headers else 'a'
    with open(output_file, mode, newline='') as f:
        writer = csv.writer(f)
        if headers:
            writer.writerow(headers)
        for row in csv.reader(data.splitlines()):
            writer.writerow(row)


# Create the Analyzer Agent
def analyzer_agent(sample_data):
    message = client.messages.create(
        model=sonnet,
        max_tokens=400,
        temperature=0.1,
        system=ANALYZER_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": ANALYZER_USER_PROMPT.format(sample_data=sample_data)
            }
        ]
    )
    return message.content[0].text

# create the Generator Agent


def generator_agent(sample_data, analysis_results, num_rows=30):
    message = client.messages.create(
        model=sonnet,
        max_tokens=1500,
        temperature=1,
        system=GENERATOR_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": GENERATOR_USER_PROMPT.format(
                    num_rows=num_rows, analysis_results=analysis_results, sample_data=sample_data)
            }
        ]
    )
    return message.content[0].text

# Main execution flow

#Get input from the uder
file_path = input("Enter the path to the CSV file: ")
file_path = os.path.join('/app/data', file_path)
desired_rows = int(input("Enter the number of rows you want to generate: "))

# Read the CSV file
sample_data = read_csv(file_path)
sample_data_str = '\n'.join([','.join(row) for row in sample_data])

print("\nLaunching team of Agents...")
analysis_results = analyzer_agent(sample_data_str)
print("\n### Analyzer Agent Output: ###")
print(analysis_results)
print("\n-----------------------\n\nGenerating new data...")


# Set up the output file
output_file = "/app/data/generated_data.csv"
headers = sample_data[0]

save_to_csv("", output_file, headers)

batch_size = 30
generated_rows = 0
while generated_rows < desired_rows:
    rows_to_generate = min(batch_size, desired_rows - generated_rows)
    generated_data = generator_agent(sample_data_str, analysis_results, rows_to_generate)
    save_to_csv(generated_data, output_file)
    generated_rows += rows_to_generate
    print(f"Generated {generated_rows} rows of {desired_rows}")

print(f"Generated data has saved to {output_file}")