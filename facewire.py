import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import csv
import os
import time
from tkinter import Tk, filedialog

def escolher_csv():
    root = Tk()
    root.withdraw()
    caminho = filedialog.askopenfilename(
        title="Selecionar ficheiro CSV",
        filetypes=[("Ficheiros CSV", "*.csv")]
    )
    root.destroy()
    return caminho

def ler_faces_de_pontos(caminho):
    pontos = []
    with open(caminho, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 6:
                continue
            try:
                ponto = list(map(float, row[:3]))  # só o primeiro ponto
                pontos.append(ponto)
            except ValueError:
                continue

    # Agrupa a cada 4 pontos → 1 face
    faces = [pontos[i:i+4] for i in range(0, len(pontos), 4) if len(pontos[i:i+4]) == 4]
    return faces

def desenhar_faces_com_linhas(faces):
    glColor3f(0, 0, 0)  # preto
    glLineWidth(2)
    for face in faces:
        glBegin(GL_QUADS)  # conecta os 4 pontos e fecha
        for ponto in face:
            glVertex3fv(ponto)
        glEnd()

def main():
    caminho = escolher_csv()
    if not caminho or not os.path.exists(caminho):
        print("Ficheiro não encontrado.")
        return

    faces = ler_faces_de_pontos(caminho)
    if not faces:
        print("Nenhuma face válida encontrada.")
        return

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Visualizador de Faces (Linhas 3D)")

    glClearColor(1.0, 1.0, 0.0, 1.0)  # fundo amarelo
    glEnable(GL_DEPTH_TEST)

    gluPerspective(45, (display[0] / display[1]), 0.1, 1000.0)
    glTranslatef(-5, -5, -30)

    angulo = 0
    tempo_ultima_rotacao = time.time()
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(60)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for evento in pygame.event.get():
            if evento.type == QUIT:
                running = False

        # rotação automática a cada 0.1 segundos
        if time.time() - tempo_ultima_rotacao > 0.1:
            angulo += 5
            tempo_ultima_rotacao = time.time()

        glPushMatrix()
        glRotatef(angulo % 360, 0, 1, 0)
        desenhar_faces_com_linhas(faces)
        glPopMatrix()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

