from webdav3.client import Client
import os,time,requests

def list_files(webdav_url, username, password):
	# 创建WebDAV客户端
	options = {
		'webdav_hostname': webdav_url,
		'webdav_login': username,
		'webdav_password': password
	}
	

	client = Client(options)
	mulu=[]
	wenjian=[]
	q=1
	while q<15:
		try:		   
		   # 获取WebDAV服务器上的文件列表
			files = client.list()
		except:
			q+=1
			print('连接失败，1秒后重试...')
			time.sleep(1)
		else:
			if q>1:
				print('重连成功...')
			break

	for file in files[1:]:
		if file[-1]=='/':
			mulu.append(file)
		else:
			wenjian.append(file)
	return mulu,wenjian
	#print(files)
	# 生成本地txt文件路径
	#local_file_path = 'file_list.txt'
	
	# with open(local_file_path, 'w') as file:
		# # 写入文件名和链接到txt文件，并输出
		# for file_info in files:
			# file_name = file_info['path'].split('/')[-1]
			# file_link = webdav_url + file_info['path']
			
			# file.write(f"{file_name}: {file_link}")
			# print(f"{file_name}: {file_link}")
	
	# print(f"文件列表已保存到 {local_file_path}")

# 输入WebDAV地址、用户名和密码
webdav_url = 'http://tevin.dynv6.net:5244/dav/guest/阿里云盘alist/电影/'
save_mulu='Z:/OpenWrt/mnt/mmcblk2p4/TV/电影/'
username = 'admin'
password = 'admin'

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
			try:
				os.makedirs(os.path.dirname(save_mulu+b.replace(webdav_url,'')[:-3]+'strm'),exist_ok=True)
				with open(save_mulu+b.replace(webdav_url,'')[:-3]+'strm',"w",encoding='utf-8') as f:
					f.write(b.replace('tevin.dynv6.net:5244/dav','192.168.0.222:5244/d'))
			except:
				try:
					os.makedirs(os.path.dirname(save_mulu+b.replace(webdav_url,'').replace('：','.')[:-3]+'strm'),exist_ok=True)
					with open(save_mulu+b.replace(webdav_url,'').replace('：','.')[:-3]+'strm',"w",encoding='utf-8') as f:
						f.write(b.replace('tevin.dynv6.net:5244/dav','192.168.0.222:5244/d'))
				except:
					print(b.replace(webdav_url,'')+'处理失败，文件名包含特殊符号，建议重命名！')
	elif b[-3:].upper() in ['ASS','SRT','SSA']:
		if not os.path.exists(save_mulu+b.replace(webdav_url,'') ):
			p=1
			while p<10:
				try:
					print('正在下载：'+save_mulu+b.replace(webdav_url,''))
					r=requests.get(b.replace('/dav','/d'))
					os.makedirs(os.path.dirname(save_mulu+b.replace(webdav_url,'')),exist_ok=True)
					with open (save_mulu+b.replace(webdav_url,''),'wb')as f:
						f.write(r.content)
						f.close
					#wget.download(b.replace('/dav','/d'),save_mulu+b.replace(webdav_url,''))
				except:
					p+=1
					print('下载失败，1秒后重试...')
					time.sleep(1)
				else:
					if p>1:
						print('重新下载成功！')
					break
				
print('处理完毕！')
input('按任意键退出...')
