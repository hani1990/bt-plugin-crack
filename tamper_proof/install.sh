#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH
install_tmp='/tmp/bt_install.pl'
public_file=/www/server/panel/install/public.sh
if [ ! -f $public_file ];then
	wget -O $public_file http://download.bt.cn/install/public.sh -T 5;
fi
. $public_file

download_Url=$NODE_URL
pluginPath=/www/server/panel/plugin/tamper_proof

Install_tamper_proof()
{
	pip install pyinotify
	mkdir -p $pluginPath
	mkdir -p $pluginPath/sites
	echo '正在安装脚本文件...' > $install_tmp
	wget -O $pluginPath/tamper_proof_main.py $download_Url/install/lib/plugin/tamper_proof/tamper_proof_main.py -T 5
	wget -O $pluginPath/tamper_proof_init.py $download_Url/install/lib/plugin/tamper_proof/tamper_proof_init.py -T 5
	wget -O $pluginPath/tamper_proof_service.py $download_Url/install/lib/plugin/tamper_proof/tamper_proof_service.py -T 5
	wget -O $pluginPath/index.html $download_Url/install/lib/plugin/tamper_proof/index.html -T 5
	wget -O $pluginPath/config.json $download_Url/install/lib/plugin/tamper_proof/config.json -T 5
	wget -O $pluginPath/icon.png $download_Url/install/lib/plugin/tamper_proof/icon.png -T 5
	wget -O $pluginPath/info.json $download_Url/install/lib/plugin/tamper_proof/info.json -T 5

	siteJson=$pluginPath/sites.json
	if [ ! -f $siteJson ];then
		wget -O $siteJson $download_Url/install/lib/plugin/tamper_proof/sites.json -T 5
	fi
	initSh=/etc/init.d/bt_tamper_proof
	wget -O $initSh $download_Url/install/lib/plugin/tamper_proof/init.sh -T 5
	chmod +x $initSh
	chmod +x /etc/init.d/bt_tamper_proof
	update-rc.d bt_tamper_proof defaults
	chkconfig --add bt_tamper_proof
	chkconfig --level 2345 bt_tamper_proof on
	check_fs
	$initSh stop
	$initSh start
	chmod -R 600 $pluginPath

	echo '安装完成' > $install_tmp
}

check_fs()
{
	is_max_user_instances=`cat /etc/sysctl.conf|grep max_user_instances`
	if [ "$is_max_user_instances" == "" ];then
		echo "fs.inotify.max_user_instances = 1024" >> /etc/sysctl.conf
		echo "1024" > /proc/sys/fs/inotify/max_user_instances
	fi
	
	is_max_user_watches=`cat /etc/sysctl.conf|grep max_user_watches`
	if [ "$is_max_user_watches" == "" ];then
		echo "fs.inotify.max_user_watches = 81920000" >> /etc/sysctl.conf
		echo "81920000" > /proc/sys/fs/inotify/max_user_watches
	fi
}

Uninstall_tamper_proof()
{
	initSh=/etc/init.d/bt_tamper_proof
	$initSh stop
	update-rc.d bt_tamper_proof remove
	chkconfig --del bt_tamper_proof
	rm -rf $pluginPath
	rm -f $initSh
}


action=$1
if [ "${1}" == 'install' ];then
	Install_tamper_proof
else
	Uninstall_tamper_proof
fi
