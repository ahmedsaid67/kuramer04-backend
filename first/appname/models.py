import os
from django.db import models
from datetime import datetime



def get_image_path(instance, filename):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return os.path.join('sliders/', f'{timestamp}_{filename}')


class Slider(models.Model):
    name = models.CharField(max_length=200)
    img = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Menu (models.Model):
    title = models.CharField(max_length=255)
    selected = models.BooleanField(default=False)

class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255,blank=True,null=True)
    order = models.PositiveIntegerField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True,null=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    is_disabled = models.BooleanField(default=False)



class PersonelTuru(models.Model):
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


import uuid


def personel_fotograf_path(instance, filename):
    # Dosya uzantısını al (örn: .jpg, .png)
    ext = filename.split('.')[-1]
    # Benzersiz bir dosya ismi oluştur
    filename = f"{uuid.uuid4()}.{ext}"
    # 'media/personel/' altında bu dosyayı sakla
    return f'personel/{filename}'


class Persons(models.Model):
    ad = models.CharField(max_length=100)
    soyad = models.CharField(max_length=100)
    unvan= models.CharField(max_length=100,null=True, blank=True)
    personel_turu = models.ForeignKey(PersonelTuru, on_delete=models.CASCADE,null=True, blank=True)
    img = models.ImageField(upload_to=personel_fotograf_path, default='defaults/defaultprofilephoto.jpeg')
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.ad} {self.soyad}"



## YAYINLAR
## -BROŞÜRLER


def kapakfoto_path(instance, filename):
    # Dosya uzantısını al (örn: .jpg, .png)
    ext = filename.split('.')[-1]
    # Benzersiz bir dosya ismi oluştur
    filename = f"{uuid.uuid4()}.{ext}"
    # 'media/kapakfoto/' altında bu dosyayı sakla
    return f'brosurler/kapakfoto/{filename}'

def pdf_dosya_path(instance, filename):
    # Dosya uzantısını al (örn: .pdf)
    ext = filename.split('.')[-1]
    # Benzersiz bir dosya ismi oluştur
    filename = f"{uuid.uuid4()}.{ext}"
    # 'media/pdf_dosyalar/' altında bu dosyayı sakla
    return f'brosurler/pdf_dosyalar/{filename}'
class Brosurler(models.Model):
    baslik = models.TextField()
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path, blank=True, null=True)
    pdf_dosya = models.FileField(upload_to=pdf_dosya_path, blank=True, null=True)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.baslik


def kapakfoto_path_bultenler(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'bultenler/kapakfoto/{filename}'

def pdf_dosya_path_bultenler(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    return f'bultenler/pdf_dosyalar/{filename}'
class Bultenler(models.Model):
    baslik = models.TextField()
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_bultenler, blank=True, null=True)
    pdf_dosya = models.FileField(upload_to=pdf_dosya_path_bultenler, blank=True, null=True)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.baslik













## TEMEL KONU VE KAVRAMLAR
## TEMEL KONULAR


def kapakfoto_path_temelkonular(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'temelkonular/kapakfoto/{filename}'

def pdf_dosya_path_temelkonular(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    return f'temelkonular/pdf_dosyalar/{filename}'
class Temelkonular(models.Model):
    baslik = models.TextField()
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_temelkonular, blank=True, null=True)
    pdf_dosya = models.FileField(upload_to=pdf_dosya_path_temelkonular, blank=True, null=True)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.baslik



## TEMEL KAVRAMLAR


def kapakfoto_path_temelkavramlar(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'temelkavramlar/kapakfoto/{filename}'

def pdf_dosya_path_temelkavramlar(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    return f'temelkavramlar/pdf_dosyalar/{filename}'
class Temelkavramlar(models.Model):
    baslik = models.TextField()
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_temelkavramlar, blank=True, null=True)
    pdf_dosya = models.FileField(upload_to=pdf_dosya_path_temelkavramlar, blank=True, null=True)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.baslik











###### YAYINLARIMIZDAN SEÇMELER


def kapakfoto_path_yayinlarimizdansecmeler(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'yayinlarimizdansecmeler/kapakfoto/{filename}'

def pdf_dosya_path_yayinlarimizdansecmeler(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    return f'yayinlarimizdansecmeler/pdf_dosyalar/{filename}'
class YayinlarimizdanSecmeler(models.Model):
    baslik = models.TextField()
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_yayinlarimizdansecmeler, blank=True, null=True)
    pdf_dosya = models.FileField(upload_to=pdf_dosya_path_yayinlarimizdansecmeler, blank=True, null=True)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.baslik







### BASINDA BİZ


# YAZILI BASIN


def kapakfoto_path_yazilibasin(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'yazilibasin/kapakfoto/{filename}'


class YaziliBasin(models.Model):
    baslik = models.TextField()
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_yazilibasin, blank=True, null=True)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)



# GORSEL BASIN


def kapakfoto_path_gorselbasin(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'gorselbasin/kapakfoto/{filename}'


class GorselBasin(models.Model):
    baslik = models.TextField()
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_gorselbasin, blank=True, null=True)
    url = models.URLField(max_length=500)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)






### KAMUOYU DUYURULARI


def kapakfoto_path_kamuoyuduyurulari(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'kamuoyuduyurulari/kapakfoto/{filename}'


class KamuoyuDuyurulari(models.Model):
    baslik = models.TextField()
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_kamuoyuduyurulari, blank=True, null=True)
    tarih = models.DateField()
    durum = models.BooleanField(default=True)
    icerik=models.TextField()
    is_removed = models.BooleanField(default=False)










#### MÜSHAFLAR

# MÜSHAF KATEGORİ

class MushafKategori(models.Model):
    baslik=models.CharField(max_length=200)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)



# MÜSHAFLAR


def kapakfoto_path_mushaflar(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'mushaflar/kapakfoto/{filename}'

def pdf_dosya_path_mushaflar(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'mushaflar/pdf_dosyalar/{filename}'


class Mushaflar(models.Model):
    baslik=models.CharField(max_length=200)
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_mushaflar, blank=True, null=True)
    pdf_dosya = models.FileField(upload_to=pdf_dosya_path_mushaflar, blank=True, null=True)
    mushaf_kategori=models.ForeignKey(MushafKategori,on_delete=models.CASCADE,null=True, blank=True)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)
