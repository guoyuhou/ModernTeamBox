document.addEventListener('DOMContentLoaded', () => {
    // 平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // 导航栏滚动效果
    const header = document.querySelector('header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // 动画效果
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
            }
        });
    });

    animatedElements.forEach(el => observer.observe(el));

    // 表单验证
    const contactForm = document.querySelector('#contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            if (validateForm()) {
                // 这里可以添加AJAX提交表单的代码
                alert('表单提交成功！');
                contactForm.reset();
            }
        });
    }
});

function validateForm() {
    // 简单的表单验证逻辑
    const name = document.querySelector('#name').value;
    const email = document.querySelector('#email').value;
    const message = document.querySelector('#message').value;

    if (!name || !email || !message) {
        alert('请填写所有必填字段');
        return false;
    }

    if (!isValidEmail(email)) {
        alert('请输入有效的电子邮件地址');
        return false;
    }

    return true;
}

function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

particlesJS.load('particles-js', '/static/particles.json', function() {
    console.log('particles.js loaded - callback');
});

window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const bgVideo = document.querySelector('#bg-video');
    bgVideo.style.transform = `translate3d(-50%, -${scrolled * 0.5}px, 0)`;
});