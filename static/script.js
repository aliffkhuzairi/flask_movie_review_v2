// Sticky Header
window.addEventListener('scroll', function () {
    const header = document.querySelector('header');
    header.classList.toggle('sticky', window.scrollY > 0);
});

// Toggle Review
const toggleReview = (button) => {
    const text = button.previousElementSibling;

    if (text.classList.contains('expanded')) {
        text.classList.remove('expanded');
        button.textContent = 'Read more';
    } else {
        text.classList.add('expanded');
        button.textContent = 'Show less';
    }
}

// Toggle Menu
const toggleMenu = (button) => {
    const menu = document.getElementById('navMenu');
    const icon = button.querySelector('i');

    const open = !menu.classList.contains('open');
    closeSearch();

    if (open) {
        menu.classList.add('open');
        icon.classList.remove('fa-bars');
        icon.classList.add('fa-xmark');
    }
    else {
        closeMenu();
    }
}

// Toggle Search
const toggleHeaderSearch = (button) => {
    const searchForm = document.getElementById('headerSearchForm');
    const icon = button.querySelector('i');
    const input = searchForm.querySelector('input');

    const open = !searchForm.classList.contains('open');
    closeMenu()

    if (open) {
        searchForm.classList.add('open');
        icon.classList.remove('fa-magnifying-glass');
        icon.classList.add('fa-xmark');
        input.focus();
    }
    else {
        closeSearch();
    }
};

// Close Menu
const closeMenu = () => {
    const menu = document.getElementById('navMenu');
    const menuToggle = document.querySelector('.menu-toggle');
    const menuIcon = menuToggle.querySelector('i');

    if (!menu || !menuToggle) return;

    menu.classList.remove('open');
    menuIcon.classList.remove('fa-xmark');
    menuIcon.classList.add('fa-bars');
}

// Close Search
const closeSearch = () => {
    const searchForm = document.getElementById('headerSearchForm');
    const searchToggle = document.querySelector('.header-search-toggle');
    const searchIcon = searchToggle.querySelector('i');

    if (!searchForm || !searchToggle) return;

    searchForm.classList.remove('open');
    searchIcon.classList.remove('fa-xmark');
    searchIcon.classList.add('fa-magnifying-glass');

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

// Star Rating
const setupStarRating = () => {
    const ratingContainers = document.querySelectorAll('.star-rating-input');

    ratingContainers.forEach(container => {
        const ratingInput = container.querySelector('input[name="rating"]');
        const ratingText = container.querySelector('.rating-text');
        const starButtons = container.querySelectorAll('.star-btn');

        const paintStars = (rating) => {
            starButtons.forEach(button => {
                const buttonRating = Number(button.dataset.rating);
                const icon = button.querySelector('i');

                if (buttonRating <= rating) {
                    icon.classList.remove('fa-regular');
                    icon.classList.add('fa-solid');
                } else {
                    icon.classList.remove('fa-solid');
                    icon.classList.add('fa-regular');
                }
            });
        }

        const setRating = (rating) => {
            ratingInput.value = rating;
            ratingText.textContent = `${rating}/5`;
            paintStars(rating);
        }

        const currentRating = Number(ratingInput.value || container.dataset.currentRating || 0);
        paintStars(currentRating);

        starButtons.forEach(button => {
            button.addEventListener('click', function () {
                setRating(Number(button.dataset.rating));
            });

            button.addEventListener('mouseenter', function () {
                paintStars(Number(button.dataset.rating));
            });

            button.addEventListener('mouseleave', function () {
                paintStars(Number(ratingInput.value || 0));
            });
        });
    });
}

document.addEventListener('DOMContentLoaded', setupStarRating);

