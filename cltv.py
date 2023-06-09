############################################
# CUSTOMER LIFETIME VALUE (Müşteri Yaşam Boyu Değeri)

# => Customer Life Value : Bir Müşterinin bir şirket ile kurduğu ilişki -iletişim süresince bu şirkete kazandıracağı
# parasal değerdir. Eğer gelecekte müşterilerimizin bize sağlayabileceği değeri belirleyebilirsek, müşterilerimiz ile
# olan ilişkilerimizi düzenleyebiliriz hemde şirket olarak müşteri odaklı orta uzun vadede daha katma değerli yaklaşım
# sergileyebiriz. Bu değerin hesaplanması aynı zamanda pazarlama faaliyetleri alanında ayrılacak olan bütçelerin
# bilrlenmesinde önemli bir rol oynayacaktır. Eğer bu değeri CLTV yi bilirsek mevcut müşteri değerini bilirsek yeni
# müşteri kazanma için harcanacak maliyeti de hesaplarsak var olanlar ile yeni müşteri kazanma için gereken maliyeti
# karşılaştırabilir bilgi edinmiş ve daha sağlıklı bir yaklaşım sergileyebiliriz.

# CUSTOMER LIFETIME VALUE (Müşteri Yaşam Boyu Değeri) Hesaplama
# => Bu hesaplanan değer zaman projeksiyon yönü taşımadığı için ileriyi dönük bir tahinde bulunmamızı sağlamamaktadır.
# Ama mevcut müşterilerin değeerlerinin belirlenmesi açısından oldukça değerli bir çalışma olacaktır.

#                   Bilgiler

# Churn Rate: Müşteri Terk oranıdır. Bu bir sabit değerdir. Şirkete göre değişmektedir.
# Churn Rate = 1 - Repeat Rate
# Profit Margin: Şirketin müşteriler ile yaptığı alışverişlerde var sayacağı bir kar miktarı olacaktır.
# Profit Margin = Total Price * 0.10
# Total Numer of Customer = Toplam Müşteri sayısı
# Repeat Rate = Tekrar oranıdır. Yani Retansion rate dir. Elde tutma oranıdır. Bir müşteri birden fazla alışveriş
# yaptığında elde tutulan müşteridir.

# Bir Örnek üzerinden bu işlemleri kullnarak bir CLTV hesabı yapalım.
# Total Number of Customer = 100
# Churn Rate= 0.8
# Profit = 0.10

#                               Müşteri
#           İşlemler(Transaction)                Ücretler(Price)
#                   1                                   300
#                   2                                   400
#                   3                                   500
#  Toplam           3                                   1200

# 1 => Average Order Value = Total Price / Tatal Transaction = 1200 / 3 = 400
# 2 => Purchase Frequency  = Total Transaction / Total Number Of Customers = 3 / 100 = 0.03
# 3 => Profit Margin = Total Price * 0.10 = 1200 * 0.10 = 120
# 4 => Customer Value = Average Order Value  * Purchase Frequency = 400 * 0.03 = 12
# 5 => CLTV (customer life time value) = ( Customer Value / Churn Rate ) * Profit Margin = (12 / 0.8) * 120 = 1800


############################################

# 1. Veri Hazırlama
# 2. Average Order Value (average_order_value = total_price / total_transaction)
# 3. Purchase Frequency (total_transaction / total_number_of_customers)
# 4. Repeat Rate & Churn Rate (birden fazla alışveriş yapan müşteri sayısı / tüm müşteriler)
# 5. Profit Margin (profit_margin =  total_price * 0.10)
# 6. Customer Value (customer_value = average_order_value * purchase_frequency)
# 7. Customer Lifetime Value (CLTV = (customer_value / churn_rate) x profit_margin)
# 8. Segmentlerin Oluşturulması
# 9. BONUS: Tüm İşlemlerin Fonksiyonlaştırılması

##################################################
# 1. Veri Hazırlama
##################################################

# Veri Seti Hikayesi
# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

# Online Retail II isimli veri seti İngiltere merkezli online bir satış mağazasının
# 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.

# Değişkenler
# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
# Description: Ürün ismi
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihi ve zamanı.
# UnitPrice: Ürün fiyatı (Sterlin cinsinden)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke.

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x) # burada folat formatında olan değerlerin noktadan sonra kaç
# basamağının gösterileceğini tanımladık.
pd.set_option("display.width", 200)

df_ = pd.read_excel("online_retail_II.xlsx", sheet_name="Year 2009-2010") # burada veri seti okunarak df_ değişkenine
# atanıp programa dahil edildi.
df = df_.copy() # burada df_ değişkeni üzerinden veri setinin bir kopyası alındı. böylelikle ilerleyen zamanlarda
# yaptığımız işlemlerde veri seti üzerinde bir hata yapar ve yapısını bozarsak df_ den tekrar koya alıp hızlıca devam
# edebiliriz.
df.head()

df.shape

df.isnull().sum() # veri seti içerisinde kaç tane eksik veri var onları tespit ettik.

df = df[~df["Invoice"].str.contains("C", na=False)] # burada veri seti içerisindeki Invoice değişkeninde c ifadesini
# bulundurmayanların seçimi yapıldı. böylelikle iade edilmiş fatura numaralarından veri içerisinde kurtulmuş olduk.

df.describe().T # burada veri setinin betimsel özetine baktık

df[(df["Quantity"]) < 0] # bu kod çalıştırıldığında satış adedi eksi olanları ekrana getirecektir. Fakat çalıştığında
# kalıcı bir şey olmayacaktır atama yapmadığımız için. Ama aşağıdaki kodu çalıştırdığımızda ise kalıcı bir hale getirmiş
# olacağız.

df = df[(df['Quantity'] > 0)] #burada veri seti içersinden satış adedi olan quantity sütununun gözlem sayısı 0 dan
# yüksek olan yani eksi olmayanları seçtik. satış adedi eksi olamayacağı için bunları veri setinden atmış olduk. eksiler
# iade olanları temsil ediyor. biz ise satınlar ile ilgileniyor şu aşamada. bu seçimi tekrar df değişkenine atadık.

df.dropna(inplace=True)  # burada veri seti içerisinde eksik verileri veri setinden atmış oluyoruz. inplace ile de
# kalıcı hale getirdik.

df["TotalPrice"] = df["Quantity"] * df["Price"] # burada toplam fiyat bilgisini hesapladık ve bunu da df veri seti
# içerisine yeni bir sütun olarak yerleştirdik. toplam fiyatı ise satılan ürün adedi ile bir ürüne ödenen bşrşm fiyat
# ile çarpılarak tüm ürünlere uygunıp veri seti içerisine eklenmiştir.

cltv_c = df.groupby('Customer ID').agg({'Invoice': lambda Invoice: Invoice.nunique(),
                                        'Quantity': lambda Quantity: Quantity.sum(),
                                        'TotalPrice': lambda TotalPrice: TotalPrice.sum()})
cltv_c
# yukarıdaki kodda cltv_c isminde bir değişken oluşturuldu. bu değişkende ki c ifadesi calculate ifadesinin ilk harfidir
# yukarıda ki kodu satır satır açıklamak gerekirse: veri seti groupby ile Customer ID özelinde kırıldı. amacımız çoklu
# durumda olan Customer Id ileri tekilleştirmiş olduk. Bu kırılım yapıldıktan sonra agg fonksiyonu ile Invoıce (fatura)
# değişkeninin eşsiz sınıf sayısı yani farklı fatura sayısını hesapladık. Daha sonra Quantity (satış adedi ) toplam
# adedini hesapladık. Daha sonra .TotlaPrize (toplam paranın) toplamını hesapladık. bub hesaplamları da cltv_c
# değişkenine atadık.

cltv_c.columns = ['total_transaction', 'total_unit', 'total_price'] # burada ise bu cltv_c dataframe inin sütunlarının
# isimlerini değiştirdik. amacımız formüllerdeki isimler ile aynı olmasıdır. böylelikle hem literatüre bağlı kalmış
# olacağız hemde hesaplama yaparken daha okunabilir olacaktır.

##################################################
# 2. Average Order Value (average_order_value = total_price / total_transaction)
##################################################

cltv_c.head()
cltv_c["average_order_value"] = cltv_c["total_price"] / cltv_c["total_transaction"] # burada average order value
# değerini hesapladık. cltv_c veri seti içersinde average_order_value isminde bir değişken oluşturduk ve bu değişkene de
# cltv_c veri seti içerisinde yer alan total price değişkeninin total transaction değişkenine bölümünden elde edilen
# sonucu atadık.

##################################################
# 3. Purchase Frequency (total_transaction / total_number_of_customers)
##################################################

cltv_c.head()
cltv_c.shape[0] # burada şunu tespit ettik: shape ile bu veri setinin hem gözlem sayısını hemde değişken sayısını tespit
# ediyorduk. biz burada shape[0] ifadesi ile toplam gözlem sayısını almış olduk. bu şu demek: toplam gözlem sayısı aynı
# zamanda bizim toplam müşteri sayımız demektir.

cltv_c["purchase_frequency"] = cltv_c["total_transaction"] / cltv_c.shape[0] # burada cltv_c veri seti içerisine
# purchase_frequency isimnde bir değişken yerleştirilip bu değişkene de toplam fatura sayısının toplam müşteri sayısına
# bölümünden elde edilen sonuç her kişi özelinde eklenmiştir.

##################################################
# 4. Repeat Rate & Churn Rate (birden fazla alışveriş yapan müşteri sayısı / tüm müşteriler)
##################################################

repeat_rate = cltv_c[cltv_c["total_transaction"] > 1].shape[0] / cltv_c.shape[0] # burada birden fazla alışveriş yapma
# oranını hesapladık. repeat_rate isminde bir değişken oluşturduk. bu değişkene de total_transaction sütununda yer alan
# gözlemlerden 1 den büyük olanların sayısının aldık. önce 1 den büyük olanları seçtik sonra da bunları shape[0] ile de
# sıfırıncı index de yer alan sayıyı aldık. bu yöntem ile 1 den büyük olan fatura sayılarının toplamını almış olduk. bu
# değeri de cltv_c dataframe nin shape[0] ile elde ettiğimiz değere böldük. cltv_c.shape[0] şu demek bu veri setinin
# gözlem sayısı demek. bu toplam müşteri sayısı demek. yani farklı customer ıd sayısının toplamı demek.

repeat_rate # bu değer en az 2 tane alışveriş yapmış olan yani artık bizim müşterimiz olarak kabul edebileceğimiz, yani
# retantion elde tuttuğumuz müşteri olarak kabul edebilecek orandır bu değer.

churn_rate = 1 - repeat_rate # burada bizden ayrılacak müşteri oranını tespit ettik.

##################################################
# 5. Profit Margin (profit_margin =  total_price * 0.10)
##################################################

cltv_c['profit_margin'] = cltv_c['total_price'] * 0.10 # burada cltv_c veri setine profit_margin isminde bir değişken
# sütun ekliyoruz. bu sütuna ise aynı veri seti içerisinde yer alan total_price değişkeninin 0.10 ile çarpımından elde
# edilen sonucu yazıyoruz.


##################################################
# 6. Customer Value (customer_value = average_order_value * purchase_frequency)
##################################################

cltv_c['customer_value'] = cltv_c['average_order_value'] * cltv_c["purchase_frequency"] # burada cltv_c veri seti
# içerisine customer_value isimnde bir değişken sütun oluşturuluyor bu sütuna da aynı veri seti içersinde yer alan
# average_order_value sütunun değeri ile purchase_frequency sütunun değeri çarpılarak ekleniyor.

##################################################
# 7. Customer Lifetime Value (CLTV = (customer_value / churn_rate) x profit_margin)
##################################################

cltv_c["cltv"] = (cltv_c["customer_value"] / churn_rate) * cltv_c["profit_margin"] # burada ise bu cltv_c veri seti
# içerisine bir değişken bir sütun ekliyoruz. bu deişkene ise aynı veri seti içerisinde yer alan customer_value sütunun
# da yer alan değerin churn_rate değerine bölünerek elde edilen değerin aynı veri seti içerisinde yer alan profit_margin
# sütunu içerisinde yer alan değerler ile çarpılması sonucu elde edilen değerin yazılması ile elde ediliyor.
# sonuç olarak müşteri özelined istediğimiz değeri cltv değerini elde etmiş olduk.

cltv_c.sort_values(by="cltv", ascending=False).head() # burada cltv_c veri setini büyükten küçüğe doğru sırala dedik ama
# bu sıralamayı yaparken de cltv sütununu baz al yani o sütuna göre üyükten küçüğe doğru sıralama yap dedik.


##################################################
# 8. Segmentlerin Oluşturulması
##################################################
# burada müşterileri segmentlere ayıracağız. Bunu yapmamızın sebebi ise müşteri kırılımında okunabilirliği artırmak ve
# müşteriler ile ilgili çalışmalar yaparken daha sağlıklı kararlar vermemizi sağlayacaktır.

cltv_c.sort_values(by="cltv", ascending=False).tail() # burada cltv_c veri setini büyüktek küçüğe doğru cltv değişkenini
# baz alarak sıralama yaptık. Bu sıralamanın son 5 gözlemini ekrana yazdırdık.

cltv_c["segment"] = pd.qcut(cltv_c["cltv"], 4, labels=["D", "C", "B", "A"]) # burada cltv_c veri seti içerisine segment
# isminde bir değişken sütun ekledik. bu sütuna ise qcut fonksiyonu ile 4 e bölüp parçaların isimlerini de labels
# listesi içerisinde aldığımız ifadeleri ekledik.
# Bilgi: qcut fonksiyonu cltv_c veri seti içerisindeki cltv sütununu 4 e böldü ve küçükten büyüğe doğru sıraladı. Bu
# bölüm ile elde edilen parçalara da sırası ile labels içerisinde yer alan harfler atandı.Bu şekilde yaparak cltv
# sütununda sayısal bir değer varken artık bu işlem sonrasında harf olarak segment lere ayrılmış olaca böylelikle
# okunabilirliği artırmış olacağız.

cltv_c.sort_values(by="cltv", ascending=False).head() # burada cltv_c vedri seti cltv sütunu baz alınarak büyükten
# küçüğe doğru sıralandı. ama kalıcı olarak bir değişkene atanmadı. Burada en büyük segment A, sırası ile B, C, D dir.

cltv_c.groupby("segment").agg({"count", "mean", "sum"})# burada cltv_c değişkeni segment bazında groupby ile kırıldı.
# bu kırılım sonunda agg fonksiyonu ile de veri seti içerisinde yer alan her bir değişkene count, mean, sum
# fonskiyonları uygulandı. Ama kalıcı olarak veri seti içerisine kaydedilmedi.

cltv_c.to_csv("cltc_c.csv") # burada ise bu cltv_c veri seti csv dosya formatına dönüştürülüp dışarı çıkarıldı.

# 18102.00000       A
# 14646.00000       A
# 14156.00000       A
# 14911.00000       A
# 13694.00000       A

# Customer ID
# 18102.00000       A
# 14646.00000       A
# 14156.00000       A
# 14911.00000       A
# 13694.00000       A

##################################################
# 9. BONUS: Tüm İşlemlerin Fonksiyonlaştırılması
##################################################

def create_cltv_c(dataframe, profit=0.10):

    # Veriyi hazırlama
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[(dataframe['Quantity'] > 0)]
    dataframe.dropna(inplace=True)
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    cltv_c = dataframe.groupby('Customer ID').agg({'Invoice': lambda x: x.nunique(),
                                                   'Quantity': lambda x: x.sum(),
                                                   'TotalPrice': lambda x: x.sum()})
    cltv_c.columns = ['total_transaction', 'total_unit', 'total_price']
    # avg_order_value
    cltv_c['avg_order_value'] = cltv_c['total_price'] / cltv_c['total_transaction']
    # purchase_frequency
    cltv_c["purchase_frequency"] = cltv_c['total_transaction'] / cltv_c.shape[0]
    # repeat rate & churn rate
    repeat_rate = cltv_c[cltv_c.total_transaction > 1].shape[0] / cltv_c.shape[0]
    churn_rate = 1 - repeat_rate
    # profit_margin
    cltv_c['profit_margin'] = cltv_c['total_price'] * profit
    # Customer Value
    cltv_c['customer_value'] = (cltv_c['avg_order_value'] * cltv_c["purchase_frequency"])
    # Customer Lifetime Value
    cltv_c['cltv'] = (cltv_c['customer_value'] / churn_rate) * cltv_c['profit_margin']
    # Segment
    cltv_c["segment"] = pd.qcut(cltv_c["cltv"], 4, labels=["D", "C", "B", "A"])

    return cltv_c


df = df_.copy()

clv = create_cltv_c(df)

























