import pygame
import random
import math
import sys

# ==========================================
# PARÂMETROS DO PROGRAMA
# ==========================================
LARGURA_JANELA = 800
ALTURA_JANELA = 600
NUM_ESFERAS = 15
RAIO = 15
VEL_MAXIMA = 200  # Pixels por segundo
DT = 0.016        # Intervalo de tempo (aprox. 60 FPS)

# Cores
COR_FUNDO = (30, 80, 40) # Verde clássico de mesa de sinuca
BRANCO = (255, 255, 255)

class Bola:
    def __init__(self):
        # Posições aleatórias (garantindo que não nasçam coladas na parede)
        self.x = random.uniform(RAIO, LARGURA_JANELA - RAIO)
        self.y = random.uniform(RAIO, ALTURA_JANELA - RAIO)
        
        # Velocidades aleatórias (vx e vy)
        self.vx = random.uniform(-VEL_MAXIMA, VEL_MAXIMA)
        self.vy = random.uniform(-VEL_MAXIMA, VEL_MAXIMA)
        
        # Cor aleatória para visualização
        self.cor = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    def atualizar_posicao(self, dt):
        # x(novo) = x(atual) + vx * dt (Movimento Retilíneo Uniforme)
        self.x += self.vx * dt
        self.y += self.vy * dt

    def checar_colisao_parede(self):
        # Colisão com as paredes laterais (Eixo X)
        if self.x - RAIO <= 0:
            self.x = RAIO # Impede que entre na parede
            self.vx *= -1 # Inverte a velocidade perpendicular
        elif self.x + RAIO >= LARGURA_JANELA:
            self.x = LARGURA_JANELA - RAIO
            self.vx *= -1

        # Colisão com teto e chão (Eixo Y)
        if self.y - RAIO <= 0:
            self.y = RAIO
            self.vy *= -1
        elif self.y + RAIO >= ALTURA_JANELA:
            self.y = ALTURA_JANELA - RAIO
            self.vy *= -1

def resolver_colisoes_bolas(bolas):
    # Testa a colisão de todas as bolas contra todas as outras
    for i in range(len(bolas)):
        for j in range(i + 1, len(bolas)):
            b1 = bolas[i]
            b2 = bolas[j]
            
            # Distância entre os centros (Teorema de Pitágoras)
            dx = b2.x - b1.x
            dy = b2.y - b1.y
            distancia = math.hypot(dx, dy)
            
            # Se a distância é menor que 2x o raio, elas colidiram!
            if distancia < 2 * RAIO:
                # 1. PREVENÇÃO DE SOBREPOSIÇÃO (Evita que elas fiquem grudadas)
                sobreposicao = 2 * RAIO - distancia
                if distancia == 0: distancia = 0.0001 # Evita divisão por zero
                
                nx = dx / distancia # Componente X do Vetor normal
                ny = dy / distancia # Componente Y do Vetor normal
                
                # Afasta as bolas metade da sobreposição para cada lado
                b1.x -= nx * (sobreposicao / 2)
                b2.x += nx * (sobreposicao / 2)
                b1.y -= ny * (sobreposicao / 2)
                b2.y += ny * (sobreposicao / 2)
                
                # 2. FÍSICA DA COLISÃO (Troca de velocidades ao longo do vetor normal)
                # Velocidade relativa
                dvx = b1.vx - b2.vx
                dvy = b1.vy - b2.vy
                
                # Produto escalar da velocidade relativa pelo vetor normal
                p = dvx * nx + dvy * ny
                
                # Se p < 0, as bolas já estão se afastando, ignoramos a matemática
                if p < 0: continue 
                
                # Atualizamos as velocidades (Conservação do Momento e Energia Cinética)
                b1.vx -= p * nx
                b1.vy -= p * ny
                b2.vx += p * nx
                b2.vy += p * ny

# ==========================================
# LOOP PRINCIPAL DO PROGRAMA
# ==========================================
def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
    pygame.display.set_caption("Simulador de Colisões - Bolas de Sinuca")
    relogio = pygame.time.Clock()

    # Cria a lista de esferas (N posições e N velocidades)
    esferas = [Bola() for _ in range(NUM_ESFERAS)]

    rodando = True
    while rodando:
        # Evento para fechar a janela
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # 1. Atualizar física (com base no DT)
        for bola in esferas:
            bola.atualizar_posicao(DT)
            bola.checar_colisao_parede()
        
        # Checar e resolver colisões entre as esferas
        resolver_colisoes_bolas(esferas)

        # 2. Desenhar na tela
        tela.fill(COR_FUNDO) # Limpa a tela com a cor verde
        for bola in esferas:
            # Converte float para int na hora de desenhar na tela
            pygame.draw.circle(tela, bola.cor, (int(bola.x), int(bola.y)), RAIO)
            # Desenha uma borda branca sutil
            pygame.draw.circle(tela, BRANCO, (int(bola.x), int(bola.y)), RAIO, 1)

        pygame.display.flip()
        
        # Controla a taxa de atualização para manter a física constante
        relogio.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()