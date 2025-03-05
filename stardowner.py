#!/usr/bin/env python3
# hell nah

import os
import sys
import time
import argparse
from urllib.error import URLError
import re
from colorama import Fore, Back, Style, init
import pytube
from pytube.exceptions import RegexMatchError, VideoUnavailable


init()


class Colors:
    HEADER = Fore.CYAN
    TITLE = Fore.MAGENTA + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    WARNING = Fore.YELLOW
    ERROR = Fore.RED + Style.BRIGHT
    RESET = Style.RESET_ALL
    BLUE = Fore.BLUE
    CYAN = Fore.CYAN

def clear_screen():
    os.system('clear')

def print_banner():
    banner = f"""
{Colors.TITLE}
╔═╗╔╦╗╔═╗╦═╗╔╦╗  ╔╦╗╔═╗╦ ╦╔╗╔╦  ╔═╗╔═╗╔╦╗╔═╗╦═╗
╚═╗ ║ ╠═╣╠╦╝ ║    ║║║ ║║║║║║║║  ║ ║╠═╣ ║║║╣ ╠╦╝
╚═╝ ╩ ╩ ╩╩╚═ ╩   ═╩╝╚═╝╚╩╝╝╚╝╩═╝╚═╝╩ ╩═╩╝╚═╝╩╚═ v0.1 
{Colors.RESET}{Colors.HEADER}
              Created By: Rip70022
              GitHub: https://www.github.com/Rip70022
{Colors.RESET}
"""
    print(banner)

def loading_animation(text):
    animation = [
        "[⣾]", "[⣽]", "[⣻]", "[⢿]", "[⡿]", "[⣟]", "[⣯]", "[⣷]"
    ]
    
    for i in range(10):
        for frame in animation:
            sys.stdout.write(f"\r{Colors.CYAN}{text} {frame}{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(0.1)
    print()

def get_video_info(url):
    try:
        yt = pytube.YouTube(url)
        return yt
    except RegexMatchError:
        raise ValueError(f"{Colors.ERROR}Invalid URL. Make sure it's a correct YouTube URL.{Colors.RESET}")
    except VideoUnavailable:
        raise ValueError(f"{Colors.ERROR}This video is unavailable.{Colors.RESET}")
    except URLError:
        raise ConnectionError(f"{Colors.ERROR}Connection error. Check your internet connection.{Colors.RESET}")
    except Exception as e:
        raise Exception(f"{Colors.ERROR}Unknown error: {str(e)}{Colors.RESET}")

def sanitize_filename(filename):
    
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_video(url, custom_filename=None, download_path="./"):
    try:
        print(f"{Colors.HEADER}Getting video information...{Colors.RESET}")
        loading_animation("Processing")
        
        yt = get_video_info(url)
        
        print(f"\n{Colors.HEADER}Original title: {Colors.RESET}{yt.title}")
        print(f"{Colors.HEADER}Author: {Colors.RESET}{yt.author}")
        print(f"{Colors.HEADER}Duration: {Colors.RESET}{yt.length} seconds")
        
        
        if not custom_filename:
            custom_filename = input(f"\n{Colors.BLUE}Enter a name for the file (leave blank to use original title): {Colors.RESET}")
        
        
        if not custom_filename.strip():
            custom_filename = yt.title
        
        
        custom_filename = sanitize_filename(custom_filename)
        
        print(f"\n{Colors.HEADER}Selecting the best available quality...{Colors.RESET}")
        loading_animation("Analyzing formats")
        
        stream = yt.streams.get_highest_resolution()
        
        
        if not custom_filename.lower().endswith('.mp4'):
            custom_filename += '.mp4'
        
        
        file_path = os.path.join(download_path, custom_filename)
        
        print(f"\n{Colors.HEADER}Downloading video as: {Colors.RESET}{custom_filename}")
        loading_animation("Downloading")
        
       
        stream.download(output_path=download_path, filename=custom_filename)
        
        print(f"\n{Colors.SUCCESS}✓ Download completed successfully!{Colors.RESET}")
        print(f"{Colors.HEADER}File location: {Colors.RESET}{file_path}")
        
        return True
    
    except ValueError as e:
        print(f"\n{e}")
    except ConnectionError as e:
        print(f"\n{e}")
    except Exception as e:
        print(f"\n{Colors.ERROR}An unexpected error occurred: {str(e)}{Colors.RESET}")
    
    return False

def main():
    parser = argparse.ArgumentParser(description='Download YouTube videos')
    parser.add_argument('-u', '--url', help='YouTube video URL')
    parser.add_argument('-n', '--name', help='Custom filename for the video')
    parser.add_argument('-p', '--path', help='Destination path to save the file', default='./')
    
    args = parser.parse_args()
    
    clear_screen()
    print_banner()
    
    while True:
        try:
            
            if not args.url:
                url = input(f"\n{Colors.BLUE}Enter the YouTube video URL (or 'exit' to quit): {Colors.RESET}")
                if url.lower() in ['exit', 'quit', 'q']:
                    print(f"\n{Colors.SUCCESS}FOLLOW ME ON GITHUB FOR MORE TOOLS: https://www.github.com/Rip70022 {Colors.RESET}")
                    sys.exit(0)
            else:
                url = args.url
            
            
            result = download_video(url, args.name, args.path)
            
            
            if args.url:
                break
            
            
            choice = input(f"\n{Colors.BLUE}Do you want to download another video? (y/n): {Colors.RESET}")
            if choice.lower() not in ['y', 'yes']:
                print(f"\n{Colors.SUCCESS}FOLLOW ME ON GITHUB FOR MORE TOOLS: https://www.github.com/Rip70022 {Colors.RESET}")
                break
            
            clear_screen()
            print_banner()
            
           
            args.url = None
            args.name = None
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.WARNING}Operation canceled by user.{Colors.RESET}")
            print(f"{Colors.SUCCESS}FOLLOW ME ON GITHUB FOR MORE TOOLS: https://www.github.com/Rip70022 {Colors.RESET}")
            sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n{Colors.ERROR}Critical error: {str(e)}{Colors.RESET}")
        sys.exit(1)
