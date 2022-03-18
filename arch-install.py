#!/usr/bin/env python3

### INSTALLER FOR ARCH LINUX ####

from subprocess import run
import os
import shutil

#Checking root access
p1=run("whoami",capture_output=True,text=True)
if p1.stdout.strip()!="root":
    print("Please grant root access and run again")
    exit()


def pacinstall(a):
    s="pacman -S "+a+" --needed --noconfirm"
    run(s,shell=True)

def pacinstall_multi(L):
    s=''
    for i in L:
        s+=i+' '
    s2="pacman -S "+s+"--needed --noconfirm"
    run(s2,shell=True)


def systemctl(a):
    s="systemctl enable --now "+a
    run(s,shell=True)

#p1 = subprocess.run(['ls','-lah'],capture_output=True,text=True)
#print(p1.stdout)

#Pacman config
print("Copying pacman config file")
print("")
shutil.copyfile("./CONFIGS/pacman.conf","/etc/pacman.conf")
print("Pacman configured.")
print()

#Checking for UEFI

UEFI_var=False
if os.path.exists("/sys/firmware/efi/efivars"):
    UEFI_var=True

#Checking for internet connection
print("Checking for an internet connection")
print()

p1 = run(["ping", "google.com" ,"-c" ,"1"],capture_output=True,text=True)
if p1.stdout!='':
    print("You have an internet connection.")
    print()
else:
    print("You do not have an internet connection.")
    print()
    exit()

#Time

print("Configuring time")
print()
run("ln -sf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime",shell=True)

pacinstall('ntp')

run("hwclock --systohc",shell=True)

systemctl('ntpd')
print("Time configured")
print()

#Network
print("Configuring Network")
print()
hostname_var=input("Hostname: ")
with open("/etc/hostname",'w') as f:
    f.write(hostname_var)

with open("/etc/hosts",'a') as f:
    f.write("127.0.0.1\tlocalhost\n")
    f.write("::1\t\tlocalhost\n")
    f.write("127.0.1.1\t"+hostname_var+"@localdomain\t"+hostname_var)


base_packages=['grub','vim','xdg-user-dirs','xdg-utils','networkmanager','mtools','dosfstools','os-prober','git','ranger','htop','btop']
if UEFI_var==True:
    base_packages.append('efibootmgr')

pacinstall_multi(base_packages)
systemctl("NetworkManager.service")
print("Network Configured")
print()
#Locales
print("Configuring Locales")
print()
with open("/etc/locale.gen") as f:
    locale_gen=f.readlines()
for i in range(len(locale_gen)):
    if locale_gen[i].strip()=="#en_US.UTF-8 UTF-8":
        locale_gen[i]="en_US.UTF-8 UTF-8\n"
with open("/etc/locale.gen",'w') as f:
    for i in locale_gen:
        f.write(i)

run("locale-gen",shell=True)

with open("/etc/locale.conf",'w') as f:
    f.write("LANG=en_US.UTF-8")
print("Locales configured")
print()


#GRUB
print("Installing GRUB")
print()

if UEFI_var==True:
    grub_dir=input("Grub install directory: ")
    run("grub-install --target=x86_64-efi --efi-directory="+grub_dir+" --bootloader-id=GRUB",shell=True)

else:
    grub_dir=input("Grub install disk: ")
    run("grub-install --target=i386-pc "+grub_dir,shell=True)

run("grub-mkconfig -o /boot/grub/grub.cfg",shell=True)
print("GRUB installed")
print()


#Passwords
print("Accounts and Passwords")
print()
print("Set root password")
run("passwd",shell=True)
print()
#User

user = input("Username: ")
run("useradd -mG wheel,audio,video,optical,tty,network,storage "+user,shell=True)

print()
print("Set user password")
run("passwd "+user,shell=True)

print("Accounts configured")
print()
#Sudo

print("Copying sudo config file")
print()
shutil.copyfile("./CONFIGS/sudoers",'/etc/sudoers')
pacinstall('sudo')
print("Sudo configured")


#Fish
print("Installing fish shell")
print()
pacinstall("fish")
run("chsh -s /usr/bin/fish "+user,shell=True)
print("Configured fish shell")


#Paru
print("AUR helper(paru)")
print()
os.mkdir("git")
os.mkdir("git/paru-bin")
run("git clone https://aur.archlinux.org/paru-bin.git ./git/paru-bin/",shell=True)
run("cd ./git/paru-bin && makepkg -sri --noconfirm",shell=True)
print()




