// DOM Elements
const travelForm = document.getElementById('travelForm');
const imageInput = document.getElementById('imageInput');
const preferencesInput = document.getElementById('preferencesInput');
const dropZone = document.getElementById('dropZone');
const uploadButton = document.getElementById('uploadButton');
const imagePreview = document.getElementById('imagePreview');
const previewImg = document.getElementById('previewImg');
const removeImageBtn = document.getElementById('removeImage');
const imageFileName = document.getElementById('imageFileName');
const submitButton = document.getElementById('submitButton');
const loadingState = document.getElementById('loadingState');
const outputSection = document.getElementById('outputSection');
const itineraryContent = document.getElementById('itineraryContent');
const errorMessage = document.getElementById('errorMessage');

// Event Listeners for Image Upload
uploadButton.addEventListener('click', () => {
    imageInput.click();
});

imageInput.addEventListener('change', handleImageSelect);

// Drag and Drop
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        imageInput.files = files;
        handleImageSelect();
    }
});

// Handle Image Selection
function handleImageSelect() {
    const file = imageInput.files[0];
    if (file) {
        if (!file.type.startsWith('image/')) {
            showError('Please select a valid image file');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            previewImg.src = e.target.result;
            imagePreview.style.display = 'block';
            imageFileName.textContent = file.name;
            imageFileName.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

// Remove Image
removeImageBtn.addEventListener('click', () => {
    imageInput.value = '';
    imagePreview.style.display = 'none';
    imageFileName.style.display = 'none';
});

// Form Submission
travelForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const file = imageInput.files[0];
    const preferences = preferencesInput.value.trim();

    if (!file) {
        showError('Please upload an image of your destination');
        return;
    }

    if (!preferences) {
        showError('Please provide your travel preferences');
        return;
    }

    await generateItinerary(file, preferences);
});

// Generate Itinerary
async function generateItinerary(file, preferences) {
    try {
        // Clear previous errors
        hideError();
        
        // Show loading state
        showLoading();
        
        // Prepare form data
        const formData = new FormData();
        formData.append('image', file);
        formData.append('preferences', preferences);

        // Send request to backend
        const response = await fetch('/api/generate-itinerary', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Failed to generate itinerary');
        }

        const itinerary = await response.json();
        
        // Hide loading state
        hideLoading();
        
        // Display itinerary
        displayItinerary(itinerary);
        
    } catch (error) {
        hideLoading();
        showError(`Error: ${error.message}`);
        console.error('Error generating itinerary:', error);
    }
}

// Display Itinerary
function displayItinerary(itinerary) {
    itineraryContent.innerHTML = '';
    
    // Check if we have the expected structure
    if (itinerary.content) {
        // Fallback if structured data wasn't returned
        itineraryContent.innerHTML = `
            <div class="itinerary-container">
                <div style="padding: 20px;">
                    <h3>Travel Itinerary Generated</h3>
                    <div style="white-space: pre-wrap; font-family: monospace; background: #f3f4f6; padding: 15px; border-radius: 6px; max-height: 400px; overflow-y: auto;">
                        ${escapeHtml(itinerary.content)}
                    </div>
                </div>
            </div>
        `;
    } else {
        // Build structured itinerary display
        let html = '<div class="itinerary-container">';
        
        // Summary Card
        if (itinerary.summary) {
            html += buildSummaryCard(itinerary.summary);
        }
        
        // Itinerary Days
        if (itinerary.itinerary && Array.isArray(itinerary.itinerary)) {
            html += buildDaysSections(itinerary.itinerary);
        }
        
        // Dining Recommendations
        if (itinerary.dining_recommendations && Array.isArray(itinerary.dining_recommendations)) {
            html += buildDiningSection(itinerary.dining_recommendations);
        }
        
        // Travel Tips
        if (itinerary.travel_tips && Array.isArray(itinerary.travel_tips)) {
            html += buildTipsSection(itinerary.travel_tips);
        }
        
        html += '</div>';
        itineraryContent.innerHTML = html;
    }
    
    // Show output section
    outputSection.style.display = 'block';
    
    // Scroll to output
    setTimeout(() => {
        outputSection.scrollIntoView({ behavior: 'smooth' });
    }, 100);
    
    // Add event listeners for collapsible sections
    attachCollapsibleListeners();
}

// Build Summary Card
function buildSummaryCard(summary) {
    return `
        <div class="summary-card">
            <div class="summary-title">${summary.destination || 'Destination'}</div>
            <div class="summary-grid">
                <div class="summary-item">
                    <div class="summary-label">Duration</div>
                    <div class="summary-value">${summary.duration || 'N/A'}</div>
                </div>
                <div class="summary-item">
                    <div class="summary-label">Trip Type</div>
                    <div class="summary-value">${summary.trip_type || 'N/A'}</div>
                </div>
                <div class="summary-item">
                    <div class="summary-label">Budget</div>
                    <div class="summary-value">${summary.estimated_budget || 'N/A'}</div>
                </div>
            </div>
        </div>
    `;
}

// Build Days Sections
function buildDaysSections(days) {
    let html = '';
    
    days.forEach((day, index) => {
        html += `
            <div class="day-section">
                <div class="day-header" onclick="toggleDayContent(this)">
                    <span>📅 ${day.title || `Day ${day.day || index + 1}`}</span>
                    <span class="day-toggle">▼</span>
                </div>
                <div class="day-content">
        `;
        
        if (day.activities && Array.isArray(day.activities)) {
            day.activities.forEach(activity => {
                html += buildActivityCard(activity);
            });
        }
        
        html += `
                </div>
            </div>
        `;
    });
    
    return html;
}

// Build Activity Card
function buildActivityCard(activity) {
    return `
        <div class="activity">
            ${activity.time ? `<div class="activity-time">${activity.time}</div>` : ''}
            <div class="activity-name">${activity.name || 'Activity'}</div>
            ${activity.description ? `<div class="activity-description">${activity.description}</div>` : ''}
            ${activity.location ? `<div class="activity-location">${activity.location}</div>` : ''}
            ${activity.search_fact ? `<div class="search-fact">${activity.search_fact}</div>` : ''}
            ${activity.google_search_link ? `<a href="${activity.google_search_link}" target="_blank" class="search-link">🔗 Learn More</a>` : ''}
        </div>
    `;
}

// Build Dining Section
function buildDiningSection(dining) {
    let html = '<div class="section"><h3 class="section-title">🍽️ Dining Recommendations</h3><div class="recommendations-grid">';
    
    dining.forEach(restaurant => {
        html += `
            <div class="recommendation-card">
                <h4>${restaurant.name || 'Restaurant'}</h4>
                ${restaurant.type ? `<div class="recommendation-type">${restaurant.type}</div>` : ''}
                ${restaurant.description ? `<div class="recommendation-description">${restaurant.description}</div>` : ''}
                ${restaurant.average_rating ? `<div class="recommendation-rating">⭐ ${restaurant.average_rating}</div>` : ''}
            </div>
        `;
    });
    
    html += '</div></div>';
    return html;
}

// Build Tips Section
function buildTipsSection(tips) {
    let html = '<div class="section"><h3 class="section-title">💡 Travel Tips</h3><ul class="tips-list">';
    
    tips.forEach(tip => {
        html += `<li>${tip}</li>`;
    });
    
    html += '</ul></div>';
    return html;
}

// Toggle Day Content
function toggleDayContent(header) {
    const content = header.nextElementSibling;
    const toggle = header.querySelector('.day-toggle');
    
    content.classList.toggle('open');
    toggle.classList.toggle('open');
}

// Attach Collapsible Listeners
function attachCollapsibleListeners() {
    const dayHeaders = document.querySelectorAll('.day-header');
    dayHeaders.forEach(header => {
        // Open first day by default
        if (header === dayHeaders[0]) {
            header.nextElementSibling.classList.add('open');
            header.querySelector('.day-toggle').classList.add('open');
        }
    });
}

// Show Loading State
function showLoading() {
    loadingState.style.display = 'flex';
    outputSection.style.display = 'none';
    hideError();
    submitButton.disabled = true;
}

// Hide Loading State
function hideLoading() {
    loadingState.style.display = 'none';
    submitButton.disabled = false;
}

// Show Error
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    outputSection.style.display = 'none';
}

// Hide Error
function hideError() {
    errorMessage.style.display = 'none';
}

// Escape HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Set up initial state
    outputSection.style.display = 'none';
    errorMessage.style.display = 'none';
});
