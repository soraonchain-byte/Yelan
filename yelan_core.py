def create_file_in_repo(self, repo_name, file_path, content, message="Update by Yelan"):
        """Fungsi khusus untuk menyuntikkan script ke file spesifik"""
        try:
            repo = self.user.get_repo(repo_name)
            try:
                # Jika file sudah ada, kita update
                contents = repo.get_contents(file_path)
                repo.update_file(contents.path, message, content, contents.sha)
                print(f"[+] File {file_path} berhasil diperbarui!")
            except:
                # Jika file belum ada, kita buat baru
                repo.create_file(file_path, message, content)
                print(f"[+] File {file_path} berhasil dibuat!")
            return True
        except Exception as e:
            print(f"[!] Gagal menyuntikkan kode: {e}")
            return False

if __name__ == "__main__":
    # Logic untuk menentukan mode kerja Yelan
    mode = os.getenv('YELAN_MODE', 'CREATE_REPO')
    yelan = YelanCore()

    if mode == 'CREATE_REPO':
        target_name = os.getenv('TARGET_REPO_NAME', 'Project-Alpha')
        yelan.create_turborepo(target_name)
    
    elif mode == 'INJECT_CODE':
        target_repo = os.getenv('TARGET_REPO')
        file_path = os.getenv('FILE_PATH')
        content = os.getenv('CODE_CONTENT')
        yelan.create_file_in_repo(target_repo, file_path, content)
