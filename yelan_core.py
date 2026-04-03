from github import Github
import os

class YelanCore:
    def __init__(self):
        token = os.getenv('YELAN_PAT')
        if not token:
            raise ValueError("[!] Error: YELAN_PAT tidak ditemukan!")
        self.client = Github(token)
        self.user = self.client.get_user()

    def create_turborepo(self, repo_name):
        """Membangun Monorepo dengan struktur The Great Nine"""
        try:
            print(f"[*] Yelan: Membangun fondasi untuk '{repo_name}'...")
            repo = self.user.create_repo(repo_name, private=True)
            
            # Daftar file boilerplate untuk struktur Turbo Repo
            files_to_create = {
                "apps/frontend/src/assets/.gitkeep": "Folder Desain Figma Sora",
                "apps/backend/main.py": "# Backend Engine",
                "packages/contracts/program.py": "# GenLayer/Solana Scripts",
                "turbo.json": '{"pipeline": {"build": {"dependsOn": ["^build"]}}}',
                "README.md": f"# {repo_name}\nCreated by Yelan for Sora Onchain."
            }

            for path, content in files_to_create.items():
                repo.create_file(path, f"initial commit: {path}", content)
            
            print(f"[+] Sukses! Repositori {repo_name} siap dieksekusi.")
            print(f"[+] Link: {repo.html_url}")
            return True
        except Exception as e:
            print(f"[!] Gagal membangun repo: {e}")
            return False

if __name__ == "__main__":
    # Logic untuk menerima input dari GitHub Actions
    target_name = os.getenv('TARGET_REPO_NAME', 'Project-Alpha')
    yelan = YelanCore()
    yelan.create_turborepo(target_name)
