#!/bin/python
from new-vm.py import *

def ks_configurator():
  KS = "
%pre

%end

install
text
cdrom
lang en_US.UTF-8
keyboard us
network --onboot yes --device eth0 --bootproto DHCP --hostname " + NAME + "
rootpw --iscrypted 6AE6E1195FA12CBF4BE56960A2AE1852F53072B0DF6AED66CBE0F6B1EB47BA1B5073CC206A8BC9E00C05526A3FD133BD26DCE5249FDA6E7085F1030531C0F75D
firewall --disabled
authconfig --enableshadow --passalgo=sha512
selinux --disabled
services --enabled=sshd
timezone --utc America/Vancouver
zerombr
clearpart --all
part /boot --fstype=xfs --size=512
part pv.01 --grow --size=1
volgroup vgroot01 pv.01
logvol swap --name=lv_swap --vgname=vgroot01 --size=1024
logvol / --fstype=xfs --name=lv_root --vgname=vgroot01 --grow --size=1
bootloader --location=mbr --append="crashkernel=auto rhgb quiet" console=ttyS0,115200"
user --name=localadmin --iscrypted --groups=wheel --password=6AE6E1195FA12CBF4BE56960A2AE1852F53072B0DF6AED66CBE0F6B1EB47BA1B5073CC206A8BC9E00C05526A3FD133BD26DCE5249FDA6E7085F1030531C0F75D
reboot
%packages --nobase --ignoremissing
@core
openssh-server
ipa-client
vim
wget
nfs-utils
python
git
curl
sudo
iptables
rsync
%end

%post --nochroot
#!/bin/bash
cp /etc/resolv.conf /mnt/sysimage/etc/resolv.conf
%end

%post
#!/bin/bash
ipa-client-install --server=freeipa.lilac.red --domain=lilac.red --mkhomedir
gpasswd -a brian wheel
reboot
%end

"
  return KS