import pandas as pd
from io import StringIO
import argparse
import os
import re


# def extract_table_data(markdown_text):
#     pattern = r'\|(.+)\|(.+)\|\n\|[-]+\|[-]+\|(.+)\|'
#     matches = re.findall(pattern, markdown_text, re.MULTILINE)
#     table_data = [(name.strip(), description.strip()) for name, description, _ in matches]
#     return table_data

def extract_table_data(markdown_text):
    pattern = r'\| \[([^]]+)\]\(([^)]+)\) \|([^|]+)\|'
    matches = re.findall(pattern, markdown_text, re.MULTILINE)
    table_data = [(f"[{name}]({link})", description.strip()) for name, link, description in matches]
    return table_data



def main():
    
    with open('D:\jisu file\jisu\AE Github\Automated-Readme\example_code\Python\SEG\README.md', 'r') as file:
        markdown_text = file.read()
        print(f" markdown : \n{markdown_text}\n")

        table_data = extract_table_data(markdown_text)
        print(f" table data : \n{table_data}")

        # df_new = pd.read_table(file, sep="|", header=0, index_col=1, skipinitialspace=True).dropna(axis=1, how='all').iloc[1:]
        df_new = pd.read_csv(
                    StringIO(markdown_text.replace(' ', ' ')),  # Get rid of whitespaces
                    sep='|',
                    index_col=1
                ).dropna(
                    axis=1,
                    how='all'
                ).iloc[1:]
        print(f"\ndf_new : \n{df_new}")

        df_markdown = df_new.to_markdown() #index=False
        print(f"\ndf_markdown : \n{df_markdown}")

        # df = pd.DataFrame(table_data, columns=['File Name', 'Description'])
        # print(f"df : \n{df.head()}")
        
    

if __name__ == "__main__":
    main()