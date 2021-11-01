# ALPHA VERSION - USE AT YOUR OWN RISK
# THIS IS A PERSONAL PROJECT


import os
import urllib.request

def welcome():
    print('\n - - - Converting your boring distro into a hacking powerhouse - - - \n')

def goodbye():
    print("\nDon't forget to perform 'sudo apt update'")
    print('Thank you for using @@@. Happy hacking!\n')

def menu():
    print('==================================')
    print('|                                |')
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

def repo_clean():
    os.system("sed -i '/deb http://http.kali.org/kali kali-rolling main non-free contrib/d' /etc/apt/sources.list")
    os.system("sed -i '/deb https://deb.parrotsec.org/parrot parrot main contrib non-free/d' /etc/apt/sources.list")

def main():
    choice = int(input('--> '))
    if choice == 1:
        with open('/etc/apt/sources.list', 'a') as f:
            f.write('deb http://http.kali.org/kali kali-rolling main non-free contrib\n')
            fullfilename = os.path.join('/etc/apt/trusted.gpg.d', 'kali-archive-key.asc')
            urllib.request.urlretrieve('https://archive.kali.org/archive-key.asc', filename=fullfilename)
            #os.system('sudo apt-key add /etc/apt/trusted.gpg.d/kali-archive-key.asc')
    elif choice == 2:
        with open('/etc/apt/sources.list', 'a') as f:
            f.write('deb https://deb.parrotsec.org/parrot parrot main contrib non-free\n')
            fullfilename = os.path.join('/etc/apt/trusted.gpg.d', 'parrotsec.gpg')
            urllib.request.urlretrieve('https://archive.parrotsec.org/parrot/misc/parrotsec.gpg', filename=fullfilename)
            #os.system('sudo apt-key add /etc/apt/trusted.gpg.d/parrotsec.gpg')
    else:
        print('\nInvalid option\nExiting...\n')
        exit()

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("You need to run this tool with sudo privileges!")
        exit()
    welcome()
    menu()
    detect()
    main()
    goodbye()
