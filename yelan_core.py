import os
from github import Github

class YelanCore:
    def __init__(self):
        token = os.getenv('YELAN_PAT')
        if not token:
            raise ValueError("[!] Error: YELAN_PAT missing!")
        self.client = Github(token)
        self.user = self.client.get_user()

    def create_turborepo(self, repo_name):
        """Membangun fondasi Monorepo untuk The Great Nine"""
        try:
            print(f"[*] Yelan: Attempting to create '{repo_name}'...")
            # Gunakan try-except spesifik untuk menangkap error perizinan
            repo = self.user.create_repo(repo_name, private=True)
            
            files = {
                "apps/frontend/src/assets/.gitkeep": "Folder for Sora's Figma Designs",
                "apps/backend/main.py": "# Backend Engine for Selena",
                "packages/programs/src/lib.rs": "// Selena Solana Program",
                "turbo.json": '{"pipeline": {"build": {"dependsOn": ["^build"]}}}',
                "README.md": f"# {repo_name}\nCreated by Yelan for Sora Onchain."
            }

            for path, content in files.items():
                repo.create_file(path, f"init: {path}", content)
            
            print(f"[+] SUCCESS: Repo '{repo_name}' is live!")
            return True
        except Exception as e:
            # Ini akan membuat workflow gagal (Merah) jika repo tidak tercipta
            print(f"[!] CRITICAL ERROR: {e}")
            raise e 

    def inject_code(self, repo_name, file_path, content):
        """Menyuntikkan kode ke repo spesifik"""
        try:
            repo = self.client.get_repo(f"{self.user.login}/{repo_name}")
            try:
                contents = repo.get_contents(file_path)
                repo.update_file(contents.path, "Update by Yelan", content, contents.sha)
                print(f"[+] SUCCESS: '{file_path}' updated!")
            except:
                repo.create_file(file_path, "Created by Yelan", content)
                print(f"[+] SUCCESS: '{file_path}' created!")
            return True
        except Exception as e:
            print(f"[!] INJECTION FAILED: {e}")
            raise e

if __name__ == "__main__":
    mode = os.getenv('YELAN_MODE', 'CREATE_REPO')
    yelan = YelanCore()

    if mode == 'CREATE_REPO':
        name = os.getenv('TARGET_REPO_NAME', 'New-Project')
        yelan.create_turborepo(name)
    elif mode == 'INJECT_CODE':
        target = os.getenv('TARGET_REPO')
        path = os.getenv('FILE_PATH')
        code = os.getenv('CODE_CONTENT')
        yelan.inject_code(target, path, code)
