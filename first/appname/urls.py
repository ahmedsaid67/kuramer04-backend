from django.urls import path, include
from .views import SliderListView, MenuViewSet, MenuItemListCreateView, MenuItemByMenuView, \
    MenuItemDetailView, MenuSelectedItemList, CustomAuthToken, CheckToken, UserInfoView
from rest_framework.routers import DefaultRouter
from .views import PersonelTuruViewSet, PersonellerViewSet, PersonelTuruListView,\
    BrosurlerViewSet,BultenlerViewSet,TemelkonularViewSet,\
    TemelkavramlarViewSet,YayinlarimizdanSecmelerViewSet,YaziliBasinViewSet,\
    GorselBasinViewSet,KamuoyuDuyurulariViewSet,MushafKategoriViewSet,\
    MushafKategoriListView,MushaflarViewSet,MushaffarklariViewSet,KitapKategoriViewSet,\
    KitapKategoriListView,KitaplarViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'menus', MenuViewSet)

router_personel_turu = DefaultRouter()
router_personel_turu.register(r'personelturu', PersonelTuruViewSet)

router_personel = DefaultRouter()
router_personel.register(r'personeller', PersonellerViewSet)

router_brosurler = DefaultRouter()
router_brosurler.register(r'brosurler', BrosurlerViewSet)

router_bultenler = DefaultRouter()
router_bultenler.register(r'bultenler', BultenlerViewSet)

router_temelkonular = DefaultRouter()
router_temelkonular.register(r'temelkonular', TemelkonularViewSet)

router_temelkavramlar = DefaultRouter()
router_temelkavramlar.register(r'temelkavramlar', TemelkavramlarViewSet)

router_yayinlarimizdansecmeler = DefaultRouter()
router_yayinlarimizdansecmeler.register(r'yayinlarimizdansecmeler', YayinlarimizdanSecmelerViewSet)

router_yazilibasin = DefaultRouter()
router_yazilibasin.register(r'yazilibasin', YaziliBasinViewSet)

router_gorselbasin = DefaultRouter()
router_gorselbasin.register(r'gorselbasin', GorselBasinViewSet)

router_kamuoyuduyurulari = DefaultRouter()
router_kamuoyuduyurulari.register(r'kamuoyuduyurulari', KamuoyuDuyurulariViewSet)

router_mushafkategori = DefaultRouter()
router_mushafkategori.register(r'mushafkategori', MushafKategoriViewSet)

router_mushaflar = DefaultRouter()
router_mushaflar.register(r'mushaflar', MushaflarViewSet)

router_mushaffarklari = DefaultRouter()
router_mushaffarklari.register(r'mushaffarklari', MushaffarklariViewSet)

router_kitapkategori = DefaultRouter()
router_mushaffarklari.register(r'kitapkategori', KitapKategoriViewSet)

router_kitaplar = DefaultRouter()
router_mushaffarklari.register(r'kitaplar', KitaplarViewSet)




urlpatterns = [
    # ...
    path('sliders/', SliderListView.as_view(), name='slider-list'),  # SliderListView'ı URL'ye ekleyin

    # menu apileri
    path('menu/', include(router.urls)),
    path('menuitems/', MenuItemListCreateView.as_view(), name='menuitem-list'),
    # Tüm nesneleri sunma için ve yeni öge üretmek
    path('menuitems/menu/<int:menu_id>/', MenuItemByMenuView.as_view(), name='menuitem-by-menu'),
    # Mkullanıcının isteği her hangi bir menünün ögelerini listeler
    path('menuitems/menu/selected/', MenuSelectedItemList.as_view(), name='menuitem-by-menu'),
    # seçili menünün ögeleri listeler
    path('menuitems/<int:pk>/', MenuItemDetailView.as_view(), name='menuitem-detail'),
    # Tekil menu öğelerini sunma için

    # personeller
    path('', include(router_personel_turu.urls)),
    path('personelturu-list/', PersonelTuruListView.as_view(), name='personelturu-list'),
    path('', include(router_personel.urls)),

    ##yayınlar
    #broşürler
    path('', include(router_brosurler.urls)),
    #bültenler
    path('', include(router_bultenler.urls)),

    ##temelkonu ve kavramlar
    #temel konular
    path('', include(router_temelkonular.urls)),
    #temel kavramlar
    path('', include(router_temelkavramlar.urls)),

    ##yayınlarımızdanseçmeler
    path('', include(router_yayinlarimizdansecmeler.urls)),


    ##basında biz
    #yazılı basın
    path('', include(router_yazilibasin.urls)),
    #yazılı basın
    path('', include(router_gorselbasin.urls)),

    #kamuoyu duruyuruları
    path('', include(router_kamuoyuduyurulari.urls)),


    ## mushaflar

    #mushafkategori
    path('', include(router_mushafkategori.urls)),
    path('mushafkategori-list/', MushafKategoriListView.as_view(), name='mushafkategori-list'),

    #mushaflar
    path('', include(router_mushaflar.urls)),

    #mushaffarklari
    path('', include(router_mushaffarklari.urls)),

    #kitaplar
    #kitap kategori
    path('', include(router_kitapkategori.urls)),
    path('kitapkategori-list/', KitapKategoriListView.as_view(), name='kitapkategori-list'),
    #kitaplar
    path('', include(router_kitaplar.urls)),





    # auth apileri
    path('token/', CustomAuthToken.as_view(), name='api-token'),
    path('check-token/', CheckToken.as_view(), name='check-token'),
    path('user-info/', UserInfoView.as_view(), name='user-info'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
