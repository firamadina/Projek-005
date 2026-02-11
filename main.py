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

def starfield(lines=1):
    for _ in range(lines):
        row = ''.join(random.choice([' ', '.', '*', ' ']) for _ in range(60))
        print(' ' + row)

def status(pemain):
    weapon = pemain.get('weapon', {'name':'Tangan Kosong', 'bonus':0})
    luck = pemain.get('luck', 0)
    slow(f"[STATUS] HP: {pemain['hp']}  ATK: {pemain['atk']} (+{weapon.get('bonus',0)})  NYAWA: {pemain['nyawa']} ⭐  SENJATA: {weapon.get('name','Tangan Kosong')}  LUCK: {luck}")

def choose_weapon(pemain):
    slow('\n🔧 Pilih senjata untuk pertempuranmu (membayar dengan nyawa):')
    slow("1) Laser Blaster 🔫  (ATK +2, akurasi 92%, biaya nyawa 10)")
    slow("2) Plasma Rifle ⚡ (ATK +4, akurasi 78%, biaya nyawa 20)")
    slow("3) Ion Cutter 🗡️  (ATK +3, crit 15%, biaya nyawa 15)")
    pilih = input("Masukkan nomor senjata pilihan (1/2/3): ").strip()
    if pilih == '1':
        cost = 10
        pemain['weapon'] = {'name': 'Laser Blaster', 'bonus': 2, 'acc': 0.92, 'crit': 0.05}
        slow('Laser Blaster siap. Cahaya biru menyala di larasmu.')
    elif pilih == '2':
        cost = 20
        pemain['weapon'] = {'name': 'Plasma Rifle', 'bonus': 4, 'acc': 0.78, 'crit': 0.08}
        slow('Plasma Rifle mengaum, inti panas berdenyut.')
    elif pilih == '3':
        cost = 15
        pemain['weapon'] = {'name': 'Ion Cutter', 'bonus': 3, 'acc': 0.85, 'crit': 0.15}
        slow('Ion Cutter bergetar, siap memotong perisai musuh.')
    else:
        slow('Pilihan senjata tidak valid! Kamu kehilangan fokus saat memilih.')
        pemain['nyawa'] -= 20
        slow(f"Nyawa berkurang 20. Sisa nyawa: {pemain['nyawa']}")
        if pemain['nyawa'] <= 0:
            slow('💀 Nyawa habis... Petualangan berakhir.')
            return False
        slow('Default: Laser Blaster dipasang secara otomatis.')
        cost = 10
        pemain['weapon'] = {'name': 'Laser Blaster', 'bonus': 2, 'acc': 0.92, 'crit': 0.05}

    # elemen keberuntungan mempengaruhi harga (bisa lebih murah/mahal)
    luck = pemain.get('luck', 0)
    delta = random.randint(-luck//2, luck//2)
    adjusted = max(0, cost + delta)
    pemain['nyawa'] -= adjusted
    slow(f"Keteruntunganmu: {luck}. Harga asli {cost}, penyesuaian {delta}, bayar {adjusted} nyawa untuk {pemain['weapon']['name']}. Sisa nyawa: {pemain['nyawa']}")
    if pemain['nyawa'] <= 0:
        slow('💀 Nyawa habis setelah membeli senjata... Petualangan berakhir.')
        return False
    return True

def pertarungan(pemain, musuh_nama, musuh_hp, musuh_atk):
    slow(f"\n⚔️  Bertemu: {musuh_nama} (HP {musuh_hp}, ATK {musuh_atk})")
    while pemain['hp'] > 0 and musuh_hp > 0:
        status(pemain)
        aksi = input("Aksi kamu (serang / bertahan / kabur): ").strip().lower()
        if aksi == 'serang':
            weapon = pemain.get('weapon', {'name':'Tangan Kosong','bonus':0,'acc':1.0,'crit':0})
            if random.random() <= weapon.get('acc', 1.0):
                base = pemain['atk'] + weapon.get('bonus', 0)
                dmg = max(1, base + random.randint(-2, 2))
                if random.random() < weapon.get('crit', 0):
                    dmg = int(dmg * 1.75)
                    slow('🔥 Serangan Kritis!')
                musuh_hp -= dmg
                slow(f"➡️  Kamu menyerang {musuh_nama} dengan {weapon['name']} dan memberi {dmg} kerusakan.")
            else:
                slow('✨ Serangan meleset karena gangguan ruang-waktu!')
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
            # peluang mengelak berdasarkan luck
            evade_chance = min(0.5, pemain.get('luck', 0) * 0.02)
            if random.random() < evade_chance:
                slow('🍀 Beruntung! Kamu mengelak dari serangan musuh.')
            else:
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

    pemain = {'hp': 40, 'atk': 6, 'nyawa': 100, 'luck': random.randint(1, 10)}
    status(pemain)
    if not choose_weapon(pemain):
        return
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

    # elemen keberuntungan: kemungkinan menemukan cache atau menghadapi ambush acak
    event_roll = random.random()
    luck = pemain.get('luck', 0)
    if event_roll < 0.15 + luck * 0.01:
        slow('\n✨ Keberuntungan! Kamu menemukan Nebula Cache yang menyembuhkan 10 HP.')
        pemain['hp'] = min(40, pemain['hp'] + 10)
        status(pemain)
    elif event_roll > 0.95 - luck * 0.01:
        slow('\n⚠️ Malang! Kamu terkena ambush tambahan saat memasuki dungeon.')
        encounters.insert(0, ('Skirmisher Nebula', 8, 4))

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
        while True:
            game_utama()
            again = input("\nMain lagi? (y/n): ").strip().lower()
            if again and again[0] == 'y':
                slow('\nMemulai ulang permainan...\n')
                continue
            else:
                slow('\nTerima kasih telah bermain. Sampai jumpa!')
                break
    except KeyboardInterrupt:
        slow('\nPermainan dihentikan. Sampai nanti, penjelajah!')
        sys.exit(0)