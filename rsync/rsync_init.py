 #coding: utf-8
# +-------------------------------------------------------------------
# | 宝塔Linux面板
# +-------------------------------------------------------------------
# | Copyright (c) 2015-2019 宝塔软件(http://bt.cn) All rights reserved.
# +-------------------------------------------------------------------
# | Author: 黄文良 <287962566@qq.com>
# +-------------------------------------------------------------------
import re ,os ,sys ,time #line:9
sys .path .append ("/www/server/panel/class/")#line:10
import public ,db ,crontab #line:11
import re ,json #line:12
import time ,base64 ,web #line:13
from panelAuth import panelAuth #line:14
class plugin_rsync_init ():#line:16
    __OO0O00O0OOOO0OOOO ='/usr/bin/rsync'#line:17
    rsyn_file ="/etc/rsyncd.conf"#line:18
    lsync_file ="/etc/lsyncd.conf"#line:19
    rsyn_path ='/www/server/panel/plugin/rsync'#line:20
    def __init__ (OO0O000OO00OOOO00 ):#line:22
        OOO0O0OO0OO000000 =OO0O000OO00OOOO00 .rsyn_path +'/sclient';#line:23
        if not os .path .exists (OOO0O0OO0OO000000 ):public .ExecShell ("mkdir -p "+OOO0O0OO0OO000000 );#line:24
        OOO0O0OO0OO000000 =OO0O000OO00OOOO00 .rsyn_path +'/secrets';#line:25
        if not os .path .exists (OOO0O0OO0OO000000 ):public .ExecShell ("mkdir -p "+OOO0O0OO0OO000000 );#line:26
        O000OO0O0OO00O00O =OO0O000OO00OOOO00 .rsyn_path +'/lsyncd.log'#line:27
        if os .path .exists (O000OO0O0OO00O00O ):#line:28
            if os .path .getsize (O000OO0O0OO00O00O )*1024 *1024 >1024 :public .writeFile (O000OO0O0OO00O00O ,public .GetNumLines (O000OO0O0OO00O00O ,2000 ))#line:29
    def get_logs (O00O000O0OO0000O0 ,O00O0OOOO0OO00O00 ):#line:31
        import page #line:32
        page =page .Page ();#line:33
        OO00OOO0OO0O0O0O0 =public .M ('logs').where ('type=?',(u'数据同步工具',)).count ();#line:34
        OOO00O000OO0O0OOO =12 ;#line:35
        del (O00O0OOOO0OO00O00 .data )#line:36
        del (O00O0OOOO0OO00O00 .zunfile )#line:37
        OOO0OO0O000O0OO0O ={}#line:38
        OOO0OO0O000O0OO0O ['count']=OO00OOO0OO0O0O0O0 #line:39
        OOO0OO0O000O0OO0O ['row']=OOO00O000OO0O0OOO #line:40
        OOO0OO0O000O0OO0O ['p']=1 #line:41
        if hasattr (O00O0OOOO0OO00O00 ,'p'):#line:42
            OOO0OO0O000O0OO0O ['p']=int (O00O0OOOO0OO00O00 ['p'])#line:43
        OOO0OO0O000O0OO0O ['uri']=O00O0OOOO0OO00O00 #line:44
        OOO0OO0O000O0OO0O ['return_js']=''#line:45
        if hasattr (O00O0OOOO0OO00O00 ,'tojs'):#line:46
            OOO0OO0O000O0OO0O ['return_js']=O00O0OOOO0OO00O00 .tojs #line:47
        OO000OO000OOO00O0 ={}#line:48
        OO000OO000OOO00O0 ['page']=page .GetPage (OOO0OO0O000O0OO0O ,'1,2,3,4,5,8');#line:50
        OO000OO000OOO00O0 ['data']=public .M ('logs').where ('type=?',(u'数据同步工具',)).order ('id desc').limit (bytes (page .SHIFT )+','+bytes (page .ROW )).field ('log,addtime').select ();#line:51
        return OO000OO000OOO00O0 ;#line:52
    def get_rsync_conf (OO0OO0OOO0O00000O ,OOO0000O000O000OO ):#line:54
        OOO0O0O0O00O0O0O0 =json .loads (public .readFile (OO0OO0OOO0O00000O .rsyn_path +'/config.json'))#line:55
        return OOO0O0O0O00O0O0O0 #line:56
    def get_global_conf (OO00O0O00O00OO00O ,O000OO00O000OO000 ):#line:58
        OOOO0OOOOOOO00OO0 =OO00O0O00O00OO00O .get_rsync_conf (None );#line:59
        OOO000OOOO000O0O0 ={}#line:60
        OOO000OOOO000O0O0 ['modules']=OOOO0OOOOOOO00OO0 ['modules']#line:61
        OOO000OOOO000O0O0 ['global']=OOOO0OOOOOOO00OO0 ['global']#line:62
        OOO000OOOO000O0O0 ['open']=(len (public .ExecShell ("/etc/init.d/rsynd status|grep 'already running'")[0 ])>1 )|False #line:63
        return OOO000OOOO000O0O0 ;#line:64
    def modify_global_conf (OO00OOOO00OO0000O ,O0OO000000O00O0O0 ):#line:66
        O0OO0O000O0000O00 =OO00OOOO00OO0000O .get_rsync_conf (None );#line:67
        if 'port'in O0OO000000O00O0O0 :O0OO0O000O0000O00 ['global']['port']=int (O0OO000000O00O0O0 .port )#line:68
        if 'hosts_allow'in O0OO000000O00O0O0 :O0OO0O000O0000O00 ['global']['hosts allow']=" ".join (O0OO000000O00O0O0 .hosts_allow .split ());#line:69
        if 'timeout'in O0OO000000O00O0O0 :O0OO0O000O0000O00 ['global']['timeout']=int (O0OO000000O00O0O0 .timeout );#line:70
        if 'max_connections'in O0OO000000O00O0O0 :O0OO0O000O0000O00 ['global']['max connections']=int (O0OO000000O00O0O0 .max_connections )#line:71
        if 'dont_compress'in O0OO000000O00O0O0 :O0OO0O000O0000O00 ['global']['dont compress']=O0OO000000O00O0O0 .dont_compress #line:72
        OO00OOOO00OO0000O .__O00OOOOO0000OO00O (O0OO0O000O0000O00 );#line:73
        OO00OOOO00OO0000O .__O0OO0O0OOO000OOO0 ('修改rsync服务器全局配置');#line:74
        return public .returnMsg (True ,'设置成功!');#line:75
    def get_secretkey (O0O00O0OO0OOO00OO ,O0000OOO000O0O0OO ):#line:77
        OO0O0000O0000000O =O0O00O0OO0OOO00OO .get_module (O0000OOO000O0O0OO )#line:78
        OOOO000OOO00OO0O0 =O0O00O0OO0OOO00OO .__OOOOOO0OOO0O00OOO (OO0O0000O0000000O ['name'],OO0O0000O0000000O ['password'],OO0O0000O0000000O ['port'])#line:79
        return OOOO000OOO00OO0O0 #line:80
    def add_module (OO0OO00000000O0O0 ,O0OO0O00OOOOO0O0O ):#line:82
        if OO0OO00000000O0O0 .__OO00OO0OO00O0O0O0 (O0OO0O00OOOOO0O0O .path ):return public .returnMsg (False ,'不能同步系统关键目录');#line:83
        if OO0OO00000000O0O0 .__OOOOOOO000OOOOOO0 (O0OO0O00OOOOO0O0O .mName ):return public .returnMsg (False ,'您输入的用户名已存在');#line:84
        O00O00O00OO0000O0 =OO0OO00000000O0O0 .get_rsync_conf (None );#line:85
        O0O00OO0O0OOOOO0O =OO0OO00000000O0O0 .rsyn_path +'/secrets/'+O0OO0O00OOOOO0O0O .mName +'.db';#line:86
        O00OO0O00O0O0OOO0 ={'name':O0OO0O00OOOOO0O0O .mName ,'path':O0OO0O00OOOOO0O0O .path ,'password':O0OO0O00OOOOO0O0O .password ,'comment':O0OO0O00OOOOO0O0O .comment ,'read only':'false','ignore errors':True ,'auth users':O0OO0O00OOOOO0O0O .mName ,'secrets file':O0O00OO0O0OOOOO0O ,'addtime':int (time .time ())}#line:96
        O00O00O00OO0000O0 ['modules'].insert (0 ,O00OO0O00O0O0OOO0 )#line:97
        OO0OO00000000O0O0 .__O00OOOOO0000OO00O (O00O00O00OO0000O0 );#line:98
        OO0OO00000000O0O0 .__O0OO0O0OOO000OOO0 ('添加rsync接收帐户['+O0OO0O00OOOOO0O0O .mName +']');#line:99
        return public .returnMsg (True ,'添加成功!');#line:100
    def modify_module (O0OOOO000OO00000O ,O0O0000O0OO00O0O0 ):#line:102
        if O0OOOO000OO00000O .__OO00OO0OO00O0O0O0 (O0O0000O0OO00O0O0 .path ):return public .returnMsg (False ,'不能同步系统关键目录');#line:103
        OOOOOO0OOOOOOO00O =O0OOOO000OO00000O .get_rsync_conf (None );#line:104
        for O000OOOO0OOOOO00O in xrange (len (OOOOOO0OOOOOOO00O ['modules'])):#line:105
            if OOOOOO0OOOOOOO00O ['modules'][O000OOOO0OOOOO00O ]['name']==O0O0000O0OO00O0O0 .mName :#line:106
                OOOOOO0OOOOOOO00O ['modules'][O000OOOO0OOOOO00O ]['password']=O0O0000O0OO00O0O0 .password ;#line:107
                OOOOOO0OOOOOOO00O ['modules'][O000OOOO0OOOOO00O ]['path']=O0O0000O0OO00O0O0 .path ;#line:108
                OOOOOO0OOOOOOO00O ['modules'][O000OOOO0OOOOO00O ]['comment']=O0O0000O0OO00O0O0 .comment ;#line:109
                O0OOOO000OO00000O .__OO0O0O0000O000000 (OOOOOO0OOOOOOO00O ['modules'][O000OOOO0OOOOO00O ]['name'],OOOOOO0OOOOOOO00O ['modules'][O000OOOO0OOOOO00O ]['auth users'],OOOOOO0OOOOOOO00O ['modules'][O000OOOO0OOOOO00O ]['password'],False )#line:110
                O0OOOO000OO00000O .__O00OOOOO0000OO00O (OOOOOO0OOOOOOO00O );#line:111
                O0OOOO000OO00000O .__O0OO0O0OOO000OOO0 ('修改rsync接收帐户['+O0O0000O0OO00O0O0 .mName +']');#line:112
                return public .returnMsg (True ,'编辑成功!');#line:113
        return public .returnMsg (False ,'指定模块不存在!');#line:114
    def remove_module (OOOOO00OOO0O0OOO0 ,O0O0OOO00OO00OO0O ):#line:116
        OOO0O0O00O0O0O000 =OOOOO00OOO0O0OOO0 .get_rsync_conf (None );#line:117
        for O0O0O0OOOO0OO00O0 in xrange (len (OOO0O0O00O0O0O000 ['modules'])):#line:118
            if OOO0O0O00O0O0O000 ['modules'][O0O0O0OOOO0OO00O0 ]['name']==O0O0OOO00OO00OO0O .mName :#line:119
                del (OOO0O0O00O0O0O000 ['modules'][O0O0O0OOOO0OO00O0 ])#line:120
                OOOOO00OOO0O0OOO0 .__O00OOOOO0000OO00O (OOO0O0O00O0O0O000 );#line:121
                O00O0O0O0OO0O0OOO =OOOOO00OOO0O0OOO0 .rsyn_path +'/secrets/'+O0O0OOO00OO00OO0O .mName +'.db';#line:122
                if os .path .exists (O00O0O0O0OO0O0OOO ):os .remove (O00O0O0O0OO0O0OOO );#line:123
                OOOOO00OOO0O0OOO0 .__O0OO0O0OOO000OOO0 ('删除rsync接收帐户['+O0O0OOO00OO00OO0O .mName +']');#line:124
                return public .returnMsg (True ,'删除成功!');#line:125
        return public .returnMsg (False ,'指定模块不存在!');#line:126
    def get_module (O00O0OOOOOOO0O0OO ,O0OOO0O000OOOO0OO ,name =None ):#line:129
        if O0OOO0O000OOOO0OO :name =O0OOO0O000OOOO0OO .mName ;#line:130
        OOO00OOOO0O0OOO0O =O00O0OOOOOOO0O0OO .get_rsync_conf (None );#line:131
        for OO000000OO0O0O00O in xrange (len (OOO00OOOO0O0OOO0O ['modules'])):#line:132
            if OOO00OOOO0O0OOO0O ['modules'][OO000000OO0O0O00O ]['name']==name :#line:133
                OOO00OOOO0O0OOO0O ['modules'][OO000000OO0O0O00O ]['port']=OOO00OOOO0O0OOO0O ['global']['port'];#line:134
                return OOO00OOOO0O0OOO0O ['modules'][OO000000OO0O0O00O ]#line:135
        return public .returnMsg (False ,'指定模块不存在!');#line:136
    def get_send_conf (OO0O0O0000OO0O0O0 ,OO000000OO000OO00 ):#line:138
        # OOO000OOO0OOO0O00 =OO0O0O0000OO0O0O0 .__O0O0OOO0O00000O00 (OO000000OO000OO00 )#line:139
        # if not getattr (web .ctx .session ,'rsync',False ):return OOO000OOO0OOO0O00 ;#line:140
        # O0O0OOOOOO00O0000 =OO0O0O0000OO0O0O0 .get_rsync_conf (None );#line:141
        # return O0O0OOOOOO00O0000 ['client'];#line:142
        return public .returnMsg (True ,'ok!');#line:136
    def get_send_byname (OO0OO0O0O0O0OO0OO ,OOOOOOOOOO0O0OO0O ):#line:144
        O000OO0O000OO0OOO =OO0OO0O0O0O0OO0OO .get_rsync_conf (None );#line:145
        for OO0OO000O00O00O00 in xrange (len (O000OO0O000OO0OOO ['client'])):#line:146
            if O000OO0O000OO0OOO ['client'][OO0OO000O00O00O00 ]['name']==OOOOOOOOOO0O0OO0O ['mName']:#line:147
                O00O0O0000000000O =O000OO0O000OO0OOO ['client'][OO0OO000O00O00O00 ];#line:148
                O00O0O0000000000O ['secret_key']=OO0OO0O0O0O0OO0OO .__OOOOOO0OOO0O00OOO (O00O0O0000000000O ['name'],O00O0O0000000000O ['password'],O00O0O0000000000O ['rsync']['port'])#line:149
                return O00O0O0000000000O ;#line:150
        return public .returnMsg (False ,'指定任务不存在!');#line:151
    def __O0O0OOO0O00000O00 (OO0OOOO000OO00O0O ,O000OO00OOO00OO00 ):#line:153
        O0OO0000OO00O0OOO ='/www/server/panel/plugin/rsync/rsync_init.py';#line:154
        if os .path .exists (O0OO0000OO00O0OOO ):os .remove (O0OO0000OO00O0OOO );#line:155
        if getattr (web .ctx .session ,'rsync',False ):return public .returnMsg (True ,'OK!');#line:156
        O00000OO00O0OOOO0 ={}#line:157
        O00000OO00O0OOOO0 ['pid']='100000005';#line:158
        O00OOO000OO0O0OO0 =panelAuth ().send_cloud ('check_plugin_status',O00000OO00O0OOOO0 )#line:159
        try :#line:160
            if not O00OOO000OO0O0OO0 ['status']:#line:161
                if getattr (web .ctx .session ,'rsync',False ):del (web .ctx .session ['rsync'])#line:162
                return O00OOO000OO0O0OO0 ;#line:163
        except :pass ;#line:164
        web .ctx .session .rsync =True #line:165
        return O00OOO000OO0O0OO0 #line:166
    def __OOOOOO0OOO0O00OOO (OOO000OOO0OO0O0OO ,O000O000000O00000 ,O0O00O0000OO0OO00 ,O00OO00O0OOO0000O ):#line:168
        OO0OO000000OO00OO =json .dumps ({'A':re .sub ("(\d+\.){3,3}\d+_",'',O000O000000O00000 ),'B':O0O00O0000OO0OO00 ,'C':O00OO00O0OOO0000O })#line:169
        return base64 .b64encode (OO0OO000000OO00OO )#line:170
    def __O0000O0OO0OO00OOO (OOOO0OO0O0O000O00 ,O0O00O0O0O0OO0OO0 ,O00O0O0O0O00OO000 ,timeout =3 ):#line:172
        import socket #line:173
        O00O000OO00OO0000 =True ;#line:174
        try :#line:175
            O0O0OOO000000OOO0 =socket .socket ()#line:176
            O0O0OOO000000OOO0 .settimeout (timeout )#line:177
            O0O0OOO000000OOO0 .connect ((O0O00O0O0O0OO0OO0 ,O00O0O0O0O00OO000 ))#line:178
            O0O0OOO000000OOO0 .close ()#line:179
        except :#line:180
            O00O000OO00OO0000 =False ;#line:181
        return O00O000OO00OO0000 ;#line:182
    def add_ormodify_send (OO00O00O0OOOOOOO0 ,O0O00O0O00O00OO00 ):#line:184
        if OO00O00O0OOOOOOO0 .__OO00OO0OO00O0O0O0 (O0O00O0O00O00OO00 .path ):return public .returnMsg (False ,'不能同步系统关键目录');#line:185
        O0O00O0O00O00OO00 .delay =getattr (O0O00O0O00O00OO00 ,'delay','3');#line:186
        O0O00O0O00O00OO00 .model =getattr (O0O00O0O00O00OO00 ,'model','default.rsync');#line:187
        O0O00O0O00O00OO00 .to =getattr (O0O00O0O00O00OO00 ,'to','');#line:188
        O0O00O0O00O00OO00 .ip =getattr (O0O00O0O00O00OO00 ,'ip','');#line:189
        O0O00O0O00O00OO00 .delete =getattr (O0O00O0O00O00OO00 ,'delete','true');#line:190
        O0O00O0O00O00OO00 .realtime =getattr (O0O00O0O00O00OO00 ,'realtime',True );#line:191
        O0O00O0O00O00OO00 .ps =getattr (O0O00O0O00O00OO00 ,'ps','');#line:192
        O0O00O0O00O00OO00 .bwlimit =getattr (O0O00O0O00O00OO00 ,'bwlimit','1024');#line:193
        O0O00O0O00O00OO00 .compress =getattr (O0O00O0O00O00OO00 ,'compress','true');#line:194
        O0O00O0O00O00OO00 .archive =getattr (O0O00O0O00O00OO00 ,'archive','true');#line:195
        O0O00O0O00O00OO00 .verbose =getattr (O0O00O0O00O00OO00 ,'verbose','true');#line:196
        O0O00O0O00O00OO00 .index =getattr (O0O00O0O00O00OO00 ,'index','-1');#line:197
        if int (O0O00O0O00O00OO00 .delay )<0 :O0O00O0O00O00OO00 .delay ='0';#line:199
        if int (O0O00O0O00O00OO00 .bwlimit )<0 :O0O00O0O00O00OO00 .bwlimit ='0';#line:200
        if type (O0O00O0O00O00OO00 .realtime )!=bool :#line:202
            O0O00O0O00O00OO00 .realtime =(O0O00O0O00O00OO00 .realtime =='true')|False ;#line:203
        if O0O00O0O00O00OO00 .model =='default.rsync':#line:206
            try :#line:207
                O00OOOOO0OOO00OO0 =json .loads (base64 .b64decode (O0O00O0O00O00OO00 ['secret_key']))#line:208
            except :#line:209
                return public .returnMsg (False ,'错误的接收密钥');#line:210
            if not re .match ("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",O0O00O0O00O00OO00 .ip ):return public .returnMsg (False ,'请填写正确的IP地址!');#line:212
            OO0O0O000O000OOO0 =json .loads (O0O00O0O00O00OO00 .cron )#line:213
            if not OO00O00O0OOOOOOO0 .__O0000O0OO0OO00OOO (O0O00O0O00O00OO00 .ip ,int (O00OOOOO0OOO00OO0 ['C'])):#line:214
                return public .returnMsg (False ,'无法连接['+O0O00O0O00O00OO00 .ip +':'+str (O00OOOOO0OOO00OO0 ['C'])+'],请检查IP地址是否正确,若正确无误，请检查远程服务器的安全组及防火墙是否正确放行['+str (O00OOOOO0OOO00OO0 ['C'])+']端口!');#line:215
        else :#line:216
            if O0O00O0O00O00OO00 .path ==O0O00O0O00O00OO00 .to :return public .returnMsg (False ,'不能同步两个相同的目录');#line:217
            if not os .path .exists (O0O00O0O00O00OO00 .to ):public .ExecShell ('mkdir -p '+O0O00O0O00O00OO00 .to );#line:218
            O00OOOOO0OOO00OO0 ={'A':O0O00O0O00O00OO00 .mName ,'B':'','C':'873'}#line:219
            OO0O0O000O000OOO0 ={}#line:220
        if O0O00O0O00O00OO00 .index =='-1':#line:222
            if OO00O00O0OOOOOOO0 .__O0OO00O0O00OOOO0O (O00OOOOO0OOO00OO0 ['A']):return public .returnMsg (False ,'已存在同名任务!');#line:223
        if not os .path .exists (O0O00O0O00O00OO00 .path ):public .ExecShell ('mkdir -p '+O0O00O0O00O00OO00 .path );#line:225
        OO000O0OOO00OOOOO ={'model':O0O00O0O00O00OO00 .model ,'name':O00OOOOO0OOO00OO0 ['A'],'ip':O0O00O0O00O00OO00 .ip ,'password':O00OOOOO0OOO00OO0 ['B'],'path':O0O00O0O00O00OO00 .path ,'to':O0O00O0O00O00OO00 .to ,'exclude':[],'delete':O0O00O0O00O00OO00 .delete ,'realtime':O0O00O0O00O00OO00 .realtime |False ,'delay':str (int (O0O00O0O00O00OO00 .delay )),'rsync':{'bwlimit':str (int (O0O00O0O00O00OO00 .bwlimit )),'port':str (O00OOOOO0OOO00OO0 ['C']),'compress':O0O00O0O00O00OO00 .compress ,'archive':O0O00O0O00O00OO00 .archive ,'verbose':O0O00O0O00O00OO00 .verbose },'ps':O0O00O0O00O00OO00 .ps ,'cron':OO0O0O000O000OOO0 ,'update':time .time ()}#line:247
        if O0O00O0O00O00OO00 .model =='default.rsync':#line:249
            O0O0OOOOOO0OOOO0O =OO00O00O0OOOOOOO0 .rsyn_path +'/sclient/'+OO000O0OOO00OOOOO ['name']+'_exclude'#line:250
            if not os .path .exists (O0O0OOOOOO0OOOO0O ):public .writeFile (O0O0OOOOOO0OOOO0O ,'');#line:251
            OO00O00O0OOOOOOO0 .__OO00O00O000OO0O0O (OO000O0OOO00OOOOO ['name'],OO000O0OOO00OOOOO ['password'],False )#line:252
            OO00O00O0OOOOOOO0 .__O0OO0000OO0OO0OO0 (OO000O0OOO00OOOOO ,O0O00O0O00O00OO00 );#line:253
        OOO000OOOOO0O0OO0 =OO00O00O0OOOOOOO0 .rsyn_path +'/sclient/'+OO000O0OOO00OOOOO ['name']+'_cmd'#line:255
        public .writeFile (OOO000OOOOO0O0OO0 ,OO00O00O0OOOOOOO0 .__O0O0O00O0O0OOO0OO (OO000O0OOO00OOOOO ))#line:256
        OOOOO0OO0O00000O0 =OO00O00O0OOOOOOO0 .get_rsync_conf (None );#line:258
        OOO0O00O0OO0OO00O =True ;#line:259
        if O0O00O0O00O00OO00 .index !='-1':#line:260
                OO000O0OOO00OOOOO ['exclude']=OOOOO0OO0O00000O0 ['client'][int (O0O00O0O00O00OO00 .index )]['exclude']#line:261
                OOOOO0OO0O00000O0 ['client'][int (O0O00O0O00O00OO00 .index )]=OO000O0OOO00OOOOO ;#line:262
                OOO0O00O0OO0OO00O =False ;#line:263
        if OOO0O00O0OO0OO00O :OOOOO0OO0O00000O0 ['client'].insert (0 ,OO000O0OOO00OOOOO )#line:264
        OO00O00O0OOOOOOO0 .__O00OOOOO0000OO00O (OOOOO0OO0O00000O0 ,True )#line:265
        if OOO0O00O0OO0OO00O :#line:266
            public .writeFile (OO00O00O0OOOOOOO0 .rsyn_path +'/sclient/'+OO000O0OOO00OOOOO ['name']+'_exec.log','');#line:267
            OO00O00O0OOOOOOO0 .__O0OO0O0OOO000OOO0 ('添加同步任务['+OO000O0OOO00OOOOO ['name']+']');#line:268
            public .ExecShell ("nohup bash "+OOO000OOOOO0O0OO0 +" >> "+OO00O00O0OOOOOOO0 .rsyn_path +"/sclient/"+OO000O0OOO00OOOOO ['name']+"_exec.log 2>&1 &");#line:269
            return public .returnMsg (True ,'添加成功!');#line:270
        OO00O00O0OOOOOOO0 .__O0OO0O0OOO000OOO0 ('修改同步任务['+OO000O0OOO00OOOOO ['name']+']');#line:271
        return public .returnMsg (True ,'修改成功!')#line:272
    def get_rsync_logs (OOO0OOOO000000O0O ,O0O0OOOO0O000OO0O ):#line:274
        if O0O0OOOO0O000OO0O .mName =='lsyncd_logs':#line:275
            O00O00OOOO00O0OOO =OOO0OOOO000000O0O .rsyn_path +'/lsyncd.log';#line:276
        else :#line:277
            O00O00OOOO00O0OOO =OOO0OOOO000000O0O .rsyn_path +'/sclient/'+O0O0OOOO0O000OO0O .mName +'_exec.log';#line:278
        if not os .path .exists (O00O00OOOO00O0OOO ):public .writeFile (O00O00OOOO00O0OOO ,'');#line:279
        return public .returnMsg (True ,public .GetNumLines (O00O00OOOO00O0OOO ,2000 ));#line:280
    def remove_rsync_logs (O00000O000O0OO0OO ,OO00OOO0O0OOO00O0 ):#line:282
        if OO00OOO0O0OOO00O0 .mName =='lsyncd_logs':#line:283
            OOO0O00OO00O00OOO =O00000O000O0OO0OO .rsyn_path +'/lsyncd.log';#line:284
            O00000O000O0OO0OO .__O0OO0O0OOO000OOO0 ('清空实时同步日志');#line:285
        else :#line:286
            OOO0O00OO00O00OOO =O00000O000O0OO0OO .rsyn_path +'/sclient/'+OO00OOO0O0OOO00O0 .mName +'_exec.log';#line:287
            O00000O000O0OO0OO .__O0OO0O0OOO000OOO0 ('清空发送日志['+OO00OOO0O0OOO00O0 .mName +']');#line:288
        public .writeFile (OOO0O00OO00O00OOO ,'');#line:289
        return public .returnMsg (True ,'清除成功!');#line:291
    def exec_cmd (O0O0OO0OO0OOO0O0O ,O0O0O00OO000OO0O0 ):#line:293
        OO0O0OO0O0O0OOO0O =O0O0OO0OO0OOO0O0O .rsyn_path +'/sclient/'+O0O0O00OO000OO0O0 ['mName']+'_cmd'#line:294
        O0OO00000O0O0000O =O0O0OO0OO0OOO0O0O .get_send_byname (O0O0O00OO000OO0O0 )#line:295
        public .writeFile (OO0O0OO0O0O0OOO0O ,O0O0OO0OO0OOO0O0O .__O0O0O00O0O0OOO0OO (O0OO00000O0O0000O ))#line:296
        os .system ('echo "【'+public .getDate ()+'】" >> '+O0O0OO0OO0OOO0O0O .rsyn_path +"/sclient/"+O0O0O00OO000OO0O0 .mName +"_exec.log")#line:298
        public .ExecShell ("nohup bash "+OO0O0OO0O0O0OOO0O +" >> "+O0O0OO0OO0OOO0O0O .rsyn_path +"/sclient/"+O0O0O00OO000OO0O0 .mName +"_exec.log 2>&1 &")#line:299
        O0O0OO0OO0OOO0O0O .__O0OO0O0OOO000OOO0 ('手动执行同步任务['+O0O0O00OO000OO0O0 ['mName']+']');#line:300
        return public .returnMsg (True ,'同步指令已发送!');#line:301
    def remove_send (OOO0O000OOO0O0O00 ,OOO0O0O00OOO0O0OO ):#line:303
        O000O00OO000000O0 =OOO0O000OOO0O0O00 .get_rsync_conf (None );#line:304
        for O0OO00OO00O000O00 in xrange (len (O000O00OO000000O0 ['client'])):#line:305
            if O000O00OO000000O0 ['client'][O0OO00OO00O000O00 ]['name']!=OOO0O0O00OOO0O0OO .mName :continue ;#line:306
            O000O00OO000000O0 ['client'][O0OO00OO00O000O00 ]['realtime']=True #line:307
            OOO0O000OOO0O0O00 .__O0OO0000OO0OO0OO0 (O000O00OO000000O0 ['client'][O0OO00OO00O000O00 ],OOO0O0O00OOO0O0OO )#line:308
            del (O000O00OO000000O0 ['client'][O0OO00OO00O000O00 ])#line:309
            public .ExecShell ("rm -f "+OOO0O000OOO0O0O00 .rsyn_path +'/sclient/'+OOO0O0O00OOO0O0OO .mName +'_*')#line:310
            OOO0O000OOO0O0O00 .__O00OOOOO0000OO00O (O000O00OO000000O0 ,True )#line:311
            OOO0O000OOO0O0O00 .__O0OO0O0OOO000OOO0 ('删除发送配置['+OOO0O0O00OOO0O0OO ['mName']+']');#line:312
            break ;#line:313
        return public .returnMsg (True ,'删除成功!');#line:314
    def get_exclude (O000O000O0O0O0O00 ,O0O00000OO00O00OO ):#line:316
        O0O000O0O00OOOO00 =O000O000O0O0O0O00 .get_rsync_conf (None );#line:317
        for O0000OOO0OOOO00O0 in xrange (len (O0O000O0O00OOOO00 ['client'])):#line:318
            if O0O000O0O00OOOO00 ['client'][O0000OOO0OOOO00O0 ]['name']==O0O00000OO00O00OO ['mName']:return O0O000O0O00OOOO00 ['client'][O0000OOO0OOOO00O0 ]['exclude'];#line:319
        return public .returnMsg (False ,'指定任务不存在!');#line:320
    def add_exclude (O0000O00OOOO00OOO ,OOOO0O0OOO0O0OO00 ):#line:322
        OOO00O0O00OO0OO00 =O0000O00OOOO00OOO .get_rsync_conf (None );#line:323
        for OO0O0O000O0O00000 in xrange (len (OOO00O0O00OO0OO00 ['client'])):#line:324
            if OOO00O0O00OO0OO00 ['client'][OO0O0O000O0O00000 ]['name']!=OOOO0O0OOO0O0OO00 ['mName']:continue ;#line:325
            OOO00O0O00OO0OO00 ['client'][OO0O0O000O0O00000 ]['exclude'].insert (0 ,OOOO0O0OOO0O0OO00 .exclude )#line:326
            O0000O00OOOO00OOO .__O00OOOOO0000OO00O (OOO00O0O00OO0OO00 ,True )#line:327
            O0000O00OOOO00OOO .__O0OO0O0OOO000OOO0 ('添加排除规则['+OOOO0O0OOO0O0OO00 .exclude +']到['+OOOO0O0OOO0O0OO00 ['mName']+']');#line:328
            break ;#line:329
        return public .returnMsg (True ,'添加成功!');#line:330
    def remove_exclude (O0OO000OOOO000000 ,O0OO00O0O00000O0O ):#line:332
        OOOO0OO00OOO0OOO0 =O0OO000OOOO000000 .get_rsync_conf (None );#line:333
        for O00O0OO00O0000O0O in xrange (len (OOOO0OO00OOO0OOO0 ['client'])):#line:334
            if OOOO0OO00OOO0OOO0 ['client'][O00O0OO00O0000O0O ]['name']!=O0OO00O0O00000O0O ['mName']:continue ;#line:335
            OOOO0OO00OOO0OOO0 ['client'][O00O0OO00O0000O0O ]['exclude'].remove (O0OO00O0O00000O0O .exclude )#line:336
            O0OO000OOOO000000 .__O00OOOOO0000OO00O (OOOO0OO00OOO0OOO0 ,True )#line:337
            O0OO000OOOO000000 .__O0OO0O0OOO000OOO0 ('从['+O0OO00O0O00000O0O ['mName']+']删除排除规则['+O0OO00O0O00000O0O .exclude +']');#line:338
            break ;#line:339
        return public .returnMsg (True ,'删除成功!');#line:340
    def rsync_service (OOO0OOO0O00O0OOOO ,O00OO0O000OOOOO00 ):#line:342
        O0O000000OO0O0O0O ="/etc/init.d/rsynd "+O00OO0O000OOOOO00 .state #line:343
        public .ExecShell (O0O000000OO0O0O0O );#line:344
        OOO0OOO0O00O0OOOO .__O000000OO0OOOO0O0 (O00OO0O000OOOOO00 );#line:345
        OOO0OOO0O00O0OOOO .__O0OO0O0OOO000OOO0 (O0O000000OO0O0O0O +'已执行');#line:346
        return public .returnMsg (True ,'操作成功!');#line:347
    def __OO0O00OOO000000OO (O0O00OO00O00O0OO0 ,OO0000O00O00OO000 ):#line:349
        O0000OO0O0000OOO0 ="settings {\n"#line:350
        for OOO0OOO0OO0OOOOOO in OO0000O00O00OO000 ['settings'].keys ():#line:351
            if re .search ("^\d+$",OO0000O00O00OO000 ['settings'][OOO0OOO0OO0OOOOOO ])or OO0000O00O00OO000 ['settings'][OOO0OOO0OO0OOOOOO ]in ['true','false']:#line:352
                O0000OO0O0000OOO0 +="\t"+OOO0OOO0OO0OOOOOO +' = '+OO0000O00O00OO000 ['settings'][OOO0OOO0OO0OOOOOO ]+','+"\n"#line:353
            else :#line:354
                O0000OO0O0000OOO0 +="\t"+OOO0OOO0OO0OOOOOO +' = "'+OO0000O00O00OO000 ['settings'][OOO0OOO0OO0OOOOOO ]+'",'+"\n"#line:355
        O0000OO0O0000OOO0 =O0000OO0O0000OOO0 [:-2 ]+"\n}\n";#line:356
        for OO0000O00OO0OO000 in OO0000O00O00OO000 ['client']:#line:358
            if OO0000O00OO0OO000 ['model']=='default.rsync':#line:359
                O0000OO0O0000OOO0 +=O0O00OO00O00O0OO0 .__OOO00O0O00OOOOO00 (OO0000O00OO0OO000 );#line:360
                O0O00OO00O00O0OO0 .__OO00O00O000OO0O0O (OO0000O00OO0OO000 ['name'],OO0000O00OO0OO000 ['password'])#line:361
            else :#line:362
                O0000OO0O0000OOO0 +=O0O00OO00O00O0OO0 .__O0OOO0OOO0OOO00OO (OO0000O00OO0OO000 );#line:363
        public .writeFile (O0O00OO00O00O0OO0 .lsync_file ,O0000OO0O0000OOO0 )#line:364
        if os .path .exists ('/etc/init.d/lsyncd'):#line:365
            public .ExecShell ("/etc/init.d/lsyncd restart");#line:366
        else :#line:367
            public .ExecShell ("systemctl restart lsyncd");#line:368
        return True #line:369
    def __O0OOO0OOO0OOO00OO (O0OO0000O00OOO00O ,O000OOOO0O00O00O0 ):#line:371
        O0OO0OO00OOOO00OO =O0OO0000O00OOO00O .__O000OOOOOO0O00OOO (O000OOOO0O00O00O0 ['exclude'])#line:372
        O0O0OOO00OO0O00OO ='''
sync {
    default.direct,
    source    = "%s",
    target    = "%s",
    delay = 1,
    maxProcesses = 2,
    exclude = {%s}
}
'''%(O000OOOO0O00O00O0 ['path'],O000OOOO0O00O00O0 ['to'],O0OO0OO00OOOO00OO )#line:382
        return O0O0OOO00OO0O00OO #line:383
    def __O000OOOOOO0O00OOO (O0OO0O0O0OO0O0000 ,O0OOOOO0OOOO000OO ):#line:385
        O00O00O00OOO0OO0O ='"'+'","'.join (O0OOOOO0OOOO000OO )+'"';#line:386
        if O00O00O00OOO0OO0O =='""':#line:387
            O00O00O00OOO0OO0O ='".user.ini"';#line:388
        else :#line:389
            O00O00O00OOO0OO0O +=',".user.ini"';#line:390
        return O00O00O00OOO0OO0O #line:391
    def __OOO00O0O00OOOOO00 (OOOOOOO000O0000OO ,O0OO00000O0000OO0 ):#line:393
        O0O000000OOO000OO =OOOOOOO000O0000OO .rsyn_path +'/sclient/'+O0OO00000O0000OO0 ['name']+'_pass'#line:394
        OO0O0O000O0OOO0OO =OOOOOOO000O0000OO .__O000OOOOOO0O00OOO (O0OO00000O0000OO0 ['exclude'])#line:395
        OO00O00O000000O0O ='''
sync {
    %s,
    source = "%s",
    target = "%s@%s::%s",
    delete = %s,
    exclude = {%s},
    delay = %s,
    init = false,
    rsync = {
        binary = "%s",
        archive = %s,
        compress = %s,
        verbose = %s,
        password_file = "%s",
        _extra = {"--bwlimit=%s","--port=%s"}
    }
}'''%(O0OO00000O0000OO0 ['model'],O0OO00000O0000OO0 ['path'],O0OO00000O0000OO0 ['name'],O0OO00000O0000OO0 ['ip'],O0OO00000O0000OO0 ['name'],O0OO00000O0000OO0 ['delete'],OO0O0O000O0OOO0OO ,O0OO00000O0000OO0 ['delay'],OOOOOOO000O0000OO .__OO0O00O0OOOO0OOOO ,O0OO00000O0000OO0 ['rsync']["archive"],O0OO00000O0000OO0 ['rsync']["compress"],O0OO00000O0000OO0 ['rsync']["verbose"],O0O000000OOO000OO ,O0OO00000O0000OO0 ['rsync']["bwlimit"],O0OO00000O0000OO0 ['rsync']["port"])#line:428
        return OO00O00O000000O0O ;#line:429
    def __O0OO0000OO0OO0OO0 (OO0OO00OO000O000O ,O0OOO000OOOO00OO0 ,get ={}):#line:433
        OOO000O0O0OOOOOOO ='%s_%s'%(O0OOO000OOOO00OO0 ['ip'],O0OOO000OOOO00OO0 ['name'])#line:434
        O0O00O000000O0000 =public .M ('crontab').where ("name=?",('R'+OOO000O0O0OOOOOOO ,)).field ('id').find ()#line:435
        if O0O00O000000O0000 :#line:436
            get ['id']=O0O00O000000O0000 ['id']#line:437
            OO0OO00OO000O000O .__O000OO0OO0O0OO0O0 (get )#line:438
        O0O00O000000O0000 =public .M ('crontab').where ("name=?",('定时数据同步任务【'+O0OOO000OOOO00OO0 ['name']+'】',)).field ('id').find ()#line:440
        if O0O00O000000O0000 :#line:441
            get ['id']=O0O00O000000O0000 ['id']#line:442
            OO0OO00OO000O000O .__O000OO0OO0O0OO0O0 (get )#line:443
        if O0OOO000OOOO00OO0 ['realtime']:return True #line:445
        OO0O0O00OO00OO000 ='`date +\"%Y-%m-%d %H:%M:%S\"`';#line:446
        OO0OO00OO000O000O .__O0O0O00O0O0OOO0OO (O0OOO000OOOO00OO0 )#line:447
        O0OOOOO0OO0OOO0O0 ='''
rname="%s"
plugin_path="%s"
logs_file=$plugin_path/sclient/${rname}_exec.log
echo "★【%s】 STSRT" >> $logs_file
echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" >> $logs_file
bash $plugin_path/sclient/${rname}_cmd >> $logs_file 2>&1
echo "【%s】 END★" >> $logs_file
echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<" >> $logs_file
'''%(O0OOO000OOOO00OO0 ['name'],OO0OO00OO000O000O .rsyn_path ,OO0O0O00OO00OO000 ,OO0O0O00OO00OO000 )#line:457
        OO00OO0000000OOO0 ={}#line:458
        OO00OO0000000OOO0 ['backupTo']='localhost'#line:459
        OO00OO0000000OOO0 ['sType']='toShell'#line:460
        OO00OO0000000OOO0 ['week']=''#line:461
        OO00OO0000000OOO0 ['sName']=''#line:462
        OO00OO0000000OOO0 ['urladdress']=''#line:463
        OO00OO0000000OOO0 ['save']=''#line:464
        OO00OO0000000OOO0 ['name']='定时数据同步任务【'+O0OOO000OOOO00OO0 ['name']+'】'#line:466
        OO00OO0000000OOO0 ['type']=O0OOO000OOOO00OO0 ['cron']['type']#line:467
        OO00OO0000000OOO0 ['where1']=O0OOO000OOOO00OO0 ['cron']['where1']#line:468
        OO00OO0000000OOO0 ['sBody']=O0OOOOO0OO0OOO0O0 #line:469
        OO00OO0000000OOO0 ['hour']=O0OOO000OOOO00OO0 ['cron']['hour']#line:470
        OO00OO0000000OOO0 ['minute']=O0OOO000OOOO00OO0 ['cron']['minute']#line:471
        crontab .crontab ().AddCrontab (OO00OO0000000OOO0 )#line:473
        return True #line:474
    def __O000000OO0OOOO0O0 (OOO0O0OO0OO00O0OO ,O00000O00OOOO000O ):#line:476
        import firewalls ;#line:477
        O00000O00OOOO000O .port =str (OOO0O0OO0OO00O0OO .get_rsync_conf (None )['global']['port']);#line:478
        O00000O00OOOO000O .ps ='数据同步工具rsync端口';#line:479
        firewalls .firewalls ().AddAcceptPort (O00000O00OOOO000O );#line:480
    def __O000OO0OO0O0OO0O0 (O0O00000O0O00OO0O ,O000O00OO0OO0O0O0 ):#line:482
        crontab .crontab ().DelCrontab (O000O00OO0OO0O0O0 )#line:483
    def __O0O0O00O0O0OOO0OO (OO0O0OOO00OOO00OO ,O0O000O00O00OOO00 ):#line:485
        OOOO0OOOOO000O0OO =OO0O0OOO00OOO00OO .rsyn_path +'/sclient/'+O0O000O00O00OOO00 ['name']+'_exclude'#line:486
        O0OO000OO0000OO00 =OO0O0OOO00OOO00OO .rsyn_path +'/sclient/'+O0O000O00O00OOO00 ['name']+'_pass'#line:487
        public .writeFile (OOOO0OOOOO000O0OO ,("\n".join (O0O000O00O00OOO00 ['exclude'])+"\n.user.ini").strip ()+"\n");#line:488
        OO0O0OOO00OOO00OO .__OO00O00O000OO0O0O (O0O000O00O00OOO00 ['name'],O0O000O00O00OOO00 ['password'],False )#line:489
        if O0O000O00O00OOO00 ['model']=='default.rsync':#line:490
            __OO0OOOOOOOOO0OO0O =''#line:491
            if O0O000O00O00OOO00 ['delete']=='true':__OO0OOOOOOOOO0OO0O =' --delete';#line:492
            OOO000OO0000OO0OO =OO0O0OOO00OOO00OO .__OO0O00O0OOOO0OOOO +' -avzP'+__OO0OOOOOOOOO0OO0O +' --port='+O0O000O00O00OOO00 ['rsync']['port']+' --bwlimit='+O0O000O00O00OOO00 ['rsync']['bwlimit']+' --exclude-from='+OOOO0OOOOO000O0OO +' --password-file='+O0OO000OO0000OO00 +' '+O0O000O00O00OOO00 ['path']+' '+O0O000O00O00OOO00 ['name']+'@'+O0O000O00O00OOO00 ['ip']+'::'+O0O000O00O00OOO00 ['name']#line:496
        else :#line:497
            OOO000OO0000OO0OO =OO0O0OOO00OOO00OO .__OO0O00O0OOOO0OOOO +" -avzP --exclude-from="+OOOO0OOOOO000O0OO +' '+O0O000O00O00OOO00 ['path']+' '+O0O000O00O00OOO00 ['to'];#line:498
        return OOO000OO0000OO0OO ;#line:499
    def __O00OO0OOO0OO00OO0 (OO000OOO00000OO00 ,OO00000OOO0O0OO00 ):#line:501
        OOOOO0OO00OOOOO0O ='';#line:502
        for O0O000O00O0O000OO in OO00000OOO0O0OO00 ['global'].keys ():#line:503
            if type (OO00000OOO0O0OO00 ['global'][O0O000O00O0O000OO ])!=bool :#line:504
                OOOOO0OO00OOOOO0O +=O0O000O00O0O000OO +' = '+str (OO00000OOO0O0OO00 ['global'][O0O000O00O0O000OO ])+"\n"#line:505
            else :#line:506
                OOOOO0OO00OOOOO0O +=O0O000O00O0O000OO +"\n"#line:507
        O00OO00O0O000O000 =['name','password','addtime']#line:508
        for O0OOO0OOOO0OO000O in OO00000OOO0O0OO00 ['modules']:#line:509
            OOOOO0OO00OOOOO0O +="\n";#line:510
            OOOOO0OO00OOOOO0O +="["+O0OOO0OOOO0OO000O ['name']+"]\n"#line:511
            OO000OOO00000OO00 .__OO0O0O0000O000000 (O0OOO0OOOO0OO000O ['name'],O0OOO0OOOO0OO000O ['auth users'],O0OOO0OOOO0OO000O ['password'])#line:512
            if not os .path .exists (O0OOO0OOOO0OO000O ['path']):public .ExecShell ("mkdir -p "+O0OOO0OOOO0OO000O ['path'])#line:513
            for OO00OOO000OOOO000 in O0OOO0OOOO0OO000O .keys ():#line:515
                if OO00OOO000OOOO000 in O00OO00O0O000O000 :continue ;#line:516
                OOOOO0OO00OOOOO0O +="\t"#line:517
                if type (O0OOO0OOOO0OO000O [OO00OOO000OOOO000 ])!=bool :#line:518
                    OOOOO0OO00OOOOO0O +=OO00OOO000OOOO000 +' = '+str (O0OOO0OOOO0OO000O [OO00OOO000OOOO000 ])+"\n"#line:519
                else :#line:520
                    OOOOO0OO00OOOOO0O +=OO00OOO000OOOO000 +"\n"#line:521
        public .writeFile (OO000OOO00000OO00 .rsyn_file ,OOOOO0OO00OOOOO0O )#line:522
        public .ExecShell ("/etc/init.d/rsynd restart");#line:523
        return True #line:524
    def __OO0O0O0000O000000 (O0O00OOO0000O0O0O ,OO00O000O000O00O0 ,OO0O0OO0000O000OO ,OOOOO00O0O00OO0OO ,focre =True ):#line:526
        O00O00O00O0OOO00O =O0O00OOO0000O0O0O .rsyn_path +'/secrets/'+OO00O000O000O00O0 +'.db';#line:527
        if os .path .exists (O00O00O00O0OOO00O )and focre :return True ;#line:528
        public .writeFile (O00O00O00O0OOO00O ,OO0O0OO0000O000OO +':'+OOOOO00O0O00OO0OO )#line:529
        public .ExecShell ("chmod 600 "+O00O00O00O0OOO00O )#line:530
        return True #line:531
    def __OO00O00O000OO0O0O (O00OO0O0OO0OOO00O ,OOOO0O00OOO00O00O ,OO00O0O000000000O ,focre =True ):#line:533
        O000OO00OOOOOO0OO =O00OO0O0OO0OOO00O .rsyn_path +'/sclient/'+OOOO0O00OOO00O00O +'_pass';#line:534
        if os .path .exists (O000OO00OOOOOO0OO )and focre :return True ;#line:535
        public .writeFile (O000OO00OOOOOO0OO ,OO00O0O000000000O )#line:536
        public .ExecShell ("chmod 600 "+O000OO00OOOOOO0OO )#line:537
        return True #line:538
    def __O00OOOOO0000OO00O (OO0OO0O0000OO000O ,OO0OOOOOO000OO000 ,lsyncd =False ):#line:540
        public .writeFile (OO0OO0O0000OO000O .rsyn_path +'/config.json',json .dumps (OO0OOOOOO000OO000 ))#line:541
        if not lsyncd :#line:542
            OO0OO0O0000OO000O .__O00OO0OOO0OO00OO0 (OO0OOOOOO000OO000 )#line:543
        else :#line:544
            OO0OO0O0000OO000O .__OO0O00OOO000000OO (OO0OOOOOO000OO000 )#line:545
        return True #line:546
    def __O0OO0O0OOO000OOO0 (OOO00O0OO00O000O0 ,OO0OO00OO000O0O00 ):#line:548
        public .WriteLog ('数据同步工具',OO0OO00OO000O0O00 );#line:549
    def __OOOOOOO000OOOOOO0 (O0OOO0OO0OO0O000O ,O0OOO0OOOO000OO0O ):#line:551
        OOO0000O0O000000O =O0OOO0OO0OO0O000O .get_rsync_conf (None )#line:552
        for O0OOOOO0OO00O0O00 in OOO0000O0O000000O ['modules']:#line:553
            if O0OOOOO0OO00O0O00 ['name']==O0OOO0OOOO000OO0O :return True ;#line:554
        return False #line:555
    def __O0OO00O0O00OOOO0O (OOO0O0OO00O0OO000 ,O000O00O00000OOOO ):#line:557
        O00O0O0O000OO0OOO =OOO0O0OO00O0OO000 .get_rsync_conf (None )#line:558
        for O00OOOO0O000OO000 in O00O0O0O000OO0OOO ['client']:#line:559
            if O00OOOO0O000OO000 ['name']==O000O00O00000OOOO :return True ;#line:560
        return False #line:561
    def __OO00OO0OO00O0O0O0 (OOOO00000OOO00O00 ,O0OO000O0OOO00OOO ):#line:563
        if O0OO000O0OOO00OOO [-1 ]!='/':O0OO000O0OOO00OOO +='/'#line:564
        for O0O0O0OO00O0O0OOO in ['/usr/','/var/','/proc/','/boot/','/etc/','/dev/','/root/','/run/','/sys/','/tmp/']:#line:565
            if re .match ('^'+O0O0O0OO00O0O0OOO ,O0OO000O0OOO00OOO ):return True #line:566
        if O0OO000O0OOO00OOO in ['/','/www/','/www/server/','/home/']:return True #line:567
        return False #line:568
    def to_new_version (OO0OO0O000O0O0O0O ,get =None ):#line:570
        if not os .path .exists (OO0OO0O000O0O0O0O .rsyn_path +'secrets'):#line:571
            os .mkdir (OO0OO0O000O0O0O0O .rsyn_path +'secrets')#line:572
        if not os .path .exists (OO0OO0O000O0O0O0O .rsyn_file ):#line:574
            os .mknod (OO0OO0O000O0O0O0O .rsyn_file )#line:575
            OOOOOO0O00OO0O0OO ='''uid = root
gid = root
use chroot = yes
port = 873
hosts allow =
log file = /var/log/rsyncd.log
pid file = /var/run/rsyncd.pid
            '''#line:583
            public .ExecShell ('echo "%s" > %s'%(OOOOOO0O00OO0O0OO ,OO0OO0O000O0O0O0O .rsyn_file ))#line:584
        OO0OO0O000O0O0O0O .rsyn_conf ={}#line:585
        with open (OO0OO0O000O0O0O0O .rsyn_file ,"r")as OO0OOO0OO00OO0OO0 :#line:586
            O0OO0OOO0OOO0OO0O ='is_global'#line:587
            OO0OO0O000O0O0O0O .rsyn_conf [O0OO0OOO0OOO0OO0O ]={}#line:588
            for OO00000OO00O0000O in OO0OOO0OO00OO0OO0 :#line:589
                if not re .match ("^[\s]*?#",OO00000OO00O0000O )and OO00000OO00O0000O !="\n":#line:590
                    OOOO000O00OOOO0O0 =re .findall ("\[(.*?)\]",OO00000OO00O0000O )#line:591
                    if OOOO000O00OOOO0O0 :#line:592
                        O0OO0OOO0OOO0OO0O =OOOO000O00OOOO0O0 [0 ]#line:593
                        OO0OO0O000O0O0O0O .rsyn_conf [O0OO0OOO0OOO0OO0O ]={}#line:594
                    else :#line:595
                        try :#line:596
                            O00O000O00OO00OO0 =OO00000OO00O0000O .split ('=')#line:597
                            O0O0O0O0O0O00OOOO =O00O000O00OO00OO0 [0 ].strip ()#line:598
                            O000OOO00O000OO0O =O00O000O00OO00OO0 [1 ].strip ()#line:599
                            if O0OO0OOO0OOO0OO0O =='is_global'and O0O0O0O0O0O00OOOO in ["log file","pid file","uid","gid","use chroot"]:#line:600
                                continue #line:601
                            if O0O0O0O0O0O00OOOO =="secrets file":#line:602
                                OOOO0OO00OOO0OOOO =re .findall (":(\w+)",public .readFile (O000OOO00O000OO0O ))[0 ]#line:604
                                OO0OO0O000O0O0O0O .rsyn_conf [O0OO0OOO0OOO0OO0O ]["passwd"]=OOOO0OO00OOO0OOOO #line:605
                                continue #line:606
                            if O0O0O0O0O0O00OOOO =="auth users":#line:607
                                continue #line:608
                                O0O0O0O0O0O00OOOO ="user"#line:609
                            if O0O0O0O0O0O00OOOO =="hosts allow":#line:610
                                O0O0O0O0O0O00OOOO ="ip"#line:611
                                O000OOO00O000OO0O =O000OOO00O000OO0O .replace (",","\n")#line:612
                            if O0O0O0O0O0O00OOOO =="dont commpress":#line:613
                                O0O0O0O0O0O00OOOO ="dont_commpress"#line:614
                                O000OOO00O000OO0O =O000OOO00O000OO0O .replace (' *.',',')[2 :]#line:615
                            O0O0O0O0O0O00OOOO =O0O0O0O0O0O00OOOO .replace (" ","_")#line:616
                            OO0OO0O000O0O0O0O .rsyn_conf [O0OO0OOO0OOO0OO0O ][O0O0O0O0O0O00OOOO ]=O000OOO00O000OO0O #line:617
                        except :#line:618
                            pass #line:619
            if not 'port'in OO0OO0O000O0O0O0O .rsyn_conf ['is_global'].keys ():#line:621
                OO0OO0O000O0O0O0O .rsyn_conf ['is_global']['port']=873 #line:622
            if not 'ip'in OO0OO0O000O0O0O0O .rsyn_conf ['is_global'].keys ():#line:623
                OO0OO0O000O0O0O0O .rsyn_conf ['is_global']['ip']=''#line:624
            O0O0000000O00OOO0 =OO0OO0O000O0O0O0O .get_rsync_conf (None )#line:626
            O0O0000000O00OOO0 ['global']['port']=OO0OO0O000O0O0O0O .rsyn_conf ['is_global']['port']#line:627
            del (OO0OO0O000O0O0O0O .rsyn_conf ['is_global'])#line:628
            for O0OO0000OO0OOOO00 in OO0OO0O000O0O0O0O .rsyn_conf .keys ():#line:629
                OOO00O0OOO00OO00O =OO0OO0O000O0O0O0O .rsyn_path +'/secrets/'+O0OO0000OO0OOOO00 +'.db';#line:630
                OOO00O0O00OOO0OOO =True ;#line:631
                for O0O000OO0OO0000O0 in O0O0000000O00OOO0 ['modules']:#line:632
                    if O0O000OO0OO0000O0 ['name']==O0OO0000OO0OOOO00 :#line:633
                        OOO00O0O00OOO0OOO =False #line:634
                        break ;#line:635
                if not OOO00O0O00OOO0OOO :continue ;#line:636
                O0O0O0OOO0O0OOO00 ={'name':O0OO0000OO0OOOO00 ,'path':OO0OO0O000O0O0O0O .rsyn_conf [O0OO0000OO0OOOO00 ]['path'],'password':OO0OO0O000O0O0O0O .rsyn_conf [O0OO0000OO0OOOO00 ]['passwd'],'comment':OO0OO0O000O0O0O0O .rsyn_conf [O0OO0000OO0OOOO00 ]['comment'],'read only':'false','ignore errors':True ,'auth users':O0OO0000OO0OOOO00 ,'secrets file':OOO00O0OOO00OO00O ,'addtime':time .time ()}#line:647
                O0O0000000O00OOO0 ['modules'].insert (0 ,O0O0O0OOO0O0OOO00 )#line:648
            O0OOOOOOO0O00OO0O =public .readFile (OO0OO0O000O0O0O0O .rsyn_path +'/serverdict.json')#line:650
            if O0OOOOOOO0O00OO0O :#line:651
                O0OOOOOOO0O00OO0O =json .loads (O0OOOOOOO0O00OO0O )#line:652
                for O0OO0000OO0OOOO00 in O0OOOOOOO0O00OO0O .keys ():#line:653
                    del (O0OOOOOOO0O00OO0O [O0OO0000OO0OOOO00 ]['cron_info']['id']);#line:654
                    OO00OO0OO00OOO0O0 =O0OO0000OO0OOOO00 .split ('_')#line:655
                    OO0O0OOOOOOO00OOO ={'model':'default.rsync','name':O0OO0000OO0OOOO00 ,'ip':OO00OO0OO00OOO0O0 [0 ],'password':public .readFile (OO0OO0O000O0O0O0O .rsyn_path +'/sclient/'+O0OO0000OO0OOOO00 +'.db'),'path':O0OOOOOOO0O00OO0O [O0OO0000OO0OOOO00 ]['path'],'to':'','exclude':[],'delete':'false','realtime':O0OOOOOOO0O00OO0O [O0OO0000OO0OOOO00 ]['inotify_info'],'delay':3 ,'rsync':{'bwlimit':'200','port':str (O0OOOOOOO0O00OO0O [O0OO0000OO0OOOO00 ]['port']),'compress':'true','archive':'true','verbose':'true'},'ps':'','cron':O0OOOOOOO0O00OO0O [O0OO0000OO0OOOO00 ]['cron_info'],'addtime':time .time ()}#line:677
                    O0O0000000O00OOO0 ['client'].insert (0 ,OO0O0OOOOOOO00OOO )#line:678
                os .remove (OO0OO0O000O0O0O0O .rsyn_path +'/serverdict.json')#line:679
            public .writeFile (OO0OO0O000O0O0O0O .rsyn_path +'/config.json',json .dumps (O0O0000000O00OOO0 ))#line:680
