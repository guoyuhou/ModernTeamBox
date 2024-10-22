document.addEventListener('DOMContentLoaded', function() {
    const title = document.querySelector('.futuristic-title');
    const tagline = document.querySelector('.tagline');
    const ctaContainer = document.querySelector('.cta-container');
    const letters = document.querySelectorAll('.futuristic-title .letter');
    const buttons = document.querySelectorAll('.cta-container .btn');

    if (title && tagline && ctaContainer) {
        // 重置初始状态
        letters.forEach(letter => {
            letter.style.opacity = '0';
            letter.style.transform = 'translateY(50px)';
        });
        tagline.style.opacity = '0';
        tagline.style.transform = 'translateY(20px)';
        buttons.forEach(button => {
            button.style.opacity = '0';
            button.style.transform = 'translateY(20px)';
        });

        // 文字动画
        letters.forEach((letter, index) => {
            setTimeout(() => {
                letter.style.opacity = '1';
                letter.style.transform = 'translateY(0)';
            }, 100 * index);
        });

        setTimeout(() => {
            tagline.style.opacity = '1';
            tagline.style.transform = 'translateY(0)';
        }, letters.length * 100 + 200);

        buttons.forEach((button, index) => {
            setTimeout(() => {
                button.style.opacity = '1';
                button.style.transform = 'translateY(0)';
            }, letters.length * 100 + 500 + 200 * index);
        });

        // 创新展示项目动画
        const innovationItems = document.querySelectorAll('.innovation-item');
        innovationItems.forEach((item, index) => {
            gsap.from(item, {
                opacity: 0,
                y: 50,
                duration: 0.8,
                delay: 0.2 * index,
                scrollTrigger: {
                    trigger: item,
                    start: "top 80%"
                }
            });
        });

        // 视差效果
        gsap.to('.parallax-bg', {
            yPercent: 30,
            ease: "none",
            scrollTrigger: {
                trigger: ".parallax-section",
                scrub: true
            }, 
        });

        // 服务卡片滑动效果
        const serviceSlider = document.querySelector('.services-slider');
        const serviceCards = document.querySelectorAll('.service-card');
        let activeServiceIndex = 0;

        function updateActiveService() {
            serviceCards.forEach((card, index) => {
                if (index === activeServiceIndex) {
                    card.classList.add('active');
                } else {
                    card.classList.remove('active');
                }
            });
            
            gsap.to(serviceSlider, {
                x: -activeServiceIndex * (300 + 30), // 卡片宽度 + 间距
                duration: 0.5,
                ease: "power2.out"
            });
        }

        setInterval(() => {
            activeServiceIndex = (activeServiceIndex + 1) % serviceCards.length;
            updateActiveService();
        }, 5000);

        updateActiveService();

        // 客户评价轮播
        const testimonialItems = document.querySelectorAll('.testimonial-item');
        const prevButton = document.querySelector('.carousel-control.prev');
        const nextButton = document.querySelector('.carousel-control.next');
        let currentTestimonial = 0;

        function showTestimonial(index) {
            testimonialItems[currentTestimonial].classList.remove('active');
            testimonialItems[index].classList.add('active');
            currentTestimonial = index;
        }

        function showNextTestimonial() {
            showTestimonial((currentTestimonial + 1) % testimonialItems.length);
        }

        function showPrevTestimonial() {
            showTestimonial((currentTestimonial - 1 + testimonialItems.length) % testimonialItems.length);
        }

        if (prevButton && nextButton) {
            prevButton.addEventListener('click', showPrevTestimonial);
            nextButton.addEventListener('click', showNextTestimonial);
        }

        setInterval(showNextTestimonial, 7000);

        // 添加滚动触发动画
        gsap.registerPlugin(ScrollTrigger);

        gsap.from('.services-showcase .section-title', {
            opacity: 0,
            y: 50,
            duration: 1,
            scrollTrigger: {
                trigger: '.services-showcase',
                start: 'top 80%'
            }
        });

        gsap.from('.testimonials .section-title', {
            opacity: 0,
            y: 50,
            duration: 1,
            scrollTrigger: {
                trigger: '.testimonials',
                start: 'top 80%'
            }
        });

        // 控制头部显示和隐藏
        const header = document.querySelector('.main-header');
        let lastScrollTop = 0;
        let scrollThreshold = 100; // 滚动多少像素后触发隐藏/显示

        window.addEventListener('scroll', function() {
            let currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (currentScrollTop > lastScrollTop && currentScrollTop > scrollThreshold) {
                // 向下滚动且超过阈值，隐藏头部
                header.classList.add('hidden');
            } else if (currentScrollTop < lastScrollTop || currentScrollTop <= scrollThreshold) {
                // 向上滚动或回到顶部，显示头部
                header.classList.remove('hidden');
            }
            
            lastScrollTop = currentScrollTop <= 0 ? 0 : currentScrollTop;
        }, false);
    }
});
