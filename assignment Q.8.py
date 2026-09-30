import os
import pickle
import zipfile

def build_index(folder_path, output_zip):
    index = {}
    total_files = 0
    total_lines = 0

    # Scan all files in the folder
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            total_files += 1
            with open(filepath, "r", encoding="utf-8") as f:
                for line_no, line in enumerate(f, start=1):
                    total_lines += 1
                    tokens = line.strip().lower().split()
                    for token in tokens:
                        if token not in index:
                            index[token] = []
                        index[token].append((filename, line_no))

    # Save index using pickle
    pickle_file = "index.pkl"
    with open(pickle_file, "wb") as pf:
        pickle.dump(index, pf)

    # Compress logs + index into zip
    with zipfile.ZipFile(output_zip, "w") as zf:
        zf.write(pickle_file)
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            if os.path.isfile(filepath):
                zf.write(filepath)

    print(f"FILES {total_files}")
    print(f"LINES {total_lines}")
    print(f"TOKENS {len(index)}")


def search_index(pickle_path, queries):
    with open(pickle_path, "rb") as pf:
        index = pickle.load(pf)

    for token in queries:
        token = token.lower()
        if token in index:
            print(f"{token}:")
            for file, line in index[token]:
                print(f"  {file}:{line}")
        else:
            print(f"{token}: Not found")


# ---------------- SAMPLE USAGE ----------------
# BUILD mode
# Assume we have a folder "logs" containing files:
# log1.txt, log2.txt, log3.txt
# Each file has some text lines.

build_index("logs", "archive.zip")

# SEARCH mode
search_index("index.pkl", ["error", "login", "timeout"])
