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
 - First round of changes I want: 
    - modularize the style gathering process.  I should make a writingstyle.md file that I can update as i see fit.  It doesn't make a ton of sense to generate that over and over if it'll be (mostly) static. 
    - For now, remove the date from the header of the post.md blog file that gets generated. This has scheduling functionality in Jekyll which means if I put the date to today and don't align the date AND time with whatever system time github pages uses (I'm assuming this is what's going on, system time stuff is a great enemy)
    - Pull the notes.md file I create with each of these repos.  That plus the style guide should be enough to create a solid first draft.
    - If draft is denied instead of being iterated on, ask if you want to save it as a draft.  
- I need to break down this process a TON! I mean, especially because I'm working with an  8b model, but also because the probabilistic nature of the LLMs makes it so, when they do mess up, you don't want them trying to do 10 things at once.  At least the small ones.  The question is probably one of effort and total steps though, which is what makes these systems so interesting. 
    - To expand a little, I think it's interesting that you could give a long set of instructions to a very cheap, very fast model, and lets say out of 10 runs it hits an average of 4 steps per run.  
    - If you broke down that single longer script into 4 shorter steps, you're not ever going to beat the step game, which means the latency back and forth (even locally to begin processing each call) will be a bottleneck
    - If you broke it down into very small steps though, you could finish the step faster, and theoretically fix problems in the step faster (since the LLM kinda just retries the same thing over and over with slightly different fixes).  The fewer things that could go wrong when fixing = faster fixes. 
- Or maybe I don't need to break anything down, and I should just max out in the other direction with LLM power.  I'm using almost the bottom of the barrel with these 8B models.  I could utilize something like Flash 2.5 or V3.1 without any cost.  
- I gave it another try and it worked surprisingly well! 
    - Already on branch: master Pulling latest changes from origin/master... Pull successful.
    File '_posts/20250510-Stinky-Farts-Today.md' written successfully.
    File '_posts/20250510-Stinky-Farts-Today.md' added to index.
    Committed with message: 'Add new blog post: Stinky Farts Today'
    Pushing to origin/master...
    Push successful.
    Out - Final answer: Successfully created, committed, and pushed 
    '_posts/20250510-Stinky-Farts-Today.md' with message: 'Add new blog post:  
    Stinky Farts Today' to branch 'master'.
    [Step 5: Duration 10.75 seconds| Input tokens: 40,264 | Output tokens: 3,174]
    - Main technical problem I see is the date format is missing (-).  Again highlights how this whole thing would function better as different steps/tools.  Come to think of it I don't actually know how to make separate steps, only tools. 
- After fixing the date and reviewing the blog, it's very very mid! which, tracks for a fully default 8b model.  
    - Bad things are it making stuff up, which, is just on me.  I gave it no context besides my existing posts.  It made up youtube videos (and linked to the Bohemian Rhapsody music video by the Muppets).  This goes to show you that if you are using something small, Filllll that context window. 
    - Good things are the formatting and the github commit stuff all working.  Very cool to see the change live!
- I've got https://github.com/Arize-ai/phoenix installed and will add the telemetry to the agents.  
- Because I'm trying to bring all these systems together, this might also be a good opportunity to use https://github.com/upstash/context7.  I'm not sure how to use it with Aider, so if that's too much to integrate I might just wait til the next project to investigate.  I think utilizing the /web functionality in aider with doc pages will work well enough
- JESUS CHRIST Gemini 2.0 flash murdered it first try. 