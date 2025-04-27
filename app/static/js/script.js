document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const searchForm = document.getElementById('search-form');
    const queryInput = document.getElementById('query');
    const resultsContainer = document.getElementById('results');
    const messagesContainer = document.getElementById('messages');
    const listingsContainer = document.getElementById('listings');
    const loadingEl = document.getElementById('loading');
    
    // Event listeners
    searchForm.addEventListener('submit', handleSearch);
    
    /**
     * Handle search form submission
     */
    function handleSearch(e) {
        e.preventDefault();
        
        const query = queryInput.value.trim();
        if (!query) return;
        
        // Show loading state
        showLoading();
        
        // Add user query to messages
        addMessage('user', query);
        
        // Show results container
        resultsContainer.classList.add('visible');
        
        // Send request to server
        fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `query=${encodeURIComponent(query)}`
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Hide loading
            hideLoading();
            
            // Process search results
            displayResults(data);
        })
        .catch(error => {
            console.error('Error:', error);
            hideLoading();
            addMessage('system', 'Sorry, something went wrong with your search. Please try again.');
        });
    }
    
    /**
     * Add a message to the messages container
     */
    function addMessage(type, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = text;
        messagesContainer.appendChild(messageDiv);
        
        // Scroll to message
        messageDiv.scrollIntoView({ behavior: 'smooth' });
    }
    
    /**
     * Display search results
     */
    function displayResults(data) {
        // Clear previous listings
        listingsContainer.innerHTML = '';
        
        const listings = data.results || [];
        const count = listings.length;
        
        // Add system message with results count
        if (count > 0) {
            addMessage('system', `Found ${count} places that match your criteria.`);
        } else {
            addMessage('system', "I couldn't find any places matching those criteria. Try a different search.");
            return;
        }
        
        // Add each listing
        listings.forEach(listing => addListingCard(listing));
    }
    
    /**
     * Add a listing card to the listings container
     */
    function addListingCard(listing) {
        const card = document.createElement('div');
        card.className = 'listing-card';
        
        // Image
        const imageDiv = document.createElement('div');
        imageDiv.className = 'listing-image';
        
        const img = document.createElement('img');
        img.src = listing.image_url || '/static/images/placeholder.svg';
        img.alt = listing.title;
        img.onerror = function() {
            this.src = '/static/images/placeholder.svg';
        };
        
        imageDiv.appendChild(img);
        card.appendChild(imageDiv);
        
        // Details
        const details = document.createElement('div');
        details.className = 'listing-details';
        
        // Price
        const price = document.createElement('div');
        price.className = 'listing-price';
        price.textContent = `$${listing.price.toLocaleString()}`;
        details.appendChild(price);
        
        // Title
        const title = document.createElement('h3');
        title.className = 'listing-title';
        title.textContent = listing.title;
        details.appendChild(title);
        
        // Info (beds/baths)
        const info = document.createElement('div');
        info.className = 'listing-info';
        
        const beds = document.createElement('span');
        beds.innerHTML = `<i class="fas fa-bed"></i> ${listing.bedrooms || 'N/A'} bed`;
        info.appendChild(beds);
        
        const baths = document.createElement('span');
        baths.innerHTML = `<i class="fas fa-bath"></i> ${listing.bathrooms || 'N/A'} bath`;
        info.appendChild(baths);
        
        if (listing.square_footage) {
            const sqft = document.createElement('span');
            sqft.innerHTML = `<i class="fas fa-vector-square"></i> ${listing.square_footage} sqft`;
            info.appendChild(sqft);
        }
        
        details.appendChild(info);
        
        // Address
        const address = document.createElement('div');
        address.className = 'listing-address';
        address.textContent = `${listing.address || ''}, ${listing.city}, ${listing.state} ${listing.zip_code || ''}`;
        details.appendChild(address);
        
        // View link
        const link = document.createElement('a');
        link.className = 'listing-link';
        link.href = listing.url;
        link.target = '_blank';
        link.textContent = 'View Listing';
        details.appendChild(link);
        
        // Source
        const source = document.createElement('div');
        source.className = 'listing-source';
        source.textContent = `Source: ${listing.source}`;
        details.appendChild(source);
        
        card.appendChild(details);
        listingsContainer.appendChild(card);
    }
    
    /**
     * Show loading spinner
     */
    function showLoading() {
        loadingEl.classList.add('visible');
        listingsContainer.innerHTML = '';
    }
    
    /**
     * Hide loading spinner
     */
    function hideLoading() {
        loadingEl.classList.remove('visible');
    }
});