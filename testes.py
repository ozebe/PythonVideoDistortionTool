import ffmpeg
from datetime import datetime


def main():
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
    
    nomeArqivo = './input/meu-filho-quer-bolacha'
    extensaoArq = '.mp4'
    nomeVideo = nomeArqivo + extensaoArq
    
    video = ffmpeg.input(nomeVideo)

    #isola o aúdio e aplica o efeito vibrato
    audio = video.audio.filter("vibrato", 12)
    audio2 = video.audio.filter("tremolo",5, 0.7)
    #audio2 = video.audio.filter("chorus", 0.4, 0.4, 100, 16, 2.5, 40)
    #video.audio.filter("tremolo",15)
    
    ffmpeg.concat(video, audio2, audio, v=1, a=2).output(f"./output/pronto{dt_string}.mp4").run()


if __name__ == "__main__":
    main()