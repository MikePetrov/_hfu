
# Проверка условий
######################################
if [[ $EUID -ne 0 ]]; then
    echo "\n\n\n Скрипт должен запускаться root \n\n\n"
    exit 1
fi
######################################

#!/bin/sh

# Создание переменных
red=$(tput setf 4)
green=$(tput setf 2)
reset=$(tput sgr0)
toend=$(tput hpa $(tput cols))$(tput cub 15)

# Проверка системы
echo -e "\n Обновляем систему... \n"
apt-get update
apt-get upgrade -y
apt-get dist-upgrade -y

echo -e "\n\n\n Проверяем наличие пакетов... \n\n\n"
for package in mc htop
do
	dpkg -s $package >/dev/null 2>&1 && echo -e -n "  $package" "${green}${toend}[OK]\n" && echo -n "${reset}" || aptitude install -y $package
done

# Hook
# sed -i 's/^ff02::1 ip6-allnodes$/\0\n127.0.0.1 microsoft.com/' /etc/hosts
echo -e "### Hooks ###" >> /boot/config.txt
echo -e "dtoverlay=w1-gpio" >> /boot/config.txt
