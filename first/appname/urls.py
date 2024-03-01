
from django.urls import path, include
from .views import SlidersViewSet, MenuViewSet, MenuItemListCreateView, MenuItemByMenuView, \
    MenuItemDetailView, MenuSelectedItemViewSet, CustomAuthToken, CheckToken, UserInfoView
from rest_framework.routers import DefaultRouter
from .views import PersonelTuruViewSet, PersonellerViewSet, PersonelTuruListView,\
    BrosurlerViewSet,BultenlerViewSet,TemelkonularViewSet,\
    TemelkavramlarViewSet,YayinlarimizdanSecmelerViewSet,YaziliBasinViewSet,\
    GorselBasinViewSet,KamuoyuDuyurulariViewSet,MushafKategoriViewSet,\
    MushafKategoriListView,MushaflarViewSet,MushaffarklariViewSet,KitapKategoriViewSet,\
    KitapKategoriListView,KitaplarViewSet,VideoGaleriKategoriViewSet,\
    VideoGaleriKategoriListView,VideoGaleri01ViewSet,FotoGaleriKategoriViewSet,FotoGaleriKategoriListView,\
    FotoGaleriViewSet,ImageViewSet,SempozyumlarViewSet,VideoGaleri01ListView,FotoGaleriListView,\
    CalistaylarViewSet,EgitimlerViewSet,KonferanslarViewSet,ArastirmalarViewSet,PuppupViewSet,\
    BalikGorselViewSet,BultenlerListView,Logout



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

router_videogalerikategori = DefaultRouter()
router_videogalerikategori.register(r'videogalerikategori', VideoGaleriKategoriViewSet)

router_videogaleri = DefaultRouter()
router_videogaleri.register(r'videogaleri', VideoGaleri01ViewSet)

router_fotogalerikategori = DefaultRouter()
router_fotogalerikategori.register(r'fotogalerikategori', FotoGaleriKategoriViewSet)

router_fotogaleri = DefaultRouter()
router_fotogaleri.register(r'fotogaleri', FotoGaleriViewSet)

router_image = DefaultRouter()
router_image.register(r'image', ImageViewSet)

router_sempozyumlar = DefaultRouter()
router_sempozyumlar.register(r'sempozyumlar', SempozyumlarViewSet)

router_calistaylar = DefaultRouter()
router_calistaylar.register(r'calistaylar', CalistaylarViewSet)


router_egitimler = DefaultRouter()
router_egitimler.register(r'egitimler', EgitimlerViewSet)


router_konferanslar = DefaultRouter()
router_konferanslar.register(r'konferanslar', KonferanslarViewSet)


router_arastirmalar = DefaultRouter()
router_arastirmalar.register(r'arastirmalar', ArastirmalarViewSet)


router_sliders = DefaultRouter()
router_sliders.register(r'sliders', SlidersViewSet)

router_puppup = DefaultRouter()
router_puppup.register(r'puppup', PuppupViewSet)

router_selectedmenuitems= DefaultRouter()
router_selectedmenuitems.register(r'menuitems/menu/selected', MenuSelectedItemViewSet)


router_baslikgorsel = DefaultRouter()
router_baslikgorsel.register(r'baslikgorsel', BalikGorselViewSet)



urlpatterns = [
    # ...
    #sliders
    path('', include(router_sliders.urls)),

    #selectedmenuitems
    path('', include(router_selectedmenuitems.urls)),



    # menu apileri
    path('menu/', include(router.urls)),

    # menu apileri
    path('menu/', include(router.urls)),
    path('menuitems/', MenuItemListCreateView.as_view(), name='menuitem-list'),
    # Tüm nesneleri sunma için ve yeni öge üretmek
    path('menuitems/menu/<int:menu_id>/', MenuItemByMenuView.as_view(), name='menuitem-by-menu'),


    # personeller
    path('', include(router_personel_turu.urls)),
    path('personelturu-list/', PersonelTuruListView.as_view(), name='personelturu-list'),
    path('', include(router_personel.urls)),
    

    ##yayınlar
    #broşürler
    path('', include(router_brosurler.urls)),
    #bültenler
    path('', include(router_bultenler.urls)),
    path('bultenler-list/', BultenlerListView.as_view(), name='bultenler-list'),




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


    #medyagaleri
    #videogalerikategori
    path('', include(router_videogalerikategori.urls)),
    path('videogalerikategori-list/', VideoGaleriKategoriListView.as_view(), name='medyagalerikategori-list'),
    #videogaleri
    path('', include(router_videogaleri.urls)),
    path('videogaleri-list/', VideoGaleri01ListView.as_view(), name='videogaleri-list'),
    #fotogalerikategori
    path('', include(router_fotogalerikategori.urls)),
    path('fotogalerikategori-list/', FotoGaleriKategoriListView.as_view(), name='fotogalerikategori-list'),
    #fotogaleri
    path('', include(router_fotogaleri.urls)),
    path('fotogaleri-list/', FotoGaleriListView.as_view(), name='fotogaleri-list'),
    #Image
    path('', include(router_image.urls)),


    ##faliyetler
    #sempozyumlar
    path('', include(router_sempozyumlar.urls)),
    #çalıştaylar
    path('', include(router_calistaylar.urls)),
    #çeğitimler
    path('', include(router_egitimler.urls)),
    #konferanslar
    path('', include(router_konferanslar.urls)),
    #arastirmalar
    path('', include(router_arastirmalar.urls)),


    #puppup
    path('', include(router_puppup.urls)),

    #baslikgrosel
    path('', include(router_baslikgorsel.urls)),



    # auth apileri
    path('token/', CustomAuthToken.as_view(), name='api-token'),
    path('check-token/', CheckToken.as_view(), name='check-token'),
    path('user-info/', UserInfoView.as_view(), name='user-info'),
    path('logout/', Logout.as_view(), name='logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
