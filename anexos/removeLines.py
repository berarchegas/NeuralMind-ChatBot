# Script usado para remover linhas vazias das tabelas

def remove_empty_lines(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.split():
                outfile.write(line)

if __name__ == "__main__":
    try:
        input_file = "obras.txt"
        output_file = "whatever.txt"

        remove_empty_lines(input_file, output_file)
        print("Empty lines removed successfully.")
    except FileNotFoundError:
        print("File not found. Please check the file path and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")