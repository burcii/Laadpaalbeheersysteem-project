// search.js
export function initSearch(searchInput, clickableHeaders, statusFilterSelect, userTableBody, defaultPlaceholder) {

    function handleSearch() {
        const filter = searchInput.value.toLowerCase();
        const rows = userTableBody.querySelectorAll('tr');

        const activeHeader = document.querySelector('.active-search-header');
        let searchFieldKey = null;

        if (activeHeader) {
            const fieldName = activeHeader.dataset.searchField;
            if (fieldName === 'naam') searchFieldKey = 'name';
            else if (fieldName === 'e-mailadres') searchFieldKey = 'email';
            else if (fieldName === 'pasnummer') searchFieldKey = 'pass';
            else if (fieldName === 'telefoon') searchFieldKey = 'phone';
        }

        const statusFilter = statusFilterSelect.value.toLowerCase();

        rows.forEach(row => {
            const name = row.dataset.name;
            const email = row.dataset.email;
            const pass = row.dataset.pass;
            const phone = row.dataset.phone;
            const status = row.dataset.status;

            let textMatch = false;
            let statusMatch = false;

            if (searchFieldKey) {
                textMatch = row.dataset[searchFieldKey].includes(filter);
            } else {
                textMatch = (
                    name.includes(filter) ||
                    email.includes(filter) ||
                    pass.includes(filter) ||
                    phone.includes(filter)
                );
            }

            statusMatch = (statusFilter === 'alle') || (status === statusFilter);

            row.style.display = (textMatch && statusMatch) ? '' : 'none';
        });
    }

    function resetActiveHeaderStyling() {
        clickableHeaders.forEach(header => header.classList.remove('active-search-header'));
    }

    function handleHeaderClick(e) {
        const fieldText = e.currentTarget.dataset.searchField;
        const isAlreadyActive = e.currentTarget.classList.contains('active-search-header');

        resetActiveHeaderStyling();

        if (!isAlreadyActive) {
            e.currentTarget.classList.add('active-search-header');
            searchInput.placeholder = `zoeken op ${fieldText}...`;
        } else {
            searchInput.placeholder = defaultPlaceholder;
        }

        searchInput.value = '';
        searchInput.focus();
        handleSearch();
    }

    // EVENT BINDINGS
    searchInput.addEventListener('input', handleSearch);
    statusFilterSelect.addEventListener('change', handleSearch);

    clickableHeaders.forEach(header => {
        header.addEventListener('click', handleHeaderClick);
    });

    document.addEventListener('click', e => {
        const searchBar = document.querySelector('.search');

        const clickedInSearchArea =
            (searchBar && searchBar.contains(e.target)) ||
            Array.from(clickableHeaders).some(h => h.contains(e.target));

        if (!clickedInSearchArea) resetActiveHeaderStyling();
    });

    searchInput.addEventListener('blur', () => {
        if (searchInput.value === '') searchInput.placeholder = defaultPlaceholder;
    });

    return { handleSearch };
}
