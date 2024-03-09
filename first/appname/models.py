import os
from django.db import models
from datetime import datetime
from django.utils.text import slugify


def slider_path(instance, filename):
    # Dosya uzantısını al (örn: .jpg, .png)
    ext = filename.split('.')[-1]
    # Benzersiz bir dosya ismi oluştur
    filename = f"{uuid.uuid4()}.{ext}"
    # 'media/personel/' altında bu dosyayı sakla
    return f'slider/{filename}'


class Sliders(models.Model):
    name = models.CharField(max_length=200)
    img = models.ImageField(upload_to=slider_path, blank=True, null=True)
    url = models.URLField(max_length=500)
    order = models.IntegerField()
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)

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
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)



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
    baslik = models.CharField(max_length=200)
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
    baslik = models.CharField(max_length=200)
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
    baslik = models.CharField(max_length=200)
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
    baslik = models.CharField(max_length=200)
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
    baslik = models.CharField(max_length=200)
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
    baslik = models.CharField(max_length=200)
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_yazilibasin, blank=True, null=True)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)



# GORSEL BASIN


def kapakfoto_path_gorselbasin(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'gorselbasin/kapakfoto/{filename}'


class GorselBasin(models.Model):
    baslik = models.CharField(max_length=200)
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_gorselbasin, blank=True, null=True)
    url = models.URLField(max_length=500)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)






### KAMUOYU DUYURULARI

def pdf_dosya_path_kamuoyuduyurulari(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'kamuoyuduyurulari/pdf_dosyalar/{filename}'


def kapakfoto_path_kamuoyuduyurulari(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'kamuoyuduyurulari/kapakfoto/{filename}'


class KamuoyuDuyurulari(models.Model):
    baslik = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_kamuoyuduyurulari, blank=True, null=True)
    tarih = models.DateField()
    durum = models.BooleanField(default=True)
    pdf_dosya = models.FileField(upload_to=pdf_dosya_path_kamuoyuduyurulari, blank=True, null=True)
    is_removed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Eğer slug boşsa ve bu yeni bir nesne ise
        if not self.id and not self.slug:
            # Önce nesneyi veritabanına kaydet (bu, bir id atar)
            super(KamuoyuDuyurulari, self).save(*args, **kwargs)
            # Slug alanını oluştur
            self.slug = slugify(f"{self.baslik}-{self.id}")
            # save() metodunu tekrar çağırarak slug'ı kaydet
            kwargs.pop('force_insert', None)  # force_insert argümanını kaldır
            super(KamuoyuDuyurulari, self).save(*args, **kwargs)
        else:
            super(KamuoyuDuyurulari, self).save(*args, **kwargs)






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



## MUSHAF FARKLARI


def kapakfoto_path_mushaffarklari(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'mushaffarklari/kapakfoto/{filename}'

def pdf_dosya_path_mushaffarklari(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    return f'mushaffarklari/pdf_dosyalar/{filename}'
class Mushaffarklari(models.Model):
    baslik = models.CharField(max_length=200)
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_mushaffarklari, blank=True, null=True)
    pdf_dosya = models.FileField(upload_to=pdf_dosya_path_mushaffarklari, blank=True, null=True)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.baslik




## KİTAP KATEGORİ


def kapakfoto_path_kitapkategori(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'kitapkategori/kapakfoto/{filename}'

class KitapKategori(models.Model):
    baslik = models.CharField(max_length=200)
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_kitapkategori, blank=True, null=True)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.baslik


# KİTAPLAR



def kapakfoto_path_kitaplar(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'kitaplar/kapakfoto/{filename}'


class Kitap(models.Model):
    ad=models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    yazar=models.CharField(max_length=200)
    yayin_tarihi = models.DateField()
    sayfa_sayisi=models.IntegerField(default=0)
    isbn = models.CharField(max_length=50)
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_kitaplar, blank=True, null=True)
    ozet=models.TextField()
    kitap_kategori=models.ForeignKey(KitapKategori,on_delete=models.CASCADE,null=True, blank=True)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Eğer slug boşsa ve bu yeni bir nesne ise
        if not self.id and not self.slug:
            # Önce nesneyi veritabanına kaydet (bu, bir id atar)
            super(Kitap, self).save(*args, **kwargs)
            # Slug alanını oluştur
            self.slug = slugify(f"{self.ad}-{self.id}")
            # save() metodunu tekrar çağırarak slug'ı kaydet
            kwargs.pop('force_insert', None)  # force_insert argümanını kaldır
            super(Kitap, self).save(*args, **kwargs)
        else:
            super(Kitap, self).save(*args, **kwargs)



## MEDYA GALERİ

# VIDEO GALERİ KATEGORİ



def kapakfoto_path_videogalerikategori(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'videogalerikategori/kapakfoto/{filename}'

class VideoGaleriKategori(models.Model):
    baslik = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_videogalerikategori, blank=True, null=True)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.baslik

    def save(self, *args, **kwargs):
        # Eğer slug boşsa ve bu yeni bir nesne ise
        if not self.id and not self.slug:
            # Önce nesneyi veritabanına kaydet (bu, bir id atar)
            super(VideoGaleriKategori, self).save(*args, **kwargs)
            # Slug alanını oluştur
            self.slug = slugify(f"{self.baslik}-{self.id}")
            # save() metodunu tekrar çağırarak slug'ı kaydet
            kwargs.pop('force_insert', None)  # force_insert argümanını kaldır
            super(VideoGaleriKategori, self).save(*args, **kwargs)
        else:
            super(VideoGaleriKategori, self).save(*args, **kwargs)






# VİDEO GALERİ


import re
import requests
import PIL
from io import BytesIO
from django.core.files.base import ContentFile


def kapakfoto_path_videogaleri(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'videogaleri/kapakfoto/{filename}'

class VideoGaleri01(models.Model):
    baslik = models.CharField(max_length=200)
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_videogaleri, blank=True, null=True)
    videogaleri_kategori=models.ForeignKey(VideoGaleriKategori,on_delete=models.CASCADE,null=True, blank=True)
    url = models.URLField(max_length=500)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.url and not self.kapak_fotografi:
            # YouTube video ID'sini URL'den çıkar
            youtube_id_match = re.search(r'v=([0-9A-Za-z_-]{11})', self.url)
            youtube_id_match = youtube_id_match or re.search(r'be/([0-9A-Za-z_-]{11})', self.url)
            if youtube_id_match:
                video_id = youtube_id_match.group(1)
                image_url = f'https://img.youtube.com/vi/{video_id}/mqdefault.jpg'
                response = requests.get(image_url)

                if response.status_code == 200:
                    # Resmi Pillow ile aç
                    image = PIL.Image.open(BytesIO(response.content))
                    image_io = BytesIO()
                    image.save(image_io, format='JPEG')

                    # Resmi Django ImageField'a kaydet
                    self.kapak_fotografi.save(f"{video_id}.jpg", ContentFile(image_io.getvalue()), save=False)

        super(VideoGaleri01, self).save(*args, **kwargs)




## FOTOGALERİ
# FOTOGALERİ KATEGORİ


def kapakfoto_path_fotogalerikategori(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'fotogalerikategori/kapakfoto/{filename}'

class FotoGaleriKategori(models.Model):
    baslik = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_fotogalerikategori, blank=True, null=True)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.baslik

    def save(self, *args, **kwargs):
        # Eğer slug boşsa ve bu yeni bir nesne ise
        if not self.id and not self.slug:
            # Önce nesneyi veritabanına kaydet (bu, bir id atar)
            super(FotoGaleriKategori, self).save(*args, **kwargs)
            # Slug alanını oluştur
            self.slug = slugify(f"{self.baslik}-{self.id}")
            # save() metodunu tekrar çağırarak slug'ı kaydet
            kwargs.pop('force_insert', None)  # force_insert argümanını kaldır
            super(FotoGaleriKategori, self).save(*args, **kwargs)
        else:
            super(FotoGaleriKategori, self).save(*args, **kwargs)





# FOTOGALERİ


def kapakfoto_path_fotogaleri(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'fotogaleri/kapakfoto/{filename}'
class FotoGaleri(models.Model):
    baslik = models.CharField(max_length=255)
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_fotogaleri, blank=True, null=True)
    fotogaleri_kategori=models.ForeignKey(FotoGaleriKategori,on_delete=models.CASCADE,null=True, blank=True)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)



    def __str__(self):
        return self.baslik



def album_path_fotogaleri(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'fotogaleri/album/{filename}'

class Image(models.Model):
    album = models.ForeignKey(FotoGaleri, related_name='images', on_delete=models.CASCADE,null=True, blank=True)
    image = models.ImageField(upload_to=album_path_fotogaleri, blank=True, null=True)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.album.baslik} - Image {self.id}"



#### FALİYETLER

# SEMPOZYUMLAR



def kapakfoto_path_sempozyumlar(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'sempozyumlar/kapakfoto/{filename}'

def pdf_dosya_path_sempozyumlar(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'sempozyumlar/pdf_dosyalar/{filename}'

class Sempozyumlar(models.Model):
    baslik = models.CharField(max_length=200)
    tarih = models.DateTimeField()
    konum = models.CharField(max_length=200)
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_sempozyumlar, blank=True, null=True)
    pdf_dosya = models.FileField(upload_to=pdf_dosya_path_sempozyumlar, blank=True, null=True)
    album = models.ForeignKey(FotoGaleri, on_delete=models.CASCADE, null=True, blank=True)
    yayin = models.ForeignKey(VideoGaleri01, on_delete=models.CASCADE, null=True, blank=True)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)


# ÇALIŞTAYLAR

def kapakfoto_path_calistaylar(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'calistaylar/kapakfoto/{filename}'

def pdf_dosya_path_calistaylar(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'calistaylar/pdf_dosyalar/{filename}'

class Calistaylar(models.Model):
    baslik = models.CharField(max_length=200)
    tarih = models.DateTimeField()
    konum = models.CharField(max_length=200)
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_calistaylar, blank=True, null=True)
    pdf_dosya = models.FileField(upload_to=pdf_dosya_path_calistaylar, blank=True, null=True)
    album = models.ForeignKey(FotoGaleri, on_delete=models.CASCADE, null=True, blank=True)
    yayin = models.ForeignKey(VideoGaleri01, on_delete=models.CASCADE, null=True, blank=True)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)



# EĞİTİMLER


def pdf_dosya_path_egitimler(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'egitimler/pdf_dosyalar/{filename}'

def kapakfoto_path_egitimler(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'egitimler/kapakfoto/{filename}'



class Egitimler(models.Model):
    baslik = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    tarih = models.DateTimeField()
    egitmen = models.CharField(max_length=200)
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_egitimler, blank=True, null=True)
    pdf_dosya = models.FileField(upload_to=pdf_dosya_path_egitimler, blank=True, null=True)
    album = models.ForeignKey(FotoGaleri, on_delete=models.CASCADE, null=True, blank=True)
    yayin = models.ForeignKey(VideoGaleri01, on_delete=models.CASCADE, null=True, blank=True)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        # Eğer slug boşsa ve bu yeni bir nesne ise
        if not self.id and not self.slug:
            # Önce nesneyi veritabanına kaydet (bu, bir id atar)
            super(Egitimler, self).save(*args, **kwargs)
            # Slug alanını oluştur
            self.slug = slugify(f"{self.baslik}-{self.id}")
            # save() metodunu tekrar çağırarak slug'ı kaydet
            kwargs.pop('force_insert', None)  # force_insert argümanını kaldır
            super(Egitimler, self).save(*args, **kwargs)
        else:
            super(Egitimler, self).save(*args, **kwargs)




# KONFERANS

def kapakfoto_path_konferanslar(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'konferanslar/kapakfoto/{filename}'



class Konferanslar(models.Model):
    baslik = models.CharField(max_length=200)
    tarih = models.DateTimeField()
    konum = models.CharField(max_length=200, null=True, blank=True)
    konusmaci = models.CharField(max_length=200)
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_egitimler, blank=True, null=True)
    album = models.ForeignKey(FotoGaleri, on_delete=models.CASCADE, null=True, blank=True)
    yayin = models.ForeignKey(VideoGaleri01, on_delete=models.CASCADE, null=True, blank=True)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)




# ARAŞTIRMALAR

def kapakfoto_path_arastirmalar(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'arastirmalar/kapakfoto/{filename}'

def pdf_dosya_path_arastirmalar(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'arastirmalar/pdf_dosyalar/{filename}'



class Arastirmalar(models.Model):
    baslik = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    kapak_fotografi = models.ImageField(upload_to=kapakfoto_path_egitimler, blank=True, null=True)
    pdf_dosya = models.FileField(upload_to=pdf_dosya_path_arastirmalar, blank=True, null=True)
    album = models.ForeignKey(FotoGaleri, on_delete=models.CASCADE, null=True, blank=True)
    yayin = models.ForeignKey(VideoGaleri01, on_delete=models.CASCADE, null=True, blank=True)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        # Eğer slug boşsa ve bu yeni bir nesne ise
        if not self.id and not self.slug:
            # Önce nesneyi veritabanına kaydet (bu, bir id atar)
            super(Arastirmalar, self).save(*args, **kwargs)
            # Slug alanını oluştur
            self.slug = slugify(f"{self.baslik}-{self.id}")
            # save() metodunu tekrar çağırarak slug'ı kaydet
            kwargs.pop('force_insert', None)  # force_insert argümanını kaldır
            super(Arastirmalar, self).save(*args, **kwargs)
        else:
            super(Arastirmalar, self).save(*args, **kwargs)



# PUPPUP
def kapakfoto_path_puppup(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'puppup/kapakfoto/{filename}'


class Puppup(models.Model):
    name = models.CharField(max_length=200)
    img = models.ImageField(upload_to=kapakfoto_path_puppup, blank=True, null=True)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)




from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=Puppup)
def deactivate_other_popups(sender, instance, **kwargs):
    if instance.durum:
        # Eğer bir Popup aktif olarak ayarlanıyorsa, diğerlerini pasif yap
        Puppup.objects.filter(durum=True).exclude(pk=instance.pk).update(durum=False)





def kapakfoto_path_baslikgorsel(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'baslikgorsel/kapakfoto/{filename}'


class BalikGorsel(models.Model):
    name = models.CharField(max_length=200)
    img = models.ImageField(upload_to=kapakfoto_path_baslikgorsel, blank=True, null=True)
    durum = models.BooleanField(default=True)
    is_removed = models.BooleanField(default=False)


@receiver(pre_save, sender=BalikGorsel)
def deactivate_other_popups(sender, instance, **kwargs):
    if instance.durum:
        BalikGorsel.objects.filter(durum=True).exclude(pk=instance.pk).update(durum=False)
