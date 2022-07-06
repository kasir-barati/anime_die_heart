# next function

- Retrieve the next item from the iterator by calling its `__next__()` method.
  ```py
  list1 = [1, 2, 3, 4, 5]
  # converting list to iterator
  list1 = iter(list1)
  print("The contents of list are : ")
  # printing using next()
  # using default
  while True:
      val = next(list1, 'end')
      if val == 'end':
          print('list end')
          break
      else:
          print(val)
  ```

# Comparison with None

- Comparisons to singletons like None should always be done with is or is not, never the equality operators.
- [Stackoverflow Q&A](https://stackoverflow.com/questions/3965104)

# `os.path.*`

- Some useful functions on pathnames
- Unlike a unix shell, Python does not do any automatic path expansions.
- methods:
  - `os.path.dirname`
    - Returns the directory of the given file path.
  - `os.path.basename`
    - To get the file name from a complete path
  - `os.path.isabs`
    - To check if a path is absolute or not
  - `os.path.splitext`
    - To separate filename from its extension
    - Not too accurate, I mean `abc.tar.gz` will be splited into `('abc.tar', '.gz')`
