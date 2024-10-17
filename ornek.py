import pdfplumber
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO
import os

def pdf_kelimeleri_ara_ve_yeni_pdf(pdf_dosya, kelimeler, yeni_pdf):
    aranan_satirlar = []

    try:
        # PDF dosyasını okuma modunda aç
        with pdfplumber.open(pdf_dosya) as pdf:
            toplam_sayfa = len(pdf.pages)

            # Her sayfayı tarama
            for sayfa_numarasi in range(toplam_sayfa):
                sayfa = pdf.pages[sayfa_numarasi]
                sayfa_metni = sayfa.extract_text()

                if sayfa_metni:  # Metin varsa işle
                    satirlar = sayfa_metni.split('\n')
                    
                    # Her kelimeyi tarama
                    for kelime in kelimeler:
                        for satir in satirlar:
                            if re.search(rf'\b{kelime}\b', satir, re.IGNORECASE):
                                aranan_satirlar.append(f"Sayfa {sayfa_numarasi + 1}: {satir}")

    except Exception as e:
        print(f"PDF okuma sırasında bir hata oluştu: {e}")
        return

    try:
        # Arial font dosyasının yolu (sisteminizdeki doğru yolu kullanın)
        font_dosya_yolu = "C:\\Users\\iremb\\OneDrive\\Masaüstü\\Yeni klasör\\arial.ttf"

        # Font dosyasının mevcut olduğundan emin olun
        if not os.path.isfile(font_dosya_yolu):
            print(f"Font dosyası bulunamadı: {font_dosya_yolu}")
            return

        # PDF oluşturma işlemini ByteIO ile yapalım
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        y = height - 40  # Sayfanın üst kısmından başlayarak yazmaya başla
        font_size = 10  # Yazı tipi boyutu
        margin = 40     # Sol ve sağ margin

        # Arial fontunu yükle
        pdfmetrics.registerFont(TTFont('Arial', font_dosya_yolu))
        c.setFont("Arial", font_size)

        for satir in aranan_satirlar:
            satir_length = len(satir) * (font_size / 1.5)  # Tahmini satır uzunluğu
            
            # Satır uzunluğunu sayfanın genişliğine sığdır
            if satir_length > (width - 2 * margin):
                words = satir.split(' ')
                line = ""
                for word in words:
                    if c.stringWidth(line + word, "Arial", font_size) > (width - 2 * margin):
                        c.drawString(margin, y, line)
                        y -= (font_size + 2)  # Satır aralığı
                        line = word + ' '
                        if y < 40:  # Sayfa sonuna geldiysek yeni sayfa ekle
                            c.showPage()
                            c.setFont("Arial", font_size)
                            y = height - 40
                    else:
                        line += word + ' '
                
                # Son satırı da yaz
                if line:
                    c.drawString(margin, y, line)
                    y -= (font_size + 2)
                    
            else:
                if y < 40:  # Sayfa sonuna geldiysek yeni sayfa ekle
                    c.showPage()
                    c.setFont("Arial", font_size)
                    y = height - 40
                c.drawString(margin, y, satir)
                y -= (font_size + 2)

        c.save()

        # ByteIO'dan dosya olarak yazma
        buffer.seek(0)
        with open(yeni_pdf, 'wb') as f:
            f.write(buffer.getvalue())

        buffer.close()
        print(f"{yeni_pdf} dosyası başarıyla oluşturuldu.")

    except Exception as e:
        print(f"PDF oluşturma sırasında bir hata oluştu: {e}")

# PDF dosyası, aranacak kelimeler ve yeni oluşturulacak PDF dosyası
pdf_dosya = "ornek.pdf"
kelimeler = ["TIBBİ SEKRETER"]  # Buraya aramak istediğiniz kelimeleri yazın
yeni_pdf = "aranan_kelimeler.pdf"

# Kelimeleri ara ve yeni PDF'yi oluştur
pdf_kelimeleri_ara_ve_yeni_pdf(pdf_dosya, kelimeler, yeni_pdf)
