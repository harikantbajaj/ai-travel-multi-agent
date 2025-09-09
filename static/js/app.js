document.addEventListener('DOMContentLoaded', () => {
    const planningButtons = document.querySelectorAll('.planning-btn');
    const planningModal = new bootstrap.Modal(document.getElementById('planningModal'));
    const tripFormContainer = document.getElementById('tripFormContainer');
    let currentMode = null;
    let planningId = null;
    let statusInterval = null;

    planningButtons.forEach(button => {
        button.addEventListener('click', () => {
            currentMode = button.getAttribute('data-mode');
            loadTripForm(currentMode);
            planningModal.show();
        });
    });

    function loadTripForm(mode) {
        // Enhanced form with more fields and progress tracking
        let formHtml = `
            <form id="tripForm">
                <div class="mb-3">
                    <label for="destination" class="form-label">Destination</label>
                    <input type="text" class="form-control" id="destination" name="destination" required placeholder="e.g., Paris, Tokyo, Bali">
                </div>
                <div class="mb-3 row">
                    <div class="col">
                        <label for="startDate" class="form-label">Start Date</label>
                        <input type="date" class="form-control" id="startDate" name="startDate" required>
                    </div>
                    <div class="col">
                        <label for="endDate" class="form-label">End Date</label>
                        <input type="date" class="form-control" id="endDate" name="endDate" required>
                    </div>
                </div>
                <div class="mb-3">
                    <label for="budget" class="form-label">Budget Range</label>
                    <select class="form-select" id="budget" name="budget" required>
                        <option value="budget">Budget - $50-80/day (Hostels, street food)</option>
                        <option value="mid-range" selected>Mid-range - $100-150/day (Hotels, restaurants)</option>
                        <option value="luxury">Luxury - $200+/day (Premium hotels, fine dining)</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label for="currency" class="form-label">Currency</label>
                    <select class="form-select" id="currency" name="currency" required>
                        <option value="USD" selected>USD (US Dollar)</option>
                        <option value="EUR">EUR (Euro)</option>
                        <option value="GBP">GBP (British Pound)</option>
                        <option value="INR">INR (Indian Rupee)</option>
                        <option value="JPY">JPY (Japanese Yen)</option>
                        <option value="CAD">CAD (Canadian Dollar)</option>
                        <option value="AUD">AUD (Australian Dollar)</option>
                        <option value="CHF">CHF (Swiss Franc)</option>
                        <option value="CNY">CNY (Chinese Yuan)</option>
                        <option value="SGD">SGD (Singapore Dollar)</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label for="groupSize" class="form-label">Group Size</label>
                    <input type="number" class="form-control" id="groupSize" name="groupSize" min="1" max="20" value="1" required>
                </div>
                <div class="mb-3">
                    <label for="interests" class="form-label">Interests (comma-separated)</label>
                    <input type="text" class="form-control" id="interests" name="interests" placeholder="e.g., museums, food, adventure, culture, beaches">
                    <div class="form-text">Examples: museums, art, history, food, nightlife, shopping, nature, adventure, culture, architecture, photography, music, sports, beaches, mountains, festivals</div>
                </div>
                <div class="mb-3">
                    <label for="dietary" class="form-label">Dietary Restrictions/Preferences</label>
                    <input type="text" class="form-control" id="dietary" name="dietary" placeholder="e.g., vegetarian, vegan, halal, gluten-free">
                </div>
                <div class="mb-3">
                    <label for="mobility" class="form-label">Mobility Considerations</label>
                    <input type="text" class="form-control" id="mobility" name="mobility" placeholder="e.g., wheelchair accessible, limited walking, elderly care">
                </div>
                <div class="mb-3">
                    <label for="activityLevel" class="form-label">Preferred Activity Level</label>
                    <select class="form-select" id="activityLevel" name="activityLevel" required>
                        <option value="relaxed" selected>Relaxed - Minimal walking, leisure activities</option>
                        <option value="moderate">Moderate - Some walking, balanced itinerary</option>
                        <option value="active">Active - Lots of walking, adventure activities</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary w-100">Start Planning</button>
            </form>
            <div id="formFeedback" class="mt-3"></div>
            <div id="progressContainer" class="mt-3" style="display: none;">
                <div class="progress mb-2">
                    <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 0%"></div>
                </div>
                <div id="progressText" class="text-center small text-muted">Initializing...</div>
            </div>
            <div id="resultsContainer" class="mt-3" style="display: none;">
                <div class="card results-card">
                    <div class="card-header bg-success text-white">
                        <h6 class="mb-0"><i class="fas fa-check-circle me-2"></i>Planning Completed!</h6>
                    </div>
                    <div class="card-body" id="resultsContent">
                        <!-- Results will be displayed here -->
                    </div>
                </div>
            </div>
        `;

        tripFormContainer.innerHTML = formHtml;

        const tripForm = document.getElementById('tripForm');
        const formFeedback = document.getElementById('formFeedback');
        const progressContainer = document.getElementById('progressContainer');
        const resultsContainer = document.getElementById('resultsContainer');
        const progressBar = progressContainer.querySelector('.progress-bar');
        const progressText = document.getElementById('progressText');

        tripForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            formFeedback.innerHTML = '';
            resultsContainer.style.display = 'none';

            const formData = new FormData(tripForm);
            const tripDetails = {};
            formData.forEach((value, key) => {
                tripDetails[key] = value;
            });

            // Basic validation
            if (new Date(tripDetails.startDate) >= new Date(tripDetails.endDate)) {
                formFeedback.innerHTML = '<div class="alert alert-danger">End date must be after start date.</div>';
                return;
            }

            // Show progress container
            progressContainer.style.display = 'block';
            progressBar.style.width = '10%';
            progressText.textContent = 'Starting planning process...';

            try {
                const response = await fetch('/plan', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        mode: mode,
                        trip_details: tripDetails
                    })
                });

                const result = await response.json();

                if (result.status === 'success') {
                    planningId = result.planning_id;
                    formFeedback.innerHTML = `<div class="alert alert-success">${result.message}</div>`;

                    // Start polling for status updates
                    startStatusPolling();
                } else {
                    formFeedback.innerHTML = `<div class="alert alert-danger">${result.message}</div>`;
                    progressContainer.style.display = 'none';
                }
            } catch (error) {
                formFeedback.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
                progressContainer.style.display = 'none';
            }
        });

        function startStatusPolling() {
            statusInterval = setInterval(async () => {
                try {
                    const response = await fetch(`/planning_status/${planningId}`);
                    const status = await response.json();

                    progressBar.style.width = `${status.progress}%`;
                    progressText.textContent = status.message;

                    if (status.status === 'completed') {
                        clearInterval(statusInterval);
                        progressContainer.style.display = 'none';
                        displayResults(status.result);
                    } else if (status.status === 'error') {
                        clearInterval(statusInterval);
                        progressContainer.style.display = 'none';
                        formFeedback.innerHTML = `<div class="alert alert-danger">${status.message}</div>`;
                    }
                } catch (error) {
                    console.error('Error polling status:', error);
                }
            }, 1000);
        }

        function displayResults(result) {
            let resultsHtml = `
                <div class="row">
                    <div class="col-md-6">
                        <h6 class="fw-bold text-primary"><i class="fas fa-map-marker-alt me-2"></i>Destination</h6>
                        <p class="mb-3">${result.destination || 'N/A'}</p>

                        <h6 class="fw-bold text-primary"><i class="fas fa-dollar-sign me-2"></i>Estimated Cost</h6>
                        <p class="mb-3">${result.estimated_cost || 'N/A'}</p>

                        <h6 class="fw-bold text-primary"><i class="fas fa-plane me-2"></i>Flight Information</h6>
                        <p class="mb-3">${result.flight_info || 'Flight information not available'}</p>
                    </div>
                    <div class="col-md-6">
                        <h6 class="fw-bold text-primary"><i class="fas fa-calendar me-2"></i>Duration</h6>
                        <p class="mb-3">${result.duration || 'N/A'}</p>

                        <h6 class="fw-bold text-primary"><i class="fas fa-users me-2"></i>Planning Method</h6>
                        <p class="mb-3">${result.planning_method || result.agents_used || 'N/A'}</p>

                        <h6 class="fw-bold text-primary"><i class="fas fa-tshirt me-2"></i>Clothing Suggestion</h6>
                        <p class="mb-3">${result.clothing_suggestion || 'N/A'}</p>
                    </div>
                </div>
            `;

            if (result.ai_agents) {
                resultsHtml += `
                    <div class="mt-3">
                        <h6 class="fw-bold text-primary"><i class="fas fa-robot me-2"></i>AI Agents Used</h6>
                        <div class="row">
                            ${result.ai_agents.map(agent => `
                                <div class="col-md-4 mb-2">
                                    <span class="badge bg-info">${agent}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `;
            }

            if (result.weather_forecast) {
                resultsHtml += `
                    <div class="mt-3">
                        <h6 class="fw-bold text-primary"><i class="fas fa-cloud-sun me-2"></i>Weather Forecast</h6>
                        <p class="mb-0">${result.weather_forecast}</p>
                    </div>
                `;
            }

            if (result.attractions && result.attractions.length > 0) {
                resultsHtml += `
                    <div class="mt-3">
                        <h6 class="fw-bold text-primary"><i class="fas fa-camera me-2"></i>Recommended Attractions</h6>
                        <ul class="list-unstyled">
                            ${result.attractions.map(attraction => `<li><i class="fas fa-check text-success me-2"></i>${attraction}</li>`).join('')}
                        </ul>
                    </div>
                `;
            }

            // Display day-wise itinerary
            if (result.itinerary && result.itinerary.length > 0) {
                resultsHtml += `
                    <div class="mt-4">
                        <h6 class="fw-bold text-primary"><i class="fas fa-calendar-day me-2"></i>Day-wise Itinerary</h6>
                        <div class="accordion" id="itineraryAccordion">
                `;

                result.itinerary.forEach((day, index) => {
                    const dayId = `day${index + 1}`;
                    resultsHtml += `
                        <div class="accordion-item">
                            <h2 class="accordion-header" id="heading${dayId}">
                                <button class="accordion-button ${index === 0 ? '' : 'collapsed'}" type="button" data-bs-toggle="collapse" data-bs-target="#${dayId}" aria-expanded="${index === 0 ? 'true' : 'false'}" aria-controls="${dayId}">
                                    <strong>Day ${day.day} - ${day.date}</strong>
                                    <span class="ms-auto text-muted">${day.weather || 'Weather N/A'}</span>
                                </button>
                            </h2>
                            <div id="${dayId}" class="accordion-collapse collapse ${index === 0 ? 'show' : ''}" aria-labelledby="heading${dayId}" data-bs-parent="#itineraryAccordion">
                                <div class="accordion-body">
                                    ${day.attractions && day.attractions.length > 0 ? `
                                        <div class="mb-3">
                                            <h6 class="text-success"><i class="fas fa-camera me-2"></i>Attractions</h6>
                                            <ul class="list-unstyled">
                                                ${day.attractions.map(attr => `<li><i class="fas fa-map-marker-alt text-primary me-2"></i><strong>${attr.name}</strong>${attr.description ? ` - ${attr.description}` : ''}</li>`).join('')}
                                            </ul>
                                        </div>
                                    ` : ''}

                                    ${day.restaurants && day.restaurants.length > 0 ? `
                                        <div class="mb-3">
                                            <h6 class="text-warning"><i class="fas fa-utensils me-2"></i>Dining</h6>
                                            <ul class="list-unstyled">
                                                ${day.restaurants.map(rest => `<li><i class="fas fa-cutlery text-warning me-2"></i><strong>${rest.name}</strong>${rest.cuisine ? ` (${rest.cuisine})` : ''}${rest.address && rest.address !== 'Address not available' ? `<br><small class="text-muted"><i class="fas fa-map-marker-alt me-1"></i>${rest.address}</small>` : ''}</li>`).join('')}
                                            </ul>
                                        </div>
                                    ` : ''}

                                    ${day.activities && day.activities.length > 0 ? `
                                        <div class="mb-3">
                                            <h6 class="text-info"><i class="fas fa-running me-2"></i>Activities</h6>
                                            <ul class="list-unstyled">
                                                ${day.activities.map(act => `<li><i class="fas fa-star text-info me-2"></i><strong>${act.name}</strong>${act.description ? ` - ${act.description}` : ''}</li>`).join('')}
                                            </ul>
                                        </div>
                                    ` : ''}

                                    ${day.daily_cost ? `
                                        <div class="mt-3 p-2 bg-light rounded">
                                            <strong>Daily Cost: ${result.currency || '$'}${day.daily_cost.toFixed(2)}</strong>
                                        </div>
                                    ` : ''}
                                </div>
                            </div>
                        </div>
                    `;
                });

                resultsHtml += `
                        </div>
                    </div>
                `;
            }

            // Display recommended hotels if available
            if (result.hotels && result.hotels.length > 0) {
                resultsHtml += `
                    <div class="mt-4">
                        <h6 class="fw-bold text-primary"><i class="fas fa-hotel me-2"></i>Recommended Hotels</h6>
                        <div class="row">
                            ${result.hotels.map(hotel => `
                                <div class="col-md-6 mb-3">
                                    <div class="card h-100">
                                        <div class="card-body">
                                            <h6 class="card-title">${hotel.name}</h6>
                                            <div class="mb-2">
                                                <span class="badge bg-warning text-dark">${hotel.rating}⭐</span>
                                                <span class="ms-2">${result.currency || '$'}${hotel.price_per_night?.toFixed(2) || 'N/A'}/night</span>
                                            </div>
                                            ${hotel.address ? `<p class="card-text small text-muted"><i class="fas fa-map-marker-alt me-1"></i>${hotel.address}</p>` : ''}
                                            ${hotel.amenities && hotel.amenities.length > 0 ? `
                                                <div class="mt-2">
                                                    <small class="text-muted">Amenities:</small>
                                                    <div class="mt-1">
                                                        ${hotel.amenities.slice(0, 3).map(amenity => `<span class="badge bg-light text-dark me-1">${amenity}</span>`).join('')}
                                                        ${hotel.amenities.length > 3 ? `<span class="badge bg-light text-dark">+${hotel.amenities.length - 3} more</span>` : ''}
                                                    </div>
                                                </div>
                                            ` : ''}
                                        </div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `;
            }

            // Display expense breakdown if available
            if (result.expense_breakdown) {
                resultsHtml += `
                    <div class="mt-4">
                        <h6 class="fw-bold text-primary"><i class="fas fa-chart-pie me-2"></i>Expense Breakdown</h6>
                        <div class="row">
                            <div class="col-md-6">
                                <div class="card">
                                    <div class="card-body">
                                        <h6 class="card-title">Accommodation</h6>
                                        <p class="card-text">${result.currency || '$'}${result.expense_breakdown.accommodation?.toFixed(2) || '0.00'}</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="card">
                                    <div class="card-body">
                                        <h6 class="card-title">Food</h6>
                                        <p class="card-text">${result.currency || '$'}${result.expense_breakdown.food?.toFixed(2) || '0.00'}</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="card">
                                    <div class="card-body">
                                        <h6 class="card-title">Activities</h6>
                                        <p class="card-text">${result.currency || '$'}${result.expense_breakdown.activities?.toFixed(2) || '0.00'}</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="card">
                                    <div class="card-body">
                                        <h6 class="card-title">Transportation</h6>
                                        <p class="card-text">${result.currency || '$'}${result.expense_breakdown.transportation?.toFixed(2) || '0.00'}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            }

            resultsHtml += `
                <div class="mt-4 text-center">
                    <button class="btn btn-success me-2" onclick="downloadPlan()">
                        <i class="fas fa-download me-2"></i>Download Plan
                    </button>
                    <button class="btn btn-outline-primary" onclick="sharePlan()">
                        <i class="fas fa-share me-2"></i>Share Plan
                    </button>
                </div>
            `;

            document.getElementById('resultsContent').innerHTML = resultsHtml;
            resultsContainer.style.display = 'block';
        }

        // Global functions for buttons
        window.downloadPlan = function() {
            if (!planningId) {
                alert('No planning data available for download.');
                return;
            }

            // Create a temporary link to trigger download
            const downloadUrl = `/download/${planningId}`;
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.download = ''; // Let the server set the filename
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        };

        window.sharePlan = function() {
            if (navigator.share) {
                navigator.share({
                    title: 'My AI Travel Plan',
                    text: 'Check out this amazing travel plan created by AI!',
                    url: window.location.href
                });
            } else {
                alert('Share functionality will be implemented in the next update!');
            }
        };
    }
});
