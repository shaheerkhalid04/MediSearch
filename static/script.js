document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('symptom-input');
    const autocompleteList = document.getElementById('autocomplete-list');
    const tagsContainer = document.getElementById('selected-symptoms');
    const searchBtn = document.getElementById('search-btn');
    const resultsContainer = document.getElementById('results-container');
    const resultsList = document.getElementById('results-list');
    const resultCount = document.getElementById('result-count');

    let selectedSymptoms = new Set();
    let debounceTimer;

    // --- Autocomplete Logic ---
    input.addEventListener('input', (e) => {
        clearTimeout(debounceTimer);
        const query = e.target.value.trim();
        
        if (!query) {
            autocompleteList.style.display = 'none';
            return;
        }

        debounceTimer = setTimeout(async () => {
            try {
                const res = await fetch(`/api/suggest?q=${encodeURIComponent(query)}`);
                const suggestions = await res.json();
                
                // Filter out already selected
                const available = suggestions.filter(s => !selectedSymptoms.has(s));
                
                renderAutocomplete(available);
            } catch (err) {
                console.error("Failed to fetch suggestions:", err);
            }
        }, 300);
    });

    function renderAutocomplete(suggestions) {
        autocompleteList.innerHTML = '';
        if (suggestions.length === 0) {
            autocompleteList.style.display = 'none';
            return;
        }

        suggestions.forEach(sym => {
            const div = document.createElement('div');
            div.className = 'autocomplete-item';
            div.textContent = sym.replace(/_/g, ' '); // Format nicely
            div.addEventListener('click', () => {
                addSymptom(sym);
                input.value = '';
                autocompleteList.style.display = 'none';
                input.focus();
            });
            autocompleteList.appendChild(div);
        });
        
        autocompleteList.style.display = 'block';
    }

    // Hide autocomplete when clicking outside
    document.addEventListener('click', (e) => {
        if (e.target !== input && e.target !== autocompleteList) {
            autocompleteList.style.display = 'none';
        }
    });

    // Handle Enter key
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            const firstItem = autocompleteList.querySelector('.autocomplete-item');
            if (firstItem) {
                firstItem.click();
            }
        }
    });

    // --- Tag Management ---
    function addSymptom(sym) {
        if (selectedSymptoms.has(sym)) return;
        
        // Remove empty state if present
        const emptyState = tagsContainer.querySelector('.empty-state');
        if (emptyState) {
            emptyState.remove();
        }

        selectedSymptoms.add(sym);
        
        const tag = document.createElement('div');
        tag.className = 'symptom-tag';
        tag.innerHTML = `
            ${sym.replace(/_/g, ' ')}
            <i class="ri-close-line remove-tag"></i>
        `;
        
        tag.querySelector('.remove-tag').addEventListener('click', () => {
            tag.remove();
            selectedSymptoms.delete(sym);
            updateSearchButton();
            
            if (selectedSymptoms.size === 0) {
                tagsContainer.innerHTML = '<p class="empty-state">No symptoms added yet. Type above to add.</p>';
            }
        });
        
        tagsContainer.appendChild(tag);
        updateSearchButton();
    }

    function updateSearchButton() {
        searchBtn.disabled = selectedSymptoms.size === 0;
    }

    // --- Search Logic ---
    searchBtn.addEventListener('click', async () => {
        if (selectedSymptoms.size === 0) return;
        
        const originalText = searchBtn.innerHTML;
        searchBtn.innerHTML = '<i class="ri-loader-4-line ri-spin"></i> Analyzing...';
        searchBtn.disabled = true;

        try {
            const res = await fetch('/api/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ symptoms: Array.from(selectedSymptoms) })
            });
            
            const results = await res.json();
            renderResults(results);
        } catch (err) {
            console.error("Search failed:", err);
            alert("An error occurred while searching. Please try again.");
        } finally {
            searchBtn.innerHTML = originalText;
            searchBtn.disabled = false;
        }
    });

    function renderResults(results) {
        resultsList.innerHTML = '';
        
        if (results.length === 0) {
            resultsList.innerHTML = '<div class="result-card"><p>No matching conditions found for these symptoms.</p></div>';
            resultCount.textContent = '0 found';
        } else {
            resultCount.textContent = `${results.length} found`;
            
            results.forEach((r, index) => {
                const card = document.createElement('div');
                card.className = 'result-card';
                card.style.animationDelay = `${index * 0.1}s`;
                
                const coveragePct = Math.round(r.coverage_ratio * 100);
                
                card.innerHTML = `
                    <div class="result-header">
                        <h3>${r.condition}</h3>
                        <div class="match-score">${coveragePct}% Match</div>
                    </div>
                    <p class="result-desc">${r.description || 'No description available.'}</p>
                    <div class="result-meta">
                        <span><i class="ri-check-double-line"></i> <strong>Matched:</strong> ${r.matched_symptoms.map(s => s.replace(/_/g, ' ')).join(', ')}</span>
                        <span><i class="ri-pie-chart-2-line"></i> <strong>Score:</strong> ${r.final_score}</span>
                    </div>
                `;
                resultsList.appendChild(card);
            });
        }
        
        resultsContainer.style.display = 'block';
        setTimeout(() => {
            resultsContainer.classList.add('show');
            resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 10);
    }
});
