import math
#pega as fotos já extraídas do vídeo da pasta indicada
def makeVideo(self, videoMaxPercentage, videoWidthmultiplyer, videoHeightmultiplyer, videoWidthPorcentage, videoHeightPorcentage, videoOutputFormat = 'mp4', videoSizeReductionPercent = 0):
    self.qtdFramesVideo = len(self.photos) #quantia de frames para serem processadas, tal informação deve ser pré carregada com o multiThreadProcess
    self.qtdThreadsVideoProcess = self.qtdThreads #quantia de threads para processar os frames, tal informação deve ser pré carregada com o multiThreadProcess
    self.framesToThreads = (self.qtdFramesVideo / self.qtdThreadsVideoProcess)
    self.floorFramesToThreads = math.floor(self.framesToThreads)
    self.comeco = 0

    #ARGS PRECISA TER:
    #    def distort(self, maxPercentage, widthMultiplyer = 0, heightMultiplyer = 0, widthPercentage = 0,  heightPercentage = 0, photosToDistort = 0 , 
    # gifFrames = 1, outputFormat = 'jpg', sizeReductionPercent = 0.5):
    #args = [self.videoMaxPercentage, self.videoWidthmultiplyer, self.videoHeightmultiplyer, self.videoWidthPorcentage, self.videoHeightPorcentage, fts, gifFrames = 1, sizeRedutionPercent = 0]
    
    #caso a divisão de frames seja igual para todos as Threads
    if((self.qtdFramesVideo % self.qtdThreadsVideoProcess) == 0):
        j = self.qtdFramesVideo / self.qtdThreadsVideoProcess
        print("Total de frames: " +str( self.qtdFramesVideo))
        print("Threads executando: " + str(self.qtdThreadsVideoProcess))
        for i in range(self.qtdThreadsVideoProcess):
            #se estiver no começo
            if(i == 0):
                #chama a thread para distorção
                fts = self.photos[i:self.floorFramesToThreads]
                args = [fts, dirpath, width, height]
                
                #args.append(fts, dirpath, width, height)
                enableMultithread(distorceInicial, args)

                comeco = self.floorFramesToThreads
            #se estiver no final
            elif(i + 1 == qtdThreads):
                fts = fotos[comeco:qtdFrames]
                args = [fts, dirpath, width, height]
                
                #args.append(fts, dirpath, width, height)
                enableMultithread(distorce, args)

            #se estiver no meio
            else:
                fts = self.photos[comeco:self.floorFramesToThreads + comeco]
                args = [fts, dirpath, width, height]
                
                #args.append(fts, dirpath, width, height)
                enableMultithread(distorce, args)

                comeco += self.floorFramesToThreads

    else:
