// HEADER
const setupStickyHeader = () => {
    const header = document.querySelector('header');

    if (!header) return;

    window.addEventListener('scroll', () => {
        header.classList.toggle('sticky', window.scrollY > 0);
    });
};

// TOGGLE MENU
const setupMenuToggle = () => {
    const menuToggle = document.getElementById('menuToggle');
    const menu = document.getElementById('navMenu');

    if (!menuToggle || !menu) return;

    menuToggle.addEventListener('click', () => {
        const icon = menuToggle.querySelector('i');
        const open = !menu.classList.contains('open');

        closeSearch();

        if (open) {
            menu.classList.add('open');
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-xmark');
        } else {
            closeMenu();
        }
    });
};

// CLOSE MENU
const closeMenu = () => {
    const menu = document.getElementById('navMenu');
    const menuToggle = document.querySelector('.menu-toggle');

    if (!menu || !menuToggle) return;

    const menuIcon = menuToggle.querySelector('i');

    menu.classList.remove('open');
    menuIcon.classList.remove('fa-xmark');
    menuIcon.classList.add('fa-bars');
}

// TOGGLE SEARCH
const setupHeaderSearchToggle = () => {
    const searchToggle = document.getElementById('headerSearchToggle');
    const searchForm = document.getElementById('headerSearchForm');

    if (!searchToggle || !searchForm) return;

    searchToggle.addEventListener('click', () => {
        const icon = searchToggle.querySelector('i');
        const input = searchForm.querySelector('input');
        const open = !searchForm.classList.contains('open');

        closeMenu();

        if (open) {
            searchForm.classList.add('open');
            icon.classList.remove('fa-magnifying-glass');
            icon.classList.add('fa-xmark');

            if (input) input.focus();
        } else {
            closeSearch();
        }
    });
};

// CLOSE SEARCH
const closeSearch = () => {
    const searchForm = document.getElementById('headerSearchForm');
    const searchToggle = document.querySelector('.header-search-toggle');

    if (!searchForm || !searchToggle) return;

    const searchIcon = searchToggle.querySelector('i');

    searchForm.classList.remove('open');
    searchIcon.classList.remove('fa-xmark');
    searchIcon.classList.add('fa-magnifying-glass');
}

// PASSWORD VISIBILITY TOGGLE
const setupPasswordToggles = () => {
    const passwordToggles = document.querySelectorAll('.password-toggle');

    passwordToggles.forEach((toggle) => {
        toggle.addEventListener('click', () => {
            const passwordField = toggle.closest('.password-field');
            const input = passwordField.querySelector('input');
            const icon = toggle.querySelector('i');

            const isPassword = input.type === 'password';

            input.type = isPassword ? 'text' : 'password';

            icon.classList.toggle('fa-eye', !isPassword);
            icon.classList.toggle('fa-eye-slash', isPassword);

            toggle.setAttribute(
                'aria-label',
                isPassword ? 'Hide password' : 'Show password'
            );
        });
    });
};

// SETUP REVIEW TEXT TOGGLE
const setupReviewTextToggle = () => {
    const blocks = document.querySelectorAll('.review-text-block');

    blocks.forEach((block) => {
        const text = block.querySelector('.review-text');
        const button = block.querySelector('.text-toggle');

        if (!text || !button) return;

        if (text.scrollHeight <= text.clientHeight + 2) {
            button.style.display = 'none';
            return;
        }

        button.addEventListener('click', () => {
            const expanded = text.classList.toggle('expanded');
            button.textContent = expanded ? 'Show less' : 'Read more';
        });
    });
};

// SETUP PROFILE TAB SCROLL RESTORE
const setupProfileTabScrollRestore = () => {
    const profileTabs = document.querySelectorAll('.js-profile-tab');

    if (!profileTabs.length) return;

    profileTabs.forEach((tab) => {
        tab.addEventListener('click', () => {
            sessionStorage.setItem('profileTabScrollY', String(window.scrollY));
        });
    });

    const savedScrollY = sessionStorage.getItem('profileTabScrollY');

    if (savedScrollY !== null) {
        window.scrollTo({
            top: Number(savedScrollY),
            behavior: 'instant'
        });

        sessionStorage.removeItem('profileTabScrollY');
    }
};


let pendingConfirmForm = null;

// OPEN CONFIRMATION MODAL
const openConfirmModal = (form) => {
    const modal = document.getElementById('confirmActionModal');
    const title = document.getElementById('confirmModalTitle');
    const message = document.getElementById('confirmModalMessage');

    if (!modal || !title || !message) return;

    pendingConfirmForm = form;

    title.textContent = form.dataset.confirmTitle || 'Are you sure?';
    message.textContent = form.dataset.confirmMessage || 'This action cannot be undone.';

    modal.classList.add('open');
};

// CLOSE CONFIRMATION MODAL
const closeConfirmModal = () => {
    const modal = document.getElementById('confirmActionModal');

    if (modal) {
        modal.classList.remove('open');
    }

    pendingConfirmForm = null;
};

// SETUP CONFIRMATION MODAL
const setupConfirmModal = () => {
    const forms = document.querySelectorAll('.js-confirm-form');
    const confirmButton = document.getElementById('confirmModalSubmit');
    const modal = document.getElementById('confirmActionModal');
    const closeButton = document.getElementById('confirmModalClose');
    const cancelButton = document.getElementById('confirmModalCancel');

    forms.forEach((form) => {
        form.addEventListener('submit', (event) => {
            event.preventDefault();
            openConfirmModal(form);
        });
    });

    if (confirmButton) {
        confirmButton.addEventListener('click', () => {
            if (!pendingConfirmForm) return;

            const form = pendingConfirmForm;
            pendingConfirmForm = null;
            form.submit();
        });
    }

    if (modal) {
        modal.addEventListener('click', (event) => {
            if (event.target === modal) {
                closeConfirmModal();
            }
        });
    }

    if (closeButton) {
        closeButton.addEventListener('click', closeConfirmModal);
    }

    if (cancelButton) {
        cancelButton.addEventListener('click', closeConfirmModal);
    }
};

// SETUP AVATAR CROPPER
const setupAvatarCropper = () => {
    const avatarForm = document.getElementById('avatarForm');
    const avatarInput = document.getElementById('avatarUpload');
    const cropperOverlay = document.getElementById('avatarCropperOverlay');
    const cropperImage = document.getElementById('avatarCropperImage');
    const croppedAvatarInput = document.getElementById('croppedAvatar');

    const saveButton = document.getElementById('saveAvatarCrop');
    const cancelButton = document.getElementById('cancelAvatarCrop');
    const closeButton = document.getElementById('closeAvatarCropper');

    if (
        !avatarForm ||
        !avatarInput ||
        !cropperOverlay ||
        !cropperImage ||
        !croppedAvatarInput ||
        !saveButton ||
        !cancelButton ||
        !closeButton
    ) {
        return;
    }

    if (typeof Cropper === 'undefined') {
        console.error('Cropper.js is not loaded.');
        return;
    }

    let cropper = null;
    let objectUrl = null;

    const closeCropper = () => {
        avatarInput.value = '';
        croppedAvatarInput.value = '';
        cropperOverlay.classList.remove('open');

        if (cropper) {
            cropper.destroy();
            cropper = null;
        }

        if (objectUrl) {
            URL.revokeObjectURL(objectUrl);
            objectUrl = null;
        }
    };

    avatarInput.addEventListener('change', function () {
        const file = avatarInput.files[0];

        if (!file) return;

        if (!file.type.startsWith('image/')) {
            alert('Please choose an image file.');
            avatarInput.value = '';
            return;
        }

        if (objectUrl) {
            URL.revokeObjectURL(objectUrl);
        }

        objectUrl = URL.createObjectURL(file);
        cropperImage.src = objectUrl;
        croppedAvatarInput.value = '';
        cropperOverlay.classList.add('open');

        if (cropper) {
            cropper.destroy();
            cropper = null;
        }

        cropperImage.onload = () => {
            cropper = new Cropper(cropperImage, {
                aspectRatio: 1,
                viewMode: 1,
                dragMode: 'move',
                autoCropArea: 1,
                background: false,
                responsive: true,
                cropBoxMovable: false,
                cropBoxResizable: false,
                movable: true,
                zoomable: true,
                wheelZoomRatio: 0.08,
                rotatable: false,
                scalable: false
            });
        };
    });

    saveButton.addEventListener('click', function () {
        if (!cropper) return;

        const canvas = cropper.getCroppedCanvas({
            width: 400,
            height: 400,
            imageSmoothingEnabled: true,
            imageSmoothingQuality: 'high'
        });

        if (!canvas) return;

        croppedAvatarInput.value = canvas.toDataURL('image/jpeg', 0.9);

        cropper.destroy();
        cropper = null;

        if (objectUrl) {
            URL.revokeObjectURL(objectUrl);
            objectUrl = null;
        }

        cropperOverlay.classList.remove('open');
        avatarForm.submit();
    });

    cancelButton.addEventListener('click', closeCropper);
    closeButton.addEventListener('click', closeCropper);

    cropperOverlay.addEventListener('click', function (event) {
        if (event.target === cropperOverlay) {
            closeCropper();
        }
    });
};

// SETUP STAR RATING
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

// OPEN DELETE MODAL STEP 1
const openDeleteStepOne = () => {
    const modal = document.getElementById('deleteStepOneModal');

    if (!modal) return;

    modal.classList.add('open');
};

// OPEN DELETE MODAL STEP 2
const openDeleteStepTwo = () => {
    const stepOne = document.getElementById('deleteStepOneModal');
    const stepTwo = document.getElementById('deleteStepTwoModal');
    const passwordInput = document.getElementById('delete-password');

    if (!stepOne || !stepTwo) return;

    stepOne.classList.remove('open');
    stepTwo.classList.add('open');

    if (passwordInput) {
        passwordInput.focus();
    }
};

// CLOSE DELETE MODAL
const closeDeleteModals = () => {
    const stepOne = document.getElementById('deleteStepOneModal');
    const stepTwo = document.getElementById('deleteStepTwoModal');
    const passwordInput = document.getElementById('delete-password');
    const confirmInput = document.getElementById('confirm-delete');

    if (stepOne) {
        stepOne.classList.remove('open');
    }

    if (stepTwo) {
        stepTwo.classList.remove('open');
    }

    if (passwordInput) {
        passwordInput.value = '';
    }

    if (confirmInput) {
        confirmInput.value = '';
    }
};

document.addEventListener('click', function (event) {
    const stepOne = document.getElementById('deleteStepOneModal');
    const stepTwo = document.getElementById('deleteStepTwoModal');

    if (event.target === stepOne || event.target === stepTwo) {
        closeDeleteModals();
    }
});

document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
        closeDeleteModals();
    }
});

// INIT
document.addEventListener("DOMContentLoaded", () => {
    setupPasswordToggles();
    setupStickyHeader();
    setupMenuToggle();
    setupHeaderSearchToggle();
    setupReviewTextToggle();
    setupProfileTabScrollRestore();
    setupStarRating();
    setupAvatarCropper();
    setupConfirmModal();
})