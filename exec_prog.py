from Password_creator import *
from flask import Flask,render_template,request,redirect,url_for,send_file
from table import Table
from flask_modus import Modus
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
from global_data import GlobalData
import os
import zipfile
import mysql.connector as sqltor
import datetime

app = Flask(__name__,template_folder='template')
modus= Modus(app)
mydb =sqltor.connect(host="ZCDS4327.mysql.pythonanywhere-services.com",user="ZCDS4327",password="hello123",database="ZCDS4327$password_site")


@app.route("/")
def data_input(): # for user input for suggestions
    return render_template('input.html')

@app.route('/data-extract') # for extracting the user input
def data_extract():
    global sug
    sug = int(request.args.get('sug')) # to get the user input
    return redirect('/generate/new') # redirecting to generate
@app.route('/generate/new') # for generating the passwords
def generate():
    global final_g
    global data_x
    final_g = [] # for the passwords
    passwd_obj = ""
    del (GlobalData.password)[:]

    for i in range(sug):
     v =  password_generator("","","") #for calling the class
     alpha_g = v.alpha_rand_func()    # line 25- 30; please refer the Password_creator.py file
     sym_g = v.symbol_rand_func()
     int_g = v.int_rand_func()
     spec_g = v.special_number_production()
     final = v.final_output
     final_g.append(v.final_output)
     passwd_obj = Table(v.final_output,'nil') # for storing them in a class
     (GlobalData.password).append(passwd_obj) # for storing them in a list
    passwd_obj.count_init()

    return redirect('/generate/show-output')


@app.route('/generate/show-output',methods  = ["GET","POST"])
def show_output():
  return render_template('output_disp.html',final_lst = GlobalData.password) # rendering the output_disp.html

@app.route('/generate/<int:id>',methods = ["GET","PATCH","POST","DELETE"]) # for modifying the function
def show(id):
   found  =  next(entry for entry in GlobalData.password if entry.id == id) # for finding the entry with the required id
   if request.method  == b"PATCH": # for dealing with PATCH
        found.passwd = request.form['edit_passwd']
        found.desc = request.form['description']
        return redirect('/generate/show-output')
   if request.method == b"DELETE":  # for deleting a password suggestion
        index = found.id
        for i in range( (GlobalData.password).index(found),(len(GlobalData.password)) ): #iterating from the found password
                 (GlobalData.password[i]).id -= 1 #decreasing each password's id by 1
        (GlobalData.password).remove(found) #removing the required passwords

        return redirect('/generate/show-output') #redirecting to /generate/show-output
   return render_template('modify.html',found_entry = found)

@app.route('/generate/add-passwd-input')
def add_passwd_inp():
  return render_template('add.html')

@app.route('/generate/add-passwd-sug')
def add_passwd_sug():
  global add_sug
  add_sug = int(request.args.get('add-sug'))
  return redirect('/generate/add-passwd-create')

@app.route('/generate/add-passwd-create')
def add_passwd_func():
  new_passwd_obj = ""
  for i in range(add_sug):
       v = password_generator("","","")
       alpha_g = v.alpha_rand_func()    # line 25- 30; please refer the Password_creator.py file
       sym_g = v.symbol_rand_func()
       int_g = v.int_rand_func()
       spec_g = v.special_number_production()
       final = v.final_output
       new_passwd_obj = Table(final,"nil")
       new_passwd_obj.id = len(GlobalData.password) + 1
       (GlobalData.password).append(new_passwd_obj)
  new_passwd_obj.count_init()
  return redirect('/generate/show-output')


@app.route('/generate/file-manip-disp') # for displaying the uploading and downloading functions for password
def disp_manip_menu():
  return render_template('file-manip.html')

@app.route('/generate/file-manip',methods = ["GET","POST"]) # for saving the password(s)
def save_file():
  pass_output_lst = [] #for passwords
  desc_output_lst = [] #for descriptions of the password
  encrypted_pass_output_lst = [] #storing passwords after encryption
  encrypted_desc_output_lst = [] #storing descriptions of passwords after encryption
  UPLOAD_FOLDER = os.getcwd()
  app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
  if request.method == "POST": # checking if the request method is POST
      pass_file = request.files['passfile'] #requesting the name of the password saving file
      pass_file_Name = secure_filename(pass_file.filename) #storing the name of the password saving file
      desc_file = request.files['descfile'] #for the file storing descriptions of the file
      desc_file_Name =secure_filename(desc_file.filename)
      key = Fernet.generate_key() # generating a key
      key_init = Fernet(key)  # storing the key for encrypting purpose
      key_file = request.files['keyfile']  # requesting the key saving file
      key_file_name = secure_filename(key_file.filename) #storing the name of the key saving file
      file_lst = [pass_file_Name,desc_file_Name,key_file_name]

      for i in GlobalData.password:
       encrypted_pass_output_lst.append(key_init.encrypt(bytes(i.passwd,encoding="utf-8")))
       encrypted_desc_output_lst.append(key_init.encrypt(bytes(i.desc,encoding="utf-8")))
      with open(pass_file_Name,"wb+") as k:

       for i in encrypted_pass_output_lst:
         k.write(i)
         k.write(b'\n')

      with open(desc_file_Name,"wb+") as k:

       for i in encrypted_desc_output_lst:
         k.write(i)
         k.write(b'\n')
      with open(key_file_name,"wb+") as k:
        k.write(key)


  if GlobalData.password == []: # for showing the error when no password is created
    return render_template('semantic-error.html',message = "Illegal method. Can't save the file when no password is generated")
  else: #[pass_file_Name,desc_file_Name,key_file_name]

        zip_obj = zipfile.ZipFile('/home/ZCDS4327/proj/cs_proj_pro_1/zipfile.zip','w')

        #SQL Execution
        getDate = datetime.datetime.now()
        cursor = mydb.cursor()
        n_passwd = len(GlobalData.password)
        insert_query = "INSERT INTO password_table VALUES(%s,%s)"
        query_val = (n_passwd,getDate)
        cursor.execute(insert_query,query_val)
        mydb.commit()


        for i in file_lst:
            zip_obj.write(i,compress_type =zipfile.ZIP_DEFLATED)
        zip_obj.close()
        zip_obj_name = zip_obj.filename
        for i in file_lst:
            os.remove(i)
        del file_lst
        return send_file(zip_obj_name),os.remove('/home/ZCDS4327/proj/cs_proj_pro_1/zipfile.zip')
@app.route('/generate/file-manip-upload',methods = ["GET","POST"])
def upload_file(): #for uploading the file
  UPLOAD_FOLDER = os.getcwd()
  decrypted_pass_output_lst = []
  decrypted_desc_output_lst = []
  decrypted_password = []
  decrypted_data = ""
  Upload_key = "" #for storing the key
  app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
  if request.method == "POST":
    Uploadpassfile= request.files['Uploadpassfile'] #requesting the name of the required file
    Uploadpassfile_name = secure_filename(Uploadpassfile.filename) #storing the name of the password saving file
    Uploadkeyfile = request.files['Uploadkeyfile'] #requesting the name of the key storing file
    Uploadkeyfile_name = secure_filename(Uploadkeyfile.filename) #storing the name of the key storing file
    descfileUpload = request.files['descfileUpload'] #requesting the name of the file storing descriptions
    descfileUpload_name = secure_filename(descfileUpload.filename) #storing the name of the file string descriptions
  #print(Uploadkeyfile_name,Uploadpassfile_name,descfileUpload_name)
    Uploadpassfile.save(os.path.join(app.config['UPLOAD_FOLDER'],Uploadpassfile_name))
    Uploadkeyfile.save(os.path.join(app.config['UPLOAD_FOLDER'],Uploadkeyfile_name))
    descfileUpload.save(os.path.join(app.config['UPLOAD_FOLDER'],descfileUpload_name))



    with open(Uploadkeyfile_name,"rb") as k: # reading the containing the key
      Upload_key = k.read()
    key_init_sec = Fernet(Upload_key)

    with open(Uploadpassfile_name,"rb") as k: # reading the file containing the passwords by decrypting them
       for i in k:
         decrypted_pass_output_lst.append(str(key_init_sec.decrypt(i),encoding="utf-8"))

    with open(descfileUpload_name,"rb") as k: #reading the file containing the descriptions by decrypting them
        for i in k:
          decrypted_desc_output_lst.append(str(key_init_sec.decrypt(i),encoding="utf-8"))

  x = len(decrypted_pass_output_lst)
  (GlobalData.password).clear() #clearing the GlobalData.password list to avoid piling up of data
  for s in range(x): #for inserting the decrypted data inside the GlobalData.password list for display
        data_decrypted = Table(decrypted_pass_output_lst[s],decrypted_desc_output_lst[s])
        (GlobalData.password).append(data_decrypted)
  os.remove(os.path.join(app.config['UPLOAD_FOLDER'],Uploadpassfile_name))
  os.remove(os.path.join(app.config['UPLOAD_FOLDER'],Uploadkeyfile_name))
  os.remove(os.path.join(app.config['UPLOAD_FOLDER'],descfileUpload_name))

  return redirect('/generate/show-output') #redirecting to /generate/show-output

