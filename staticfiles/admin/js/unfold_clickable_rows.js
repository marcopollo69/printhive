document.addEventListener('DOMContentLoaded', function () {
    // Select all table rows in the results table
    // Unfold uses standard HTML tables but with Tailwind classes
    const rows = document.querySelectorAll('table tbody tr');

    rows.forEach(row => {
        // Find the first link that goes to a change page
        const editLink = row.querySelector('a[href*="/change/"]');

        if (editLink) {
            // Make the row look clickable
            row.style.cursor = 'pointer';
            row.classList.add('hover:bg-gray-50', 'dark:hover:bg-gray-800', 'transition-colors');

            // Add click event
            row.addEventListener('click', function (e) {
                // Prevent redirect if user clicked a button, link, or checkbox directly
                if (e.target.closest('a') || e.target.closest('button') || e.target.closest('input') || e.target.closest('label')) {
                    return;
                }

                // Navigate to the edit page
                window.location.href = editLink.href;
            });
        }
    });
});
