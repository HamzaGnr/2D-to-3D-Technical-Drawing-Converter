import numpy as np
import cv2
import open3d as o3d
from skimage import measure
from technical_drawing_processor import TechnicalDrawingProcessor

class TechnicalDrawingTo3D:
    def __init__(self, image_path: str):
        self.processor = TechnicalDrawingProcessor(image_path)
        self.data = self.processor.process()
        
    def create_profile_mask(self, thickness=100):
        """2D profilden 3D maske oluştur"""
        binary = self.data['binary_image']
        main_contour = self.data['main_contour']
        holes = self.data['holes']
        
        if main_contour is None:
            raise ValueError("Ana profil bulunamadı")
        
        print(f"🔍 Ana profil alanı: {cv2.contourArea(main_contour):.1f}")
        print(f"🕳️ Bulunan delik sayısı: {len(holes)}")
        for i, hole in enumerate(holes):
            print(f"   Delik {i+1}: alan={cv2.contourArea(hole):.1f}")
        
        # Ana profil maskesi - daha büyük canvas kullan
        h, w = binary.shape
        profile_mask = np.zeros((h, w), dtype=np.uint8)
        
        # Ana şekli çiz (beyaz - 255)
        cv2.drawContours(profile_mask, [main_contour], -1, 255, -1)
        
        # Delikleri çiz (siyah - 0) - Ana şeklin içindeki alanları kes
        for i, hole in enumerate(holes):
            print(f"🕳️ Delik {i+1} çiziliyor...")
            cv2.drawContours(profile_mask, [hole], -1, 0, -1)
        
        # Debug: maskeyi kaydet
        cv2.imwrite("debug_profile_with_holes.png", profile_mask)
        
        # Float'a çevir (0.0 - 1.0 aralığı)
        profile_mask = profile_mask.astype(np.float32) / 255.0
        
        # Çok hafif profil temizleme
        kernel_clean = np.ones((2,2), np.uint8)
        profile_mask = cv2.morphologyEx(profile_mask, cv2.MORPH_CLOSE, kernel_clean, iterations=1)
        
        # Çok hafif kenar yumuşatma - ama delikleri koruyacak şekilde
        profile_mask = cv2.GaussianBlur(profile_mask, (3, 3), 0.5)
        
        # Keskin threshold - deliklerin kaybolmaması için
        profile_mask = (profile_mask > 0.3).astype(np.float32)
        
        cv2.imwrite("debug_cleaned_profile.png", (profile_mask * 255).astype(np.uint8))
        print("🧹 Hafif profil temizleme yapıldı")
        
        # Profilde gerçekten delik var mı kontrol et
        unique_values = np.unique(profile_mask)
        print(f"📊 Profil değerleri: {unique_values}")
        white_pixels = np.sum(profile_mask > 0.5)
        total_pixels = profile_mask.size
        hole_ratio = 1.0 - (white_pixels / total_pixels)
        print(f"🕳️ Delik oranı: {hole_ratio:.3f}")
        
        # Grid boyutu
        depth = thickness
        
        # 3D grid oluştur
        voxel_grid = np.zeros((h, w, depth), dtype=np.float32)
        
        # Z ekseni boyunca ekstrüzyon - delikleri koru
        for z in range(depth):
            voxel_grid[:, :, z] = profile_mask.copy()
        
        print(f"🎯 Voxel grid oluşturuldu: {voxel_grid.shape}")
        print(f"🎯 Voxel grid değer aralığı: {np.min(voxel_grid):.2f} - {np.max(voxel_grid):.2f}")
        
        return voxel_grid
    
    def create_mesh(self, voxel_grid):
        """Voxel'lerden mesh oluştur"""
        try:
            # Voxel grid'i kontrol et
            print(f"🔍 Voxel grid analizi:")
            print(f"   Şekil: {voxel_grid.shape}")
            print(f"   Değer aralığı: {np.min(voxel_grid):.3f} - {np.max(voxel_grid):.3f}")
            print(f"   Benzersiz değerler: {np.unique(voxel_grid)}")
            
            # Material alanlarını say
            material_voxels = np.sum(voxel_grid > 0.5)
            hole_voxels = np.sum(voxel_grid <= 0.5) 
            total_voxels = voxel_grid.size
            
            print(f"   Material voxels: {material_voxels:,} ({material_voxels/total_voxels*100:.1f}%)")
            print(f"   Delik voxels: {hole_voxels:,} ({hole_voxels/total_voxels*100:.1f}%)")
            
            # Voxel grid'i düzelt - delikleri GERÇEKTEN boş yap
            print("🔧 Voxel grid'de delikleri açıyoruz...")
            
            main_contour = self.data['main_contour']
            holes = self.data.get('holes', [])
            h, w = voxel_grid.shape[:2]
            depth = voxel_grid.shape[2]
            
            # Yeni voxel grid - baştan oluştur
            corrected_voxel_grid = np.zeros((h, w, depth), dtype=np.float32)
            
            # Ana şekil maskesi
            main_mask = np.zeros((h, w), dtype=np.uint8)
            cv2.drawContours(main_mask, [main_contour], -1, 255, -1)
            
            # Delikleri ana maskeden çıkar
            for hole in holes:
                cv2.drawContours(main_mask, [hole], -1, 0, -1)  # Siyah = delik
                
            # Debug kaydet
            cv2.imwrite("debug_corrected_mask.png", main_mask)
            
            # Float'a çevir
            main_mask = main_mask.astype(np.float32) / 255.0
            
            # 3D ekstrüzyon - delikleri koruyarak
            for z in range(depth):
                corrected_voxel_grid[:, :, z] = main_mask.copy()
            
            # Yeni voxel istatistikleri
            new_material = np.sum(corrected_voxel_grid > 0.5)
            new_holes = np.sum(corrected_voxel_grid <= 0.5)
            print(f"   Düzeltilmiş - Material: {new_material:,} ({new_material/total_voxels*100:.1f}%)")
            print(f"   Düzeltilmiş - Delik: {new_holes:,} ({new_holes/total_voxels*100:.1f}%)")
            
            # Marching cubes ile mesh oluştur
            vertices, faces, _, _ = measure.marching_cubes(
                corrected_voxel_grid, 
                level=0.5,
                spacing=(2.0, 2.0, 2.0)
            )
            
            print(f"🔧 Mesh oluşturuldu: {len(vertices)} vertex, {len(faces)} face")
            
            # Koordinatları merkeze al ve ölçekle
            vertices = vertices - np.mean(vertices, axis=0)
            max_dimension = np.max(np.ptp(vertices, axis=0))
            if max_dimension > 0:
                vertices = vertices * (200.0 / max_dimension)
            
            # Open3D mesh
            mesh = o3d.geometry.TriangleMesh()
            mesh.vertices = o3d.utility.Vector3dVector(vertices)
            mesh.triangles = o3d.utility.Vector3iVector(faces)
            
            # Mesh'i sağlamlaştır
            mesh.remove_degenerate_triangles()
            mesh.remove_duplicated_triangles()
            mesh.remove_duplicated_vertices()
            mesh.remove_non_manifold_edges()
            mesh.compute_vertex_normals()
            
            # Hafif smoothing
            mesh = mesh.filter_smooth_laplacian(number_of_iterations=1, lambda_filter=0.05)
            mesh.compute_vertex_normals()
            
            print(f"🎯 Final mesh: {len(mesh.vertices)} vertex, {len(mesh.triangles)} face")
            
            if mesh.is_watertight():
                print("✅ Mesh kapalı ve sağlam")
            else:
                print("⚠️ Mesh'te açıklar var (deliklerin olması beklenen)")
            
            return mesh
            
        except Exception as e:
            print(f"Mesh oluşturma hatası: {e}")
            return None
    
    def visualize(self, mesh):
        """3D görselleştirme"""
        if mesh is None:
            print("Görselleştirilecek mesh yok")
            return
            
        # Ana mesh'e renk ver
        mesh.paint_uniform_color([0.7, 0.8, 0.9])
        
        # Koordinat eksenleri ekle
        coordinate_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=50)
        
        # Görselleştirme ayarları
        vis = o3d.visualization.Visualizer()
        vis.create_window(window_name="3D Teknik Çizim Modeli - Gerçek Deliklerle", width=1200, height=800)
        vis.add_geometry(mesh)
        vis.add_geometry(coordinate_frame)
        
        # Render ayarları
        render_option = vis.get_render_option()
        render_option.mesh_show_wireframe = False
        render_option.mesh_show_back_face = True
        render_option.light_on = True
        
        # Kamera pozisyonu
        view_control = vis.get_view_control()
        view_control.set_zoom(0.8)
        view_control.rotate(300, 200)
        
        vis.run()
        vis.destroy_window()
    
    def process(self):
        """Ana işlem"""
        print("3D dönüşüm başlıyor...")
        
        # Voxel grid oluştur
        voxel_grid = self.create_profile_mask()
        print(f"Voxel grid: {voxel_grid.shape}")
        
        # Mesh oluştur
        mesh = self.create_mesh(voxel_grid)
        
        if mesh:
            print(f"Mesh oluşturuldu: {len(mesh.vertices)} vertex, {len(mesh.triangles)} face")
            self.visualize(mesh)
        else:
            print("Mesh oluşturulamadı")
        
        return mesh

def main():
    converter = TechnicalDrawingTo3D("new_dataset/autocad-ornek-cizim-kasnak.jpg")
    converter.process()

if __name__ == "__main__":
    main() 