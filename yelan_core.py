import os
from github import Github

class YelanCore:
    def __init__(self):
        # Ambil token dari brankas rahasia
        token = os.getenv('YELAN_PAT')
        if not token:
            raise ValueError("[!] Error: YELAN_PAT tidak ditemukan!")
        self.client = Github(token)
        self.user = self.client.get_user()

    def create_turborepo(self, repo_name):
        """Membangun fondasi Monorepo untuk The Great Nine"""
        try:
            print(f"[*] Yelan: Memulai pembangunan '{repo_name}'...")
            repo = self.user.create_repo(repo_name, private=True)
            
            # Struktur boilerplate awal
            files = {
                "apps/frontend/src/assets/.gitkeep": "Folder untuk Design Figma Sora",
                "apps/backend/main.py": "# Backend Engine for Selena",
                "packages/programs/src/lib.rs": "// Selena Solana Program",
                "turbo.json": '{"pipeline": {"build": {"dependsOn": ["^build"]}}}',
                "README.md": f"# {repo_name}\nCreated by Yelan for Sora Onchain."
            }

            for path, content in files.items():
                repo.create_file(path, f"init: {path}", content)
            
            print(f"[+] Sukses! Repo {repo_name} sudah lahir.")
            return True
        except Exception as e:
            print(f"[!] Gagal build repo: {e}")
            return False

    def create_file_in_repo(self, repo_name, file_path, content, message="Update by Yelan"):
        """Menyuntikkan kode ke file spesifik di repositori tujuan"""
        try:
            # Cari repo target berdasarkan nama (misal: Selena-Agent-Solana)
            # Karena repo mungkin tidak diawali dengan username, kita cari di akun user
            repo = self.client.get_repo(f"{self.user.login}/{repo_name}")
            
            try:
                # Cek jika file sudah ada untuk di-update
                contents = repo.get_contents(file_path)
                repo.update_file(contents.path, message, content, contents.sha)
                print(f"[+] File '{file_path}' di '{repo_name}' berhasil diperbarui!")
            except:
                # Jika file belum ada, buat baru
                repo.create_file(file_path, message, content)
                print(f"[+] File '{file_path}' di '{repo_name}' berhasil dibuat!")
            return True
        except Exception as e:
            print(f"[!] Gagal menyuntikkan kode: {e}")
            return False

if __name__ == "__main__":
    # Inilah otak yang mengatur mode kerja Yelan
    mode = os.getenv('YELAN_MODE', 'CREATE_REPO')
    yelan = YelanCore()

    if mode == 'CREATE_REPO':
        target_name = os.getenv('TARGET_REPO_NAME', 'Project-Alpha')
        yelan.create_turborepo(target_name)
    
    elif mode == 'INJECT_CODE':
        target_repo = os.getenv('TARGET_REPO')
        target_file = os.getenv('FILE_PATH')
        code = os.getenv('CODE_CONTENT')
        
        if target_repo and target_file and code:
            yelan.create_file_in_repo(target_repo, target_file, code)
        else:
            print("[!] Parameter INJECT_CODE tidak lengkap.")
