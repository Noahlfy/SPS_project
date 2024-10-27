// Search bar

const searchIcon = document.getElementById('searchIcon');
const searchInput = document.getElementById('searchInput');

if (searchIcon && searchInput) {  // Vérifie si les éléments existent
    searchIcon.addEventListener('click', function() {
        searchInput.focus(); 
    });
} else {
    console.log('Search elements not found on this page.');
}







