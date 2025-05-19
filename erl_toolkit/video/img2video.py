import ffmpeg
import os
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-folder", type=str, default="images")
    parser.add_argument("--fps", type=int, default=15)
    parser.add_argument("--video-path", type=str, default="video.mp4")
    args = parser.parse_args()
    video_path = os.path.realpath(args.video_path)
    os.chdir(args.image_folder)
    ffmpeg.input("*.png", pattern_type="glob").output(
        video_path, vcodec="libx264", framerate=args.fps, pix_fmt="yuv420p"
    ).run()


if __name__ == "__main__":
    main()
