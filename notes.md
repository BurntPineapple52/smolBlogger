# NOTES
- goals
    - learn about smolagents from huggingface
    - improve my blog creation process, which is to use aider within my github blog project.  It's fast but I have to navigate to the project and manually add context *sob*
- I started by checking in with 2.5 pro on aistudio about my idea to use smolagents vs ADK from google or langgraph.  Smolagents seems to be powerful enough to do what I need while keeping everything light and vendor agnostic. Just what I like to hear. 
- I got the smolagent documentation from their github, and specifically added the guided tour text as context into gemini 2.5 pro (just copy/paste)https://github.com/huggingface/smolagents/blob/main/docs/source/en/guided_tour.mdx
- I then asked for guided instructions to set up my blogging agents. Here's my attempt to implement based off of that.  I'll be saving the instructions as imp1.md
 - sick I got smolagent to run a test, and it looks like it's functioning fine just fine.  websearch worked and the fibanachi test worked.  Token usage seems acceptable with input tokens at ~5k and output at ~500 per 2 step task. 
 - model wise I've been using qwen 2.5 7b instruct free via litellm and openrouter. 
 - I tried to do a mini "research" question, asking it to return the highest starred LLM observability platforms, and it did a good job! It got stuck for a bunch of loops, I think cause qwen 7b is just too small a context window to do real webscraping, but it still got me a good list.  