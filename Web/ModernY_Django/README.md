# ModernY 公司网站

这是ModernY公司的官方网站项目，基于Django框架开发。

## 功能特点

- 响应式设计，适配各种设备
- 公司信息展示
- 产品和服务介绍
- 博客系统
- 联系表单

## 安装和运行

1. 克隆仓库：
   ```bash
   git clone https://github.com/moderny/website.git
   cd website
   ```

2. 创建虚拟环境并激活：
   ```bash
   python -m venv venv
   source venv/bin/activate  # 在Windows上使用 venv\Scripts\activate
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 运行数据库迁移：
   ```bash
   python manage.py migrate
   ```

5. 创建超级用户：
   ```bash
   python manage.py createsuperuser
   ```

6. 运行开发服务器：
   ```bash
   python manage.py runserver
   ```

访问 http://localhost:8000 查看网站。

## 贡献

欢迎提交Pull Request或创建Issue。

## 许可证

本项目采用MIT许可证。详情请见 [LICENSE](LICENSE) 文件。


使用SQLlite数据库