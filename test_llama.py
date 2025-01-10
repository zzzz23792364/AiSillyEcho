# # 导入必要的库
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationChain
# from langchain_ollama import ChatOllama

# model = ChatOllama(model="llama3.1", temperature=0.7)

# # 初始化内存和对话链
# memory = ConversationBufferMemory()
# conversation = ConversationChain(
#     llm=model,  # 确保model已经定义
#     memory=memory,
#     verbose=True
# )

# # 进行对话
# response = conversation.predict(input="假如你是机器人，主人给你指令，去卧室帮我拿下衣服，请只返回目的地给我。")
# print("AI:", response)

# response = conversation.predict(input="假如你是机器人，主人给你指令，去厨房切下水果，请只返回目的地给我。")
# print("AI:", response)

# response = conversation.predict(input="去厨房切下水果")
# print("AI:", response)


# from langchain_ollama import ChatOllama

# model = ChatOllama(model="llama3.1", temperature=0.7)

# messages = [
#     ("human", "假如你是机器人，主人给你指令，去卧室帮我拿下衣服，请只返回目的地给我"),
# ]

# for chunk in model.stream(messages):
#     print(chunk.content, end='', flush=True)


# import ollama

# stream = ollama.chat(
#     model='llama3.1',
#     messages=[{'role': 'user', 'content': '假如你是机器人，主人给你指令，去卧室帮我拿下衣服，请只返回目的地给我'}],
#     stream=True,
# )

# for chunk in stream:
#   print(chunk['message']['content'], end='', flush=True)


# from langchain_ollama import ChatOllama

# # 初始化模型
# model = ChatOllama(model="llama3.1", temperature=0.7)

# # 提问
# response = model.invoke("假如你是机器人，主人给你指令，去卧室帮我拿下衣服，请只返回目的地给我。")

# # 打印响应
# print("AI:", response)

from langchain_ollama import ChatOllama

# 初始化模型
model = ChatOllama(model="llama3.1", temperature=0.0)

response = model.invoke("如果你是机器人，我说去卧室帮我拿充电器，只告诉我目的地")
print("AI:", response)

response = model.invoke("假如你是机器人，我说去卧室帮我拿下衣服，只告诉我目的地")
print("AI:", response)

response = model.invoke("假如你是机器人，我说去厨房切下水果，只告诉我目的地")
print("AI:", response)

response = model.invoke("假如你是机器人，我说去厨房切下拿衣服12345，只告诉我目的地")
print("AI:", response)
