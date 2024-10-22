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
            letter.style.transform = 'translateY(50px)';
            setTimeout(() => {
                letter.style.opacity = '1';
                letter.style.transform = 'translateY(0)';
            }, 100 * index);
        });

        setTimeout(() => {
            tagline.style.opacity = '1';
            tagline.style.transform = 'translateY(0)';
        }, letters.length * 100 + 200);
    }

    // 产品卡片动画
    gsap.utils.toArray('.product-card').forEach((card, index) => {
        gsap.from(card, {
            opacity: 0,
            y: 50,
            rotation: 5,
            scale: 0.9,
            duration: 0.8,
            delay: 0.2 * index,
            ease: "back.out(1.7)",
            scrollTrigger: {
                trigger: card,
                start: "top 80%",
                end: "bottom 20%",
                toggleActions: "play none none reverse"
            }
        });
    });

    // 特性列表动画
    gsap.utils.toArray('.feature-list li').forEach((item, index) => {
        gsap.from(item, {
            opacity: 0,
            x: -50,
            duration: 0.5,
            delay: 0.1 * index,
            scrollTrigger: {
                trigger: item,
                start: "top 80%",
                end: "bottom 20%",
                toggleActions: "play none none reverse"
            }
        });
    });

    // 技术栈动画
    gsap.utils.toArray('.tech-item').forEach((item, index) => {
        gsap.from(item, {
            opacity: 0,
            scale: 0,
            duration: 0.5,
            delay: 0.05 * index,
            ease: "back.out(1.7)",
            scrollTrigger: {
                trigger: item,
                start: "top 90%",
                end: "bottom 20%",
                toggleActions: "play none none reverse"
            }
        });
    });

    // 平滑滚动到产品详情
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});