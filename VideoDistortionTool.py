
from wand.image import Image
from wand.display import display
from datetime import datetime
import fnmatch
import os
import time
import ffmpeg

#now = datetime.now()
#dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
"""
dirpathInput = 'entrada'
dirpathOutput = 'saida'
fotos = fnmatch.filter(os.listdir(dirpathInput), '*.jpg')
ts = round(time.time() * 1000)


#print('iniciando...')
#for foto in fotos:
#    with Image(filename=f'./{dirpathInput}/{foto}') as img:
#        width = img.width
#        height = img.height
#        img.liquid_rescale(width - int((width * 0.4)), height - int((height * 0.4)),1)
#       img.sample(width, height)  
#        img.save(filename=f'./{dirpathOutput}/{foto}.jpg')
#        print("Salvo " + foto + ", em: " + "./"+dirpathOutput+"/")

porcentagem = 0

reducaoTamFoto = 0.5 #reduz a qualidade em 50%
multiplyer = 0.01
outputFormat = 'jpg'
for foto in fotos:
    for i in range(50):
        nome = "{:04d}".format(i)
        with Image(filename=f'./{dirpathInput}/{foto}') as img:
            width = img.width
            height = img.height
            #realiza o rescale, com base no valor de porcentagem
            img.liquid_rescale(width - int((width * porcentagem)), height - int((height * porcentagem)),1)
            #aumenta o tamanho da imagem, realizando o resample, é afetado pelo valor de redução de tamanho de foto
            img.sample(width - int(width * reducaoTamFoto), height - int(height * reducaoTamFoto))
            img.save(filename=f'./{dirpathOutput}/' 'image'+ nome + '.' + outputFormat)
            print("Salvo "+ str(i) + "-" + foto + ", em: " + "./"+dirpathOutput+"/")
            porcentagem += multiplyer
            print(str(porcentagem))
tf = round(time.time() * 1000)


print("Demorou " + str(tf - ts) +" ms para processar.")
"""
#carrega o construtor, extrai os frames, multiprocessa
class Distortion:
    def __init__(self, dirpathInput, dirpathOutput):
        self.dirpathInput = dirpathInput
        self.dirpathOutput = dirpathOutput
        if not os.path.exists(f'./{self.dirpathInput}'):
            print('Diretorio não encontrado, criando ' + self.dirpathInput + '...')
            os.makedirs(f'./{self.dirpathInput}')
            
        if not os.path.exists(f'./{self.dirpathOutput}'):
            print('Diretorio não encontrado, criando ' + self.dirpathOutput + '...')
            os.makedirs(f'./{self.dirpathOutput}')

    #corrigir, imagesDirpathInput, imageInputFormat, estruturar corretamente
    def multiprocessing(self, qtdThreads, imagesDirpathInput, imageInputFormat):
        self.qtdThreads = qtdThreads
        self.imagesDirpathInput = imagesDirpathInput
        self.imageInputFormat = imageInputFormat
        self.photos = fnmatch.filter(os.listdir('./'+f'{self.imagesDirpathInput}' + '/'), '*.' + f'{self.imageInputFormat}')
        #dirpath = './output/'
        #fotos = fnmatch.filter(os.listdir(dirpath), '*.jpg')
        print("Carregado " +  str(len(self.photos)) + " fotos!")

    def distort(self, photosToDistort, percentage, multiplyer = 0, outputFormat = 'jpg', sizeReductionPercent = 0.5):
        self.percentage = percentage
        self.multiplyer = multiplyer
        self.sizeReductionPercent = sizeReductionPercent
        self.outputFormat = outputFormat
        #alterar parametro fotos, para ser possível repassar uma lista especifica, para multithread
        self.photosToDistort = photosToDistort

        for self.p in self.photosToDistort:
            with Image(filename= f'./{self.imagesDirpathInput}/{self.p}') as self.img:
                self.width = self.img.width
                self.height = self.img.height
                #realiza o rescale, com base no valor de porcentagem
                self.img.liquid_rescale(self.width - int((self.width * self.percentage)), self.height - int((self.height * self.percentage)),1)
                #aumenta o tamanho da imagem, realizando o resample, é afetado pelo valor de redução de tamanho de foto
                self.img.sample(self.width - int(self.width * self.sizeReductionPercent), self.height - int(self.height * self.sizeReductionPercent))
                self.img.save(filename=f'./{self.dirpathOutput}/'+ self.p)
                print("Salvo "+ self.p +", em: " + "./"+self.dirpathOutput+"/")
                self.percentage += self.multiplyer

    def extractVideoFrames(self, videoName, videoInputFormat, imageOutputFormat = 'jpg', nameFormatter = "%04d", fpsOutput = 25):
        self.nameFormatter = nameFormatter
        self.videoName = videoName
        self.videoInputFormat = videoInputFormat
        self.fpsOutput = fpsOutput
        self.imageOutputFormat = imageOutputFormat

        self.probe = ffmpeg.probe('./' + self.dirpathInput + '/' + self.videoName + '.' + self.videoInputFormat)
        self.video = next((stream for stream in self.probe['streams'] if stream['codec_type'] == 'video'), None)
        self.width = int(self.video['width'])
        self.height = int(self.video['height'])

        print('Extraindo frames do vídeo ' + self.videoName + '.' + self.videoInputFormat + '...')
        try:
            (ffmpeg.input(f'./{self.dirpathInput}/{self.videoName}.{self.videoInputFormat}')
                .filter('fps', fps=self.fpsOutput)
                .output(f"./{self.dirpathOutput}/"+"image-"+f'{self.nameFormatter}.'+f'{self.imageOutputFormat}', 
                    video_bitrate='5000k',
                    s=f"{self.width}x{self.height}",
                    sws_flags='bilinear',
                    start_number=0)
            .run(capture_stdout=True, capture_stderr=True))
        except ffmpeg.Error as e:
            print('stdout:', e.stdout.decode('utf8'))
            print('stderr:', e.stderr.decode('utf8'))
    
        print('Extraido frames para ' + self.dirpathOutput + ' !')

distorcer = Distortion('input', 'output')
#distorcer.extractVideoFrames('teste','mp4')
distorcer.multiprocessing(1,'output', 'jpg')
#distorcer.distort('output', 'jpg', 0.4)