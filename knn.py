from tkinter import *

class Nokta:
    no_say = 1
    def __init__(self, x, y):
        self.no = Nokta.no_say
        self.x  = x
        self.y  = y

        Nokta.no_say += 1

    def reset(self):
        Nokta.no_say = 1
        
    def __repr__(self):
        return '%s:(%s,%s)' % (self.no,self.x,self.y)

class Kume:
    no_say = 1
    def __init__(self):
        self.no = Kume.no_say
        self.noktalar = []
        Kume.no_say += 1
        
    def reset(self):
        Kume.no_say = 1
        
    def __repr__(self):
        noktalari = '-'.join([str(n) for n in self.noktalar])
        return '%s:[%s]' % (self.no,noktalari)

        
            
class knn_hesap:
    def __init__(self):

        self.kume_adedi = 1
        
        self.noktalar  = []
        self.noktalar_arasi_mesafeler = {}
        self.kumeler = []
        self.kalan_noktalar = []
        
        #self.test_nokta_ekle()

        self.sonuclandi = False

        
        
    def test_nokta_ekle(self):
        for i in ((4,2), (6,4),(5,1), (10,6), (11,8)):
            self.noktalar.append(Nokta(i[0]*10, i[1]*10))
                                 
    def noktalara_nokta_ekle(self, x, y):
        nokta = Nokta(x,y)
        self.noktalar.append(nokta)
        return nokta.no
                             
        
    def kumelere_nokta_ekle(self, kume, nokta):
        kume.noktalar.append(nokta)
        self.kalan_noktalar.remove(nokta)
        
        
    def noktalar_arasi_mesafe_bul(self, nokta1, nokta2):
        mesafe = ((nokta1.x - nokta2.x)**2 + (nokta1.y - nokta2.y)**2) ** .5
        return mesafe

    def noktalar_arasi_mesafeler_bul(self, goster=False):
        self.noktalar_arasi_mesafeler = {}
        
        for n1 in self.noktalar:
            for n2 in [n for n in self.noktalar if n.no > n1.no]:
                mesafe = self.noktalar_arasi_mesafe_bul(n1,n2)
                key = n1.no, n2.no
                self.noktalar_arasi_mesafeler[key]= mesafe

                if goster:
                    print(key,'-->', mesafe)


    def iki_nokta_arasi_mesafe(self, nokta1, nokta2):
        key = min(nokta1.no, nokta2.no), max(nokta1.no, nokta2.no)
        mesafe = self.noktalar_arasi_mesafeler[key]
        return mesafe
    
    def kume_kume_mesafesi(self, kume1, kume2):
        lmesafeler = []
        for n in kume1.noktalar:
            for m in kume2.noktalar:
                mesafe = self.iki_nokta_arasi_mesafe(n, m)
                lmesafeler.append((mesafe,n,m))
        return min(lmesafeler,key=lambda x:x[0])

    def kume_nokta_mesafesi(self, kume, nokta):
        lmesafeler = []
        for n in kume.noktalar:
            mesafe = self.iki_nokta_arasi_mesafe(n, nokta)
            lmesafeler.append((mesafe, n, nokta))
        return min(lmesafeler, key = lambda x:x[0])

    def nokta_nokta_mesafesi(self, nokta1, nokta2):
        mesafe = self.iki_nokta_arasi_mesafe(nokta1, nokta2)
        return (mesafe, nokta1, nokta2)
                

    def mesafeleri_bul(self):
        #noktalar arası mesafeleri biliyoruz. self.noktalar_arasi_mesafeler sözlüğünede
        #küçük nokta.no, büyük nokta.no key'i saklı.

        lmesafeler = {}
        #Kümelerle kümeler arasındaki mesafeler bulunup,'K'+küme.no - 'K'+küme.no keyi ile saklayalım
        for k1 in self.kumeler:
            for k2 in [k for k in self.kumeler if k.no > k1.no]:
                mesafe = self.kume_kume_mesafesi(k1,k2)
                key = 'K%s-K%s' % (k1.no, k2.no)
                lmesafeler[key] = mesafe
            
        # Kümeler ile noktalar arasındaki mesafeleri 'K'+küme.no - 'N'+nokta.no keyi ile saklayalım.
        for k in self.kumeler:
            for n in self.kalan_noktalar:
                mesafe = self.kume_nokta_mesafesi(k,n)
                key = 'K%s-N%s' % (k.no, n.no)
                lmesafeler[key] = mesafe

        # Noktalar ile Noktalar arası mesafeleri 'N'+nokta.no - 'N'+nokta.no keyi ile saklayalım.
        for n1 in self.kalan_noktalar:
            for n2 in [n for n in self.kalan_noktalar if n.no > n1.no]:
                mesafe = self.nokta_nokta_mesafesi(n1,n2)
                key = 'N%s-N%s' % (n1.no, n2.no)
                lmesafeler[key] = mesafe

        #minimum value'u bulup, key'i bulalım
        min_val = min(lmesafeler.values(), key=lambda x:x[0])
        for k,v in lmesafeler.items():
            if v[0] == min_val[0]:
                break

        #print('Key:',k,'Min_Val:',min_val, 'value:', v)
        mesaj = 'En kısa mesafe %s arasında olup, %7.2f dır' % (k, min_val[0])
        
        # Key : Nx-Ny şeklindeyse, bu iki nokta için bir küme oluşturulup, Nx, Ny kalan noktalardan silinecek.
        if k.count('N') == 2:
            kume = Kume()
            self.kumeler.append(kume)
            self.kumelere_nokta_ekle(kume, v[1])
            self.kumelere_nokta_ekle(kume, v[2])
        
        # Key : Kx-Ny şeklindeyse, Ny noktası Kx kümesine eklenecek, Ny silinecek
        if k.count('K') == 1:
            kume_adi = k.partition('-')[0]
            kume_no = int(kume_adi[1:])
            #print()
            #print('kume_adi:',kume_adi, 'kume_no:', kume_no)
            for kume in self.kumeler:
                if kume.no == kume_no:
                    self.kumelere_nokta_ekle(kume, v[2])
                    break
        
        # Key : Kx-Ky şeklindeyse, Kx kümesine Ky kümesi eklenecek ve Ky kümesi kümelerden silinecek.
        if k.count('K') == 2:
            k1 = k.partition('-')[0]
            k1_no = int(k1[1:])
            k2 = k.partition('-')[2]
            k2_no = int(k2[1:])
            for kume in self.kumeler:
                if kume.no == k1_no:
                    kume1 = kume
                    break
            for kume in self.kumeler:
                if kume.no == k2_no:
                    kume2 = kume
                    break

            for n in kume2.noktalar:
                kume1.noktalar.append(n)

            self.kumeler.remove(kume2)

        return mesaj, min_val
        
    def kume_temizlik(self):
        self.kumeler =[]
        k=Kume()
        k.reset()

    def tum_temizlik(self):
        self.kume_temizlik()
        self.noktalar = []
        n= Nokta(0,0)
        n.reset()
        
    def hesaba_basla(self):
        self.kalan_noktalar = self.noktalar[:]
        self.noktalar_arasi_mesafeler_bul(goster=False)

        
    def hesaba_devam(self):
        toplamkume = len(self.kalan_noktalar) + len(self.kumeler)
        if toplamkume == self.kume_adedi:
            self.sonuclandi = True
            mesaj = 'Döngü tamamlandı'
            min_val = ''
        else:
            mesaj, min_val = self.mesafeleri_bul()

            #print('kalan noktalar:',self.kalan_noktalar)
            #print('kumeler:', self.kumeler)
            #print('Min_Val inceleme')

            n1=min_val[1]

            #print('Nokta1:%s x:%s, y:%s' % (n1.no, n1.x, n1.y))

            n1=min_val[2]

            #print('Nokta2:%s x:%s, y:%s' % (n1.no, n1.x, n1.y))
            #print()
            
            
        return mesaj, min_val        
    
        

class Cizim(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        
        self.canvas_width = 500
        self.canvas_height =500

        self.knn = knn_hesap()
        
        self.renk0 = "#476042"

        self.kume_adedi = self.knn.kume_adedi

        self.canvas_noktalar = []
        self.canvas_textler = []
        self.canvas_line = []

        self.alanlariYap()
        
    def kume_temizlik(self):
        self.knn.kume_temizlik()
        for l in self.canvas_line:
            self.w.delete(l)
        self.canvas_line = []

    def tum_temizlik(self):
        self.knn.tum_temizlik()
        self.kume_temizlik()

        for n in self.canvas_noktalar:
            self.w.delete(n)
        self.canvas_noktalar = []
        
        for t in self.canvas_textler:
            self.w.delete(t)
        self.canvas_textler = []
        
    def stateler(self, stateno):
        if stateno == 1:
            #nokta girişleri
            self.tuslar['Hesaba Başla']['state']='normal'
            self.tuslar['Hesaba Devam']['state']='disabled'
            self.chk1['state'] = 'normal'
            self.chkvar1.set(1)
            self.ent_kume_adedi['state'] = 'normal'
            self.tuslar['Kümeleri Temizle']['state']='normal'
            self.tuslar['Herşeyi Temizle']['state']='normal'            
        elif stateno == 2:
            self.tuslar['Hesaba Başla']['state']='disabled'
            self.tuslar['Hesaba Devam']['state']='normal'
            self.chk1['state'] = 'disabled'
            self.chkvar1.set(0)
            self.ent_kume_adedi['state'] = 'disabled'
            self.tuslar['Kümeleri Temizle']['state']='disabled'
            self.tuslar['Herşeyi Temizle']['state']='disabled'
            
            
    def hesaba_basla(self):
        self.knn.kume_adedi = int(self.ent_kume_adedi.get())
        if self.knn.kume_adedi >= len(self.knn.noktalar):
            mesaj = 'HATA:Küme sayısı nokta sayısından az olamaz'
            self.mesaj_bas(mesaj, renk='red')
        else:
            self.kume_temizlik()
            self.stateler(2)
            
            # Şu kadar adet nokta ile hesaba başlandı mesajı verilecek.
            mesaj = '%s adet nokta ile hesaba başlandı.' % len(self.knn.noktalar)
            self.mesaj_bas(mesaj)
            
            self.knn.hesaba_basla()

    def hesaba_devam(self):
        mesaj, min_val = self.knn.hesaba_devam()
        self.mesaj_bas(mesaj)
        if min_val:
            #iki nokta arasına line cizilecek
            self.cizgi_ciz(min_val[1], min_val[2])
        else:
            self.stateler(1)

        
    def mesaj_bas(self, mesaj,renk = 'blue'):
        self.bilgi.config(text=mesaj, fg=renk)

    def cizgi_ciz(self, nokta1, nokta2):
        l = self.w.create_line(nokta1.x, nokta1.y, nokta2.x, nokta2.y, fill=self.renk0,width=3)
        self.canvas_line.append(l)
        
    def alanlariYap(self):
        
        self.master.title( "K - En Yakın Komşu Algoritması" )

        #Tuşlar için frame
        frmTus = Frame(self, width = 250,
                       height = self.canvas_height, bd=3,
                       relief = RAISED)
        frmTus.pack(side=LEFT, expand=YES, fill = BOTH)
        
        #Checkbox
        self.chkvar1 = IntVar()
        self.chkvar1.set(1)
        self.chk1 = Checkbutton(frmTus,text= 'Nokta Oluştur', variable=self.chkvar1)
        self.chk1.grid(row=0, sticky=W,padx=15)
        
        
        #Butonlar
        tus_bilgi = (
                     ('Hesaba Başla', self.hesaba_basla,'normal'),
                     ('Hesaba Devam', self.hesaba_devam,'disabled'),
                     ('Kümeleri Temizle', self.kume_temizlik, 'normal'),
                     ('Herşeyi Temizle', self.tum_temizlik, 'normal'),
                     ('Çıkış', self.quit,'normal'),
                      )

        self.tuslar = {}
  
        row=1
        for text, metot, durum in tus_bilgi:
            b = Button(frmTus, text = text, command = metot, state=durum, width=15)
            b.grid(row =row,sticky=W, padx=15, pady=5)
            row += 1
            self.tuslar[text] = b
            

        # Küme sayısı için Entry oluştur
        lab = Label(frmTus, text='Küme Sayısı', width=15)
        ent = Entry(frmTus, justify=CENTER, bd=3, width=15)
        ent.insert(0, self.kume_adedi)
        lab.grid(row=row, sticky=W, padx=15)
        ent.grid(row = row+1, sticky=W, padx=15)
        self.ent_kume_adedi = ent
        
        # Bilgi label'i
        l = Label(self, text='Bilgi: ', fg='red', bd=4, relief=RAISED)
        l.pack(side=TOP, fill=X)
        self.bilgi = l

        #Canvas
        self.w = Canvas(self, width = self.canvas_width,
                        height = self.canvas_height)
        self.w.pack(expand=YES, fill = BOTH)
        self.w.bind("<Button-1>", self.paint)
        
        
    def paint(self, event):
        if self.chkvar1.get():
            x1, y1 = ( event.x - 3 ), ( event.y - 3 )
            x2, y2 = ( event.x + 3 ), ( event.y + 3 )
            n=self.w.create_oval( x1, y1, x2, y2, fill = self.renk0 )
            no = self.knn.noktalara_nokta_ekle(event.x, event.y)
            t=self.w.create_text(event.x, y2+10,text=no)
            self.canvas_noktalar.append(n)
            self.canvas_textler.append(t)
            


if __name__ == '__main__':

    czm = Cizim()
    czm.mainloop()
