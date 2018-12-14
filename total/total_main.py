#coding: utf-8
# +-------------------------------------------------------------------
# | 宝塔Linux面板
# +-------------------------------------------------------------------
# | Copyright (c) 2015-2099 宝塔软件(http://bt.cn) All rights reserved.
# +-------------------------------------------------------------------
# | Author: 黄文良 <287962566@qq.com>
# +-------------------------------------------------------------------

#+--------------------------------------------------------------------
#|   宝塔网站防火墙 for httpd
#+--------------------------------------------------------------------
import sys,os;
p_path = '/www/server/panel/plugin/total';
sys.path.append(p_path);
import total_init;
reload(total_init);

class total_main(total_init.plugin_total_init):pass;
        
if __name__ == "__main__":
    os.chdir('/www/server/panel')
    p = total_main();
    p._check_site();
    