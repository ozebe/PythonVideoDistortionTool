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
                #args = [fts, dirpath, width, height]
                args = [self.videoMaxPercentage, self.videoWidthmultiplyer, self.videoHeightmultiplyer, self.videoWidthPorcentage, self.videoHeightPorcentage, fts, gifFrames = 1, sizeRedutionPercent = 0]
                
                #args.append(fts, dirpath, width, height)
                #enableMultithread(distorceInicial, args)
                enableMultithread(self.distort, args)

                comeco = self.floorFramesToThreads
            #se estiver no final
            elif(i + 1 == self.qtdThreadsVideoProcess):
                fts = self.photos[comeco:self.qtdFramesVideo]
                args = [self.videoMaxPercentage, self.videoWidthmultiplyer, self.videoHeightmultiplyer, self.videoWidthPorcentage, self.videoHeightPorcentage, fts, gifFrames = 1, sizeRedutionPercent = 0]
                
                #args.append(fts, dirpath, width, height)
                enableMultithread(self.distort, args)

            #se estiver no meio
            else:
                fts = self.photos[comeco:self.floorFramesToThreads + comeco]
                args = [self.videoMaxPercentage, self.videoWidthmultiplyer, self.videoHeightmultiplyer, self.videoWidthPorcentage, self.videoHeightPorcentage, fts, gifFrames = 1, sizeRedutionPercent = 0]
                
                #args.append(fts, dirpath, width, height)
                enableMultithread(self.distort, args)

                comeco += self.floorFramesToThreads

    else:
        #caso a divisão resultante seja par
        if((self.qtdFramesVideo % 2) == 0):
            c = math.ceil(self.framesToThreads - self.floorFramesToThreads)
            d = (self.floorFramesToThreads * self.qtdThreadsVideoProcess) + (c * 2)
            e = self.floorFramesToThreads + (c * 2)
            print("Total de frames: " +str( self.qtdFramesVideo))
            print("Threads executando: " + str(self.qtdThreadsVideoProcess))
            print("Frames para Threads: " + str(d))
            for x in range(self.qtdThreadsVideoProcess):
                #se estiver no começo
                if(x == 0):
                    #chama a thread para distorção
                    fts = self.photos[x:self.floorFramesToThreads]
                    args = [self.videoMaxPercentage, self.videoWidthmultiplyer, self.videoHeightmultiplyer, self.videoWidthPorcentage, self.videoHeightPorcentage, fts, gifFrames = 1, sizeRedutionPercent = 0]
                    
                    
                    #args.append((fts, dirpath, width, height))
                    #enableMultithread(distorceInicial, args)
                    enableMultithread(self.distort, args)

                    #print("Thread " + str(x) + ", frames: " + str(floorFramesToThreads) + " : " + str(fotos[x:floorFramesToThreads])) 
                    comeco = self.floorFramesToThreads
                #se estiver no final
                elif(x + 1 == self.qtdThreadsVideoProcess):
                    #chama a thread para distorção
                    fts = self.photos[comeco:self.qtdFramesVideo]
                    args = [self.videoMaxPercentage, self.videoWidthmultiplyer, self.videoHeightmultiplyer, self.videoWidthPorcentage, self.videoHeightPorcentage, fts, gifFrames = 1, sizeRedutionPercent = 0]
                    
                    #args.append((fts, dirpath, width, height))
                    enableMultithread(distorce, args)

                    #print("Thread " + str(x) + ", frames: " + str(e) + " : " + str(fotos[comeco:qtdFrames])) 

                #se estiver no meio    
                else:
                    #chama a thread para distorção
                    fts = self.photos[comeco:self.floorFramesToThreads + comeco]
                    args = [self.videoMaxPercentage, self.videoWidthmultiplyer, self.videoHeightmultiplyer, self.videoWidthPorcentage, self.videoHeightPorcentage, fts, gifFrames = 1, sizeRedutionPercent = 0]
                    
                    #args.append((fts, dirpath, width, height))
                    enableMultithread(distorce, args)

                    #print("Thread " + str(x) + ", frames: " + str(floorFramesToThreads) + " : " + str(fotos[comeco:floorFramesToThreads + comeco])) 
                    comeco += self.floorFramesToThreads
        #se for impar
        else:
            #a2 = qtdFrames / qtdThreads
            #b2 = math.floor(a2)
            c2 = math.floor((self.framesToThreads - self.floorFramesToThreads) * self.qtdThreadsVideoProcess)
            d2 = (self.floorFramesToThreads * self.qtdThreadsVideoProcess) + c2
            e2 = self.floorFramesToThreads + c2
            print("Total de frames: " +str(self.qtdFramesVideo))
            print("Threads executando: " + str(self.qtdThreadsVideoProcess))
            print("Frames para Threads: " + str(d2))
            #comeco = 0
            for x2 in range(self.qtdThreadsVideoProcess):
                #se estiver no começo
                if(x2 == 0):
                    #chama a thread para distorção
                    fts = self.photos[x2:self.floorFramesToThreads]
                    args = [self.videoMaxPercentage, self.videoWidthmultiplyer, self.videoHeightmultiplyer, self.videoWidthPorcentage, self.videoHeightPorcentage, fts, gifFrames = 1, sizeRedutionPercent = 0]
                    
                    #args.append((fts, dirpath, width, height))
                    #enableMultithread(distorceInicial, args)
                    enableMultithread(self.distort, args)
                    
                    #print("Thread " + str(x2) + ", frames: " + str(floorFramesToThreads) + " : " + str(fotos[x2:floorFramesToThreads])) 
                    comeco = self.floorFramesToThreads
                #se estiver no final
                elif(x2 + 1 == self.qtdThreadsVideoProcess):
                    #chama a thread para distorção
                    fts = self.photos[comeco:self.qtdFramesVideo]
                    args = [self.videoMaxPercentage, self.videoWidthmultiplyer, self.videoHeightmultiplyer, self.videoWidthPorcentage, self.videoHeightPorcentage, fts, gifFrames = 1, sizeRedutionPercent = 0]
                    
                    #args.append((fts, dirpath, width, height))
                    enableMultithread(distorce, args)

                    #print("Thread " + str(x2) + ", frames: " + str(e2) + " : " + str(fotos[comeco:qtdFrames])) 
                #se estiver no meio
                else:
                    #chama a thread para distorção
                    fts = self.photos[comeco:self.floorFramesToThreads + comeco]
                    args = [self.videoMaxPercentage, self.videoWidthmultiplyer, self.videoHeightmultiplyer, self.videoWidthPorcentage, self.videoHeightPorcentage, fts, gifFrames = 1, sizeRedutionPercent = 0]
                    
                    #args.append((fts, dirpath, width, height))
                    enableMultithread(distorce, args)

                    #print("Thread " + str(x2) + ", frames: " + str(floorFramesToThreads) + " : " + str(fotos[comeco:floorFramesToThreads + comeco])) 
                    comeco += self.floorFramesToThreads
    ###################################################################################################################