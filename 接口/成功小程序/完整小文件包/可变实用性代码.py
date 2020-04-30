class sql():
    # 传入的参数params分别为查询体和查询表
    def select_sql(self, conn_obj, *params):
        # 默认以数组存储，转为字符后，去掉(和’
        field = str(params[0][0])[2:-2]  # 查询字段
        view = str(params[0][1])[2:-2]  # 查询表
        condition = str(params[0][2])[2:-2]  # 查询条件
        # 定义数据库连接
        conn = conn_obj
        cursor = conn.cursor()
        if not condition:
            b = 'select %s from %s' % (field, view)
        else:
            b = 'select %s from %s where %s' % (field, view ,condition)
        print(b)
        cursor.execute(b)
        return cursor.fetchall()
        conn.close()
        # 传入的参数params分别为查询体和查询表
    def insert_sql(self, conn_obj, *params):
        # 默认以数组存储，转为字符后，去掉(和’
        field = str(params[0][0])[2:-2]  # 插入字段
        view = str(params[0][1])[2:-2]  # 插入表
        new_values = str(params[0][2])[2:-2]  # 插入数据
        # 定义数据库连接
        conn = conn_obj
        cursor = conn.cursor()
        b = 'insert into %s (%s)values (%s)' % (view, field, new_values)
        print(b)
        cursor.execute(b)
        conn.commit()
        conn.close()
    def delete_sql(self, conn_obj, *params):
        field = str(params[0][0])[2:-2]  # 删除字段
        view = str(params[0][1])[2:-2]  # 删除视图
        condition = str(params[0][2])[2:-2]  # 删除的数据
        # 定义数据库连接
        conn = conn_obj
        cursor = conn.cursor()
        if not condition:
            res = input('是否要删除表(Y/N)：%s') % view
            if res == 'Y':
                b = 'delete from %s' % (view)
            else:
                print('请增加限制条件')
                exit()
        else:
            b = 'delete from %s where %s' % (view, condition)
        print(b)
        cursor.execute(b)
        conn.commit()
        conn.close()