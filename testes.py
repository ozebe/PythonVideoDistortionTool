def multiprocessamento(qtdThreads, fotos, dirpath, width, height):
    ###################################################################################################################
    qtdFrames = len(fotos)
    framesToThreads = (qtdFrames / qtdThreads)
    floorFramesToThreads = math.floor(framesToThreads) #arredonda para baixo a quantia de frames para cada Thread
    comeco = 0

    #caso a divisão de frames seja igual para todos as Threads
    if((qtdFrames % qtdThreads) == 0):
        j = qtdFrames / qtdThreads
        print("Total de frames: " +str( qtdFrames))
        print("Threads executando: " + str(qtdThreads))
        for i in range(qtdThreads):
            #se estiver no começo
            if(i == 0):
                #chama a thread para distorção
                fts = fotos[i:floorFramesToThreads]
                args = [fts, dirpath, width, height]
                
                #args.append(fts, dirpath, width, height)
                enableMultithread(distorceInicial, args)

                #chama a funcao que irá aplicar o efeito e passa a lista fotos[i:floorFramesToThreads]
                #print("Thread " + str(i) + ", frames: " + str(j) + " : " + str(fotos[i:floorFramesToThreads]))
                comeco = floorFramesToThreads
            #se estiver no final
            elif(i + 1 == qtdThreads):
                fts = fotos[comeco:qtdFrames]
                args = [fts, dirpath, width, height]
                
                #args.append(fts, dirpath, width, height)
                enableMultithread(distorce, args)

                #print("Thread " + str(i) + ", frames: " + str(j) + " : " + str(fotos[comeco:qtdFrames]))
            #se estiver no meio
            else:
                fts = fotos[comeco:floorFramesToThreads + comeco]
                args = [fts, dirpath, width, height]
                
                #args.append(fts, dirpath, width, height)
                enableMultithread(distorce, args)

                #print("Thread " + str(i) + ", frames: " + str(j) + " : " + str(fotos[comeco:floorFramesToThreads + comeco])) 
                comeco += floorFramesToThreads

    else:
        #caso a divisão resultante seja par
        if((qtdFrames % 2) == 0):
            c = math.ceil(framesToThreads - floorFramesToThreads)
            d = (floorFramesToThreads * qtdThreads) + (c * 2)
            e = floorFramesToThreads + (c * 2)
            print("Total de frames: " +str( qtdFrames))
            print("Threads executando: " + str(qtdThreads))
            print("Frames para Threads: " + str(d))
            for x in range(qtdThreads):
                #se estiver no começo
                if(x == 0):
                    #chama a thread para distorção
                    fts = fotos[x:floorFramesToThreads]
                    args = [fts, dirpath, width, height]
                    
                    
                    #args.append((fts, dirpath, width, height))
                    enableMultithread(distorceInicial, args)

                    #print("Thread " + str(x) + ", frames: " + str(floorFramesToThreads) + " : " + str(fotos[x:floorFramesToThreads])) 
                    comeco = floorFramesToThreads
                #se estiver no final
                elif(x + 1 == qtdThreads):
                    #chama a thread para distorção
                    fts = fotos[comeco:qtdFrames]
                    args = [fts, dirpath, width, height]
                    
                    #args.append((fts, dirpath, width, height))
                    enableMultithread(distorce, args)

                    #print("Thread " + str(x) + ", frames: " + str(e) + " : " + str(fotos[comeco:qtdFrames])) 

                #se estiver no meio    
                else:
                    #chama a thread para distorção
                    fts = fotos[comeco:floorFramesToThreads + comeco]
                    args = [fts, dirpath, width, height]
                    
                    #args.append((fts, dirpath, width, height))
                    enableMultithread(distorce, args)

                    #print("Thread " + str(x) + ", frames: " + str(floorFramesToThreads) + " : " + str(fotos[comeco:floorFramesToThreads + comeco])) 
                    comeco += floorFramesToThreads
        #se for impar
        else:
            #a2 = qtdFrames / qtdThreads
            #b2 = math.floor(a2)
            c2 = math.floor((framesToThreads - floorFramesToThreads) * qtdThreads)
            d2 = (floorFramesToThreads * qtdThreads) + c2
            e2 = floorFramesToThreads + c2
            print("Total de frames: " +str( qtdFrames))
            print("Threads executando: " + str(qtdThreads))
            print("Frames para Threads: " + str(d2))
            #comeco = 0
            for x2 in range(qtdThreads):
                #se estiver no começo
                if(x2 == 0):
                    #chama a thread para distorção
                    fts = fotos[x2:floorFramesToThreads]
                    args = [fts, dirpath, width, height]
                    
                    #args.append((fts, dirpath, width, height))
                    enableMultithread(distorceInicial, args)
                    
                    #print("Thread " + str(x2) + ", frames: " + str(floorFramesToThreads) + " : " + str(fotos[x2:floorFramesToThreads])) 
                    comeco = floorFramesToThreads
                #se estiver no final
                elif(x2 + 1 == qtdThreads):
                    #chama a thread para distorção
                    fts = fotos[comeco:qtdFrames]
                    args = [fts, dirpath, width, height]
                    
                    #args.append((fts, dirpath, width, height))
                    enableMultithread(distorce, args)

                    #print("Thread " + str(x2) + ", frames: " + str(e2) + " : " + str(fotos[comeco:qtdFrames])) 
                #se estiver no meio
                else:
                    #chama a thread para distorção
                    fts = fotos[comeco:floorFramesToThreads + comeco]
                    args = [fts, dirpath, width, height]
                    
                    #args.append((fts, dirpath, width, height))
                    enableMultithread(distorce, args)

                    #print("Thread " + str(x2) + ", frames: " + str(floorFramesToThreads) + " : " + str(fotos[comeco:floorFramesToThreads + comeco])) 
                    comeco += floorFramesToThreads
    ###################################################################################################################