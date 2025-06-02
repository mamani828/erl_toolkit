import ffmpeg
import os
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-folder", type=str, default="images")
    parser.add_argument("--fps", type=int, default=15)
    parser.add_argument("--video-path", type=str, default="video.mp4")
    parser.add_argument("--img-ext", type=str, default="png")
    args = parser.parse_args()
    video_path = os.path.realpath(args.video_path)
    cmd = f'ffmpeg -framerate {args.fps} -pattern_type glob -i "*.{args.img_ext}" -vcodec libx264 '
    cmd += f'-pix_fmt yuv420p -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" '
    cmd += f"{video_path}"
    print(cmd)
    os.chdir(args.image_folder)
    os.system(cmd)
    # ffmpeg.input(f"*.{args.img_ext}", pattern_type="glob").output(
    #     video_path, vcodec="libx264", framerate=args.fps, pix_fmt="yuv420p"
    # ).run()


if __name__ == "__main__":
    main()
