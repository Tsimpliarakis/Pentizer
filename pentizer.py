## -- Michail Tsimpliarakis -- ##

import os
import urllib.request

def welcome():
    print('\n - - - Converting any Debian based distro into a hacking powerhouse - - - \n')

def goodbye():
    os.system("sudo apt-get update")
    os.system("clear")
    print('Do not perform upgrade with the new repositories.')
    print('Thank you for using Pentizer. Happy hacking!\n')

def menu():
    print('==================================')
    print('|                                |')
    print('| 0. Clean repositories and Exit |')
    print('| 1. Add Kali Linux repositories |')
    print('| 2. Add Parrot Os repositories  |')
    print('|                                |')
    print('==================================\n')

def detect():
    kali = 'deb http://http.kali.org/kali kali-rolling main non-free contrib'
    parrot = 'deb https://deb.parrotsec.org/parrot parrot main contrib non-free'
    if kali in open('/etc/apt/sources.list').read():
        print ('Kali repositories are already on your system')
    if parrot in open('/etc/apt/sources.list').read():
        print ('Parrot repositories are already on your system')

def clean():
    os.system("sudo sed -i '/kali kali-rolling main non-free contrib/d' /etc/apt/sources.list")
    os.system("sudo sed -i '/parrot parrot main contrib non-free/d' /etc/apt/sources.list")
    os.system("sudo sed -i '/parrot parrot-security main contrib non-free/d' /etc/apt/sources.list")
    os.system("sudo rm -f /etc/apt/trusted.gpg.d/kali-archive-key.asc")
    os.system("sudo rm -f /etc/apt/trusted.gpg.d/parrotseckey")
    # os.system("sudo apt-key del 0A91 2CDE 87F9 9722 36AF  8B50 363A 96A5 CEA9 EA27")          -- See line 61 --
    os.system("sudo rm -f /etc/apt/trusted.gpg~")

def main():
    choice = int(input('--> '))
    if choice == 0:
        goodbye()
        clean()
        exit()
    elif choice == 1:
        with open('/etc/apt/sources.list', 'a') as f:
            f.write('deb http://http.kali.org/kali kali-rolling main non-free contrib\n')
            f.write('deb-src http://http.kali.org/kali kali-rolling main non-free contrib\n')
            fullfilename = os.path.join('/etc/apt/trusted.gpg.d', 'kali-archive-key.asc')
            urllib.request.urlretrieve('https://archive.kali.org/archive-key.asc', filename=fullfilename)
    elif choice == 2:
        with open('/etc/apt/sources.list', 'a') as f:
            f.write('deb https://deb.parrotsec.org/parrot parrot main contrib non-free\n')
            f.write('deb https://deb.parrotsec.org/parrot parrot-security main contrib non-free\n')
            f.write('deb-src https://deb.parrotsec.org/parrot parrot main contrib non-free\n')
            f.write('deb-src https://deb.parrotsec.org/parrot parrot-security main contrib non-free\n')
            fullfilename = os.path.join('/etc/apt/trusted.gpg.d', 'parrotseckey')
            urllib.request.urlretrieve('http://archive.parrotsec.org/parrot/misc/parrotsec.gpg', filename=fullfilename)
            # os.system('sudo apt-key add /etc/apt/trusted.gpg.d/parrotseckey')                                                        -- Might need that later --
    else:
        print('\nInvalid option\nExiting...\n')
        clean()
        exit()
    goodbye()

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("You need to run this tool with sudo privileges!")
        exit()
    welcome()
    menu()
    detect()
    main()
