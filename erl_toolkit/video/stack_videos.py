import os
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--videos", type=str, nargs="+")
    parser.add_argument("--orientation", type=str, default="vertical", choices=["horizontal", "vertical"])
    parser.add_argument("--output-video-path", type=str, default="stacked.mp4")

    args = parser.parse_args()
    if len(args.videos) == 0:
        raise ValueError("No videos provided")
    if len(args.videos) == 1:
        raise ValueError("Only one video provided")
    video_path = os.path.realpath(args.output_video_path)
    cmd = f"ffmpeg -i {args.videos[0]}"
    filter_complex = "[0:v]"
    for i in range(1, len(args.videos)):
        cmd += f" -i {args.videos[i]}"
        filter_complex += f"[{i}:v]"
    if args.orientation == "horizontal":
        filter_complex += f"hstack={len(args.videos)}[v]"
    else:
        filter_complex += f"vstack={len(args.videos)}[v]"
    cmd += f" -filter_complex {filter_complex} -map [v] {video_path}"
    print(cmd)
    os.system(cmd)


if __name__ == "__main__":
    main()
