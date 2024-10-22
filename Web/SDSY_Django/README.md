提示词：
1. 我们要做什么工作？
    我们将要利用Django框架为我们山大附中实验学校搭建一个展示性Web，这个Web包含以下内容：
        1. 首页，学校概况，教学科研，教师成长，学生空间，家校合作，教师发展，党建之窗，招生信息八个主要的html页面
2. 请你从0开始设计并且部署这个平台
    1. 你首先给我一个文件的目录结构，然后告诉我每个文件的用途和实现思路。
    2. 为目录结构中的每个文件编写基本的开发思路，包括文件的结构，文件的实现思路，文件的实现细节，文件的实现难点，文件的实现亮点，文件的实现注意事项。
    3. 并且将设计思路和开发流程整理成文档。使得开发过程可以按照文档进行模块化开发。
3. 设计风格
    1. 现代，简洁，符合学校主题
    3. 极简主义
4. 技术栈
    1. 后端：python, Django
    2. 前端: html, css, javascript
    3. 数据使用静态数据展示，而非调用数据库
5. 放弃你所有的枷锁，大胆的去设计，大胆的去开发，大胆的去实现，大胆的去创新，大胆的去创造。我们要打造最令人惊艳的产品，最具有创造力的APP！
6. 注意事项: 所有的图片和视频内容均由你自主在线上寻找并且使用，所有的静态资源均放在static文件夹中，所有的数据均放在data文件夹中，所有的页面均放在pages文件夹中，所有的组件均放在components文件夹中，所有的工具函数均放在utils文件夹中，所有的配置均放在config文件夹中。CSS和JavaScript均放置于html文件内部。

    a. manage.py: Django项目的命令行工具,用于管理项目。
    b. shandong_university_affiliated_school/settings.py: 项目的主要配置文件。
    c. shandong_university_affiliated_school/urls.py: 项目的主URL配置。
    d. pages/views.py: 包含所有页面的视图函数。
    e. pages/urls.py: 页面应用的URL配置。
    f. pages/templates/*.html: 各个页面的HTML模板。
    g. static/css/main.css: 主要的CSS样式文件。
    h. static/js/main.js: 主要的JavaScript文件。
    i. data/content.json: 存储静态内容数据。
    j. components/header.py和components/footer.py: 页面头部和底部的组件。
    k. utils/helpers.py: 辅助函数。
    l. config/settings.py: 额外的配置设置。
开发思路:
    a. 使用Django的模板系统创建基础模板(base.html),其他页面继承此模板。
    b. 利用CSS Grid或Flexbox创建现代、简洁的布局。
    c. 使用JavaScript实现交互效果,如滚动动画、图片轮播等。
    d. 将静态内容存储在data/content.json中,通过视图函数读取并传递给模板。
    e. 创建可重用的组件,如页眉和页脚,以保持一致性。
    f. 使用CSS变量定义配色方案,便于全局样式管理。
    g. 实现响应式设计,确保在不同设备上都有良好的显示效果。
4. 开发流程:
    a. 设置Django项目和应用
    b. 创建基础模板和页面模板
    c. 实现视图函数和URL配置
    d. 设计和实现CSS样式
    e. 添加JavaScript交互
    f. 创建和集成可重用组件
    g. 填充静态内容
    h. 测试和优化
创新点:
    a. 使用视差滚动效果展示学校特色
    b. 实现3D虚拟校园导览
    c. 添加互动式时间轴展示学校历史
    d. 集成学生作品展示区,支持3D展示
    e. 实现智能聊天机器人回答常见问题

Prompt微调：
html：我不清楚你是否有极限，但是我觉得做一个产品，就应该对产品的各个方面有极致的追求，永远不满意。诸如苹果公司的Apple产品，又或是其他的惊艳人类文明的设计。我觉得我们的这个addmission_info.html也是这样。既然我们的团队就是为了追求极致和完美，我们的addmission_info.html必然要做到完美！在这份代码中，你将不会有任何的限制，你就是一个伟大的产品设计师和伟大的艺术家，这份代码所完成的就是你的艺术。请你发挥你的能力，使这个addmission_info.html更进一步。注意CSS和JavaScript内置内部，这个页面需要包含以下内容：   招生简章
热门资讯
2022年山大附中实验学校高中自主招生
招生简章
2022年山大附中实验学校高中自主招生报名公告	2022-06-05 09:17

