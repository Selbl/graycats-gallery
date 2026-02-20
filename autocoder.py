import os
import subprocess
import time
from google import genai

# --- Configuration ---
MAX_ITERATIONS = 10
FILE_TO_EDIT = "app.py"
NEW_BRANCH_NAME = "gemini-autonomous-improvements"

# Initialize the Gemini client (It automatically looks for the GEMINI_API_KEY environment variable)
client = genai.Client()

def run_cmd(cmd):
    """Helper to run terminal commands."""
    subprocess.run(cmd, shell=True, check=True, capture_output=True)

def get_code():
    with open(FILE_TO_EDIT, "r") as f:
        return f.read()

def save_code(code_string):
    # Strip markdown code blocks if the model includes them
    clean_code = code_string.replace("```python", "").replace("```", "").strip()
    with open(FILE_TO_EDIT, "w") as f:
        f.write(clean_code)

def main():
    print(f"✨ Starting autonomous coding loop for {MAX_ITERATIONS} iterations...")
    
    # 1. Create and checkout the new branch
    run_cmd(f"git checkout -B {NEW_BRANCH_NAME}")
    
    change_log = []

    # 2. The Iteration Loop
    for i in range(MAX_ITERATIONS):
        print(f"\n--- Iteration {i+1} of {MAX_ITERATIONS} ---")
        current_code = get_code()
        
        # The Prompt: Instructing the model on what to do
        prompt = f"""
        Act as an expert Streamlit developer. Review the following code for a Reddit cat photo gallery.
        Identify ONE small, meaningful improvement you can make (e.g., a new UI feature, better error handling, a new animation, or cleaner code).
        
        Return ONLY the completely updated, runnable Python code. Do not include explanations.
        
        Current Code:
        {current_code}
        """
        
        print("🧠 Gemini is thinking and writing code...")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        # Save the new code
        save_code(response.text)
        
        # Ask Gemini to write a 1-sentence commit message about what it just did
        summary_prompt = "In one short sentence, summarize the single change that was just made to this code: \n" + response.text
        commit_msg = client.models.generate_content(model='gemini-2.5-flash', contents=summary_prompt).text.strip()
        change_log.append(f"Iteration {i+1}: {commit_msg}")
        
        # 3. Commit the changes to Git
        print(f"💾 Committing: {commit_msg}")
        run_cmd(f"git add {FILE_TO_EDIT}")
        run_cmd(f'git commit -m "Auto-Update {i+1}: {commit_msg}"')

        # Add a 30-second pause to respect API rate limits
        print("⏳ Sleeping for 30 seconds to respect API limits...")
        time.sleep(30)

    # Push the new branch to GitHub
    print("\n🚀 Pushing the new branch to GitHub...")
    run_cmd(f"git push -u origin {NEW_BRANCH_NAME}")

    # 4. Generate and display the final summary
    print("\n=========================================")
    print("✅ AUTONOMOUS LOOP COMPLETE! ✅")
    print("=========================================\n")
    print("Here is the summary of what changed:\n")
    for change in change_log:
        print(f"- {change}")

if __name__ == "__main__":
    main()