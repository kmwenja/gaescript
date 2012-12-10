import os,sys,argparse

main_py="""# main.py

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from urls import urlconf

def main():
    myapp=webapp.WSGIApplication(urlconf,debug=True)
    util.run_wsgi_app(myapp)

if __name__=="__main__":
    main()"""

app_yaml="""application: %s
version: %s
runtime: python27
api_version: 1
threadsafe: false

handlers:
  - url: /assets
    static_dir: assets

  - url: .*
    script: main.py"""

urls_py="""# urls.py

urlconf=[
    # ('url here','handler here'),
]"""

"""def load_template(name):
  template=""
	f=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"templates",name))
	template=f.read()
	f.close()
	return template"""

def create_file(filename,content):
	f=open(filename,"w")
	f.write(content)
	f.close()
	
def create_project(project_name,version_no=1,with_version=False):
	# create project folder
	print 'creating project folder....'
	project_folder=project_name
	if with_version:
		project_folder=project_folder+"_"+repr(version_no)
	
	if not os.path.isdir(project_folder):
		os.mkdir(project_folder)
	
	os.chdir(project_folder)
	print 'done'
	
	print ''
	
	# create folders
	print 'adding folders....'
	folder_list=['models','templates','views','tests','assets',os.path.join('assets','js'),os.path.join('assets','imgs'),os.path.join('assets','css'),'lib','vendor']
	for folder in folder_list:
		print 'adding folder: %s' % folder
		os.mkdir(folder)
	print 'done'
	
	print ''
	
	# create project files
	print 'adding files....'
	file_list=[]
	file_list.append(("main.py",main_py))
	file_list.append(("app.yaml",app_yaml % (project_name,version_no)))
	file_list.append(("urls.py",urls_py))
	file_list.append((os.path.join("views","__init__.py"),""))
	file_list.append((os.path.join("models","__init__.py"),""))
	
	for file in file_list:
		print 'adding file: %s' % file[0]
		create_file(file[0],file[1])
	print 'done'
	
	print ''
	
	# finished
	print 'finished creating project: %s' % project_name

def main():
	parser=argparse.ArgumentParser(description='gae project setup and scaffolding script')
	
	subparsers= parser.add_subparsers(help='commands')
	
	# start project command
	
	start_project_parser = subparsers.add_parser('startproject',help='creates and initializes project files and folders')
	start_project_parser.add_argument('projectname',action='store',help='new project')
	start_project_parser.add_argument('--version-no','-n',default=1,action='store',type=int,help='version no of the project')
	start_project_parser.add_argument('--with-version','-w',default=False,action='store_true',help='add the version no to the project folder name')
	
	args = parser.parse_args()
	
	if args.projectname:
		create_project(args.projectname,args.version_no,args.with_version)
	
if __name__=="__main__":
	main()