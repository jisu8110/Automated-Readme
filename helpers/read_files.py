import pandas as pd
from io import StringIO
import argparse
import os
import re

def preprocessing_des(text):
    des = text.lstrip()
    if des.startswith('#'):
        des = des[1:]
    elif des.startswith('//'):
        des = des[2:]
    des = des.lstrip()
    return des

# def extract_table_data(markdown_text):
#     pattern = r'\|(.+)\|(.+)\|\n\|[-]+\|[-]+\|(.+)\|'
#     matches = re.findall(pattern, markdown_text, re.MULTILINE)
#     table_data = [(name.strip(), description.strip()) for name, description, _ in matches]
#     return table_data

def extract_table_data(markdown_text):
    # pattern = r'\| \[([^]]+)\]\(([^)]+)\) \|([^|]+)\|'
    # matches = re.findall(pattern, markdown_text, re.MULTILINE)
    # table_data = [(f"[{name}]({link})", description.strip()) for name, link, description in matches]
    
    df_new = pd.read_csv(
                    StringIO(markdown_text.replace(' ', ' ')),  # Get rid of whitespaces
                    sep='|',
                    index_col=0
                ).dropna(
                    axis=1,
                    how='all'
                ).iloc[1:]

    return df_new


def group_files_by_directory(file_paths_list):
    dir_groups = {}
    for file_path in file_paths_list:
        dir_name = os.path.dirname(file_path)
        dir_groups.setdefault(dir_name, []).append(file_path)
    return dir_groups

def add_line(column_names, added_dir_groups):
    for dir_name, file_paths_list in added_dir_groups.items():
        file_names = []
        first_lines = []
        file_info = []

        for file_path in file_paths_list:
            file_name = os.path.basename(file_path)
            file_names.append(file_name)

            if os.path.exists(file_path):
                print(f"=== open file: {file_path}")
                with open(file_path, 'r') as file:
                    first_line = file.readline().strip()
                    first_lines.append(preprocessing_des(first_line))
            else:
                print(f"There's no file in {file_path}")

        readme_path = os.path.join(dir_name, "README.md")
        if os.path.exists(readme_path):
            print(f"=== open readme: {readme_path}")
            with open(readme_path, 'r') as file:
                markdown_text = file.read()
                print(f" markdown : {markdown_text}")
                if markdown_text != None:
                    df_original = extract_table_data(markdown_text)
                else:
                    df_original = pd.DataFrame(columns=column_names)

                # table_data = extract_table_data(markdown_text)
                # print(f" table data : {table_data}")
                # df_original = pd.DataFrame(table_data, columns=column_names)

                ###############################################
                for file_name in file_names:
                    file_info.append(f"[{file_name}](./{file_name})")
                # file_info = ["[{}](./{})".format(file_name, file_name) for file_name in zip(file_names, file_names)]
                print("[[[ file_info ]]]")
                print(file_info)
                print("[[[ first_lines ]]]")
                print(first_lines)
                df_new = pd.DataFrame({
                    column_names[0]: file_info,
                    column_names[1]: first_lines 
                })
                df_original = pd.concat([df_original, df_new]).sort_values(by=column_names[0]).reset_index(drop=True)
                ###############################################
            
                df_markdown = df_original.to_markdown(index=False)

            with open(readme_path, 'w+') as file:
                file.write(df_markdown)
        else:
            print(f"There's no file in {file_path}")

def delete_line(column_names, deleted_dir_groups):
    for dir_name, file_paths_list in deleted_dir_groups.items():
        file_names = []

        for file_path in file_paths_list:
            file_name = os.path.basename(file_path)
            file_names.append(file_name)

        readme_path = os.path.join(dir_name, "README.md")
        if os.path.exists(readme_path):
            print(f"=== open readme: {file_path}")
            with open(readme_path, 'r') as file:
                markdown_text = file.read()
                print(f" markdown : {markdown_text}")

                df_original = extract_table_data(markdown_text)


                # table_data = extract_table_data(markdown_text)
                # print(f" table data : {table_data}")

                # df_original = pd.DataFrame(table_data, columns=column_names)
                # print(f"===original df===")
                # print(df_original)

                ###############################################
                for file_name in file_names:
                    escaped_file_name = re.escape(file_name)
                    df_original = df_original[~df_original[column_names[0]].str.contains(f"{escaped_file_name}")]

                    # df_original = df_original[~df_original[column_names[0]].str.contains(f"[{file_name}]")]
                    # print(f"file_name : {file_name}")
                    # print(df_original)
                    # df_original = df_original[df_original[column_names[0]].str.contains({file_name}) == False]
                    
                # df_original = df_original[~df_original[column_names[0]].str.contains('|'.join(file_names))]

                ###############################################
                # print()
            
                df_markdown = df_original.to_markdown(index=False) # 

            with open(readme_path, 'w+') as file:
                file.write(df_markdown)
        else:
            print(f"There's no file in {file_path}")

def modify_line(column_names, modified_dir_groups):
    for dir_name, file_paths_list in modified_dir_groups.items():
        file_names = []
        first_lines = []

        for file_path in file_paths_list:
            file_name = os.path.basename(file_path)
            file_names.append(file_name)

            if os.path.exists(file_path):
                print(f"=== open file: {file_path}")
                with open(file_path, 'r') as file:
                    first_line = file.readline().strip()
                    first_lines.append(preprocessing_des(first_line))
            else:
                print(f"There's no file in {file_path}")

        readme_path = os.path.join(dir_name, "README.md")
        if os.path.exists(readme_path):
            print(f"=== open readme: {file_path}")
            with open(readme_path, 'r') as file:
                markdown_text = file.read()
                table_data = extract_table_data(markdown_text)
                df_original = pd.DataFrame(table_data, columns=column_names)

                ###############################################
                for i in range(len(file_names)):
                    target_row = df_original[column_names[0]].str.contains(f"[{file_names[i]}]")
                    df_original.loc[target_row, column_names[1]] = first_lines[i]
                ###############################################
            
                df_markdown = df_original.to_markdown(index=False)

            with open(readme_path, 'w+') as file:
                file.write(df_markdown)
        else:
            print(f"There's no file in {file_path}")

def rename_line(column_names, renamed_dir_groups):
    for dir_name, file_paths_list in renamed_dir_groups.items():
        file_names = []
        first_lines = []
        file_info = []

        for file_path in file_paths_list:
            file_name = os.path.basename(file_path)
            file_names.append(file_name)

            if os.path.exists(file_path):
                print(f"=== open file: {file_path}")
                with open(file_path, 'r') as file:
                    first_line = file.readline().strip()
                    first_lines.append(preprocessing_des(first_line))
            else:
                print(f"There's no file in {file_path}")

        readme_path = os.path.join(dir_name, "README.md")
        if os.path.exists(readme_path):
            print(f"=== open readme: {file_path}")
            with open(readme_path, 'r') as file:
                markdown_text = file.read()
                table_data = extract_table_data(markdown_text)
                df_original = pd.DataFrame(table_data, columns=column_names)

                ###############################################
                for file_name in file_names:
                    file_info.append(f"[{file_name}](./{file_name})")
                # file_info = ["[{}](./{})".format(file_name, file_name) for file_name in zip(file_names, file_names)]
                for i in range(len(file_names)):
                    target_row = df_original[column_names[1]].str.contains(f"{first_lines[i]}")
                    df_original.loc[target_row, column_names[0]] = file_info[i]
                ###############################################
            
                df_markdown = df_original.to_markdown(index=False)

            with open(readme_path, 'w+') as file:
                file.write(df_markdown)
        else:
            print(f"There's no file in {file_path}")


def main():
    parser = argparse.ArgumentParser(description="Read a first line of the file.")
    parser.add_argument("added_files", type=str, help="Path to the added files")
    parser.add_argument("deleted_files", type=str, help="Path to the deleted files")
    parser.add_argument("modified_files", type=str, help="Path to the modified files")
    parser.add_argument("renamed_files", type=str, help="Path to the renamed files")
    args = parser.parse_args()

    column_names = ["File Name", "Description"]
    
    added_dir_groups = group_files_by_directory(args.added_files.split())
    deleted_dir_groups = group_files_by_directory(args.deleted_files.split())
    modified_dir_groups = group_files_by_directory(args.modified_files.split())
    renamed_dir_groups = group_files_by_directory(args.renamed_files.split())
    
    add_line(column_names, added_dir_groups)
    delete_line(column_names, deleted_dir_groups)
    modify_line(column_names, modified_dir_groups)
    rename_line(column_names, renamed_dir_groups)
    

if __name__ == "__main__":
    main()