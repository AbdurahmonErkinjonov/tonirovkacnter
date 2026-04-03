// Pul formatlash funksiyasi
function parseMoney(value) {
    if (!value) return 0;
    let cleaned = value.toString().replace(/\s/g, '');
    cleaned = cleaned.replace(',', '.');
    let num = parseFloat(cleaned);
    return isNaN(num) ? 0 : num;
}

function formatMoneyDisplay(value) {
    let num = parseMoney(value);
    if (num === 0) return '0';
    let formatted = Math.round(num * 1000);
    return formatted.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
}

function formatAllMoneyValues() {
    document.querySelectorAll('.money-value').forEach(el => {
        let value = parseFloat(el.dataset.value);
        if (!isNaN(value)) {
            if (value > 0) {
                let formatted = Math.round(value * 1000);
                el.innerHTML = formatted.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' so\'m';
            } else {
                el.innerHTML = '0 so\'m';
            }
        }
    });
}

// Inputlarni formatlash
document.addEventListener('DOMContentLoaded', function() {
    // Money value larni formatlash
    formatAllMoneyValues();
    
    // Money inputlarni formatlash
    const moneyInputs = document.querySelectorAll('.money-input');
    moneyInputs.forEach(input => {
        input.addEventListener('blur', function() {
            let num = parseMoney(this.value);
            if (num > 0) {
                this.value = formatMoneyDisplay(num);
            }
        });
        input.addEventListener('focus', function() {
            let num = parseMoney(this.value);
            if (num > 0) {
                this.value = num;
            }
        });
    });
});