from asyncio import Event
import pygame as pg
import sys

WIDTH = 800
HEIGHT = 600


class Bird(pg.sprite.Sprite):
    """
    ゲームキャラクター(こうかとん)に関するクラス
    """
    def __init__(self,num: int,x: int):
        """
        こうかとん画像Surfaceを生成する
        引数1 num:こうかとん画像ファイル名の番号
        """
        super().__init__()
        self.mode = 0
        self.jump = 0
        self.cnt = 0
        self.num=num
        self.img = pg.image.load(f"ex05/fig/{self.num}.png")
        self.rect = self.img.get_rect()
        self.rect.centerx = x
        self.rect.bottom = 500
        print(f"bird.height:{self.rect.height}")
        print(f"bird.bottom:{self.rect.bottom}")
        
    def update(self,screen: pg.Surface, mode: int):
        """
        
        """
        if mode == 0:
            if self.mode == 0:
                screen.blit(self.img,self.rect)
            if self.mode == 1:
                screen.blit(pg.transform.flip(self.img,True,False),self.rect)
            if self.jump == 1:
                self.rect.bottom -=5
                if self.rect.bottom <= 350:
                    self.cnt +=1
                    self.rect.bottom += 5
                    if self.cnt >=20:
                        self.jump = 0
                        self.cnt = 0
            if self.jump == 0 and self.rect.bottom < 500:
                self.rect.bottom += 5
        elif mode == 1:
            self.img = pg.image.load(f"ex05/fig/{self.num}.png")
            screen.blit(self.img,self.rect)
        elif mode == 2:
            self.img = pg.image.load(f"ex05/fig/{self.num}.png")
            screen.blit(self.img,self.rect)

class Background:
    """
    背景の処理をする
    """
    def __init__(self, screen: pg.Surface):
        self.x=0
        self.bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
        self.bg_img_fl = pg.transform.flip(self.bg_img,True,False)
        screen.blit(self.bg_img_fl,[-800,0])

    def update(self, screen: pg.Surface, mode: int):
        """
        移動に応じたupdateを行う
        """
        if mode == 0:
            self.x%=3200
            screen.blit(self.bg_img,[800-self.x,0])
            screen.blit(self.bg_img_fl,[2400-self.x,0])
            screen.blit(self.bg_img_fl,[-800-self.x,0])
        else:
            screen.blit(self.bg_img,[800-self.x,0])
            screen.blit(self.bg_img_fl,[2400-self.x,0])
            screen.blit(self.bg_img_fl,[-800-self.x,0])


class Enemy(pg.sprite.Sprite):
    def __init__(self, screen: pg.Surface, e_x: int):
        super().__init__()
        self.e_x = e_x
        self.vx = 0
        self.ene_img = pg.transform.rotozoom(pg.image.load("ex05/fig/monster11.png"),0,0.2)
        self.rect = self.ene_img.get_rect()
        self.rect.centerx = self.e_x
        self.rect.bottom = 500
        screen.blit(self.ene_img,self.rect)
        print(f"ene.height:{self.rect.height}")
        print(f"ene.bottom:{self.rect.bottom}")

    def update(self, screen: pg.Surface, vx: int, mode: int):
        if mode == 0:
            self.vx = vx
            self.rect.move_ip(-self.vx,0)
            self.rect.centerx -= 3
            screen.blit(self.ene_img,self.rect)
        else:
            screen.blit(self.ene_img,self.rect)
        

class Goal(pg.sprite.Sprite):
    def __init__(self, screen: pg.Surface):
        super().__init__()
        self.g_img = pg.transform.rotozoom(pg.image.load("ex05/fig/torinosu_egg.png"),0,0.2)
        self.rect = self.g_img.get_rect()
        self.rect.centerx = 3200
        self.rect.bottom = 500
        screen.blit(self.g_img,self.rect)
        print(f"gl.height:{self.rect.height}")
        print(f"gl.bottom:{self.rect.bottom}")

    def update(self, screen: pg.Surface,bg: Background):
        self.rect.centerx = 3200 - bg.x
        screen.blit(self.g_img,self.rect)


def main():
    pg.display.set_caption("Super_Kokaton")
    screen = pg.display.set_mode((WIDTH,HEIGHT))

    bird = Bird(2,200)
    bg = Background(screen)
    enes = pg.sprite.Group()
    gls = pg.sprite.Group()
    for i in range(3):
        enes.add(Enemy(screen,i*400+800))
    gl = Goal(screen)
    gls.add(gl)

    tmr = 0
    mode = 0
    clock = pg.time.Clock()
    
    while True:
        vx = 0
        for  event in pg.event.get():
            if event.type == pg.QUIT: return
        if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT and mode == 0:
            bird.mode = 0
            bg.x += 5
            vx = 5
        if event.type == pg.KEYDOWN and event.key == pg.K_LEFT and mode == 0:
            bird.mode = 1
            bg.x -= 5
            if bg.x > 0:
                vx = -5
        if bg.x <= 0:
            bg.x = 0
        if bird.rect.centerx >= gl.rect.centerx:
            bg.x = 3000
        if bird.rect.bottom == 500 and event.type == pg.KEYDOWN and event.key == pg.K_UP:
            bird.jump = 1
        for ene in pg.sprite.spritecollide(bird, enes, False):
            if bird.rect.bottom <= ene.rect.top + 5:
                enes.remove(ene)
                pass
            else:
                bird.num = 8
                tmr += 1
                mode = 1
        for goal in pg.sprite.spritecollide(bird,gls,False):
            bird.num = 6
            tmr += 1
            mode = 2
        if tmr >= 150:
            return

        bg.update(screen, mode)
        bird.update(screen, mode)
        enes.update(screen, vx, mode)
        gls.update(screen,bg)
        pg.display.update()
        clock.tick(60)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

