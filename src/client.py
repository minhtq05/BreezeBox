import socket
import threading

from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, Container
from textual.widgets import Header, Footer, Input, Label, Button

HOST = '127.0.0.1'
PORT = 5000


class ChatClient(App):
    def __init__(self, host, port):
        super().__init__()
        self._host = host
        self._port = port

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self._host, self._port))

    BINDINGS = [
        ('q', 'quit', 'Quit'),
        ('d', 'toggle_dark', 'Toogle Dark Mode'),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ScrollableContainer(id='messages')
        yield Input(id='message_box', placeholder='Enter your message')

    def on_input_submitted(self, event: Input.Submitted) -> None:
        content = self.query_one('#message_box', Input).value
        new_message = Label(content)
        self.query_one('#messages').mount(new_message)
        new_message.scroll_visible()

        self.client_socket.sendall(content.encode('utf-8'))
        data = self.client_socket.recv(1024)
        response = data.decode('utf-8')
        self.query_one('#messages').mount(Label(response))

        self.query_one('#message_box', Input).value = ''

    def action_quit(self) -> None:
        print('App quitted!')
        self.exit()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark


def main():
    # Initiate client GUI and connect user to the main server
    client_app = ChatClient(HOST, PORT)
    client_app.run()

    # host = '127.0.0.1'
    # port = 5000

    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client_socket.connect((host, port))

    # while True:
    #     message = input('> ')
    #     client_socket.sendall(message.encode('utf-8'))
    #     data = client_socket.recv(1024)
    #     response = data.decode('utf-8')
    #     print(f'Server response: {response}')


if __name__ == '__main__':
    main()
