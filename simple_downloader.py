from pytube import YouTube
import argparse


def argument_parser():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('yt_link', metavar='N', nargs='+',
                        help='youtube link')
    return parser.parse_args()


def on_progress(stream, chunk, file_handle,bytes_remaining):
    percent = round((1-bytes_remaining/video.filesize)*100)
    if percent%10 == 0:
        print(percent, '% done...')


if __name__ == "__main__":
    args = argument_parser()
    youtube_link = args.yt_link[1]
    yt = YouTube(youtube_link)
    video = yt.streams.get_highest_resolution().download()
