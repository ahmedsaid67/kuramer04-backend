from rest_framework import serializers
from .models import Slider

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')




class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
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
        instance.img = validated_data.get('img', instance.img)
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


