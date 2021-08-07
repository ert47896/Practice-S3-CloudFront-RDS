from flask import Flask, render_template, request, redirect
import os, boto3
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from random import randint
from datetime import datetime
from module.rdsMysql import connection_pool
from route.message import messageApi
load_dotenv

app = Flask(__name__, static_folder="public", static_url_path="/")

app.config["JSON_AS_ASCII"] = False         #避免中文顯示為ASII編碼
app.config["TEMPLATES_AUTO_RELOAD"] = True  #True當flask偵測到template有修改會自動更新
app.config["MAX_CONTENT_LENGTH"] = 16 * 1000 * 1000     #接受的上傳檔案單檔上限約16MB

#Api
app.register_blueprint(messageApi, url_prefix="/api")

#連接s3
s3 = boto3.client(
    "s3",
    aws_access_key_id = os.getenv("S3_KEY"),
    aws_secret_access_key = os.getenv("S3_SECRET")
)
def uploadFileTos3(file, bucketName, fileType):
    try:
        s3.upload_fileobj(
            Fileobj = file,
            Bucket = bucketName,
            Key = file.filename,
            ExtraArgs = {
                "ContentType": fileType
            }
        )
    except Exception as e:
        # Catch all exception
        print ("Something Happened: ", e)
        return e
    return "Upload success!"

#檢查傳入檔案類型
ALLOWED_EXTENSTIONS = {"png", "jpg", "jpeg", "gif"}
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSTIONS

@app.route("/", methods=["GET", "POST"])
def index():
    # 提交form表單資料
    if request.method == "POST":
        # Check if the post request has the file part(the name of the file input on form)
        if "uploadfile" not in request.files:
            return "No uploadfile key in request.files."
        # form確實有uploadfile key用變數file儲存內容
        file = request.files["uploadfile"]
        # 使用者沒選擇檔案，瀏覽器送了空的檔案過來
        if file.filename == "":
            return "Please select a file."
        if file and allowed_file(file.filename):
            file.filename = secure_filename(file.filename)
            # 若檔名非ASCII格式，產生隨機亂碼當檔名
            if "." not in file.filename:
                file.filename = datetime.strftime(datetime.today(), "%Y%m%d")+"".join([str(randint(0,9)) for num in range(8)]) + "." + file.filename
            output = uploadFileTos3(file, os.getenv("S3_BUCKET"), file.content_type)
            # 檔案上傳S3成功，將文字跟檔案路徑放到RDS
            if output == "Upload success!":
                fileUrl = os.getenv("CLOUDFRONT_URL") + file.filename
                text = request.form["uploadtext"]
                try:
                    sql = "INSERT INTO message (message, file_url) VALUES (%s, %s)"
                    value = (text, fileUrl)
                    connection_object = connection_pool.get_connection()
                    with connection_object.cursor() as cursor:
                        cursor.execute(sql, value)
                        connection_object.commit()
                    connection_object.close()
                    return redirect("/")
                except:
                    return {"error":True, "message":"伺服器內部錯誤！"}
    # 瀏覽首頁
    elif request.method == "GET":
        return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)