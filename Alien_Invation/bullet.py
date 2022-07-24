import pygame
from pygame.sprite import Sprite
class Bullet(Sprite):   #继承Sprite类，进行游戏编组，从而操作所有元素
    "对飞船发射的子弹进行管理"
    def __init__(self,ai_settings,screen,ship):
        super(Bullet,self).__init__() #加载父类的所有属性
        self.screen = screen
        #在（0，0）位置创建一个表示子弹的矩形，再进行移动。
        self.rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top   #代表子弹是从ship的顶部射出来的
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
    def update(self):
        #向上移动子弹
        self.y -= self.speed_factor #更新表示子弹位置的小数值
        self.rect.y = self.y    #更新表示子弹的rect的位置

    def draw_bullet(self):
        #再屏幕上绘制子弹
        pygame.draw.rect(self.screen,self.color,self.rect)