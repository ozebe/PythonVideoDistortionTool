
from wand.image import Image
from wand.display import display
from threading import Thread
from datetime import datetime
import fnmatch
import os
import time
import ffmpeg
from datetime import datetime
import math

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
    def multiThreadProcess(self, qtdThreads, imagesDirpathInputThread = '', imageInputFormatThread = 'jpg'):

        print("Iniciando em multi Thread...")
        self.qtdThreads = qtdThreads
        self.imagesDirpathInputThread = imagesDirpathInputThread
        self.imageInputFormatThread = imageInputFormatThread

        if(self.imagesDirpathInputThread == ''):
            self.imagesDirpathInputThread = self.dirpathInput

        self.photos = fnmatch.filter(os.listdir('./'+f'{self.imagesDirpathInputThread}' + '/'), '*.' + f'{self.imageInputFormatThread}')

        if(len(self.photos) == 0 ):
            print("Nenhuma foto carregada, verifique a pasta " + './'+f'{self.imagesDirpathInputThread}' + '/')
        else:
            print("Carregado " +  str(len(self.photos)) + " fotos!")

    def imagePreProcess(self, imagesDirpathInput = '', imageInputFormat = 'jpg'):
        """
        Esse método realiza o pré processamento das imagens contidas na pasta "dirpathInput"
        É carregado as fotos que existem na pasta para uma lista de imagens, podendo ser apenas uma ou mais imagens

        :param imagesDirpathInput -- local de onde a/as fotos serão carregadas, caso seja deixado em branco, irá pegar o parâmetro de entrada carregado no construtor
        é necessário defini-lo, caso esteja carregando as imagens extraídas de um vídeo processado.
        :param imageInputFormat -- formato da imagem, ex: jpg
        """
        self.imagesDirpathInput = imagesDirpathInput
        self.imageInputFormat = imageInputFormat
        print("Pré processamento iniciado...")
        if(self.imagesDirpathInput == ''):
            self.imagesDirpathInput = self.dirpathInput #o diretorio para input das fotos é o mesmo do dirpathInput
            print("Diretório de processamento não específicado, utilizando " + './'+f'{self.dirpathInput}' + '/')
         #tipo de arquivo padrão para processamento é 'jpg'

        
        self.photos = fnmatch.filter(os.listdir('./'+f'{self.imagesDirpathInput}' + '/'), '*.' + f'{self.imageInputFormat}')

        print("Carregado " + str(len(self.photos)) + " frames, de :" + self.imagesDirpathInput + " tipo: " + self.imageInputFormat)

    def makeGif(self, maxPercentage = 0.4, gifWidthmultiplyer = 0.01, gifHeightmultiplyer = 0.01, gifWidthPorcentage = 0, gifHeightPorcentage = 0,  qtdFramesGif = 50, outputFormat = 'jpg', sizeReductionPercent = 0.5):
        """
        Realiza a criação de um gif, após chamar o pre processador de imagem, é possível realizar a criação do gif, nenhum parâmetro é de preenchimento obrigatório
        É relizado a criação de vários frames, sendo modificado pouco a pouco a distorção, a quantia padrão de frames criados é 50.

        :param gifWidthPorcentage -- Porcentagem de distorção da largura da imagem original, inicial, valor padrão é 0.
        :param gifHeightPorcentage -- Porcentagem de distorção da altura da imagem original inicial, valor padrão é 0.
        :param maxPercentage -- Porcentagem máxima de distorção, sendo 1, 100%, o valor padrão é 0.4 o que equivale a uma distorção máxima de 40% da foto original.
        :param qtdFramesGif -- Quantia de frames que serão criadas a partir da foto carregada, o valor padrão é de 50 frames.
        :param gifWidthmultiplyer -- Multiplicador de distorção da largura dos frames, o valor de distorção inicial da largura é acrescido com esse parâmetro a cada iteração, o 
        valor padrão é de 0.01 de distorção por frame, o que equivale a 1%.
        :param gifHeightmultiplyer -- Multiplicador de distorção da altura dos frames, o valor de distorção inicial da altura é acrescido com esse parâmetro a cada iteração, o 
        valor padrão é de 0.01 de distorção por frame, o que equivale a 1%.
        :param outputFormat -- Formato de saída dos frames, o valor padrão de saída é 'jpg'.
        :param sizeReductionPercent -- é a quantia de redução no tamanho original da foto carregada, o valor padrão é 0.5 o que equivale a uma diminuiçao de 50% na largura
        e altura da foto original.
        """
        self.maxPercentage = maxPercentage
        self.gifWidthPorcentage = gifWidthPorcentage
        self.gifHeightPorcentage = gifHeightPorcentage
        self.qtdFramesGif = qtdFramesGif
        self.gifWidthmultiplyer = gifWidthmultiplyer
        self.gifHeightmultiplyer = gifHeightmultiplyer
        self.gifHeightPorcentage = gifHeightPorcentage
        self.outputFormat = outputFormat
        self.sizeReductionPercent = sizeReductionPercent
        #realizar um split 
        print("Iniciando criação do GIF!")
        try:
            if(len(self.photos) == 0 ):
                print("Nenhuma foto carregada, verifique a pasta " + './'+f'{self.dirpathInput}' + '/')
                exit()
            elif(len(self.photos) > 1 ):
                print("Não é possível criar o GIF pois na pasta " + self.dirpathInput + " há mais de um arquivo!")
                exit()
            else:
                self.distort(self.maxPercentage, self.gifWidthmultiplyer, self.gifHeightmultiplyer, self.gifWidthPorcentage, self.gifHeightPorcentage, self.photos , self.qtdFramesGif, self.outputFormat, self.sizeReductionPercent)
                #UNI OS FRAMES E CRIA O GIF
                #apaga os arquivos individuais da criação
        except AttributeError:
            print("Deve chamar o pre processador de imagem antes de continuar.")
            exit()

    def enableMultithread(self, functions, argss):
        thread = Thread(target=functions,args=argss)
        self.threadsExecutando.append(thread)
        thread.start()
        #thread.join()

    def distort(self, maxPercentage, widthMultiplyer = 0, heightMultiplyer = 0, widthPercentage = 0,  heightPercentage = 0, photosToDistort = 0 , gifFrames = 1, outputFormat = 'jpg', sizeReductionPercent = 0.5):
        self.widthPercentage = widthPercentage
        self.heightPercentage = heightPercentage
        self.widthMultiplyer = widthMultiplyer
        self.heightMultiplyer = heightMultiplyer
        self.sizeReductionPercent = sizeReductionPercent
        self.outputFormat = outputFormat
        self.gifFrames = gifFrames
        self.photoNameFormat = self.photoNameFormatter
        if(photosToDistort == 0): #caso não tenha sido repassado o parametro de fotos, ele carrega as fotos pré carregas com o pré processador
            self.photosToDistort = self.photos
        else:
            self.photosToDistort = photosToDistort
        self.maxPercentage = maxPercentage

        if(self.gifFrames <= 1):
            i = 0
            for self.p in self.photosToDistort:
            #corrigir, quando coloca mais de uma imagem na pasta ele da problema, substitui a imagem
                    if(self.widthPercentage > self.maxPercentage):
                        self.widthPercentage -= self.widthMultiplyer
                
                    if(self.heightPercentage > self.maxPercentage):
                        self.heightPercentage -= self.heightMultiplyer

                    with Image(filename= f'./{self.imagesDirpathInput}/{self.p}') as self.img:
                        self.width = self.img.width
                        self.height = self.img.height
                        #realiza o rescale, com base no valor de porcentagem
                        self.img.liquid_rescale(self.width - int((self.width * self.widthPercentage)), self.height - int((self.height * self.heightPercentage)),1,1)
                        #aumenta o tamanho da imagem, realizando o resample, é afetado pelo valor de redução de tamanho de foto
                        self.img.sample(self.width - int(self.width * self.sizeReductionPercent), self.height - int(self.height * self.sizeReductionPercent))
                        self.img.save(filename=f'./{self.dirpathOutput}/'+ self.photoNameFormat.format(i) + '.' + self.outputFormat) 
                        print("Salvo "+ self.photoNameFormat.format(i) + '.' + self.outputFormat +", em: " + "./"+self.dirpathOutput+"/")
                        self.widthPercentage += self.widthMultiplyer
                        self.heightPercentage += self.heightMultiplyer
                    i += 1
        else:
            for self.p in self.photosToDistort:
                #corrigir, quando coloca mais de uma imagem na pasta ele da problema, substitui a imagem
                for i in range(self.gifFrames):
                    if(self.widthPercentage > self.maxPercentage):
                        self.widthPercentage -= self.widthMultiplyer
                
                    if(self.heightPercentage > self.maxPercentage):
                        self.heightPercentage -= self.heightMultiplyer

                    with Image(filename= f'./{self.imagesDirpathInput}/{self.p}') as self.img:
                        self.width = self.img.width
                        self.height = self.img.height
                        #realiza o rescale, com base no valor de porcentagem
                        self.img.liquid_rescale(self.width - int((self.width * self.widthPercentage)), self.height - int((self.height * self.heightPercentage)),1,1)
                        #aumenta o tamanho da imagem, realizando o resample, é afetado pelo valor de redução de tamanho de foto
                        self.img.sample(self.width - int(self.width * self.sizeReductionPercent), self.height - int(self.height * self.sizeReductionPercent))
                        self.img.save(filename=f'./{self.dirpathOutput}/'+ self.photoNameFormat.format(i) + '.' + self.outputFormat) 
                        print("Salvo "+ self.photoNameFormat.format(i) + '.' + self.outputFormat +", em: " + "./"+self.dirpathOutput+"/")
                        self.widthPercentage += self.widthMultiplyer
                        self.heightPercentage += self.heightMultiplyer

    def extractVideoFrames(self, videoName, videoInputFormat, imageOutputFormat = 'jpg', fpsOutput = 25):
        """
        Realiza a extração dos frames do vídeo que se encontra na pasta de entrada

        :param videoName -- nome do video, ex: teste
        :param videoInputFormat -- formato do vídeo a ser processado, ex: mp4
        :param imageOutputFormat -- formato de saída dos frames processados, ex: jpg, não é de preenchimento obrigatório.
        :param fpsOutput -- quantia de FPS que irá se basear para retirar os frames, padrão é 25fps.
        """
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
        #adicionar pasta de onde serão carregados os arquivos para melhorar o fluxo, além de existir possibilidade de imbutir o aúdio.
        self.joinInputFormat = joinInputFormat
        self.JoinOutputFormat = JoinOutputFormat
        self.joinFPS = joinFPS
        self.now = datetime.now()
        self.dt_string = self.now.strftime("%d-%m-%Y-%H-%M-%S")


        self.joinDirpathInput = self.dirpathOutput
        self.joinDirpathOutput = self.dirpathOutput

        print('Realizando junção dos frames...')
        self.videoJoined = ffmpeg.input(f'./{self.joinDirpathInput}/' + self.nameFormatter +"."+ self.joinInputFormat, framerate=self.joinFPS).output(f"./{self.joinDirpathOutput}/{self.dt_string}.{self.JoinOutputFormat}").run()
        print('Processo de junção finalizado...')

    def removePhotos(self, dirpathToRem, formatToRem):
        self.removePattern = self.photoNameFormatter
        self.dirpathToRem = dirpathToRem
        self.formatToRem = formatToRem
        self.photosToRemove = fnmatch.filter(os.listdir('./'+f'{self.dirpathToRem}' + '/'), self.removePattern +'.' + f'{self.formatToRem}')
        print(str(len(self.photosToRemove)))
        for f in self.photosToRemove:
            os.remove(self.dirpathToRem + f)
            print("Removido " + self.dirpathToRem + f)
            #concluir remoção

#---EXEMPLOS---#

##Utiliza uma foto em específica e transforma ela em um GIF, distorcendo pouco a pouco, com base nos parâmetros repassados:##
#distorcer = Distortion('input', 'output') #construtor padrão
#distorcer.imagePreProcess() ##carrega as fotos que existem na pasta citada no construtor ex: 'input', para a memória
#distorcer.makeGif(0.8, 0.00, 0.014, 0.0, 0.0,50, 'jpg',0)
#distorcer.joinFrames('gif', 25) #realiza o join de todos os frames da pasta output
#distorcer.removePhotos('output', 'jpg') #remove todas as fotos da pasta indicada, que são do formato 'jpg'

##Distorce um frame Unico. ou todos que estejam na pasta de entrada de dados##
ts = round(time.time() * 1000)
distorcer = Distortion('input', 'output') #construtor padrão
distorcer.imagePreProcess() ##carrega as fotos que existem na pasta citada no construtor ex: 'input', para a memória
distorcer.distort(0.8, 0.01, 0.01, 0.0, 0.7, sizeReductionPercent = 0) #distorce as imagens especificas com os padrões de distorções inseridos. NÃO USAR PARA PROCESSAR FRAMES DE VÍDEOS
tf = round(time.time() * 1000)
print("Demorou " + str(tf - ts) +" ms para processar.")

#EM TESTE#
##Extrai frames de vídeo, aplica a distorção nos frames com multiThread para agilizar o processo##
#distorcer = Distortion('input', 'output') #construtor padrão
#distorcer.extractVideoFrames('percebemos','mp4') #extrai os frames do vídeo com os argumentos passados, colocar referencia processedVideo, para aplicar o efeito de aúdio
#distorcer.multiThreadProcess(4, 'output') #inicia o parametro de carregamento das fotos, o segundo argumento é de onde as fotos serão carregads
#distorcer.makeVideo
#criar método que realiza o processamento paralelo com a quantia de threads paassadas, com as fotos carregas em multiThread e também colocar em threadsRodando cada thread
#nova que seja iniciada
#criar método para unir os frames resultantes com o audio editado e finalizar o vídeo