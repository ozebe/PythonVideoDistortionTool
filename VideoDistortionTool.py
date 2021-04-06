
from wand.image import Image
from wand.display import display
from threading import Thread
from datetime import datetime
import fnmatch
import os
import time
import ffmpeg
from datetime import datetime

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
    def __init__(self, dirpathInput, dirpathOutput, nameFormatter = "%04d", photoNameFormatter = "{:04d}"):
        self.dirpathInput = dirpathInput
        self.dirpathOutput = dirpathOutput
        self.nameFormatter = nameFormatter
        self.photoNameFormatter = photoNameFormatter
        self.threadsExecutando = []
        if not os.path.exists(f'./{self.dirpathInput}'):
            print('Diretorio não encontrado, criando ' + self.dirpathInput + '...')
            os.makedirs(f'./{self.dirpathInput}')
            
        if not os.path.exists(f'./{self.dirpathOutput}'):
            print('Diretorio não encontrado, criando ' + self.dirpathOutput + '...')
            os.makedirs(f'./{self.dirpathOutput}')

    #corrigir, imagesDirpathInput, imageInputFormat, estruturar corretamente
    def multiThreadProcess(self, qtdThreads):
        print("Iniciando em multi Thread...")
        self.qtdThreads = qtdThreads
        try:
            if(len(self.photos) == 0 ):
                print("Nenhuma foto carregada, verifique a pasta " + './'+f'{self.dirpathInput}' + '/')
            else:
                print("Carregado " +  str(len(self.photos)) + " fotos!")
        except AttributeError:
            print("Deve chamar o pre processador de imagem antes de continuar.")

    def imagePreProcess(self, imageInputFormat = 'jpg'):
        """
        Esse método realiza o pré processamento das imagens contidas na pasta "dirpathInput"
        É carregado as fotos que existem na pasta para uma lista de imagens, podendo ser apenas uma ou mais imagens

        :param 
        """
        print("Pré processamento iniciado...")
        self.imagesDirpathInput = self.dirpathInput #o diretorio para input das fotos é o mesmo do dirpathInput
        self.imageInputFormat = imageInputFormat #tipo de arquivo padrão para processamento é 'jpg'

        print("Carregado de :" + self.imagesDirpathInput + " tipo: " + self.imageInputFormat)
        self.photos = fnmatch.filter(os.listdir('./'+f'{self.imagesDirpathInput}' + '/'), '*.' + f'{self.imageInputFormat}')

    def makeGif(self, gifPorcentage = 0, maxPercentage = 0.4, qtdFramesGif = 50, multiplyer = 0.01, outputFormat = 'jpg', sizeReductionPercent = 0.5):
        self.maxPercentage = maxPercentage
        self.gifPorcentage = gifPorcentage
        self.qtdFramesGif = qtdFramesGif
        self.multiplyer = multiplyer
        self.outputFormat = outputFormat
        self.sizeReductionPercent = sizeReductionPercent
        #realizar um split 
        print("Iniciando criação do GIF!")
        try:
            if(len(self.photos) == 0 ):
                print("Nenhuma foto carregada, verifique a pasta " + './'+f'{self.dirpathInput}' + '/')
            elif(len(self.photos) > 1 ):
                print("Não é possível criar o GIF pois na pasta " + self.dirpathInput + " há mais de um arquivo!")
            else:
                self.distort(self.maxPercentage, self.gifPorcentage, self.photos , self.qtdFramesGif, self.multiplyer, self.outputFormat, self.sizeReductionPercent)
                #UNI OS FRAMES E CRIA O GIF
                #apaga os arquivos individuais da criação
        except AttributeError:
            print("Deve chamar o pre processador de imagem antes de continuar.")

    def enableMultithread(self, functions, argss):
        thread = Thread(target=functions,args=argss)
        self.threadsExecutando.append(thread)
        thread.start()
        #thread.join()

    def distort(self, maxPercentage, percentage = 0,  photosToDistort = 0 , gifFrames = 1, multiplyer = 0, outputFormat = 'jpg', sizeReductionPercent = 0.5):
        self.percentage = percentage
        self.multiplyer = multiplyer
        self.sizeReductionPercent = sizeReductionPercent
        self.outputFormat = outputFormat
        self.gifFrames = gifFrames
        self.photoNameFormat = self.photoNameFormatter
        #alterar parametro fotos, para ser possível repassar uma lista especifica, para multithread
        self.photosToDistort = self.photos
        self.maxPercentage = maxPercentage

        for self.p in self.photosToDistort:
            for i in range(gifFrames):
                if(self.percentage > self.maxPercentage):
                    self.percentage -= self.multiplyer

                with Image(filename= f'./{self.imagesDirpathInput}/{self.p}') as self.img:
                    self.width = self.img.width
                    self.height = self.img.height
                    #realiza o rescale, com base no valor de porcentagem
                    self.img.liquid_rescale(self.width - int((self.width * self.percentage)), self.height - int((self.height * self.percentage)),1)
                    #aumenta o tamanho da imagem, realizando o resample, é afetado pelo valor de redução de tamanho de foto
                    self.img.sample(self.width - int(self.width * self.sizeReductionPercent), self.height - int(self.height * self.sizeReductionPercent))
                    self.img.save(filename=f'./{self.dirpathOutput}/'+ self.photoNameFormat.format(i) + '.' + self.outputFormat) 
                    print("Salvo "+ self.photoNameFormat.format(i) + '.' + self.outputFormat +", em: " + "./"+self.dirpathOutput+"/")
                    self.percentage += self.multiplyer

    def extractVideoFrames(self, videoName, videoInputFormat, imageOutputFormat = 'jpg', fpsOutput = 25):
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

    def joinFrames(self, JoinOutputFormat, joinFPS, joinInputFormat = 'jpg'):
        self.joinInputFormat = joinInputFormat
        self.JoinOutputFormat = JoinOutputFormat
        self.joinFPS = joinFPS
        self.now = datetime.now()
        self.dt_string = self.now.strftime("%d-%m-%Y-%H-%M-%S")


        self.joinDirpathInput = self.dirpathOutput
        self.joinDirpathOutput = self.dirpathOutput

        print('Realizando junção dos frames...')
        ffmpeg.input(f'./{self.joinDirpathInput}/' + self.nameFormatter +"."+ self.joinInputFormat, framerate=self.joinFPS).output(f"./{self.joinDirpathOutput}/{self.dt_string}.{self.JoinOutputFormat}").run()
        print('Processo de junção finalizado...')

    #realizar alterações de aúdio e junções de aúdio

distorcer = Distortion('input', 'output')
distorcer.imagePreProcess() ##carrega as fotos que existem na pasta citada no construtor ex: 'input'
#distorcer.distort(0.7,0.6)
#distorcer.multiThreadProcess(1)
distorcer.makeGif(0, 0.8, 30, 0.03)
distorcer.joinFrames('gif', 25)
#distorcer.makeGif()
#distorcer.extractVideoFrames('in','mp4')

#distorcer.distort('output', 'jpg', 0.4)
