import pandas as pd
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

def extract_table_data(markdown_text):
    pattern = r'\|(.+)\|(.+)\|\n\|[-]+\|[-]+\|(.+)\|'
    matches = re.findall(pattern, markdown_text, re.MULTILINE)
    table_data = [(name.strip(), description.strip()) for name, description, _ in matches]
    return table_data

def add_line(column_names, file_paths):
    print("[[[ fisrt file_paths ]]]")
    print(type(file_paths))
    print(len(file_paths))
    print(file_paths)
    file_paths_list = file_paths.split()

    dir_groups = {}
    
    print("[[[ for file_paths ]]]")
    for file_path in file_paths_list:
        print(file_path)
        dir_name = os.path.dirname(file_path)
        dir_groups.setdefault(dir_name, []).append(file_path)
    print("[[[ dir_groups ]]]")
    print(dir_groups)

    for dir_name, file_paths_list in dir_groups.items():
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

                file_info = ["[{}]({})".format(file_name, file_path) for file_name, file_path in zip(file_names, file_paths_list)]
                print("[[[ file_info ]]]")
                print(file_info)
                print("[[[ first_lines ]]]")
                print(first_lines)
                df_new = pd.DataFrame({
                    column_names[0]: file_info,
                    column_names[1]: first_lines 
                })
                df_original = pd.concat([df_original, df_new]).sort_values(by=column_names[0]).reset_index(drop=True)
                df_markdown = df_original.to_markdown(index=False)

            with open(readme_path, 'w+') as file:
                file.write(df_markdown)
        else:
            print(f"There's no file in {file_path}")



# def delete_line(column_names, file_paths):

#     for file_path in file_paths:

#         ###### 리드미에서 삭제
#         ###### ==============================

# def modify_line(column_names, file_paths):

#     for file_path in file_paths:

#         ###### 리드미에서 수정
#         ###### ==============================

# def rename_line(column_names, file_paths):

#     for file_path in file_paths:

#         ###### 리드미에서 수정
#         ###### ==============================

def main():
    parser = argparse.ArgumentParser(description="Read a first line of the file.")
    parser.add_argument("added_files", type=str, help="Path to the added files")
    parser.add_argument("deleted_files", type=str, help="Path to the deleted files")
    parser.add_argument("modified_files", type=str, help="Path to the modified files")
    parser.add_argument("renamed_files", type=str, help="Path to the renamed files")
    args = parser.parse_args()

    # read_line(added_files = args.added_files, 
    #           deleted_files = args.deleted_files, 
    #           modified_files = args.modified_files, 
    #           renamed_files = args.renamed_files,)

    column_names = ["File Name", "Description"]

    add_line(column_names, args.added_files)
    # delete_line(column_names, args.deleted_files)
    # modify_line(column_names, args.modified_files)
    # rename_line(column_names, args.renamed_files)
    

if __name__ == "__main__":
    main()