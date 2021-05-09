# finddup
find file and folder duplicates quickly

- `group.py` helper module
- `filedup.py` hashes all files to find dupes (from https://www.pythoncentral.io/finding-duplicate-files-with-python/)
- `folddup.py` finds duplicate subfolders using pairwise comparison
  - `folddup_m.py` uses multiprocessing and tries to avoid unnecessary computation
- `folddup_h.py` finds duplicate subfolders it by hashing everything
