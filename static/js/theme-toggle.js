document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('theme-toggle');
    const body = document.body;

<<<<<<< HEAD
=======
    // Load the saved theme from localStorage
>>>>>>> ac485b812666c2bd949c1ff54518c909f71550d2
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.classList.add(savedTheme);
    } else {
<<<<<<< HEAD
        body.classList.add('dark-mode');
    }

=======
        body.classList.add('light-mode'); // Default theme
    }

    // Toggle theme on button click
>>>>>>> ac485b812666c2bd949c1ff54518c909f71550d2
    toggleButton.addEventListener('click', () => {
        if (body.classList.contains('light-mode')) {
            body.classList.remove('light-mode');
            body.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark-mode');
        } else {
            body.classList.remove('dark-mode');
            body.classList.add('light-mode');
            localStorage.setItem('theme', 'light-mode');
        }
    });
});
