a
    �%`��  �                   @   s�  d dl Z d dlZd dlZd dlZd dlZd dlZd dlmZ d dlZd dlZd dl	Z	d dl
Z
d dlZd dlZd dlZd dlZd dlZd dlmZ d dlZd dlmZ d dlmZmZmZmZmZmZmZmZ d dlmZmZ d dlm Z  d dl!m"Z"m#Z# d d	l$m%Z% d dl&Z&d dl'Z'G d
d� de�Z(G dd� de�Z)G dd� de�Z*dd� Z+dd� Z,dd� Z-dd� Z.dd� Z/dd� Z0dd� Z1dd� Z2d d!� Z3d"d#� Z4d$d%� Z5d&d'� Z6d(d)� Z7d*d+� Z8d,d-� Z9d.d/� Z:d0d1� Z;d2d3� Z<d4d5� Z=d6d7� Z>d8d9� Z?d:d;� Z@d<d=� ZAd>d?� ZBd@dA� ZCdBdC� ZDdDdE� ZEdFdG� ZFdHdI� ZGeHdJk�r�dKZIdLZJdMZKdNZLdOZMdPaNdPaOd aPd aQd aRdQZSdRZTe'�U� ZVdMaWdSZXejY�ZdTdU�Z[ejY�\ejY�]ej^d  ��Z_ejY�Ze[dV�a`ejY�Ze_dW�ZaejY�Ze_dX�ZbejY�ZdYdX�ZcejY�Ze_dZ�ZddMaedMafdMage-d[� e-d\� e-d]� e-d^� e-d_� e-d`� e-dM� e-dae�h� �idb� � e-dc� e-ddeT � e-dee_ � e-dft` � e-dgeb � e-dM� i ajdhtjdi< djtjdk< ejY�kea��r�e=ea�Zlel�mditjdi �tjdi< el�mdktjdk �tjdk< e-dlenea� � n*e-dmenea� � e>eatj� e-dnenea� � ejY�ZdYdo�ZoejY�Zdpdqdo�ZpdrZqg areeH�Zsees�Zte"es� et�ue(ds� et�ue)dt� et�ue*du� e �v� Zwdvew_xdwew_ye jzew_{e j|ew_}e j~ew_dSew_�dxew_�dxew_�dxew_�dyew_�dMZ�ze��dzej�ej�B �Z�dMZ�W n� e��yz Z� z�e-d{ene�� � ze��d|ej�ej�B �Z�W nR e��yd Z� z8e-d}ene�� � d~ene��v �rJe-d� e��  W Y dZ�[�n
dZ�[�0 0 W Y dZ�[�n
dZ�[�0 0 eG�  zesj�d�eSdrd�� W n   e-d�� e���  Y n0 dS )��    N)�datetime)�	unhexlify)�copyfile)�Flask�request�jsonify�Response�current_app�redirect�url_for�send_from_directory)�Resource�Api)�secure_filename)�CORS�cross_origin)�Timerc                   @   s   e Zd Zdd� ZdS )�Statusc                 C   s0   t }tj�dd�}tj�dd�}t||t�}|S )N�callbackF�_)�json_data_latestr   �args�get�jsonpr	   )�self�
statusDatar   �token�jsonp_response� r   �pd-axpert.pyr   D   s
    z
Status.getN��__name__�
__module__�__qualname__r   r   r   r   r   r   C   s   r   c                   @   s   e Zd Zdd� ZdS )�Datac                 C   s.   t t�}t|j�d��}d}tj||d�}|S )N�utf8zapplication/json��mimetype)r   r   �str�data�decoder	   �response_class)r   �jsonData�json_data_strr'   �formated_responser   r   r   r   R   s
    zData.getNr    r   r   r   r   r$   Q   s   r$   c                   @   s   e Zd Zdd� ZdS )�Settingsc           
      C   s�  d}d}d}t d� tj�dd�}t�tj�dd��}t dt|d � � |d �d	�r�t d
t|d d	 � � |d d	 td	< |d d	 td	< |d d	 t	d	< t
tt� |d �d��rt dt|d d � � |d d td< |d d td< |d d t	d< t
tt� d|d d�}|d �d��r�t d|d d d  � t|� dt d t d t d }t|�\}}|�r�d|d |�� d�}nd}d|d |�� |d�}t||t�}	|	S )N� �Falsez)[SETTINGS] Requesting Settings operationsr   Fr)   z[SETTINGS] Config : �config�unitnamez[SETTINGS] Unit Name : �
pvMaxInputz[SETTINGS] PV Max Input : Zsuccess)r)   �output�wifiz[SETTINGS] SSID : �ssidzif [ -f z ] ; then sh -c "cat z >> zS" > /dev/null 2>&1 ; wpa_cli -i $(ls /sys/class/net | grep -m1 wl) reconfigure ; fi)r)   r2   r5   z!No wpa_supplicant.conf file foundZfail)r)   r2   r5   �error)�debugPrintAndLogr   r   r   �json�loadsr(   �
configDatar   �main_json_data�saveJson�
configFile�writeWifiSettings�wpaSupplicantPath�tempwpapath�execBashCommand�stripr   r	   )
r   �filepath�bashCommandZpiArmr   Zsettings_json_datar   r5   r8   r   r   r   r   r   `   s>    

zSettings.getNr    r   r   r   r   r/   _   s   r/   c                 C   sB   t |�}t|j�d��}t| �d | d }d}|j||d�}|S )Nr%   �(�)zapplication/javascriptr&   )r   r(   r)   r*   r+   )Zcallback_data�	json_dataZcurrent_flask_appr,   r-   �contentr'   r.   r   r   r   r   �   s    r   c                 C   s   t | � d S �N)�print)ZtextToPrintr   r   r   �
debugPrint�   s    rM   c                 C   s   t | � t| � d S rK   )rM   �appendToLog)rJ   r   r   r   r9   �   s    r9   c                 C   s   t j�| �d dd � S )N�   ��os�path�splitext��filer   r   r   �fileExtension�   s    rV   c                 C   s   t j�| �d S )Nr   rP   rT   r   r   r   �fileName�   s    rW   c                 C   s  t �� �d�}tj�| �r�ttj�| ��}|dkr�z`t�	d�\}}}|dkr�t�
| t| �d | d t| � � td|  � W dS td|  � � W q�   td	|  d
 t| � d | d t| � � Y dS 0 ndS n(t�	d�\}}}|dkr�dS td|  � dS )Nz%Y-%m-%di -1�/i ���.z([LOG] Log Rotated. New Log File Started Tz-[LOG] Log cannot be Rotated. Disk space low. z[ERROR] Could not move z to Fz7[ERROR] Log cannot be created/appended. Disk space low.)r   �now�strftimerQ   rR   �exists�int�getsize�shutilZ
disk_usageZmoverW   rV   r9   )Zlog_fileZdayStampZlogFileSize�totalZusedZfreer   r   r   �checkLogSize�   s*    $,
ra   c                 C   s:   t �� �d�}tt�r6ttd| d d |  d d� d S )N�%Y-%m-%d %H:%M:%S�[�]� �
�a)r   rZ   r[   ra   �logFile�writeToFile)rJ   �	timeStampr   r   r   rN   �   s     rN   c              
   C   sl   z t | |�}|�|� |��  W nF tyP } zd}d| W  Y d }~S d }~0    d}d|  Y S 0 d S )NzFile Not Savedz[ERROR] )�open�write�close�IOError)rW   rJ   �flag�fp�eZ
writeErrorr   r   r   ri   �   s    

ri   c                 C   sV   d}d}z,t j| dt jt jd�}|�� d �d�}W n   d}d|  }Y n0 ||fS )N�   r0   T)�shell�stderr�stdoutr   �utf-8z$Could not execute bash command : %s )�
subprocess�Popen�PIPEZcommunicater*   )Zbashcmd�timeoutr8   Zp1r5   r   r   r   rC   �   s    rC   c                 C   s�   t j�t�rttt j�t�� | d dkrZd}tt|d� d}tt|d� d}tt|d� d}tt|d� d}tt|d� d	| d d
 d  d }tt|d� d| d d
 d  d }tt|d� d}tt|d� tdt � d S )Nr2   Zgoproz8ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
rg   zupdate_config=1
zcountry=GB
z,# New Wifi Network added by Playback Design
z
network={
z     ssid="r6   r7   z"
z
     psk="Zpasswordz}
z[WiFi] %s created locally)rQ   rR   r\   rB   Z
deleteFile�basenameri   r9   )rI   ZcontentLiner   r   r   r@     s(    r@   c                 C   s   t d| � td��d S )Nz!Signal handler called with signalZHandler)r9   �	Exception)Zsignum�framer   r   r   �handler_  s    
r~   c              
   C   s  d}|dkrt }|dkrt}�z�d}tdkr4t�� s>tdk�r�t| |�}d|v sX|dkrptdkrjt�d� W dS |szW d S t�	d	d|�}| d
k�r |�
�  |�
�  |s�W d S |�dd�}|�dd�}|d dkr�dtd< dtd< danj|d dk�r
dtd< dtd< danF|d dk�r.dtd< dtd< dan"|d dk�rPdtd< dtd< da|d td< |d td< |d td< |d td< |d td< |d td< |d  td!< |d" td#< |d$ td%< |d& td'< |d( td)< |d* td+< |d, td-< |d. td/< tt�td0< t|d �at|d �}	�n�| d1k�r�|�
�  |�
�  |�sFW d S |�dd�}|�dd�}|d dk�r�dtd< dtd< danj|d dk�r�dtd< dtd< danF|d dk�r�dtd< dtd< dan"|d dk�r�dtd< dtd< da|d td< |d td< |d td< |d td< |d td< |d td< |d  td!< |d" td#< |d$ td%< |d& td'< |d( td)< |d* td+< |d, td-< |d. td/< tt�td0< t|d �at|d �}	�n�| d2k�r�|�
�  |�s�W d S |�dd�}|d td3< |d td4< |d td5< |d td6< |d7 td8< |d9 td:< |d; td<< |d= td>< |d? td@< |dA tdB< |d tdC< |dD tdE< |dF tdG< |dH tdI< |dJ tdK< |d tdL< |d  tdM< |d$ tdN< n�| dOk�rd|�
�  |�s�W d S |�dd�}|d tdP< |d tdQ< |d7 tdR< |d9 tdS< |d; tdT< |d= tdU< |d? tdV< |dA tdW< |d tdX< |dF tdY< nJ| dZk�r�|�
�  |�s�W d S |�dd�}|d td[< |d td\< nW dS W nL t�y� }
 z2td]t|
� � td^|  d_ | � W Y d }
~
dS d }
~
0 0 |S )`N�����r   rO   r0   �serial�USB�NAKssg�������?z[^0-9. ]�QPGS0re   �c   �   �L�1ZGridmode�0Z	Solarmode�B�S�F�   ZThe_parallel_numZSerial_numberZ
Fault_code�
   ZLoad_percentage�   ZTotal_charging_current�   ZTotal_AC_output_active_power�   ZTotal_AC_output_apparent_power�   ZTotal_AC_output_percentage�   ZInverter_Status�   ZOutput_mode�   ZCharger_source_priority�   ZMax_Charger_current�   ZMax_Charger_range�   ZMax_AC_charger_currentZInverter_modeZQPGS1�QPIGSZGrid_voltageZGrid_frequencyZAC_output_voltageZAC_output_frequency�   ZAC_output_apparent_powerrr   ZAC_output_active_power�   ZOutput_Load_Percent�   ZBus_voltage�   ZBattery_voltage�	   ZBattery_charging_currentZBattery_capacity�   ZInverter_heatsink_temperature�   ZPV_input_current_for_battery�   ZPV_Input_Voltage�   ZBattery_voltage_from_SCCZBattery_discharge_currentZDevice_statusZPV_Input_Watt�Q1Z	SCCOkFlagZAllowSCCOkFlagZChargeAverageCurrentZSCCPWMTemperatureZInverterTemperatureZBatteryTemperatureZTransformerTemperatureZGPDATZFanLockStatusZFanPWM�QBVZBattery_voltage_compensatedZSoC� error parsing inverter data...: zproblem command: z: )�usb0�usb1�
connection�ser�isOpen�serial_command�time�sleep�re�sub�rstrip�splitr=   �mode0r(   r]   �parrallel_num�mode1r|   r9   )�command�inverterZstatus�devicer)   �responseZresponse_num�numsZ	nums_mode�loadrq   r   r   r   �get_datae  s   








r�   c               
   C   s�  �z�t dkrt�� st dk�rpd} d}tdt�}d|v rPt dkrJt�d� W dS |��  |�dd	�}t	|d
 �} tdt�}d|v r�t dkr�t�d� W dS |��  |�dd	�}t	|d �}t
|� |dkr�| dks�d} tdt�}n`|dk�r| dk�sBd} tdt�}n<|dk�r*| dk�sBd} tdt�}n| dk�sBd} tdt�}t
| � d|v �r�t dk�rht�d� W dS n t dk�r�t��  t
d� W dS W n8 t�y� } zt
dt|� � W Y d }~dS d }~0 0 | S )Nr�   r�   r   r�   r�   �      �?r0   re   r�   r�   r�   rr   i�  r�   Z	MUCHGC002i�  r�   Z	MUCHGC010i�  r�   Z	MUCHGC020�   Z	MUCHGC030�cannot use serial port ...r�   )r�   r�   r�   r�   r�   r�   r�   r�   r�   r]   r9   rm   r|   r(   )ZcurrentZ
load_powerr�   r�   rq   r   r   r   �set_charge_currentR  s\    	










r�   c               
   C   s�   d} z�t dkrt�� st dkrftdt�}d|v rHt dkrBt�d� W dS |��  |�dd	�}|d
 } nt dkr�t�	�  t
d� W dS W n6 ty� } zt
dt|� � W Y d }~dS d }~0 0 | S )N�8r�   r�   �QPIRIr�   r�   r0   re   r�   r�   r�   r�   �r�   r�   r�   r�   r�   r�   r�   r�   r�   rm   r9   r|   r(   )�output_source_priorityr�   r�   rq   r   r   r   �get_output_source_priority�  s$    


r�   c               
   C   s�   d} z�t dkrt�� st dkrftdt�}d|v rHt dkrBt�d� W dS |��  |�dd	�}|d
 } nt dkr�t�	�  t
d� W dS W n6 ty� } zt
dt|� � W Y d }~dS d }~0 0 | S )Nr�   r�   r�   r�   r�   r�   r0   re   r�   r�   r�   r�   r�   )�charger_source_priorityr�   r�   rq   r   r   r   �get_charger_source_priority�  s$    


r�   c              
   C   s�   | dks�z�t dkrt�� s"t dkrv| dkr>tdt�}t|� q�| dkrZtdt�}t|� q�| dkr�td	t�}t|� nt dkr�t��  td
� W dS W n6 ty� } ztdt|� � W Y d }~dS d }~0 0 dS )Nr0   r�   r�   r   ZPOP00rO   ZPOP01r�   �POP02r�   r�   �	r�   r�   r�   r�   r�   r9   rm   r|   r(   )r�   r�   rq   r   r   r   �set_output_source_priority�  s(    






r�   c              
   C   s�   | dks�z�t dkrt�� s"t dkr�| dkr>tdt�}t|� q�| dkrZtdt�}t|� q�| dkrvtd	t�}t|� q�| d
kr�tdt�}t|� nt dkr�t��  td� W dS W n6 ty� } ztdt|� � W Y d }~dS d }~0 0 dS )Nr0   r�   r�   r   ZPCP00rO   ZPCP01r�   ZPCP02r�   ZPCP03r�   r�   r�   )r�   r�   rq   r   r   r   �set_charger_source_priority�  s.    








r�   c                 C   s�   z�t | t� ttd���}|�dd� |�|�� d d� |�� dkrbtd� t | t� t�	| � � |�|�� d d� |�
�  |�d� t�||� |�d� |��  W d   � n1 s�0    Y  t t| � W dS    Y d	S 0 d S )
Nza+r   r�   rO   rd   zF[ERROR] File JSON data verify failed. Crating backup and removing file�,TF)r   �jsonfileTmprk   �seek�tell�readr9   �jsonfileBackuprQ   �remove�truncaterl   r:   �dumprm   )rR   r)   �outfiler   r   r   �save_tmp�  s(    




&
r�   c                 C   sX   i }z6t | ��}t�|�}W d   � n1 s.0    Y  W n   td|  � Y n0 |S )Nz[ERROR] Could not load )rk   r:   r�   r9   )�	json_fileZ	temp_data�fr   r   r   �loadJson  s    
,r�   c                 C   s�   t j�t j�| ��rtz:t| d��}t�||� W d   � n1 sB0    Y  W q�   td|  � t�	d� Y q�0 ntd|  � t�	d� d S )N�w�[ERROR] Could not save rO   z"[ERROR] Path missing. Cannot Save )
rQ   rR   r\   �dirnamerk   r:   r�   r9   �sys�exit)r�   r)   r�   r   r   r   r>   &  s    .r>   c                 C   s�   t | �r�tj�tj�| ��r�zjtj�| �r@t| |�}|dkr�� nDt| d��*}g }|�|� t	�
||� W d   � n1 sz0    Y  W q�   td|  � t�d� Y q�0 ntd|  � t�d� d S )NFr�   r�   rO   z.[ERROR] Solar Cache path missing. Cannot Save )ra   rQ   rR   r\   r�   �isfiler�   rk   �appendr:   r�   r9   r�   r�   )r�   r)   Z	tempCheckr�   Zarrayr   r   r   �saveJsonLog8  s    

.r�   c              
   C   sN   | a ztt| � W n6 tyH } ztdt|� � W Y d }~dS d }~0 0 dS )Nzerror sending to emoncms...: r0   rO   )r   r�   �jsonfiler|   r9   r(   )r)   rq   r   r   r   �	send_dataP  s    
	r�   c           
   
   C   s�  �z$d}t j�d�}| dkr(t�d�}n4t�| �tt|t�| ����ddd�� t�d� }t|�dk r�t	�
d	� t�||� nN|d d
� }|d
d � }t	�
d	� t�||� t	�
d	� t�||� t	�
d� t	�
d� t�|d��dd�}d|v r��q$z||�d�7 }W q�   td|� Y q�0 q�W n� t�y� } z�tdt|� d | � d}	d�shdt|�v �r�td� t	�
d� t�d� tdk�r�t	�
d� t��  t	�
d� W Y d }~dS W Y d }~n
d }~0 0 tj��  |S )Nr0   Zxmodemr�   u
   POP02âZ0xrO   �r�   gffffff�?r�   g      �?g333333�?�   �   (�    �   rv   z#This bit raw data caused an issue: z$[SERIAL] error reading inverter...: z. Response:z
[Errno 11]z
[Errno 19]z?[ERROR] USB not working or Device not found - rebooting in 5minih  zshutdown -Fr nowr�   r�   r�   )�crcmodZ
predefinedZmkCrcFunr(   �encoder   �hex�replace�lenr�   r�   rQ   rl   r�   r*   r9   r|   �systemr�   r�   rk   r�   ru   �flush)
r�   r�   r�   Zxmodem_crc_funcZcommand_crcZcmd1Zcmd2�rrq   r)   r   r   r   r�   p  sH    4









$
r�   c               
   C   s�  d} t � � t }�zBtdtt� d tt� d tt� d tt|�� d � tdk r�tdkr�tdkr�|d	kr�td
� tdt	�} n�tdk r�tdkr�tdkr�|d	k r�td� n�tdkr�tdkr�tdkr�td� tdt	�} t � � anXtdk �r
tdk�r
tdk�r
td� n0tdk�r2tdk�r2tdk�r2td� ntd� d| v �rRtd� W d S W n8 t
�y� } ztdt|� � W Y d }~d S d }~0 0 dS )Nz no command zLoad: z
 W, MODE: �|z, time: z secondsi�  rO   i,  z"Second inverter go to standby modeZ
MNCHGC1497z9waiting 5 minutes to be sure that inverter could go sleepi  r�   zSecond Inverter wake upZ
MNCHGC1498z Second inverter already sleepingzBoth inverters runningzNo idea what to dor�   z"Inverter didn't recognized commandz error setting inverter mode...: )r�   �wake_up_startr9   r(   r�   r�   r�   r]   r�   r�   r|   )r�   Ztime_tmprq   r   r   r   �dynamic_control�  s2    <  






r�   c                  C   s&   d} t | �\}}|r|�� }nd}|S )Nz�myIP=$(ip -4 addr show $(ls /sys/class/net | grep -m1 wl) | grep -oP "(?<=inet ).*(?=/)" ); if [ $myIP ] ; then echo $myIP ; else hostname -I | cut -d' ' -f1 ; fir0   �rC   rD   )rF   r5   r8   Ztemp_ipr   r   r   �getIP�  s    
r�   c                  C   s4   d} t | �\}}|r,|�� �dd��d�}ng }|S )NzMiwlist $(ls /sys/class/net | grep -m1 wl) scan | grep SSID | cut -d':' -f2- ;�"r0   rf   )rC   rD   r�   r�   )ZssidListr5   r8   Ztmp_ssid_listr   r   r   �getSSIDS�  s    r�   c                  C   s*   d} | }t |�\}}|r"|�� }nd}|S )Nz
iwgetid -rr0   r�   )Z
WifiActiverF   r5   r8   Z	temp_wifir   r   r   �getWifi�  s    
r�   c                  C   s&   d} | }t |�\}}|rd}nd}|S )Nzapan=$(ls /sys/class/net | grep pan); if [ $pan ]; then ip -4 addr show $pan | grep "\ UP\ "; fi ;�Truer0   )rC   )ZBtActiverF   r5   r8   Ztemp_btr   r   r   �getBluetooth�  s    r�   c                  C   s�   t � at� at� atg kr t� atr,t�	�  d} i a
t�� �d�}|t
d< tt
d< tt
d< tt
d< tt
d< tt
d< tt
d	< td
 t
d
< td t
d< td| �}td| �}td| �}tt
� ttt�at��  dS )Nr   rb   Z	Timestamp�serverZipr6   ZbtZssidsZhostnamer3   r4   r�   r�   r�   T)r�   �statusIpr�   �
statusWifir�   �statusBt�statusSsidListr�   �connectionTimerZcancelr=   r   rZ   r[   �serverVersion�localHostnamer<   r�   r�   r   �checkInterval�	getStatus�start)r�   rj   r)   r   r   r   r    s4    



r  �__main__z....orgr�   r0   z...r�   r   Z5009z	0.92 betarO   z/var�logzpd-axpert.logzpd-axpert.confzpd-axpert.jsonz/tmpzpd-axpert-backup.jsonz4           _         _                          _   z4 _ __   __| |       / \   __  ___ __   ___ _ __| |_ z4| '_ \ / _` |_____ / _ \  \ \/ / '_ \ / _ \ '__| __|z4| |_) | (_| |_____/ ___ \  >  <| |_) |  __/ |  | |_ z4| .__/ \__,_|    /_/   \_\/_/\_\ .__/ \___|_|   \__|z'|_|                            |_|     z#by PLAYBACK DESIGN - Copyright (c) z%Yz"                                  zServer Version   : %szInstall folder   : %szLog file         : %szJSON file        : %szHome Inverter 1r3   �500r4   z[SETUP] Config file loaded z[SETUP] No Config file found z [SETUP] New Config file created zwpa_supplicant.confz/etcZwpa_supplicantTz/statusz/dataz	/settingsz/dev/ttyUSB0i`	  Fr�   z/dev/hidraw0zError opening USB port 0 : z/dev/hidraw1zError opening USB port 1 : z	[Errno 2]z=[ERROR] USB Device not found. Unplug and re-connect - quitingz0.0.0.0)Zhost�portZthreadedz0[FATAL ERROR] Cannot start Flask Server. Quiting)�r�   r�   r�   �stringr:   Zurllibr   ZcalendarrQ   r�   r�   Zusb.coreZusbZusb.util�signalZbinasciir   r_   r   Zflaskr   r   r   r   r	   r
   r   r   Zflask_restfulr   r   Zwerkzeug.utilsr   Z
flask_corsr   r   Z	threadingr   rw   �platformr   r$   r/   r   rM   r9   rV   rW   ra   rN   ri   rC   r@   r~   r�   r�   r�   r�   r�   r�   r�   r�   r>   r�   r�   r�   r�   r�   r�   r�   r�   r  r!   r�   r�   ZemoncmspathZapikeyZnodeid0r�   r�   r�   r�   r�   Z
serverPortr�   Znoder   r�   r  rR   �joinZlogPathr�   �abspath�argvZ
installDirrh   r?   r�   r�   r�   r�   r�   r�   rZ   r[   r<   r\   ZnewConfigDatar   r(   rB   rA   ZverboseDebugr�   ZappZapiZadd_resourceZSerialr�   r  ZbaudrateZ	EIGHTBITSZbytesizeZPARITY_NONEZparityZSTOPBITS_ONEZstopbitsrz   ZxonxoffZrtsctsZdsrdtrZwriteTimeoutrq   rk   �O_RDWR�
O_NONBLOCKr�   r�   r|   r�   �runr   r   r   r   �<module>+   s$   (A!
W n<# =,<

2