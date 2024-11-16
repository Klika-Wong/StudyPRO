import mysql.connector

def fetch_records(user_id):
    """
    从指定数据库的表中查询符合 user_id 的所有唯一数据。

    参数:
    - user_id (str): 要查找的用户ID
    - database (str): 数据库名
    - table_name (str): 表名

    返回:
    - 查询结果的列表，去除重复记录
    """
    # 连接到数据库
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        port="3306",
        database="questionbank"
    )

    # 创建游标对象
    cursor = connection.cursor()

    # 使用 DISTINCT 去重
    query = f"SELECT DISTINCT * FROM questions WHERE user_id='{user_id}'"
    
    # 执行查询
    cursor.execute(query)
    
    # 获取查询结果
    raw_results = cursor.fetchall()

    # 关闭游标和连接
    cursor.close()
    connection.close()
    
    # 使用 set 去除重复行
    unique_results = list(set(raw_results))
    
    return unique_results  # 返回去重后的结果




