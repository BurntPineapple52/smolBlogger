from smolagents import CodeAgent, LiteLLMModel

model = LiteLLMModel(model_id="openrouter/qwen/qwen-2.5-7b-instruct:free") # Could use 'gpt-4o'
agent = CodeAgent(tools=[], model=model, add_base_tools=True)

agent.run(
    "Search for open source ai observability platforms on github.  Sort by stars and provide a short summary of each. Output as a table",
)