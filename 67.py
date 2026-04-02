#!/data/data/com.termux/files/usr/bin/python3
import discord
import asyncio
import requests
import sys
import os
import time

class DiscordReporter:
    def __init__(self):
        self.token = None
        self.server_url = None
        self.running = False
        
    def clear(self):
        os.system('clear')
        
    def get_token(self):
        self.clear()
        print("=== Painel de Denúncias Discord ===")
        print("\n[+] Obtenha seu token de conta Discord:")
        print("[*] Acesse: https://discord.com/api/v9/users/@me")
        print("[*] Cole seu token abaixo:")
        self.token = input("> ").strip()
        
        if not self.token:
            print("[-] Token inválido!")
            return False
        return True
    
    def get_server_url(self):
        print("\n[+] Digite o link do servidor:")
        self.server_url = input("> ").strip()
        
        if not self.server_url or not self.server_url.startswith(("http://", "https://")):
            print("[-] URL inválido!")
            return False
        return True
    
    async def send_report(self):
        headers = {
            "Authorization": self.token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        payload = {
            "report_type": "spam",
            "reason": "spamming",
            "timestamp": int(time.time())
        }
        
        try:
            response = requests.post(
                self.server_url, 
                json=payload, 
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"[+] Denúncia enviada: {response.text}")
            else:
                print(f"[!] Erro: {response.text}")
                
        except Exception as e:
            print(f"[X] Erro: {str(e)}")
    
    async def run(self):
        if not self.get_token() or not self.get_server_url():
            return
            
        self.running = True
        print("\n[+] Bot iniciado! Pressione Ctrl+C para sair.")
        
        try:
            while self.running:
                await self.send_report()
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n[+] Parando bot...")
            self.running = False

if __name__ == "__main__":
    reporter = DiscordReporter()
    asyncio.run(reporter.run())
