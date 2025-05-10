import os
import sys
from datetime import datetime
from smolagents import CodeAgent, LiteLLMModel, tool
from git import Repo, GitCommandError # pip install GitPython

# --- Custom Tool Definitions ---

@tool
def get_current_date_tool() -> str:
    """
    Returns the current date in YYYY-MM-DD format.
    This is useful for naming blog posts and for the date part in the Jekyll frontmatter.
    """
    return datetime.now().strftime("%Y-%m-%d")

@tool
def github_commit_tool(repo_path: str, relative_file_path: str, file_content: str, commit_message: str) -> str:
    """
    Adds a new file to the specified local Git repository, commits it, and pushes to the default remote's default branch (e.g., origin/main or origin/master).
    It first tries to pull the latest changes from the remote.

    Args:
        repo_path: The absolute local path to the Git repository.
        relative_file_path: The path of the file to be created/updated, relative to the repository root (e.g., '_posts/2023-10-27-new-post.md').
        file_content: The content to write into the file.
        commit_message: The commit message.
    """
    try:
        repo = Repo(repo_path)
        origin = repo.remotes.origin

        # Determine default branch (common names)
        default_branch_name = ""
        if "main" in repo.heads:
            default_branch_name = "main"
        elif "master" in repo.heads:
            default_branch_name = "master"
        else:
            # If not main or master, try to get the symbolic ref for HEAD from remote
            try:
                remote_head = next(r for r in origin.refs if r.name == 'origin/HEAD')
                default_branch_name = remote_head.ref.name.split('/')[-1]
            except StopIteration:
                 # Fallback to current active branch if remote HEAD is not clear
                default_branch_name = repo.active_branch.name
                print(f"Warning: Could not reliably determine default remote branch (main/master/HEAD). Using current active branch: {default_branch_name}")


        # Checkout default branch if not already on it
        if repo.active_branch.name != default_branch_name:
            print(f"Switching to branch: {default_branch_name}")
            repo.git.checkout(default_branch_name)
        else:
            print(f"Already on branch: {default_branch_name}")

        print(f"Pulling latest changes from origin/{default_branch_name}...")
        try:
            origin.pull(default_branch_name)
            print("Pull successful.")
        except GitCommandError as e:
            if "Already up to date." in str(e):
                print("Already up to date.")
            elif "fatal: couldn't find remote ref" in str(e) or "no tracking information" in str(e):
                 print(f"Warning: Could not pull. Branch '{default_branch_name}' might not be tracked or remote ref not found. Proceeding without pull.")
            else:
                print(f"Git pull error: {e}. Attempting to proceed, but conflicts might occur.")
                # return f"Error during Git pull: {e}. Please resolve conflicts or check repository state." # Option to stop

        # Create/Update the file
        full_file_path = os.path.join(repo_path, relative_file_path)
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
        with open(full_file_path, "w", encoding="utf-8") as f:
            f.write(file_content)
        print(f"File '{relative_file_path}' written successfully.")

        # Add, commit, and push
        repo.index.add([full_file_path])
        print(f"File '{relative_file_path}' added to index.")
        repo.index.commit(commit_message)
        print(f"Committed with message: '{commit_message}'")

        print(f"Pushing to origin/{default_branch_name}...")
        origin.push(default_branch_name)
        print("Push successful.")
        return f"Successfully created, committed, and pushed '{relative_file_path}' with message: '{commit_message}' to branch '{default_branch_name}'."

    except GitCommandError as e:
        print(f"Git command error: {e}")
        return f"Error during Git operation: {e}. Please check Git setup, permissions, and repository state (e.g., merge conflicts)."
    except Exception as e:
        print(f"An unexpected error occurred in github_commit_tool: {e}")
        return f"An unexpected error occurred: {e}"

# --- Configuration ---
# IMPORTANT: Set your LiteLLM model ID.
# Examples: "gpt-4o", "anthropic/claude-3-5-sonnet-20240620", "ollama_chat/llama3" (if ollama is running)
# Ensure necessary API keys (e.g., OPENAI_API_KEY, ANTHROPIC_API_KEY) are set in your environment
# or pass api_key="YOUR_KEY" to LiteLLMModel.
LLM_MODEL_ID = "openrouter/qwen/qwen-2.5-7b-instruct:free"  # <--- CHANGE THIS TO YOUR PREFERRED MODEL

# IMPORTANT: Set the absolute path to your local clone of the blog repository
LOCAL_BLOG_REPO_PATH = r'C:\Users\maxro\Documents\GitHub\burntpineapple52.github.io'  # <--- CHANGE THIS

# Relative path to the posts directory within your blog repo
POSTS_DIR = "_posts"  # Usually this for Jekyll

# IMPORTANT: Set the filenames of your example posts (located in LOCAL_BLOG_REPO_PATH/POSTS_DIR/)
EXAMPLE_POST_1_FILENAME = "2024-10-03-today-1.md" # <--- CHANGE THIS
EXAMPLE_POST_2_FILENAME = "2024-10-04-today-2.md" # <--- CHANGE THIS

# --- Helper to read example files ---
def get_example_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: Example post {file_path} not found. Style guidance will be limited.")
        return "No example content available."
    except Exception as e:
        print(f"Warning: Error reading {file_path}: {e}. Style guidance will be limited.")
        return "Error reading example content."

# --- Main Application Logic ---
def blog_post_assistant():
    print("Welcome to the AI Blog Post Assistant!")

    if LOCAL_BLOG_REPO_PATH == ".\burntpineapple52.github.io":
        print("ERROR: Please update 'LOCAL_BLOG_REPO_PATH' in the script with the actual path to your blog repository.")
        return

    # Initialize LiteLLMModel
    # If your model needs an api_base (e.g., for Ollama or local OpenAI-compatible servers):
    # llm_model = LiteLLMModel(model_id=LLM_MODEL_ID, api_base="http://localhost:11434")
    # If your model requires an API key directly:
    # llm_model = LiteLLMModel(model_id=LLM_MODEL_ID, api_key="sk-...")
    llm_model = LiteLLMModel(model_id=LLM_MODEL_ID)
    print(f"Using LLM: {LLM_MODEL_ID}")

    # Initialize Agent
    tools = [get_current_date_tool, github_commit_tool]
    agent = CodeAgent(tools=tools, model=llm_model, add_base_tools=False)

    user_topic = input("What topic would you like the blog post to be about?\n> ")

    example_post_path_1 = os.path.join(LOCAL_BLOG_REPO_PATH, POSTS_DIR, EXAMPLE_POST_1_FILENAME)
    example_post_path_2 = os.path.join(LOCAL_BLOG_REPO_PATH, POSTS_DIR, EXAMPLE_POST_2_FILENAME)
    example_content_1 = get_example_content(example_post_path_1)
    example_content_2 = get_example_content(example_post_path_2)

    initial_prompt = f"""
You are a helpful AI assistant that helps write blog posts for a personal Jekyll blog.
Your goal is to generate a new blog post based on the user's topic.

**User's Topic:** "{user_topic}"

**Style and Tone Guidelines:**
Please emulate the style and tone of the following example posts:
--- EXAMPLE POST 1 ---
{example_content_1}
--- END EXAMPLE POST 1 ---

--- EXAMPLE POST 2 ---
{example_content_2}
--- END EXAMPLE POST 2 ---

**Formatting Requirements (Jekyll Markdown):**
The post MUST be in Markdown format.
It MUST include Jekyll frontmatter at the very beginning, enclosed by triple hyphens (---).
The frontmatter should include (adapt based on examples if they differ, but ensure these are present):
- layout: post
- title: [A suitable title for the blog post, based on the topic. This title will also be used for the filename and commit message.]
- date: [Use the `get_current_date_tool()` to get today's date in YYYY-MM-DD format. Then, construct the full date string for Jekyll like 'YYYY-MM-DD HH:MM:SS +/-ZZZZ'. For example, if the tool returns '2024-07-29', you could use '2024-07-29 10:00:00 -0700'. Pick a sensible time (e.g., 10:00:00) and a common timezone offset (e.g., -0700 for PDT, +0000 for UTC, or match the examples).]
- (Include other common frontmatter fields from the examples, like 'tags: [tag1, tag2]', 'categories: [category]', 'excerpt_separator: "<!--more-->"', etc. If examples have 'author', include that too.)

The filename for the post should be in the format: YYYY-MM-DD-slugified-title.md.
A slugified title is all lowercase, with spaces replaced by hyphens, and special characters (not alphanumeric or hyphens) removed or transliterated. For example, "My Awesome Post!" becomes "my-awesome-post".

**Your Task:**
1. Generate a compelling title for the blog post based on the user's topic.
2. Use the `get_current_date_tool()` to get today's date for the frontmatter and filename.
3. Construct the full blog post content, including the Jekyll frontmatter and the main body.
4. The main body should be well-structured, engaging, and match the style of the examples.
5. Output the complete Markdown content of the blog post (frontmatter + body) by calling `final_answer(markdown_content)`. Do NOT try to commit it yet.
    """

    print("\nGenerating initial draft...")
    current_draft = agent.run(initial_prompt)
    print("\n--- DRAFT ---")
    print(current_draft)
    print("--- END DRAFT ---\n")

    while True:
        action = input("Review the draft. Type your feedback, 'approve' to commit, or 'deny' to stop.\n> ").strip().lower()

        if action == 'deny':
            print("Operation cancelled by user.")
            break
        elif action == 'approve':
            # Extract title from draft for commit message and filename
            extracted_title = "New Blog Post" # Default
            if current_draft and isinstance(current_draft, str):
                try:
                    lines = current_draft.splitlines()
                    for line in lines:
                        if line.lower().startswith("title:"):
                            extracted_title = line.split(":", 1)[1].strip()
                            # Remove potential quotes around title
                            if extracted_title.startswith(('"', "'")) and extracted_title.endswith(('"', "'")):
                                extracted_title = extracted_title[1:-1]
                            break
                except Exception as e:
                    print(f"Could not automatically extract title due to: {e}. Using default: '{extracted_title}'")
            else:
                print(f"Draft content is not a string or is empty. Using default title: '{extracted_title}'")


            commit_prompt = f"""
The user has approved the following blog post content:
--- APPROVED CONTENT ---
{current_draft}
--- END APPROVED CONTENT ---

The title of this post is (or should be close to): "{extracted_title}"

Your tasks are:
1. Get the current date using `get_current_date_tool()`. Let this be `current_date_str`.
2. Create a slugified version of the title: "{extracted_title}". A slugified title is all lowercase, spaces replaced by hyphens, and non-alphanumeric characters (except hyphens) removed. For example, "My Awesome Post! & More" becomes "my-awesome-post-and-more".
3. Construct the full filename: `{{current_date_str}}-{{slugified_title}}.md`. For example, if date is "2024-07-29" and slug is "my-title", filename is "2024-07-29-my-title.md".
4. The file should be placed in the '{POSTS_DIR}/' directory of the repository. So the `relative_file_path` for the tool will be '{POSTS_DIR}/{{filename}}'.
5. Use the `github_commit_tool()` with the following arguments:
    - repo_path: "{LOCAL_BLOG_REPO_PATH}"
    - relative_file_path: The path constructed in step 4.
    - file_content: The "APPROVED CONTENT" provided above.
    - commit_message: "Add new blog post: {extracted_title}"
6. Call `final_answer()` with the exact string output returned by the `github_commit_tool()`.
            """
            print("\nAttempting to commit and push to GitHub...")
            commit_result = agent.run(commit_prompt, reset=False) # reset=False to maintain context if needed, though for a final action it might not be critical
            print(f"\nCommit Result: {commit_result}")
            break
        else: # User provided feedback
            feedback_prompt = f"""
The user has reviewed the previous draft and provided feedback.

Previous Draft:
---
{current_draft}
---
User's Feedback: "{action}"

Please revise the draft based on this feedback, keeping all original style and formatting requirements in mind.
Ensure the Jekyll frontmatter is correct and complete as per the initial instructions (layout, title, date format, etc.).
Output the complete revised Markdown content by calling `final_answer(revised_markdown_content)`.
            """
            print("\nRevising draft based on feedback...")
            current_draft = agent.run(feedback_prompt, reset=False)
            print("\n--- REVISED DRAFT ---")
            print(current_draft)
            print("--- END REVISED DRAFT ---\n")

if __name__ == "__main__":
    blog_post_assistant()