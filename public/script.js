// MAHIR Advanced Signal Generator - Client-Side Controller
// Professional Quotex Future Signal System

(function () {
    'use strict';

    // DOM Elements
    const elements = {
        timezone: document.getElementById('timezone'),
        timeframe: document.getElementById('timeframe'),
        martingale: document.getElementById('martingale'),

        btnSingle: document.getElementById('btn-single'),
        btnAllAssets: document.getElementById('btn-all-assets'),
        btnLive: document.getElementById('btn-live'),
        btnStop: document.getElementById('btn-stop'),
        btnExport: document.getElementById('btn-export'),
        btnClear: document.getElementById('btn-clear'),

        signalsContainer: document.getElementById('signals-container'),
        signalCount: document.getElementById('signal-count'),
        totalSignals: document.getElementById('total-signals'),
        avgConfidence: document.getElementById('avg-confidence'),
        totalAssets: document.getElementById('total-assets'),
        liveStatus: document.getElementById('live-status'),

        // Modal Elements
        historyModal: document.getElementById('history-modal'),
        closeModal: document.querySelector('.close-modal'),
        historyList: document.getElementById('history-list'),
        modalTitle: document.getElementById('modal-title')
    };

    // State Management
    const state = {
        signals: [],
        liveInterval: null,
        isLive: false,
        dailyCount: 0,
        dailyLimit: 20
    };

    // Initialize
    function init() {
        loadSettings();
        attachEventListeners();
        updateStats();
        checkAPIStatus();
    }

    // Load saved settings
    function loadSettings() {
        const saved = localStorage.getItem('mahir_settings');
        if (saved) {
            try {
                const settings = JSON.parse(saved);
                elements.timezone.value = settings.timezone || 6;
            } catch (e) {
                console.error('Failed to load settings:', e);
            }
        }
    }

    // Save settings
    function saveSettings() {
        const settings = {
            timezone: elements.timezone.value,
            timeframe: elements.timeframe.value,
            martingale: elements.martingale.value
        };
        localStorage.setItem('mahir_settings', JSON.stringify(settings));
    }

    // Event Listeners
    function attachEventListeners() {
        elements.btnSingle.addEventListener('click', generateSingleSignal);
        elements.btnAllAssets.addEventListener('click', scanAllAssets);
        elements.btnLive.addEventListener('click', startLiveMode);
        elements.btnStop.addEventListener('click', stopLiveMode);
        elements.btnExport.addEventListener('click', exportSignals);
        elements.btnClear.addEventListener('click', clearAllSignals);

        elements.timezone.addEventListener('change', saveSettings);

        // Modal Listeners
        if (elements.closeModal) {
            elements.closeModal.addEventListener('click', () => {
                elements.historyModal.style.display = 'none';
            });
        }

        window.addEventListener('click', (event) => {
            if (event.target === elements.historyModal) {
                elements.historyModal.style.display = 'none';
            }
        });
    }

    // API Functions
    async function fetchSignal(pair = null) {
        const tz = elements.timezone.value;
        const tf = elements.timeframe.value;

        const url = pair
            ? `/api/signal?pair=${pair}&timeframe=${tf}&tz=${tz}`
            : `/api/signal?pair=ALL&timeframe=${tf}&tz=${tz}`;

        try {
            const response = await fetch(url);
            const data = await response.json();

            // Update daily limits
            if (data.daily_count !== undefined) {
                state.dailyCount = data.daily_count;
                state.dailyLimit = data.daily_limit;
                updateDailyStats();
            }

            if (response.status === 429) {
                showToast(data.message, 'warning');
                return null;
            }

            if (!response.ok) {
                if (data.status === 'low_quality') {
                    showToast(data.message, 'warning');
                }
                return null;
            }

            return data;
        } catch (error) {
            console.error('Fetch error:', error);
            showToast('Failed to fetch signal. Please try again.', 'error');
            return null;
        }
    }

    async function fetchHistory(pair, count = 30, period = 60) {
        try {
            const response = await fetch(`/api/history?pair=${pair}&count=${count}&period=${period}`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('History fetch error:', error);
            return null;
        }
    }

    async function viewHistory(pair) {
        elements.historyModal.style.display = 'block';
        elements.modalTitle.textContent = `History: ${pair}`;
        elements.historyList.innerHTML = '<div style="text-align:center; padding: 20px;">Loading history...</div>';

        const historyData = await fetchHistory(pair);

        if (historyData && historyData.status === 'success' && historyData.data) {
            renderHistory(historyData.data);
        } else if (historyData && historyData.status === 'simulation') {
            renderHistory(historyData.data);
            showToast('Showing simulated history (API unavailable)', 'info');
        } else {
            elements.historyList.innerHTML = '<div style="text-align:center; padding: 20px; color: var(--accent-rose);">Failed to load history</div>';
        }
    }

    function renderHistory(candles) {
        if (!candles || candles.length === 0) {
            elements.historyList.innerHTML = '<div style="text-align:center; padding: 20px;">No history data available</div>';
            return;
        }

        const html = candles.map(candle => {
            const time = new Date(candle.time * 1000).toLocaleTimeString();
            const isUp = candle.close > candle.open;
            const colorClass = isUp ? 'price-up' : 'price-down';
            const icon = isUp ? '▲' : '▼';

            return `
                <div class="history-item">
                    <span class="history-time">${time}</span>
                    <span class="history-price ${colorClass}">
                        ${candle.close.toFixed(5)} ${icon}
                    </span>
                </div>
            `;
        }).join('');

        elements.historyList.innerHTML = html;
    }

    async function checkAPIStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            if (data.status === 'online') {
                elements.liveStatus.style.color = '#10b981';
                elements.totalAssets.textContent = '80+';
            }
        } catch (error) {
            elements.liveStatus.style.color = '#f43f5e';
        }
    }

    // Generate Single Signal
    async function generateSingleSignal() {
        setButtonLoading(elements.btnSingle, true);

        // Random asset selection
        const assets = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'EURUSD-OTC', 'GBPUSD-OTC', 'SHIBA_OTC', 'DOGE_OTC'];
        const randomAsset = assets[Math.floor(Math.random() * assets.length)];

        const data = await fetchSignal(randomAsset);

        if (data && data.status === 'success') {
            addSignal(data);
            showToast(`✅ Signal generated for ${data.pair}`, 'success');
        }

        setButtonLoading(elements.btnSingle, false);
        saveSettings();
    }

    // Scan All Assets
    async function scanAllAssets() {
        setButtonLoading(elements.btnAllAssets, true);
        showToast('🔍 Scanning all assets...', 'info');

        const data = await fetchSignal('ALL');

        if (data && data.status === 'success' && data.signals) {
            if (data.signals.length > 0) {
                data.signals.forEach(signal => addSignal(signal));
                showToast(`✅ Generated ${data.signals.length} signals!`, 'success');
            } else {
                showToast('No signals available right now.', 'warning');
            }
        }

        setButtonLoading(elements.btnAllAssets, false);
        saveSettings();
    }

    // Live Mode
    function startLiveMode() {
        if (state.isLive) return;

        state.isLive = true;
        elements.btnLive.disabled = true;
        elements.btnStop.disabled = false;
        elements.liveStatus.style.color = '#10b981';

        // Generate immediately
        generateSingleSignal();

        // Then every 30 seconds
        state.liveInterval = setInterval(() => {
            generateSingleSignal();
        }, 30000);

        showToast('▶️ Live mode activated! Generating signals every 30s', 'success');
    }

    function stopLiveMode() {
        if (!state.isLive) return;

        state.isLive = false;
        clearInterval(state.liveInterval);
        state.liveInterval = null;

        elements.btnLive.disabled = false;
        elements.btnStop.disabled = true;
        elements.liveStatus.style.color = '#fbbf24';

        showToast('⏸️ Live mode stopped', 'info');
    }

    // Add Signal to Display
    function addSignal(signalData) {
        const signal = {
            id: Date.now() + Math.random(),
            pair: signalData.pair,
            direction: signalData.dir,
            time: signalData.time,
            indicators: signalData.indicators || {},
            timestamp: Date.now()
        };

        state.signals.unshift(signal);

        if (state.signals.length > 100) {
            state.signals = state.signals.slice(0, 100);
        }

        renderSignals();
        updateStats();
    }

    // Render Signals
    function renderSignals() {
        if (state.signals.length === 0) {
            elements.signalsContainer.innerHTML = `
                <div style="text-align: center; padding: 40px; color: var(--text-muted);">
                    <p>No signals yet. Click "Generate Single Signal" or "Scan All Assets" to start.</p>
                </div>
            `;
            return;
        }

        elements.signalsContainer.innerHTML = state.signals.map(signal => `
            <div class="signal-card">
                <div class="signal-direction ${signal.direction.toLowerCase()}">
                    ${signal.direction}
                </div>
                <div class="signal-info">
                    <div class="signal-pair">${signal.pair}</div>
                    <div class="signal-time">⏰ ${signal.time} | ${formatTimestamp(signal.timestamp)}</div>
                </div>
                <div class="signal-indicators">
                    <button class="btn-history" onclick="window.MAHIR.viewHistory('${signal.pair}')">📊 History</button>
                    ${signal.indicators.rsi ? `<span class="indicator-badge">RSI: ${signal.indicators.rsi}</span>` : ''}
                    ${signal.indicators.macd ? `<span class="indicator-badge">MACD: ${signal.indicators.macd > 0 ? '+' : ''}${signal.indicators.macd}</span>` : ''}
                    ${signal.indicators.ema5 ? `<span class="indicator-badge">EMA5: ${signal.indicators.ema5}</span>` : ''}
                </div>
            </div>
        `).join('');
    }

    // Update Statistics
    function updateStats() {
        elements.signalCount.textContent = `${state.signals.length} signals`;
        elements.totalSignals.textContent = state.signals.length;
        updateDailyStats();
    }

    function updateDailyStats() {
        const remaining = state.dailyLimit - state.dailyCount;
        elements.avgConfidence.textContent = `${remaining}/${state.dailyLimit}`;
    }

    // Export Signals - EXACT FORMAT FROM PYTHON SCRIPT
    function exportSignals() {
        if (state.signals.length === 0) {
            showToast('No signals to export', 'warning');
            return;
        }

        const tz = elements.timezone.value;
        const sign = tz >= 0 ? '+' : '';
        const martingale = elements.martingale.value;

        // Get timezone emoji
        let tzEmoji = '';
        if (tz == 6) tzEmoji = '🇧🇩';
        else if (tz == 0) tzEmoji = 'UTC';
        else if (tz == 5) tzEmoji = '🇮🇳';
        else if (tz == -5) tzEmoji = '🇺🇸';

        let text = `◇──◇──◇──◇──◇──◇──◇\n\n`;
        text += `❈  UTC/GMT :   ( ${sign}${tz}:00 ) ${tzEmoji}\n`;
        text += `❈  ${martingale}STEP MARTINGALE\n`;
        text += `❈  1MINUTE TIMEFRAME\n\n`;
        text += `◇──◇──◇──◇──◇──◇──◇\n\n`;

        state.signals.forEach((signal) => {
            text += `⚙️${signal.pair}-${signal.time} - ${signal.direction}\n`;
        });

        text += `\n⛩ RULES -\n\n`;
        text += `✧ MUST BE USE SAFETY MARGIN\n`;
        text += `✧ BACK 2 BACK 2 LOSS SKIP MUST\n`;
        text += `✧ MTG (MARTINGALE) RECOMMENDED\n\n`;
        text += `━━━━━━━━━━━━━━━━━⍟\n\n`;
        text += `✧  X MAHIR SYSTEM  ✧\n\n`;
        text += `═══❰  OWNER  @LUX_DOT 💸 ❱══❍⊱\n`;

        navigator.clipboard.writeText(text).then(() => {
            showToast('✅ Signals copied to clipboard!', 'success');
            elements.btnExport.textContent = '✓ Copied!';
            setTimeout(() => {
                elements.btnExport.textContent = '📋 Copy Signals';
            }, 2000);
        }).catch(() => {
            // Fallback - show in alert
            alert(text);
        });
    }

    // Clear All Signals
    function clearAllSignals() {
        if (confirm('Are you sure you want to clear all signals?')) {
            state.signals = [];
            renderSignals();
            updateStats();
            showToast('All signals cleared', 'info');
        }
    }

    // Utility Functions
    function formatTimestamp(timestamp) {
        const now = Date.now();
        const diff = now - timestamp;
        const seconds = Math.floor(diff / 1000);
        const minutes = Math.floor(seconds / 60);

        if (minutes === 0) return 'Just now';
        if (minutes === 1) return '1 min ago';
        if (minutes < 60) return `${minutes} mins ago`;

        const hours = Math.floor(minutes / 60);
        if (hours === 1) return '1 hour ago';
        return `${hours} hours ago`;
    }

    function setButtonLoading(button, isLoading) {
        if (isLoading) {
            button.disabled = true;
            button.dataset.originalText = button.textContent;
            button.innerHTML = '<span class="loading"></span> Loading...';
        } else {
            button.disabled = false;
            button.textContent = button.dataset.originalText;
        }
    }

    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;

        const colors = {
            success: '#10b981',
            error: '#f43f5e',
            warning: '#fbbf24',
            info: '#3b82f6'
        };

        toast.style.borderLeft = `4px solid ${colors[type] || colors.info}`;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // Initialize on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    window.MAHIR = {
        state,
        generateSingleSignal,
        scanAllAssets,
        exportSignals,
        viewHistory,
        fetchHistory
    };

})();