import tkinter as tk
import threading
import numpy as np
import wave
import socket
from functools import partial
from funasr import AutoModel
from langchain_ollama import ChatOllama

def start_recording_thread(videoTrans):
    threading.Thread(target=videoTrans.start_recording).start()

def stop_recording_thread(videoTrans):
    threading.Thread(target=videoTrans.stop_recording).start()

def start_transcription_thread(videoTrans):
    threading.Thread(target=videoTrans.start_transcription).start()

class VideoTrans():
    def __init__(self, tk_root):
        self.is_recording = False
        # 设置UDP接收参数
        self.UDP_IP = "127.0.0.1"
        self.UDP_PORT = 1234
        self.OUTPUT_FILE = "output_audio.wav"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        print(f"Listening on {self.UDP_IP}:{self.UDP_PORT}...")
        # 设置WAV文件参数
        self.CHANNELS = 2 # 立体声
        self.RATE = 44100 # 采样率
        self.SAMPLE_WIDTH = 2 # 16位PCM
        self.model = AutoModel(model="paraformer-zh", disable_update=True)
        self.llama3_model = ChatOllama(model="llama3.1", temperature=0.0)
        self.creat_tk_element(tk_root)

    def creat_tk_element(self, tk_root):
        # 创建按钮
        btn_start = tk.Button(tk_root, text="Start Record", command=partial(start_recording_thread, self))
        btn_start.pack(pady=10)

        btn_stop = tk.Button(tk_root, text="Stop Record", command=partial(stop_recording_thread, self))
        btn_stop.pack(pady=10)

        btn_transcribe = tk.Button(tk_root, text="Start Translate", command=partial(start_transcription_thread, self))
        btn_transcribe.pack(pady=10)

        self.label1 = tk.Label(tk_root, text="Voice TransResult:")
        self.label1.pack(pady=5)  # 添加标签并设置间距

        # 创建第一个文字显示区域（语音转换结果）
        self.text_area1 = tk.Text(tk_root, wrap=tk.WORD, height=10, font=("song ti", 20))
        self.text_area1.pack(expand=True, fill=tk.BOTH)  # 扩展并填充

        # 添加标签指示第二个区域
        self.label2 = tk.Label(tk_root, text="GPT TransResult:")
        self.label2.pack(pady=5)  # 添加标签并设置间距

        # 创建第二个文字显示区域（GPT返回结果）
        self.text_area2 = tk.Text(tk_root, wrap=tk.WORD, height=10, font=("song ti", 20))
        self.text_area2.pack(expand=True, fill=tk.BOTH)  # 扩展并填充

    def start_recording(self):
        print("开始录音...")
        self.is_recording = True
        with wave.open(self.OUTPUT_FILE, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.SAMPLE_WIDTH)  # 16位PCM
            wf.setframerate(self.RATE)
            while self.is_recording:
                # 接收数据
                data, addr = self.sock.recvfrom(2048)  # 每次接收1024字节的数据
                wf.writeframes(data)  # 写入WAV文件
            print(f"Audio saved to {self.OUTPUT_FILE}")

    def stop_recording(self):
        print("停止录音...")
        self.is_recording = False
        
    def start_transcription(self):
        print("开始转译...")
        res = self.model.generate(input=self.OUTPUT_FILE)
        print("res:", res)
        print("res1:", res[0]['text'])

        self.text_area1.delete(1.0, tk.END)  # 清空区域1
        self.text_area1.insert(tk.END, res[0]['text'])  # 显示语音转换结果

        inv_str = "如果你是机器人，我说" + str(res[0]['text']) + ",只告诉我目的地"
        print("inv_str:", inv_str)
        response = self.llama3_model.invoke(inv_str)
        # response = model.invoke("如果你是机器人，我说去卧室帮我拿充电器，只告诉我目的地")
        print("AI:", response)
        print("AI res:", response.content)

        self.text_area2.delete(1.0, tk.END)  # 清空区域1
        self.text_area2.insert(tk.END, response.content)  # 显示语音转换结果


if __name__ == '__main__':
    # 创建主窗口
    root = tk.Tk()
    root.title("SillyEcho")
    root.geometry("400x600")  # 设置窗口大小

    videoTrans = VideoTrans(root)

    # 启动主循环
    root.mainloop()

# .\ffmpeg.exe  -list_devices true -f dshow -i dummy
# .\ffmpeg.exe -f dshow -i audio="麦克风 (WEB CAM)" -f wav udp://127.0.0.1:1234