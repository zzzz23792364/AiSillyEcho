import tkinter as tk
import threading
import numpy as np
import wave
import socket
from functools import partial
from funasr import AutoModel


class VideoTrans():
    def __init__(self):
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
        print(res)


def start_recording_thread(videoTrans):
    threading.Thread(target=videoTrans.start_recording).start()

def stop_recording_thread(videoTrans):
    threading.Thread(target=videoTrans.stop_recording).start()

def start_transcription_thread(videoTrans):
    threading.Thread(target=videoTrans.start_transcription).start()

if __name__ == '__main__':
    # 创建主窗口
    root = tk.Tk()
    root.title("SillyEcho")
    root.geometry("400x300")  # 设置窗口大小

    videoTrans = VideoTrans()

    # 创建按钮
    btn_start = tk.Button(root, text="Start Record", command=partial(start_recording_thread, videoTrans))
    btn_start.pack(pady=10)

    btn_stop = tk.Button(root, text="Stop Record", command=partial(stop_recording_thread, videoTrans))
    btn_stop.pack(pady=10)

    btn_transcribe = tk.Button(root, text="Start Translate", command=partial(start_transcription_thread, videoTrans))
    btn_transcribe.pack(pady=10)

    # 启动主循环
    root.mainloop()

# .\ffmpeg.exe  -list_devices true -f dshow -i dummy
# .\ffmpeg.exe -f dshow -i audio="麦克风 (WEB CAM)" -f wav udp://127.0.0.1:1234