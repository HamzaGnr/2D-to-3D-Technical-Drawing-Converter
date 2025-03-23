import numpy as np
import cv2
import open3d as o3d
from skimage import measure
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class TechnicalDrawingTo3D:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if self.image is None:
            raise ValueError("Görüntü yüklenemedi")
        
    def preprocess_image(self):
        """Görüntüyü işleme hazırlık"""
        # Görüntüyü ikili formata dönüştür
        _, binary = cv2.threshold(self.image, 127, 255, cv2.THRESH_BINARY_INV)
        # Gürültüyü temizle
        kernel = np.ones((3,3), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        return binary

    def extract_profile(self, binary_image):
        """Teknik çizimden profil çıkar"""
        # Konturları bul
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            raise ValueError("Kontur bulunamadı")
        
        # En büyük konturu al
        main_contour = max(contours, key=cv2.contourArea)
        
        # Kontur noktalarını düzleştir ve basitleştir
        epsilon = 0.01 * cv2.arcLength(main_contour, True)
        approx_contour = cv2.approxPolyDP(main_contour, epsilon, True)
        
        # Kontur sınırlarını al
        x, y, w, h = cv2.boundingRect(approx_contour)
        
        # Profil maskesi oluştur
        mask = np.zeros_like(binary_image)
        cv2.drawContours(mask, [approx_contour], -1, (255), -1)
        
        return {
            'contour': approx_contour,
            'mask': mask,
            'bounds': (x, y, w, h)
        }

    def create_voxel_grid(self, profile_data):
        """Profilden voxel grid oluştur"""
        mask = profile_data['mask']
        x, y, w, h = profile_data['bounds']
        
        # Grid boyutlarını ayarla
        scale = 2  # Çözünürlük için ölçek faktörü
        width = w * scale
        height = h * scale
        depth = min(w, h) * scale
        
        # Maske boyutunu yeniden boyutlandır
        mask_resized = cv2.resize(mask[y:y+h, x:x+w], (width, height))
        
        # 3B grid oluştur
        voxel_grid = np.zeros((height, width, depth))
        
        # Profili 3B'ye dönüştür
        for z in range(depth):
            # Profil maskesini kullan
            layer = mask_resized.copy()
            # Derinlik boyunca değişen yoğunluk
            depth_factor = 1.0 - (abs(z - depth//2) / (depth//2))
            voxel_grid[:, :, z] = (layer > 0) * depth_factor
            
        return voxel_grid

    def create_mesh_from_voxels(self, voxel_grid):
        """Voxel'lerden mesh oluştur"""
        try:
            vertices, faces, normals, _ = measure.marching_cubes(voxel_grid, level=0.3)
            
            # Open3D mesh oluştur
            mesh = o3d.geometry.TriangleMesh()
            mesh.vertices = o3d.utility.Vector3dVector(vertices)
            mesh.triangles = o3d.utility.Vector3iVector(faces)
            mesh.compute_vertex_normals()
            
            # Mesh'i düzgün yönlendir
            mesh.orient_triangles()
            
            return mesh
        except RuntimeError as e:
            print(f"Mesh oluşturma hatası: {e}")
            return None

    def visualize_3d_model(self, mesh):
        """3B modeli görselleştir"""
        if mesh is None:
            print("Görselleştirilecek mesh bulunamadı")
            return
            
        # Mesh'i görselleştirmeden önce normalize et
        mesh.normalize_normals()
        
        # Görselleştirme seçeneklerini ayarla
        vis = o3d.visualization.Visualizer()
        vis.create_window()
        
        # Mesh'i ekle ve ayarları yapılandır
        vis.add_geometry(mesh)
        opt = vis.get_render_option()
        opt.mesh_show_back_face = True
        opt.background_color = np.array([1, 1, 1])  # Beyaz arkaplan
        opt.mesh_shade_option = o3d.visualization.MeshShadeOption.Color
        
        # Kamera kontrolü
        ctr = vis.get_view_control()
        ctr.set_zoom(0.8)
        ctr.set_front([0, 0, -1])
        ctr.set_up([0, 1, 0])
        
        vis.run()
        vis.destroy_window()

    def process(self):
        """Ana işlem akışı"""
        binary = self.preprocess_image()
        profile_data = self.extract_profile(binary)
        voxel_grid = self.create_voxel_grid(profile_data)
        mesh = self.create_mesh_from_voxels(voxel_grid)
        self.visualize_3d_model(mesh)

def main():
    # Örnek kullanım
    converter = TechnicalDrawingTo3D("dataset/data_4.png")
    converter.process()

if __name__ == "__main__":
    main() 