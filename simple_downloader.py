from pytube import YouTube
import argparse
from pathlib import Path
import os

def argument_parser():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('yt_link', metavar='yt_link', nargs='+',
                        help='youtube link')
    parser.add_argument('--output_path',default="../Downloads" ,help='')
    return parser.parse_args()

def on_complete(stream, filehandle):
    print("done")
    return None

if __name__ == "__main__":
    args = argument_parser()
    youtube_link = args.yt_link[1]
    download_path = args.output_path
    os.chdir(download_path)
    print(download_path)
    yt = YouTube(youtube_link,on_complete_callback=on_complete)

    video = yt.streams.get_highest_resolution().download(download_path)
    os.rename(video,"high.mp4")
    audio = yt.streams.get_audio_only().download(download_path)
    os.rename(audio, "audio.mp4")
    captions = yt.captions.get_by_language_code('en')
    text_file = open("Output.txt", "w")
    text_file.write(captions.generate_srt_captions())
    text_file.close()