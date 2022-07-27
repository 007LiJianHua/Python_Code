import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self,screen,ai_settings):
        #初始化飞船并设置其起始位置
        super(Ship,self).__init__()
        self.screen = screen    #初始化飞船并设置其初始位置
        self.ai_settings = ai_settings  #将setting中飞船的设置加入进来。
        self.image = pygame.image.load("images/ship.bmp")   #加载图片，并将图片元素存储在self.image中
        self.rect = self.image.get_rect()   #获取图像相应的属性
        self.screen_rect = self.screen.get_rect()    #获取整个游戏屏幕的矩形
        self.rect.centerx = self.screen_rect.centerx    #飞船中心的x坐标 = 屏幕矩形的属性centerx
        self.rect.bottom = self.screen_rect.bottom  #飞船中心下边缘的y坐标 = 屏幕矩形的bottom
        self.center = float(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False

    def update(self):
        #根据移动标志调整飞船的位置
        if self.moving_right and self.rect.right < self.screen_rect.right:  #飞船矩形的右边缘坐标小于屏幕边框
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0: #飞船矩形的左边缘坐标大于0
            self.center -= self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center
    def blitme(self):   #根据图片和飞船的位置，进行显示
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        "让飞船在屏幕上居中"
        self.center = self.screen_rect.centerx