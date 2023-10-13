import os,time,requests,datetime
#from getpass import getpass
from xml.etree import ElementTree as ET
from urllib.request import quote, unquote

def list_files(webdav_url, username, password):
	# 构建 WebDAV URL
	if not webdav_url.endswith("/"):
		webdav_url += "/"

	# 发送 PROPFIND 请求
	headers = {"Depth": "1"}
	response = requests.request("PROPFIND", webdav_url, auth=(username, password), headers=headers)

	# 解析 XML 响应
	xml_data = response.content
	namespaces = {"d": "DAV:"}
	xml_tree = ET.fromstring(xml_data)
	#print(xml_tree)
	# 提取文件和目录信息
	wenjian = []
	mulu = []
	for response in xml_tree.findall(".//d:response", namespaces=namespaces)[1:]:
		href = response.find("d:href", namespaces=namespaces).text
		#print(href)
		#display_name = response.find("d:propstat/d:prop/d:displayname", namespaces=namespaces).text
		#print(display_name)
		if href.endswith("/"):
			h_1=unquote(href.split('/')[-2]+'/', encoding='utf-8')
			mulu.append(h_1)
		else:
			wenjian.append(unquote(href.split('/')[-1], encoding='utf-8'))
	return mulu,wenjian




now = datetime.datetime.now().strftime('%Y-%m-%d  %H-%M-%S')
# 输入WebDAV地址、用户名和密码
#webdav_url = 'http://tevin.dynv6.net:5244/dav/guest/阿里云盘alist/剧集/'


webdav_url='http://192.168.0.222:5244/dav/guest/阿里云盘alist/剧集/'
save_mulu='/mnt/mmcblk2p4/TV/剧集/'

	
#webdav_url = 'http://192.168.0.222:5244/dav/guest/阿里云盘alist/剧集/'
#save_mulu='Z:/OpenWrt/mnt/mmcblk2p4/TV/剧集/'
#save_mulu='/mnt/mmcblk2p4/TV/剧集/'
username = 'admin'
password = 'admin'
print('开始处理...')
with open('log/'+now+'.txt', 'a',encoding='utf-8') as file_object:
	file_object.write('开始处理...\n')
a=list_files(webdav_url, username, password)[0]
b=list_files(webdav_url, username, password)[1]

# 调用函数获取文件列表并保存到本地
#r1,r2=list_files(webdav_url, username, password)
l_0=list_files(webdav_url, username, password)[0]
l_1=list_files(webdav_url, username, password)[1]

url_1=[webdav_url]
url_2=[]
url_3=[]
wenjian_1=[webdav_url + str(k) for k in l_1]
wenjian_2=[]
wenjian_3=[]
if l_0 !=[]:
	for u in l_0:
		url_2.append(webdav_url+u)
		wenjian_2+=[webdav_url+u+str(i) for i in list_files(webdav_url+u, username, password)[1]]
	for x in url_2:
		l_x=list_files(x, username, password)[0]
		if l_x !=[]:
			for y in l_x:
				url_3.append(x+y)
				wenjian_3+=[x+y+str(j) for j in list_files(x+y, username, password)[1]]
url=url_1+url_2+url_3
wenjian_all=wenjian_1+wenjian_2+wenjian_3
#print(url)
# for a in url:
	# os.makedirs(os.path.dirname(a.replace(webdav_url,'')),exist_ok=True)

for b in wenjian_all:
	if b[-3:].upper() in ['MP4','MKV','FLV','AVI']:
		if not os.path.exists(save_mulu+b.replace(webdav_url,'')[:-3]+'strm' ):
			print('正在处理：'+b.replace(webdav_url,''))
			with open('log/'+now+'.txt', 'a',encoding='utf-8') as file_object:
				file_object.write('正在处理：'+b.replace(webdav_url,'')+'\n')
			try:
				os.makedirs(os.path.dirname(save_mulu+b.replace(webdav_url,'')[:-3]+'strm'),exist_ok=True)
				with open(save_mulu+b.replace(webdav_url,'')[:-3]+'strm',"w",encoding='utf-8') as f:
					#f.write(b.replace('tevin.dynv6.net:5244/dav','192.168.0.222:5244/d'))
					f.write(b.replace('/dav','/d'))
			except:
				try:
					os.makedirs(os.path.dirname(save_mulu+b.replace(webdav_url,'').replace('：','.')[:-3]+'strm'),exist_ok=True)
					with open(save_mulu+b.replace(webdav_url,'').replace('：','.')[:-3]+'strm',"w",encoding='utf-8') as f:
						#f.write(b.replace('tevin.dynv6.net:5244/dav','192.168.0.222:5244/d'))
						f.write(b.replace('/dav','/d'))
				except:
					print(b.replace(webdav_url,'')+'处理失败，文件名包含特殊符号，建议重命名！')
					with open('log/'+now+'.txt', 'a',encoding='utf-8') as file_object:
						file_object.write(b.replace(webdav_url,'')+'处理失败，文件名包含特殊符号，建议重命名！'+'\n')
	elif b[-3:].upper() in ['ASS','SRT','SSA']:
		if not os.path.exists(save_mulu+b.replace(webdav_url,'') ):
			p=1
			while p<10:
				try:
					print('正在下载：'+save_mulu+b.replace(webdav_url,''))
					with open('log/'+now+'.txt', 'a',encoding='utf-8') as file_object:
						file_object.write('正在下载：'+save_mulu+b.replace(webdav_url,'')+'\n')
					r=requests.get(b.replace('/dav','/d'))
					os.makedirs(os.path.dirname(save_mulu+b.replace(webdav_url,'')),exist_ok=True)
					with open (save_mulu+b.replace(webdav_url,''),'wb')as f:
						f.write(r.content)
						f.close
					#wget.download(b.replace('/dav','/d'),save_mulu+b.replace(webdav_url,''))
				except:
					p+=1
					print('下载失败，1秒后重试...')
					with open('log/'+now+'.txt', 'a',encoding='utf-8') as file_object:
						file_object.write('下载失败，1秒后重试...'+'\n')
					time.sleep(1)
				else:
					if p>1:
						print('重新下载成功！')
						with open('log/'+now+'.txt', 'a',encoding='utf-8') as file_object:
							file_object.write('重新下载成功！'+'\n')
					break
				
print('处理完毕！')
with open('log/'+now+'.txt', 'a',encoding='utf-8') as file_object:
	file_object.write('处理完毕！'+'\n')
input('按任意键退出...')
