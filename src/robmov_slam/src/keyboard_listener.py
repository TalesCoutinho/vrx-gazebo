#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Empty
import sys
import select
import termios
import tty

class KeyboardListener(Node):
    def __init__(self):
        super().__init__('keyboard_listener')
        self.publisher = self.create_publisher(Empty, '/system/shutdown', 10)
        self.get_logger().info("Pressione 'F' para finalizar a missão e gerar o mapa batimétrico...")

    def run(self):
        try:
            # Configura o terminal para leitura de um caractere sem precisar de Enter
            old_settings = termios.tcgetattr(sys.stdin)
            try:
                tty.setcbreak(sys.stdin.fileno())
                while rclpy.ok():
                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        key = sys.stdin.read(1)
                        if key.lower() == 'f':
                            self.get_logger().info("Tecla 'F' pressionada. Encerrando sistema...")
                            msg = Empty()
                            self.publisher.publish(msg)
                            break
                        elif key == '\x03': # Ctrl+C
                            break
            finally:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        except Exception as e:
            # Fallback se o terminal não suportar termios (ex: aba do vscode)
            self.get_logger().warn(f"Modo interativo falhou ({e}). Usando modo fallback. Pressione 'F' e depois Enter.")
            while rclpy.ok():
                try:
                    user_input = input()
                    if user_input.lower().strip() == 'f':
                        self.get_logger().info("Tecla 'F' pressionada. Encerrando sistema...")
                        msg = Empty()
                        self.publisher.publish(msg)
                        break
                except EOFError:
                    break

def main(args=None):
    rclpy.init(args=args)
    node = KeyboardListener()
    
    # Rodamos o loop do teclado no thread principal
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
