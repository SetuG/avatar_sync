
import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil
from pathlib import Path

class Wav2LipAvatarGenerator:
    def __init__(self):
        self.base_dir = Path("wav2lip_workspace")
        self.wav2lip_dir = self.base_dir / "Wav2Lip"
        self.models_dir = self.base_dir / "models"
        self.output_dir = self.base_dir / "outputs"
        
      
        self.base_dir.mkdir(exist_ok=True)
        self.models_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
    def check_dependencies(self):
       
      
        
        required = {
            'torch': 'torch',
            'cv2': 'opencv-python',
            'numpy': 'numpy',
            'librosa': 'librosa',
            'scipy': 'scipy',
            'tqdm': 'tqdm',
            'numba': 'numba'
        }
        
        missing = []
        for module, package in required.items():
            try:
                __import__(module)
                print(f" {package}")
            except ImportError:
                print(f" {package} - MISSING")
                missing.append(package)
        
        if missing:
            print(f"\n Missing packages: {', '.join(missing)}")
            print("\nInstall with:")
            print(f"pip install {' '.join(missing)}")
            return False
        
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         capture_output=True, check=True)
            print(" ffmpeg")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(" ffmpeg - MISSING")
            print("\nInstall ffmpeg:")
            print("  • Windows: Download from https://ffmpeg.org")
            print("  • Mac: brew install ffmpeg")
            print("  • Linux: sudo apt install ffmpeg")
            return False
        
        print("\n✓ All dependencies satisfied!\n")
        return True
    
    def setup_wav2lip(self):
        """Download and setup Wav2Lip repository"""
        
        print("SETTING UP WAV2LIP")
        
        
        if self.wav2lip_dir.exists():
            print("Wav2Lip already downloaded")
        else:
            print("None")
            try:
                subprocess.run([
                    'git', 'clone',
                    'https://github.com/Rudrabha/Wav2Lip.git',
                    str(self.wav2lip_dir)
                ], check=True)
                print("Wav2Lip downloaded successfully")
            except subprocess.CalledProcessError:
                print("\n Git not found. Downloading as ZIP...")
                zip_url = "https://github.com/Rudrabha/Wav2Lip/archive/refs/heads/master.zip"
                zip_path = self.base_dir / "wav2lip.zip"
                
                urllib.request.urlretrieve(zip_url, zip_path)
                
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(self.base_dir)
                
                # Rename extracted folder
                (self.base_dir / "Wav2Lip-master").rename(self.wav2lip_dir)
                zip_path.unlink()
                print(" Wav2Lip downloaded and extracted")
    
    def download_model(self):
        """Download pre-trained Wav2Lip model"""
        
        
        model_path = self.models_dir / "wav2lip_gan.pth"
        
        if model_path.exists():
            print(" Model already downloaded")
            return str(model_path)
        
        
        
        
        model_url = "https://iiitaphyd-my.sharepoint.com/personal/radrabha_m_research_iiit_ac_in/_layouts/15/download.aspx?share=EdjI7bZlgApMqsVoEUUXpLsBxqXbn5z8VTmoxp55YNDcIA"
        
        try:
            
            def reporthook(count, block_size, total_size):
                percent = int(count * block_size * 100 / total_size)
                bar_length = 50
                filled = int(bar_length * percent / 100)
                bar = '█' * filled + '░' * (bar_length - filled)
                print(f'\r[{bar}] {percent}%', end='', flush=True)
            
            urllib.request.urlretrieve(model_url, model_path, reporthook)
            print("\n Model downloaded successfully")
            return str(model_path)
            
        except Exception as e:
            
            
            print(f". Place it in: {model_path}")
            return None
    
    def generate_video(self, face_image, audio_file, output_name="result.mp4"):
        """Generate lip-synced video using Wav2Lip"""
        
        print("GENERATING LIP-SYNCED VIDEO")
        
        
        # Validate inputs
        if not os.path.exists(face_image):
            print(f"✗ Error: Face image not found: {face_image}")
            return None
        
        if not os.path.exists(audio_file):
            print(f"✗ Error: Audio file not found: {audio_file}")
            return None
        
        model_path = self.models_dir / "wav2lip_gan.pth"
        if not model_path.exists():
            print("✗ Error: Model not found. Please run setup first.")
            return None
        
        output_path = self.output_dir / output_name
        
        
        inference_script = self.wav2lip_dir / "inference.py"
        
        print(f"Input face: {face_image}")
        print(f"Input audio: {audio_file}")
        print(f"Output: {output_path}\n")
        
        
        cmd = [
            sys.executable,
            str(inference_script),
            '--checkpoint_path', str(model_path),
            '--face', face_image,
            '--audio', audio_file,
            '--outfile', str(output_path),
            '--resize_factor', '1',
            '--nosmooth'  # Remove for smoother results but slower processing
        ]
        
        print("Running Wav2Lip inference...")
        print("This may take a few minutes depending on audio length...\n")
        
        try:
            # Change to Wav2Lip directory for inference
            original_dir = os.getcwd()
            os.chdir(self.wav2lip_dir)
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            os.chdir(original_dir)
            
            if result.returncode == 0:
                print("\n✓ Video generated successfully!")
                print(f"✓ Saved to: {output_path}")
                
                # Check file size
                if output_path.exists():
                    size_mb = output_path.stat().st_size / (1024 * 1024)
                    print(f"✓ File size: {size_mb:.2f} MB")
                
                return str(output_path)
            else:
                print(f"\n✗ Error during generation:")
                print(result.stderr)
                return None
                
        except Exception as e:
            print(f"\n✗ Error: {e}")
            os.chdir(original_dir)
            return None
    
    def quick_setup(self):
        """Quick setup - check everything and download if needed"""
        print("\n" + "="*70)
        print("WAV2LIP PROFESSIONAL TALKING AVATAR GENERATOR")
        print("="*70)
        
        if not self.check_dependencies():
            print("\n⚠ Please install missing dependencies first.")
            return False
        
        self.setup_wav2lip()
        model_path = self.download_model()
        
        if model_path:
            print("\n" + "="*70)
            print("✓ SETUP COMPLETE!")
            print("="*70)
            return True
        return False


def main():
    """Main execution function"""
    
    # Configuration - UPDATE THESE PATHS
    FACE_IMAGE = "unnamed.png"      # Your avatar/face image
    AUDIO_FILE = "Recording (3).mp3"  # Your audio file
    OUTPUT_NAME = "talking_avatar_professional.mp4"
    
    print("\n" + "="*70)
    print("PROFESSIONAL TALKING AVATAR GENERATOR")
    print("Powered by Wav2Lip")
    print("="*70)
    
    # Initialize generator
    generator = Wav2LipAvatarGenerator()
    
    # Run setup (first time only, then cached)
    if not generator.quick_setup():
        print("\n✗ Setup failed. Please fix errors and try again.")
        return
    
    # Validate input files
    if not os.path.exists(FACE_IMAGE):
        print(f"\n✗ Error: Face image not found: {FACE_IMAGE}")
        print("Please update FACE_IMAGE path in the script.")
        return
    
    if not os.path.exists(AUDIO_FILE):
        print(f"\n✗ Error: Audio file not found: {AUDIO_FILE}")
        print("Please update AUDIO_FILE path in the script.")
        return
    
    # Generate video
    result = generator.generate_video(
        face_image=FACE_IMAGE,
        audio_file=AUDIO_FILE,
        output_name=OUTPUT_NAME
    )
    
    if result:
        print("\n" + "="*70)
        print("✓ SUCCESS!")
        print("="*70)
        print(f"\nYour professional talking avatar video is ready:")
        print(f"📁 {result}")
        print("\nThe video includes:")
        print("  ✓ Photorealistic lip movements")
        print("  ✓ Synchronized audio")
        print("  ✓ High-quality output")
        print("\n" + "="*70 + "\n")
    else:
        print("\n✗ Video generation failed. Check errors above.")


if __name__ == "__main__":
    main()