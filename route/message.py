from flask import Blueprint, jsonify
from module.rdsMysql import connection_pool

messageApi = Blueprint("messageApi", __name__)

@messageApi.route("/message")
def messageData():
    responseSet = dict()
    responseSet["data"] = []
    try:
        connection_object = connection_pool.get_connection()
        with connection_object.cursor() as cursor:
            cursor.execute("SELECT message_id, message, file_url FROM message;")
            for row in cursor:
                eachMessage = {
                    "id": row[0],
                    "message": row[1],
                    "file_url": row[2]
                }
                responseSet["data"].insert(0, eachMessage)
        connection_object.close()
        return jsonify(responseSet), 200
    except:
        return jsonify(error=True, message="伺服器內部錯誤！"), 500