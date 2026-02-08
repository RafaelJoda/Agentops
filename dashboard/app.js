document.addEventListener('DOMContentLoaded', () => {
    fetchData();
});

let redditData = {};
let currentTab = 'n8n';

let dataChart = null;

async function fetchData() {
    try {
        // Fetch from the .tmp directory structure served by Python
        const response = await fetch('/.tmp/latest_reddit_posts.json');

        if (!response.ok) throw new Error('Failed to load data');

        redditData = await response.json();

        // Ensure default tabs exist in data just in case
        if (!redditData['n8n']) redditData['n8n'] = [];
        if (!redditData['automation']) redditData['automation'] = [];

        renderPosts(currentTab);
        renderChart(currentTab);

    } catch (error) {
        console.error('Error:', error);
        document.getElementById('content-area').innerHTML = `
            <div style="text-align: center; color: #ef4444; padding: 2rem;">
                <i data-lucide="alert-triangle" style="width: 48px; height: 48px; margin-bottom: 1rem;"></i>
                <p>Failed to load data. Make sure the scraper has run.</p>
                <p style="font-size: 0.8rem; opacity: 0.7;">Run "py execution/fetch_reddit_posts.py"</p>
            </div>
        `;
        lucide.createIcons();
    }
}

async function addTopicFromInput() {
    const input = document.getElementById('newTopicInput');
    const topic = input.value.trim().toLowerCase();

    if (!topic) return;

    // UI Feedback
    input.disabled = true;
    const originalPlaceholder = input.placeholder;
    input.placeholder = "Loading...";

    try {
        const response = await fetch(`/api/fetch_topic?name=${topic}`);
        if (!response.ok) throw new Error('API Error');

        const posts = await response.json();

        // Add to data
        redditData[topic] = posts;

        // Create Tab UI if doesn't exist
        const tabsContainer = document.getElementById('tabs-container');
        const existingBtn = Array.from(tabsContainer.children).find(btn => btn.innerText.toLowerCase().includes(topic));

        if (!existingBtn) {
            const btn = document.createElement('button');
            btn.className = 'tab-btn';
            btn.onclick = () => switchTab(topic);
            btn.innerHTML = `<i data-lucide="hash"></i> r/${topic}`;
            tabsContainer.appendChild(btn);
            lucide.createIcons();
        }

        // Switch to new tab
        switchTab(topic);

        input.value = '';

    } catch (error) {
        alert("Failed to fetch topic. Using cached data if available.");
    } finally {
        input.disabled = false;
        input.placeholder = originalPlaceholder;
        input.focus();
    }
}

function handleTopicKeypress(e) {
    if (e.key === 'Enter') addTopicFromInput();
}

function switchTab(tab) {
    currentTab = tab;

    // Update buttons
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));

    // Fix for the button active state visual update
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(b => {
        if (b.innerText.toLowerCase().includes(tab)) {
            b.classList.add('active');
        } else {
            b.classList.remove('active');
        }
    });

    // Clear search
    document.getElementById('searchInput').value = '';

    renderPosts(tab);
    renderChart(tab);
}

function handleSearch() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    renderPosts(currentTab, query);
}

function renderChart(subreddit) {
    const ctx = document.getElementById('engagementChart').getContext('2d');
    const posts = redditData[subreddit] || [];

    // Prepare data
    const labels = posts.map(p => p.title.substring(0, 20) + '...');
    const dataPoints = posts.map(p => p.engagement);

    // Colors based on subreddit
    const color = subreddit === 'n8n' ? '#ff6e40' : '#3b82f6';

    if (dataChart) {
        dataChart.destroy();
    }

    dataChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Engagement Score',
                data: dataPoints,
                backgroundColor: color,
                borderColor: color,
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                title: {
                    display: true,
                    text: `Top Engagement in r/${subreddit}`,
                    color: '#9ca3af',
                    font: { family: 'Inter', size: 14 }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#9ca3af' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#9ca3af' }
                }
            }
        }
    });
}

function renderPosts(subreddit, filter = '') {
    const container = document.getElementById('content-area');
    container.innerHTML = ''; // Clear current content

    let posts = redditData[subreddit] || [];

    // Filter logic
    if (filter) {
        posts = posts.filter(p => p.title.toLowerCase().includes(filter));
    }

    if (posts.length === 0) {
        container.innerHTML = '<p class="loading">No posts found matching criteria.</p>';
        return;
    }

    posts.forEach((post, index) => {
        const card = document.createElement('div');
        card.className = 'card';
        card.style.animationDelay = `${index * 0.1}s`;

        let imageHtml = '';
        if (post.thumbnail) {
            imageHtml = `<div class="card-image" style="background-image: url('${post.thumbnail}')"></div>`;
            card.classList.add('has-image');
        }

        card.innerHTML = `
            ${imageHtml}
            <div class="card-content">
                <div class="card-header">
                    <h3><a href="${post.url}" target="_blank">${post.title}</a></h3>
                    <div class="engagement-badge">
                        <i data-lucide="flame" style="width: 14px;"></i>
                        ${post.engagement}
                    </div>
                </div>
                
                <div class="stats">
                    <div class="stat-item score" title="Upvotes">
                        <i data-lucide="arrow-big-up" style="width: 16px;"></i>
                        ${post.score}
                    </div>
                    <div class="stat-item comments" title="Comments">
                        <i data-lucide="message-square" style="width: 16px;"></i>
                        ${post.comments}
                    </div>
                    <div class="date-badge">
                        ${post.created_utc}
                    </div>
                </div>
            </div>
        `;

        container.appendChild(card);
    });

    // Refresh icons
    lucide.createIcons();
}
