import base64
import bz2
import sys
import re
import os
import time
from colorama import Fore, Style, init
from threading import Thread
from queue import Queue

# Inisialisasi colorama
init(autoreset=True)

# Animasi spinner
def spinner(message):
    chars = "⣾⣽⣻⢿⡿⣟⣯⣷"
    while not done:
        for char in chars:
            sys.stdout.write(f"\r{Fore.YELLOW}⏳ {message} {char} {Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write("\r" + " " * 60 + "\r")

# Dekorator untuk animasi
def animate(message):
    def decorator(func):
        def wrapper(*args, **kwargs):
            global done
            done = False
            t = Thread(target=spinner, args=(message,))
            t.start()
            result = func(*args, **kwargs)
            done = True
            t.join()
            return result
        return wrapper
    return decorator

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    clear_screen()
    print(f"""{Fore.CYAN}
    ██████╗ ███████╗ ██████╗██████╗ ██╗████████╗
    ██╔══██╗██╔════╝██╔════╝██╔══██╗██║╚══██╔══╝
    ██║  ██║█████╗  ██║     ██████╔╝██║   ██║   
    ██║  ██║██╔══╝  ██║     ██╔══██╗██║   ██║   
    ██████╔╝███████╗╚██████╗██║  ██║██║   ██║   
    ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝   ╚═╝   
    {Style.RESET_ALL}
    {Fore.MAGENTA}• Created by Yinn •{Style.RESET_ALL}
    {Fore.YELLOW}• Multi-Decryption Tool •{Style.RESET_ALL}
    """)

def show_menu():
    print(f"\n{Fore.GREEN}⋆⋆⋆ Main Menu ⋆⋆⋆{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[1]{Style.RESET_ALL} Base64 Operations")
    print(f"{Fore.CYAN}[2]{Style.RESET_ALL} BZip2 Operations")
    print(f"{Fore.CYAN}[3]{Style.RESET_ALL} BashArmor Operations")
    print(f"{Fore.CYAN}[4]{Style.RESET_ALL} SHC Operations")
    print(f"{Fore.CYAN}[5]{Style.RESET_ALL} Exit")
    return input(f"\n{Fore.YELLOW}⎋ Select option [1-5]: {Style.RESET_ALL}")

def base64_menu():
    clear_screen()
    print(f"{Fore.GREEN}⋆⋆⋆ Base64 Operations ⋆⋆⋆{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[1]{Style.RESET_ALL} Decode Base64 File")
    print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Encode to Base64")
    print(f"{Fore.CYAN}[3]{Style.RESET_ALL} Back to Main Menu")
    return input(f"\n{Fore.YELLOW}⎋ Select option [1-3]: {Style.RESET_ALL}")

def bzip2_menu():
    clear_screen()
    print(f"{Fore.GREEN}⋆⋆⋆ BZip2 Operations ⋆⋆⋆{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[1]{Style.RESET_ALL} Decompress File")
    print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Compress File")
    print(f"{Fore.CYAN}[3]{Style.RESET_ALL} Back to Main Menu")
    return input(f"\n{Fore.YELLOW}⎋ Select option [1-3]: {Style.RESET_ALL}")

def basharmor_menu():
    clear_screen()
    print(f"{Fore.GREEN}⋆⋆⋆ BashArmor Operations ⋆⋆⋆{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[1]{Style.RESET_ALL} Decrypt File")
    print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Encrypt File")
    print(f"{Fore.CYAN}[3]{Style.RESET_ALL} Back to Main Menu")
    return input(f"\n{Fore.YELLOW}⎋ Select option [1-3]: {Style.RESET_ALL}")

def shc_menu():
    clear_screen()
    print(f"{Fore.GREEN}⋆⋆⋆ SHC Operations ⋆⋆⋆{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[1]{Style.RESET_ALL} Decrypt SHC File")
    print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Generate SHC File")
    print(f"{Fore.CYAN}[3]{Style.RESET_ALL} Back to Main Menu")
    return input(f"\n{Fore.YELLOW}⎋ Select option [1-3]: {Style.RESET_ALL}")

# Fungsi-fungsi dekripsi
def decode_base64(data):
    try:
        return base64.b64decode(data)
    except Exception as e:
        print(f"{Fore.RED}Base64 Error: {e}{Style.RESET_ALL}")
        return None

def encode_base64(data):
    return base64.b64encode(data)

def decompress_bzip2(data):
    try:
        return bz2.decompress(data)
    except Exception as e:
        print(f"{Fore.RED}BZip2 Error: {e}{Style.RESET_ALL}")
        return None

def compress_bzip2(data):
    return bz2.compress(data)

def decrypt_basharmor(data):
    try:
        decoded = base64.b64decode(data)
        return bz2.decompress(decoded)
    except Exception as e:
        print(f"{Fore.RED}BashArmor Error: {e}{Style.RESET_ALL}")
        return None

def encrypt_basharmor(data):
    compressed = bz2.compress(data)
    return base64.b64encode(compressed)

def decrypt_shc(data):
    try:
        pattern = re.compile(b'\x21\x21\x21\x21\x00\x00\x00\x00(.)')
        match = pattern.search(data)
        if not match:
            return None
        xor_key = match.group(1)[0]
        payload_start = match.end()
        payload_end = data.find(b'\x21\x21\x21\x21\x00\x00\x00\x00', payload_start)
        encrypted = data[payload_start:payload_end]
        return bytes([b ^ xor_key for b in encrypted])
    except Exception as e:
        print(f"{Fore.RED}SHC Error: {e}{Style.RESET_ALL}")
        return None

@animate("Processing file...")
def process_file(filename, func):
    try:
        with open(filename, 'rb') as f:
            data = f.read()
        return func(data)
    except Exception as e:
        print(f"{Fore.RED}✖ Error: {e}{Style.RESET_ALL}")
        return None

def main():
    global done
    while True:
        show_banner()
        main_choice = show_menu()
        
        if main_choice == '5':
            print(f"\n{Fore.GREEN}✌ Thank you! Goodbye!{Style.RESET_ALL}")
            break
            
        # Base64 Operations
        if main_choice == '1':
            while True:
                choice = base64_menu()
                if choice == '3':
                    break
                
                filename = input(f"\n{Fore.BLUE}⌲ Enter filename: {Style.RESET_ALL}")
                
                if choice == '1':
                    result = process_file(filename, decode_base64)
                elif choice == '2':
                    result = process_file(filename, encode_base64)
                else:
                    continue
                
                # [Bagian tampilan hasil sama seperti sebelumnya]
        
        # [Implementasi menu serupa untuk BZip2, BashArmor, dan SHC]
        
if __name__ == '__main__':
    done = False
    main()