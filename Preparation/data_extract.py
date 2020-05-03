from pytube import YouTube
import argparse
from pathlib import Path
import os
import subprocess
import csv


class data_fetch():
    def argument_parser(self):
        parser = argparse.ArgumentParser(description='Process some integers.')
        parser.add_argument('input_csv', nargs='+',
                            help='A CSV file containing links to youtube links of audios to be extracted')
        parser.add_argument('--output-path', default="audio_samples", help='')
        parser.add_argument('--video', default=False, help="download videos to and create a new folder")
        return parser.parse_args()

    def on_complete(self, stream, filehandle):
        print(stream)
        print("done")
        return None

    def parse_csv(self, input_csv):
        with open(input_csv, 'r') as input_file:
            Dict = csv.DictReader(input_file)
            return list(Dict)

    def read_and_download(self):
        video_list = data_fetch.parse_csv(args.input_csv[1])
        download_path = "video_samples" if args.video else args.output_path
        print(download_path)
        print(os.getcwd())
        Path(download_path).mkdir(parents=True, exist_ok=True)
        os.chdir(download_path)
        print(os.getcwd())
        for x in video_list:
            print(x["completed"])
            if x["completed"] == "0":
                youtube_link = x["URL"]
                new_name = x["Rename"] + ".mp4"
                print(youtube_link)
                yt = YouTube(youtube_link, on_complete_callback=data_fetch.on_complete)
                if args.video:
                    video = yt.streams.get_highest_resolution().download()
                    os.rename(video, new_name)
                else:
                    audio = yt.streams.get_audio_only().download()
                    os.rename(audio, new_name)
                    mp4 = "%s.mp4" % audio
                    wav = "%s.wav" % x["Rename"]
                    print(wav)
                    print(new_name)

                    ffmpeg = ('ffmpeg -i %s ' % new_name + wav)

                    subprocess.call(ffmpeg, shell=True)
                    os.remove(new_name)


if __name__ == "__main__":
    data_fetch = data_fetch()
    args = data_fetch.argument_parser()

    data_fetch.read_and_download()