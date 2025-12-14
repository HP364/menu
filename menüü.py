import pygame
import pygame_gui

pygame.init()

ekraan = pygame.display.set_mode([640, 480])
manager = pygame_gui.UIManager([640, 480])
pygame.display.set_caption("mäng")
ekraan.fill([0,0,0])
heli = pygame.mixer.Sound("tp3.wav")
heli.set_volume(0.5)
kell = pygame.time.Clock()
kuju=pygame.image.load("kuju.png")
kuju_x=580/2
kuju_y=300
kuju_x_kiirus=0
kuju_y_kiirus=0
kuju_w=kuju.get_width()
kuju_h=kuju.get_height()
gravitatsioon=980
maapind=300
kuju_baaskiirus=400
mäng_töötab = True
paus=False 
pealkiri= pygame.image.load("tiitel.png")
olek="menüü"
slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((0, 0), (250, 40)),
    start_value=50,
    value_range=(0, 100),
    manager=manager)

nupp1=pygame_gui.elements.UIButton(pygame.Rect((530,0),(120,50)),"autorid",manager)

nupp2=pygame_gui.elements.UIButton(pygame.Rect((530,0),(120,50)),"sulge",manager)

nupp3=pygame_gui.elements.UIButton(pygame.Rect((220,300),(120,50)),"sulge?",manager)

nupp4=pygame_gui.elements.UIButton(pygame.Rect((150,370),(120,50)),"jah",manager)

nupp5=pygame_gui.elements.UIButton(pygame.Rect((290,370),(120,50)),"ei",manager)

nupp6=pygame_gui.elements.UIButton(pygame.Rect((240,300),(120,50)),"exit",manager)

nupp7=pygame_gui.elements.UIButton(pygame.Rect((240,200),(120,50)),"start",manager)

teade=pygame_gui.elements.UITextBox("Autor:Holger",((420, 80), (460, 150)),manager)


slider.hide()
nupp1.hide()
nupp2.hide()
teade.hide()
nupp3.hide()
nupp4.hide()
nupp5.hide()
def mine_pausi():
    slider.show()
    heli.stop()
    nupp1.show()
    nupp3.show()
    heli.stop()
def lahku_pausist():
    slider.hide()
    heli.play()
    nupp1.hide()
    nupp3.hide()
    nupp4.hide()
    nupp5.hide()
    teade.hide()
    nupp2.hide()    
def mine_mängu():
    nupp7.hide()
    nupp6.hide()
    slider.hide()
    nupp1.hide()
    nupp3.hide()
    nupp4.hide()
    nupp5.hide()
    teade.hide()
    heli.play()
while mäng_töötab:
    
    dt = kell.tick(60) / 1000
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            mäng_töötab = False
       

        if e.type == pygame.KEYDOWN:
            
            if e.key==pygame.K_ESCAPE and olek=="mäng":
                paus= not paus 
                if paus:
                    mine_pausi()
                else:
                    lahku_pausist()
            #tegelase liikumine
            if e.key==pygame.K_LEFT and olek=="mäng" and not paus:
                kuju_x_kiirus+=-kuju_baaskiirus
            if e.key==pygame.K_RIGHT and olek=="mäng" and not paus:
                kuju_x_kiirus+=kuju_baaskiirus
            if e.key==pygame.K_SPACE and olek=="mäng" and not paus:
                kuju_y_kiirus=-kuju_baaskiirus
        elif e.type==pygame.KEYUP:
            if e.key==pygame.K_LEFT and olek=="mäng" and not paus:
                kuju_x_kiirus-=-kuju_baaskiirus
            if e.key==pygame.K_RIGHT and olek=="mäng" and not paus:
                kuju_x_kiirus-=kuju_baaskiirus
            
                    
        if e.type==pygame_gui.UI_BUTTON_PRESSED:
            if e.ui_element==nupp1:
                teade_nähtav=True
                if teade_nähtav==True:
                    teade.show()
                    nupp2.show()
                    nupp1.hide()
               
            elif e.ui_element == nupp2:
                teade_nähtav = False
                if teade_nähtav==False:
                    teade.hide()
                    nupp2.hide()
                    nupp1.show()
            elif e.ui_element == nupp3:
                nupp4.show()
                nupp5.show()
            elif e.ui_element==nupp4:
                pygame.quit()
            elif e.ui_element==nupp5:
                nupp4.hide()
                nupp5.hide()
            elif e.ui_element==nupp6:
                    pygame.quit()
            elif e.ui_element==nupp7:
                olek="mäng"
                paus=False
                mine_mängu()
                
            
        
        
        
        elif e.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if e.ui_element == slider:
                    val = e.value
                    heli.set_volume(val / 100)  
                 

        manager.process_events(e)
    if olek=="mäng" and not paus:
        kuju_y_kiirus += gravitatsioon * dt 
        kuju_y += kuju_y_kiirus * dt
        kuju_x+=kuju_x_kiirus*dt
        if kuju_x>640:
            kuju_x=-kuju_w
        if kuju_x<-kuju_w:
            kuju_x=640
        if kuju_y>maapind:
            kuju_y=maapind
            kuju_y_kiirus=0
        
    
    
    ekraan.fill([255, 255, 255])
   
    if olek=="mäng" and kuju_x+kuju_w>640:
        ekraan.blit(kuju,[kuju_x,kuju_y])
    if olek=="mäng" and kuju_x+kuju_w<0:
        ekraan.blit(kuju,[kuju_x,kuju_y])
    if olek=="mäng":
        ekraan.blit(kuju,[kuju_x,kuju_y])
     if olek=="mäng" and paus:
        ekraan.blit(pealkiri, (250,200))
        
            

           

    manager.update(dt)
    manager.draw_ui(ekraan)
    pygame.display.flip()
pygame.quit()
          
                 



    




                
               
                    
            



