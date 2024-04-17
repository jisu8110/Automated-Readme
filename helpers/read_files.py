import argparse
import os

def read_line(file_path):

    if os.path.exists(file_path):
        if file_path.endswith('.py'):
            with open(file_path, 'r') as file:
                first_line = file.readline()
                print(f"-- {file_path}")
                print("First line of the file:", first_line.strip())  # strip()으로 개행 문자 제거
        else:
            print(f"File '{file_path}' doesn't match target file type.")
    else:
        print(f"File '{file_path}' does not exist.")


def main():
    parser = argparse.ArgumentParser(description="Read a first line of the file.")
    parser.add_argument("file_path", type=str, help="Path to the target file")
    args = parser.parse_args()

    read_line(file_path=args.file_path)

if __name__ == "__main__":
    main()