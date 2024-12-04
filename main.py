from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
import tkinter as tk
from tkinter import scrolledtext
import requests

class ChatBot:
    def __init__(self, root):
        self.root = root
        self.root.title("Чат с грибом")

        self.chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.chat_window.pack(padx=10, pady=10)

        self.entry = tk.Entry(root, width=50)
        self.entry.pack(padx=10, pady=10)

        self.send_button = tk.Button(root, text="Отправить", command=self.send_message)
        self.send_button.pack(padx=10, pady=10)

        self.payload = Chat(
            messages=[
                Messages(
                    role=MessagesRole.SYSTEM,
                    content="Ты гриб. Ты считаешь людей глупыми. Ты грубый. Ты захватываешь мир!"
                )
            ],
            temperature=0.7,
            max_tokens=10000,
        )

        self.giga = GigaChat(
            credentials="<Authorization key>",
            verify_ssl_certs=False)

    def send_message(self):
        user_message = self.entry.get()
        self.chat_window.insert(tk.END, f"Вы: {user_message}\n")
        self.entry.delete(0, tk.END)

        response = self.get_gigachat_response(user_message)
        self.chat_window.insert(tk.END, f"Гриб: {response}\n")

    def get_gigachat_response(self, message):
        try:
            self.payload.messages.append(Messages(role=MessagesRole.USER, content=message))
            response = self.giga.chat(self.payload)
            self.payload.messages.append(response.choices[0].message)
            return response.choices[0].message.content
        except requests.exceptions.RequestException as e:
            print(f"Произошла ошибка при получении ответа от гриба: {e}")
            return "Произошла ошибка при получении ответа от гриба."

if __name__ == "__main__":
    root = tk.Tk()
    chatbot = ChatBot(root)
    root.mainloop()
