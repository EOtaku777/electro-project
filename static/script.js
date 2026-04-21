let selectedEquipment = [];

async function calculate() {
    const power = document.getElementById('power').value;
    const response = await fetch('/api/calculate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({power_kw: parseFloat(power)})
    });
    const data = await response.json();
    document.getElementById('result').innerHTML = `
        <strong>Результат:</strong><br>
        Расчётный ток: ${data.current_a} А<br>
        Рекомендуемый автомат: ${data.recommended_breaker} А<br>
        ${data.message}
    `;
}

async function loadEquipment() {
    const response = await fetch('/api/equipment');
    const equipment = await response.json();
    const listDiv = document.getElementById('equipment-list');
    listDiv.innerHTML = '<h3>Выберите оборудование:</h3>';
    equipment.forEach(item => {
        listDiv.innerHTML += `
            <div class="equipment-item">
                ${item.name} - ${item.rated_current}А - ${item.price} руб.
                <button onclick="addToShield(${item.id})">+ Добавить</button>
            </div>
        `;
    });
}

function addToShield(id) {
    selectedEquipment.push({id, name: 'Автомат', quantity: 1});
    updateShieldDisplay();
}

function updateShieldDisplay() {
    const shieldDiv = document.getElementById('shield');
    shieldDiv.innerHTML = selectedEquipment.map((item, idx) => 
        `<div>${item.name} (${item.quantity} шт)</div>`
    ).join('');
}

function generateEstimate() {
    const total = selectedEquipment.length * 450; // примерная цена
    document.getElementById('estimate').innerHTML = `
СМЕТА
Оборудование: ${selectedEquipment.length} шт.
Итого: ${total} руб.
    `;
}

// Загружаем оборудование при старте
loadEquipment();