import pygame
import pygame_gui
pygame.init()
#***üldine***
ekraan = pygame.display.set_mode([640, 480])
manager = pygame_gui.UIManager([640, 480])
pygame.display.set_caption("mäng")
#***elemendid mõistatuse jaoks***
sisu = pygame_gui.elements.UITextBox("""Mis aastal ehitati see kindlus?
(Vihje leiad siit toast)

a - 2025
b - 1918
c - 1761""", pygame.Rect((120, 80), (400, 240)), manager)
a = pygame_gui.elements.UIButton(pygame.Rect((170, 320), (100, 40)), 'a',manager)
b = pygame_gui.elements.UIButton(pygame.Rect((270, 320), (100, 40)), 'b',manager)
c = pygame_gui.elements.UIButton(pygame.Rect((370, 320), (100, 40)), 'c',manager)
raamat = pygame_gui.elements.UIButton(pygame.Rect((272, 268), (223, 40)), 'Raamat',manager)
sulge = pygame_gui.elements.UIButton(pygame.Rect((516, 80), (40, 40)), 'X ',manager)
taust2 = pygame.image.load("ruum.png")
halb = pygame.image.load("halb_lopp.png")
hea=pygame.image.load("hea_lopp.png")
töötab = True
lohistamas = False
sisu.hide()
sulge.hide()
a.hide()
b.hide()
c.hide()
#elemendid võitlusmängu jaoks
hüppab = False
max_hüppe_aeg = 0.25   
hüppe_aeg = 0
hüppe_jõud = 1200
mängija_max_elu = 10
mängija_elu = mängija_max_elu
heli = pygame.mixer.Sound("tp3.wav")
heli2=pygame.mixer.Sound("woosh.wav")
heli.set_volume(0.2)
heli2.set_volume(0.2)
kanal=pygame.mixer.Channel(0)
kell = pygame.time.Clock()
#***pildid***
kuju=pygame.image.load("tegelane.png")
taust1=pygame.image.load("voitlus_taust.png")
rünnak=pygame.image.load("rünnak.png")
halb_lõpp=pygame.image.load("halb_lopp.png")
rünnak_vasak=pygame.transform.flip(rünnak,True,False)
koll=pygame.image.load("roheline_koll.png")
luukere=pygame.image.load("luukere.png")
koll_parem = pygame.image.load("roheline_koll.png")
koll_vasak = pygame.transform.flip(koll_parem, True, False)
rünnaku_cooldown = 0.3
rünnaku_timer = 0
luukere_parem = pygame.image.load("luukere.png")
luukere_vasak = pygame.transform.flip(luukere_parem, True, False)
LEVELI_LÕPP = 3000
#***tegelase füüsika***
taust_w = taust1.get_width()
kaamera_x=0
kuju_x=0
maapind=300
kuju_x_kiirus=0
kuju_y_kiirus=0
kuju_w=kuju.get_width()
kuju_h=kuju.get_height()
gravitatsioon=980
kuju_baaskiirus=400
kuju_y=maapind
praegune_tegelase_pilt=kuju
rünnak_olek=False
#***vaenlase klass***
class Vaenlane:
    def __init__(self, x, y, sprite_parem, sprite_vasak,max_elu=3):#omadused
        self.sprite_parem = sprite_parem
        self.sprite_vasak = sprite_vasak
        self.sprite = sprite_parem

        self.rect = pygame.Rect(
            x, y,
            sprite_parem.get_width(),
            sprite_parem.get_height()
        )

        self.kiirus = 80
        self.suund = 1

        self.max_elu = max_elu
        self.elu = self.max_elu
        self.elus = True

        self.algus_x = x
        self.patrulli_vahe = 120
        self.ründe_ulatus = 0
        self.ründe_cooldown = 4
        self.ründe_timer = 0

    def update(self, dt,mängija_rect):#liigub edasi-tagasi
        if not self.elus:
            return

        self.rect.x += self.suund * self.kiirus * dt

        if abs(self.rect.x - self.algus_x) > self.patrulli_vahe:
            self.suund *= -1

        self.sprite = self.sprite_parem if self.suund == 1 else self.sprite_vasak
        self.ründe_timer -= dt
        if self.rect.colliderect(mängija_rect) and self.ründe_timer <= 0:
            self.ründe_timer = self.ründe_cooldown
            return True   

        return False

    def saa_viga(self, kogus=1):#saab viga
        if not self.elus:
            return

        self.elu -= kogus
        if self.elu <= 0:
            self.elus = False

    def draw(self, ekraan, kaamera_x):#elud
        if not self.elus:
            return

        ekraan.blit(
            self.sprite,
            (self.rect.x - kaamera_x, self.rect.y)
        )

        
        riba_laius = self.rect.w
        riba_korgus = 6
        elu_suhe = self.elu / self.max_elu

        pygame.draw.rect(
            ekraan, (255, 0, 0),
            (self.rect.x - kaamera_x, self.rect.y - 10, riba_laius, riba_korgus)
        )
        pygame.draw.rect(
            ekraan, (0, 255, 0),
            (self.rect.x - kaamera_x, self.rect.y - 10, riba_laius * elu_suhe, riba_korgus)
        )

#***vaenlaste list***            
vaenlased = [
    Vaenlane(500, maapind, koll_parem, koll_vasak),
    Vaenlane(900, maapind, luukere_parem, luukere_vasak,max_elu=1),
    Vaenlane(1300, maapind, koll_parem, koll_vasak),
    Vaenlane(2000, maapind, koll_parem, koll_vasak,max_elu=5),
    Vaenlane(2600, maapind, luukere_parem, luukere_vasak,max_elu=1),
    Vaenlane(2700, maapind, luukere_parem, luukere_vasak,max_elu=2),
    Vaenlane(2500, maapind, luukere_parem, luukere_vasak,max_elu=3),
    Vaenlane(2000, maapind, koll_parem, koll_vasak,max_elu=5)]

#***mõned elemendid veel***
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

teade=pygame_gui.elements.UITextBox("Autorid:Holger,Lola,Eno",((420, 80), (460, 150)),manager)
#***siin peidan kõik ui elemendid ära***
raamat.hide()
slider.hide()
nupp1.hide()
nupp2.hide()
teade.hide()
nupp3.hide()
nupp4.hide()
nupp5.hide()
def mine_pausi():
    slider.show()
    kanal.pause()
    nupp1.show()
    nupp3.show()
    pygame.mixer.music.pause()
    if olek != "mäng":
        return
    slider.show()
    kanal.pause()
    nupp1.show()
    nupp3.show()
    
def lahku_pausist():
    slider.hide()
    kanal.unpause()
    nupp1.hide()
    nupp3.hide()
    nupp4.hide()
    nupp5.hide()
    teade.hide()
    nupp2.hide()
    slider.hide()
    kanal.unpause()
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
    kanal.play(heli)
#***mängu tsükkel***
while mäng_töötab:
    
    dt = kell.tick(60) / 1000
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            mäng_töötab = False
       
#liikumine ja pausimenüü
        if e.type == pygame.KEYDOWN:
            
            if e.key==pygame.K_ESCAPE and olek=="mäng" or e.key==pygame.K_ESCAPE and olek=="mõistatus":
                paus= not paus 
                if paus:
                    mine_pausi()
                else:
                    lahku_pausist()
            
            if e.key==pygame.K_LEFT and olek=="mäng" and not paus:
                kuju_x_kiirus+=-kuju_baaskiirus
            if e.key==pygame.K_RIGHT and olek=="mäng" and not paus:
                kuju_x_kiirus+=kuju_baaskiirus
            if e.key==pygame.K_SPACE and olek=="mäng" and not paus and on_ground:
                kuju_y_kiirus=-kuju_baaskiirus
                on_ground=False
                hüppe_aeg = 0
                hüppab=True
            if e.key == pygame.K_z and olek == "mäng" and not paus:
                rünnak_olek = True
                heli2.play()
                
            
#liikumine                
                
        elif e.type==pygame.KEYUP:
            if e.key==pygame.K_LEFT and olek=="mäng" and not paus:
                kuju_x_kiirus-=-kuju_baaskiirus
            if e.key==pygame.K_RIGHT and olek=="mäng" and not paus:
                kuju_x_kiirus-=kuju_baaskiirus
            if e.key == pygame.K_SPACE:
                hüppab = False
            if e.key == pygame.K_z:
                rünnak_olek = False
        if rünnak_olek==True:
            praegune_tegelase_pilt = rünnak
        else:
            praegune_tegelase_pilt = kuju
        rünnaku_timer -= dt
#gui nupud    
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
            if e.ui_element == raamat:
                sisu.show()
                sulge.show()
                a.show()
                b.show()
                c.show()
                raamat.hide()
            elif e.ui_element == sulge:
                sisu.hide()
                sulge.hide()
                a.hide()
                b.hide()
                c.hide()
            if e.ui_element == a or e.ui_element == b:
                sisu.hide()
                sulge.hide()
                a.hide()
                b.hide()
                c.hide()
                raamat.hide()
                olek="kaotus"
            elif e.ui_element == c:
                print("yippe")
                olek="võit"
                
            
        
        
        
        elif e.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if e.ui_element == slider:
                    val = e.value
                    heli.set_volume(val / 100)  
                 

        manager.process_events(e)
    if olek=="mäng" and not paus:
        
        
        klahvid = pygame.key.get_pressed()

        kuju_x_kiirus = 0
        
        if klahvid[pygame.K_LEFT]:
            kuju_x_kiirus -= kuju_baaskiirus
        if klahvid[pygame.K_RIGHT]:
            kuju_x_kiirus += kuju_baaskiirus
        mängija_rect = pygame.Rect(kuju_x, kuju_y, kuju_w, kuju_h)
        #mängija elud
        for v in vaenlased:
            lõi = v.update(dt, mängija_rect)
            if lõi:
               mängija_elu -= 1
               print("Mängija sai viga! Elu:", mängija_elu)

               if mängija_elu <= 0:
                   olek="kaotus"
        for i in range(mängija_elu):
            pygame.draw.rect(ekraan, (255, 0, 0), (10 + i*25, 10, 20, 20))
            
        
        
#mängija füüsika 2
        kuju_y_kiirus += gravitatsioon * dt 
        kuju_y += kuju_y_kiirus * dt
        kuju_x+=kuju_x_kiirus*dt
        if kuju_x < 0:
            kuju_x = 0
        if hüppab:
            hüppe_aeg += dt
            if hüppe_aeg < max_hüppe_aeg:
                kuju_y_kiirus -= hüppe_jõud * dt
            else:
                hüppab = False
        if rünnak_olek:
            ründe_rect = pygame.Rect(
                kuju_x + kuju_w,kuju_y,40,kuju_h)
        rünnaku_timer -= dt
#ründamine
        if rünnak_olek and rünnaku_timer <= 0:
            rünnaku_timer = rünnaku_cooldown
            for v in vaenlased:
                if v.elus and ründe_rect.colliderect(v.rect):
                    v.saa_viga(1)


        
        

        
        if kuju_y>maapind:
            kuju_y=maapind
            kuju_y_kiirus=0
            on_ground=True
        else:
            on_ground=False
        
        SIHT = kuju_x - 320

        if SIHT > 0:
           kaamera_x += (SIHT - kaamera_x) * 0.1
        else:
           kaamera_x = 0
        if kuju_x >= LEVELI_LÕPP:
            olek = "mõistatus"
            if olek == "mõistatus":
                ekraan.blit(taust2, [0, 0])
                raamat.show()
                
                


        
    
    
    
    
    if olek=="mäng" and kuju_x+kuju_w>640:
        ekraan.blit(kuju,[kuju_x,kuju_y])
    if olek=="mäng" and kuju_x+kuju_w<0:
        ekraan.blit(kuju,[kuju_x,kuju_y])
    if olek=="mäng":
        taust_x = int(-kaamera_x % taust_w)
        ekraan.blit(taust1, (taust_x - taust_w, 0))
        ekraan.blit(taust1, (taust_x, 0))
        ekraan.blit(taust1, (taust_x + taust_w, 0))
        ekraan.blit(praegune_tegelase_pilt, (kuju_x - kaamera_x, kuju_y))
    
        
        
 #olekud, kaotus ja lõpp   
    if olek == "mäng":
        for v in vaenlased:
            v.draw(ekraan, kaamera_x)
    if olek=="mäng" and paus:
        ekraan.blit(pealkiri, (0,0))
    if olek=="menüü":
        ekraan.blit(pealkiri, (0,0))
    
    if olek=="kaotus":
        ekraan.blit(halb_lõpp,(0,0))
        nupp6.show()
    if olek=="võit":
        ekraan.blit(hea,(0,0))
        nupp6.show()
        sisu.hide()
    if olek == "mõistatus":
        ekraan.blit(taust2, (0, 0))
        raamat.show()
    if olek=="mõistatus" and paus:
        ekraan.blit(pealkiri,(0,0))
        raamat.hide()

     
    
        
            

           

    manager.update(dt)
    manager.draw_ui(ekraan)
    pygame.display.flip()
pygame.quit()
 



    




                
               
                    
            







