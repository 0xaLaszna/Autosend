import os
from datetime import datetime
from colorama import Fore, init
from web3 import Web3
from dotenv import load_dotenv

# membuat variabel dari file .env
load_dotenv()

# Inisialisasi colorama
init(autoreset=True)

# Inisialisasi Web3
web3 = Web3(Web3.HTTPProvider("https://sepolia.infura.io/v3/096ed894233241ecb2e7db47f84505fc"))
sender_address = os.getenv("SENDER_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def tampilkan_menu():
    clear_screen()
    print(Fore.CYAN + "=" * 50)
    print(Fore.GREEN + " SELAMAT DATANG DI FOMO AIRDROP".center(50))
    print(Fore.YELLOW + " Script BY Alazna".center(50))
    print(Fore.CYAN + "=" * 50)
    print(Fore.MAGENTA + "Menu Utama:")
    print(Fore.BLUE + "1. Kirim Ether ke Alamat")
    print(Fore.BLUE + "2. Lihat Log Transaksi")
    print(Fore.RED + "3. Keluar")
    print(Fore.CYAN + "=" * 50)

def kirim_ether():
    print(Fore.YELLOW + "\nMasukkan detail transaksi:")
    while True:
        penerima = input(Fore.CYAN + "Masukkan alamat penerima (atau ketik 'selesai' untuk mengakhiri): ")
        if penerima.lower() == 'selesai':
            break
        jumlah = input(Fore.CYAN + f"Masukkan jumlah Ether yang ingin dikirim ke {penerima} (dalam ETH): ")
        print(Fore.YELLOW + "\nKonfirmasi Transaksi:")
        print(Fore.CYAN + f"Alamat Penerima: {penerima}")
        print(Fore.CYAN + f"Jumlah: {jumlah} ETH")
        konfirmasi = input(Fore.YELLOW + "Apakah Anda yakin ingin melanjutkan? (y/n): ")

        if konfirmasi.lower() == 'y':
            kirim_transaksi(penerima, jumlah)
        else:
            print(Fore.RED + "Transaksi dibatalkan.")
        print(Fore.CYAN + "-" * 50)  # Tambahkan pemisah untuk tiap transaksi

def kirim_transaksi(penerima, jumlah):
    try:
        # Periksa dan set nonce sebelum transaksi
        nonce = web3.eth.getTransactionCount(sender_address)

        # Lakukan transaksi
        transaksi = {
            'nonce': nonce,
            'to': penerima,
            'value': web3.toWei(jumlah, 'ether'),
            'gas': 21000,
            'gasPrice': web3.toWei('50', 'gwei')
        }

        # Tanda tangan transaksi
        signed_tx = web3.eth.account.signTransaction(transaksi, private_key)

        # Kirim transaksi dan ambil hash
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_hash_hex = web3.toHex(tx_hash)
        print(Fore.GREEN + f"Transaksi berhasil dikirim ke {penerima}! Hash: {tx_hash_hex}")

        # Simpan ke log transaksi
        with open("transaction_log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} - Penerima: {penerima}, Jumlah: {jumlah} ETH, Hash: {tx_hash_hex}\n")
    except Exception as e:
        print(Fore.RED + f"Gagal mengirim transaksi: {str(e)}")

def lihat_log():
    clear_screen()
    print(Fore.CYAN + "=" * 50)
    print(Fore.MAGENTA + "Log Transaksi".center(50))
    print(Fore.CYAN + "=" * 50)
    if os.path.exists("transaction_log.txt"):
        with open("transaction_log.txt", "r") as log_file:
            for line in log_file:
                print(Fore.WHITE + line.strip())
    else:
        print(Fore.RED + "Belum ada log transaksi.")
    input(Fore.YELLOW + "\nTekan Enter untuk kembali ke menu utama...")

def main():
    while True:
        tampilkan_menu()
        pilihan = input(Fore.YELLOW + "Pilih opsi: ")
        
        if pilihan == '1':
            kirim_ether()
        elif pilihan == '2':
            lihat_log()
        elif pilihan == '3':
            print(Fore.CYAN + "Keluar dari program. Terima kasih!")
            break
        else:
            print(Fore.RED + "Pilihan tidak valid. Coba lagi.")

if __name__ == "__main__":
    main()
