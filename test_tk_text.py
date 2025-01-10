import tkinter as tk

def update_text_areas():
    # 模拟语音转换结果
    speech_to_text_result = "这是从语音转换得到的文本结果。"
    text_area1.delete(1.0, tk.END)  # 清空区域1
    text_area1.insert(tk.END, speech_to_text_result)  # 显示语音转换结果
    
    # 模拟 GPT 返回结果
    gpt_response = "这是 GPT 模型返回的结果。"
    text_area2.delete(1.0, tk.END)  # 清空区域2
    text_area2.insert(tk.END, gpt_response)  # 显示 GPT 返回结果

# 创建主窗口
root = tk.Tk()
root.title("语音转换与GPT结果显示")
root.geometry("400x500")  # 设置窗口大小

# 添加标签指示第一个区域
label1 = tk.Label(root, text="语音转换结果：", font=("Arial", 12))
label1.pack(pady=5)  # 添加标签并设置间距

# 创建第一个文字显示区域（语音转换结果）
text_area1 = tk.Text(root, wrap=tk.WORD, height=10)
text_area1.pack(expand=True, fill=tk.BOTH)  # 扩展并填充

# 添加标签指示第二个区域
label2 = tk.Label(root, text="GPT 返回结果：", font=("Arial", 12))
label2.pack(pady=5)  # 添加标签并设置间距

# 创建第二个文字显示区域（GPT返回结果）
text_area2 = tk.Text(root, wrap=tk.WORD, height=10)
text_area2.pack(expand=True, fill=tk.BOTH)  # 扩展并填充

# 创建更新按钮
update_button = tk.Button(root, text="更新结果", command=update_text_areas)
update_button.pack(pady=10)  # 添加按钮并设置间距

# 运行主循环
root.mainloop()
