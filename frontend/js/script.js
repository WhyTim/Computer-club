// Массив с информацией о доступных компьютерах в клубе (здесь можно добавить больше компьютеров)
const availableComputers = [
    { id: 1, name: 'Компьютер 1' },
    { id: 2, name: 'Компьютер 2' },
    { id: 3, name: 'Компьютер 3' },
    { id: 4, name: 'Компьютер 4' },
    { id: 5, name: 'Компьютер 5' },
    { id: 6, name: 'Компьютер 6' },
    { id: 7, name: 'Компьютер 7' },
    { id: 8, name: 'Компьютер 8' },
    { id: 9, name: 'Компьютер 9' },
    { id: 10, name: 'Компьютер 10' },
    // Добавьте остальные компьютеры по аналогии
];

// Функция для добавления карточек компьютеров в сетку
function populateComputerGrid() {
    const computerGrid = document.getElementById('computer-grid');
    computerGrid.innerHTML = ''; // Очистка сетки перед добавлением новых компьютеров

    let row;
    let count = 0;

    availableComputers.forEach(computer => {
        if (count % 5 === 0) {
            row = document.createElement('div');
            row.classList.add('row');
            computerGrid.appendChild(row);
        }

        const card = document.createElement('div');
        card.classList.add('card');
        card.dataset.computerId = computer.id;

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = 'computer-checkbox-' + computer.id;
        checkbox.classList.add('hidden-checkbox');
        checkbox.name = 'computers[]';
        checkbox.value = computer.id;

        const label = document.createElement('label');
        label.setAttribute('for', 'computer-checkbox-' + computer.id);
        label.textContent = computer.name;

        card.appendChild(checkbox);
        card.appendChild(label);

        row.appendChild(card);

        count++;
    });
}

// Вызов функции для заполнения сетки компьютеров при загрузке страницы
populateComputerGrid();

// Обработчик событий для клика на карточку компьютера
document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('click', function(event) {
        const checkbox = this.querySelector('.hidden-checkbox');
        checkbox.checked = !checkbox.checked; // Переключение состояния чекбокса
        this.classList.toggle('selected'); // Добавление или удаление класса "selected" для стилизации выбранной карточки

        // Подсчет количества выбранных компьютеров и отображение в поле
        const selectedCount = document.querySelectorAll('.card.selected').length;
        document.getElementById('total-computers').value = selectedCount;

        // Обновление списка выбранных компьютеров
        updateSelectedComputers();

        // Пересчет итоговой стоимости
        calculateTotalCost();

        // Остановка всплытия события клика, чтобы избежать переключения чекбокса при клике на текст карточки
        event.stopPropagation();
    });

    // Прикрепляем обработчик клика на чекбокс, чтобы он работал при клике на текст карточки
    card.querySelector('.hidden-checkbox').addEventListener('click', function(event) {
        event.stopPropagation(); // Остановка всплытия события клика, чтобы избежать переключения чекбокса при клике на сам чекбокс
    });
});

// Функция для обновления списка выбранных компьютеров
function updateSelectedComputers() {
    const selectedComputersDiv = document.getElementById('selected-computers');
    const selectedComputers = Array.from(document.querySelectorAll('.card.selected')).map(card => card.textContent);
    selectedComputersDiv.innerHTML = selectedComputers.length > 0 ? '<strong>Выбранные компьютеры:</strong><br>' + selectedComputers.map(computer => '<li>' + computer + '</li>').join('') : '';

}

// Функция для пересчета итоговой стоимости
function calculateTotalCost() {
    const selectedService = document.querySelector('select[name="service"]').value;
    const duration = parseInt(document.querySelector('input[name="duration"]').value);
    const selectedCount = parseInt(document.getElementById('total-computers').value);
    
    // Пример расчета: стоимость = цена услуги * продолжительность * количество компьютеров
    const pricePerHour = getServicePrice(selectedService);
    const totalPrice = pricePerHour * duration * selectedCount;

    // Отображение итоговой стоимости
    document.getElementById('total-cost').value = totalPrice.toFixed(2) == 'NaN' ? '0' : totalPrice.toFixed(2) + ' руб.';
}

// Функция для получения цены выбранной услуги
function getServicePrice(service) {
    // Здесь можно использовать базу данных или другой источник данных для получения цен
    const prices = {
        'basic': 100,
        'premium': 150,
        // Добавьте остальные услуги и их цены
    };
    return prices[service] || 0; // Если цена не найдена, возвращаем 0
}

// Обработчик событий для изменения продолжительности или выбора услуги
document.querySelectorAll('input[name="duration"], select[name="service"]').forEach(input => {
    input.addEventListener('change', function() {
        calculateTotalCost();
    });
});

// Вызываем функцию для инициализации списка выбранных компьютеров и итоговой стоимости
updateSelectedComputers();
calculateTotalCost();
