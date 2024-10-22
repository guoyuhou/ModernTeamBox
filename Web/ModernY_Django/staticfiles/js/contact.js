document.addEventListener('DOMContentLoaded', function() {
    // 初始化 AOS
    AOS.init({
        duration: 1000,
        once: true
    });

    // 标题动画
    const title = document.querySelector('.futuristic-title');
    const tagline = document.querySelector('.tagline');
    const letters = document.querySelectorAll('.futuristic-title .letter');

    if (title && tagline) {
        letters.forEach((letter, index) => {
            letter.style.opacity = '0';
            letter.style.transform = 'translateY(50px) rotate(45deg)';
            setTimeout(() => {
                gsap.to(letter, {
                    opacity: 1,
                    y: 0,
                    rotation: 0,
                    duration: 0.8,
                    ease: "back.out(1.7)"
                });
            }, 100 * index);
        });

        setTimeout(() => {
            gsap.to(tagline, {
                opacity: 1,
                y: 0,
                duration: 1,
                ease: "power3.out"
            });
        }, letters.length * 100 + 200);
    }

    // 表单动画
    const formInputs = document.querySelectorAll('.form-group input, .form-group textarea');
    formInputs.forEach(input => {
        input.addEventListener('focus', () => {
            gsap.to(input, {
                scale: 1.05,
                duration: 0.3,
                ease: "power2.out"
            });
        });

        input.addEventListener('blur', () => {
            gsap.to(input, {
                scale: 1,
                duration: 0.3,
                ease: "power2.out"
            });
        });
    });

    // 社交图标动画
    const socialIcons = document.querySelectorAll('.social-icon');
    socialIcons.forEach(icon => {
        icon.addEventListener('mouseenter', () => {
            gsap.to(icon, {
                y: -5,
                scale: 1.2,
                duration: 0.3,
                ease: "power2.out"
            });
        });

        icon.addEventListener('mouseleave', () => {
            gsap.to(icon, {
                y: 0,
                scale: 1,
                duration: 0.3,
                ease: "power2.out"
            });
        });
    });

    // 互动项目动画
    const interactiveItems = document.querySelectorAll('.interactive-item');
    interactiveItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            gsap.to(item.querySelector('.hologram-effect'), {
                scale: 1.1,
                duration: 0.3,
                ease: "power2.out"
            });
        });

        item.addEventListener('mouseleave', () => {
            gsap.to(item.querySelector('.hologram-effect'), {
                scale: 1,
                duration: 0.3,
                ease: "power2.out"
            });
        });
    });

    // 平滑滚动
    document.querySelectorAll('a.scroll-to').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // 表单提交处理
    const contactForm = document.getElementById('contact-form');
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        // 这里添加表单提交逻辑
        alert('感谢您的留言，我们会尽快回复您！');
        contactForm.reset();
    });
});