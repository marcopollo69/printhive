// Mobile menu toggle
document.getElementById('menu-toggle').addEventListener('click', function () {
    const menu = document.getElementById('mobile-menu');
    menu.classList.toggle('hidden');
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;

        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            e.preventDefault();
            targetElement.scrollIntoView({
                behavior: 'smooth'
            });

            // Close mobile menu if open
            const mobileMenu = document.getElementById('mobile-menu');
            if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
                mobileMenu.classList.add('hidden');
            }
        }
    });
});

// Pricing Calculator Modal
const modal = document.getElementById('estimate-modal');
const modalTitle = document.getElementById('modal-title');
const estimateQty = document.getElementById('estimate-qty');
const estimateTotal = document.getElementById('estimate-total');
const minQtySpan = document.getElementById('min-qty');
const closeModalBtn = document.getElementById('close-modal');

let currentUnitPrice = 0;
let currentMinQty = 1;
let currentProductId = null;
let debounceTimer;

// Open modal when clicking estimate buttons
document.querySelectorAll('.estimate-btn').forEach(btn => {
    btn.addEventListener('click', function () {
        const title = this.dataset.title;
        const unitPrice = parseFloat(this.dataset.unitPrice);
        const minQty = parseInt(this.dataset.minQty) || 1;
        const productId = this.dataset.productId;

        currentUnitPrice = unitPrice;
        currentMinQty = minQty;
        currentProductId = productId;

        modalTitle.textContent = `Estimate: ${title}`;
        estimateQty.min = minQty;
        estimateQty.value = Math.max(minQty, 1);
        minQtySpan.textContent = minQty;

        calculateEstimate();
        modal.classList.remove('hidden');

        // Re-initialize feather icons for the modal
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    });
});

// Close modal
if (closeModalBtn) {
    closeModalBtn.addEventListener('click', function () {
        modal.classList.add('hidden');
    });
}

// Close modal when clicking outside
if (modal) {
    modal.addEventListener('click', function (e) {
        if (e.target === modal) {
            modal.classList.add('hidden');
        }
    });
}

// Calculate estimate on quantity change
if (estimateQty) {
    estimateQty.addEventListener('input', calculateEstimate);
}

function calculateEstimate() {
    let qty = parseInt(estimateQty.value) || currentMinQty;

    // Enforce minimum quantity
    if (qty < currentMinQty) {
        qty = currentMinQty;
        estimateQty.value = qty;
    }

    // Clear previous timer
    clearTimeout(debounceTimer);

    // Show loading state
    estimateTotal.textContent = 'Calculating...';
    estimateTotal.classList.add('text-gray-500', 'text-xl');
    estimateTotal.classList.remove('text-3xl', 'text-accent');

    // Debounce API call
    debounceTimer = setTimeout(() => {
        if (!currentProductId) {
            // Fallback to client-side if no product ID (shouldn't happen)
            const total = qty * currentUnitPrice;
            updateTotalDisplay(total);
            return;
        }

        fetch(`/api/calculate-price/?product_id=${currentProductId}&qty=${qty}`)
            .then(response => response.json())
            .then(data => {
                if (data.total_price) {
                    updateTotalDisplay(data.total_price);
                } else {
                    console.error('Error calculating price:', data);
                    estimateTotal.textContent = 'Error';
                }
            })
            .catch(error => {
                console.error('Network error:', error);
                estimateTotal.textContent = 'Error';
            });
    }, 500); // 500ms debounce
}

function updateTotalDisplay(amount) {
    estimateTotal.textContent = `KSh ${amount.toLocaleString('en-KE', { maximumFractionDigits: 0 })}`;
    estimateTotal.classList.remove('text-gray-500', 'text-xl');
    estimateTotal.classList.add('text-3xl', 'text-accent');
}

// Phone number validation (Kenyan format)
function validateKenyanPhone(phone) {
    const cleaned = phone.replace(/[\s-]/g, '');
    const pattern = /^(\+254|0)[17]\d{8}$/;
    return pattern.test(cleaned);
}

// Form validation
const contactForm = document.getElementById('contact-form');
if (contactForm) {
    const phoneInput = document.getElementById('id_phone');

    if (phoneInput) {
        phoneInput.addEventListener('blur', function () {
            const isValid = validateKenyanPhone(this.value);
            if (!isValid && this.value.length > 0) {
                this.classList.add('border-red-500');
                this.classList.remove('border-gray-300');
            } else {
                this.classList.remove('border-red-500');
                this.classList.add('border-gray-300');
            }
        });
    }
}

// WhatsApp link generator
function generateWhatsAppLink(phone, message) {
    let cleaned = phone.replace(/[\s-]/g, '');
    if (cleaned.startsWith('0')) {
        cleaned = '254' + cleaned.substring(1);
    } else if (cleaned.startsWith('+')) {
        cleaned = cleaned.substring(1);
    }
    const encodedMessage = encodeURIComponent(message);
    return `https://wa.me/${cleaned}?text=${encodedMessage}`;
}

// Close modal on escape key
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && modal && !modal.classList.contains('hidden')) {
        modal.classList.add('hidden');
    }
});

// =============================================
// Hero Image Carousel
// =============================================
(function initHeroCarousel() {
    const carousel = document.getElementById('hero-carousel');
    if (!carousel) return;

    const slides = carousel.querySelectorAll('.carousel-slide');
    const dots = carousel.querySelectorAll('.carousel-dot');
    const prevBtn = document.getElementById('carousel-prev');
    const nextBtn = document.getElementById('carousel-next');

    if (slides.length === 0) return;

    let currentSlide = 0;
    let autoPlayInterval = null;
    let isPaused = false;
    const autoPlayDelay = 5000; // 5 seconds between slides

    // Initialize first slide as active
    function initSlides() {
        slides.forEach((slide, index) => {
            slide.classList.toggle('active', index === 0);
            slide.style.opacity = index === 0 ? '1' : '0';
        });
        updateDots(0);
    }

    // Go to a specific slide
    function goToSlide(index) {
        // Handle wrap-around
        if (index < 0) {
            index = slides.length - 1;
        } else if (index >= slides.length) {
            index = 0;
        }

        // Hide current slide
        slides[currentSlide].classList.remove('active');
        slides[currentSlide].style.opacity = '0';

        // Show new slide
        slides[index].classList.add('active');
        slides[index].style.opacity = '1';

        currentSlide = index;
        updateDots(index);
    }

    // Update dot indicators
    function updateDots(activeIndex) {
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === activeIndex);
        });
    }

    // Next slide
    function nextSlide() {
        goToSlide(currentSlide + 1);
    }

    // Previous slide
    function prevSlide() {
        goToSlide(currentSlide - 1);
    }

    // Start auto-play
    function startAutoPlay() {
        if (autoPlayInterval) return;
        autoPlayInterval = setInterval(() => {
            if (!isPaused) {
                nextSlide();
            }
        }, autoPlayDelay);
    }

    // Stop auto-play
    function stopAutoPlay() {
        if (autoPlayInterval) {
            clearInterval(autoPlayInterval);
            autoPlayInterval = null;
        }
    }

    // Pause on hover
    carousel.addEventListener('mouseenter', function () {
        isPaused = true;
        carousel.classList.add('paused');
    });

    carousel.addEventListener('mouseleave', function () {
        isPaused = false;
        carousel.classList.remove('paused');
    });

    // Touch/focus pause
    carousel.addEventListener('focusin', function () {
        isPaused = true;
        carousel.classList.add('paused');
    });

    carousel.addEventListener('focusout', function () {
        isPaused = false;
        carousel.classList.remove('paused');
    });

    // Navigation arrow clicks
    if (prevBtn) {
        prevBtn.addEventListener('click', function (e) {
            e.preventDefault();
            prevSlide();
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', function (e) {
            e.preventDefault();
            nextSlide();
        });
    }

    // Dot navigation
    dots.forEach((dot, index) => {
        dot.addEventListener('click', function (e) {
            e.preventDefault();
            goToSlide(index);
        });
    });

    // Keyboard navigation when carousel is focused
    carousel.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowLeft') {
            e.preventDefault();
            prevSlide();
        } else if (e.key === 'ArrowRight') {
            e.preventDefault();
            nextSlide();
        }
    });

    // Touch swipe support
    let touchStartX = 0;
    let touchEndX = 0;
    const minSwipeDistance = 50;

    carousel.addEventListener('touchstart', function (e) {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    carousel.addEventListener('touchend', function (e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, { passive: true });

    function handleSwipe() {
        const swipeDistance = touchEndX - touchStartX;
        if (Math.abs(swipeDistance) >= minSwipeDistance) {
            if (swipeDistance > 0) {
                prevSlide(); // Swipe right = previous
            } else {
                nextSlide(); // Swipe left = next
            }
        }
    }

    // Visibility API - pause when tab is not visible
    document.addEventListener('visibilitychange', function () {
        if (document.hidden) {
            stopAutoPlay();
        } else {
            startAutoPlay();
        }
    });

    // Initialize
    initSlides();
    startAutoPlay();

    // Make carousel focusable for keyboard navigation
    carousel.setAttribute('tabindex', '0');
    carousel.setAttribute('role', 'region');
    carousel.setAttribute('aria-label', 'Product image carousel');
})();

// Initialize feather icons
if (typeof feather !== 'undefined') {
    feather.replace();
}
