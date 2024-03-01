from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import Sliders
from .serializers import SlidersSerializer,UserSerializer
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
from .authentication import token_expire_handler

from django.contrib.auth.models import User





class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        try:
            token = Token.objects.get(user=user)
            is_expired, token = token_expire_handler(token)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        return Response({'token': token.key})

class CheckToken(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Token is valid'})

class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get the token of the user from the request
        try:
            token = request.auth
            # Delete the token to effectively log the user out
            Token.objects.filter(key=token).delete()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)






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




from rest_framework.decorators import action

# seçili menünün ögeleri listele
class MenuSelectedItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.filter(menu__selected=True,is_removed=False)
    serializer_class = MenuItemSerializer
    pagination_class = None

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = MenuItem.objects.filter(menu__selected=True,durum=True, is_removed=False)
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'])
    def update_status(self, request):
        changes = request.data
        print(changes)
        for item_id, status in changes.items():
            try:
                item = MenuItem.objects.get(id=item_id)
                item.durum = status
                item.save()
            except MenuItem.DoesNotExist:
                return Response({'error': f'Item with id {item_id} does not exist.'}, status=404)

        return Response({'message': 'Items updated successfully.'})






# Personeller
#personeltürü
from .models import PersonelTuru,Persons
from .serializers import PersonelTuruSerializer
from rest_framework.decorators import action

class PersonelTuruViewSet(viewsets.ModelViewSet):
    queryset = PersonelTuru.objects.filter(is_removed=False).order_by('-id')
    serializer_class = PersonelTuruSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        PersonelTuru.objects.filter(id__in=ids).update(is_removed=True)
        Persons.objects.filter(personel_turu__id__in=ids).update(personel_turu=None,durum=False)


        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = PersonelTuru.objects.filter(status=True,is_removed=False).order_by('-id')

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # 'durum' değeri false ise ilgili VideoGaleri01 nesnelerini güncelle
        if 'status' in serializer.validated_data and not serializer.validated_data['status']:
            Persons.objects.filter(personel_turu=instance).update(personel_turu=None, durum=False)

        return Response(serializer.data)




from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView

class PersonelTuruListView(ListModelMixin, GenericAPIView):
    queryset = PersonelTuru.objects.filter(is_removed=False,status=True).order_by('-id')
    serializer_class = PersonelTuruSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

#personeller

from .models import Persons
from .serializers import PersonellerSerializer

from django_filters import rest_framework as filters


class PersonelFilter(filters.FilterSet):
    kategori = filters.NumberFilter(field_name='personel_turu__id', method='filter_kategori')  # URL'de kategori olarak geçecek

    def filter_kategori(self, queryset, name, value):
        # Kategoriye göre filtreleme yaparken, aynı zamanda durum=True koşulunu da uygula
        return queryset.filter(**{name: value, 'durum': True})


    class Meta:
        model = Persons
        fields = ['kategori']

class PersonellerViewSet(viewsets.ModelViewSet):
    queryset = Persons.objects.filter(is_removed=False).order_by('-id').select_related('personel_turu')
    serializer_class = PersonellerSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PersonelFilter

    def get_permissions(self):
        if self.request.method == 'GET' or self.request.query_params.get('kategori') is not None:
            # GET istekleri ve 'kategori' sorgu parametresi olan istekler için permission yok
            permission_classes = []
        else:
            # Diğer tüm durumlar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

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
        active = Persons.objects.filter(durum=True,is_removed=False).order_by('-id').select_related('personel_turu')
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

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

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


from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.conf import settings

class BultenlerViewSet(viewsets.ModelViewSet):
    queryset = Bultenler.objects.filter(is_removed=False).order_by('-id')
    serializer_class = BultenlerSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

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






class BultenlerListView(ListModelMixin, GenericAPIView):
    queryset = Bultenler.objects.filter(is_removed=False,durum=True).order_by('-id')
    serializer_class = BultenlerSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)











## TEMEL KONU VE KAVRAMLAR
## TEMEL KONULAR

from .models import Temelkonular
from .serializers import TemelkonularSerializer

class TemelkonularViewSet(viewsets.ModelViewSet):
    queryset = Temelkonular.objects.filter(is_removed=False).order_by('-id')
    serializer_class = TemelkonularSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

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

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

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

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

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

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

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

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

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
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

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

from .models import MushafKategori,Mushaflar
from .serializers import MushafKategoriSerializer



class MushafKategoriViewSet(viewsets.ModelViewSet):
    queryset = MushafKategori.objects.filter(is_removed=False).order_by('-id')
    serializer_class = MushafKategoriSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        MushafKategori.objects.filter(id__in=ids).update(is_removed=True)

        Mushaflar.objects.filter(mushaf_kategori__id__in=ids).update(mushaf_kategori=None,durum=False)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = MushafKategori.objects.filter(durum=True,is_removed=False).order_by('-id')


        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # 'durum' değeri false ise ilgili VideoGaleri01 nesnelerini güncelle
        if 'durum' in serializer.validated_data and not serializer.validated_data['durum']:
            Mushaflar.objects.filter(mushaf_kategori=instance).update(mushaf_kategori=None, durum=False)

        return Response(serializer.data)


class MushafKategoriListView(ListModelMixin, GenericAPIView):
    queryset = MushafKategori.objects.filter(is_removed=False,durum=True).order_by('-id')
    serializer_class = MushafKategoriSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



# MÜSHAFLAR

from .models import Mushaflar
from .serializers import MushaflarSerializer

from django_filters import rest_framework as filters


class MushafFilter(filters.FilterSet):
    kategori = filters.NumberFilter(field_name='mushaf_kategori__id', method='filter_kategori')  # URL'de kategori olarak geçecek

    def filter_kategori(self, queryset, name, value):
        # Kategoriye göre filtreleme yaparken, aynı zamanda durum=True koşulunu da uygula
        return queryset.filter(**{name: value, 'durum': True})

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
    queryset = Mushaflar.objects.filter(is_removed=False).order_by('-id').select_related('mushaf_kategori')
    serializer_class = MushaflarSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MushafFilter

    def get_permissions(self):
        if self.request.method == 'GET' or self.request.query_params.get('kategori') is not None:
            # GET istekleri ve 'kategori' sorgu parametresi olan istekler için permission yok
            permission_classes = []
        else:
            # Diğer tüm durumlar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

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
        active = Mushaflar.objects.filter(durum=True,is_removed=False).order_by('-id').select_related('mushaf_kategori')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)



# MÜSHAFLAR FARKLARI

from .models import Mushaffarklari
from .serializers import MushaffarklariSerializer

class MushaffarklariViewSet(viewsets.ModelViewSet):
    queryset = Mushaffarklari.objects.filter(is_removed=False).order_by('-id')
    serializer_class = MushaffarklariSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

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

from .models import KitapKategori,Kitap
from .serializers import KitapKategoriSerializer

class KitapKategoriViewSet(viewsets.ModelViewSet):
    queryset = KitapKategori.objects.filter(is_removed=False).order_by('-id')
    serializer_class = KitapKategoriSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        KitapKategori.objects.filter(id__in=ids).update(is_removed=True)

        Kitap.objects.filter(kitap_kategori__id__in=ids).update(kitap_kategori=None,durum=False)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = KitapKategori.objects.filter(durum=True,is_removed=False).order_by('-id')

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)

    ## burası zaten ön yüz için yazılmış silinmöiş ve aktif olmayan nesneleri döndürmemeyi sağlıyordu.
    # biz ek olarak diğerlerinden ayrı burada paginations'u kaldırdık. çünkü kullanıcı arayüzü tarafında
    # kategorinin tamamının listelenmesini istioruz.


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # 'durum' değeri false ise ilgili VideoGaleri01 nesnelerini güncelle
        if 'durum' in serializer.validated_data and not serializer.validated_data['durum']:
            Kitap.objects.filter(kitap_kategori=instance).update(kitap_kategori=None, durum=False)

        return Response(serializer.data)

class KitapKategoriListView(ListModelMixin, GenericAPIView):
    queryset = KitapKategori.objects.filter(is_removed=False,durum=True).order_by('-id')
    serializer_class = KitapKategoriSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# Kitaplar

from .models import Kitap
from .serializers import KitaplarSerializer
from django_filters import rest_framework as filters


class KitapFilter(filters.FilterSet):
    kategori = filters.NumberFilter(field_name='kitap_kategori__id', method='filter_kategori')

    def filter_kategori(self, queryset, name, value):
        # Kategoriye göre filtreleme yaparken, aynı zamanda durum=True koşulunu da uygula
        return queryset.filter(**{name: value, 'durum': True})

    class Meta:
        model = Kitap
        fields = ['kategori']
class KitaplarViewSet(viewsets.ModelViewSet):
    queryset = Kitap.objects.filter(is_removed=False).order_by('-id').select_related('kitap_kategori')
    serializer_class = KitaplarSerializer
    lookup_field = 'slug'

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = KitapFilter

    def get_permissions(self):
        if self.request.method == 'GET' or self.request.query_params.get('kategori') is not None:
            # GET istekleri ve 'kategori' sorgu parametresi olan istekler için permission yok
            permission_classes = []
        else:
            # Diğer tüm durumlar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

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
        active = Kitap.objects.filter(durum=True,is_removed=False).order_by('-id').select_related('kitap_kategori')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)






## MEDYA GALERİ
# VİDEO GALERİ KATEGORİSİ

from .models import VideoGaleriKategori,VideoGaleri01,Sempozyumlar,Calistaylar,Konferanslar,Arastirmalar,Egitimler
from .serializers import VideoGaleriKategoriSerializer

class VideoGaleriKategoriViewSet(viewsets.ModelViewSet):
    queryset = VideoGaleriKategori.objects.filter(is_removed=False).order_by('-id')
    serializer_class = VideoGaleriKategoriSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]

        # İlgili VideoGaleri01 nesnelerinin ID'lerini al
        videogaleri_ids = list(
            VideoGaleri01.objects.filter(videogaleri_kategori__id__in=ids, is_removed=False).values_list('id',
                                                                                                         flat=True))

        # Belirtilen ID'lere sahip VideoGaleriKategori nesnelerini soft delete işlemi ile güncelle
        VideoGaleriKategori.objects.filter(id__in=ids).update(is_removed=True)

        # İlgili VideoGaleri01 nesnelerini soft delete işlemi ile güncelle
        VideoGaleri01.objects.filter(id__in=videogaleri_ids).update(videogaleri_kategori=None,
                                                                    durum=False)

        # Güncellenen VideoGaleri01 nesneleriyle ilişkili diğer nesnelerin video değerlerini None olarak ayarla
        related_models = [Sempozyumlar, Calistaylar, Konferanslar, Arastirmalar, Egitimler]
        for model in related_models:
            model.objects.filter(yayin__id__in=videogaleri_ids).update(yayin=None)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = VideoGaleriKategori.objects.filter(durum=True,is_removed=False).order_by('-id')


        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # 'durum' değeri false ise ilgili VideoGaleri01 nesnelerini güncelle
        if 'durum' in serializer.validated_data and not serializer.validated_data['durum']:
            # İlgili VideoGaleri01 nesnelerinin ID'lerini al
            videogaleri_ids = list(
                VideoGaleri01.objects.filter(videogaleri_kategori=instance).values_list('id', flat=True))

            # VideoGaleri01 nesnelerini güncelle
            VideoGaleri01.objects.filter(id__in=videogaleri_ids).update(durum=False, videogaleri_kategori=None)

            # Güncellenen VideoGaleri01 nesneleriyle ilişkili diğer nesnelerin yayin değerlerini None olarak ayarla
            related_models = [Sempozyumlar, Calistaylar, Konferanslar, Arastirmalar, Egitimler]
            for model in related_models:
                model.objects.filter(yayin__id__in=videogaleri_ids).update(yayin=None)


        return Response(serializer.data)







class VideoGaleriKategoriListView(ListModelMixin, GenericAPIView):
    queryset = VideoGaleriKategori.objects.filter(is_removed=False,durum=True).order_by('-id')
    serializer_class = VideoGaleriKategoriSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



## VİDEO GALERİ


from .models import VideoGaleri01
from .serializers import VideoGaleri01Serializer

class VideoGaleri01Filter(filters.FilterSet):
    kategori = filters.CharFilter(field_name='videogaleri_kategori__slug', method='filter_kategori')  # URL'de kategori olarak geçecek
    def filter_kategori(self, queryset, name, value):
        # Kategoriye göre filtreleme yaparken, aynı zamanda durum=True koşulunu da uygula
        return queryset.filter(**{name: value, 'durum': True})
    class Meta:
        model = VideoGaleri01
        fields = ['kategori']
class VideoGaleri01ViewSet(viewsets.ModelViewSet):
    queryset = VideoGaleri01.objects.filter(is_removed=False).order_by('-id').select_related('videogaleri_kategori')
    serializer_class = VideoGaleri01Serializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = VideoGaleri01Filter

    def get_permissions(self):
        if self.request.method == 'GET' or self.request.query_params.get('kategori') is not None:
            # GET istekleri ve 'kategori' sorgu parametresi olan istekler için permission yok
            permission_classes = []
        else:
            # Diğer tüm durumlar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        VideoGaleri01.objects.filter(id__in=ids).update(is_removed=True)

        Sempozyumlar.objects.filter(yayin__id__in=ids).update(yayin=None)
        Calistaylar.objects.filter(yayin__id__in=ids).update(yayin=None)
        Konferanslar.objects.filter(yayin__id__in=ids).update(yayin=None)
        Arastirmalar.objects.filter(yayin__id__in=ids).update(yayin=None)
        Egitimler.objects.filter(yayin__id__in=ids).update(yayin=None)


        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = VideoGaleri01.objects.filter(durum=True,is_removed=False).order_by('-id').select_related('videogaleri_kategori')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if 'durum' in serializer.validated_data and not serializer.validated_data['durum']:
            Sempozyumlar.objects.filter(yayin=instance).update(yayin=None)
            Calistaylar.objects.filter(yayin=instance).update(yayin=None)
            Konferanslar.objects.filter(yayin=instance).update(yayin=None)
            Arastirmalar.objects.filter(yayin=instance).update(yayin=None)
            Egitimler.objects.filter(yayin=instance).update(yayin=None)

        return Response(serializer.data)



class VideoGaleri01ListView(ListModelMixin, GenericAPIView):
    queryset = VideoGaleri01.objects.filter(is_removed=False,durum=True).order_by('-id')
    serializer_class = VideoGaleri01Serializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


## FOTOGALERİ
# FOTOGALERİ KATEGORİ

from .models import FotoGaleriKategori,FotoGaleri
from .serializers import FotoGaleriKategoriSerializer

class FotoGaleriKategoriViewSet(viewsets.ModelViewSet):
    queryset = FotoGaleriKategori.objects.filter(is_removed=False).order_by('-id')
    serializer_class = FotoGaleriKategoriSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        FotoGaleriKategori.objects.filter(id__in=ids).update(is_removed=True)
        FotoGaleri.objects.filter(fotogaleri_kategori__id__in=ids).update(fotogaleri_kategori=None,durum=False)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]

        # İlgili VideoGaleri01 nesnelerinin ID'lerini al
        fotogaleri_ids = list(
            FotoGaleri.objects.filter(fotogaleri_kategori__id__in=ids, is_removed=False).values_list('id',
                                                                                                         flat=True))

        # Belirtilen ID'lere sahip VideoGaleriKategori nesnelerini soft delete işlemi ile güncelle
        FotoGaleriKategori.objects.filter(id__in=ids).update(is_removed=True)

        # İlgili VideoGaleri01 nesnelerini soft delete işlemi ile güncelle
        FotoGaleri.objects.filter(id__in=fotogaleri_ids).update(fotogaleri_kategori=None,
                                                                    durum=False)

        # Güncellenen VideoGaleri01 nesneleriyle ilişkili diğer nesnelerin video değerlerini None olarak ayarla
        related_models = [Sempozyumlar, Calistaylar, Konferanslar, Arastirmalar, Egitimler]
        for model in related_models:
            model.objects.filter(album__id__in=fotogaleri_ids).update(album=None)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = FotoGaleriKategori.objects.filter(durum=True,is_removed=False).order_by('-id')


        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)



    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # 'durum' değeri false ise ilgili FotoGaleri nesnelerini güncelle
        if 'durum' in serializer.validated_data and not serializer.validated_data['durum']:
            # İlgili FotoGaleri nesnelerinin ID'lerini al
            fotogaleri_ids = list(FotoGaleri.objects.filter(fotogaleri_kategori=instance).values_list('id', flat=True))

            # FotoGaleri nesnelerini güncelle
            FotoGaleri.objects.filter(id__in=fotogaleri_ids).update(durum=False, fotogaleri_kategori=None)

            # Güncellenen FotoGaleri nesneleriyle ilişkili diğer nesnelerin album değerlerini None olarak ayarla
            related_models = [Sempozyumlar, Calistaylar, Konferanslar, Arastirmalar, Egitimler]
            for model in related_models:
                model.objects.filter(album__id__in=fotogaleri_ids).update(album=None)

        return Response(serializer.data)

class FotoGaleriKategoriListView(ListModelMixin, GenericAPIView):
    queryset = FotoGaleriKategori.objects.filter(is_removed=False,durum=True).order_by('-id')
    serializer_class = FotoGaleriKategoriSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



# FOTOGALERİ


from .models import FotoGaleri
from .serializers import FotoGaleriSerializer

class FotoGaleriFilter(filters.FilterSet):
    kategori = filters.CharFilter(field_name='fotogaleri_kategori__slug', method='filter_kategori')  # URL'de kategori olarak geçecek

    def filter_kategori(self, queryset, name, value):
        # Kategoriye göre filtreleme yaparken, aynı zamanda durum=True koşulunu da uygula
        return queryset.filter(**{name: value, 'durum': True})

    class Meta:
        model = FotoGaleri
        fields = ['kategori']
class FotoGaleriViewSet(viewsets.ModelViewSet):
    queryset = FotoGaleri.objects.filter(is_removed=False).order_by('-id').select_related('fotogaleri_kategori')
    serializer_class = FotoGaleriSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FotoGaleriFilter

    def get_permissions(self):
        if self.request.method == 'GET' or self.request.query_params.get('kategori') is not None:
            # GET istekleri ve 'kategori' sorgu parametresi olan istekler için permission yok
            permission_classes = []
        else:
            # Diğer tüm durumlar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        FotoGaleri.objects.filter(id__in=ids).update(is_removed=True)

        Sempozyumlar.objects.filter(album__id__in=ids).update(album=None)
        Calistaylar.objects.filter(album__id__in=ids).update(album=None)
        Konferanslar.objects.filter(album__id__in=ids).update(album=None)
        Arastirmalar.objects.filter(album__id__in=ids).update(album=None)
        Egitimler.objects.filter(album__id__in=ids).update(album=None)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = FotoGaleri.objects.filter(durum=True,is_removed=False).order_by('-id').select_related('fotogaleri_kategori')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if 'durum' in serializer.validated_data and not serializer.validated_data['durum']:
            Sempozyumlar.objects.filter(album=instance).update(album=None)
            Calistaylar.objects.filter(album=instance).update(album=None)
            Konferanslar.objects.filter(album=instance).update(album=None)
            Arastirmalar.objects.filter(album=instance).update(album=None)
            Egitimler.objects.filter(album=instance).update(album=None)

        return Response(serializer.data)


class FotoGaleriListView(ListModelMixin, GenericAPIView):
    queryset = FotoGaleri.objects.filter(is_removed=False, durum=True).order_by('-id')
    serializer_class = FotoGaleriSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



## IMAGE

from .models import Image
from .serializers import ImageSerializer

class ImageFilter(filters.FilterSet):
    kategori = filters.NumberFilter(field_name='album__id')  # URL'de kategori olarak geçecek

    class Meta:
        model = Image
        fields = ['kategori']
class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.filter(is_removed=False).select_related('album').order_by('-id')
    serializer_class = ImageSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ImageFilter
    pagination_class = None

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        Image.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)




## FALİYETLER
# SEMPOZYUMLAR

from .models import Sempozyumlar
from .serializers import SempozyumlarSerializer

class SempozyumlarViewSet(viewsets.ModelViewSet):
    queryset = Sempozyumlar.objects.filter(is_removed=False).select_related('album', 'yayin').order_by('-id')
    serializer_class = SempozyumlarSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        Sempozyumlar.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = Sempozyumlar.objects.filter(durum=True,is_removed=False).order_by('-id').select_related('album', 'yayin')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)



# ÇALIŞTAYLAR

from .models import Calistaylar
from .serializers import CalistaylarSerializer

class CalistaylarViewSet(viewsets.ModelViewSet):
    queryset = Calistaylar.objects.filter(is_removed=False).select_related('album', 'yayin').order_by('-id')
    serializer_class = CalistaylarSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        Calistaylar.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = Calistaylar.objects.filter(durum=True,is_removed=False).order_by('-id').select_related('album', 'yayin')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)



# EĞİTİMLER

from .models import Egitimler
from .serializers import EgitimlerSerializer

class EgitimlerViewSet(viewsets.ModelViewSet):
    queryset = Egitimler.objects.filter(is_removed=False).select_related('album', 'yayin').order_by('-id')
    serializer_class = EgitimlerSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        Egitimler.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = Egitimler.objects.filter(durum=True,is_removed=False).order_by('-id').select_related('album', 'yayin')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)




# KONFERANS

from .models import Konferanslar
from .serializers import KonferanslarSerializer

class KonferanslarViewSet(viewsets.ModelViewSet):
    queryset = Konferanslar.objects.filter(is_removed=False).select_related('album', 'yayin').order_by('-id')
    serializer_class = KonferanslarSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        Konferanslar.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = Konferanslar.objects.filter(durum=True,is_removed=False).order_by('-id').select_related('album', 'yayin')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)






# ARAŞTIRMALAR

from .models import Arastirmalar
from .serializers import ArastirmalarSerializer

class ArastirmalarViewSet(viewsets.ModelViewSet):
    queryset = Arastirmalar.objects.filter(is_removed=False).select_related('album', 'yayin').order_by('-id')
    serializer_class = ArastirmalarSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        Arastirmalar.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = Arastirmalar.objects.filter(durum=True,is_removed=False).order_by('-id').select_related('album', 'yayin')
        page = self.paginate_queryset(active)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)



# PUPPUP

from .models import Puppup
from .serializers import PuppupSerializer


class PuppupViewSet(viewsets.ModelViewSet):
    queryset = Puppup.objects.filter(is_removed=False).order_by('-id')
    serializer_class = PuppupSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        Puppup.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = Puppup.objects.filter(durum=True, is_removed=False).order_by('-id')

        # Varsayılan paginasyonu devre dışı bırak
        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)





# SLİDERS
from django.db.models import F


class SlidersViewSet(viewsets.ModelViewSet):
    queryset = Sliders.objects.filter(is_removed=False).order_by('-id')
    serializer_class = SlidersSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        Sliders.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = Sliders.objects.filter(durum=True, is_removed=False).order_by('-id')

        # Varsayılan paginasyonu devre dışı bırak
        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        order = request.data.get('order', None)

        if order is not None:
            existing_slider = Sliders.objects.filter(order=order).first()

            if existing_slider:
                Sliders.objects.filter(order__gte=order).update(order=F('order') + 1)

        # Koddan önce super().create() çağrılarak üst sınıfın create yöntemi çağrılır.
        response = super().create(request, *args, **kwargs)

        return response

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        order = request.data.get('order', None)

        if order is not None and order != instance.order:
            existing_slider = instance

            if existing_slider and isinstance(existing_slider, Sliders):
                if existing_slider.order < int(order):
                    Sliders.objects.filter(order__range=(existing_slider.order, int(order))).exclude(
                        pk=instance.pk).update(
                        order=F('order') - 1)
                elif existing_slider.order > int(order):
                    Sliders.objects.filter(order__range=(int(order), existing_slider.order)).exclude(
                        pk=instance.pk).update(
                        order=F('order') + 1)

        return super().update(request, *args, partial=partial, **kwargs)


# BAŞLIK GÖRSEL

from .models import BalikGorsel
from .serializers import BalikGorselSerializer


class BalikGorselViewSet(viewsets.ModelViewSet):
    queryset = BalikGorsel.objects.filter(is_removed=False).order_by('-id')
    serializer_class = BalikGorselSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            # 'list', 'retrieve' ve 'get_active' için herhangi bir permission gerekmez
            permission_classes = []
        else:
            # Diğer tüm action'lar için IsAuthenticated kullan
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def bulk_soft_delete(self, request):
        ids = request.data.get('ids', [])
        # Güvenli bir şekilde int listesi oluştur
        ids = [int(id) for id in ids if id.isdigit()]
        # Belirtilen ID'lere sahip nesneleri soft delete işlemi ile güncelle
        BalikGorsel.objects.filter(id__in=ids).update(is_removed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_active(self, request):
        active = BalikGorsel.objects.filter(durum=True, is_removed=False).order_by('-id')

        # Varsayılan paginasyonu devre dışı bırak
        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)