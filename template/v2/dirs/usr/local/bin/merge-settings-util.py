import json
from sys import argv


# merges json files file1 and file2, overwriting any settings that already exist in file1
# todo: add error handling and logging
def main():
    file1, file2 = argv[1], argv[2]
    # Read JSON data from files
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    # Merge the data (simple update)
    merged_data = {**data1, **data2}

    # Write the merged data to a new file
    with open(file2, 'w') as f:
        json.dump(merged_data, f)


if __name__ == "__main__":
    main()
