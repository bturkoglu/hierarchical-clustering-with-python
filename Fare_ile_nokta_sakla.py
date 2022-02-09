from tkinter import *

class Noktalar:
    no = 1
    def __init__(self):
        self.noktalar={}
        self.mesafeler = {}
        
    def nokta_ekle(self, x, y):
        self.noktalar[Noktalar.no] = (x,y)
        Noktalar.no +=1

    def mesafe_bul(self, nokta1, nokta2):
        mesafe = ((nokta1.x - nokta2.x)**2 + (nokta1.y - nokta2.y)**2) ** .5
        return mesafe

    def mesafeler(self):
        for n1 in noktalar:
            for n2 in [n for n in noktalar if n.no > n1.no]:
                mesafe = self.mesafe_bul(n1,n2)
                self.mesafeler[n1.n0, n2.no]= mesafe
                
            
        
        

class Cizim:
    def __init__(self):
        self.canvas_width = 500
        self.canvas_height =500
        self.nk = Noktalar()
        self.renk0 = "#476042"

        self.alanlariYap()
        

    def alanlariYap(self):
        self.master = Tk()
        self.master.title( "K - En Yakın Komşu Algoritması" )
        #Tuşlar için frame
        self.f = Frame(self.master, width = 150,
                       height = self.canvas_height, bd=3,
                       relief = RAISED)
        self.f.pack(side=LEFT, fill = BOTH)
        
        #Checkbox
        self.chkvar1 = IntVar()
        Checkbutton(self.f,text= 'Nokta Oluştur', variable=self.chkvar1).grid(row=0, sticky=W)
        
        #Canvas
        self.w = Canvas(self.master, width = self.canvas_width,
                        height = self.canvas_height)
        self.w.pack(expand=YES, fill = BOTH)
        self.w.bind("<Button-1>", self.paint)
        
        
    def paint(self, event):
        if self.chkvar1.get():
            x1, y1 = ( event.x - 3 ), ( event.y - 3 )
            x2, y2 = ( event.x + 3 ), ( event.y + 3 )
            self.w.create_oval( x1, y1, x2, y2, fill = self.renk0 )
            self.nk.nokta_ekle(event.x, event.y)
    


if __name__ == '__main__':

    czm = Cizim()
    czm.master.mainloop()
