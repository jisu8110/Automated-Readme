import pandas as pd
from io import StringIO
import argparse
import os
import re

column_names = ["File Name", "Description"]

def preprocessing_des(text):
    des = text.lstrip()
    if des.startswith('#'):
        des = des[1:]
    elif des.startswith('//'):
        des = des[2:]
    des = des.lstrip()
    return des

def extract_table_data(markdown_text):
    if markdown_text.strip():
        markdown_text = re.sub(r'\s{2,}', ' ', markdown_text)
        df = pd.read_csv(
                        StringIO(markdown_text.replace(' ', ' ')),  # Get rid of whitespaces
                        sep='|',
                        index_col=0
                    ).dropna(
                        axis=1,
                        how='all'
                    ).iloc[1:]
        df = df.rename(columns=dict(zip(df.columns, column_names)))
        df.index = range(0, len(df))
    else:
        df = pd.DataFrame(columns=column_names)

    return df


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
                df_original = extract_table_data(markdown_text)
                    
                for file_name in file_names:
                    file_info.append(f"[{file_name}](./{file_name})")
                df_new = pd.DataFrame({
                    column_names[0]: file_info,
                    column_names[1]: first_lines 
                })
                df_original = pd.concat([df_original, df_new]).sort_values(by=column_names[1]).reset_index(drop=True)
            
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
            print(f"=== open readme: {readme_path}")
            with open(readme_path, 'r') as file:
                markdown_text = file.read()
                print(f" markdown : {markdown_text}")
                df_original = extract_table_data(markdown_text)

                for file_name in file_names:
                    escaped_file_name = re.escape(file_name)
                    df_original = df_original[~df_original[column_names[0]].str.contains(f"{escaped_file_name}")]

                df_markdown = df_original.to_markdown(index=False)  

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
            print(f"=== open readme: {readme_path}")
            with open(readme_path, 'r') as file:
                markdown_text = file.read()
                df_original = extract_table_data(markdown_text)
                for i, file_name in enumerate(file_names):
                    target_row = df_original[df_original[column_names[0]].str.contains(file_name)].index

                    if not target_row.empty:
                        print(f"target_row : {target_row}")
                        df_original.at[target_row[0], column_names[1]] = first_lines[i]
                    else:
                        print("Target row is empty.")

            
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
            print(f"=== open readme: {readme_path}")
            with open(readme_path, 'r') as file:
                markdown_text = file.read()
                df_original = extract_table_data(markdown_text)

                for i, file_name in enumerate(file_names):
                    target_row = df_original[df_original[column_names[1]].str.contains(first_line[i])].index

                    if not target_row.empty:
                        print(f"target_row : {target_row}")
                        df_original.at[target_row[0], column_names[0]] = f"[{file_name}](./{file_name})"
                    else:
                        print("Target row is empty.")


                ###############################################
                # for file_name in file_names:
                #     file_info.append(f"[{file_name}](./{file_name})")
                # # file_info = ["[{}](./{})".format(file_name, file_name) for file_name in zip(file_names, file_names)]
                # for i in range(len(file_names)):
                #     target_row = df_original[column_names[1]].str.contains(f"{first_lines[i]}")
                #     df_original.loc[target_row, column_names[0]] = file_info[i]
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