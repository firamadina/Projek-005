import time
import random
import sys

def slow(text, delay=0.02):
    for ch in str(text):
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()

def header():
    print('🚀' + '-'*50 + '🪐')
    slow('   ✨ PETUALANGAN ANTARIKSA: MENCARI BINTANG CANOPUS ✨', 0.005)
    print('👾' + '-'*50 + '👾')

def status(pemain):
    slow(f"[STATUS] HP: {pemain['hp']}  ATK: {pemain['atk']}  NYAWA: {pemain['nyawa']} ⭐")

def pertarungan(pemain, musuh_nama, musuh_hp, musuh_atk):
    slow(f"\n⚔️  Bertemu: {musuh_nama} (HP {musuh_hp}, ATK {musuh_atk})")
    while pemain['hp'] > 0 and musuh_hp > 0:
        status(pemain)
        aksi = input("Aksi kamu (serang / bertahan / kabur): ").strip().lower()
        if aksi == 'serang':
            dmg = max(1, pemain['atk'] + random.randint(-2, 2))
            musuh_hp -= dmg
            slow(f"➡️  Kamu menyerang {musuh_nama} dan memberi {dmg} kerusakan.")
        elif aksi == 'bertahan' or aksi == 'defend':
            slow("🛡️  Kamu bertahan, mengurangi serangan musuh berikutnya.")
            dmg_m = max(0, musuh_atk + random.randint(-1, 1) - 3)
            pemain['hp'] -= dmg_m
            slow(f"{musuh_nama} menyerang dan memberi {dmg_m} kerusakan. (HP kamu: {pemain['hp']})")
            continue
        elif aksi == 'kabur':
            if random.random() < 0.6:
                slow("🏃‍♂️ Kamu berhasil kabur dari pertempuran!")
                return False
            else:
                slow("❌ Gagal kabur!")
        else:
            slow("⚠️ Pilihan tidak dikenali.")
            pemain['nyawa'] -= 20
            slow(f"Nyawa berkurang 20. Sisa nyawa: {pemain['nyawa']}")
            if pemain['nyawa'] <= 0:
                slow("💀 Nyawa habis... Petualangan berakhir.")
                return False
            continue

        if musuh_hp > 0:
            dmg_m = max(1, musuh_atk + random.randint(-1, 2))
            pemain['hp'] -= dmg_m
            slow(f"{musuh_nama} membalas dan memberi {dmg_m} kerusakan. (HP kamu: {pemain['hp']})")

    if pemain['hp'] > 0:
        slow(f"🏆 {musuh_nama} dikalahkan!")
        # reward kecil
        pemain['atk'] += 1
        slow(f"Kamu mendapatkan pengalaman, ATK +1 (sekarang {pemain['atk']}).")
        return True
    else:
        slow("💀 Kamu tumbang... Petualangan berakhir.")
        return False

def game_utama():
    header()
    slow("Di masa depan, galaksi terpecah oleh perang korporasi antarplanet.")
    slow("Kamu adalah MC — seorang penjelajah yang ditugaskan memasuki dungeon ruang angkasa")
    slow("yang konon menyimpan bintang legendaris: Canopus. Tanpa Canopus, stasiunmu akan hancur.")
    nama = input("Masukkan nama MC kamu: ").strip() or 'MC'
    slow(f"Selamat datang, {nama}. Misimu: temukan Canopus dan pulang hidup-hidup.")

    pemain = {'hp': 40, 'atk': 6, 'nyawa': 100}
    status(pemain)

    slow("\nDi mulut dungeon, ada dua jalur bercabang:")
    slow("🟣  Venus — kabut asam, alien lincah, jebakan kimia.")
    slow("🔴  Mars  — reruntuhan besi, alien berat, medan berbahaya.")
    pilihan = input("Pilih jalur ('Venus' atau 'Mars'): ").strip().lower()

    if pilihan == 'venus':
        slow("Kamu melangkah ke Venus. Aroma asam menggigit helmmu.")
        encounters = [
            ('Alien Raptor', 10, 4),
            ('Drone Asam', 12, 5)
        ]
    elif pilihan == 'mars':
        slow("Kamu turun ke reruntuhan Mars. Debu merah menerjang.")
        encounters = [
            ('Guerilla Mars', 12, 5),
            ('Behemoth Kecil', 14, 6)
        ]
    else:
        slow("⚠️ Pilihan tidak valid — kamu kehilangan fokus dan tersesat sejenak!")
        pemain['nyawa'] -= 20
        slow(f"Nyawa berkurang 20. Sisa nyawa: {pemain['nyawa']}")
        if pemain['nyawa'] <= 0:
            slow("💀 Nyawa habis... Petualangan berakhir.")
            return
        slow("Sistem auto-navigasi memilihkan jalur aman: Mars.")
        encounters = [
            ('Guerilla Mars', 12, 5),
            ('Behemoth Kecil', 14, 6)
        ]

    slow('\n-- Perjalanan Dimulai --')
    for nama_m, hp_m, atk_m in encounters:
        ok = pertarungan(pemain, nama_m, hp_m, atk_m)
        if not ok:
            slow("Kamu tidak dapat melanjutkan perjalanan.")
            return
        if pemain.get('nyawa', 0) <= 0:
            slow("Nyawa kamu habis setelah keputusan salah. Petualangan berakhir.")
            return

    slow("\nKamu menemukan pintu gerbang bercahaya — ruang tahta raja alien.")
    slow("Langit-langit bergetar saat Taurus muncul: seekor raksasa bertanduk berkekuatan kosmik.")
    ok = pertarungan(pemain, 'Taurus — Raja Alien', 32, 8)
    if ok:
        slow("✨ Dengan serangan terakhir, Taurus roboh. Cahaya Canopus menyala! ✨")
        slow(f"Selamat, {nama}! Kamu membawa pulang bintang Canopus dan menyelamatkan stasiunmu.")
        slow("🏅 Pencapaian: Penakluk Taurus — Pemilik Canopus")
    else:
        slow("Taurus terlalu kuat. Kamu gugur di hadapannya.")

    slow('\nTerima kasih telah bermain — sampai jumpa di petualangan berikutnya! 🚀')

if __name__ == "__main__":
    try:
        game_utama()
    except KeyboardInterrupt:
        slow('\nPermainan dihentikan. Sampai nanti, penjelajah!')
        sys.exit(0)