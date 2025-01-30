import os

def apply_patch():
    # Path to the ShExDocLexer.py file inside your virtual environment
    venv_path = os.path.join(os.getenv("VIRTUAL_ENV"), "Lib", "site-packages", "pyshexc", "parser", "ShExDocLexer.py")
    
    try:
        # Open the file for reading and modifying
        with open(venv_path, "r") as file:
            file_content = file.read()

        # Replace 'from typing.io import TextIO' with 'from typing import TextIO'
        file_content = file_content.replace("from typing.io import TextIO", "from typing import TextIO")
        
        # Write the changes back to the file
        with open(venv_path, "w") as file:
            file.write(file_content)
        
        print("Patch applied successfully!")
    
    except FileNotFoundError:
        print(f"Could not find the file: {venv_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    apply_patch()
