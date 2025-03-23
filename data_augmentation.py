import os
import random
import cv2
import numpy as np

from utils import get_images, cleanup_dataset_files, kac_veri_var, veri_say


def rotate_image(image, angle):
    """
    Görüntüyü belirtilen açıda döndürür.

    Args:
        image (numpy.ndarray): Döndürülecek görüntü
        angle (int): Dönüş açısı

    Returns:
        numpy.ndarray: Döndürülmüş görüntü
    """
    if image is None:
        raise ValueError("Hata: Görüntü yüklenemedi veya None değeri içeriyor.")

    if angle not in [cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_90_COUNTERCLOCKWISE, cv2.ROTATE_180]:
        raise ValueError(f"Hata: Geçersiz açı değeri ({angle}). Geçerli değerler: "
                         "cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_90_COUNTERCLOCKWISE, cv2.ROTATE_180")

    return cv2.rotate(image, angle)


def add_noise(image):
    """
    Görüntüye tuz-biber gürültüsü ekler.

    Args:
        image (numpy.ndarray): Gürültü eklenecek görüntü

    Returns:
        numpy.ndarray: Gürültü eklenmiş görüntü
    """
    s_vs_p = 0.5
    amount = 0.04


    noisy_image = np.copy(image)


    h, w = image.shape[:2]


    num_salt = int(amount * image.size * s_vs_p)
    salt_coords = np.column_stack(np.random.randint(0, [h, w], size=(num_salt, 2)).T)
    noisy_image[salt_coords[:, 0], salt_coords[:, 1]] = 255


    num_pepper = int(amount * image.size * (1. - s_vs_p))
    pepper_coords = np.column_stack(np.random.randint(0, [h, w], size=(num_pepper, 2)).T)
    noisy_image[pepper_coords[:, 0], pepper_coords[:, 1]] = 0

    return noisy_image


def main():
    cleanup_dataset_files('./dataset')

    allowed_extensions = ['.jpg', '.jpeg', '.png']

    images = get_images()

    for image_path in images:
        _, image_ext = os.path.splitext(image_path)

        if image_ext.lower() not in allowed_extensions:
            print(f"Atlandı: {image_path} - Desteklenmeyen dosya formatı")
            continue

        try:
            np_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            if np_image is None:
                print(f"Okunamadı: {image_path}")
                continue

            angles = [cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_90_COUNTERCLOCKWISE, cv2.ROTATE_180]
            random_angle = random.choice(angles)

            rotated_image = rotate_image(np_image, random_angle)

            noisy_image = add_noise(np_image)

            image_name = os.path.splitext(image_path)[0]

            rotated_filename = f"{image_name}_rotated{image_ext}"
            noisy_filename = f"{image_name}_noisy{image_ext}"

            cv2.imwrite(rotated_filename, rotated_image)
            cv2.imwrite(noisy_filename, noisy_image)

            print(f"İşlendi: {image_path}")

        except Exception as e:
            print(f"Hata oluştu {image_path}: {e}")


if __name__ == '__main__':
    main()
    print(f"Toplam veri sayısı: {veri_say()}")