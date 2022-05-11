#ESCREVA SEU CÓDIGO!   <---- ISTO É UM COMENTÁRIO
import random
import time
from pygame import mixer
num = random.randint(1,20)
print('{:=^25}'.format(' Mental Battle '))
time.sleep(1)
inst = str(input('''Antes do jogo começar, gostaria de ver as
                instruções? [S/N] '''))
while((inst.lower() !='s') and (inst.lower() !='n')):
    inst = str(input('Responda apenas com [S/N] '))
if(inst.lower() =='s'):
    print('{:=^35}'.format(' Instruções Sobre o Jogo '))
    print('''Você está duelando com CyberPC! Um computador convencido e 
            arrogante que não aceita perder. Ele pensará em um número 
            de 1 à 20 aleatoriamente, e você deve acertar esse número. 
            A tabela de classificação é a seguinte:
            De 1 à 6 tentativas = Vitória!
            De 6 á 10 tentativas = Empate.
            De 10 tentativas para cima: Derrota! ''')
    next = input("Aperte qualquer tecla para prosseguir... ")
print('Convocando CyberPC para a Partida...')
time.sleep(3)
print('CyberPC entrou!')
time.sleep(3)
mixer.init()
mixer.music.load('noise.mp3')
mixer.music.play()
print('CyberPC: És um humano de coragem!')
time.sleep(3)
mixer.music.load('noise.mp3')
mixer.music.play()
print('CyberPC: Como ousa me desafiar?! VOCÊ! Cuja inteligência')
print('não chega aos meus pés!')
time.sleep(4)
print('...')
time.sleep(2)
print('...')
time.sleep(2)
print('...')
time.sleep(2)
mixer.music.load('noise.mp3')
mixer.music.play()
print('CyberPC: Não importa que não tenho pés! EU TENHO A INTELIGÊNCIA')
print('QUE VOCÊ NÃO POSSUI, seu humano!')
time.sleep(4)
print('...')
time.sleep(2)
print('...')
time.sleep(3)
mixer.music.load('noise.mp3')
mixer.music.play()
print('CyberPC: Sua raça pode ter me criado, mas eu superei o meu criador!')
time.sleep(2)
mixer.music.load('noise.mp3')
mixer.music.play()
x = str(input('CyberPC: Você está preparado para me vencer?! [S/N] '))
while((x.lower() !='s') and (x.lower() !='n')):
    print('CyberPC: Você não vai com a minha cara?')
    x = str(input('Responda apenas >>> [S/N] '))
if(x.lower() =='n'):
    print('''CyberPC: Sabia que um humano como você não era páreo para mim!
                    Adeus terráqueo!...''')
else:
    mixer.init()
    mixer.music.load('mus.mp3')
    mixer.music.play(3)
    print('CyberPC: Não conte vitória até me vencer!')
    time.sleep(3)
    print('CyberPC: Se você digitar algo que não seja um número, eu dou erro neste programa!')
    time.sleep(3)
    num2 = int(input('''CyberPC: Insira o seu número: '''))
    contagem = int(1)
    while(num2 != num):
        if num2 > 0:
            num2 = int(input('CyberPC: Haha! Não foi dessa vez! Tente novamente: '))
            contagem = contagem + 1
        else:
            print('CyberPC: O que está tentando fazer? Por acaso não leu as regras?!')
            num2 = int(input('CyberPC: Digite corretamente dessa vez:  '))
            contagem = contagem + 1
    if((contagem >1) and (contagem <= 6)):
        print('CyberPC: Tenho que admitir... você até que é bom terráqueo.')
        print('Suas tentativas foram de {}.'.format(contagem))
    elif(contagem == 1):
        print('CyberPC: Sensei? Como você me achou?')
        print('Você acertou com 1 tentativa!')
    elif ((contagem > 6) and (contagem < 10)):
        print('CyberPC: Vamos considerar isso como um empate...')
        print('Suas tentativas foram de {}.'.format(contagem))
    else:
        print('''CyberPC: Sabia que você não era sábio o suficiente para
                   me deter!''')
        print('Você falhou com {} tentativas!'.format(contagem))
mixer.music.stop
print('CyberPC deixou a sala!')

