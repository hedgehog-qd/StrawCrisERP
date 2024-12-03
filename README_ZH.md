# StrawCrisERP - 适用于小规模的简单元件库存管理

这是一个基于Python **Quart** 框架构建的电子元件库存管理系统，使用了 **AdminLTE** 前端模板和 **HTML5 QR Code** 库实现扫码功能。

系统可以方便地进行库存管理，支持扫码录入（目前只支持立创商城和Digikey标签），筛选库存元件，修改信息，逐个取出以及BOM表对比。

**注意:** 目前本项目仅设计为局域网使用，如需在公网环境部署请***务必***增加***登录密码加密***，并进行必要的安全检查

## 功能特点

- **库存管理**：支持扫码/上传文件批量增加，修改信息，库存元件筛选，对比BOM表等
- **扫码功能**：通过扫描二维码轻松添加/更新/取出
- **轻量**：仅需Python和MySQL就可以部署使用

## 安装与使用

### 环境要求

- Python 3.7+
- pip
- MySQL

### 安装依赖

1. 克隆仓库：
  ```bash
  git clone https://github.com/hedgehog-qd/StrawCrisERP.git
  cd StrawCrisERP
  ```
2. 安装必要包：
  ```bash
  pip install -r requirements.txt
  ```
3. 创建并导入MySQL：
  ```mysql
  CREATE DATABASE strawcriserp;
  USE strawcriserp;
  SOURCE /您strawcriserp.sql的路径/strawcriserp.sql;
  ```
4. 修改配置文件config.py
  ```python
  # Port Config

  port = 5000                  # 您希望网站运行的端口号
  # Mysql Config
  db_host = "localhost"        # MySQL主机
  db_port = 3306               # MySQL端口
  db_user = "strawcris"        # MySQL用户名
  db_passwd = "password"      # 该用户的密码
  db_name = "strawcriserp"     # 数据库名
  ```
5. 启动
  ```bash
  python main.py
  ```
6. 如果您希望在后台运行，可以尝试使用screen或者nohup
## 功能介绍
### 搜索
在搜索页面中，您可以使用添加标签的方式来进行搜索。每个标签就是您的关键词，您可以任意新增或者删除  
![搜索](/images/search.png)
![使用标签](/images/search_tag.png)
### 查看所有条目
在此页面中，您可以查看目前所有的库存信息  
![查看所有](/images/viewall.png)
### 新增项目
当您购买元件时，您可以在此页面中单个添加新元件，或者直接上传您批量购买的表格，我们的后端会帮您自动完成规整。  
![新增页面](/images/addnew.png)
![新增上传](/images/addnew_uploadfile.png)
- 若您选择批量上传，请确保您的表格列名符合要求。您可以点击*Download the Example*来获取样例模板  
若您选择单个添加，则可尝试使用QR Scanner。此工具会帮助您自动填写MPN，数量，SPN，供应商等必要信息。  
![单个扫码](/images/addnew_scanQR.png)
### 编辑现有项目
在您盘点库存时，可以在此页面中编辑已有元件的数据，例如制造商，购买时间，或是修正数量信息等等。请注意，您必须先填写MPN（也可扫码自动填写），后端查询确有此库存后才能修改  
![修改页面](/images/edit.png)
### 取出
当您完成设计或是开始制作时，可以在此页面中进行取出操作。您可以直接上传由您EDA软件导出的BOM表（可能需要修改两处列名，根据系统弹窗提示即可），  
系统将会帮助您对比哪些物料您有库存，哪些没有或者数量不够，之后您可以选择从库存中扣除BOM表中元件对应的库存。  
当然，您也可以单个取出物料。填入MPN（或扫码）和所需数量，点击提交即可。  
![取出页面](/images/checkout.png)
## 后记
欢迎尝试！如果有什么问题烦请提交issues，与我们共同改进这个项目。谢谢您！
