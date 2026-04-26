function toggleReview(button) {
    const text = button.previousElementSibling;

    if (text.classList.contains('expanded')) {
        text.classList.remove('expanded');
        button.textContent = 'Read more';
    } else {
        text.classList.add('expanded');
        button.textContent = 'Show less';
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const blocks = document.querySelectorAll('.review-text-block');

    blocks.forEach(block => {
        const text = block.querySelector('.review-text');
        const button = block.querySelector('.text-toggle');

        if (text.scrollHeight <= text.clientHeight + 2) {
            button.style.display = 'none';
        }
    });
});

// Restore scroll position after reload
window.addEventListener('load', function () {
    const scrollPos = localStorage.getItem('scrollPosition');

    if (scrollPos !== null) {
        window.scrollTo({
            top: parseInt(scrollPos),
            behavior: 'smooth'
        });
        localStorage.removeItem('scrollPosition');
    }
});

// Sticky Header
window.addEventListener('scroll', function () {
    const header = document.querySelector('header');
    header.classList.toggle('sticky', window.scrollY > 0);
});


