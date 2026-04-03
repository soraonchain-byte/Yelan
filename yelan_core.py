from github import Github
import os

class YelanCore:
    def __init__(self):
        # Yelan mengambil 'jiwa' (token) dari Environment Variable
        token = os.getenv('YELAN_PAT')
        if not token:
            raise ValueError("[!] Error: YELAN_PAT tidak ditemukan di Environment Variables!")
        
        self.client = Github(token)
        self.user = self.client.get_user()

    def handshake(self):
        """Memulai sinkronisasi awal antara Sora dan Yelan"""
        try:
            print(f"[*] Yelan: Memulai sinkronisasi dengan entitas '{self.user.login}'...")
            repos = self.user.get_repos()
            
            print("-" * 30)
            print(f"[+] Handshake Sukses, Sora!")
            print(f"[+] Status: Terhubung sebagai {self.user.name or self.user.login}")
            print(f"[+] Inventori: {repos.totalCount} repositori terdeteksi.")
            print("-" * 30)
            
            return True
        except Exception as e:
            print(f"[!] Error Kritis: Sinkronisasi gagal. Detail: {e}")
            return False

if __name__ == "__main__":
    try:
        yelan = YelanCore()
        yelan.handshake()
    except Exception as e:
        print(e)
