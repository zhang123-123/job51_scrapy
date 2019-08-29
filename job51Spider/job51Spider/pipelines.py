# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Job51SpiderPipeline(object):
    def process_item(self, item, spider):
        return item


import sqlite3


class SqlitePipeline(object):
    def __init__(self, db_name):
        if not db_name:
            db_name = "db.sqlite"
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

    def close_spider(self):
        # 关闭爬虫和数据库
        self.cur.close()
        self.con.close()
        self.cur = None
        self.con = None
        print("数据库关闭")

    # 加载配置文件
    # 获取setting中的DB_NAME的值当做数据库的名字
    @classmethod
    def from_settings(cls, settings):
        db_name = settings["DB_NAME"]
        return cls(db_name)

    def sql(self, item):
        key_info = ""
        keys = []
        values = []
        # value_type = ""
        for key, value in item.items():
            if key != "job_type_":
                if isinstance(value, str):
                    value_type = "varchar(255)"
                elif isinstance(value, int):
                    value_type = "integer"
                elif isinstance(value, float):
                    value_type = "float"
                else:
                    value_type = "varchar(255)"
                key_info += f"{key} {value_type},"
                keys.append(key)
                values.append(value)
        return key_info[:-1], keys, values

    def process_item(self, item, spider):
        key_info = ""
        keys = []
        values = []
        for key, value in item.items():
            if isinstance(value, str):
                value_type = "varchar(255)"
            elif isinstance(value, int):
                value_type = "integer"
            elif isinstance(value, float):
                value_type = "float"
            else:
                value_type = "varchar(255)"
            key_info += f"{key} {value_type},"
            keys.append(key)
            values.append(value)
        key_info = key_info[:-1]
        sql1 = f"""
                    create table if not exists {spider.name}(
                        id integer primary key autoincrement,
                        {key_info}
                    )
                """
        print(sql1)
        self.cur.execute(sql1)
        sql2 = f"""
                    insert into {spider.name}({",".join(keys)}) values ({("?,"* len(keys))[:-1]})
                """
        print(sql2)
        self.cur.execute(sql2, values)
        self.con.commit()
        # elif item["job_type_"] == 2:
        #     key_info, keys, values = self.sql(item)
        #     sql1 = f"""
        #         create table if not exists jobdetail(
        #             id integer primary key autoincrement,
        #             {key_info}
        #         )
        #     """
        #     print(sql1)
        #     self.cur.execute(sql1)
        #     sql2 = f"""
        #                             insert into jobdetail({",".join(keys)}) values ({("?," * len(keys))[:-1]})
        #                         """
        #     print(sql2)
        #     self.cur.execute(sql2, values)
        #     self.con.commit()

        return item

