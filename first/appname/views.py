from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import Slider
from .serializers import SliderSerializer,UserSerializer
from rest_framework import status


from django.utils.translation import gettext as _
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_200_OK,
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from rest_framework.authtoken.views import ObtainAuthToken

from django.contrib.auth.models import User





class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class CheckToken(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Token is valid'})


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)



class SliderListView(ListAPIView):
    queryset = Slider.objects.filter(is_published=True)
    serializer_class = SliderSerializer


from rest_framework import viewsets
from .models import Menu, MenuItem
from .serializers import MenuSerializer, MenuItemSerializer

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    pagination_class = None
    def create(self, request, *args, **kwargs):
        selected = request.data.get('selected', False)

        # Eğer yeni menü seçili ise, diğer seçili menüyü bul ve selected değerini False yap
        if selected:
            try:
                existing_selected_menu = Menu.objects.get(selected=True)
                existing_selected_menu.selected = False
                existing_selected_menu.save()
            except Menu.DoesNotExist:
                pass  # Hiç seçili menü yok, devam et

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        # Yeni verilerden seçili değerini kontrol et
        selected = serializer.validated_data.get('selected', False)
        if selected:
            try:
                existing_selected_menu = Menu.objects.get(selected=True)
                if existing_selected_menu != serializer.instance:
                    # Güncellenecek menü, zaten seçili menü değilse
                    existing_selected_menu.selected = False
                    existing_selected_menu.save()
            except Menu.DoesNotExist:
                pass  # Hiç seçili menü yok, devam et

        serializer.save()

#class MenuItemViewSet(viewsets.ModelViewSet):
#    queryset = MenuItem.objects.all()
#    serializer_class = MenuItemSerializer

#    def retrieve(self, request, pk=None):
#        # Belirli bir menüye ait MenuItem nesnelerini getir
#        menu_items = MenuItem.objects.filter(menu_id=pk)
#        serializer = self.get_serializer(menu_items, many=True)
#       return Response(serializer.data)

from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer


# tüm menü ögelerini getirir
class MenuItemListCreateView(generics.ListAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    pagination_class = None


# x menuye aıt menu ogelerini getir ve yeni öge üretir.
class MenuItemByMenuView(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer
    pagination_class = None

    def get_queryset(self):
        menu_id = self.kwargs.get('menu_id')
        return MenuItem.objects.filter(menu__id=menu_id)





# menu ogelerin her birinin tekil olarak detaylarını getir.
class MenuItemDetailView(generics.RetrieveUpdateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    pagination_class = None

# seçili menünün ögeleri listele
class MenuSelectedItemList(generics.ListAPIView):
    queryset = MenuItem.objects.filter(menu__selected=True,is_disabled=False)
    serializer_class = MenuItemSerializer
    #permission_classes = [IsAuthenticated]
    pagination_class = None






# Personeller
#personeltürü
from .models import PersonelTuru
from .serializers import PersonelTuruSerializer
from rest_framework.decorators import action

class PersonelTuruViewSet(viewsets.ModelViewSet):
    queryset = PersonelTuru.objects.filter(is_removed=False).order_by('-id')
    serializer_class = PersonelTuruSerializer

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        PersonelTuru.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = PersonelTuru.objects.filter(status=True,is_removed=False).order_by('-id')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)




from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView

class PersonelTuruListView(ListModelMixin, GenericAPIView):
    queryset = PersonelTuru.objects.filter(is_removed=False,status=True).order_by('-id')
    serializer_class = PersonelTuruSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

#personeller

from .models import Persons
from .serializers import PersonellerSerializer

from django_filters import rest_framework as filters


class PersonelFilter(filters.FilterSet):
    kategori = filters.NumberFilter(field_name='personel_turu__id')  # URL'de kategori olarak geçecek

    class Meta:
        model = Persons
        fields = ['kategori']

class PersonellerViewSet(viewsets.ModelViewSet):
    queryset = Persons.objects.filter(is_removed=False).order_by('-id')
    serializer_class = PersonellerSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PersonelFilter

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        Persons.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = Persons.objects.filter(durum=True,is_removed=False).order_by('-id')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)


### YAYINLAR
#BROŞÜRLER

from .models import Brosurler
from .serializers import BrosurlerSerializer

class BrosurlerViewSet(viewsets.ModelViewSet):
    queryset = Brosurler.objects.filter(is_removed=False).order_by('-id')
    serializer_class = BrosurlerSerializer

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        Brosurler.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = Brosurler.objects.filter(durum=True,is_removed=False).order_by('-id')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)



# BÜLTENLER


from .models import Bultenler
from .serializers import BultenlerSerializer

class BultenlerViewSet(viewsets.ModelViewSet):
    queryset = Bultenler.objects.filter(is_removed=False).order_by('-id')
    serializer_class = BultenlerSerializer

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        Bultenler.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = Bultenler.objects.filter(durum=True,is_removed=False).order_by('-id')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)




## TEMEL KONU VE KAVRAMLAR
## TEMEL KONULAR

from .models import Temelkonular
from .serializers import TemelkonularSerializer

class TemelkonularViewSet(viewsets.ModelViewSet):
    queryset = Temelkonular.objects.filter(is_removed=False).order_by('-id')
    serializer_class = TemelkonularSerializer

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        Temelkonular.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = Temelkonular.objects.filter(durum=True,is_removed=False).order_by('-id')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)

## TEMEL KAVRAMLAR

from .models import Temelkavramlar
from .serializers import TemelkavramlarSerializer

class TemelkavramlarViewSet(viewsets.ModelViewSet):
    queryset = Temelkavramlar.objects.filter(is_removed=False).order_by('-id')
    serializer_class = TemelkavramlarSerializer

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        Temelkavramlar.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = Temelkavramlar.objects.filter(durum=True,is_removed=False).order_by('-id')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)



###### YAYINLARIMIZDAN SEÇMELER


from .models import YayinlarimizdanSecmeler
from .serializers import YayinlarimizdanSecmelerSerializer

class YayinlarimizdanSecmelerViewSet(viewsets.ModelViewSet):
    queryset = YayinlarimizdanSecmeler.objects.filter(is_removed=False).order_by('-id')
    serializer_class = YayinlarimizdanSecmelerSerializer

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        YayinlarimizdanSecmeler.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = YayinlarimizdanSecmeler.objects.filter(durum=True,is_removed=False).order_by('-id')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)


### BASINDA BİZ


# YAZILI BASIN

from .models import YaziliBasin
from .serializers import YaziliBasinSerializer

class YaziliBasinViewSet(viewsets.ModelViewSet):
    queryset = YaziliBasin.objects.filter(is_removed=False).order_by('-id')
    serializer_class = YaziliBasinSerializer

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        YaziliBasin.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = YaziliBasin.objects.filter(durum=True,is_removed=False).order_by('-id')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)



# GORSEL BASIN


from .models import GorselBasin
from .serializers import GorselBasinSerializer

class GorselBasinViewSet(viewsets.ModelViewSet):
    queryset = GorselBasin.objects.filter(is_removed=False).order_by('-id')
    serializer_class = GorselBasinSerializer

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        GorselBasin.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = GorselBasin.objects.filter(durum=True,is_removed=False).order_by('-id')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)


### KAMUOYU DUYURULARI

from .models import KamuoyuDuyurulari
from .serializers import KamuoyuDuyurulariSerializer

class KamuoyuDuyurulariViewSet(viewsets.ModelViewSet):
    queryset = KamuoyuDuyurulari.objects.filter(is_removed=False).order_by('-id')
    serializer_class = KamuoyuDuyurulariSerializer

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        KamuoyuDuyurulari.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = KamuoyuDuyurulari.objects.filter(durum=True,is_removed=False).order_by('-id')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)


#### MÜSHAFLAR

# MÜSHAF KATEGORİ

from .models import MushafKategori
from .serializers import MushafKategoriSerializer



class MushafKategoriViewSet(viewsets.ModelViewSet):
    queryset = MushafKategori.objects.filter(is_removed=False).order_by('-id')
    serializer_class = MushafKategoriSerializer

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        MushafKategori.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = MushafKategori.objects.filter(durum=True,is_removed=False).order_by('-id')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)


class MushafKategoriListView(ListModelMixin, GenericAPIView):
    queryset = MushafKategori.objects.filter(is_removed=False,durum=True).order_by('-id')
    serializer_class = MushafKategoriSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



# MÜSHAFLAR

from .models import Mushaflar
from .serializers import MushaflarSerializer

from django_filters import rest_framework as filters


class MushafFilter(filters.FilterSet):
    kategori = filters.NumberFilter(field_name='mushaf_kategori__id')  # URL'de kategori olarak geçecek

    class Meta:
        model = Mushaflar
        fields = ['kategori']

    # tüm musafları mushafkategoriyi göre filtreleyebilioruz bu sayede.
    # mushafkategorinin id sini istiyoruz o idye göre mushafkategoriye ulasıyoruz. ve mushaflarda mushaf_kategor alanı
    # ulaşılan mushafkategor ile dolu olan mushafları cekıyoruz. ve pgainationda mevcut.
    # http://127.0.0.1:8000/api/appname/mushaflar/?kategori=1  ---> bir örnek.
    # buradaki 1 , mushafkategori nesnenisin id sini temsil eder.
    # yani id 'si 1 olan mushaf kategorisi ile ilişkili tüm mushafları getirir.



class MushaflarViewSet(viewsets.ModelViewSet):
    queryset = Mushaflar.objects.filter(is_removed=False).order_by('-id')
    serializer_class = MushaflarSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MushafFilter

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        Mushaflar.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = Mushaflar.objects.filter(durum=True,is_removed=False).order_by('-id')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)



# MÜSHAFLAR

from .models import Mushaffarklari
from .serializers import MushaffarklariSerializer

class MushaffarklariViewSet(viewsets.ModelViewSet):
    queryset = Mushaffarklari.objects.filter(is_removed=False).order_by('-id')
    serializer_class = MushaffarklariSerializer

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        Mushaffarklari.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = Mushaffarklari.objects.filter(durum=True,is_removed=False).order_by('-id')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)





# KitapKategori

from .models import KitapKategori
from .serializers import KitapKategoriSerializer

class KitapKategoriViewSet(viewsets.ModelViewSet):
    queryset = KitapKategori.objects.filter(is_removed=False).order_by('-id')
    serializer_class = KitapKategoriSerializer

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        KitapKategori.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = KitapKategori.objects.filter(durum=True,is_removed=False).order_by('-id')

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)

    ## burası zaten ön yüz için yazılmış silinmöiş ve aktif olmayan nesneleri döndürmemeyi sağlıyordu.
    # biz ek olarak diğerlerinden ayrı burada paginations'u kaldırdık. çünkü kullanıcı arayüzü tarafında
    # kategorinin tamamının listelenmesini istioruz.

class KitapKategoriListView(ListModelMixin, GenericAPIView):
    queryset = KitapKategori.objects.filter(is_removed=False,durum=True).order_by('-id')
    serializer_class = KitapKategoriSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# KitapKategori

from .models import Kitap
from .serializers import KitaplarSerializer
from django_filters import rest_framework as filters


class KitapFilter(filters.FilterSet):
    kategori = filters.NumberFilter(field_name='kitap_kategori__id')  # URL'de kategori olarak geçecek

    class Meta:
        model = Kitap
        fields = ['kategori']
class KitaplarViewSet(viewsets.ModelViewSet):
    queryset = Kitap.objects.filter(is_removed=False).order_by('-id')
    serializer_class = KitaplarSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = KitapFilter

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        Kitap.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = Kitap.objects.filter(durum=True,is_removed=False).order_by('-id')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)
