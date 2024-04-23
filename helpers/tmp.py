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
    
    # with open('D:\jisu file\jisu\AE Github\Automated-Readme\example_code\Python\SEG\README.md', 'r') as file:
    #     markdown_text = file.read()
    #     print(f" markdown : \n{markdown_text}\n")

    #     table_data = extract_table_data(markdown_text)
    #     print(f" table data : \n{table_data}")

    #     # df_new = pd.read_table(file, sep="|", header=0, index_col=1, skipinitialspace=True).dropna(axis=1, how='all').iloc[1:]
    #     df_new = pd.read_csv(
    #                 StringIO(markdown_text.replace(' ', ' ')),  # Get rid of whitespaces
    #                 sep='|',
    #                 index_col=0
    #             ).dropna(
    #                 axis=1,
    #                 how='all'
    #             ).iloc[1:]
    #     print(f"\ndf_new : \n{df_new}")
    #     print(f"\ncol: {df_new.columns}")

    #     df_markdown = df_new.to_markdown(index=False) #
    #     print(f"\ndf_markdown : \n{df_markdown}")
    #     # df = pd.DataFrame(table_data, columns=['File Name', 'Description'])
    #     # print(f"df : \n{df.head()}")

    # 샘플 데이터프레임 생성
    data = {
        'File Name': ['file1.py', 'file2.py', 'file3.py'],
        'Description': ['Description of file1', 'Description of file2', 'Description of file3']
    }
    df_original = pd.DataFrame(data)

    # 수정할 파일 이름과 설명
    file_names = ['file1.py', 'file3.py']
    first_lines = ['Updated description of file1', 'Updated description of file3']

    # 수정할 열 이름
    column_names = ['File Name', 'Description']

    # 파일 이름이 포함된 행을 찾아 설명을 업데이트
    for i, file_name in enumerate(file_names):
        target_row = df_original[df_original[column_names[0]] == file_name].index
        if not target_row.empty:
            df_original.at[target_row[0], column_names[1]] = first_lines[i]


    # 결과 출력
    print(df_original)
        
    

if __name__ == "__main__":
    main()