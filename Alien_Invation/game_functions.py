import sys
import pygame
from bullet import Bullet
from alien import Alien
def check_keydown_events(event,ship,screen,ai_settings,bullets):
    #相应按键
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings=ai_settings,screen=screen,ship=ship,bullets=bullets)
    elif event.key == pygame.K_q:
        sys.quit()

def fire_bullet(ai_settings,screen,ship,bullets):
    "如果没有达到限制，就发射一颗子弹"
    #创建新子弹，并将其加入到编组bullets中。
    if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings=ai_settings,screen=screen,ship=ship)
            bullets.add(new_bullet)
def check_up_events(event,ship):
    #相应松开
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ship,ai_settings,screen,bullets):
    #相应键盘和鼠标事件
    for event in pygame.event.get():    #用来获取用户的键盘输入
            if event.type == pygame.QUIT:   #如果用户点击了屏幕的退出按钮，调用sys方法退出
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                check_keydown_events(event=event,ship=ship,ai_settings=ai_settings,screen=screen,bullets=bullets)
            elif event.type == pygame.KEYUP:
                check_up_events(event=event,ship=ship)

def update_screen(ai_settings,screen,ship,bullets,aliens):
    screen.fill(ai_settings.bg_color)   #每次循环的时候重新绘制屏幕，只接受一个颜色参数
    "在飞船和外星人后面重新绘制所有子弹"
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()   #将飞船显示在屏幕前
    aliens.draw(screen)  #显示外星人
    pygame.display.flip()   #在每一次while循环结束后，刷新新的screen像素点位。

def update_bullets(bullets):
    "更新子弹的位置，并删除已经消失的子弹"
    #更新子弹的位置
    bullets.update()
    "消除已经消失的子弹"
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    print(len(bullets))
def create_fleet(ai_settings,screen,aliens):
    "创建外星人群"
    alien = Alien(ai_settings=ai_settings,screen=screen)
    alien_width = alien.rect.width  #创建一个外星人
    #计算一行可以容纳多少个外星人
    available_space_x = ai_settings.screen_width - 2* alien_width
    number_alien_x = int(available_space_x / (2* alien_width))
    #创建第一行外星人
    for alien_number in range(number_alien_x):
        #创建第一个外星人并将其加入到当前行
        alien = Alien(ai_settings=ai_settings,screen=screen)
        alien.x = alien_width +2 * alien_width* alien_number
        alien.rect.x = alien.x
        aliens.add(alien)