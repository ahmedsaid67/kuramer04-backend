from rest_framework import serializers

from .models import Sliders


from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')




class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class SlidersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sliders
        fields = '__all__'


from .models import Menu, MenuItem

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuItem
        fields = '__all__'


# Personel

from .models import PersonelTuru

class PersonelTuruSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonelTuru
        fields = ['id', 'name', 'status', 'is_removed']



from .models import Persons

class PersonellerSerializer(serializers.ModelSerializer):
    personel_turu = PersonelTuruSerializer(read_only=True)
    personel_turu_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Persons
        fields = ['id', 'ad', 'soyad','unvan', 'personel_turu', 'personel_turu_id', 'img', 'durum', 'is_removed']

    def create(self, validated_data):
        personel_turu_id = validated_data.pop('personel_turu_id')
        personel_turu = PersonelTuru.objects.get(id=personel_turu_id)
        return Persons.objects.create(personel_turu=personel_turu, **validated_data)

    def update(self, instance, validated_data):
        personel_turu_id = validated_data.get('personel_turu_id', instance.personel_turu_id)
        personel_turu = PersonelTuru.objects.get(id=personel_turu_id)

        instance.ad = validated_data.get('ad', instance.ad)
        instance.soyad = validated_data.get('soyad', instance.soyad)
        instance.unvan = validated_data.get('unvan', instance.unvan)
        instance.personel_turu = personel_turu

        # img alanı için kontrol
        img = validated_data.get('img', None)
        print("img:",img)
        if img is not None:
            instance.img = img
        else:
            print("gorsel boş")
            instance.img = 'defaults/defaultprofilephoto.jpeg'

        instance.durum = validated_data.get('durum', instance.durum)
        instance.is_removed = validated_data.get('is_removed', instance.is_removed)

        instance.save()
        return instance




### YAYINLAR
#BROŞÜRLER

from .models import Brosurler
class BrosurlerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brosurler
        fields = '__all__'


# BÜLTENLER
from .models import Bultenler
class BultenlerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bultenler
        fields = '__all__'





## TEMEL KONU VE KAVRAMLAR
## TEMEL KONULAR

from .models import Temelkonular
class TemelkonularSerializer(serializers.ModelSerializer):

    class Meta:
        model = Temelkonular
        fields = '__all__'


## TEMEL KONULAR

from .models import Temelkavramlar
class TemelkavramlarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Temelkavramlar
        fields = '__all__'


###### YAYINLARIMIZDAN SEÇMELER

from .models import YayinlarimizdanSecmeler
class YayinlarimizdanSecmelerSerializer(serializers.ModelSerializer):

    class Meta:
        model = YayinlarimizdanSecmeler
        fields = '__all__'


### BASINDA BİZ


# YAZILI BASIN


from .models import YaziliBasin
class YaziliBasinSerializer(serializers.ModelSerializer):

    class Meta:
        model = YaziliBasin
        fields = '__all__'



# GORSEL BASIN


from .models import GorselBasin
class GorselBasinSerializer(serializers.ModelSerializer):

    class Meta:
        model = GorselBasin
        fields = '__all__'


### KAMUOYU DUYURULARI

from .models import KamuoyuDuyurulari
class KamuoyuDuyurulariSerializer(serializers.ModelSerializer):

    class Meta:
        model = KamuoyuDuyurulari
        fields = '__all__'



#### MÜSHAFLAR

# MÜSHAF KATEGORİ

from .models import MushafKategori


class MushafKategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = MushafKategori
        fields = '__all__'



#MUSHAFLAR


from .models import Mushaflar

class MushaflarSerializer(serializers.ModelSerializer):
    mushaf_kategori = MushafKategoriSerializer(read_only=True)
    mushaf_kategori_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Mushaflar
        fields = ['id', 'baslik', 'kapak_fotografi','pdf_dosya', 'mushaf_kategori', 'mushaf_kategori_id', 'durum', 'is_removed']

    def create(self, validated_data):
        mushaf_kategori_id = validated_data.pop('mushaf_kategori_id')
        mushaf_kategori = MushafKategori.objects.get(id=mushaf_kategori_id)
        return Mushaflar.objects.create(mushaf_kategori=mushaf_kategori, **validated_data)

    def update(self, instance, validated_data):
        mushaf_kategori_id = validated_data.get('mushaf_kategori_id', instance.mushaf_kategori_id)
        mushaf_kategori = MushafKategori.objects.get(id=mushaf_kategori_id)

        instance.baslik = validated_data.get('baslik', instance.baslik)
        instance.kapak_fotografi = validated_data.get('kapak_fotografi', instance.kapak_fotografi)
        instance.pdf_dosya = validated_data.get('pdf_dosya', instance.pdf_dosya)
        instance.mushaf_kategori = mushaf_kategori
        instance.durum = validated_data.get('durum', instance.durum)
        instance.is_removed = validated_data.get('is_removed', instance.is_removed)

        instance.save()
        return instance


# MÜSHAF FARKLARI

from .models import Mushaffarklari


class MushaffarklariSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mushaffarklari
        fields = '__all__'


# Kitap Kategori

from .models import KitapKategori


class KitapKategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitapKategori
        fields = '__all__'



# Kitaplar



from .models import Kitap

class KitaplarSerializer(serializers.ModelSerializer):
    kitap_kategori = KitapKategoriSerializer(read_only=True)
    kitap_kategori_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Kitap
        fields = ['id', 'ad','slug','yazar','yayin_tarihi','sayfa_sayisi','isbn','kapak_fotografi','ozet', 'kitap_kategori', 'kitap_kategori_id', 'durum', 'is_removed']

    def create(self, validated_data):
        kitap_kategori_id = validated_data.pop('kitap_kategori_id')
        kitap_kategori = KitapKategori.objects.get(id=kitap_kategori_id)
        return Kitap.objects.create(kitap_kategori=kitap_kategori, **validated_data)

    def update(self, instance, validated_data):
        kitap_kategori_id = validated_data.get('kitap_kategori_id', instance.kitap_kategori_id)
        kitap_kategori = KitapKategori.objects.get(id=kitap_kategori_id)

        instance.ad = validated_data.get('ad', instance.ad)
        instance.yazar = validated_data.get('yazar', instance.yazar)
        instance.yayin_tarihi = validated_data.get('yayin_tarihi', instance.yayin_tarihi)
        instance.sayfa_sayisi = validated_data.get('sayfa_sayisi', instance.sayfa_sayisi)
        instance.isbn = validated_data.get('isbn', instance.isbn)
        instance.kapak_fotografi = validated_data.get('kapak_fotografi', instance.kapak_fotografi)
        instance.ozet = validated_data.get('ozet', instance.ozet)
        instance.kitap_kategori = kitap_kategori
        instance.durum = validated_data.get('durum', instance.durum)
        instance.is_removed = validated_data.get('is_removed', instance.is_removed)

        instance.save()
        return instance




### MEDYA GALERİ
#VİDEO GALERİ KATEGORİ

from .models import VideoGaleriKategori

class VideoGaleriKategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoGaleriKategori
        fields = '__all__'

#VİDEO GALERİ


from .models import VideoGaleri01

class VideoGaleri01Serializer(serializers.ModelSerializer):
    videogaleri_kategori = VideoGaleriKategoriSerializer(read_only=True)
    videogaleri_kategori_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = VideoGaleri01
        fields = ['id','baslik','kapak_fotografi', 'videogaleri_kategori', 'videogaleri_kategori_id','url', 'durum', 'is_removed']

    def create(self, validated_data):
        videogaleri_kategori_id = validated_data.pop('videogaleri_kategori_id')
        videogaleri_kategori = VideoGaleriKategori.objects.get(id=videogaleri_kategori_id)
        return VideoGaleri01.objects.create(videogaleri_kategori=videogaleri_kategori, **validated_data)

    def update(self, instance, validated_data):
        videogaleri_kategori_id = validated_data.get('videogaleri_kategori_id', instance.videogaleri_kategori_id)
        videogaleri_kategori = VideoGaleriKategori.objects.get(id=videogaleri_kategori_id)

        instance.baslik = validated_data.get('baslik', instance.baslik)
        instance.url = validated_data.get('url', instance.url)
        instance.videogaleri_kategori = videogaleri_kategori
        instance.durum = validated_data.get('durum', instance.durum)
        instance.is_removed = validated_data.get('is_removed', instance.is_removed)


        instance.save()
        return instance



## FOTOGALERİ
# FOTOGALERİ KATEGORİ


from .models import FotoGaleriKategori

class FotoGaleriKategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoGaleriKategori
        fields = '__all__'


#FOTOGALERİ

from .models import FotoGaleri

class FotoGaleriSerializer(serializers.ModelSerializer):
    fotogaleri_kategori = FotoGaleriKategoriSerializer(read_only=True)
    fotogaleri_kategori_id = serializers.IntegerField(write_only=True)


    class Meta:
        model = FotoGaleri
        fields = ['id','baslik','kapak_fotografi', 'fotogaleri_kategori', 'fotogaleri_kategori_id', 'durum', 'is_removed']

    def create(self, validated_data):
        fotogaleri_kategori_id = validated_data.pop('fotogaleri_kategori_id')
        fotogaleri_kategori = FotoGaleriKategori.objects.get(id=fotogaleri_kategori_id)
        return FotoGaleri.objects.create(fotogaleri_kategori=fotogaleri_kategori, **validated_data)

    def update(self, instance, validated_data):
        fotogaleri_kategori_id = validated_data.get('fotogaleri_kategori_id', instance.fotogaleri_kategori_id)
        fotogaleri_kategori = FotoGaleriKategori.objects.get(id=fotogaleri_kategori_id)

        instance.baslik = validated_data.get('baslik', instance.baslik)
        instance.fotogaleri_kategori = fotogaleri_kategori
        instance.kapak_fotografi = validated_data.get('kapak_fotografi', instance.kapak_fotografi)
        instance.durum = validated_data.get('durum', instance.durum)
        instance.is_removed = validated_data.get('is_removed', instance.is_removed)

        instance.save()
        return instance


# IMAGE

from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    album_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Image
        fields = ['id','album', 'album_id', 'image', 'is_removed']

    def create(self, validated_data):
        album_id = validated_data.pop('album_id')
        album = FotoGaleri.objects.get(id=album_id)
        return Image.objects.create(album=album, **validated_data)




### FAALİYETLER

# SEMPOZYUMLAR

from .models import Sempozyumlar

class SempozyumlarSerializer(serializers.ModelSerializer):
    album = FotoGaleriSerializer(read_only=True)
    album_id = serializers.IntegerField(write_only=True, required=False)
    yayin = VideoGaleri01Serializer(read_only=True)
    yayin_id = serializers.IntegerField(write_only=True,required=False )

    class Meta:
        model = Sempozyumlar
        fields = ['id','baslik',"tarih","konum",'kapak_fotografi',"pdf_dosya", 'album', 'album_id',"yayin","yayin_id", 'durum', 'is_removed']

    def create(self, validated_data):

        album_id = validated_data.pop('album_id', None)
        yayin_id = validated_data.pop('yayin_id', None)



        if album_id is not None:
            album = FotoGaleri.objects.get(id=album_id)
            validated_data['album'] = album

        if yayin_id is not None:
            yayin = VideoGaleri01.objects.get(id=yayin_id)
            validated_data['yayin'] = yayin

        return Sempozyumlar.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # album_id için kontrol
        album_id = validated_data.get('album_id', None)
        if album_id is not None:
            try:
                album = FotoGaleri.objects.get(id=album_id)
                instance.album = album
            except FotoGaleri.DoesNotExist:
                # Burada, isteğe bağlı olarak bir hata fırlatabilir veya işlem yapmamayı tercih edebilirsiniz.
                pass
        else:

            instance.album = None

        # yayin_id için kontrol
        yayin_id = validated_data.get('yayin_id', None)
        if yayin_id is not None:
            try:
                yayin = VideoGaleri01.objects.get(id=yayin_id)
                instance.yayin = yayin
            except VideoGaleri01.DoesNotExist:
                # Burada da, isteğe bağlı olarak bir hata fırlatabilir veya işlem yapmamayı tercih edebilirsiniz.
                pass
        else:
            instance.yayin = None

        # Diğer alanların güncellenmesi
        instance.baslik = validated_data.get('baslik', instance.baslik)
        instance.tarih = validated_data.get('tarih', instance.tarih)
        instance.konum = validated_data.get('konum', instance.konum)
        instance.kapak_fotografi = validated_data.get('kapak_fotografi', instance.kapak_fotografi)
        instance.pdf_dosya = validated_data.get('pdf_dosya', instance.pdf_dosya)
        instance.durum = validated_data.get('durum', instance.durum)
        instance.is_removed = validated_data.get('is_removed', instance.is_removed)

        instance.save()
        return instance



# CALIŞTAYLAR

from .models import Calistaylar

class CalistaylarSerializer(serializers.ModelSerializer):
    album = FotoGaleriSerializer(read_only=True)
    album_id = serializers.IntegerField(write_only=True, required=False)
    yayin = VideoGaleri01Serializer(read_only=True)
    yayin_id = serializers.IntegerField(write_only=True,required=False )

    class Meta:
        model = Calistaylar
        fields = ['id','baslik',"tarih","konum",'kapak_fotografi',"pdf_dosya", 'album', 'album_id',"yayin","yayin_id", 'durum', 'is_removed']

    def create(self, validated_data):

        album_id = validated_data.pop('album_id', None)
        yayin_id = validated_data.pop('yayin_id', None)



        if album_id is not None:
            album = FotoGaleri.objects.get(id=album_id)
            validated_data['album'] = album

        if yayin_id is not None:
            yayin = VideoGaleri01.objects.get(id=yayin_id)
            validated_data['yayin'] = yayin

        return Calistaylar.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # album_id için kontrol
        album_id = validated_data.get('album_id', None)
        if album_id is not None:
            try:
                album = FotoGaleri.objects.get(id=album_id)
                instance.album = album
            except FotoGaleri.DoesNotExist:
                # Burada, isteğe bağlı olarak bir hata fırlatabilir veya işlem yapmamayı tercih edebilirsiniz.
                pass
        else:

            instance.album = None


        # yayin_id için kontrol
        yayin_id = validated_data.get('yayin_id', None)
        if yayin_id is not None:
            try:
                yayin = VideoGaleri01.objects.get(id=yayin_id)
                instance.yayin = yayin
            except VideoGaleri01.DoesNotExist:
                # Burada da, isteğe bağlı olarak bir hata fırlatabilir veya işlem yapmamayı tercih edebilirsiniz.
                pass
        else:
            instance.yayin = None


        # Diğer alanların güncellenmesi
        instance.baslik = validated_data.get('baslik', instance.baslik)
        instance.tarih = validated_data.get('tarih', instance.tarih)
        instance.konum = validated_data.get('konum', instance.konum)
        instance.kapak_fotografi = validated_data.get('kapak_fotografi', instance.kapak_fotografi)
        instance.pdf_dosya = validated_data.get('pdf_dosya', instance.pdf_dosya)
        instance.durum = validated_data.get('durum', instance.durum)
        instance.is_removed = validated_data.get('is_removed', instance.is_removed)

        instance.save()
        return instance



# EĞİTİMLER

from .models import Egitimler

class EgitimlerSerializer(serializers.ModelSerializer):
    album = FotoGaleriSerializer(read_only=True)
    album_id = serializers.IntegerField(write_only=True, required=False)
    yayin = VideoGaleri01Serializer(read_only=True)
    yayin_id = serializers.IntegerField(write_only=True,required=False )

    class Meta:
        model = Egitimler
        fields = ['id','baslik',"tarih","egitmen",'kapak_fotografi',"icerik","slug", 'album', 'album_id',"yayin","yayin_id", 'durum', 'is_removed']

    def create(self, validated_data):

        album_id = validated_data.pop('album_id', None)
        yayin_id = validated_data.pop('yayin_id', None)



        if album_id is not None:
            album = FotoGaleri.objects.get(id=album_id)
            validated_data['album'] = album

        if yayin_id is not None:
            yayin = VideoGaleri01.objects.get(id=yayin_id)
            validated_data['yayin'] = yayin

        return Egitimler.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # album_id için kontrol
        album_id = validated_data.get('album_id', None)
        if album_id is not None:
            try:
                album = FotoGaleri.objects.get(id=album_id)
                instance.album = album
            except FotoGaleri.DoesNotExist:
                # Burada, isteğe bağlı olarak bir hata fırlatabilir veya işlem yapmamayı tercih edebilirsiniz.
                pass
        else:

            instance.album = None

        # yayin_id için kontrol
        yayin_id = validated_data.get('yayin_id', None)
        if yayin_id is not None:
            try:
                yayin = VideoGaleri01.objects.get(id=yayin_id)
                instance.yayin = yayin
            except VideoGaleri01.DoesNotExist:
                # Burada da, isteğe bağlı olarak bir hata fırlatabilir veya işlem yapmamayı tercih edebilirsiniz.
                pass
        else:
            instance.yayin = None

        # Diğer alanların güncellenmesi
        instance.baslik = validated_data.get('baslik', instance.baslik)
        instance.tarih = validated_data.get('tarih', instance.tarih)
        instance.egitmen = validated_data.get('egitmen', instance.egitmen)
        instance.kapak_fotografi = validated_data.get('kapak_fotografi', instance.kapak_fotografi)
        instance.icerik = validated_data.get('icerik', instance.icerik)
        instance.durum = validated_data.get('durum', instance.durum)
        instance.is_removed = validated_data.get('is_removed', instance.is_removed)

        instance.save()
        return instance






# KONFERANSLAR

from .models import Konferanslar

class KonferanslarSerializer(serializers.ModelSerializer):
    album = FotoGaleriSerializer(read_only=True)
    album_id = serializers.IntegerField(write_only=True, required=False)
    yayin = VideoGaleri01Serializer(read_only=True)
    yayin_id = serializers.IntegerField(write_only=True,required=False )

    class Meta:
        model = Konferanslar
        fields = ['id','baslik',"tarih","konum","konusmaci",'kapak_fotografi', 'album', 'album_id',"yayin","yayin_id", 'durum', 'is_removed']

    def create(self, validated_data):

        album_id = validated_data.pop('album_id', None)
        yayin_id = validated_data.pop('yayin_id', None)



        if album_id is not None:
            album = FotoGaleri.objects.get(id=album_id)
            validated_data['album'] = album

        if yayin_id is not None:
            yayin = VideoGaleri01.objects.get(id=yayin_id)
            validated_data['yayin'] = yayin

        return Konferanslar.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # album_id için kontrol
        album_id = validated_data.get('album_id', None)
        if album_id is not None:
            try:
                album = FotoGaleri.objects.get(id=album_id)
                instance.album = album
            except FotoGaleri.DoesNotExist:
                # Burada, isteğe bağlı olarak bir hata fırlatabilir veya işlem yapmamayı tercih edebilirsiniz.
                pass
        else:

            instance.album = None

        # yayin_id için kontrol
        yayin_id = validated_data.get('yayin_id', None)
        if yayin_id is not None:
            try:
                yayin = VideoGaleri01.objects.get(id=yayin_id)
                instance.yayin = yayin
            except VideoGaleri01.DoesNotExist:
                # Burada da, isteğe bağlı olarak bir hata fırlatabilir veya işlem yapmamayı tercih edebilirsiniz.
                pass
        else:
            instance.yayin = None

        # Diğer alanların güncellenmesi
        instance.baslik = validated_data.get('baslik', instance.baslik)
        instance.tarih = validated_data.get('tarih', instance.tarih)
        instance.konum = validated_data.get('konum', instance.konum)
        instance.konusmaci = validated_data.get('konusmaci', instance.konusmaci)
        instance.kapak_fotografi = validated_data.get('kapak_fotografi', instance.kapak_fotografi)
        instance.durum = validated_data.get('durum', instance.durum)
        instance.is_removed = validated_data.get('is_removed', instance.is_removed)

        instance.save()
        return instance




from .models import Arastirmalar

class ArastirmalarSerializer(serializers.ModelSerializer):
    album = FotoGaleriSerializer(read_only=True)
    album_id = serializers.IntegerField(write_only=True, required=False)
    yayin = VideoGaleri01Serializer(read_only=True)
    yayin_id = serializers.IntegerField(write_only=True,required=False )

    class Meta:
        model = Arastirmalar
        fields = ['id','baslik','kapak_fotografi',"icerik","slug", 'album', 'album_id',"yayin","yayin_id", 'durum', 'is_removed']

    def create(self, validated_data):

        album_id = validated_data.pop('album_id', None)
        yayin_id = validated_data.pop('yayin_id', None)



        if album_id is not None:
            album = FotoGaleri.objects.get(id=album_id)
            validated_data['album'] = album

        if yayin_id is not None:
            yayin = VideoGaleri01.objects.get(id=yayin_id)
            validated_data['yayin'] = yayin

        return Arastirmalar.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # album_id için kontrol
        album_id = validated_data.get('album_id', None)
        if album_id is not None:
            try:
                album = FotoGaleri.objects.get(id=album_id)
                instance.album = album
            except FotoGaleri.DoesNotExist:
                # Burada, isteğe bağlı olarak bir hata fırlatabilir veya işlem yapmamayı tercih edebilirsiniz.
                pass
        else:

            instance.album = None

        # yayin_id için kontrol
        yayin_id = validated_data.get('yayin_id', None)
        if yayin_id is not None:
            try:
                yayin = VideoGaleri01.objects.get(id=yayin_id)
                instance.yayin = yayin
            except VideoGaleri01.DoesNotExist:
                # Burada da, isteğe bağlı olarak bir hata fırlatabilir veya işlem yapmamayı tercih edebilirsiniz.
                pass
        else:
            instance.yayin = None

        # Diğer alanların güncellenmesi
        instance.baslik = validated_data.get('baslik', instance.baslik)
        instance.kapak_fotografi = validated_data.get('kapak_fotografi', instance.kapak_fotografi)
        instance.icerik = validated_data.get('icerik', instance.icerik)
        instance.durum = validated_data.get('durum', instance.durum)
        instance.is_removed = validated_data.get('is_removed', instance.is_removed)

        instance.save()
        return instance




# PUPPUP


from .models import Puppup
class PuppupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Puppup
        fields = '__all__'


# BAŞLIK GÖRSEL


from .models import BalikGorsel
class BalikGorselSerializer(serializers.ModelSerializer):

    class Meta:
        model = BalikGorsel
        fields = '__all__'
