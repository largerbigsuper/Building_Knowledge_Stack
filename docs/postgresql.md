## postgresql 相关

### postgresql 安装与启动

```
# 安装数据库
brew install postgresql

# 如果有之前版本需要执行迁移数据的命令
brew postgresql-upgrade-database

# 启动数据库
brew services start postgresql
```

### 数据库创建

```
# 创建数据库
createdb building_knowledge_stack_db

# 连接数据库
psql building_knowledge_stack_db

```

### 基本数据操作

1. 查看数据库信息

```shell

building_knowledge_stack_db=# SELECT version();
                                                     version
------------------------------------------------------------------------------------------------------------------
 PostgreSQL 11.3 on x86_64-apple-darwin17.7.0, compiled by Apple LLVM version 10.0.0 (clang-1000.11.45.5), 64-bit
(1 row)

building_knowledge_stack_db=#

```

2. 帮助和退出

```
# 帮助
\h

# 退出
\q
```

