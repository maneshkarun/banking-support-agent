from langchain_openai import ChatOpenAI


llm = ChatOpenAI(model="models/gemma-4-12b-it-Q8_0.gguf",
                 base_url="http://localhost:8080/v1",
                 api_key="slklvkjksdkdv")

response = llm.invoke("Hello, Which model are you?")
print(response.content)

