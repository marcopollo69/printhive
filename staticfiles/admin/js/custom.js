/**
 * PrintHive Kenya - Admin Dashboard JavaScript
 * Version: 2.0 - Cleaned & Optimized
 */

(function () {
    'use strict';

    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', init);

    function init() {
        initSidebar();
        initQuickSearch();
        initDeleteConfirmation();
        highlightActiveMenu();
    }

    /**
     * Sidebar Toggle for Mobile
     */
    function initSidebar() {
        const menuToggle = document.getElementById('menuToggle');
        const sidebar = document.getElementById('adminSidebar');
        const overlay = document.getElementById('sidebarOverlay');

        if (!menuToggle || !sidebar) return;

        // Toggle sidebar on button click
        menuToggle.addEventListener('click', toggleSidebar);

        // Close sidebar when clicking overlay
        if (overlay) {
            overlay.addEventListener('click', closeSidebar);
        }

        // Close sidebar on Escape key
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && sidebar.classList.contains('open')) {
                closeSidebar();
            }
        });

        function toggleSidebar() {
            sidebar.classList.toggle('open');
            if (overlay) overlay.classList.toggle('active');
            document.body.style.overflow = sidebar.classList.contains('open') ? 'hidden' : '';
        }

        function closeSidebar() {
            sidebar.classList.remove('open');
            if (overlay) overlay.classList.remove('active');
            document.body.style.overflow = '';
        }
    }

    /**
     * Highlight Active Menu Item Based on Current URL
     */
    function highlightActiveMenu() {
        const currentPath = window.location.pathname;
        const menuLinks = document.querySelectorAll('.sidebar-menu-link');

        menuLinks.forEach(function (link) {
            const href = link.getAttribute('href');
            if (!href) return;

            // Remove existing active state
            link.classList.remove('active');

            // Check for exact match or partial match (excluding dashboard)
            if (href !== '/admin/' && currentPath.includes(href)) {
                link.classList.add('active');
            } else if (href === '/admin/' && (currentPath === '/admin/' || currentPath === '/admin')) {
                link.classList.add('active');
            }
        });
    }

    /**
     * Quick Search in Header
     */
    function initQuickSearch() {
        const searchInputs = document.querySelectorAll('#quickSearch, .header-search input');

        searchInputs.forEach(function (input) {
            if (!input) return;

            input.addEventListener('keypress', function (e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    const value = this.value.trim();

                    if (value) {
                        const url = new URL(window.location.href);
                        url.searchParams.set('q', value);
                        window.location.href = url.toString();
                    }
                }
            });
        });
    }

    /**
     * Delete Confirmation Dialog
     */
    function initDeleteConfirmation() {
        const deleteLinks = document.querySelectorAll('.deletelink, .deletelink-box a, input[name="delete"]');

        deleteLinks.forEach(function (link) {
            link.addEventListener('click', function (e) {
                const confirmed = confirm('Are you sure you want to delete this item? This action cannot be undone.');

                if (!confirmed) {
                    e.preventDefault();
                    return false;
                }
            });
        });
    }

    /**
     * Toast Notification (for future use)
     */
    window.showToast = function (message, type) {
        type = type || 'success';

        const toast = document.createElement('div');
        toast.className = 'toast toast-' + type;

        const icon = type === 'success' ? '✓' : type === 'error' ? '✕' : '!';
        toast.innerHTML = '<span class="toast-icon">' + icon + '</span><span>' + message + '</span>';

        // Styles
        toast.style.cssText = [
            'position: fixed',
            'bottom: 24px',
            'right: 24px',
            'padding: 14px 20px',
            'background: #fff',
            'border-radius: 12px',
            'box-shadow: 0 8px 24px rgba(0,0,0,0.12)',
            'display: flex',
            'align-items: center',
            'gap: 10px',
            'font-size: 14px',
            'font-weight: 500',
            'z-index: 9999',
            'transform: translateY(100px)',
            'opacity: 0',
            'transition: all 0.3s ease'
        ].join(';');

        document.body.appendChild(toast);

        // Animate in
        requestAnimationFrame(function () {
            toast.style.transform = 'translateY(0)';
            toast.style.opacity = '1';
        });

        // Remove after 3 seconds
        setTimeout(function () {
            toast.style.transform = 'translateY(100px)';
            toast.style.opacity = '0';
            setTimeout(function () {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, 3000);
    };

})();
