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

    // 团队成员动画
    const teamMembers = document.querySelectorAll('.team-member');
    
    teamMembers.forEach((member, index) => {
        gsap.from(member, {
            opacity: 0,
            y: 50,
            rotation: 15,
            scale: 0.8,
            duration: 0.8,
            delay: 0.2 * index,
            ease: "back.out(1.7)",
            scrollTrigger: {
                trigger: member,
                start: "top 80%",
                end: "bottom 20%",
                toggleActions: "play none none reverse"
            }
        });
    });

    // 时间线动画
    gsap.registerPlugin(ScrollTrigger);

    gsap.utils.toArray('.timeline-item').forEach((item, index) => {
        gsap.from(item, {
            opacity: 0,
            y: 50,
            duration: 1,
            scrollTrigger: {
                trigger: item,
                start: 'top 80%',
                end: 'bottom 20%',
                toggleActions: 'play none none reverse'
            }
        });
    });
});
