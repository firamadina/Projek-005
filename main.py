import time
import random

def slow(text, delay=0.03):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()

def pertarungan(pemain, musuh_nama, musuh_hp, musuh_atk):
    slow(f"Bertempur melawan {musuh_nama}!")
    while pemain['hp'] > 0 and musuh_hp > 0:
        aksi = input("Pilih aksi (serang / kabur): ").strip().lower()
        if aksi == 'serang':
            dmg = max(1, pemain['atk'] + random.randint(-2, 2))
            musuh_hp -= dmg
            slow(f"Kamu menyerang {musuh_nama} dan memberi {dmg} kerusakan.")
        elif aksi == 'kabur':
            if random.random() < 0.5:
                slow("Kamu berhasil kabur!")
                return False
            else:
                slow("Gagal kabur!")
        else:
            slow("Aksi tidak dikenal. Gunakan 'serang' atau 'kabur'.")
            continue

        if musuh_hp > 0:
            dmg_m = max(1, musuh_atk + random.randint(-1, 2))
            pemain['hp'] -= dmg_m
            slow(f"{musuh_nama} menyerang dan memberi {dmg_m} kerusakan. (HP kamu: {pemain['hp']})")

    if pemain['hp'] > 0:
        slow(f"{musuh_nama} dikalahkan!")
        return True
    else:
        slow("Kamu tumbang... Petualangan berakhir.")
        return False

def game_utama():
    slow("--- MEMULAI PETUALANGAN ANTARIKSA ---", 0.01)
    nama = input("Masukkan nama MC kamu: ").strip() or 'MC'
    slow(f"Halo, {nama}. Kamu memasuki dungeon luar angkasa mencari bintang Canopus.")

    pemain = {'hp': 40, 'atk': 6}

    slow("Di depanmu ada dua jalur: Venus dan Mars.")
    pilihan = input("Pilih jalur ('Venus' atau 'Mars'): ").strip().lower()

    if pilihan == 'venus':
        slow("Kamu memilih jalur Venus — penuh kabut asam dan alien cepat.")
        encounters = [
            ('Alien Raptor', 10, 4),
            ('Drone Asam', 12, 5)
        ]
    else:
        slow("Kamu memilih jalur Mars — reruntuhan dan alien berat.")
        encounters = [
            ('Guerilla Mars', 12, 5),
            ('Behemoth Kecil', 14, 6)
        ]

    for nama_m, hp_m, atk_m in encounters:
        ok = pertarungan(pemain, nama_m, hp_m, atk_m)
        if not ok:
            slow("Kamu gagal melanjutkan. Coba lagi lain waktu.")
            return

    slow("Kamu sampai di ruangan raja — Taurus, Raja Alien.")
    ok = pertarungan(pemain, 'Taurus', 28, 8)
    if ok:
        slow("Selamat! Kamu mengalahkan Taurus dan mendapatkan bintang Canopus.")
        slow("Misi selesai — kamu keluar dari dungeon dengan kemenangan.")
    else:
        slow("Taurus terlalu kuat. Petualangan berakhir.")

if __name__ == "__main__":
    game_utama()