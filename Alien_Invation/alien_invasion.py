'''
外星人入侵的主文件，设置屏幕的大小，颜色
'''
import pygame
import sys
from settings import Settings
from ship import Ship
import game_functions as gf
from alien import Alien
from pygame.sprite import Group
def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))    #创建一个1200像素高，800像素宽的屏幕
    pygame.display.set_caption("Alien Invation")    #显示屏幕框的文字。
    ship  = Ship(screen,ai_settings)  #创建一个飞船
    bullets = Group()   #创建一个用于存储子弹的编组
    aliens = Group()    #创建一个存储外星人的编组
    gf.create_fleet(ai_settings,screen,aliens)
    alien = Alien(ai_settings=ai_settings,screen=screen)    #创建一个外星人实例
    while True:
        gf.check_events(ship=ship,ai_settings=ai_settings,screen=screen,bullets=bullets)   #为了代码整洁，将函数写在了gf中。#相应键盘和鼠标事件
        ship.update()
        gf.update_bullets(bullets=bullets)
        gf.update_screen(ai_settings=ai_settings,screen=screen,ship=ship,bullets=bullets,aliens=aliens)
        
run_game()  