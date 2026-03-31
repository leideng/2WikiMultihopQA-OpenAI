from openai import OpenAI
import os


client = OpenAI(
	api_key=os.getenv("OPENAI_API_KEY"),
	base_url=os.getenv("OPENAI_BASE_URL")
)

completion = client.chat.completions.create(
	model="kimi-k2.5",  
	messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
			  {'role': 'user', 'content': 'If 2x+3y=10, 3x-4y=-2; then what is x and y?'}]
	)
print(completion.model_dump_json())
print("="*50+"response"+"="*50)
print(completion.choices[0].message.content)
