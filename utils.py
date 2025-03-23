import os
import shutil

def copy_files(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isdir(src_path):
            shutil.copytree(src_path, dest_path)
        else:
            shutil.copy2(src_path, dest_path)

def veri_say():
    resimler = os.listdir("dataset")
    return len(resimler)

import fitz
def pdf_to_images(pdfPath, output_folder, count):
    pdfPath = os.path.join("pdf", pdfPath)
    pdf_document = fitz.open(pdfPath)
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image = page.get_pixmap()
        image_filename = os.path.join(output_folder, f"data_{count}.png")
        image.save(image_filename)
        count += 1
        print(f"{image_filename} kaydedildi.")
    print("Tüm sayfalar başarıyla PNG formatında kaydedildi.")
    pdf_document.close()
    return count

def kac_veri_var():
    print("Kopyalamadan önceki veri sayısı: ", veri_say())
    pdf_paths = ["autocad-210118070151.pdf", "cadexercisedrawing-181123062428.pdf"]
    page_count = 0
    for pdf_path in pdf_paths:
        page_count = pdf_to_images(pdf_path, "dataset2", page_count)

def copy_file():
    source_directory = "dataset2"
    destination_directory = "dataset"

    copy_files(source_directory, destination_directory)
    print(f"'{source_directory}' içeriği '{destination_directory}' klasörüne başarıyla kopyalandı!")


def get_images():
    folder_path = "./dataset"
    images = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
            images += [os.path.join(folder_path, filename)]

    return images


def cleanup_dataset_files(dataset_path):
    # Silinen dosyaların sayısını takip etmek için değişkenler
    rotated_deleted = 0
    noisy_deleted = 0

    # ./dataset klasörünü gezme
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            # Dosya yolunu tam olarak oluşturma
            file_path = os.path.join(root, file)

            # Dosya adında 'rotated.' veya 'noisy.' içeren dosyaları silme
            if 'rotated.' in file or 'noisy.' in file:
                try:
                    os.remove(file_path)

                    # Hangi türden dosya silindiyse ona göre sayacı artırma
                    if 'rotated.' in file:
                        rotated_deleted += 1
                    else:
                        noisy_deleted += 1

                    print(f"Silinen dosya: {file_path}")
                except Exception as e:
                    print(f"Dosya silinemedi {file_path}: {e}")

    # Toplam silinen dosya sayısını raporlama
    print(f"\nToplam silinen dosyalar:")
    print(f"Rotated dosyaları: {rotated_deleted}")
    print(f"Noisy dosyaları: {noisy_deleted}")
    print(f"Toplam: {rotated_deleted + noisy_deleted} dosya silindi.")